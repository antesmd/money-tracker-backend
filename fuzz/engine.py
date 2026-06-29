from __future__ import annotations

import copy
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx
import yaml

from fuzz.auth import AuthClient, AuthSession
from fuzz.reporter import EndpointCoverage, FuzzFinding, FuzzReport


@dataclass
class FuzzConfig:
    base_url: str
    timeout_seconds: float
    max_response_body_chars: int
    payload_sets: list[str]
    include_json_mutations: bool
    include_path_params: bool
    include_query_params: bool
    delay_ms: int
    rejection_statuses: set[int]
    success_statuses: set[int]
    include_passed: bool
    body_preview_chars: int
    output_dir: Path


JSON_MUTATIONS: list[tuple[str, str | bytes | dict[str, Any]]] = [
    ("empty_object", {}),
    ("empty_array", []),
    ("null_body", "null"),
    ("invalid_json", b"{not-json"),
    ("extra_field", {"__proto__": {"admin": True}, "injected": True}),
    ("numeric_string", "12345"),
]


class FuzzEngine:
    def __init__(
        self,
        *,
        client: httpx.Client,
        config: FuzzConfig,
        endpoints: list[dict[str, Any]],
        payloads: dict[str, list[str]],
        auth_client: AuthClient,
        report: FuzzReport,
    ) -> None:
        self._client = client
        self._config = config
        self._endpoints = endpoints
        self._payloads = payloads
        self._auth_client = auth_client
        self._report = report
        self._coverage_map: dict[str, EndpointCoverage] = {}

    def run(self, session: AuthSession) -> FuzzReport:
        context = self._auth_client.template_context(session)
        for endpoint in self._endpoints:
            coverage = EndpointCoverage(
                endpoint_id=endpoint["id"],
                method=endpoint["method"],
                path=endpoint["path"],
            )
            self._coverage_map[endpoint["id"]] = coverage

            self._fuzz_endpoint(endpoint, session, context, coverage)

            if self._config.include_json_mutations and endpoint.get("body") is not None:
                self._fuzz_json_mutations(endpoint, session, context, coverage)

        self._report.coverage = list(self._coverage_map.values())
        self._report.finish()
        return self._report

    def _fuzz_endpoint(
        self,
        endpoint: dict[str, Any],
        session: AuthSession,
        context: dict[str, str],
        coverage: EndpointCoverage,
    ) -> None:
        baseline = self._send_request(endpoint, session, context)
        self._record_baseline(endpoint, baseline, coverage)

        for category, values in self._payloads.items():
            for field_name in endpoint.get("fuzz_fields", []):
                for payload in values:
                    mutated_body = copy.deepcopy(endpoint.get("body", {}))
                    mutated_body[field_name] = payload
                    self._send_fuzz(
                        endpoint=endpoint,
                        session=session,
                        context=context,
                        coverage=coverage,
                        payload_category=category,
                        payload=payload,
                        target_field=field_name,
                        body=mutated_body,
                    )

            if self._config.include_path_params:
                for field_name in endpoint.get("fuzz_path_params", []):
                    for payload in values:
                        path_params = copy.deepcopy(endpoint.get("path_params", {}))
                        path_params[field_name] = payload
                        self._send_fuzz(
                            endpoint=endpoint,
                            session=session,
                            context=context,
                            coverage=coverage,
                            payload_category=category,
                            payload=payload,
                            target_field=f"path:{field_name}",
                            path_params=path_params,
                        )

            if self._config.include_query_params:
                for field_name in endpoint.get("fuzz_query_params", []):
                    for payload in values:
                        query_params = copy.deepcopy(endpoint.get("query_params", {}))
                        query_params[field_name] = payload
                        self._send_fuzz(
                            endpoint=endpoint,
                            session=session,
                            context=context,
                            coverage=coverage,
                            payload_category=category,
                            payload=payload,
                            target_field=f"query:{field_name}",
                            query_params=query_params,
                        )

        for field_name in endpoint.get("fuzz_cookies", []):
            for category, values in self._payloads.items():
                for payload in values:
                    cookies = httpx.Cookies()
                    cookies.set(field_name, payload)
                    try:
                        self._send_fuzz(
                            endpoint=endpoint,
                            session=session,
                            context=context,
                            coverage=coverage,
                            payload_category=category,
                            payload=payload,
                            target_field=f"cookie:{field_name}",
                            override_cookies=cookies,
                        )
                    except Exception as e:
                        print(f"Error occurred while sending fuzz request for cookie {field_name}: {e}")

    def _fuzz_json_mutations(
        self,
        endpoint: dict[str, Any],
        session: AuthSession,
        context: dict[str, str],
        coverage: EndpointCoverage,
    ) -> None:
        for mutation_name, body in JSON_MUTATIONS:
            self._send_fuzz(
                endpoint=endpoint,
                session=session,
                context=context,
                coverage=coverage,
                payload_category="json_mutation",
                payload=mutation_name,
                target_field="body",
                raw_body=body,
            )

    def _record_baseline(
        self,
        endpoint: dict[str, Any],
        result: dict[str, Any],
        coverage: EndpointCoverage,
    ) -> None:
        coverage.requests_sent += 1
        self._report.total_requests += 1
        self._report.record_status(result["status_code"])
        finding = self._classify(
            endpoint=endpoint,
            payload_category="baseline",
            payload="baseline",
            target_field=None,
            result=result,
        )
        self._report.add_finding(finding, include_passed=self._config.include_passed)

    def _send_fuzz(
        self,
        *,
        endpoint: dict[str, Any],
        session: AuthSession,
        context: dict[str, str],
        coverage: EndpointCoverage,
        payload_category: str,
        payload: str,
        target_field: str | None,
        body: dict[str, Any] | None = None,
        path_params: dict[str, Any] | None = None,
        query_params: dict[str, Any] | None = None,
        raw_body: str | bytes | dict[str, Any] | list[Any] | None = None,
        override_cookies: httpx.Cookies | None = None,
    ) -> None:
        result = self._send_request(
            endpoint,
            session,
            context,
            body=body,
            path_params=path_params,
            query_params=query_params,
            raw_body=raw_body,
            override_cookies=override_cookies,
        )
        coverage.requests_sent += 1
        self._report.total_requests += 1
        self._report.record_status(result["status_code"])

        finding = self._classify(
            endpoint=endpoint,
            payload_category=payload_category,
            payload=payload,
            target_field=target_field,
            result=result,
        )
        self._report.add_finding(finding, include_passed=self._config.include_passed)

        if self._config.delay_ms > 0:
            time.sleep(self._config.delay_ms / 1000)

    def _send_request(
        self,
        endpoint: dict[str, Any],
        session: AuthSession,
        context: dict[str, str],
        *,
        body: dict[str, Any] | None = None,
        path_params: dict[str, Any] | None = None,
        query_params: dict[str, Any] | None = None,
        raw_body: str | bytes | dict[str, Any] | list[Any] | None = None,
        override_cookies: httpx.Cookies | None = None,
    ) -> dict[str, Any]:
        resolved_path_params = self._auth_client.resolve_placeholders(
            path_params or endpoint.get("path_params", {}),
            context,
        )
        resolved_query = self._auth_client.resolve_placeholders(
            query_params or endpoint.get("query_params"),
            context,
        )
        path = endpoint["path"]
        for key, value in resolved_path_params.items():
            path = path.replace(f"{{{key}}}", str(value))

        url = f"{self._config.base_url.rstrip('/')}{path}"
        cookies = override_cookies or self._auth_client.cookies_for(endpoint.get("auth", "none"), session)

        request_kwargs: dict[str, Any] = {
            "method": endpoint["method"],
            "url": url,
            "cookies": cookies,
            "timeout": self._config.timeout_seconds,
        }
        if resolved_query:
            request_kwargs["params"] = resolved_query

        request_body_preview: str | None = None
        if raw_body is not None:
            if isinstance(raw_body, (dict, list)):
                request_kwargs["json"] = raw_body
                request_body_preview = json.dumps(raw_body)[: self._config.body_preview_chars]
            elif isinstance(raw_body, bytes):
                request_kwargs["content"] = raw_body
                request_body_preview = raw_body.decode("utf-8", errors="replace")[
                    : self._config.body_preview_chars
                ]
            else:
                request_kwargs["content"] = raw_body
                request_body_preview = str(raw_body)[: self._config.body_preview_chars]
        elif body is not None or endpoint.get("body") is not None:
            resolved_body = self._auth_client.resolve_placeholders(body or endpoint.get("body"), context)
            request_kwargs["json"] = resolved_body
            request_body_preview = json.dumps(resolved_body)[: self._config.body_preview_chars]

        started = time.perf_counter()
        try:
            response = self._client.request(**request_kwargs)
            elapsed_ms = (time.perf_counter() - started) * 1000
            body_text = response.text[: self._config.max_response_body_chars]
            return {
                "url": url,
                "status_code": response.status_code,
                "elapsed_ms": elapsed_ms,
                "body_preview": body_text[: self._config.body_preview_chars],
                "request_body_preview": request_body_preview,
                "timeout": False,
            }
        except httpx.TimeoutException:
            elapsed_ms = (time.perf_counter() - started) * 1000
            return {
                "url": url,
                "status_code": 0,
                "elapsed_ms": elapsed_ms,
                "body_preview": None,
                "request_body_preview": request_body_preview,
                "timeout": True,
            }

    def _classify(
        self,
        *,
        endpoint: dict[str, Any],
        payload_category: str,
        payload: str,
        target_field: str | None,
        result: dict[str, Any],
    ) -> FuzzFinding:
        status_code = result["status_code"]
        body_preview = result.get("body_preview") or ""
        auth_mode = endpoint.get("auth", "none")

        if result.get("timeout"):
            return FuzzFinding(
                endpoint_id=endpoint["id"],
                method=endpoint["method"],
                path=endpoint["path"],
                payload_category=payload_category,
                payload=payload,
                status_code=0,
                elapsed_ms=result["elapsed_ms"],
                classification="timeout",
                severity="medium",
                target_field=target_field,
                url=result["url"],
                request_body_preview=result.get("request_body_preview"),
                response_body_preview=None,
                notes="Request exceeded configured timeout",
            )

        if 500 <= status_code <= 599:
            return FuzzFinding(
                endpoint_id=endpoint["id"],
                method=endpoint["method"],
                path=endpoint["path"],
                payload_category=payload_category,
                payload=payload,
                status_code=status_code,
                elapsed_ms=result["elapsed_ms"],
                classification="server_error",
                severity="critical",
                target_field=target_field,
                url=result["url"],
                request_body_preview=result.get("request_body_preview"),
                response_body_preview=body_preview,
                notes="Server returned 5xx on fuzz input",
            )

        if auth_mode in {"access", "refresh"} and status_code in self._config.success_statuses:
            if payload_category != "baseline" and payload not in {"", "baseline"}:
                return FuzzFinding(
                    endpoint_id=endpoint["id"],
                    method=endpoint["method"],
                    path=endpoint["path"],
                    payload_category=payload_category,
                    payload=payload,
                    status_code=status_code,
                    elapsed_ms=result["elapsed_ms"],
                    classification="unexpected_success",
                    severity="high",
                    target_field=target_field,
                    url=result["url"],
                    request_body_preview=result.get("request_body_preview"),
                    response_body_preview=body_preview,
                    notes="Authenticated endpoint accepted fuzz payload with success status",
                )

        if payload_category in {"xss", "sql_injection"} and payload in body_preview:
            return FuzzFinding(
                endpoint_id=endpoint["id"],
                method=endpoint["method"],
                path=endpoint["path"],
                payload_category=payload_category,
                payload=payload,
                status_code=status_code,
                elapsed_ms=result["elapsed_ms"],
                classification="payload_reflected",
                severity="high",
                target_field=target_field,
                url=result["url"],
                request_body_preview=result.get("request_body_preview"),
                response_body_preview=body_preview,
                notes="Payload appears reflected in response body",
            )

        if auth_mode == "none" and endpoint["id"] != "identity.login" and status_code in self._config.success_statuses:
            if payload_category not in {"baseline", "common"} and payload not in {"baseline"}:
                return FuzzFinding(
                    endpoint_id=endpoint["id"],
                    method=endpoint["method"],
                    path=endpoint["path"],
                    payload_category=payload_category,
                    payload=payload,
                    status_code=status_code,
                    elapsed_ms=result["elapsed_ms"],
                    classification="unexpected_success",
                    severity="low",
                    target_field=target_field,
                    url=result["url"],
                    request_body_preview=result.get("request_body_preview"),
                    response_body_preview=body_preview,
                    notes="Unauthenticated endpoint returned success for fuzz input",
                )

        if status_code in self._config.rejection_statuses or payload_category == "baseline":
            return FuzzFinding(
                endpoint_id=endpoint["id"],
                method=endpoint["method"],
                path=endpoint["path"],
                payload_category=payload_category,
                payload=payload,
                status_code=status_code,
                elapsed_ms=result["elapsed_ms"],
                classification="expected_rejection" if payload_category != "baseline" else "baseline",
                severity="info",
                target_field=target_field,
                url=result["url"],
                request_body_preview=result.get("request_body_preview"),
                response_body_preview=body_preview,
            )

        return FuzzFinding(
            endpoint_id=endpoint["id"],
            method=endpoint["method"],
            path=endpoint["path"],
            payload_category=payload_category,
            payload=payload,
            status_code=status_code,
            elapsed_ms=result["elapsed_ms"],
            classification="anomaly",
            severity="medium",
            target_field=target_field,
            url=result["url"],
            request_body_preview=result.get("request_body_preview"),
            response_body_preview=body_preview,
            notes="Response status did not match expected rejection/success patterns",
        )


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_payloads(payload_dir: Path, payload_sets: list[str]) -> dict[str, list[str]]:
    payloads: dict[str, list[str]] = {}
    for name in payload_sets:
        file_path = payload_dir / f"{name}.txt"
        if not file_path.exists():
            msg = f"Payload set not found: {file_path}"
            raise FileNotFoundError(msg)
        lines = [
            line.strip()
            for line in file_path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        payloads[name] = lines
    return payloads


def build_config(raw: dict[str, Any], *, config_path: Path, project_root: Path) -> FuzzConfig:
    target = raw["target"]
    report = raw["report"]
    fuzz = raw["fuzz"]
    expected = raw["expected_status"]
    output_dir = project_root / report["output_dir"]

    return FuzzConfig(
        base_url=target["base_url"],
        timeout_seconds=float(target["timeout_seconds"]),
        max_response_body_chars=int(target["max_response_body_chars"]),
        payload_sets=list(fuzz["payload_sets"]),
        include_json_mutations=bool(fuzz["include_json_mutations"]),
        include_path_params=bool(fuzz["include_path_params"]),
        include_query_params=bool(fuzz["include_query_params"]),
        delay_ms=int(fuzz["delay_ms"]),
        rejection_statuses=set(expected["rejection"]),
        success_statuses=set(expected["success"]),
        include_passed=bool(report["include_passed"]),
        body_preview_chars=int(report["body_preview_chars"]),
        output_dir=output_dir,
    )
