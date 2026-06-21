#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from earnsai.backtest.adapter import (
    build_backtest_adapter_plan,
    build_backtest_adapter_report,
    validate_backtest_adapter_plan,
    write_all_backtest_adapter_reports,
)


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    plan = build_backtest_adapter_plan()
    valid, errors = validate_backtest_adapter_plan(plan)

    assert_true(valid, f"plan must be valid: {errors}")
    assert_true(plan.mode == "PAPER_ONLY", "plan mode must be PAPER_ONLY")
    assert_true(plan.live_trading_locked is True, "live trading must remain locked")
    assert_true(plan.private_exchange_api_used is False, "private exchange API must not be used")
    assert_true(plan.execution_enabled is False, "execution must remain disabled in Phase 8D")

    report = build_backtest_adapter_report()
    assert_true(report["ok"] is True, "backtest adapter report must be ok")
    assert_true(report["fixture_readiness"]["total_scenarios"] >= 4, "must evaluate fixture scenarios")
    assert_true(report["fixture_readiness"]["failed"] == 0, "fixture readiness must have zero failures")

    written = write_all_backtest_adapter_reports()
    assert_true(written["ok"] is True, "backtest adapter reports must be written successfully")

    json_path = ROOT / written["json_path"]
    markdown_path = ROOT / written["markdown_path"]

    assert_true(json_path.exists(), "json report must exist")
    assert_true(markdown_path.exists(), "markdown report must exist")

    parsed = json.loads(json_path.read_text(encoding="utf-8"))
    assert_true(parsed["plan"]["mode"] == "PAPER_ONLY", "json report mode must be PAPER_ONLY")
    assert_true(parsed["plan"]["execution_enabled"] is False, "json report execution must be disabled")

    print(
        "PHASE8D_SMOKE PASS "
        f"scenarios={report['fixture_readiness']['total_scenarios']} "
        f"passed={report['fixture_readiness']['passed']} "
        f"failed={report['fixture_readiness']['failed']} "
        f"json={written['json_path']} "
        f"md={written['markdown_path']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
