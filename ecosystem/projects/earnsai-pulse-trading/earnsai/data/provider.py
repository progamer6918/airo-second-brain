from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class MarketDataRequest:
    symbol: str = "BTC/USDT"
    timeframe: str = "1h"
    scenario: str = "bullish"


@dataclass(frozen=True)
class MarketDataSnapshot:
    symbol: str
    timeframe: str
    prices: list[float]
    source: str
    scenario: str
    private_exchange_api_used: bool = False
    live_data_used: bool = False

    def to_context(self) -> dict:
        return {
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "prices": list(self.prices),
            "scenario": self.scenario,
            "data_source": self.source,
            "private_exchange_api_used": self.private_exchange_api_used,
            "live_data_used": self.live_data_used,
        }

    def to_dict(self) -> dict:
        return {
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "prices": list(self.prices),
            "source": self.source,
            "scenario": self.scenario,
            "private_exchange_api_used": self.private_exchange_api_used,
            "live_data_used": self.live_data_used,
        }


class MarketDataProvider(Protocol):
    name: str

    def fetch(self, request: MarketDataRequest) -> MarketDataSnapshot:
        ...
