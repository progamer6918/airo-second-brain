from __future__ import annotations

from typing import Any

from earnsai.agents.orchestrator import run_multi_agent_cycle
from earnsai.data.local_fixture_provider import get_default_provider
from earnsai.data.provider import MarketDataRequest, MarketDataSnapshot


def fetch_market_context(
    *,
    symbol: str = "BTC/USDT",
    timeframe: str = "1h",
    scenario: str = "bullish",
) -> dict[str, Any]:
    provider = get_default_provider()
    snapshot = provider.fetch(
        MarketDataRequest(
            symbol=symbol,
            timeframe=timeframe,
            scenario=scenario,
        )
    )
    return snapshot.to_context()


def run_cycle_from_provider(
    *,
    symbol: str = "BTC/USDT",
    timeframe: str = "1h",
    scenario: str = "bullish",
) -> dict[str, Any]:
    context = fetch_market_context(
        symbol=symbol,
        timeframe=timeframe,
        scenario=scenario,
    )
    result = run_multi_agent_cycle(context)
    result["data_provider"] = {
        "source": context["data_source"],
        "scenario": context["scenario"],
        "private_exchange_api_used": context["private_exchange_api_used"],
        "live_data_used": context["live_data_used"],
    }
    return result


def validate_snapshot(snapshot: MarketDataSnapshot) -> tuple[bool, list[str]]:
    errors: list[str] = []

    if not snapshot.symbol:
        errors.append("missing_symbol")

    if not snapshot.timeframe:
        errors.append("missing_timeframe")

    if len(snapshot.prices) < 3:
        errors.append("insufficient_prices")

    if snapshot.private_exchange_api_used is not False:
        errors.append("private_exchange_api_must_not_be_used")

    if snapshot.live_data_used is not False:
        errors.append("live_data_must_not_be_used_in_phase9a")

    return len(errors) == 0, errors
