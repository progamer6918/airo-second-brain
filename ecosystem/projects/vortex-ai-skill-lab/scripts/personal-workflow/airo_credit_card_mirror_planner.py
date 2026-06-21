#!/usr/bin/env python3
"""
AIRO Credit Card Mirror Planner v0.9.

Purpose:
- Generate 💳 Credit Card mirror operations for Tokopedia Card transactions.
- Apply Tokopedia Card billing cycle rule: 16th to 15th.
- Perform no Google write.
- Read no credentials.

Integration:
- airo_sheets_sync_write_preview.py imports this module and appends mirror
  operations to the existing dry-run planned operations.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


BILLING_SCRIPT = Path(__file__).resolve().with_name("airo_credit_card_billing_cycle.py")
DRY_RUN_SCRIPT = Path(__file__).resolve().with_name("airo_sheets_sync_dry_run.py")


def load_module(path: Path, name: str):
    if not path.is_file():
        raise SystemExit(f"ABORT: module not found: {path}")

    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"ABORT: unable to load module: {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def normalize_text(value: Any) -> str:
    return str(value or "").strip().lower()


def is_tokopedia_credit_card_text(value: Any) -> bool:
    text = normalize_text(value)
    compact = text.replace(" ", "").replace("-", "").replace("_", "")

    return any(
        token in text or token in compact
        for token in [
            "tokopedia credit card",
            "tokopedia cc",
            "tokped credit card",
            "tokped cc",
            "tokopediacreditcard",
            "tokopediacc",
            "tokpedcreditcard",
            "tokpedcc",
        ]
    )


def is_tokopedia_credit_card_operation(op: dict[str, Any]) -> bool:
    # AIRO_CC_MIRROR_DEDUP_V091
    target_tab = str(op.get("target_tab") or "")

    if target_tab == "NO_WRITE":
        return False

    # Mirror only canonical 💸 Transactions operations.
    # Legacy/direct 💳 Credit Card operations must not be mirrored again.
    if target_tab != "💸 Transactions":
        return False

    action = str(op.get("action") or "")
    if action.startswith("skip"):
        return False

    row = op.get("row_preview") or {}

    fields = [
        op.get("payment_method"),
        op.get("account"),
        op.get("merchant"),
        op.get("reason"),
        row.get("payment_method"),
        row.get("account"),
        row.get("merchant"),
        row.get("merchant_app"),
        row.get("description"),
        row.get("raw_text"),
        row.get("notes"),
    ]

    return any(is_tokopedia_credit_card_text(value) for value in fields)


def get_transaction_id(op: dict[str, Any]) -> str:
    row = op.get("row_preview") or {}

    for key in ("transaction_id", "linked_txn_id", "entity_id"):
        value = row.get(key) or op.get(key)
        if value:
            return str(value)

    duplicate_key = str(op.get("duplicate_key") or "")
    if ":" in duplicate_key:
        return duplicate_key.split(":", 1)[1]

    return duplicate_key


def get_transaction_date(op: dict[str, Any]) -> str:
    row = op.get("row_preview") or {}
    for key in ("date", "transaction_date", "created_at"):
        value = row.get(key) or op.get(key)
        if value:
            return str(value)[:10]

    return ""


def stable_hash(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:24]


def build_credit_card_mirror_operation(op: dict[str, Any]) -> dict[str, Any] | None:
    if not is_tokopedia_credit_card_operation(op):
        return None

    billing = load_module(BILLING_SCRIPT, "airo_credit_card_billing_cycle_v09")
    row = op.get("row_preview") or {}

    transaction_id = get_transaction_id(op)
    transaction_date = get_transaction_date(op)

    if not transaction_id or not transaction_date:
        return None

    cycle = billing.compute_tokped_card_billing_cycle(transaction_date)

    amount = row.get("amount") or row.get("parsed_amount") or op.get("amount") or 0
    description = row.get("description") or row.get("raw_text") or row.get("notes") or ""
    merchant_app = row.get("merchant") or row.get("merchant_app") or "Tokopedia"

    mirror_row = {
        "cc_entry_id": "cc_" + hashlib.sha256(transaction_id.encode("utf-8")).hexdigest()[:12],
        "date": transaction_date,
        "merchant_app": merchant_app,
        "amount": amount,
        "description": description,
        "status_pocket_blu": "pending_transfer",
        "transferred_at": "",
        "linked_txn_id": transaction_id,
        "notes": "auto_mirror_from_transactions_v0_9",
        "billing_cycle_id": cycle.billing_cycle_id,
        "billing_start": cycle.billing_start,
        "billing_end": cycle.billing_end,
        "statement_month": cycle.statement_month,
        "due_date": "",
        "is_statement_locked": "FALSE",
    }

    sync_hash = stable_hash(mirror_row)

    return {
        "target_tab": "💳 Credit Card",
        "source_table": op.get("source_table") or "transactions",
        "source_rowid": op.get("source_rowid"),
        "entity_id": transaction_id,
        "duplicate_key": transaction_id,
        "action": "insert_or_update",
        "sync_hash": sync_hash,
        "reason": "tokopedia credit card mirror with billing cycle v0.9",
        "row_preview": mirror_row,
    }


def build_credit_card_mirror_operations(planned_operations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []

    for op in planned_operations:
        if not isinstance(op, dict):
            continue

        mirror = build_credit_card_mirror_operation(op)
        if mirror is not None:
            out.append(mirror)

    return out


def summarize(ops: list[dict[str, Any]]) -> dict[str, Any]:
    by_cycle: dict[str, int] = {}
    for op in ops:
        cycle_id = str((op.get("row_preview") or {}).get("billing_cycle_id") or "")
        by_cycle[cycle_id] = by_cycle.get(cycle_id, 0) + 1

    return {
        "mirror_operations": len(ops),
        "by_billing_cycle_id": by_cycle,
        "google_write_performed": False,
        "credentials_read": False,
    }


def load_planned_operations(path: str | None) -> list[dict[str, Any]]:
    if path:
        data = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
        return data.get("planned_operations") or data.get("decisions") or []

    dry_run = load_module(DRY_RUN_SCRIPT, "airo_sheets_sync_dry_run_for_cc_mirror")
    report = dry_run.build_report(Path.home() / ".local/share/airo-personal-workflow/airo.sqlite3")
    return report.get("planned_operations") or []


def main() -> int:
    parser = argparse.ArgumentParser(description="AIRO Credit Card mirror planner v0.9.")
    parser.add_argument("--planned-ops-json", default="", help="Optional dry-run JSON containing planned_operations.")
    args = parser.parse_args()

    planned_ops = load_planned_operations(args.planned_ops_json or None)
    mirror_ops = build_credit_card_mirror_operations(planned_ops)

    report = {
        "title": "AIRO CREDIT CARD MIRROR PLANNER",
        "version": "v0.9",
        "summary": summarize(mirror_ops),
        "mirror_operations": mirror_ops,
        "warnings": [
            "planner performs no Google write",
            "planner reads no credentials",
            "existing sheet duplicate check happens in write_preview",
        ],
    }

    print(json.dumps(report, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
