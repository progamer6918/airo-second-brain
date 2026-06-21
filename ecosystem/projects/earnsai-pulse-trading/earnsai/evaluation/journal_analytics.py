from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from earnsai.common.config import get_config
from earnsai.evaluation.metrics import evaluation_metrics
from earnsai.journal.jsonl_store import read_jsonl


def _safe_pct(count: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return round((count / total) * 100, 3)


def _extract_final(row: dict[str, Any]) -> dict[str, Any]:
    final = row.get("final", {})
    return final if isinstance(final, dict) else {}


def _extract_risk(row: dict[str, Any]) -> dict[str, Any]:
    risk = row.get("risk", {})
    return risk if isinstance(risk, dict) else {}


def analyze_journal(limit: int = 500) -> dict[str, Any]:
    cfg = get_config()
    rows = read_jsonl(cfg.journal_path, limit=limit)

    events: Counter[str] = Counter()
    phases: Counter[str] = Counter()
    actions: Counter[str] = Counter()
    risk_statuses: Counter[str] = Counter()
    symbols: Counter[str] = Counter()
    timeframes: Counter[str] = Counter()
    confidence_buckets: Counter[str] = Counter()

    latest_rows: list[dict[str, Any]] = []

    for row in rows:
        events[str(row.get("event", "UNKNOWN"))] += 1
        phases[str(row.get("phase", "UNKNOWN"))] += 1

        final = _extract_final(row)
        risk = _extract_risk(row)

        action = str(final.get("action", risk.get("action", "UNKNOWN")))
        risk_status = str(final.get("risk_status", risk.get("risk_status", "UNKNOWN")))

        actions[action] += 1
        risk_statuses[risk_status] += 1
        symbols[str(final.get("symbol", risk.get("symbol", "UNKNOWN")))] += 1
        timeframes[str(final.get("timeframe", risk.get("timeframe", "UNKNOWN")))] += 1

        try:
            confidence = float(final.get("confidence", risk.get("confidence", 0.0)))
        except Exception:
            confidence = 0.0

        if confidence < 0.30:
            confidence_buckets["0.00-0.29"] += 1
        elif confidence < 0.60:
            confidence_buckets["0.30-0.59"] += 1
        elif confidence < 0.80:
            confidence_buckets["0.60-0.79"] += 1
        else:
            confidence_buckets["0.80-1.00"] += 1

        latest_rows.append(
            {
                "journaled_at": row.get("journaled_at"),
                "phase": row.get("phase"),
                "event": row.get("event"),
                "action": action,
                "risk_status": risk_status,
                "confidence": confidence,
            }
        )

    total = len(rows)
    approved = risk_statuses.get("APPROVED_FOR_PAPER_ONLY", 0)
    rejected = risk_statuses.get("REJECTED", 0)
    blocked = risk_statuses.get("BLOCKED", 0)
    hold = actions.get("HOLD", 0)
    buy = actions.get("BUY", 0)
    sell = actions.get("SELL", 0)

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "limit": limit,
        "total_rows": total,
        "events": dict(events),
        "phases": dict(phases),
        "actions": dict(actions),
        "risk_statuses": dict(risk_statuses),
        "symbols": dict(symbols),
        "timeframes": dict(timeframes),
        "confidence_buckets": dict(confidence_buckets),
        "rates_pct": {
            "approved_paper_pct": _safe_pct(approved, total),
            "rejected_pct": _safe_pct(rejected, total),
            "blocked_pct": _safe_pct(blocked, total),
            "hold_pct": _safe_pct(hold, total),
            "buy_pct": _safe_pct(buy, total),
            "sell_pct": _safe_pct(sell, total),
        },
        "latest_rows": latest_rows[-10:],
        "metrics_snapshot": evaluation_metrics(limit=limit),
    }


def write_journal_analytics_json(path: str | Path = "reports/phase8b_journal_analytics.json", limit: int = 500) -> dict[str, Any]:
    analysis = analyze_journal(limit=limit)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(analysis, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "ok": True,
        "path": str(target),
        "analysis": analysis,
    }


def render_journal_analytics_markdown(analysis: dict[str, Any]) -> str:
    rates = analysis["rates_pct"]
    metrics = analysis["metrics_snapshot"]
    latest = metrics["latest_signal"]

    latest_rows_md = "\n".join(
        [
            f"| {row.get('phase')} | {row.get('event')} | {row.get('action')} | {row.get('risk_status')} | {row.get('confidence')} |"
            for row in analysis.get("latest_rows", [])
        ]
    )

    if not latest_rows_md:
        latest_rows_md = "| - | - | - | - | - |"

    return f"""# EarnsAI Pulse — Phase 8B Journal Analytics

## Safety Snapshot
- Mode: `{metrics.get("mode")}`
- Live trading locked: `{metrics.get("live_trading_locked")}`
- Safety OK: `{metrics.get("safety_ok")}`
- Latest signal action: `{latest.get("action")}`
- Latest risk status: `{latest.get("risk_status")}`

## Journal Overview
- Total rows: `{analysis.get("total_rows")}`
- Events: `{analysis.get("events")}`
- Phases: `{analysis.get("phases")}`
- Actions: `{analysis.get("actions")}`
- Risk statuses: `{analysis.get("risk_statuses")}`

## Rates
- Approved paper-only: `{rates.get("approved_paper_pct")}%`
- Rejected: `{rates.get("rejected_pct")}%`
- Blocked: `{rates.get("blocked_pct")}%`
- HOLD: `{rates.get("hold_pct")}%`
- BUY: `{rates.get("buy_pct")}%`
- SELL: `{rates.get("sell_pct")}%`

## Confidence Buckets
`{analysis.get("confidence_buckets")}`

## Latest Journal Rows

| Phase | Event | Action | Risk Status | Confidence |
|---|---|---|---|---|
{latest_rows_md}

## Notes
- This report is for paper/dry-run evaluation only.
- It does not imply live trading readiness.
- Private exchange API remains disabled.
"""


def write_journal_analytics_markdown(path: str | Path = "reports/phase8b_journal_analytics.md", limit: int = 500) -> dict[str, Any]:
    analysis = analyze_journal(limit=limit)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_journal_analytics_markdown(analysis), encoding="utf-8")
    return {
        "ok": True,
        "path": str(target),
        "analysis": analysis,
    }


def write_all_journal_analytics(limit: int = 500) -> dict[str, Any]:
    json_report = write_journal_analytics_json(limit=limit)
    markdown_report = write_journal_analytics_markdown(limit=limit)
    return {
        "ok": True,
        "json_path": json_report["path"],
        "markdown_path": markdown_report["path"],
        "total_rows": json_report["analysis"]["total_rows"],
        "rates_pct": json_report["analysis"]["rates_pct"],
    }
