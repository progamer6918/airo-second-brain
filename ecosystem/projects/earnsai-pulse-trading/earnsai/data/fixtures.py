from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ScenarioName = Literal["bullish", "bearish", "flat", "volatile"]


@dataclass(frozen=True)
class PriceScenario:
    name: str
    symbol: str
    timeframe: str
    prices: list[float]
    expected_trend: str
    expected_candidate_action: str
    description: str

    def to_context(self) -> dict:
        return {
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "prices": list(self.prices),
            "scenario": self.name,
        }

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "prices": list(self.prices),
            "expected_trend": self.expected_trend,
            "expected_candidate_action": self.expected_candidate_action,
            "description": self.description,
        }


def bullish_scenario() -> PriceScenario:
    return PriceScenario(
        name="bullish",
        symbol="BTC/USDT",
        timeframe="1h",
        prices=[100.0, 101.0, 102.0, 104.0, 106.0, 108.0],
        expected_trend="bullish",
        expected_candidate_action="BUY",
        description="Steady upward movement. Short moving average should be above long moving average.",
    )


def bearish_scenario() -> PriceScenario:
    return PriceScenario(
        name="bearish",
        symbol="BTC/USDT",
        timeframe="1h",
        prices=[108.0, 106.0, 104.0, 102.0, 101.0, 100.0],
        expected_trend="bearish",
        expected_candidate_action="SELL",
        description="Steady downward movement. Short moving average should be below long moving average.",
    )


def flat_scenario() -> PriceScenario:
    return PriceScenario(
        name="flat",
        symbol="BTC/USDT",
        timeframe="1h",
        prices=[100.0, 100.0, 100.0, 100.0, 100.0, 100.0],
        expected_trend="flat",
        expected_candidate_action="HOLD",
        description="No directional movement. Strategy should stay defensive.",
    )


def volatile_scenario() -> PriceScenario:
    return PriceScenario(
        name="volatile",
        symbol="BTC/USDT",
        timeframe="1h",
        prices=[100.0, 106.0, 98.0, 108.0, 97.0, 109.0],
        expected_trend="bullish",
        expected_candidate_action="BUY",
        description="High variance sequence with final short average above long average.",
    )


def all_scenarios() -> list[PriceScenario]:
    return [
        bullish_scenario(),
        bearish_scenario(),
        flat_scenario(),
        volatile_scenario(),
    ]


def get_scenario(name: str) -> PriceScenario:
    scenarios = {scenario.name: scenario for scenario in all_scenarios()}
    if name not in scenarios:
        raise KeyError(f"unknown_scenario:{name}")
    return scenarios[name]


def fixture_catalog() -> dict:
    return {
        scenario.name: scenario.to_dict()
        for scenario in all_scenarios()
    }
