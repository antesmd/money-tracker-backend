from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass
class FuzzFinding:
    endpoint_id: str
    method: str
    path: str
    payload_category: str
    payload: str
    status_code: int
    elapsed_ms: float
    classification: str
    severity: str
    target_field: str | None = None
    url: str = ""
    request_body_preview: str | None = None
    response_body_preview: str | None = None
    notes: str = ""

    @property
    def finding_id(self) -> str:
        return str(uuid.uuid5(uuid.NAMESPACE_URL, f"{self.endpoint_id}:{self.target_field}:{self.payload}"))


@dataclass
class EndpointCoverage:
    endpoint_id: str
    method: str
    path: str
    requests_sent: int = 0


@dataclass
class FuzzReport:
    run_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    started_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))
    finished_at: datetime | None = None
    target: str = ""
    config_path: str = ""
    endpoints_path: str = ""
    payload_sets: list[str] = field(default_factory=list)
    findings: list[FuzzFinding] = field(default_factory=list)
    coverage: list[EndpointCoverage] = field(default_factory=list)
    total_requests: int = 0
    responses_by_status: dict[str, int] = field(default_factory=dict)

    def record_status(self, status_code: int) -> None:
        key = str(status_code)
        self.responses_by_status[key] = self.responses_by_status.get(key, 0) + 1

    def add_finding(self, finding: FuzzFinding, *, include_passed: bool) -> None:
        if finding.severity == "info" and not include_passed:
            return
        self.findings.append(finding)

    def finish(self) -> None:
        self.finished_at = datetime.now(tz=UTC)

    def to_dict(self) -> dict[str, Any]:
        finished = self.finished_at or datetime.now(tz=UTC)
        duration = (finished - self.started_at).total_seconds()
        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
        for finding in self.findings:
            severity_counts[finding.severity] = severity_counts.get(finding.severity, 0) + 1

        return {
            "metadata": {
                "schema_version": "1.0",
                "run_id": self.run_id,
                "started_at": self.started_at.isoformat(),
                "finished_at": finished.isoformat(),
                "duration_seconds": round(duration, 3),
                "target": self.target,
                "config_path": self.config_path,
                "endpoints_path": self.endpoints_path,
                "payload_sets": self.payload_sets,
            },
            "summary": {
                "total_requests": self.total_requests,
                "endpoints_tested": len(self.coverage),
                "findings_by_severity": severity_counts,
                "responses_by_status": self.responses_by_status,
            },
            "coverage": [
                {
                    "endpoint_id": item.endpoint_id,
                    "method": item.method,
                    "path": item.path,
                    "requests_sent": item.requests_sent,
                }
                for item in self.coverage
            ],
            "findings": [
                {
                    "id": item.finding_id,
                    "severity": item.severity,
                    "classification": item.classification,
                    "endpoint_id": item.endpoint_id,
                    "method": item.method,
                    "path": item.path,
                    "target_field": item.target_field,
                    "payload_category": item.payload_category,
                    "payload": item.payload,
                    "request": {
                        "url": item.url,
                        "body_preview": item.request_body_preview,
                    },
                    "response": {
                        "status_code": item.status_code,
                        "elapsed_ms": round(item.elapsed_ms, 2),
                        "body_preview": item.response_body_preview,
                    },
                    "notes": item.notes,
                }
                for item in self.findings
            ],
        }

    def write(self, output_dir: Path) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = self.started_at.strftime("%Y%m%dT%H%M%SZ")
        report_path = output_dir / f"fuzz_{timestamp}_{self.run_id[:8]}.json"
        report_path.write_text(
            json.dumps(self.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        latest_path = output_dir / "latest.json"
        latest_path.write_text(report_path.read_text(encoding="utf-8"), encoding="utf-8")
        return report_path
