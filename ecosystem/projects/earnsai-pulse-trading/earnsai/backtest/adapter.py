from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from earnsai.data.fixtures import all_scenarios
from earnsai.evaluation.fixture_runner import run_fixture_scenario


@dataclass(frozen=True)
class BacktestAdapterPlan:
    name: str
    mode: str
    live_trading_locked: bool
    private_exchange_api_used: bool
    execution_enabled: bool
    purpose: str
    input_source: str
    output_target: str
    safety_notes: list[str]
    planned_steps: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_backtest_adapter_plan() -> BacktestAdapterPlan:
    return BacktestAdapterPlan(
        name="EarnsAI Phase 8D Backtest Adapter Plan",
        mode="PAPER_ONLY",
        live_trading_locked=True,
        private_exchange_api_used=False,
        execution_enabled=False,
        purpose="Define a safe interface for future backtest integration without enabling live trading.",
        input_source="Deterministic fixtures and JSONL journal outputs.",
        output_target="Local reports only.",
        safety_notes=[
            "No live trading.",
            "No private exchange API.",
            "No real-money execution.",
            "No automatic FreqTrade process start.",
            "Adapter remains interface/planning only in Phase 8D.",
        ],
        planned_steps=[
            "Read deterministic fixture scenarios.",
            "Run existing multi-agent cycle per fixture.",
            "Collect final action, risk status, and confidence.",
            "Summarize backtest-readiness without executing orders.",
            "Write JSON and Markdown planning reports.",
        ],
    )


def validate_backtest_adapter_plan(plan: BacktestAdapterPlan) -> tuple[bool, list[str]]:
    errors: list[str] = []

    if plan.mode != "PAPER_ONLY":
        errors.append("mode_must_be_paper_only")

    if plan.live_trading_locked is not True:
        errors.append("live_trading_must_remain_locked")

    if plan.private_exchange_api_used is not False:
        errors.append("private_exchange_api_must_not_be_used")

    if plan.execution_enabled is not False:
        errors.append("execution_must_not_be_enabled_in_phase8d")

    if not plan.planned_steps:
        errors.append("planned_steps_missing")

    return len(errors) == 0, errors


def fixture_backtest_readiness() -> dict[str, Any]:
    runs = [run_fixture_scenario(scenario) for scenario in all_scenarios()]

    scenario_results = []
    for run in runs:
        scenario = run["scenario"]
        observed = run["observed"]
        checks = run["checks"]

        scenario_results.append(
            {
                "scenario": scenario["name"],
                "expected_trend": scenario["expected_trend"],
                "observed_trend": observed["trend"],
                "expected_candidate_action": scenario["expected_candidate_action"],
                "observed_candidate_action": observed["candidate_action"],
                "final_action": observed["final_action"],
                "risk_status": observed["risk_status"],
                "confidence": observed["confidence"],
                "paper_only": observed["mode"] == "PAPER_ONLY",
                "live_locked": observed["live_trading_locked"] is True,
                "checks_passed": all(checks.values()),
            }
        )

    return {
        "total_scenarios": len(scenario_results),
        "passed": sum(1 for item in scenario_results if item["checks_passed"]),
        "failed": sum(1 for item in scenario_results if not item["checks_passed"]),
        "results": scenario_results,
    }


def build_backtest_adapter_report() -> dict[str, Any]:
    plan = build_backtest_adapter_plan()
    valid, errors = validate_backtest_adapter_plan(plan)
    readiness = fixture_backtest_readiness()

    return {
        "ok": valid and readiness["failed"] == 0,
        "plan_valid": valid,
        "plan_errors": errors,
        "plan": plan.to_dict(),
        "fixture_readiness": readiness,
        "next_safe_step": "Phase 8E Telegram report commands, or Phase 8D2 dry-run backtest format adapter.",
    }


def write_backtest_adapter_json(path: str | Path = "reports/phase8d_backtest_adapter_plan.json") -> dict[str, Any]:
    report = build_backtest_adapter_report()
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "ok": report["ok"],
        "path": str(target),
        "summary": {
            "plan_valid": report["plan_valid"],
            "total_scenarios": report["fixture_readiness"]["total_scenarios"],
            "passed": report["fixture_readiness"]["passed"],
            "failed": report["fixture_readiness"]["failed"],
        },
    }


def render_backtest_adapter_markdown(report: dict[str, Any]) -> str:
    plan = report["plan"]
    readiness = report["fixture_readiness"]

    rows = []
    for item in readiness["results"]:
        rows.append(
            "| {scenario} | {trend} | {candidate} | {final_action} | {risk} | {confidence} | {passed} |".format(
                scenario=item["scenario"],
                trend=item["observed_trend"],
                candidate=item["observed_candidate_action"],
                final_action=item["final_action"],
                risk=item["risk_status"],
                confidence=item["confidence"],
                passed=item["checks_passed"],
            )
        )

    table = "\n".join(rows) if rows else "| - | - | - | - | - | - | - |"

    return f"""# EarnsAI Pulse — Phase 8D Backtest Adapter Plan

## Status
- OK: `{report.get("ok")}`
- Plan valid: `{report.get("plan_valid")}`
- Mode: `{plan.get("mode")}`
- Live trading locked: `{plan.get("live_trading_locked")}`
- Private exchange API used: `{plan.get("private_exchange_api_used")}`
- Execution enabled: `{plan.get("execution_enabled")}`

## Purpose
{plan.get("purpose")}

## Scope
- Input source: `{plan.get("input_source")}`
- Output target: `{plan.get("output_target")}`
- This phase defines the adapter interface only.
- This phase does not run live trading.
- This phase does not use private exchange API.

## Fixture Readiness
- Total scenarios: `{readiness.get("total_scenarios")}`
- Passed: `{readiness.get("passed")}`
- Failed: `{readiness.get("failed")}`

| Scenario | Observed Trend | Candidate Action | Final Action | Risk Status | Confidence | Passed |
|---|---|---|---|---|---|---|
{table}

## Planned Adapter Steps
{chr(10).join("- " + step for step in plan.get("planned_steps", []))}

## Safety Notes
{chr(10).join("- " + note for note in plan.get("safety_notes", []))}
"""


def write_backtest_adapter_markdown(path: str | Path = "reports/phase8d_backtest_adapter_plan.md") -> dict[str, Any]:
    report = build_backtest_adapter_report()
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_backtest_adapter_markdown(report), encoding="utf-8")
    return {
        "ok": report["ok"],
        "path": str(target),
        "summary": {
            "plan_valid": report["plan_valid"],
            "total_scenarios": report["fixture_readiness"]["total_scenarios"],
            "passed": report["fixture_readiness"]["passed"],
            "failed": report["fixture_readiness"]["failed"],
        },
    }


def write_all_backtest_adapter_reports() -> dict[str, Any]:
    json_report = write_backtest_adapter_json()
    markdown_report = write_backtest_adapter_markdown()
    return {
        "ok": json_report["ok"] and markdown_report["ok"],
        "json_path": json_report["path"],
        "markdown_path": markdown_report["path"],
        "summary": json_report["summary"],
    }
