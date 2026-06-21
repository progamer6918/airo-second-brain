from __future__ import annotations

from earnsai.agents.base import AgentResult, clamp_confidence


def run_strategy_agent(context: dict, agent_results: dict[str, dict]) -> AgentResult:
    technical = agent_results.get("technical", {})
    sentiment = agent_results.get("sentiment", {})

    technical_data = technical.get("data", {})
    suggested_action = technical_data.get("suggested_action", "HOLD")
    sentiment_label = sentiment.get("data", {}).get("sentiment", "neutral")

    technical_conf = float(technical.get("confidence", 0.0))
    sentiment_conf = float(sentiment.get("confidence", 0.0))

    if suggested_action in {"BUY", "SELL"} and sentiment_label == "neutral":
        action = suggested_action
        confidence = min(0.82, (technical_conf * 0.75) + (sentiment_conf * 0.25) + 0.08)
    else:
        action = "HOLD"
        confidence = 0.45

    return AgentResult(
        agent="strategy",
        status="OK",
        confidence=clamp_confidence(confidence),
        summary=f"Strategy baseline selected action={action} from technical={suggested_action}, sentiment={sentiment_label}.",
        data={
            "candidate_action": action,
            "technical_action": suggested_action,
            "sentiment": sentiment_label,
            "position_sizing_model": "fixed_small_paper_position",
            "max_position_pct": 0.05 if action in {"BUY", "SELL"} else 0.0,
            "stoploss_pct": -0.02 if action in {"BUY", "SELL"} else 0.0,
            "take_profit_pct": 0.04 if action in {"BUY", "SELL"} else 0.0,
        },
    )
