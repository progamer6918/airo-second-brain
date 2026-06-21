from __future__ import annotations

from statistics import mean

from earnsai.agents.base import AgentResult, clamp_confidence


def run_technical_agent(context: dict) -> AgentResult:
    prices = context.get("prices") or [100.0, 101.0, 102.0, 103.0, 104.0, 105.0]
    symbol = context.get("symbol", "BTC/USDT")

    short_window = prices[-3:]
    long_window = prices[-6:] if len(prices) >= 6 else prices

    short_ma = mean(short_window)
    long_ma = mean(long_window)

    if short_ma > long_ma:
        trend = "bullish"
        suggested_action = "BUY"
        confidence = 0.70
    elif short_ma < long_ma:
        trend = "bearish"
        suggested_action = "SELL"
        confidence = 0.66
    else:
        trend = "flat"
        suggested_action = "HOLD"
        confidence = 0.45

    return AgentResult(
        agent="technical",
        status="OK",
        confidence=clamp_confidence(confidence),
        summary=f"Technical baseline for {symbol}: short_ma={short_ma:.2f}, long_ma={long_ma:.2f}, trend={trend}.",
        data={
            "prices": prices,
            "short_ma": short_ma,
            "long_ma": long_ma,
            "trend": trend,
            "suggested_action": suggested_action,
        },
    )
