#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from earnsai.agents.orchestrator import run_multi_agent_cycle, run_once
from earnsai.common.config import get_config
from earnsai.journal.jsonl_store import read_jsonl
from earnsai.signals.schema import read_signal, validate_signal


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    cfg = get_config()

    compat = run_once(action="HOLD", confidence=0.0)
    assert_true(compat["signal"]["action"] == "HOLD", "Compatibility HOLD must stay HOLD")

    cycle = run_multi_agent_cycle(
        {
            "symbol": cfg.default_symbol,
            "timeframe": cfg.default_timeframe,
            "prices": [100.0, 101.0, 102.0, 104.0, 106.0, 108.0],
        }
    )

    signal = cycle["signal"]
    agents = cycle["agents"]

    required_agents = {"research", "technical", "sentiment", "strategy", "risk", "decision", "monitoring"}
    assert_true(required_agents.issubset(set(agents.keys())), f"Missing agents: {required_agents - set(agents.keys())}")

    assert_true(signal["mode"] == "PAPER_ONLY", "Final signal must be PAPER_ONLY")
    assert_true(signal["live_trading_locked"] is True, "Final signal must keep live trading locked")
    assert_true(signal["risk_status"] in {"APPROVED_FOR_PAPER_ONLY", "REJECTED", "BLOCKED"}, "Invalid risk status")

    latest = read_signal(cfg.latest_signal_path)
    is_valid, errors = validate_signal(latest)
    assert_true(is_valid, f"Latest signal invalid: {errors}")

    mirrored = read_signal(cfg.freqtrade_signal_path)
    assert_true(mirrored.signal_id == latest.signal_id, "FreqTrade mirrored signal must match latest EarnsAI signal")

    journal_rows = read_jsonl(cfg.journal_path, limit=10)
    assert_true(any(row.get("phase") == "7C" for row in journal_rows), "Journal must include Phase 7C decision row")

    print(
        "PHASE7C_SMOKE PASS "
        f"agents={len(agents)} "
        f"action={signal['action']} "
        f"risk={signal['risk_status']} "
        f"journal_rows={len(journal_rows)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
