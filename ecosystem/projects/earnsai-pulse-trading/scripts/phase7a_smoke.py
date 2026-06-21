#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from earnsai.common.config import get_config
from earnsai.risk.gate import apply_risk_gate
from earnsai.signals.schema import make_hold_signal, validate_signal, write_signal


def main() -> int:
    cfg = get_config()
    signal = apply_risk_gate(
        make_hold_signal(
            symbol=cfg.default_symbol,
            timeframe=cfg.default_timeframe,
            reason="Phase 7A smoke safety baseline.",
        ),
        cfg,
    )

    is_valid, errors = validate_signal(signal)
    if not is_valid:
        raise AssertionError(f"schema invalid: {errors}")

    if signal.action != "HOLD":
        raise AssertionError("Phase 7A smoke must remain HOLD")

    if signal.risk_status not in {"REJECTED", "BLOCKED"}:
        raise AssertionError("Phase 7A smoke must not approve paper trade")

    write_signal(cfg.latest_signal_path, signal)
    write_signal(cfg.freqtrade_signal_path, signal)

    print(f"PHASE7A_SMOKE PASS symbol={signal.symbol} action={signal.action} risk={signal.risk_status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
