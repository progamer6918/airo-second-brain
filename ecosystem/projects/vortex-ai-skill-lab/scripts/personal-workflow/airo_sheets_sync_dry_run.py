#!/usr/bin/env python3
"""
AIRO Google Sheets Sync Dry-run Mapper v0.1.

Dry-run only:
- Reads SQLite.
- Builds planned Google Sheet operations in memory.
- Prints redacted JSON.
- Performs no Google write.
- Reads no credentials.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sqlite3
import sys
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

ASSET_PLANNER_SCRIPT = Path(__file__).resolve().with_name("airo_asset_event_planner.py")
from typing import Any

# AIRO_ALIAS_RESCUE_V05
import importlib.util as _airo_alias_importlib_util

_AIRO_ACCOUNT_ALIASES_PATH = Path(__file__).resolve().with_name("airo_account_aliases.py")
if _AIRO_ACCOUNT_ALIASES_PATH.exists():
    _spec = _airo_alias_importlib_util.spec_from_file_location("airo_account_aliases", _AIRO_ACCOUNT_ALIASES_PATH)
    _airo_alias_mod = _airo_alias_importlib_util.module_from_spec(_spec)
    assert _spec is not None and _spec.loader is not None
    _spec.loader.exec_module(_airo_alias_mod)
    normalize_account_alias = _airo_alias_mod.normalize_account_alias
    extract_account_from_text = _airo_alias_mod.extract_account_from_text
else:
    normalize_account_alias = None
    extract_account_from_text = None

KNOWN_CATEGORY_MAP = {
    "makan": "Makan",
    "makanan": "Makan",
    "belanja": "Belanja",
    "transport": "Transport",
    "tagihan": "Tagihan",
    "digital": "Digital",
    "cicilan": "Cicilan",
    "hutang": "Hutang",
    "aset": "Aset",
    "tabungan": "Tabungan",
}

VALIDATION_MARKERS = ["validasi-persistent-db", "TXN-SAMPLE-001"]
SUSPICIOUS_AMOUNT_LIMIT = 1_000_000_000


@dataclass
class PlannedOperation:
    target_tab: str
    action: str
    source_table: str
    source_rowid: int | None
    entity_id: str | None
    duplicate_key: str
    sync_hash: str
    reason: str
    row_preview: dict[str, Any]
    section: str = ""


def stable_hash(parts: list[Any]) -> str:
    payload = "|".join("" if p is None else str(p) for p in parts)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]


def truncate(value: Any, limit: int = 160) -> Any:
    if value is None:
        return None
    text = str(value)
    return text[:limit] + ("..." if len(text) > limit else "")


def contains_marker(*values: Any) -> bool:
    blob = " ".join("" if v is None else str(v) for v in values).lower()
    return any(marker.lower() in blob for marker in VALIDATION_MARKERS)


def normalize_category(value: Any) -> tuple[str, str]:
    if value is None or str(value).strip() == "":
        return "Lainnya", "missing_category"
    raw = str(value).strip()
    key = raw.lower()
    if key in KNOWN_CATEGORY_MAP:
        return KNOWN_CATEGORY_MAP[key], "mapped"
    return raw.title(), "unknown_category"


def month_from_date(value: Any) -> str:
    if not value:
        return ""
    text = str(value)
    return text[:7] if len(text) >= 7 else text


def is_tokopedia_cc(*values: Any) -> bool:
    blob = " ".join("" if v is None else str(v) for v in values).lower()
    return "tokopedia credit card" in blob or "tokopedia cc" in blob


def connect(db_path: Path) -> sqlite3.Connection:
    con = sqlite3.connect(str(db_path))
    con.row_factory = sqlite3.Row
    return con


def get_tables(cur: sqlite3.Cursor) -> set[str]:
    return {
        row["name"]
        for row in cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
    }


def account_lookup(cur: sqlite3.Cursor, tables: set[str]) -> dict[str, dict[str, Any]]:
    if "accounts" not in tables:
        return {}
    rows = cur.execute("SELECT rowid, * FROM accounts").fetchall()
    return {row["id"]: dict(row) for row in rows}


def resolve_account_alias_for_sync(value: Any, raw_text: Any = None) -> str:
    """Resolve account alias from payment_method/account fields or raw note text."""
    for candidate in (value,):
        if candidate and normalize_account_alias is not None:
            resolved = normalize_account_alias(str(candidate))
            if resolved:
                return resolved

    if raw_text and extract_account_from_text is not None:
        resolved = extract_account_from_text(str(raw_text))
        if resolved:
            return resolved

    return "" if value is None else str(value)

def load_asset_planner_module():
    if not ASSET_PLANNER_SCRIPT.is_file():
        return None

    spec = importlib.util.spec_from_file_location("airo_asset_event_planner", ASSET_PLANNER_SCRIPT)
    if spec is None or spec.loader is None:
        return None

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def classify_cashflow_for_sync(note: Any, category: Any) -> tuple[str, str]:
    text = str(note or "").lower()
    cat = str(category or "").strip().lower()

    if any(word in text for word in ("nabung", "tabung", "simpan")) or cat == "tabungan":
        return "asset_transfer", "transfer"

    if "transfer" in text and " dari " in f" {text} " and " ke " in f" {text} ":
        return "internal_transfer", "transfer"

    if any(word in text for word in ("tarik", "withdraw", "ambil")) and " dari " in f" {text} ":
        return "internal_transfer", "transfer"

    if "topup" in text or "top up" in text or "isi saldo" in text:
        return "internal_transfer", "transfer"

    if "emas" in text or "gold" in text or cat == "investasi":
        return "asset_purchase", "asset_purchase"

    return "operating_expense", "expense"


def plan_transaction(row: sqlite3.Row, account_by_id: dict[str, dict[str, Any]]) -> list[PlannedOperation]:
    if "deleted_at" in row.keys() and row["deleted_at"]:
        return []

    item = dict(row)
    rowid = item.get("rowid")
    txid = item.get("id")

    account = account_by_id.get(item.get("account_id") or "")
    account_name = resolve_account_alias_for_sync((account or {}).get("name") or item.get("payment_method") or "", item.get("note"))

    sync_hash = stable_hash([
        "transactions",
        txid,
        item.get("transaction_date"),
        item.get("account_id"),
        item.get("merchant"),
        item.get("category"),
        item.get("amount"),
        item.get("currency"),
        item.get("payment_method"),
        item.get("status"),
        item.get("source"),
        item.get("created_at"),
        item.get("updated_at"),
    ])

    if item.get("deleted_at"):
        return [PlannedOperation(
            target_tab="NO_WRITE",
            action="skip_deleted",
            source_table="transactions",
            source_rowid=rowid,
            entity_id=txid,
            duplicate_key=f"transactions:{txid}",
            sync_hash=sync_hash,
            reason="deleted_at is set",
            row_preview={"transaction_id": txid, "deleted_at": item.get("deleted_at")},
        )]

    if contains_marker(item.get("note"), item.get("merchant"), item.get("payment_method")):
        return [PlannedOperation(
            target_tab="NO_WRITE",
            action="skip_validation_marker",
            source_table="transactions",
            source_rowid=rowid,
            entity_id=txid,
            duplicate_key=f"transactions:{txid}",
            sync_hash=sync_hash,
            reason="validation marker detected in note/merchant/payment_method",
            row_preview={
                "transaction_id": txid,
                "date": item.get("transaction_date"),
                "amount": item.get("amount"),
                "merchant": item.get("merchant"),
                "note": truncate(item.get("note")),
            },
        )]

    amount = item.get("amount")
    amount_problem = False
    try:
        amount_int = int(amount)
        amount_problem = amount_int <= 0 or amount_int > SUSPICIOUS_AMOUNT_LIMIT
    except Exception:
        amount_int = amount
        amount_problem = True

    category, category_status = normalize_category(item.get("category"))

    if amount_problem:
        return [PlannedOperation(
            target_tab="🧾 Review Queue",
            action="route_review_queue",
            source_table="transactions",
            source_rowid=rowid,
            entity_id=txid,
            duplicate_key=f"review:transactions:{rowid}",
            sync_hash=sync_hash,
            reason="suspicious or invalid amount",
            row_preview={
                "queue_id": f"review_transactions_{rowid}",
                "created_at": item.get("created_at"),
                "source": item.get("source"),
                "raw_text": truncate(item.get("note")),
                "parsed_type": "expense",
                "parsed_category": category,
                "parsed_amount": amount,
                "issue_reason": "suspicious_amount",
                "review_status": "pending",
                "local_db_table": "transactions",
                "local_db_rowid": rowid,
                "sync_hash": sync_hash,
            },
        )]

    needs_review = False
    review_reasons: list[str] = []

    if category_status == "missing_category":
        needs_review = True
        review_reasons.append("missing_category")
    elif category_status == "unknown_category":
        review_reasons.append("unknown_category")

    if item.get("account_id") and not account:
        needs_review = True
        review_reasons.append("account_id_not_found")

    if needs_review:
        return [PlannedOperation(
            target_tab="🧾 Review Queue",
            action="route_review_queue",
            source_table="transactions",
            source_rowid=rowid,
            entity_id=txid,
            duplicate_key=f"review:transactions:{rowid}",
            sync_hash=sync_hash,
            reason=";".join(review_reasons),
            row_preview={
                "queue_id": f"review_transactions_{rowid}",
                "created_at": item.get("created_at"),
                "source": item.get("source"),
                "raw_text": truncate(item.get("note")),
                "parsed_type": "expense",
                "parsed_category": category,
                "parsed_amount": amount_int,
                "parsed_currency": item.get("currency") or "IDR",
                "parsed_account": account_name,
                "issue_reason": ";".join(review_reasons),
                "review_status": "pending",
                "local_db_table": "transactions",
                "local_db_rowid": rowid,
                "sync_hash": sync_hash,
            },
        )]

    cashflow_treatment, transaction_type = classify_cashflow_for_sync(item.get("note"), category)

    tx_preview = {
        "transaction_id": txid,
        "date": item.get("transaction_date"),
        "month": month_from_date(item.get("transaction_date")),
        "type": transaction_type,
        "category": category,
        "subcategory": "",
        "description": truncate(item.get("note"), 80) or item.get("merchant") or "",
        "merchant": item.get("merchant") or "",
        "amount": amount_int,
        "account": account_name,
        "source": item.get("source") or "sqlite",
        "status": "synced",
        "confidence": 0.90,
        "raw_text": truncate(item.get("note")),
        "synced_at": "",
        "notes": "",
        "currency": item.get("currency") or "IDR",
        "review_status": "auto_approved",
        "local_db_table": "transactions",
        "local_db_rowid": rowid,
        "sync_hash": sync_hash,
        "duplicate_key": f"transactions:{txid}",
        "created_at": item.get("created_at"),
        "updated_at": item.get("updated_at"),
        "from_account": "",
        "to_account": "",
        "transfer_purpose": "",
        "asset_bucket": "",
        "pocket_name": "",
        "cashflow_treatment": cashflow_treatment,
    }

    ops = [PlannedOperation(
        target_tab="💸 Transactions",
        action="insert_or_update",
        source_table="transactions",
        source_rowid=rowid,
        entity_id=txid,
        duplicate_key=f"transactions:{txid}",
        sync_hash=sync_hash,
        reason="normal transaction candidate",
        row_preview=tx_preview,
    )]

    if is_tokopedia_cc(item.get("merchant"), item.get("payment_method"), account_name):
        ops.append(PlannedOperation(
            target_tab="💳 Credit Card",
            action="insert_or_update",
            source_table="transactions",
            source_rowid=rowid,
            entity_id=txid,
            duplicate_key=f"credit_card:{txid}",
            sync_hash=sync_hash,
            reason="Tokopedia Credit Card detected",
            row_preview={
                "cc_entry_id": f"cc_{txid}",
                "date": item.get("transaction_date"),
                "merchant_app": item.get("merchant") or "Tokopedia Credit Card",
                "amount": amount_int,
                "description": truncate(item.get("note"), 120),
                "status_pocket_blu": "⏳ Belum",
                "transferred_at": "",
                "linked_txn_id": txid,
                "notes": "sqlite dry-run candidate",
            },
        ))

    return ops


def plan_approval_queue(row: sqlite3.Row) -> PlannedOperation:
    item = dict(row)
    rowid = item.get("rowid")
    # AIRO_V13_SPECIAL_APPROVAL_QUEUE_TARGET_TAB
    raw_payload = item.get("proposed_change_json") or item.get("payload_json") or "{}"
    try:
        payload = json.loads(raw_payload or "{}")
    except Exception:
        payload = {}

    if isinstance(payload, dict) and payload.get("schema_version") == "airo.finance.v1.3.special.approval_queue":
        target_tab = payload.get("target_tab")
        if target_tab in {"💵 Cash Ledger", "🏠 Cicilan Rumah", "🤝 Hutang"}:
            duplicate_key = payload.get("duplicate_key") or f"{item.get('entity_type')}:{item.get('entity_id')}"
            row_preview = dict(payload.get("row_preview") or {})
            row_preview.update({
                "duplicate_key": duplicate_key,
                "raw_text": payload.get("raw_text") or row_preview.get("raw_text") or "",
                "source": payload.get("source") or row_preview.get("source") or "approval_queue",
                "local_db_table": "approval_queue",
                "local_db_rowid": rowid,
            })
            sync_hash = stable_hash([
                "approval_queue_special",
                target_tab,
                duplicate_key,
                item.get("entity_type"),
                item.get("entity_id"),
                item.get("created_at"),
            ])
            return PlannedOperation(
                target_tab=target_tab,
                action="insert_or_update",
                source_table="approval_queue",
                source_rowid=rowid,
                entity_id=item.get("entity_id"),
                duplicate_key=duplicate_key,
                sync_hash=sync_hash,
                reason=item.get("reason") or "approval queue special finance candidate",
                row_preview=row_preview,
            )

    qid = item.get("id")
    payload = {}

    raw_payload = item.get("payload_json") or item.get("proposed_change_json") or "{}"
    try:
        payload = json.loads(raw_payload or "{}")
    except Exception:
        payload = {}

    if isinstance(payload, dict) and payload.get("schema_version") == "airo.finance.v1.3.review_queue.persistence":
        duplicate_key = payload.get("duplicate_key") or "review_queue:" + str(payload.get("queue_id") or qid or rowid)
        sync_hash = stable_hash([
            duplicate_key,
            payload.get("queue_id"),
            payload.get("raw_text"),
            payload.get("status"),
            item.get("created_at"),
        ])
        return PlannedOperation(
            target_tab="🧾 Review Queue",
            action="insert_or_update",
            source_table="approval_queue",
            source_rowid=rowid,
            entity_id=payload.get("queue_id") or qid,
            duplicate_key=duplicate_key,
            sync_hash=sync_hash,
            reason="approval queue v1.3 review candidate",
            row_preview={
                "queue_id": payload.get("queue_id") or qid,
                "created_at": item.get("created_at"),
                "source": payload.get("source") or item.get("source") or "sqlite_approval_queue",
                "raw_text": payload.get("raw_text"),
                "parsed_type": payload.get("intent") or item.get("request_type") or item.get("action_type"),
                "issue_reason": item.get("reason") or item.get("approval_note") or "ambiguous finance needs review",
                "review_status": payload.get("status") or item.get("status") or "pending",
                "reviewed_at": item.get("decided_at"),
                "local_db_table": "approval_queue",
                "local_db_rowid": rowid,
                "sync_hash": sync_hash,
                "notes": duplicate_key,
            },
        )

    sync_hash = stable_hash([
        "approval_queue",
        qid,
        item.get("request_type"),
        item.get("entity_type"),
        item.get("entity_id"),
        item.get("proposed_change_json"),
        item.get("status"),
        item.get("created_at"),
        item.get("decided_at"),
    ])
    return PlannedOperation(
        target_tab="🧾 Review Queue",
        action="insert_or_update",
        source_table="approval_queue",
        source_rowid=rowid,
        entity_id=qid,
        duplicate_key="review:approval_queue:" + str(rowid),
        sync_hash=sync_hash,
        reason="approval queue row",
        row_preview={
            "queue_id": qid,
            "created_at": item.get("created_at"),
            "source": "sqlite_approval_queue",
            "raw_text": truncate(item.get("proposed_change_json")),
            "parsed_type": item.get("request_type"),
            "issue_reason": item.get("reason") or "",
            "review_status": item.get("status") or "pending",
            "reviewed_at": item.get("decided_at"),
            "local_db_table": "approval_queue",
            "local_db_rowid": rowid,
            "sync_hash": sync_hash,
            "notes": "{}:{}".format(item.get("entity_type") or "", item.get("entity_id") or ""),
        },
    )


def plan_installment_payment(row: sqlite3.Row) -> PlannedOperation:
    item = dict(row)
    rowid = item.get("rowid")
    payment_id = item.get("id")
    sync_hash = stable_hash([
        "installment_payments",
        payment_id,
        item.get("installment_id"),
        item.get("payment_date"),
        item.get("installment_number"),
        item.get("amount"),
        item.get("method"),
        item.get("verified"),
        item.get("created_at"),
    ])
    return PlannedOperation(
        target_tab="🏠 Cicilan Rumah",
        action="insert_or_update",
        source_table="installment_payments",
        source_rowid=rowid,
        entity_id=payment_id,
        duplicate_key=f"installment_payment:{payment_id}",
        sync_hash=sync_hash,
        reason="installment payment row",
        row_preview={
            "payment_id": payment_id,
            "cicilan_ke": item.get("installment_number"),
            "date_paid": item.get("payment_date"),
            "amount_paid": item.get("amount"),
            "status": "paid" if item.get("verified") in ("yes", "true", "1") else "upcoming",
            "notes": truncate(item.get("note")),
        },
    )


def summarize(ops: list[PlannedOperation]) -> dict[str, Any]:
    by_target: dict[str, int] = {}
    by_action: dict[str, int] = {}
    for op in ops:
        by_target[op.target_tab] = by_target.get(op.target_tab, 0) + 1
        by_action[op.action] = by_action.get(op.action, 0) + 1
    return {"by_target": by_target, "by_action": by_action, "total_operations": len(ops)}


def build_report(db_path: Path) -> dict[str, Any]:
    run_id = "dryrun_" + datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:8]
    con = connect(db_path)
    try:
        cur = con.cursor()
        tables = get_tables(cur)
        accounts = account_lookup(cur, tables)

        row_counts = {
            table: cur.execute(f"SELECT COUNT(*) AS c FROM {table}").fetchone()["c"]
            for table in sorted(tables)
        }

        ops: list[PlannedOperation] = []

        asset_planner_warning = ""

        if "transactions" in tables:
            transaction_rows = cur.execute("SELECT rowid, * FROM transactions ORDER BY rowid ASC").fetchall()

            for row in transaction_rows:
                ops.extend(plan_transaction(row, accounts))

            try:
                asset_planner = load_asset_planner_module()
                if asset_planner is not None:
                    tx_dicts = [dict(row) for row in transaction_rows]
                    row_by_txid = {str(item.get("id") or ""): item for item in tx_dicts}
                    for asset_plan in asset_planner.plan_asset_events_from_transactions(tx_dicts):
                        row_preview = dict(asset_plan.get("row") or {})
                        section = str(asset_plan.get("section") or "")
                        linked_txn_id = str(row_preview.get("linked_transaction_id") or "")
                        source_item = row_by_txid.get(linked_txn_id, {})
                        ops.append(PlannedOperation(
                            target_tab=str(asset_plan.get("target_tab") or "🥇 Aset"),
                            action="insert_or_update",
                            source_table="transactions",
                            source_rowid=source_item.get("rowid"),
                            entity_id=linked_txn_id or str(asset_plan.get("duplicate_key") or ""),
                            duplicate_key=str(asset_plan.get("duplicate_key") or ""),
                            sync_hash=str(asset_plan.get("sync_hash") or ""),
                            reason=str(asset_plan.get("reason") or "asset event detected"),
                            row_preview=row_preview,
                            section=section,
                        ))
            except Exception as exc:
                asset_planner_warning = "asset planner skipped: " + str(exc)

        if "approval_queue" in tables:
            for row in cur.execute("SELECT rowid, * FROM approval_queue WHERE COALESCE(status, 'pending') IN ('pending', 'pending_review') ORDER BY rowid ASC").fetchall():
                ops.append(plan_approval_queue(row))

        if "installment_payments" in tables:
            for row in cur.execute("SELECT rowid, * FROM installment_payments ORDER BY rowid ASC").fetchall():
                ops.append(plan_installment_payment(row))

        sync_log_preview = {
            "sync_id": "sync_" + uuid.uuid4().hex[:12],
            "run_id": run_id,
            "source_db": str(db_path),
            "source_table": "multiple",
            "source_rowid": "",
            "target_tab": "dry_run_only",
            "transaction_id": "",
            "action": "dry_run",
            "status": "success",
            "records_seen": sum(row_counts.values()),
            "records_inserted": sum(1 for op in ops if op.action == "insert_or_update"),
            "records_updated": 0,
            "records_skipped": sum(1 for op in ops if op.action.startswith("skip")),
            "records_failed": 0,
            "error_message": "",
            "started_at": "",
            "finished_at": "",
            "synced_at": "",
            "notes": "NO GOOGLE WRITE PERFORMED",
        }

        return {
            "title": "AIRO SHEETS SYNC DRY RUN",
            "run_id": run_id,
            "db_path": str(db_path),
            "google_write_performed": False,
            "credentials_read": False,
            "tables": sorted(tables),
            "row_counts": row_counts,
            "account_lookup": {
                key: {
                    "name": value.get("name"),
                    "type": value.get("type"),
                    "provider": value.get("provider"),
                    "status": value.get("status"),
                }
                for key, value in accounts.items()
            },
            "summary": summarize(ops),
            "sync_log_preview": sync_log_preview,
            "planned_operations": [asdict(op) for op in ops],
            "warnings": [
                "This is a dry-run only. No Google Sheets write performed.",
                "Validation marker rows are skipped.",
                "Cash/Hutang/Aset special routing now includes v1.2B asset event planner when applicable.",
                asset_planner_warning,
                "Approval Queue, conflicts, installments, and installment_payments are supported when rows exist.",
            ],
        }
    finally:
        con.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Airo Google Sheets dry-run mapper.")
    parser.add_argument(
        "--db",
        default=str(Path.home() / ".local/share/airo-personal-workflow/airo.sqlite3"),
        help="Path to Airo SQLite DB.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    db_path = Path(args.db).expanduser()

    if not db_path.is_file():
        raise SystemExit(f"ABORT: DB not found: {db_path}")

    report = build_report(db_path)
    print(json.dumps(report, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
