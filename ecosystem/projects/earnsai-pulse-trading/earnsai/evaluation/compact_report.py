from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from earnsai.backtest.adapter import build_backtest_adapter_report
from earnsai.common.config import get_config
from earnsai.evaluation.fixture_runner import run_all_fixtures
from earnsai.evaluation.journal_analytics import analyze_journal
from earnsai.evaluation.metrics import evaluation_metrics
from earnsai.evaluation.stability import run_stability_checks
from earnsai.freqtrade_adapter.status_reader import read_bridge_status


def build_compact_status(limit: int = 500) -> dict[str, Any]:
    cfg = get_config()
    metrics = evaluation_metrics(limit=limit)
    journal = analyze_journal(limit=limit)
    fixtures = run_all_fixtures()
    backtest = build_backtest_adapter_report()
    stability = run_stability_checks()
    bridge = read_bridge_status()

    latest = metrics.get("latest_signal", {})
    journal_rates = journal.get("rates_pct", {})
    fixture_summary = fixtures.get("summary", {})
    backtest_readiness = backtest.get("fixture_readiness", {})

    safety_ok = (
        cfg.mode == "PAPER_ONLY"
        and cfg.live_trading_locked is True
        and metrics.get("safety_ok") is True
        and bridge.get("live_trading_locked") is True
        and bridge.get("mode") == "PAPER_ONLY"
        and stability.get("ok") is True
        and backtest.get("ok") is True
    )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": cfg.mode,
        "live_trading_locked": cfg.live_trading_locked,
        "safety_ok": safety_ok,
        "latest_signal": {
            "action": latest.get("action"),
            "risk_status": latest.get("risk_status"),
            "confidence": latest.get("confidence"),
            "valid_schema": latest.get("valid_schema"),
            "safe_for_phase8": latest.get("safe_for_phase8"),
            "age_seconds": latest.get("age_seconds"),
        },
        "bridge": {
            "signals_match": bridge.get("signals_match"),
            "latest_action": bridge.get("latest_action"),
            "latest_risk_status": bridge.get("latest_risk_status"),
            "freqtrade_action": bridge.get("freqtrade_action"),
            "freqtrade_risk_status": bridge.get("freqtrade_risk_status"),
        },
        "journal": {
            "rows": journal.get("total_rows"),
            "actions": journal.get("actions"),
            "risk_statuses": journal.get("risk_statuses"),
            "approved_paper_pct": journal_rates.get("approved_paper_pct"),
            "rejected_pct": journal_rates.get("rejected_pct"),
            "hold_pct": journal_rates.get("hold_pct"),
            "buy_pct": journal_rates.get("buy_pct"),
            "sell_pct": journal_rates.get("sell_pct"),
        },
        "fixtures": {
            "total": fixture_summary.get("total"),
            "passed": fixture_summary.get("passed"),
            "failed": fixture_summary.get("failed"),
            "final_actions": fixture_summary.get("final_actions"),
        },
        "backtest_adapter": {
            "ok": backtest.get("ok"),
            "plan_valid": backtest.get("plan_valid"),
            "execution_enabled": backtest.get("plan", {}).get("execution_enabled"),
            "private_exchange_api_used": backtest.get("plan", {}).get("private_exchange_api_used"),
            "fixture_total": backtest_readiness.get("total_scenarios"),
            "fixture_failed": backtest_readiness.get("failed"),
        },
        "stability": {
            "ok": stability.get("ok"),
            "checks": {
                name: result.get("ok")
                for name, result in stability.get("checks", {}).items()
            },
        },
        "recommended_next": "Phase 9D CI-style single gate command.",
    }


def render_compact_markdown(status: dict[str, Any]) -> str:
    latest = status["latest_signal"]
    bridge = status["bridge"]
    journal = status["journal"]
    fixtures = status["fixtures"]
    backtest = status["backtest_adapter"]
    stability = status["stability"]

    return f"""# EarnsAI Pulse — Compact Project Report

## Overall
- Generated at: `{status.get("generated_at")}`
- Mode: `{status.get("mode")}`
- Live trading locked: `{status.get("live_trading_locked")}`
- Safety OK: `{status.get("safety_ok")}`

## Latest Signal
- Action: `{latest.get("action")}`
- Risk status: `{latest.get("risk_status")}`
- Confidence: `{latest.get("confidence")}`
- Valid schema: `{latest.get("valid_schema")}`
- Safe for evaluation: `{latest.get("safe_for_phase8")}`

## Bridge
- Signals match: `{bridge.get("signals_match")}`
- Latest action: `{bridge.get("latest_action")}`
- Latest risk: `{bridge.get("latest_risk_status")}`
- FreqTrade action: `{bridge.get("freqtrade_action")}`
- FreqTrade risk: `{bridge.get("freqtrade_risk_status")}`

## Journal Snapshot
- Rows analyzed: `{journal.get("rows")}`
- Actions: `{journal.get("actions")}`
- Risk statuses: `{journal.get("risk_statuses")}`
- Approved paper-only: `{journal.get("approved_paper_pct")}%`
- Rejected: `{journal.get("rejected_pct")}%`
- HOLD: `{journal.get("hold_pct")}%`
- BUY: `{journal.get("buy_pct")}%`
- SELL: `{journal.get("sell_pct")}%`

## Fixtures
- Total: `{fixtures.get("total")}`
- Passed: `{fixtures.get("passed")}`
- Failed: `{fixtures.get("failed")}`
- Final actions: `{fixtures.get("final_actions")}`

## Backtest Adapter Plan
- OK: `{backtest.get("ok")}`
- Plan valid: `{backtest.get("plan_valid")}`
- Execution enabled: `{backtest.get("execution_enabled")}`
- Private exchange API used: `{backtest.get("private_exchange_api_used")}`
- Fixture failures: `{backtest.get("fixture_failed")}`

## Stability
- OK: `{stability.get("ok")}`
- Checks: `{stability.get("checks")}`

## Next
{status.get("recommended_next")}

## Safety Reminder
This project remains a paper/dry-run research system. Live trading and private exchange API usage remain disabled.
"""


def write_compact_report_json(path: str | Path = "reports/phase9c_compact_report.json", limit: int = 500) -> dict[str, Any]:
    status = build_compact_status(limit=limit)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(status, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "ok": status["safety_ok"],
        "path": str(target),
        "status": status,
    }


def write_compact_report_markdown(path: str | Path = "reports/phase9c_compact_report.md", limit: int = 500) -> dict[str, Any]:
    status = build_compact_status(limit=limit)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_compact_markdown(status), encoding="utf-8")
    return {
        "ok": status["safety_ok"],
        "path": str(target),
        "status": status,
    }


def write_all_compact_reports(limit: int = 500) -> dict[str, Any]:
    json_report = write_compact_report_json(limit=limit)
    markdown_report = write_compact_report_markdown(limit=limit)

    return {
        "ok": json_report["ok"] and markdown_report["ok"],
        "json_path": json_report["path"],
        "markdown_path": markdown_report["path"],
        "safety_ok": json_report["status"]["safety_ok"],
        "latest_action": json_report["status"]["latest_signal"]["action"],
        "latest_risk_status": json_report["status"]["latest_signal"]["risk_status"],
    }
