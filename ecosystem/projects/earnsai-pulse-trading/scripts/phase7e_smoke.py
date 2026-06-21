#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from earnsai.agents.orchestrator import run_multi_agent_cycle
from earnsai.evaluation.reporter import generate_markdown_report, summarize_journal
from earnsai.telegram.handlers import handle_command, run_safe_cycle_if_not_paused


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    run_multi_agent_cycle()

    allowed = ["/help", "/status", "/signal", "/risk", "/journal", "/pause", "/resume", "/lock_live"]
    for command in allowed:
        response = handle_command(command)
        assert_true(response.get("ok") is True, f"{command} should be allowed")
        assert_true("message" in response, f"{command} must return message")

    blocked = ["/buy", "/sell", "/live_on", "/show_env", "/set_secret", "/unlock_live"]
    for command in blocked:
        response = handle_command(command)
        assert_true(response.get("ok") is False, f"{command} must not be ok")
        assert_true(response.get("blocked") is True, f"{command} must be blocked")

    handle_command("/pause")
    paused_cycle = run_safe_cycle_if_not_paused()
    assert_true(paused_cycle.get("skipped") is True, "paused cycle must be skipped")

    handle_command("/resume")
    resumed_cycle = run_safe_cycle_if_not_paused()
    assert_true(resumed_cycle.get("ok") is True, "resumed cycle must run")

    handle_command("/lock_live")
    status = handle_command("/status")
    assert_true(status.get("bridge", {}).get("live_trading_locked") is True, "live trading must remain locked")

    summary = summarize_journal(limit=50)
    assert_true(summary["rows"] >= 1, "journal summary must see rows")
    assert_true(summary["latest"].get("mode") == "PAPER_ONLY", "latest mode must be PAPER_ONLY")
    assert_true(summary["latest"].get("live_trading_locked") is True, "latest must keep live trading locked")

    report = generate_markdown_report()
    report_path = ROOT / report["path"]
    assert_true(report_path.exists(), "report file must be generated")

    print(
        "PHASE7E_SMOKE PASS "
        f"allowed={len(allowed)} "
        f"blocked={len(blocked)} "
        f"journal_rows={summary['rows']} "
        f"report={report['path']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
