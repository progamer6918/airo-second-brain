from __future__ import annotations

from earnsai.agents.base import AgentResult, clamp_confidence


def run_research_agent(context: dict) -> AgentResult:
    symbol = context.get("symbol", "BTC/USDT")
    timeframe = context.get("timeframe", "1h")

    return AgentResult(
        agent="research",
        status="OK",
        confidence=clamp_confidence(0.62),
        summary=f"Research baseline for {symbol} on {timeframe}: no external/news API used in Phase 7C.",
        data={
            "symbol": symbol,
            "timeframe": timeframe,
            "external_api_used": False,
            "private_exchange_api_used": False,
            "research_bias": "neutral_to_cautious",
        },
    )
