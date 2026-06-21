#!/usr/bin/env python3
"""
AIRO Google Sheets write_preview v0.3.

Purpose:
- Reuse dry-run planner output.
- Compare planned operations against existing Google Sheet keys snapshot.
- Produce insert/update/skip/conflict plan.
- Perform NO Google write.
- Read NO credentials.

Default behavior:
- If no sheet snapshot is provided, run offline preview with empty existing keys.
- This is useful for smoke testing and current DB state.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_DB = Path.home() / ".local/share/airo-personal-workflow/airo.sqlite3"
DRY_RUN_SCRIPT = Path(__file__).resolve().with_name("airo_sheets_sync_dry_run.py")


@dataclass
class PreviewDecision:
    target_tab: str
    section: str
    source_table: str
    source_rowid: int | None
    entity_id: str | None
    duplicate_key: str
    planned_action: str
    preview_action: str
    sync_hash: str
    existing_sync_hash: str | None
    reason: str
    row_preview: dict[str, Any]


def load_dry_run_module():
    if not DRY_RUN_SCRIPT.is_file():
        raise SystemExit(f"ABORT: dry-run script not found: {DRY_RUN_SCRIPT}")

    spec = importlib.util.spec_from_file_location("airo_sheets_sync_dry_run", DRY_RUN_SCRIPT)
    if spec is None or spec.loader is None:
        raise SystemExit("ABORT: unable to load dry-run module")

    module = importlib.util.module_from_spec(spec)
    sys.modules["airo_sheets_sync_dry_run"] = module
    spec.loader.exec_module(module)
    return module


def load_sheet_snapshot(path: Path | None) -> dict[str, dict[str, str]]:
    if path is None:
        return {}

    if not path.is_file():
        raise SystemExit(f"ABORT: sheet snapshot not found: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(data, dict):
        raise SystemExit("ABORT: sheet snapshot must be a JSON object")

    tabs = data.get("tabs", data)
    if not isinstance(tabs, dict):
        raise SystemExit("ABORT: sheet snapshot tabs must be an object")

    result: dict[str, dict[str, str]] = {}

    for tab, rows in tabs.items():
        result[str(tab)] = {}

        if isinstance(rows, dict):
            for duplicate_key, sync_hash in rows.items():
                result[str(tab)][str(duplicate_key)] = "" if sync_hash is None else str(sync_hash)
            continue

        if not isinstance(rows, list):
            continue

        for row in rows:
            if not isinstance(row, dict):
                continue
            duplicate_key = row.get("duplicate_key") or row.get("linked_txn_id") or row.get("queue_id") or row.get("payment_id")
            sync_hash = row.get("sync_hash") or ""
            if duplicate_key:
                result[str(tab)][str(duplicate_key)] = str(sync_hash)

    return result


def decide_operation(op: dict, existing_by_tab: dict):
    """Return preview decision for a planned sheet operation.

    AIRO_SIGNATURE_SAFE_IDEMPOTENCY_V104:
    - preserves PreviewDecision object return type
    - supports PreviewDecision field changes by reading dataclass fields
    - accepts existing_by_tab values as dict, string sync_hash, or empty string
    - treats hashless/key-only existing rows as skip_duplicate
    """
    target_tab = op.get("target_tab")
    section = str(op.get("section") or "")
    duplicate_key = op.get("duplicate_key")
    planned_action = op.get("action") or op.get("planned_action")

    def _make_decision(preview_action: str, reason: str = "", existing_sync_hash: str = ""):
        payload = {
            "source_table": op.get("source_table", ""),
            "source_rowid": op.get("source_rowid", ""),
            "entity_id": op.get("entity_id", ""),
            "target_tab": target_tab,
            "section": section,
            "preview_action": preview_action,
            "planned_action": planned_action,
            "duplicate_key": duplicate_key,
            "sync_hash": op.get("sync_hash", ""),
            "existing_sync_hash": existing_sync_hash,
            "reason": reason,
            "row_preview": op.get("row_preview") or {},
        }

        fields = getattr(PreviewDecision, "__dataclass_fields__", None)
        if fields:
            return PreviewDecision(**{name: payload.get(name, "") for name in fields})

        return PreviewDecision(**payload)

    if target_tab == "NO_WRITE":
        return _make_decision(
            planned_action or "skip",
            op.get("reason", ""),
            "",
        )

    lookup_tab = f"{target_tab}::{section}" if target_tab == "🥇 Aset" and section else target_tab
    tab_existing = existing_by_tab.get(lookup_tab) or existing_by_tab.get(target_tab) or {}
    has_existing_key = duplicate_key in tab_existing
    existing_value = tab_existing.get(duplicate_key)

    if has_existing_key:
        if isinstance(existing_value, dict):
            existing_hash = str(existing_value.get("sync_hash") or "").strip()
        else:
            existing_hash = str(existing_value or "").strip()

        planned_hash = str(op.get("sync_hash") or "").strip()

        if not existing_hash:
            return _make_decision(
                "skip_duplicate",
                "duplicate_key exists on hashless target tab",
                existing_hash,
            )

        if existing_hash == planned_hash:
            return _make_decision(
                "skip_duplicate",
                "duplicate_key and sync_hash already match",
                existing_hash,
            )

        return _make_decision(
            "update_candidate",
            "duplicate_key exists with changed sync_hash",
            existing_hash,
        )

    return _make_decision(
        "insert_candidate",
        "duplicate_key not found in existing sheet snapshot",
        "",
    )


def summarize(decisions: list[PreviewDecision]) -> dict[str, Any]:
    by_action: dict[str, int] = {}
    by_target: dict[str, int] = {}

    for decision in decisions:
        by_action[decision.preview_action] = by_action.get(decision.preview_action, 0) + 1
        by_target[decision.target_tab] = by_target.get(decision.target_tab, 0) + 1

    return {
        "total_preview_decisions": len(decisions),
        "by_preview_action": by_action,
        "by_target_tab": by_target,
        "would_write_google": False,
    }


def normalize_credit_card_mirror_ops_v091(planned_ops: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """De-duplicate legacy/direct Credit Card ops and v0.9 mirror ops.

    Rules:
    - final 💳 Credit Card duplicate_key must be linked_txn_id
    - prefer rows with billing_cycle_id
    - drop legacy duplicate_key prefix credit_card:<txn_id> when a billing mirror exists
    """
    billing_mirror_linked_ids: set[str] = set()

    for op in planned_ops:
        if not isinstance(op, dict):
            continue
        if str(op.get("target_tab") or "") != "💳 Credit Card":
            continue
        row = op.get("row_preview") or {}
        linked = str(row.get("linked_txn_id") or op.get("entity_id") or "").strip()
        if linked and row.get("billing_cycle_id"):
            billing_mirror_linked_ids.add(linked)

    selected: dict[tuple[str, str], dict[str, Any]] = {}

    for op in planned_ops:
        if not isinstance(op, dict):
            continue

        target = str(op.get("target_tab") or "")
        duplicate_key = str(op.get("duplicate_key") or "")
        row = dict(op.get("row_preview") or {})

        if target == "💳 Credit Card":
            linked = str(row.get("linked_txn_id") or op.get("entity_id") or "").strip()

            if not linked and duplicate_key.startswith("credit_card:"):
                linked = duplicate_key.split(":", 1)[1]

            if duplicate_key.startswith("credit_card:") and linked in billing_mirror_linked_ids:
                continue

            if linked:
                op = dict(op)
                row["linked_txn_id"] = linked
                op["row_preview"] = row
                op["duplicate_key"] = linked
                duplicate_key = linked

        key = (target, duplicate_key)
        existing = selected.get(key)

        if existing is None:
            selected[key] = op
            continue

        existing_row = existing.get("row_preview") or {}
        current_row = op.get("row_preview") or {}

        existing_has_billing = bool(existing_row.get("billing_cycle_id"))
        current_has_billing = bool(current_row.get("billing_cycle_id"))

        if current_has_billing and not existing_has_billing:
            selected[key] = op

    return list(selected.values())

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AIRO Google Sheets write_preview v0.3.")
    parser.add_argument("--db", default=str(DEFAULT_DB), help="Path to Airo SQLite DB.")
    parser.add_argument("--sheet-snapshot", default="", help="Optional JSON exported by Apps Script sheet key exporter.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    db_path = Path(args.db).expanduser()

    if not db_path.is_file():
        raise SystemExit(f"ABORT: DB not found: {db_path}")

    snapshot_path = Path(args.sheet_snapshot).expanduser() if args.sheet_snapshot else None
    existing_by_tab = load_sheet_snapshot(snapshot_path)

    dry_run = load_dry_run_module()
    dry_report = dry_run.build_report(db_path)
    planned_ops = list(dry_report.get("planned_operations") or [])

    # AIRO_CC_MIRROR_PLANNER_V09
    cc_mirror_warning = None
    try:
        cc_mirror_path = Path(__file__).resolve().with_name("airo_credit_card_mirror_planner.py")
        if cc_mirror_path.is_file():
            cc_spec = importlib.util.spec_from_file_location("airo_credit_card_mirror_planner", cc_mirror_path)
            cc_module = importlib.util.module_from_spec(cc_spec)
            assert cc_spec is not None and cc_spec.loader is not None
            sys.modules[cc_spec.name] = cc_module
            cc_spec.loader.exec_module(cc_module)
            planned_ops.extend(cc_module.build_credit_card_mirror_operations(planned_ops))
    except Exception as exc:
        cc_mirror_warning = "credit card mirror planner skipped: " + str(exc)

    planned_ops = normalize_credit_card_mirror_ops_v091(planned_ops)

    decisions = [decide_operation(op, existing_by_tab) for op in planned_ops]

    run_id = "write_preview_" + datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:8]

    report = {
        "title": "AIRO SHEETS WRITE PREVIEW",
        "version": "v0.3",
        "run_id": run_id,
        "db_path": str(db_path),
        "sheet_snapshot_provided": snapshot_path is not None,
        "google_write_performed": False,
        "credentials_read": False,
        "source_dry_run_id": dry_report.get("run_id"),
        "dry_run_summary": dry_report.get("summary"),
        "row_counts": dry_report.get("row_counts"),
        "summary": summarize(decisions),
        "decisions": [asdict(decision) for decision in decisions],
        "warnings": [
            item for item in [
                "write_preview performs no Google write",
                "credentials are not read by this script",
                "without a sheet snapshot, existing keys are treated as empty",
                "finance ledger write remains disabled until explicit approval-gated implementation",
                cc_mirror_warning,
            ]
            if item
        ],
    }

    print(json.dumps(report, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
