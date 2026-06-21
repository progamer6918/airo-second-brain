from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
from typing import Any

from earnsai.common.config import EarnsAIConfig, get_config
from earnsai.signals.schema import TradingSignal, make_hold_signal, validate_signal


def _parse_dt(value: str) -> datetime | None:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=timezone.utc)
        return parsed
    except Exception:
        return None


def evaluate_risk(signal: TradingSignal, config: EarnsAIConfig | None = None) -> tuple[str, list[str]]:
    cfg = config or get_config()

    is_valid, errors = validate_signal(signal)
    if not is_valid:
        return "BLOCKED", [f"schema_error:{err}" for err in errors]

    if cfg.mode != "PAPER_ONLY" or signal.mode != "PAPER_ONLY":
        return "BLOCKED", ["mode_not_paper_only"]

    if cfg.live_trading_locked is not True or signal.live_trading_locked is not True:
        return "BLOCKED", ["live_trading_lock_missing"]

    created_at = _parse_dt(signal.created_at)
    valid_until = _parse_dt(signal.valid_until)
    now = datetime.now(timezone.utc)

    if created_at is None or valid_until is None:
        return "REJECTED", ["invalid_timestamp"]

    age_minutes = (now - created_at).total_seconds() / 60
    if age_minutes > cfg.max_signal_age_minutes:
        return "REJECTED", ["stale_signal"]

    if valid_until < now:
        return "REJECTED", ["expired_signal"]

    if signal.action == "HOLD":
        return "REJECTED", ["hold_action_default_safe"]

    if signal.confidence < cfg.min_confidence:
        return "REJECTED", [f"confidence_below_threshold:{signal.confidence:.2f}<{cfg.min_confidence:.2f}"]

    if signal.max_position_pct <= 0:
        return "REJECTED", ["max_position_pct_zero"]

    if signal.max_position_pct > cfg.max_position_pct:
        return "REJECTED", [f"max_position_pct_above_limit:{signal.max_position_pct:.2f}>{cfg.max_position_pct:.2f}"]

    if signal.stoploss_pct >= 0:
        return "REJECTED", ["stoploss_pct_must_be_negative"]

    if signal.take_profit_pct <= 0:
        return "REJECTED", ["take_profit_pct_must_be_positive"]

    return "APPROVED_FOR_PAPER_ONLY", ["approved_for_paper_only"]


def apply_risk_gate(signal: TradingSignal, config: EarnsAIConfig | None = None) -> TradingSignal:
    status, notes = evaluate_risk(signal, config)

    if status != "APPROVED_FOR_PAPER_ONLY":
        return replace(
            signal,
            action="HOLD",
            confidence=min(float(signal.confidence), 0.59),
            max_position_pct=0.0,
            risk_status=status,
            risk_notes=list(signal.risk_notes) + notes,
            mode="PAPER_ONLY",
            live_trading_locked=True,
        )

    return replace(
        signal,
        risk_status="APPROVED_FOR_PAPER_ONLY",
        risk_notes=list(signal.risk_notes) + notes,
        mode="PAPER_ONLY",
        live_trading_locked=True,
    )


def gate_or_hold(signal: TradingSignal | None, reason: str = "missing_signal") -> TradingSignal:
    if signal is None:
        return make_hold_signal(reason=reason, risk_status="BLOCKED")
    return apply_risk_gate(signal)


def risk_summary(signal: TradingSignal) -> dict[str, Any]:
    return {
        "signal_id": signal.signal_id,
        "symbol": signal.symbol,
        "timeframe": signal.timeframe,
        "action": signal.action,
        "confidence": signal.confidence,
        "risk_status": signal.risk_status,
        "mode": signal.mode,
        "live_trading_locked": signal.live_trading_locked,
        "risk_notes": signal.risk_notes,
    }
