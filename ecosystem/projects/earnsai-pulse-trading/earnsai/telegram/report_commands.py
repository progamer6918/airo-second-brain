from __future__ import annotations

from typing import Any

from earnsai.common.config import get_config
from earnsai.evaluation.fixture_runner import write_all_fixture_reports
from earnsai.evaluation.journal_analytics import write_all_journal_analytics
from earnsai.evaluation.metrics import evaluation_metrics, write_metrics_report
from earnsai.backtest.adapter import write_all_backtest_adapter_reports
from earnsai.freqtrade_adapter.status_reader import read_bridge_status


def build_health_payload() -> dict[str, Any]:
    cfg = get_config()
    bridge = read_bridge_status()
    metrics = evaluation_metrics(limit=500)

    return {
        "ok": True,
        "mode": cfg.mode,
        "live_trading_locked": cfg.live_trading_locked,
        "bridge_signals_match": bridge.get("signals_match"),
        "latest_action": bridge.get("latest_action"),
        "latest_risk_status": bridge.get("latest_risk_status"),
        "metrics_safety_ok": metrics.get("safety_ok"),
        "journal_rows": metrics.get("journal", {}).get("rows"),
    }


def build_metrics_payload() -> dict[str, Any]:
    metrics_report = write_metrics_report()
    metrics = metrics_report["metrics"]
    journal = metrics["journal"]
    latest = metrics["latest_signal"]

    return {
        "ok": True,
        "report_path": metrics_report["path"],
        "rows": journal.get("rows"),
        "hold_ratio": journal.get("hold_ratio"),
        "buy_ratio": journal.get("buy_ratio"),
        "sell_ratio": journal.get("sell_ratio"),
        "approved_paper_ratio": journal.get("approved_paper_ratio"),
        "latest_action": latest.get("action"),
        "latest_risk_status": latest.get("risk_status"),
        "safety_ok": metrics.get("safety_ok"),
    }


def build_report_payload() -> dict[str, Any]:
    metrics = write_metrics_report()
    journal = write_all_journal_analytics()
    fixtures = write_all_fixture_reports()
    backtest = write_all_backtest_adapter_reports()

    return {
        "ok": True,
        "reports": {
            "metrics": metrics["path"],
            "journal_json": journal["json_path"],
            "journal_markdown": journal["markdown_path"],
            "fixture_json": fixtures["json_path"],
            "fixture_markdown": fixtures["markdown_path"],
            "backtest_json": backtest["json_path"],
            "backtest_markdown": backtest["markdown_path"],
        },
        "summary": {
            "metrics_safety_ok": metrics["metrics"]["safety_ok"],
            "journal_rows": journal["total_rows"],
            "fixtures_ok": fixtures["ok"],
            "backtest_plan_ok": backtest["ok"],
        },
    }


def format_health_message(payload: dict[str, Any]) -> str:
    return (
        "Health: "
        f"mode={payload.get('mode')} "
        f"live_locked={payload.get('live_trading_locked')} "
        f"signals_match={payload.get('bridge_signals_match')} "
        f"latest_action={payload.get('latest_action')} "
        f"risk={payload.get('latest_risk_status')} "
        f"safety_ok={payload.get('metrics_safety_ok')} "
        f"journal_rows={payload.get('journal_rows')}"
    )


def format_metrics_message(payload: dict[str, Any]) -> str:
    return (
        "Metrics: "
        f"rows={payload.get('rows')} "
        f"hold_ratio={payload.get('hold_ratio')} "
        f"buy_ratio={payload.get('buy_ratio')} "
        f"sell_ratio={payload.get('sell_ratio')} "
        f"approved_ratio={payload.get('approved_paper_ratio')} "
        f"safety_ok={payload.get('safety_ok')} "
        f"report={payload.get('report_path')}"
    )


def format_report_message(payload: dict[str, Any]) -> str:
    reports = payload.get("reports", {})
    summary = payload.get("summary", {})

    return (
        "Reports generated: "
        f"metrics={reports.get('metrics')} "
        f"journal_md={reports.get('journal_markdown')} "
        f"fixtures_md={reports.get('fixture_markdown')} "
        f"backtest_md={reports.get('backtest_markdown')} "
        f"safety_ok={summary.get('metrics_safety_ok')} "
        f"fixtures_ok={summary.get('fixtures_ok')} "
        f"backtest_ok={summary.get('backtest_plan_ok')}"
    )
