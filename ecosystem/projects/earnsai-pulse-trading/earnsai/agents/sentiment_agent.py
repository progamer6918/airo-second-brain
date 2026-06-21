from __future__ import annotations

from earnsai.agents.base import AgentResult, clamp_confidence


def run_sentiment_agent(context: dict) -> AgentResult:
    symbol = context.get("symbol", "BTC/USDT")

    return AgentResult(
        agent="sentiment",
        status="OK",
        confidence=clamp_confidence(0.55),
        summary=f"Sentiment baseline for {symbol}: neutral because no live news/social feed is used in Phase 7C.",
        data={
            "sentiment": "neutral",
            "external_news_used": False,
            "social_scraping_used": False,
            "sentiment_modifier": 0.0,
        },
    )
