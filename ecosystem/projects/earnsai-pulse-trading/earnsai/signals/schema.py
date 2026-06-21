from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Literal

Action = Literal["BUY", "SELL", "HOLD"]
RiskStatus = Literal["APPROVED_FOR_PAPER_ONLY", "REJECTED", "BLOCKED"]
Mode = Literal["PAPER_ONLY"]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_now() -> str:
    return utc_now().isoformat()


def iso_in(minutes: int) -> str:
    return (utc_now() + timedelta(minutes=minutes)).isoformat()


@dataclass
class TradingSignal:
    signal_id: str
    created_at: str
    symbol: str
    timeframe: str
    action: Action
    confidence: float
    entry_reason: list[str] = field(default_factory=list)
    risk_notes: list[str] = field(default_factory=list)
    max_position_pct: float = 0.0
    stoploss_pct: float = 0.0
    take_profit_pct: float = 0.0
    valid_until: str = ""
    source_agents: list[str] = field(default_factory=list)
    risk_status: RiskStatus = "REJECTED"
    mode: Mode = "PAPER_ONLY"
    live_trading_locked: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)


def make_signal(
    *,
    symbol: str = "BTC/USDT",
    timeframe: str = "1h",
    action: Action = "HOLD",
    confidence: float = 0.0,
    entry_reason: list[str] | None = None,
    risk_notes: list[str] | None = None,
    max_position_pct: float = 0.0,
    stoploss_pct: float = 0.0,
    take_profit_pct: float = 0.0,
    valid_minutes: int = 60,
    source_agents: list[str] | None = None,
    risk_status: RiskStatus = "REJECTED",
    mode: Mode = "PAPER_ONLY",
    live_trading_locked: bool = True,
) -> TradingSignal:
    return TradingSignal(
        signal_id=str(uuid.uuid4()),
        created_at=iso_now(),
        symbol=symbol,
        timeframe=timeframe,
        action=action,
        confidence=float(confidence),
        entry_reason=entry_reason or [],
        risk_notes=risk_notes or [],
        max_position_pct=float(max_position_pct),
        stoploss_pct=float(stoploss_pct),
        take_profit_pct=float(take_profit_pct),
        valid_until=iso_in(valid_minutes),
        source_agents=source_agents or [],
        risk_status=risk_status,
        mode=mode,
        live_trading_locked=bool(live_trading_locked),
    )


def make_hold_signal(
    *,
    symbol: str = "BTC/USDT",
    timeframe: str = "1h",
    reason: str = "Default HOLD safety behavior.",
    risk_status: RiskStatus = "REJECTED",
) -> TradingSignal:
    return make_signal(
        symbol=symbol,
        timeframe=timeframe,
        action="HOLD",
        confidence=0.0,
        entry_reason=[reason],
        risk_notes=[reason],
        max_position_pct=0.0,
        stoploss_pct=0.0,
        take_profit_pct=0.0,
        source_agents=["system", "risk"],
        risk_status=risk_status,
        mode="PAPER_ONLY",
        live_trading_locked=True,
    )


def validate_signal(signal: TradingSignal | dict[str, Any]) -> tuple[bool, list[str]]:
    data = signal.to_dict() if isinstance(signal, TradingSignal) else dict(signal)
    errors: list[str] = []

    required = [
        "signal_id", "created_at", "symbol", "timeframe", "action", "confidence",
        "entry_reason", "risk_notes", "max_position_pct", "stoploss_pct",
        "take_profit_pct", "valid_until", "source_agents", "risk_status",
        "mode", "live_trading_locked",
    ]

    for key in required:
        if key not in data:
            errors.append(f"missing:{key}")

    if data.get("action") not in {"BUY", "SELL", "HOLD"}:
        errors.append("invalid:action")

    if data.get("risk_status") not in {"APPROVED_FOR_PAPER_ONLY", "REJECTED", "BLOCKED"}:
        errors.append("invalid:risk_status")

    if data.get("mode") != "PAPER_ONLY":
        errors.append("invalid:mode_must_be_paper_only")

    if data.get("live_trading_locked") is not True:
        errors.append("invalid:live_trading_locked_must_be_true")

    try:
        confidence = float(data.get("confidence", -1))
        if not 0.0 <= confidence <= 1.0:
            errors.append("invalid:confidence_range")
    except Exception:
        errors.append("invalid:confidence_type")

    try:
        max_position_pct = float(data.get("max_position_pct", -1))
        if not 0.0 <= max_position_pct <= 1.0:
            errors.append("invalid:max_position_pct_range")
    except Exception:
        errors.append("invalid:max_position_pct_type")

    for list_key in ["entry_reason", "risk_notes", "source_agents"]:
        if not isinstance(data.get(list_key), list):
            errors.append(f"invalid:{list_key}_must_be_list")

    return len(errors) == 0, errors


def write_signal(path: str | Path, signal: TradingSignal) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(signal.to_json() + "\n", encoding="utf-8")


def read_signal(path: str | Path) -> TradingSignal:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return TradingSignal(**data)
