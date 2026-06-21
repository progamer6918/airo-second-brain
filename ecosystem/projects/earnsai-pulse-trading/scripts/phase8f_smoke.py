#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from earnsai.agents.orchestrator import run_multi_agent_cycle
from earnsai.evaluation.stability import run_stability_checks, write_stability_report
from earnsai.telegram.handlers import handle_command


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    run_multi_agent_cycle()

    checks = run_stability_checks()
    assert_true(checks["ok"] is True, f"stability checks must pass: {checks}")

    report = write_stability_report()
    assert_true(report["ok"] is True, "stability report must be ok")
    assert_true(Path(report["path"]).exists(), "stability report must exist")

    health = handle_command("/health")
    assert_true(health.get("ok") is True, "health command must still work")
    assert_true(health["health"]["mode"] == "PAPER_ONLY", "health mode must remain PAPER_ONLY")
    assert_true(health["health"]["live_trading_locked"] is True, "health live lock must remain true")

    print(
        "PHASE8F_SMOKE PASS "
        f"checks={len(checks['checks'])} "
        f"report={report['path']} "
        f"health_mode={health['health']['mode']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
