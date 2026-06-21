from __future__ import annotations

from earnsai.agents.base import AgentResult, clamp_confidence
from earnsai.common.config import get_config


def run_risk_agent(context: dict, agent_results: dict[str, dict]) -> AgentResult:
    cfg = get_config()
    strategy = agent_results.get("strategy", {})
    strategy_data = strategy.get("data", {})

    candidate_action = strategy_data.get("candidate_action", "HOLD")
    max_position_pct = float(strategy_data.get("max_position_pct", 0.0))

    notes: list[str] = []

    if cfg.mode != "PAPER_ONLY":
        notes.append("blocked:mode_not_paper_only")

    if cfg.live_trading_locked is not True:
        notes.append("blocked:live_trading_lock_missing")

    if max_position_pct > cfg.max_position_pct:
        notes.append("rejected:max_position_above_limit")

    if candidate_action == "HOLD":
        notes.append("safe:hold_candidate")

    if not notes:
        notes.append("safe:risk_precheck_ok")

    confidence = 0.75 if notes == ["safe:risk_precheck_ok"] else 0.55

    return AgentResult(
        agent="risk",
        status="OK",
        confidence=clamp_confidence(confidence),
        summary="Risk precheck completed before final risk gate.",
        data={
            "candidate_action": candidate_action,
            "max_position_pct": max_position_pct,
            "mode": cfg.mode,
            "live_trading_locked": cfg.live_trading_locked,
            "notes": notes,
        },
    )
