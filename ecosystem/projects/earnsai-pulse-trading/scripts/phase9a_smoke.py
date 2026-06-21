#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from earnsai.data.local_fixture_provider import get_default_provider
from earnsai.data.provider import MarketDataRequest
from earnsai.data.provider_runner import fetch_market_context, run_cycle_from_provider, validate_snapshot


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    provider = get_default_provider()

    scenarios = ["bullish", "bearish", "flat", "volatile"]
    results = {}

    for scenario in scenarios:
        snapshot = provider.fetch(MarketDataRequest(scenario=scenario))
        valid, errors = validate_snapshot(snapshot)

        assert_true(valid, f"{scenario} snapshot must be valid: {errors}")
        assert_true(snapshot.private_exchange_api_used is False, "private exchange API must not be used")
        assert_true(snapshot.live_data_used is False, "live data must not be used")
        assert_true(snapshot.source == "local_fixture_provider", "source must be local fixture provider")

        context = fetch_market_context(scenario=scenario)
        assert_true(context["data_source"] == "local_fixture_provider", "context source must be local fixture provider")
        assert_true(context["private_exchange_api_used"] is False, "context private API must be false")
        assert_true(context["live_data_used"] is False, "context live data must be false")

        cycle = run_cycle_from_provider(scenario=scenario)
        signal = cycle["signal"]
        provider_meta = cycle["data_provider"]

        assert_true(signal["mode"] == "PAPER_ONLY", "signal mode must remain PAPER_ONLY")
        assert_true(signal["live_trading_locked"] is True, "live trading must remain locked")
        assert_true(provider_meta["private_exchange_api_used"] is False, "provider private API must remain false")
        assert_true(provider_meta["live_data_used"] is False, "provider live data must remain false")

        results[scenario] = {
            "action": signal["action"],
            "risk_status": signal["risk_status"],
            "source": provider_meta["source"],
        }

    print(
        "PHASE9A_SMOKE PASS "
        f"scenarios={len(results)} "
        f"bullish={results['bullish']['action']} "
        f"bearish={results['bearish']['action']} "
        f"flat={results['flat']['action']} "
        f"volatile={results['volatile']['action']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
