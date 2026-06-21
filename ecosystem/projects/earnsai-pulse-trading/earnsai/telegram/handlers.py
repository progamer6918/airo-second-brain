from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from earnsai.agents.orchestrator import run_multi_agent_cycle
from earnsai.common.config import get_config
from earnsai.freqtrade_adapter.status_reader import read_bridge_status
from earnsai.journal.jsonl_store import read_jsonl
from earnsai.signals.schema import read_signal
from earnsai.telegram.report_commands import (
    build_health_payload,
    build_metrics_payload,
    build_report_payload,
    format_health_message,
    format_metrics_message,
    format_report_message,
)

CONTROL_STATE_PATH = Path("runtime/control_state.json")

ALLOWED_COMMANDS = {
    "/status",
    "/signal",
    "/risk",
    "/journal",
    "/pause",
    "/resume",
    "/lock_live",
    "/help",
    "/report",
    "/metrics",
    "/health",
}

BLOCKED_COMMANDS = {
    "/buy",
    "/sell",
    "/live_on",
    "/show_env",
    "/set_secret",
    "/unlock_live",
    "/trade",
    "/market_order",
}


def _load_state() -> dict[str, Any]:
    if not CONTROL_STATE_PATH.exists():
        return {
            "paused": False,
            "live_trading_locked": True,
            "mode": "PAPER_ONLY",
            "last_command": None,
        }

    try:
        data = json.loads(CONTROL_STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        data = {}

    return {
        "paused": bool(data.get("paused", False)),
        "live_trading_locked": True,
        "mode": "PAPER_ONLY",
        "last_command": data.get("last_command"),
    }


def _save_state(state: dict[str, Any]) -> None:
    CONTROL_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    safe_state = {
        "paused": bool(state.get("paused", False)),
        "live_trading_locked": True,
        "mode": "PAPER_ONLY",
        "last_command": state.get("last_command"),
    }
    CONTROL_STATE_PATH.write_text(json.dumps(safe_state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def help_text() -> str:
    return (
        "EarnsAI Pulse Control Commands:\n"
        "/status - show bridge and system status\n"
        "/signal - show latest signal\n"
        "/risk - show latest risk summary\n"
        "/journal - show recent journal summary\n"
        "/report - generate Phase 8 reports\n"
        "/metrics - show evaluation metrics summary\n"
        "/health - show compact health status\n"
        "/pause - pause agent decisions\n"
        "/resume - resume agent decisions\n"
        "/lock_live - force live trading lock\n"
        "/help - show commands\n\n"
        "Blocked: /buy, /sell, /live_on, /show_env, /set_secret, /unlock_live"
    )


def _safe_latest_signal() -> dict[str, Any]:
    cfg = get_config()
    try:
        signal = read_signal(cfg.latest_signal_path)
        return signal.to_dict()
    except Exception:
        return {
            "action": "HOLD",
            "risk_status": "BLOCKED",
            "mode": "PAPER_ONLY",
            "live_trading_locked": True,
            "risk_notes": ["latest_signal_missing_or_unreadable"],
        }


def handle_command(text: str) -> dict[str, Any]:
    raw = (text or "").strip()
    command = raw.split()[0].lower() if raw else "/help"

    if command in BLOCKED_COMMANDS:
        return {
            "ok": False,
            "command": command,
            "blocked": True,
            "message": f"BLOCKED: {command} is not allowed. Paper/dry-run monitoring only.",
        }

    if command not in ALLOWED_COMMANDS:
        return {
            "ok": False,
            "command": command,
            "blocked": True,
            "message": "Unknown or unsafe command. Use /help.",
        }

    cfg = get_config()
    state = _load_state()
    state["last_command"] = command

    if command == "/help":
        _save_state(state)
        return {"ok": True, "command": command, "message": help_text()}

    if command == "/pause":
        state["paused"] = True
        state["live_trading_locked"] = True
        _save_state(state)
        return {
            "ok": True,
            "command": command,
            "message": "EarnsAI Pulse paused. Live trading remains locked.",
            "state": state,
        }

    if command == "/resume":
        state["paused"] = False
        state["live_trading_locked"] = True
        _save_state(state)
        return {
            "ok": True,
            "command": command,
            "message": "EarnsAI Pulse resumed for paper/dry-run monitoring only.",
            "state": state,
        }

    if command == "/lock_live":
        state["live_trading_locked"] = True
        _save_state(state)
        return {
            "ok": True,
            "command": command,
            "message": "Live trading lock enforced. LIVE_TRADING_LOCKED remains true.",
            "state": state,
        }

    if command == "/health":
        payload = build_health_payload()
        _save_state(state)
        return {
            "ok": True,
            "command": command,
            "message": format_health_message(payload),
            "health": payload,
        }

    if command == "/metrics":
        payload = build_metrics_payload()
        _save_state(state)
        return {
            "ok": True,
            "command": command,
            "message": format_metrics_message(payload),
            "metrics": payload,
        }

    if command == "/report":
        payload = build_report_payload()
        _save_state(state)
        return {
            "ok": True,
            "command": command,
            "message": format_report_message(payload),
            "report": payload,
        }

    if command == "/status":
        bridge = read_bridge_status()
        _save_state(state)
        return {
            "ok": True,
            "command": command,
            "message": (
                f"Status: mode={bridge.get('mode')} "
                f"live_locked={bridge.get('live_trading_locked')} "
                f"signals_match={bridge.get('signals_match')} "
                f"action={bridge.get('latest_action')} "
                f"risk={bridge.get('latest_risk_status')}"
            ),
            "bridge": bridge,
            "state": state,
        }

    if command == "/signal":
        signal = _safe_latest_signal()
        _save_state(state)
        return {
            "ok": True,
            "command": command,
            "message": (
                f"Latest signal: {signal.get('symbol', cfg.default_symbol)} "
                f"{signal.get('timeframe', cfg.default_timeframe)} "
                f"action={signal.get('action')} "
                f"confidence={signal.get('confidence')} "
                f"risk={signal.get('risk_status')}"
            ),
            "signal": signal,
        }

    if command == "/risk":
        signal = _safe_latest_signal()
        _save_state(state)
        return {
            "ok": True,
            "command": command,
            "message": (
                f"Risk: status={signal.get('risk_status')} "
                f"mode={signal.get('mode')} "
                f"live_locked={signal.get('live_trading_locked')} "
                f"notes={signal.get('risk_notes', [])[-3:]}"
            ),
            "risk": signal,
        }

    if command == "/journal":
        rows = read_jsonl(cfg.journal_path, limit=5)
        _save_state(state)
        return {
            "ok": True,
            "command": command,
            "message": f"Journal rows available={len(rows)} latest_events={[row.get('event') for row in rows[-3:]]}",
            "rows": rows,
        }

    return {
        "ok": False,
        "command": command,
        "blocked": True,
        "message": "Unhandled command.",
    }


def run_safe_cycle_if_not_paused() -> dict[str, Any]:
    state = _load_state()
    if state.get("paused"):
        return {
            "ok": False,
            "skipped": True,
            "reason": "paused",
            "state": state,
        }

    result = run_multi_agent_cycle()
    return {
        "ok": True,
        "skipped": False,
        "result": result,
        "state": state,
    }
