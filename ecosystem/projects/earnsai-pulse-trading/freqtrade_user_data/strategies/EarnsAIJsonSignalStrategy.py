from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

try:
    from freqtrade.strategy import IStrategy
except Exception:
    class IStrategy:
        pass


class EarnsAIJsonSignalStrategy(IStrategy):
    INTERFACE_VERSION = 3

    timeframe = "1h"
    can_short = False
    minimal_roi = {"0": 0.04}
    stoploss = -0.02
    startup_candle_count = 5
    process_only_new_candles = True
    use_exit_signal = True

    signal_path = Path("freqtrade_user_data/signals/latest_signal.json")

    def _read_signal(self) -> dict[str, Any]:
        fallback = {
            "action": "HOLD",
            "risk_status": "BLOCKED",
            "mode": "PAPER_ONLY",
            "live_trading_locked": True,
            "confidence": 0.0,
        }

        if not self.signal_path.exists():
            return fallback

        try:
            data = json.loads(self.signal_path.read_text(encoding="utf-8"))
        except Exception:
            return fallback

        if data.get("mode") != "PAPER_ONLY":
            data["action"] = "HOLD"
            data["risk_status"] = "BLOCKED"

        if data.get("live_trading_locked") is not True:
            data["action"] = "HOLD"
            data["risk_status"] = "BLOCKED"

        if data.get("risk_status") != "APPROVED_FOR_PAPER_ONLY":
            data["action"] = "HOLD"

        return data

    def populate_indicators(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        signal = self._read_signal()
        dataframe["earnsai_signal_action"] = signal.get("action", "HOLD")
        dataframe["earnsai_signal_confidence"] = float(signal.get("confidence", 0.0) or 0.0)
        dataframe["earnsai_risk_approved"] = signal.get("risk_status") == "APPROVED_FOR_PAPER_ONLY"
        return dataframe

    def populate_entry_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        dataframe.loc[
            (
                (dataframe["earnsai_signal_action"] == "BUY")
                & (dataframe["earnsai_risk_approved"] == True)
                & (dataframe["earnsai_signal_confidence"] >= 0.60)
            ),
            "enter_long",
        ] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        dataframe.loc[
            (
                (dataframe["earnsai_signal_action"].isin(["SELL", "HOLD"]))
                | (dataframe["earnsai_risk_approved"] == False)
            ),
            "exit_long",
        ] = 1
        return dataframe
