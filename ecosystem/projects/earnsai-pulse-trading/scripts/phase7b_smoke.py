#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from earnsai.agents.orchestrator import run_once
from earnsai.common.config import get_config
from earnsai.journal.jsonl_store import read_jsonl
from earnsai.risk.gate import apply_risk_gate
from earnsai.signals.schema import make_signal, read_signal, validate_signal


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    cfg = get_config()

    hold_result = run_once(action="HOLD", confidence=0.0)
    hold_signal = hold_result["signal"]
    assert_true(hold_signal["action"] == "HOLD", "HOLD scenario must stay HOLD")
    assert_true(hold_signal["risk_status"] in {"REJECTED", "BLOCKED"}, "HOLD scenario must not be approved")

    low_conf = make_signal(
        symbol=cfg.default_symbol,
        timeframe=cfg.default_timeframe,
        action="BUY",
        confidence=0.30,
        max_position_pct=0.05,
        stoploss_pct=-0.02,
        take_profit_pct=0.04,
        source_agents=["technical", "risk", "decision"],
    )
    low_conf_final = apply_risk_gate(low_conf, cfg)
    assert_true(low_conf_final.action == "HOLD", "Low confidence BUY must become HOLD")
    assert_true(low_conf_final.risk_status == "REJECTED", "Low confidence BUY must be REJECTED")

    approved = make_signal(
        symbol=cfg.default_symbol,
        timeframe=cfg.default_timeframe,
        action="BUY",
        confidence=0.80,
        max_position_pct=0.05,
        stoploss_pct=-0.02,
        take_profit_pct=0.04,
        source_agents=["technical", "risk", "decision"],
    )
    approved_final = apply_risk_gate(approved, cfg)
    assert_true(approved_final.action == "BUY", "Valid paper BUY should remain BUY")
    assert_true(approved_final.risk_status == "APPROVED_FOR_PAPER_ONLY", "Valid paper BUY must be approved for paper only")

    is_valid, errors = validate_signal(approved_final)
    assert_true(is_valid, f"Approved final signal schema invalid: {errors}")

    latest = read_signal(cfg.latest_signal_path)
    assert_true(latest.mode == "PAPER_ONLY", "Latest signal mode must be PAPER_ONLY")
    assert_true(latest.live_trading_locked is True, "Latest signal must keep live trading locked")

    journal_rows = read_jsonl(cfg.journal_path, limit=5)
    assert_true(len(journal_rows) >= 1, "Journal must contain at least one decision row")

    print(
        "PHASE7B_SMOKE PASS "
        f"hold={hold_signal['risk_status']} "
        f"low_conf={low_conf_final.risk_status} "
        f"approved={approved_final.risk_status} "
        f"journal_rows={len(journal_rows)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
