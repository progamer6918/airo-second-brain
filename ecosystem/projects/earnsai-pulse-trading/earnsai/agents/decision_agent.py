from __future__ import annotations

from earnsai.agents.base import AgentResult, clamp_confidence
from earnsai.common.config import get_config
from earnsai.signals.schema import make_signal


def run_decision_agent(context: dict, agent_results: dict[str, dict]) -> tuple[AgentResult, object]:
    cfg = get_config()
    strategy = agent_results.get("strategy", {})
    risk = agent_results.get("risk", {})

    strategy_data = strategy.get("data", {})
    risk_data = risk.get("data", {})

    action = strategy_data.get("candidate_action", "HOLD")
    strategy_conf = float(strategy.get("confidence", 0.0))
    risk_conf = float(risk.get("confidence", 0.0))
    final_conf = clamp_confidence((strategy_conf * 0.7) + (risk_conf * 0.3))

    if "blocked:mode_not_paper_only" in risk_data.get("notes", []):
        action = "HOLD"
        final_conf = min(final_conf, 0.30)

    if "blocked:live_trading_lock_missing" in risk_data.get("notes", []):
        action = "HOLD"
        final_conf = min(final_conf, 0.30)

    signal = make_signal(
        symbol=context.get("symbol", cfg.default_symbol),
        timeframe=context.get("timeframe", cfg.default_timeframe),
        action=action,
        confidence=final_conf,
        entry_reason=[
            agent_results.get("research", {}).get("summary", ""),
            agent_results.get("technical", {}).get("summary", ""),
            agent_results.get("strategy", {}).get("summary", ""),
        ],
        risk_notes=risk_data.get("notes", ["risk_precheck_missing"]),
        max_position_pct=float(strategy_data.get("max_position_pct", 0.0)),
        stoploss_pct=float(strategy_data.get("stoploss_pct", 0.0)),
        take_profit_pct=float(strategy_data.get("take_profit_pct", 0.0)),
        valid_minutes=60,
        source_agents=["research", "technical", "sentiment", "strategy", "risk", "decision"],
        risk_status="REJECTED",
        mode="PAPER_ONLY",
        live_trading_locked=True,
    )

    result = AgentResult(
        agent="decision",
        status="OK",
        confidence=final_conf,
        summary=f"Decision agent produced raw action={action}, confidence={final_conf:.2f}.",
        data={
            "raw_action": action,
            "confidence": final_conf,
            "source_agents": signal.source_agents,
        },
    )

    return result, signal
