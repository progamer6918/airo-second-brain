from __future__ import annotations

from earnsai.agents.decision_agent import run_decision_agent
from earnsai.agents.monitoring_agent import run_monitoring_agent
from earnsai.agents.research_agent import run_research_agent
from earnsai.agents.risk_agent import run_risk_agent
from earnsai.agents.sentiment_agent import run_sentiment_agent
from earnsai.agents.strategy_agent import run_strategy_agent
from earnsai.agents.technical_agent import run_technical_agent
from earnsai.common.config import get_config
from earnsai.journal.jsonl_store import append_decision
from earnsai.risk.gate import apply_risk_gate, risk_summary
from earnsai.signals.schema import make_signal, write_signal


def _explicit_signal(context: dict, action: str, confidence: float):
    cfg = get_config()
    return make_signal(
        symbol=context.get("symbol", cfg.default_symbol),
        timeframe=context.get("timeframe", cfg.default_timeframe),
        action=action,  # type: ignore[arg-type]
        confidence=confidence,
        entry_reason=["Explicit Phase 7B compatibility path."],
        risk_notes=["All explicit decisions still pass risk gate."],
        max_position_pct=0.05 if action in {"BUY", "SELL"} else 0.0,
        stoploss_pct=-0.02 if action in {"BUY", "SELL"} else 0.0,
        take_profit_pct=0.04 if action in {"BUY", "SELL"} else 0.0,
        valid_minutes=60,
        source_agents=["compat", "risk", "decision"],
        risk_status="REJECTED",
        mode="PAPER_ONLY",
        live_trading_locked=True,
    )


def run_multi_agent_cycle(context: dict | None = None) -> dict:
    cfg = get_config()
    ctx = {
        "symbol": cfg.default_symbol,
        "timeframe": cfg.default_timeframe,
        "prices": [100.0, 101.0, 102.0, 103.0, 104.0, 105.0],
        **(context or {}),
    }

    agent_results: dict[str, dict] = {}

    research = run_research_agent(ctx)
    agent_results["research"] = research.to_dict()

    technical = run_technical_agent(ctx)
    agent_results["technical"] = technical.to_dict()

    sentiment = run_sentiment_agent(ctx)
    agent_results["sentiment"] = sentiment.to_dict()

    strategy = run_strategy_agent(ctx, agent_results)
    agent_results["strategy"] = strategy.to_dict()

    risk = run_risk_agent(ctx, agent_results)
    agent_results["risk"] = risk.to_dict()

    decision, raw_signal = run_decision_agent(ctx, agent_results)
    agent_results["decision"] = decision.to_dict()

    final_signal = apply_risk_gate(raw_signal, cfg)
    final_dict = final_signal.to_dict()

    monitoring = run_monitoring_agent(ctx, agent_results, final_dict)
    agent_results["monitoring"] = monitoring.to_dict()

    write_signal(cfg.latest_signal_path, final_signal)
    write_signal(cfg.freqtrade_signal_path, final_signal)

    append_decision(
        {
            "event": "multi_agent_decision",
            "phase": "7C",
            "context": ctx,
            "agents": agent_results,
            "final": final_dict,
            "risk": risk_summary(final_signal),
        },
        cfg.journal_path,
    )

    return {
        "ok": True,
        "phase": "7C",
        "context": ctx,
        "agents": agent_results,
        "signal": final_dict,
        "risk": risk_summary(final_signal),
        "latest_signal_path": cfg.latest_signal_path,
        "freqtrade_signal_path": cfg.freqtrade_signal_path,
        "journal_path": cfg.journal_path,
    }


def run_once(
    *,
    symbol: str | None = None,
    timeframe: str | None = None,
    action: str = "HOLD",
    confidence: float = 0.0,
) -> dict:
    cfg = get_config()
    context = {
        "symbol": symbol or cfg.default_symbol,
        "timeframe": timeframe or cfg.default_timeframe,
    }

    if action == "AUTO":
        return run_multi_agent_cycle(context)

    raw_signal = _explicit_signal(context, action, confidence)
    final_signal = apply_risk_gate(raw_signal, cfg)

    write_signal(cfg.latest_signal_path, final_signal)
    write_signal(cfg.freqtrade_signal_path, final_signal)

    append_decision(
        {
            "event": "decision",
            "phase": "7C_COMPAT",
            "raw_action": raw_signal.action,
            "final": final_signal.to_dict(),
            "risk": risk_summary(final_signal),
        },
        cfg.journal_path,
    )

    return {
        "ok": True,
        "phase": "7C_COMPAT",
        "signal": final_signal.to_dict(),
        "risk": risk_summary(final_signal),
        "latest_signal_path": cfg.latest_signal_path,
        "freqtrade_signal_path": cfg.freqtrade_signal_path,
        "journal_path": cfg.journal_path,
    }
