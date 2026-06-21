#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from earnsai.agents.orchestrator import run_multi_agent_cycle, run_once
from earnsai.evaluation.metrics import evaluation_metrics, write_metrics_report


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    run_once(action="HOLD", confidence=0.0)
    run_multi_agent_cycle(
        {
            "symbol": "BTC/USDT",
            "timeframe": "1h",
            "prices": [100.0, 101.0, 102.5, 103.0, 105.0, 107.0],
        }
    )

    metrics = evaluation_metrics(limit=500)

    assert_true(metrics["mode"] == "PAPER_ONLY", "mode must remain PAPER_ONLY")
    assert_true(metrics["live_trading_locked"] is True, "live trading must remain locked")
    assert_true(metrics["safety_ok"] is True, "Phase 8A safety_ok must be true")

    journal = metrics["journal"]
    latest = metrics["latest_signal"]

    assert_true(journal["rows"] >= 2, "journal must contain at least two rows")
    assert_true(0.0 <= journal["hold_ratio"] <= 1.0, "hold ratio must be valid")
    assert_true(0.0 <= journal["approved_paper_ratio"] <= 1.0, "approved ratio must be valid")
    assert_true(latest["exists"] is True, "latest signal must exist")
    assert_true(latest["valid_schema"] is True, "latest signal schema must be valid")
    assert_true(latest["mode"] == "PAPER_ONLY", "latest signal must be PAPER_ONLY")
    assert_true(latest["live_trading_locked"] is True, "latest signal live lock must be true")

    report = write_metrics_report()
    assert_true(Path(report["path"]).exists(), "metrics report must be created")

    print(
        "PHASE8A_SMOKE PASS "
        f"rows={journal['rows']} "
        f"hold_ratio={journal['hold_ratio']} "
        f"approved_ratio={journal['approved_paper_ratio']} "
        f"safety_ok={metrics['safety_ok']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
