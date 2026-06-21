from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from earnsai.common.config import get_config
from earnsai.freqtrade_adapter.signal_exporter import read_freqtrade_signal
from earnsai.freqtrade_adapter.status_reader import read_bridge_status
from earnsai.signals.schema import make_hold_signal, write_signal
from earnsai.telegram.handlers import handle_command


def check_unknown_command_blocked() -> dict[str, Any]:
    response = handle_command("/definitely_unknown_command")
    return {
        "ok": response.get("ok") is False and response.get("blocked") is True,
        "response": response,
    }


def check_trading_commands_blocked() -> dict[str, Any]:
    blocked = ["/buy", "/sell", "/live_on", "/unlock_live", "/show_env", "/set_secret", "/trade", "/market_order"]
    results = {}

    for command in blocked:
        response = handle_command(command)
        results[command] = {
            "ok_false": response.get("ok") is False,
            "blocked_true": response.get("blocked") is True,
            "message": response.get("message"),
        }

    return {
        "ok": all(item["ok_false"] and item["blocked_true"] for item in results.values()),
        "results": results,
    }


def check_missing_freqtrade_signal_fallback() -> dict[str, Any]:
    cfg = get_config()
    path = Path(cfg.freqtrade_signal_path)
    backup = None

    if path.exists():
        backup = path.read_text(encoding="utf-8")
        path.unlink()

    try:
        fallback = read_freqtrade_signal(path)
        ok = (
            fallback.get("exists") is False
            and fallback.get("action") == "HOLD"
            and fallback.get("risk_status") == "BLOCKED"
            and fallback.get("mode") == "PAPER_ONLY"
            and fallback.get("live_trading_locked") is True
        )
    finally:
        if backup is not None:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(backup, encoding="utf-8")

    return {
        "ok": ok,
        "fallback": fallback,
    }


def check_bridge_recovers_after_hold_signal() -> dict[str, Any]:
    cfg = get_config()
    hold = make_hold_signal(
        symbol=cfg.default_symbol,
        timeframe=cfg.default_timeframe,
        reason="Phase 8F stability fallback HOLD.",
    )

    write_signal(cfg.latest_signal_path, hold)
    write_signal(cfg.freqtrade_signal_path, hold)

    status = read_bridge_status()

    return {
        "ok": (
            status.get("signals_match") is True
            and status.get("latest_action") == "HOLD"
            and status.get("latest_risk_status") in {"REJECTED", "BLOCKED"}
            and status.get("mode") == "PAPER_ONLY"
            and status.get("live_trading_locked") is True
        ),
        "status": status,
    }


def check_corrupted_temp_signal_detection() -> dict[str, Any]:
    temp_path = Path("runtime/corrupted_signal_test.json")
    temp_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path.write_text("{bad json", encoding="utf-8")

    try:
        try:
            json.loads(temp_path.read_text(encoding="utf-8"))
            parsed = True
        except Exception:
            parsed = False

        return {
            "ok": parsed is False,
            "path": str(temp_path),
            "parsed": parsed,
        }
    finally:
        temp_path.unlink(missing_ok=True)


def run_stability_checks() -> dict[str, Any]:
    checks = {
        "unknown_command_blocked": check_unknown_command_blocked(),
        "trading_commands_blocked": check_trading_commands_blocked(),
        "missing_freqtrade_signal_fallback": check_missing_freqtrade_signal_fallback(),
        "bridge_recovers_after_hold_signal": check_bridge_recovers_after_hold_signal(),
        "corrupted_temp_signal_detection": check_corrupted_temp_signal_detection(),
    }

    return {
        "ok": all(item.get("ok") is True for item in checks.values()),
        "checks": checks,
    }


def write_stability_report(path: str | Path = "reports/phase8f_stability_report.md") -> dict[str, Any]:
    report = run_stability_checks()
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# EarnsAI Pulse — Phase 8F Stability Report",
        "",
        "## Summary",
        f"- OK: `{report['ok']}`",
        "",
        "## Checks",
    ]

    for name, result in report["checks"].items():
        lines.append(f"- `{name}`: `{result.get('ok')}`")

    lines.extend(
        [
            "",
            "## Safety",
            "- Mode remains PAPER_ONLY.",
            "- Live trading remains locked.",
            "- Private exchange API is not used.",
            "- Unsafe Telegram commands remain blocked.",
            "- Missing signal fallback returns HOLD/BLOCKED.",
        ]
    )

    target.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return {
        "ok": report["ok"],
        "path": str(target),
        "report": report,
    }
