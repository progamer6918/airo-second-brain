#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from earnsai.agents.orchestrator import run_multi_agent_cycle
from earnsai.common.config import get_config
from earnsai.freqtrade_adapter.signal_exporter import mirror_latest_to_freqtrade, read_freqtrade_signal
from earnsai.freqtrade_adapter.status_reader import read_bridge_status
from earnsai.signals.schema import read_signal, validate_signal


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    cfg = get_config()

    run_multi_agent_cycle(
        {
            "symbol": cfg.default_symbol,
            "timeframe": cfg.default_timeframe,
            "prices": [100.0, 101.0, 102.5, 104.0, 106.0, 108.0],
        }
    )

    signal = read_signal(cfg.latest_signal_path)
    is_valid, errors = validate_signal(signal)
    assert_true(is_valid, f"latest signal invalid:{errors}")
    assert_true(signal.mode == "PAPER_ONLY", "latest signal must be PAPER_ONLY")
    assert_true(signal.live_trading_locked is True, "latest signal must keep live trading locked")

    mirror = mirror_latest_to_freqtrade()
    assert_true(mirror["ok"] is True, "mirror must be ok")

    freqtrade_signal = read_freqtrade_signal()
    assert_true(freqtrade_signal["exists"] is True, "freqtrade signal file must exist")
    assert_true(freqtrade_signal["signal_id"] == signal.signal_id, "freqtrade signal must mirror latest signal")
    assert_true(freqtrade_signal["mode"] == "PAPER_ONLY", "freqtrade signal must be PAPER_ONLY")
    assert_true(freqtrade_signal["live_trading_locked"] is True, "freqtrade signal must keep live trading locked")

    bridge_status = read_bridge_status()
    assert_true(bridge_status["signals_match"] is True, "bridge status must show matching signals")
    assert_true(bridge_status["mode"] == "PAPER_ONLY", "bridge mode must be PAPER_ONLY")
    assert_true(bridge_status["live_trading_locked"] is True, "bridge live trading must remain locked")

    config_path = ROOT / "freqtrade_user_data/config/config.dryrun.json"
    dryrun_config = json.loads(config_path.read_text(encoding="utf-8"))
    assert_true(dryrun_config.get("dry_run") is True, "FreqTrade config must be dry_run=true")
    assert_true(dryrun_config.get("initial_state") == "stopped", "FreqTrade config initial_state must stay stopped")
    assert_true(dryrun_config.get("force_entry_enable") is False, "force entry must be disabled")
    assert_true("exchange" in dryrun_config, "FreqTrade dryrun config must define exchange")
    assert_true("key" not in dryrun_config.get("exchange", {}), "Dryrun config must not contain exchange key")

    strategy_path = ROOT / "freqtrade_user_data/strategies/EarnsAIJsonSignalStrategy.py"
    ast.parse(strategy_path.read_text(encoding="utf-8"), filename=str(strategy_path))
    strategy_text = strategy_path.read_text(encoding="utf-8")
    assert_true("APPROVED_FOR_PAPER_ONLY" in strategy_text, "Strategy must check APPROVED_FOR_PAPER_ONLY")
    assert_true("PAPER_ONLY" in strategy_text, "Strategy must check PAPER_ONLY")
    assert_true("live_trading_locked" in strategy_text, "Strategy must check live trading lock")
    assert_true("enter_long" in strategy_text, "Strategy must define enter_long")
    assert_true("exit_long" in strategy_text, "Strategy must define exit_long")

    print(
        "PHASE7D_SMOKE PASS "
        f"action={signal.action} "
        f"risk={signal.risk_status} "
        f"bridge_match={bridge_status['signals_match']} "
        f"dry_run={dryrun_config.get('dry_run')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
