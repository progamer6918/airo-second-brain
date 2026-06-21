from __future__ import annotations

from earnsai.agents.base import AgentResult, clamp_confidence


def run_monitoring_agent(context: dict, agent_results: dict[str, dict], final_signal: dict) -> AgentResult:
    return AgentResult(
        agent="monitoring",
        status="OK",
        confidence=clamp_confidence(1.0),
        summary="Monitoring baseline recorded final signal and agent outputs.",
        data={
            "final_action": final_signal.get("action"),
            "risk_status": final_signal.get("risk_status"),
            "mode": final_signal.get("mode"),
            "live_trading_locked": final_signal.get("live_trading_locked"),
            "agent_count": len(agent_results),
        },
    )
