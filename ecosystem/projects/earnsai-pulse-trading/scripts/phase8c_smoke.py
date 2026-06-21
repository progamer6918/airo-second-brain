#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from earnsai.data.fixtures import all_scenarios, fixture_catalog, get_scenario
from earnsai.evaluation.fixture_runner import run_all_fixtures, run_fixture_scenario, write_all_fixture_reports


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    scenarios = all_scenarios()
    catalog = fixture_catalog()

    assert_true(len(scenarios) >= 4, "must provide at least four deterministic scenarios")
    assert_true(set(catalog.keys()) >= {"bullish", "bearish", "flat", "volatile"}, "missing required scenarios")

    bullish = run_fixture_scenario(get_scenario("bullish"))
    bearish = run_fixture_scenario(get_scenario("bearish"))
    flat = run_fixture_scenario(get_scenario("flat"))

    assert_true(bullish["checks"]["trend_matches"], "bullish trend must match")
    assert_true(bullish["checks"]["candidate_action_matches"], "bullish action must match")
    assert_true(bearish["checks"]["trend_matches"], "bearish trend must match")
    assert_true(bearish["checks"]["candidate_action_matches"], "bearish action must match")
    assert_true(flat["checks"]["trend_matches"], "flat trend must match")
    assert_true(flat["checks"]["candidate_action_matches"], "flat action must match")

    report = run_all_fixtures()
    assert_true(report["ok"] is True, "all fixture scenarios must pass")
    assert_true(report["summary"]["failed"] == 0, "fixture report must have zero failures")

    written = write_all_fixture_reports()
    assert_true(written["ok"] is True, "fixture reports must be ok")

    json_path = ROOT / written["json_path"]
    markdown_path = ROOT / written["markdown_path"]

    assert_true(json_path.exists(), "fixture JSON report must exist")
    assert_true(markdown_path.exists(), "fixture Markdown report must exist")

    parsed = json.loads(json_path.read_text(encoding="utf-8"))
    assert_true(parsed["summary"]["total"] >= 4, "json report must include scenarios")

    print(
        "PHASE8C_SMOKE PASS "
        f"scenarios={report['summary']['total']} "
        f"passed={report['summary']['passed']} "
        f"failed={report['summary']['failed']} "
        f"json={written['json_path']} "
        f"md={written['markdown_path']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
