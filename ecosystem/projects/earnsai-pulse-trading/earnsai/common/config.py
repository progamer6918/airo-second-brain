from __future__ import annotations

import os
from dataclasses import dataclass


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class EarnsAIConfig:
    mode: str = "PAPER_ONLY"
    live_trading_locked: bool = True
    default_symbol: str = "BTC/USDT"
    default_timeframe: str = "1h"
    min_confidence: float = 0.60
    max_position_pct: float = 0.10
    max_signal_age_minutes: int = 120
    journal_path: str = "logs/decisions.jsonl"
    latest_signal_path: str = "earnsai/signals/latest_signal.json"
    freqtrade_signal_path: str = "freqtrade_user_data/signals/latest_signal.json"


def get_config() -> EarnsAIConfig:
    return EarnsAIConfig(
        mode=os.getenv("EARNSAI_MODE", "PAPER_ONLY").strip().upper(),
        live_trading_locked=_as_bool(os.getenv("LIVE_TRADING_LOCKED"), True),
        default_symbol=os.getenv("EARNSAI_DEFAULT_SYMBOL", "BTC/USDT"),
        default_timeframe=os.getenv("EARNSAI_DEFAULT_TIMEFRAME", "1h"),
        min_confidence=float(os.getenv("EARNSAI_MIN_CONFIDENCE", "0.60")),
        max_position_pct=float(os.getenv("EARNSAI_MAX_POSITION_PCT", "0.10")),
        max_signal_age_minutes=int(os.getenv("EARNSAI_MAX_SIGNAL_AGE_MINUTES", "120")),
        journal_path=os.getenv("EARNSAI_JOURNAL_PATH", "logs/decisions.jsonl"),
        latest_signal_path=os.getenv("EARNSAI_LATEST_SIGNAL_PATH", "earnsai/signals/latest_signal.json"),
        freqtrade_signal_path=os.getenv("FREQTRADE_SIGNAL_PATH", "freqtrade_user_data/signals/latest_signal.json"),
    )
