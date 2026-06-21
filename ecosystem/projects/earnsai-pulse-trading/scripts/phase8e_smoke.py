#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from earnsai.agents.orchestrator import run_multi_agent_cycle
from earnsai.telegram.handlers import handle_command


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    run_multi_agent_cycle()

    allowed = ["/help", "/status", "/signal", "/risk", "/journal", "/health", "/metrics", "/report", "/pause", "/resume", "/lock_live"]
    for command in allowed:
        response = handle_command(command)
        assert_true(response.get("ok") is True, f"{command} should be allowed")
        assert_true("message" in response, f"{command} must return message")

    health = handle_command("/health")
    assert_true(health["health"]["mode"] == "PAPER_ONLY", "health mode must be PAPER_ONLY")
    assert_true(health["health"]["live_trading_locked"] is True, "health live lock must be true")
    assert_true(health["health"]["bridge_signals_match"] is True, "health bridge signals must match")

    metrics = handle_command("/metrics")
    assert_true(metrics["metrics"]["safety_ok"] is True, "metrics safety must be true")
    assert_true(Path(metrics["metrics"]["report_path"]).exists(), "metrics report must exist")

    report = handle_command("/report")
    assert_true(report["report"]["summary"]["metrics_safety_ok"] is True, "report metrics safety must be true")
    assert_true(report["report"]["summary"]["fixtures_ok"] is True, "report fixtures must be true")
    assert_true(report["report"]["summary"]["backtest_plan_ok"] is True, "report backtest plan must be true")

    for path in report["report"]["reports"].values():
        assert_true(Path(path).exists(), f"report file must exist: {path}")

    blocked = ["/buy", "/sell", "/live_on", "/show_env", "/set_secret", "/unlock_live", "/trade", "/market_order"]
    for command in blocked:
        response = handle_command(command)
        assert_true(response.get("ok") is False, f"{command} must not be ok")
        assert_true(response.get("blocked") is True, f"{command} must be blocked")

    print(
        "PHASE8E_SMOKE PASS "
        f"allowed={len(allowed)} "
        f"blocked={len(blocked)} "
        f"health_mode={health['health']['mode']} "
        f"metrics_report={metrics['metrics']['report_path']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
