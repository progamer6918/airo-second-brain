#!/usr/bin/env python3
"""
AIRO Full Auto Sheets Sync v1.1.

Full-auto core scope:
- 💸 Transactions
- 💳 Credit Card
- 🔄 Sync Log

No per-write approval phrase.
No Apps Script paste per transaction.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_DIR = SCRIPT_DIR.parents[1]
WRITE_PREVIEW = SCRIPT_DIR / "airo_sheets_sync_write_preview.py"
CLIENT_PATH = SCRIPT_DIR / "airo_google_sheets_client.py"


TRANSACTION_HEADERS = [
    "transaction_id", "date", "month", "type", "category", "subcategory",
    "description", "merchant", "amount", "account", "source", "status",
    "confidence", "raw_text", "synced_at", "notes", "currency", "review_status",
    "local_db_table", "local_db_rowid", "sync_hash", "duplicate_key",
    "created_at", "updated_at", "from_account", "to_account", "transfer_purpose",
    "asset_bucket", "pocket_name", "cashflow_treatment",
]

CREDIT_CARD_HEADERS = [
    "cc_entry_id", "date", "merchant_app", "amount", "description",
    "status_pocket_blu", "transferred_at", "linked_txn_id", "notes",
    "billing_cycle_id", "billing_start", "billing_end", "statement_month",
    "due_date", "is_statement_locked",
]

SYNC_LOG_HEADERS = [
    "sync_id", "run_id", "source_db", "source_table", "source_rowid",
    "target_tab", "transaction_id", "action", "status", "records_seen",
    "records_inserted", "records_updated", "records_skipped", "records_failed",
    "error_message", "started_at", "finished_at", "synced_at", "notes",
]


ASSET_SAVINGS_HEADERS = [
    "savings_event_id", "date", "type", "from_account", "to_account",
    "purpose", "amount", "source", "raw_text", "linked_transaction_id",
    "sync_hash", "notes",
]

ASSET_GOLD_HEADERS = [
    "gold_event_id", "date", "action", "grams_in", "grams_out",
    "price_per_gram", "fee", "total_amount", "source_account", "source",
    "raw_text", "sync_hash", "notes",
]


def asset_append_range(section: str) -> str:
    if section == "savings_transfer_ledger":
        return "O3:Z"
    if section == "gold_ledger":
        return "A24:M"
    raise ValueError(f"Unsupported 🥇 Aset section: {section}")

def asset_update_range(section: str, row_number: int) -> str:
    if section == "savings_transfer_ledger":
        return f"O{row_number}:Z{row_number}"
    if section == "gold_ledger":
        return f"A{row_number}:M{row_number}"
    raise ValueError(f"Unsupported 🥇 Aset section: {section}")




@dataclass
class ApplyResult:
    target_tab: str
    duplicate_key: str
    action: str
    status: str
    row_count: int
    message: str


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module: {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def now_jakarta_like() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def run_write_preview(snapshot_path: Path) -> dict[str, Any]:
    proc = subprocess.run(
        [sys.executable, str(WRITE_PREVIEW), "--sheet-snapshot", str(snapshot_path)],
        cwd=str(REPO_DIR),
        text=True,
        capture_output=True,
        check=False,
    )

    if proc.returncode != 0:
        raise RuntimeError(
            "write_preview failed\nSTDOUT:\n"
            + proc.stdout
            + "\nSTDERR:\n"
            + proc.stderr
        )

    return json.loads(proc.stdout)


def write_snapshot_file(snapshot: dict[str, Any], path: Path) -> None:
    path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")


def load_snapshot(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def row_from_headers(headers: list[str], row_preview: dict[str, Any]) -> list[Any]:
    return ["" if row_preview.get(h) is None else row_preview.get(h, "") for h in headers]



V13_REVIEW_QUEUE_HEADERS = ["queue_id","created_at","source","raw_text","intent","target_tab","reason","confidence","amount","account","category","status","resolution","resolved_at","resolved_by","sync_hash","notes","parser","duplicate_key","metadata"]
V13_CASH_SESSION_HEADERS = ["session_id","date","opening_cash","source","status","created_at","sync_hash","notes"]
V13_CASH_ENTRY_HEADERS = ["entry_id","session_id","date","description","category","amount","direction","balance_after","source","sync_hash","notes"]
V13_CICILAN_RUMAH_HEADERS = ["payment_id","date","cicilan_ke","amount","standard_installment","usual_paid_amount","remaining_after_payment","total_tenor","due_day","source","sync_hash","notes"]
V13_HUTANG_HEADERS = ["payment_id","date","debt_id","creditor","amount","account","balance_before","balance_after","source","sync_hash","notes"]

def v13_range_for(target_tab: str, section: str = "") -> str | None:
    if target_tab == "💵 Cash Ledger" and section == "cash_session":
        return "A2:H"
    if target_tab == "💵 Cash Ledger" and section == "cash_entry":
        return "J2:T"
    return None

def target_headers(target_tab: str, section: str = "") -> list[str]:
    # AIRO_V13_SPECIAL_TAB_HEADERS
    special_headers = {
        "💵 Cash Ledger": [
            "date", "entry_type", "direction", "amount", "category", "account",
            "description", "notes", "duplicate_key", "raw_text", "source",
            "status", "created_at", "local_db_table", "local_db_rowid"
        ],
        "🏠 Cicilan Rumah": [
            "payment_id", "cicilan_ke", "date_paid", "amount_paid", "status",
            "notes", "duplicate_key", "raw_text", "source", "local_db_table",
            "local_db_rowid"
        ],
        "🤝 Hutang": [
            "payment_id", "debt_id", "creditor", "date_paid", "amount_paid",
            "account", "balance_before", "balance_after", "status", "notes",
            "duplicate_key", "raw_text", "source", "local_db_table", "local_db_rowid"
        ],
    }
    if not section and target_tab in special_headers:
        return special_headers[target_tab]

    if target_tab == "💸 Transactions":
        return TRANSACTION_HEADERS
    if target_tab == "💳 Credit Card":
        return CREDIT_CARD_HEADERS
    if target_tab == "🔄 Sync Log":
        return SYNC_LOG_HEADERS
    if target_tab == "🥇 Aset" and section == "savings_transfer_ledger":
        return ASSET_SAVINGS_HEADERS
    if target_tab == "🥇 Aset" and section == "gold_ledger":
        return ASSET_GOLD_HEADERS
    if target_tab == "🧾 Review Queue":
        return V13_REVIEW_QUEUE_HEADERS
    if target_tab == "💵 Cash Ledger" and section == "cash_session":
        return V13_CASH_SESSION_HEADERS
    if target_tab == "💵 Cash Ledger" and section == "cash_entry":
        return V13_CASH_ENTRY_HEADERS
    if target_tab == "🏠 Cicilan Rumah":
        return V13_CICILAN_RUMAH_HEADERS
    if target_tab == "🤝 Hutang":
        return V13_HUTANG_HEADERS
    raise ValueError(f"Unsupported target tab/section: {target_tab} / {section}")


def snapshot_lookup_key(target_tab: str, section: str = "") -> str:
    if target_tab == "🥇 Aset" and section:
        return f"{target_tab}::{section}"
    return target_tab


def find_existing_row(snapshot: dict[str, Any], target_tab: str, duplicate_key: str, section: str = "") -> int | None:
    lookup_key = snapshot_lookup_key(target_tab, section)
    for item in (snapshot.get("tabs") or {}).get(lookup_key, []):
        if str(item.get("duplicate_key") or "") == str(duplicate_key or ""):
            row_number = item.get("row_number")
            return int(row_number) if row_number else None

    return None


def build_sync_log_row(run_id: str, decision: dict[str, Any], action: str, status: str, message: str) -> list[Any]:
    timestamp = now_jakarta_like()
    row = decision.get("row_preview") or {}
    transaction_id = (
        row.get("transaction_id")
        or row.get("linked_txn_id")
        or row.get("savings_event_id")
        or row.get("gold_event_id")
        or decision.get("entity_id")
        or decision.get("duplicate_key")
        or ""
    )

    return [
        "sync_auto_" + datetime.now().strftime("%Y%m%d%H%M%S%f")[-16:],
        run_id,
        "local_sqlite",
        decision.get("source_table", "transactions"),
        decision.get("source_rowid", ""),
        decision.get("target_tab", ""),
        transaction_id,
        action,
        status,
        1,
        1 if status == "success" else 0,
        1 if action == "update" and status == "success" else 0,
        0 if status == "success" else 1,
        0 if status == "success" else 1,
        "" if status == "success" else message,
        timestamp,
        timestamp,
        timestamp,
        message,
    ]


def filter_write_decisions(preview: dict[str, Any]) -> list[dict[str, Any]]:
    allowed_core = {"💸 Transactions", "💳 Credit Card", "🧾 Review Queue", "💵 Cash Ledger", "🏠 Cicilan Rumah", "🤝 Hutang"}
    out: list[dict[str, Any]] = []

    for decision in preview.get("decisions", []):
        target_tab = str(decision.get("target_tab") or "")
        action = str(decision.get("preview_action") or "")

        if target_tab in allowed_core and action in {"insert_candidate", "update_candidate"}:
            out.append(decision)
            continue

        if target_tab == "🥇 Aset" and action in {"insert_candidate", "update_candidate"}:
            out.append(decision)

    return out


def apply_decision(client, snapshot: dict[str, Any], decision: dict[str, Any], run_id: str) -> ApplyResult:
    target_tab = str(decision.get("target_tab") or "")
    duplicate_key = str(decision.get("duplicate_key") or "")
    preview_action = str(decision.get("preview_action") or "")
    row_preview = decision.get("row_preview") or {}
    section = str(decision.get("section") or "")
    values = row_from_headers(target_headers(target_tab, section), row_preview)

    if preview_action == "insert_candidate":
        if target_tab == "🥇 Aset":
            client.append_values_to_range(target_tab, asset_append_range(section), values)
            result = ApplyResult(target_tab, duplicate_key, "insert", "success", 1, f"full_auto_v1_2 asset insert:{section}")
        else:
            v13_range = v13_range_for(target_tab, section)
            if v13_range:
                client.append_values_to_range(target_tab, v13_range, values)
            else:
                client.append_values(target_tab, values)
            result = ApplyResult(target_tab, duplicate_key, "insert", "success", 1, "full_auto_v1_3 insert")
    elif preview_action == "update_candidate":
        row_number = find_existing_row(snapshot, target_tab, duplicate_key, section)
        if row_number is None:
            if target_tab == "🥇 Aset":
                result = ApplyResult(
                    target_tab,
                    duplicate_key,
                    "missing_row",
                    "failed",
                    0,
                    f"asset update row not found for section:{section}; refusing insert_fallback",
                )
            else:
                client.append_values(target_tab, values)
                result = ApplyResult(target_tab, duplicate_key, "insert_fallback", "success", 1, "full_auto_v1_1 update_missing_row_inserted")
        else:
            if target_tab == "🥇 Aset":
                client.update_values_to_range(target_tab, asset_update_range(section, row_number), values)
                result = ApplyResult(target_tab, duplicate_key, "update", "success", 1, f"full_auto_v1_2 asset update:{section}")
            else:
                client.update_values(target_tab, row_number, values)
                result = ApplyResult(target_tab, duplicate_key, "update", "success", 1, "full_auto_v1_1 update")
    else:
        result = ApplyResult(target_tab, duplicate_key, "skip", "skipped", 0, "not a write candidate")

    client.append_values("🔄 Sync Log", build_sync_log_row(run_id, decision, result.action, result.status, result.message))
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AIRO Full Auto Sheets Sync v1.1")
    parser.add_argument("--mode", choices=["dry-run", "apply"], default="dry-run")
    parser.add_argument("--target-tab", default="", help="Optional exact target tab filter, for example 🧾 Review Queue")
    parser.add_argument("--sheet-snapshot", default="", help="Optional existing key snapshot JSON. Avoids Google read in dry-run.")
    parser.add_argument("--snapshot-out", default="/tmp/airo_full_auto_sheets_sync_snapshot.json")
    parser.add_argument("--preview-out", default="/tmp/airo_full_auto_sheets_sync_preview.json")
    parser.add_argument("--report-out", default="", help="Optional path to write the final full-auto report JSON.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    snapshot_path = Path(args.sheet_snapshot).expanduser() if args.sheet_snapshot else Path(args.snapshot_out).expanduser()
    preview_out = Path(args.preview_out).expanduser()

    google_read_performed = False
    google_write_performed = False

    if args.sheet_snapshot:
        snapshot = load_snapshot(snapshot_path)
    else:
        client_mod = load_module(CLIENT_PATH, "airo_google_sheets_client")
        client = None if args.mode == "dry-run" else client_mod.build_client_from_env()
        snapshot = client.export_sheet_keys() if client is not None else {"tabs": {}}
        write_snapshot_file(snapshot, snapshot_path)
        google_read_performed = True

    preview = run_write_preview(snapshot_path)
    preview_out.write_text(json.dumps(preview, ensure_ascii=False, indent=2), encoding="utf-8")

    write_decisions = filter_write_decisions(preview)
    if args.target_tab:
        write_decisions = [d for d in write_decisions if str(d.get("target_tab") or "") == args.target_tab]
    results: list[ApplyResult] = []

    run_id = "full_auto_v1_2_" + datetime.now().strftime("%Y%m%d_%H%M%S")

    if args.mode == "apply" and write_decisions:
        client_mod = load_module(CLIENT_PATH, "airo_google_sheets_client")
        client = client_mod.build_client_from_env()

        for decision in write_decisions:
            results.append(apply_decision(client, snapshot, decision, run_id))

        google_write_performed = bool(results)

    # AIRO_FULL_AUTO_REPORT_OUT_V111
    report = {
        "title": "AIRO FULL AUTO SHEETS SYNC",
        "version": "v1.2",
        "mode": args.mode,
        "run_id": run_id,
        "google_read_performed": google_read_performed,
        "google_write_performed": google_write_performed,
        "snapshot_path": str(snapshot_path),
        "preview_out": str(preview_out),
        "preview_summary": preview.get("summary"),
        "write_candidate_count": len(write_decisions),
        "write_candidates": [
            {
                "target_tab": d.get("target_tab"),
                "section": d.get("section"),
                "preview_action": d.get("preview_action"),
                "duplicate_key": d.get("duplicate_key"),
                "amount": (d.get("row_preview") or {}).get("amount"),
                "billing_cycle_id": (d.get("row_preview") or {}).get("billing_cycle_id"),
            }
            for d in write_decisions
        ],
        "apply_results": [asdict(r) for r in results],
        "scope": [args.target_tab] if args.target_tab else ["💸 Transactions", "💳 Credit Card", "🥇 Aset", "🧾 Review Queue", "💵 Cash Ledger", "🏠 Cicilan Rumah", "🤝 Hutang", "🔄 Sync Log"],
        "approval_phrase_required": False,
    }

    if args.report_out:
        Path(args.report_out).expanduser().write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
