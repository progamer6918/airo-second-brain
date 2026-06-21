from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from earnsai.common.config import get_config
from earnsai.journal.jsonl_store import read_jsonl
from earnsai.signals.schema import read_signal


def summarize_journal(limit: int = 100) -> dict[str, Any]:
    cfg = get_config()
    rows = read_jsonl(cfg.journal_path, limit=limit)

    action_counts: Counter[str] = Counter()
    risk_counts: Counter[str] = Counter()
    phase_counts: Counter[str] = Counter()

    for row in rows:
        final = row.get("final", {})
        if isinstance(final, dict):
            action_counts[str(final.get("action", "UNKNOWN"))] += 1
            risk_counts[str(final.get("risk_status", "UNKNOWN"))] += 1
        phase_counts[str(row.get("phase", "UNKNOWN"))] += 1

    latest = {}
    try:
        latest = read_signal(cfg.latest_signal_path).to_dict()
    except Exception:
        latest = {
            "action": "HOLD",
            "risk_status": "BLOCKED",
            "mode": "PAPER_ONLY",
            "live_trading_locked": True,
        }

    return {
        "rows": len(rows),
        "actions": dict(action_counts),
        "risk_status": dict(risk_counts),
        "phases": dict(phase_counts),
        "latest": latest,
    }


def generate_markdown_report(path: str | Path = "reports/phase7e_daily_report.md") -> dict[str, Any]:
    summary = summarize_journal()
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)

    latest = summary["latest"]

    content = f"""# EarnsAI Pulse — Phase 7E Daily Report

## Safety
- Mode: `{latest.get("mode", "PAPER_ONLY")}`
- Live trading locked: `{latest.get("live_trading_locked", True)}`
- Latest action: `{latest.get("action", "HOLD")}`
- Latest risk status: `{latest.get("risk_status", "BLOCKED")}`

## Journal Summary
- Rows analyzed: `{summary["rows"]}`
- Action counts: `{summary["actions"]}`
- Risk status counts: `{summary["risk_status"]}`
- Phase counts: `{summary["phases"]}`

## Notes
- This report is generated locally.
- No private exchange API is used.
- No live trading is enabled.
- Telegram control layer remains command-safe.
"""
    target.write_text(content, encoding="utf-8")
    return {
        "ok": True,
        "path": str(target),
        "summary": summary,
    }
