#!/usr/bin/env python3
"""
AIRO Google Sheets Ledger Write Skeleton v0.4.

Status:
- Skeleton / gated.
- Default mode is preview.
- No Google write is implemented in this version.

Purpose:
- Establish production-grade write-mode structure before real ledger write.
- Reuse write_preview decisions.
- Enforce approval phrase and write scope before any future write mode.

This script intentionally does not import Google API libraries yet.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


APPROVAL_PHRASE = "I APPROVE GOOGLE SHEETS WRITE FOR AIRO FINANCE"
REPO_ROOT = Path(__file__).resolve().parents[2]
WRITE_PREVIEW_SCRIPT = Path(__file__).resolve().with_name("airo_sheets_sync_write_preview.py")


def run_write_preview(db: str, sheet_snapshot: str | None) -> dict[str, Any]:
    cmd = [sys.executable, str(WRITE_PREVIEW_SCRIPT), "--db", db]
    if sheet_snapshot:
        cmd.extend(["--sheet-snapshot", sheet_snapshot])

    proc = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return json.loads(proc.stdout)


def validate_approval(mode: str, approval: str) -> None:
    if mode == "write" and approval != APPROVAL_PHRASE:
        raise SystemExit("ABORT: Google Sheets write approval phrase missing or invalid.")


def validate_write_scope(scope: str) -> None:
    allowed = {"sync_log_only", "transactions_review_cc"}
    if scope not in allowed:
        raise SystemExit(f"ABORT: unsupported write scope: {scope}")


def build_skeleton_report(args: argparse.Namespace, preview: dict[str, Any]) -> dict[str, Any]:
    write_requested = args.mode == "write"

    return {
        "title": "AIRO SHEETS LEDGER WRITE SKELETON",
        "version": "v0.4",
        "mode": args.mode,
        "write_scope": args.write_scope,
        "google_write_performed": False,
        "credentials_read": False,
        "write_requested": write_requested,
        "approval_gate": "passed" if write_requested else "not_required_for_preview",
        "real_write_implemented": False,
        "source_preview_summary": preview.get("summary"),
        "source_preview_decisions": [
            {
                "target_tab": d.get("target_tab"),
                "preview_action": d.get("preview_action"),
                "duplicate_key": d.get("duplicate_key"),
                "reason": d.get("reason"),
            }
            for d in preview.get("decisions", [])
        ],
        "decision": (
            "NO_WRITE_IMPLEMENTED_IN_V0_4"
            if write_requested
            else "PREVIEW_ONLY"
        ),
        "next_required_step": (
            "Implement Google API client and real append/update only after credential strategy is approved."
            if write_requested
            else "Wait for real finance rows, then run write_preview again."
        ),
        "warnings": [
            "v0.4 is a skeleton and performs no Google write",
            "no credentials are read",
            "finance ledger writes remain disabled",
            "approval phrase is required for future write mode",
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AIRO Google Sheets ledger write skeleton v0.4.")
    parser.add_argument(
        "--mode",
        choices=["preview", "write"],
        default="preview",
        help="preview is default and performs no write. write is gated but still not implemented in v0.4.",
    )
    parser.add_argument(
        "--approval",
        default="",
        help="Exact approval phrase required only for future write mode.",
    )
    parser.add_argument(
        "--write-scope",
        default="transactions_review_cc",
        help="Planned write scope. v0.4 validates only.",
    )
    parser.add_argument(
        "--db",
        default=str(Path.home() / ".local/share/airo-personal-workflow/airo.sqlite3"),
        help="Path to Airo SQLite DB.",
    )
    parser.add_argument(
        "--sheet-snapshot",
        default="",
        help="Optional sheet keys snapshot JSON.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    validate_approval(args.mode, args.approval)
    validate_write_scope(args.write_scope)

    if not Path(args.db).expanduser().is_file():
        raise SystemExit(f"ABORT: DB not found: {args.db}")

    preview = run_write_preview(args.db, args.sheet_snapshot or None)
    report = build_skeleton_report(args, preview)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
