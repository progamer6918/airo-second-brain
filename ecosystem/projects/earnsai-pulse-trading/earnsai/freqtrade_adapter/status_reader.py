from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from earnsai.common.config import get_config


def read_bridge_status() -> dict[str, Any]:
    cfg = get_config()
    latest_path = Path(cfg.latest_signal_path)
    freqtrade_path = Path(cfg.freqtrade_signal_path)
    journal_path = Path(cfg.journal_path)

    latest = {}
    freqtrade = {}

    if latest_path.exists():
        latest = json.loads(latest_path.read_text(encoding="utf-8"))

    if freqtrade_path.exists():
        freqtrade = json.loads(freqtrade_path.read_text(encoding="utf-8"))

    return {
        "mode": cfg.mode,
        "live_trading_locked": cfg.live_trading_locked,
        "latest_signal_exists": latest_path.exists(),
        "freqtrade_signal_exists": freqtrade_path.exists(),
        "journal_exists": journal_path.exists(),
        "latest_signal_id": latest.get("signal_id"),
        "freqtrade_signal_id": freqtrade.get("signal_id"),
        "signals_match": bool(latest.get("signal_id") and latest.get("signal_id") == freqtrade.get("signal_id")),
        "latest_action": latest.get("action", "HOLD"),
        "freqtrade_action": freqtrade.get("action", "HOLD"),
        "latest_risk_status": latest.get("risk_status", "BLOCKED"),
        "freqtrade_risk_status": freqtrade.get("risk_status", "BLOCKED"),
    }


def print_bridge_status() -> None:
    print(json.dumps(read_bridge_status(), indent=2, sort_keys=True))
