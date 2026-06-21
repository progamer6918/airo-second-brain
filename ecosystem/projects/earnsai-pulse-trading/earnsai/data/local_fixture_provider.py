from __future__ import annotations

from earnsai.data.fixtures import get_scenario
from earnsai.data.provider import MarketDataRequest, MarketDataSnapshot


class LocalFixtureProvider:
    name = "local_fixture_provider"

    def fetch(self, request: MarketDataRequest) -> MarketDataSnapshot:
        scenario = get_scenario(request.scenario)

        return MarketDataSnapshot(
            symbol=request.symbol or scenario.symbol,
            timeframe=request.timeframe or scenario.timeframe,
            prices=list(scenario.prices),
            source=self.name,
            scenario=scenario.name,
            private_exchange_api_used=False,
            live_data_used=False,
        )


def get_default_provider() -> LocalFixtureProvider:
    return LocalFixtureProvider()
