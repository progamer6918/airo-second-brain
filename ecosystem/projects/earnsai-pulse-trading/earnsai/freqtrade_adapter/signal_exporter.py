from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from earnsai.common.config import get_config
from earnsai.risk.gate import apply_risk_gate
from earnsai.signals.schema import TradingSignal, read_signal, validate_signal, write_signal


def export_signal_to_freqtrade(
    signal: TradingSignal,
    *,
    earnsai_path: str | Path | None = None,
    freqtrade_path: str | Path | None = None,
) -> dict[str, Any]:
    cfg = get_config()
    final_signal = apply_risk_gate(signal, cfg)

    is_valid, errors = validate_signal(final_signal)
    if not is_valid:
        raise ValueError(f"final_signal_schema_invalid:{errors}")

    if final_signal.mode != "PAPER_ONLY":
        raise ValueError("blocked:mode_must_be_paper_only")

    if final_signal.live_trading_locked is not True:
        raise ValueError("blocked:live_trading_must_remain_locked")

    earnsai_target = Path(earnsai_path or cfg.latest_signal_path)
    freqtrade_target = Path(freqtrade_path or cfg.freqtrade_signal_path)

    write_signal(earnsai_target, final_signal)
    write_signal(freqtrade_target, final_signal)

    return {
        "ok": True,
        "signal_id": final_signal.signal_id,
        "action": final_signal.action,
        "risk_status": final_signal.risk_status,
        "earnsai_path": str(earnsai_target),
        "freqtrade_path": str(freqtrade_target),
    }


def mirror_latest_to_freqtrade() -> dict[str, Any]:
    cfg = get_config()
    source = Path(cfg.latest_signal_path)
    target = Path(cfg.freqtrade_signal_path)

    if not source.exists():
        raise FileNotFoundError(f"missing_latest_signal:{source}")

    signal = read_signal(source)
    return export_signal_to_freqtrade(signal, earnsai_path=source, freqtrade_path=target)


def read_freqtrade_signal(path: str | Path | None = None) -> dict[str, Any]:
    cfg = get_config()
    target = Path(path or cfg.freqtrade_signal_path)

    if not target.exists():
        return {
            "exists": False,
            "path": str(target),
            "action": "HOLD",
            "risk_status": "BLOCKED",
            "mode": "PAPER_ONLY",
            "live_trading_locked": True,
        }

    data = json.loads(target.read_text(encoding="utf-8"))
    return {
        "exists": True,
        "path": str(target),
        **data,
    }
