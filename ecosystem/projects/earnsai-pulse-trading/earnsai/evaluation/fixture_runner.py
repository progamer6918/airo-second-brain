from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from earnsai.agents.orchestrator import run_multi_agent_cycle
from earnsai.data.fixtures import PriceScenario, all_scenarios, fixture_catalog


def run_fixture_scenario(scenario: PriceScenario) -> dict[str, Any]:
    result = run_multi_agent_cycle(scenario.to_context())

    agents = result.get("agents", {})
    technical = agents.get("technical", {}).get("data", {})
    strategy = agents.get("strategy", {}).get("data", {})
    signal = result.get("signal", {})

    observed_trend = technical.get("trend")
    observed_candidate_action = strategy.get("candidate_action")

    return {
        "scenario": scenario.to_dict(),
        "observed": {
            "trend": observed_trend,
            "candidate_action": observed_candidate_action,
            "final_action": signal.get("action"),
            "risk_status": signal.get("risk_status"),
            "confidence": signal.get("confidence"),
            "mode": signal.get("mode"),
            "live_trading_locked": signal.get("live_trading_locked"),
        },
        "checks": {
            "trend_matches": observed_trend == scenario.expected_trend,
            "candidate_action_matches": observed_candidate_action == scenario.expected_candidate_action,
            "paper_only": signal.get("mode") == "PAPER_ONLY",
            "live_locked": signal.get("live_trading_locked") is True,
            "risk_status_valid": signal.get("risk_status") in {"APPROVED_FOR_PAPER_ONLY", "REJECTED", "BLOCKED"},
        },
        "raw_result": result,
    }


def run_all_fixtures() -> dict[str, Any]:
    runs = [run_fixture_scenario(scenario) for scenario in all_scenarios()]
    passed = all(
        run["checks"]["trend_matches"]
        and run["checks"]["candidate_action_matches"]
        and run["checks"]["paper_only"]
        and run["checks"]["live_locked"]
        and run["checks"]["risk_status_valid"]
        for run in runs
    )

    return {
        "ok": passed,
        "catalog": fixture_catalog(),
        "runs": runs,
        "summary": {
            "total": len(runs),
            "passed": sum(1 for run in runs if all(run["checks"].values())),
            "failed": sum(1 for run in runs if not all(run["checks"].values())),
            "final_actions": {
                run["scenario"]["name"]: run["observed"]["final_action"]
                for run in runs
            },
            "risk_statuses": {
                run["scenario"]["name"]: run["observed"]["risk_status"]
                for run in runs
            },
        },
    }


def write_fixture_report_json(path: str | Path = "reports/phase8c_fixture_report.json") -> dict[str, Any]:
    report = run_all_fixtures()
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "ok": report["ok"],
        "path": str(target),
        "summary": report["summary"],
    }


def render_fixture_report_markdown(report: dict[str, Any]) -> str:
    rows = []
    for run in report["runs"]:
        scenario = run["scenario"]
        observed = run["observed"]
        checks = run["checks"]
        rows.append(
            "| {name} | {expected_trend} | {trend} | {expected_action} | {candidate} | {final_action} | {risk} | {passed} |".format(
                name=scenario["name"],
                expected_trend=scenario["expected_trend"],
                trend=observed["trend"],
                expected_action=scenario["expected_candidate_action"],
                candidate=observed["candidate_action"],
                final_action=observed["final_action"],
                risk=observed["risk_status"],
                passed=all(checks.values()),
            )
        )

    table = "\n".join(rows)

    return f"""# EarnsAI Pulse — Phase 8C Fixture Report

## Summary
- OK: `{report.get("ok")}`
- Total scenarios: `{report["summary"]["total"]}`
- Passed: `{report["summary"]["passed"]}`
- Failed: `{report["summary"]["failed"]}`

## Scenario Results

| Scenario | Expected Trend | Observed Trend | Expected Candidate | Observed Candidate | Final Action | Risk Status | Passed |
|---|---|---|---|---|---|---|---|
{table}

## Safety
- All fixture runs remain paper-only.
- Live trading remains locked.
- Private exchange API is not used.
- This report is deterministic and intended for evaluation hardening.
"""


def write_fixture_report_markdown(path: str | Path = "reports/phase8c_fixture_report.md") -> dict[str, Any]:
    report = run_all_fixtures()
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_fixture_report_markdown(report), encoding="utf-8")
    return {
        "ok": report["ok"],
        "path": str(target),
        "summary": report["summary"],
    }


def write_all_fixture_reports() -> dict[str, Any]:
    json_report = write_fixture_report_json()
    markdown_report = write_fixture_report_markdown()
    return {
        "ok": json_report["ok"] and markdown_report["ok"],
        "json_path": json_report["path"],
        "markdown_path": markdown_report["path"],
        "summary": json_report["summary"],
    }
