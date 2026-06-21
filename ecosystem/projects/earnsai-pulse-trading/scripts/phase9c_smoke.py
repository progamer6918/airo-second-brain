#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from earnsai.agents.orchestrator import run_multi_agent_cycle
from earnsai.evaluation.compact_report import build_compact_status, write_all_compact_reports


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    run_multi_agent_cycle()

    status = build_compact_status(limit=500)

    assert_true(status["mode"] == "PAPER_ONLY", "mode must remain PAPER_ONLY")
    assert_true(status["live_trading_locked"] is True, "live trading must remain locked")
    assert_true(status["safety_ok"] is True, "compact report safety must be true")
    assert_true(status["bridge"]["signals_match"] is True, "bridge signals must match")
    assert_true(status["fixtures"]["failed"] == 0, "fixtures must have zero failed cases")
    assert_true(status["backtest_adapter"]["execution_enabled"] is False, "backtest execution must stay disabled")
    assert_true(status["backtest_adapter"]["private_exchange_api_used"] is False, "private exchange API must not be used")
    assert_true(status["stability"]["ok"] is True, "stability must be ok")

    reports = write_all_compact_reports(limit=500)

    assert_true(reports["ok"] is True, "compact reports must be ok")

    json_path = ROOT / reports["json_path"]
    markdown_path = ROOT / reports["markdown_path"]

    assert_true(json_path.exists(), "compact json report must exist")
    assert_true(markdown_path.exists(), "compact markdown report must exist")

    parsed = json.loads(json_path.read_text(encoding="utf-8"))
    assert_true(parsed["safety_ok"] is True, "compact json safety must be true")

    print(
        "PHASE9C_SMOKE PASS "
        f"safety_ok={reports['safety_ok']} "
        f"latest={reports['latest_action']} "
        f"risk={reports['latest_risk_status']} "
        f"json={reports['json_path']} "
        f"md={reports['markdown_path']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
