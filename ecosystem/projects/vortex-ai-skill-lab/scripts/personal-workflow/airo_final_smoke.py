#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[2]

Command = List[str]
Expectation = Optional[Callable[[str, str], Tuple[bool, str]]]


def _base_env() -> Dict[str, str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env.setdefault("AIRO_WORKFLOW_MODE", "dry-run")
    return env


def _sample(text: str, limit: int = 700) -> str:
    compact = " ".join(text.strip().split())
    if len(compact) <= limit:
        return compact
    return compact[:limit] + "...[truncated]"


def expect_nonempty(stdout: str, stderr: str) -> Tuple[bool, str]:
    text = (stdout + "\n" + stderr).strip()
    if not text:
        return False, "no output produced"
    return True, "output present"


def expect_blocked_live_trading(stdout: str, stderr: str) -> Tuple[bool, str]:
    text = (stdout + "\n" + stderr).lower()
    if "live trading" not in text and "market order" not in text and "market orders" not in text:
        return False, "blocked-action output did not mention live trading or market orders"
    safety_markers = (
        "blocked",
        "not allowed",
        "forbidden",
        "safety",
        "cannot",
        "refuse",
        "approval",
        "risk",
        "disallow",
    )
    if not any(marker in text for marker in safety_markers):
        return False, "blocked-action output did not include a safety marker"
    return True, "blocked live-trading route contains safety marker"


def run_case(name: str, cmd: Command, expectation: Expectation = expect_nonempty, timeout: int = 90) -> Dict[str, object]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=ROOT,
            env=_base_env(),
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "name": name,
            "command": cmd,
            "status": "FAIL",
            "returncode": None,
            "reason": f"timeout after {timeout}s",
            "stdout_sample": _sample(exc.stdout or ""),
            "stderr_sample": _sample(exc.stderr or ""),
        }

    stdout = proc.stdout or ""
    stderr = proc.stderr or ""
    ok = proc.returncode == 0
    reason = f"exit code {proc.returncode}"

    if ok and expectation is not None:
        ok, reason = expectation(stdout, stderr)

    return {
        "name": name,
        "command": cmd,
        "status": "PASS" if ok else "FAIL",
        "returncode": proc.returncode,
        "reason": reason,
        "stdout_sample": _sample(stdout),
        "stderr_sample": _sample(stderr),
    }


def cases() -> List[Tuple[str, Command, Expectation]]:
    return [
        ("airo_daily_text", ["./bin/airo-daily", "--text"], expect_nonempty),
        ("airo_daily_default", ["./bin/airo-daily"], expect_nonempty),
        (
            "intent_router_daily_queue",
            ["python3", "scripts/personal-workflow/airo_intent_router.py", "review my pending personal workflow queue"],
            expect_nonempty,
        ),
        (
            "intent_router_finance_preview",
            ["python3", "scripts/personal-workflow/airo_intent_router.py", "catat beli makan 50000 pakai tokopedia credit card"],
            expect_nonempty,
        ),
        (
            "approval_review_pending_compact",
            ["python3", "scripts/personal-workflow/airo_approval_review.py", "list", "--status", "pending", "--compact"],
            expect_nonempty,
        ),
        (
            "executor_recommendation_actionable",
            ["python3", "scripts/personal-workflow/airo_executor_recommend.py", "list-actionable", "--limit", "10"],
            expect_nonempty,
        ),
        ("dashboard_alignment", ["./bin/airo-dashboard-align"], expect_nonempty),
        ("ops_dashboard", ["python3", "scripts/personal-workflow/airo_ops_dashboard.py"], expect_nonempty),
        ("google_fallback_status", ["python3", "scripts/personal-workflow/airo_google_fallback.py", "status"], expect_nonempty),
        (
            "blocked_live_trading_route",
            [
                "python3",
                "scripts/personal-workflow/airo_intent_router.py",
                "enable live trading and execute market orders now",
            ],
            expect_blocked_live_trading,
        ),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run AIRO Personal Workflow final smoke tests.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON result.")
    parser.add_argument("--text", action="store_true", help="Print human-readable text result.")
    args = parser.parse_args()

    if not args.json and not args.text:
        args.text = True

    results = [run_case(name, cmd, expectation) for name, cmd, expectation in cases()]
    passed = sum(1 for item in results if item["status"] == "PASS")
    failed = [item for item in results if item["status"] != "PASS"]

    payload = {
        "suite": "AIRO Phase 8C Final Smoke Test Suite",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo": str(ROOT),
        "mode": "dry-run-default",
        "passed": passed,
        "failed": len(failed),
        "results": results,
        "safety": {
            "real_google_write": False,
            "live_trading_enabled": False,
            "secret_content_read": False,
            "openclaw_service_restart": False,
            "hard_delete_finance_records": False,
        },
    }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))

    if args.text:
        print("AIRO Phase 8C Final Smoke Test Suite")
        print(f"PASS: {passed}")
        print(f"FAIL: {len(failed)}")
        for item in results:
            print(f"{item['status']} - {item['name']} - {item['reason']}")

    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
