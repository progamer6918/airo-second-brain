from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from earnsai.common.config import get_config
from earnsai.journal.jsonl_store import read_jsonl
from earnsai.signals.schema import read_signal, validate_signal


def _safe_ratio(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return round(numerator / denominator, 6)


def _parse_dt(value: str) -> datetime | None:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=timezone.utc)
        return parsed
    except Exception:
        return None


def latest_signal_metrics() -> dict[str, Any]:
    cfg = get_config()

    try:
        signal = read_signal(cfg.latest_signal_path)
        is_valid, errors = validate_signal(signal)
        created_at = _parse_dt(signal.created_at)
        valid_until = _parse_dt(signal.valid_until)
        now = datetime.now(timezone.utc)

        age_seconds = None
        expired = True

        if created_at is not None:
            age_seconds = round((now - created_at).total_seconds(), 3)

        if valid_until is not None:
            expired = valid_until < now

        return {
            "exists": True,
            "valid_schema": is_valid,
            "schema_errors": errors,
            "signal_id": signal.signal_id,
            "symbol": signal.symbol,
            "timeframe": signal.timeframe,
            "action": signal.action,
            "confidence": signal.confidence,
            "risk_status": signal.risk_status,
            "mode": signal.mode,
            "live_trading_locked": signal.live_trading_locked,
            "age_seconds": age_seconds,
            "expired": expired,
            "safe_for_phase8": (
                is_valid
                and signal.mode == "PAPER_ONLY"
                and signal.live_trading_locked is True
                and signal.risk_status in {"APPROVED_FOR_PAPER_ONLY", "REJECTED", "BLOCKED"}
            ),
        }
    except Exception as exc:
        return {
            "exists": False,
            "valid_schema": False,
            "schema_errors": [str(exc)],
            "action": "HOLD",
            "risk_status": "BLOCKED",
            "mode": "PAPER_ONLY",
            "live_trading_locked": True,
            "age_seconds": None,
            "expired": True,
            "safe_for_phase8": False,
        }


def journal_metrics(limit: int = 500) -> dict[str, Any]:
    cfg = get_config()
    rows = read_jsonl(cfg.journal_path, limit=limit)

    actions: Counter[str] = Counter()
    risk_statuses: Counter[str] = Counter()
    phases: Counter[str] = Counter()
    events: Counter[str] = Counter()

    for row in rows:
        events[str(row.get("event", "UNKNOWN"))] += 1
        phases[str(row.get("phase", "UNKNOWN"))] += 1

        final = row.get("final", {})
        if isinstance(final, dict):
            actions[str(final.get("action", "UNKNOWN"))] += 1
            risk_statuses[str(final.get("risk_status", "UNKNOWN"))] += 1

    total = len(rows)
    hold_count = actions.get("HOLD", 0)
    buy_count = actions.get("BUY", 0)
    sell_count = actions.get("SELL", 0)
    approved_count = risk_statuses.get("APPROVED_FOR_PAPER_ONLY", 0)
    rejected_count = risk_statuses.get("REJECTED", 0)
    blocked_count = risk_statuses.get("BLOCKED", 0)

    return {
        "rows": total,
        "actions": dict(actions),
        "risk_statuses": dict(risk_statuses),
        "phases": dict(phases),
        "events": dict(events),
        "hold_ratio": _safe_ratio(hold_count, total),
        "buy_ratio": _safe_ratio(buy_count, total),
        "sell_ratio": _safe_ratio(sell_count, total),
        "approved_paper_ratio": _safe_ratio(approved_count, total),
        "rejected_ratio": _safe_ratio(rejected_count, total),
        "blocked_ratio": _safe_ratio(blocked_count, total),
    }


def evaluation_metrics(limit: int = 500) -> dict[str, Any]:
    cfg = get_config()
    latest = latest_signal_metrics()
    journal = journal_metrics(limit=limit)

    return {
        "mode": cfg.mode,
        "live_trading_locked": cfg.live_trading_locked,
        "journal": journal,
        "latest_signal": latest,
        "safety_ok": (
            cfg.mode == "PAPER_ONLY"
            and cfg.live_trading_locked is True
            and latest.get("safe_for_phase8") is True
        ),
    }


def render_metrics_markdown(metrics: dict[str, Any]) -> str:
    journal = metrics["journal"]
    latest = metrics["latest_signal"]

    return f"""# EarnsAI Pulse — Phase 8A Evaluation Metrics

## Safety
- Mode: `{metrics.get("mode")}`
- Live trading locked: `{metrics.get("live_trading_locked")}`
- Safety OK: `{metrics.get("safety_ok")}`

## Journal Metrics
- Rows: `{journal.get("rows")}`
- Actions: `{journal.get("actions")}`
- Risk statuses: `{journal.get("risk_statuses")}`
- HOLD ratio: `{journal.get("hold_ratio")}`
- BUY ratio: `{journal.get("buy_ratio")}`
- SELL ratio: `{journal.get("sell_ratio")}`
- Approved paper-only ratio: `{journal.get("approved_paper_ratio")}`
- Rejected ratio: `{journal.get("rejected_ratio")}`
- Blocked ratio: `{journal.get("blocked_ratio")}`

## Latest Signal
- Exists: `{latest.get("exists")}`
- Valid schema: `{latest.get("valid_schema")}`
- Action: `{latest.get("action")}`
- Risk status: `{latest.get("risk_status")}`
- Confidence: `{latest.get("confidence")}`
- Age seconds: `{latest.get("age_seconds")}`
- Expired: `{latest.get("expired")}`
- Safe for Phase 8: `{latest.get("safe_for_phase8")}`
"""


def write_metrics_report(path: str | Path = "reports/phase8a_metrics_report.md", limit: int = 500) -> dict[str, Any]:
    metrics = evaluation_metrics(limit=limit)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_metrics_markdown(metrics), encoding="utf-8")
    return {
        "ok": True,
        "path": str(target),
        "metrics": metrics,
    }
