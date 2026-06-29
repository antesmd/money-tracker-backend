#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import httpx

from fuzz.auth import AuthClient
from fuzz.engine import FuzzEngine, build_config, load_payloads, load_yaml
from fuzz.reporter import FuzzReport


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Reproducible API fuzzing for money-tracker backend",
    )
    parser.add_argument(
        "--config",
        default="fuzz/config.yaml",
        help="Path to fuzz config YAML (default: fuzz/config.yaml)",
    )
    parser.add_argument(
        "--endpoints",
        default="fuzz/endpoints.yaml",
        help="Path to endpoints catalog YAML (default: fuzz/endpoints.yaml)",
    )
    parser.add_argument(
        "--payload-dir",
        default="fuzz/payloads",
        help="Directory with payload wordlists (default: fuzz/payloads)",
    )
    parser.add_argument(
        "--include-passed",
        action="store_true",
        help="Include expected_rejection/baseline findings in report",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate config and print planned coverage without sending requests",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = PROJECT_ROOT
    config_path = (project_root / args.config).resolve()
    endpoints_path = (project_root / args.endpoints).resolve()
    payload_dir = (project_root / args.payload_dir).resolve()

    if not config_path.exists():
        print(f"Config not found: {config_path}", file=sys.stderr)
        return 1
    if not endpoints_path.exists():
        print(f"Endpoints catalog not found: {endpoints_path}", file=sys.stderr)
        return 1

    raw_config = load_yaml(config_path)
    config = build_config(raw_config, config_path=config_path, project_root=project_root)
    if args.include_passed:
        config.include_passed = True

    endpoints = load_yaml(endpoints_path)["endpoints"]
    payloads = load_payloads(payload_dir, config.payload_sets)

    print(f"Target: {config.base_url}")
    print(f"Endpoints: {len(endpoints)}")
    print(f"Payload sets: {', '.join(config.payload_sets)}")
    total_payloads = sum(len(values) for values in payloads.values())
    print(f"Total payload values: {total_payloads}")

    if args.dry_run:
        for endpoint in endpoints:
            print(f"  - {endpoint['method']} {endpoint['path']} [{endpoint['id']}]")
        return 0

    auth_settings = raw_config["auth"]
    report = FuzzReport(
        target=config.base_url,
        config_path=str(config_path.relative_to(project_root)),
        endpoints_path=str(endpoints_path.relative_to(project_root)),
        payload_sets=config.payload_sets,
    )

    with httpx.Client(follow_redirects=False) as client:
        auth_client = AuthClient(
            client=client,
            base_url=config.base_url,
            password=auth_settings["password"],
            username_prefix=auth_settings["username_prefix"],
        )

        try:
            health = client.get(f"{config.base_url.rstrip('/')}/openapi.json", timeout=config.timeout_seconds)
            health.raise_for_status()
        except httpx.HTTPError as exc:
            print(
                f"Cannot reach API at {config.base_url}. Start the server first.\nError: {exc}",
                file=sys.stderr,
            )
            return 2

        try:
            if auth_settings.get("use_existing_user") and auth_settings.get("email"):
                session = auth_client.login_existing(auth_settings["email"], auth_settings["password"])
                print(f"Using existing user: {session.email}")
            else:
                session = auth_client.create_session(
                    email=auth_settings.get("email") or "",
                    password=auth_settings.get("password") or "",
                )
                print(f"Created fuzz user: {session.email}")
        except httpx.HTTPError as exc:
            print(f"Failed to prepare authenticated session: {exc}", file=sys.stderr)
            return 3

        engine = FuzzEngine(
            client=client,
            config=config,
            endpoints=endpoints,
            payloads=payloads,
            auth_client=auth_client,
            report=report,
        )
        engine.run(session)

    report_path = report.write(config.output_dir)
    summary = report.to_dict()["summary"]
    findings = summary["findings_by_severity"]

    print()
    print("Fuzz run completed")
    print(f"  Requests: {summary['total_requests']}")
    print(f"  Endpoints: {summary['endpoints_tested']}")
    print(
        "  Findings: "
        f"critical={findings['critical']} "
        f"high={findings['high']} "
        f"medium={findings['medium']} "
        f"low={findings['low']} "
        f"info={findings['info']}",
    )
    print(f"  Report: {report_path}")
    print(f"  Latest: {config.output_dir / 'latest.json'}")

    if findings["critical"] > 0 or findings["high"] > 0:
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
