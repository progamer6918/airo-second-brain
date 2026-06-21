#!/usr/bin/env python3
"""AIRO Finance Sheet v1.2 unified regression.

Read-only regression for v1.2 planner layer.
No credential read, no SQLite mutation, no Google write, no OpenClaw restart.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib
import sys
from typing import Any

REPO = pathlib.Path(__file__).resolve().parents[2]


def load_module(name: str, relative_path: str):
    path = REPO / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {relative_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def check(condition: bool, message: str) -> dict[str, Any]:
    return {"status": "PASS" if condition else "FAIL", "message": message}


def run_regression() -> dict[str, Any]:
    status_mod = load_module("airo_finance_sheet_v12_status", "scripts/personal-workflow/airo_finance_sheet_v12_status.py")
    review_mod = load_module("airo_review_queue_planner", "scripts/personal-workflow/airo_review_queue_planner.py")
    cash_mod = load_module("airo_cash_ledger_planner", "scripts/personal-workflow/airo_cash_ledger_planner.py")
    write_preview_mod = load_module("airo_sheets_sync_write_preview", "scripts/personal-workflow/airo_sheets_sync_write_preview.py")
    cicilan_mod = load_module("airo_cicilan_rumah_planner", "scripts/personal-workflow/airo_cicilan_rumah_planner.py")
    hutang_mod = load_module("airo_hutang_planner", "scripts/personal-workflow/airo_hutang_planner.py")
    asset_mod = load_module("airo_asset_event_planner", "scripts/personal-workflow/airo_asset_event_planner.py")

    checks: list[dict[str, Any]] = []

    status_payload = status_mod.payload()
    by_tab = {row["tab"]: row for row in status_payload["tabs"]}
    apps_script_source = (REPO / "scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs").read_text(encoding="utf-8")

    checks.append(check(status_payload["tab_count"] == 11, "status CLI reports exactly 11 tabs"))
    monthly_tab = next(row for row in status_payload["tabs"] if row["tab"].endswith("Monthly Review"))
    dashboard_tab = next(row for row in status_payload["tabs"] if row["tab"].endswith("Dashboard"))
    checks.append(check(monthly_tab["status"] == "REPORTING_ONLY", "monthly review remains reporting-only"))
    checks.append(check(monthly_tab["write_mode"] == "report_refresh_not_raw_capture", "monthly review is not raw capture target"))
    checks.append(check(dashboard_tab["status"] == "DESIGN_DONE", "dashboard remains formula-driven design surface"))
    checks.append(check("cash_reporting_formula_audit" in apps_script_source, "apps script exposes cash reporting formula audit"))
    checks.append(check("Reporting formula direfresh" in apps_script_source, "apps script exposes reporting formula refresh"))
    checks.append(check("Monthly Review" in apps_script_source and "Dashboard" in apps_script_source, "apps script references Monthly Review and Dashboard reporting surfaces"))
    cc_tab = next(row for row in status_payload["tabs"] if row["tab"].endswith("Credit Card"))
    checks.append(check(cc_tab["status"] == "FULL_AUTO_CORE_READY", "credit card remains full-auto core ready"))
    checks.append(check(cc_tab["write_mode"] == "auto_write_verified", "credit card write path remains verified"))
    checks.append(check("cc_dashboard_cycle_refresh" in apps_script_source, "cc dashboard cycle refresh command is present"))
    checks.append(check("cc_cycle_runtime_audit" in apps_script_source, "cc cycle runtime audit command is present"))
    checks.append(check("Credit Card Dashboard cycle panel direfresh" in apps_script_source, "cc dashboard refresh user message is present"))
    checks.append(check("payable_cycle" in apps_script_source and "current_cycle" in apps_script_source, "cc dashboard exposes payable and current cycle"))
    checks.append(check("status_pocket_blu" in apps_script_source, "cc dashboard tracks Pocket Blu preparation status"))
    checks.append(check("Belum ke Blu" in apps_script_source or "belum disiapkan di Pocket Blu" in apps_script_source, "cc dashboard preserves Belum ke Blu explanation"))

    for tab in ["🧾 Review Queue", "💵 Cash Ledger", "🏠 Cicilan Rumah", "🤝 Hutang"]:
        checks.append(check(by_tab[tab]["status"] == "FULL_AUTO_WRITE_PATH_READY", f"{tab} is FULL_AUTO_WRITE_PATH_READY"))

    review_plan = review_mod.plan_review_queue("kayaknya bayar sesuatu kemarin", confidence=0.30, now_iso="2026-05-11T00:00:00+00:00")
    checks.append(check(review_plan["route_to_review"] is True, "ambiguous message routes to Review Queue"))
    checks.append(check(review_plan["target_tab"] == "🧾 Review Queue", "review planner target tab is Review Queue"))
    checks.append(check(hasattr(write_preview_mod, "main"), "write preview module exposes main"))
    preview_op = {
        "target_tab": "🧾 Review Queue",
        "section": "review_queue",
        "duplicate_key": "review_queue:test_key",
        "sync_hash": "hash_v1",
        "planned_action": "insert",
        "row_preview": {"raw_text": "kayaknya bayar sesuatu kemarin"},
    }
    preview_insert = write_preview_mod.decide_operation(preview_op, {})
    preview_skip = write_preview_mod.decide_operation(preview_op, {"🧾 Review Queue": {"review_queue:test_key": "hash_v1"}})
    preview_update = write_preview_mod.decide_operation(preview_op, {"🧾 Review Queue": {"review_queue:test_key": "hash_old"}})
    checks.append(check(preview_insert.preview_action == "insert_candidate", "write preview inserts missing duplicate key"))
    checks.append(check(preview_skip.preview_action == "skip_duplicate", "write preview skips matching duplicate key"))
    checks.append(check(preview_update.preview_action == "update_candidate", "write preview detects changed sync hash"))


    cash_session = cash_mod.plan_cash_ledger("saya hari ini pegang cash 100rb", now_iso="2026-05-11T00:00:00+00:00")
    cash_entry = cash_mod.plan_cash_ledger("hari ini cash kepake beli makan 20rb", now_iso="2026-05-11T00:00:00+00:00")
    checks.append(check(cash_session["operation"] == "cash_session_candidate", "cash session candidate works"))
    checks.append(check(cash_entry["operation"] == "cash_entry_candidate", "cash entry candidate works"))
    checks.append(check(cash_entry["target_tab"] == "💵 Cash Ledger", "cash entry targets Cash Ledger"))
    cash_preview_hash = "cash_preview:" + cash_entry["duplicate_key"]
    cash_preview_op = {
        "target_tab": cash_entry["target_tab"],
        "section": cash_entry.get("section", "cash_ledger"),
        "duplicate_key": cash_entry["duplicate_key"],
        "sync_hash": cash_preview_hash,
        "planned_action": "insert",
        "row_preview": cash_entry.get("row_preview", {}),
    }
    cash_preview_insert = write_preview_mod.decide_operation(cash_preview_op, {})
    cash_preview_skip = write_preview_mod.decide_operation(cash_preview_op, {cash_entry["target_tab"]: {cash_entry["duplicate_key"]: cash_preview_hash}})
    checks.append(check(cash_preview_insert.preview_action == "insert_candidate", "cash ledger write preview inserts missing duplicate key"))
    checks.append(check(cash_preview_skip.preview_action == "skip_duplicate", "cash ledger write preview skips matching duplicate key"))

    cicilan = cicilan_mod.plan_cicilan_rumah("hari ini sudah bayar cicilan rumah", now_iso="2026-05-11T00:00:00+00:00")
    checks.append(check(cicilan["operation"] == "cicilan_rumah_payment_candidate", "cicilan rumah candidate works"))
    checks.append(check(cicilan["normalized"]["next_cicilan_ke"] == 54, "cicilan rumah next count is 54"))
    cicilan_preview_hash = "cicilan_preview:" + cicilan["duplicate_key"]
    cicilan_preview_op = {
        "target_tab": cicilan["target_tab"],
        "section": cicilan.get("section", "cicilan_rumah"),
        "duplicate_key": cicilan["duplicate_key"],
        "sync_hash": cicilan_preview_hash,
        "planned_action": "insert",
        "row_preview": cicilan.get("row_preview", {}),
    }
    cicilan_preview_insert = write_preview_mod.decide_operation(cicilan_preview_op, {})
    cicilan_preview_skip = write_preview_mod.decide_operation(cicilan_preview_op, {cicilan["target_tab"]: {cicilan["duplicate_key"]: cicilan_preview_hash}})
    checks.append(check(cicilan_preview_insert.preview_action == "insert_candidate", "cicilan rumah write preview inserts missing duplicate key"))
    checks.append(check(cicilan_preview_skip.preview_action == "skip_duplicate", "cicilan rumah write preview skips matching duplicate key"))

    hutang = hutang_mod.plan_hutang("hari ini bayar hutang ke mamak egit 1 juta", now_iso="2026-05-11T00:00:00+00:00")
    checks.append(check(hutang["operation"] == "hutang_payment_candidate", "hutang payment candidate works"))
    checks.append(check(hutang["normalized"]["balance_after"] == 14000000, "hutang remaining balance preview works"))
    hutang_preview_hash = "hutang_preview:" + hutang["duplicate_key"]
    hutang_preview_op = {
        "target_tab": hutang["target_tab"],
        "section": hutang.get("section", "hutang"),
        "duplicate_key": hutang["duplicate_key"],
        "sync_hash": hutang_preview_hash,
        "planned_action": "insert",
        "row_preview": hutang.get("row_preview", {}),
    }
    hutang_preview_insert = write_preview_mod.decide_operation(hutang_preview_op, {})
    hutang_preview_skip = write_preview_mod.decide_operation(hutang_preview_op, {hutang["target_tab"]: {hutang["duplicate_key"]: hutang_preview_hash}})
    checks.append(check(hutang_preview_insert.preview_action == "insert_candidate", "hutang write preview inserts missing duplicate key"))
    checks.append(check(hutang_preview_skip.preview_action == "skip_duplicate", "hutang write preview skips matching duplicate key"))
    asset_rows = [
        {
            "transaction_id": "asset_savings_test_1",
            "date": "2026-05-11",
            "raw_text": "nabung 500rb dari bca ke blu dana darurat",
            "amount": 500000,
            "source": "regression",
        },
        {
            "transaction_id": "asset_gold_test_1",
            "date": "2026-05-11",
            "raw_text": "beli emas 2 gram harga 3jt pakai bca",
            "amount": 3000000,
            "source": "regression",
        },
    ]
    asset_plans_raw = asset_mod.plan_asset_events_from_transactions(asset_rows)
    asset_plans = [item if isinstance(item, dict) else getattr(item, "__dict__", {}) for item in asset_plans_raw]
    asset_savings = next(item for item in asset_plans if item.get("section") == "savings_transfer_ledger")
    asset_gold = next(item for item in asset_plans if item.get("section") == "gold_ledger")
    checks.append(check(asset_savings["target_tab"] == asset_mod.ASSET_TAB, "asset savings planner targets Aset"))
    checks.append(check(asset_savings["section"] == "savings_transfer_ledger", "asset savings planner detects savings movement"))
    checks.append(check(asset_gold["target_tab"] == asset_mod.ASSET_TAB, "asset gold planner targets Aset"))
    checks.append(check(asset_gold["section"] == "gold_ledger", "asset gold planner detects gold movement"))
    asset_savings_preview_op = {
        "target_tab": asset_savings["target_tab"],
        "section": asset_savings["section"],
        "duplicate_key": asset_savings["duplicate_key"],
        "sync_hash": asset_savings["sync_hash"],
        "planned_action": "insert",
        "row_preview": asset_savings.get("row", {}),
    }
    asset_savings_preview = write_preview_mod.decide_operation(asset_savings_preview_op, {})
    asset_savings_skip = write_preview_mod.decide_operation(
        asset_savings_preview_op,
        {asset_savings["target_tab"] + "::" + asset_savings["section"]: {asset_savings["duplicate_key"]: asset_savings["sync_hash"]}},
    )
    checks.append(check(asset_savings_preview.preview_action == "insert_candidate", "asset savings write preview inserts missing duplicate key"))
    checks.append(check(asset_savings_skip.preview_action == "skip_duplicate", "asset savings write preview skips matching duplicate key"))

    safety_flags = [
        review_plan,
        cash_session,
        cash_entry,
        cicilan,
        hutang,
    ]
    for idx, item in enumerate(safety_flags, start=1):
        checks.append(check(item["google_write_performed"] is False, f"safety {idx}: no Google write"))
        checks.append(check(item["sqlite_mutation_performed"] is False, f"safety {idx}: no SQLite mutation"))
        checks.append(check(item["credential_read_performed"] is False, f"safety {idx}: no credential read"))
        checks.append(check(item["openclaw_restart_performed"] is False, f"safety {idx}: no OpenClaw restart"))

    failed = [item for item in checks if item["status"] != "PASS"]

    return {
        "regression": "airo_finance_sheet_v12_unified",
        "status": "PASS" if not failed else "FAIL",
        "checks_total": len(checks),
        "checks_failed": len(failed),
        "checks": checks,
        "safety": {
            "google_write_performed": False,
            "sqlite_mutation_performed": False,
            "credential_read_performed": False,
            "openclaw_restart_performed": False,
        },
    }


def render_text(payload: dict[str, Any]) -> str:
    lines = [
        "AIRO Finance Sheet v1.2 Unified Regression",
        f"Status: {payload["status"]}",
        f"Checks: {payload["checks_total"]}",
        f"Failed: {payload["checks_failed"]}",
        "",
        "Checks:",
    ]
    for item in payload["checks"]:
        lines.append(f"- {item["status"]}: {item["message"]}")
    lines.extend([
        "",
        "Safety: no Google write, no SQLite mutation, no credential read, no OpenClaw restart",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run AIRO Finance Sheet v1.2 unified read-only regression.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    payload = run_regression()
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_text(payload))

    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
