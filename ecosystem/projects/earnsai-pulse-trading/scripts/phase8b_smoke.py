#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from earnsai.agents.orchestrator import run_multi_agent_cycle, run_once
from earnsai.evaluation.journal_analytics import analyze_journal, write_all_journal_analytics


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    run_once(action="HOLD", confidence=0.0)
    run_multi_agent_cycle(
        {
            "symbol": "BTC/USDT",
            "timeframe": "1h",
            "prices": [100.0, 101.0, 101.5, 102.0, 104.0, 106.0],
        }
    )

    analysis = analyze_journal(limit=500)

    assert_true(analysis["total_rows"] >= 2, "journal analysis must include rows")
    assert_true("actions" in analysis, "analysis must include actions")
    assert_true("risk_statuses" in analysis, "analysis must include risk statuses")
    assert_true("rates_pct" in analysis, "analysis must include rates")
    assert_true("metrics_snapshot" in analysis, "analysis must include metrics snapshot")
    assert_true(analysis["metrics_snapshot"]["safety_ok"] is True, "safety_ok must remain true")
    assert_true(0.0 <= analysis["rates_pct"]["approved_paper_pct"] <= 100.0, "approved pct must be valid")
    assert_true(0.0 <= analysis["rates_pct"]["hold_pct"] <= 100.0, "hold pct must be valid")

    reports = write_all_journal_analytics(limit=500)

    json_path = ROOT / reports["json_path"]
    markdown_path = ROOT / reports["markdown_path"]

    assert_true(json_path.exists(), "json analytics report must exist")
    assert_true(markdown_path.exists(), "markdown analytics report must exist")

    parsed = json.loads(json_path.read_text(encoding="utf-8"))
    assert_true(parsed["total_rows"] == analysis["total_rows"], "json report rows must match analysis")

    print(
        "PHASE8B_SMOKE PASS "
        f"rows={analysis['total_rows']} "
        f"approved_pct={analysis['rates_pct']['approved_paper_pct']} "
        f"hold_pct={analysis['rates_pct']['hold_pct']} "
        f"json={reports['json_path']} "
        f"md={reports['markdown_path']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
