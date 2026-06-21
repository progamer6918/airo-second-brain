#!/usr/bin/env python3
"""AIRO Finance Sheet v1.2 status reporter.

Read-only local status utility for the 11 confirmed Google Sheet Finance tabs.
It does not read credentials, mutate SQLite, call Google APIs, or restart services.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from typing import Iterable


@dataclass(frozen=True)
class SheetTabStatus:
    tab: str
    role: str
    status: str
    write_mode: str
    v12_action: str
    priority: int


SHEET_TABS: tuple[SheetTabStatus, ...] = (
    SheetTabStatus(
        tab="🏠 Dashboard",
        role="formula-driven command center",
        status="DESIGN_DONE",
        write_mode="read_only_formula_surface",
        v12_action="keep read-only; improve actionable status UX later",
        priority=4,
    ),
    SheetTabStatus(
        tab="💸 Transactions",
        role="main non-cash transaction ledger",
        status="FULL_AUTO_CORE_READY",
        write_mode="auto_write_verified",
        v12_action="preserve and regression-test before extending routes",
        priority=1,
    ),
    SheetTabStatus(
        tab="💵 Cash Ledger",
        role="cash sessions and cash entries",
        status="FULL_AUTO_WRITE_PATH_READY",
        write_mode="not_yet_full_auto",
        v12_action="add route and dry-run/sync mapping for cash session and cash spend",
        priority=2,
    ),
    SheetTabStatus(
        tab="💳 Credit Card",
        role="Tokopedia Credit Card ledger and billing cycle",
        status="FULL_AUTO_CORE_READY",
        write_mode="auto_write_verified",
        v12_action="preserve Tokopedia CC path and extend regression tests",
        priority=1,
    ),
    SheetTabStatus(
        tab="🏠 Cicilan Rumah",
        role="house installment payment history",
        status="FULL_AUTO_WRITE_PATH_READY",
        write_mode="not_yet_full_auto",
        v12_action="add payment-history route and dry-run/sync mapping",
        priority=3,
    ),
    SheetTabStatus(
        tab="🤝 Hutang",
        role="debt master and repayment history",
        status="FULL_AUTO_WRITE_PATH_READY",
        write_mode="not_yet_full_auto",
        v12_action="add debt-payment route and balance behavior mapping",
        priority=3,
    ),
    SheetTabStatus(
        tab="🥇 Aset",
        role="savings transfer ledger, gold ledger, and net worth support",
        status="PATCHED_ASSET_SYNC",
        write_mode="append_only_verified_sections",
        v12_action="verify latest regression and preserve append-only behavior",
        priority=1,
    ),
    SheetTabStatus(
        tab="📅 Monthly Review",
        role="monthly reporting and category review",
        status="REPORTING_ONLY",
        write_mode="report_refresh_not_raw_capture",
        v12_action="define refresh source and reporting behavior",
        priority=4,
    ),
    SheetTabStatus(
        tab="🧾 Review Queue",
        role="parser ambiguity and manual review guardrail",
        status="FULL_AUTO_WRITE_PATH_READY",
        write_mode="not_yet_full_auto",
        v12_action="route low-confidence parser output here before production writes",
        priority=2,
    ),
    SheetTabStatus(
        tab="⚙️ Settings",
        role="configuration and approval-gate surface",
        status="CONFIG_ONLY",
        write_mode="not_a_ledger_target",
        v12_action="do not use as finance ledger target",
        priority=5,
    ),
    SheetTabStatus(
        tab="🔄 Sync Log",
        role="sync observability and audit log",
        status="FULL_AUTO_CORE_READY",
        write_mode="auto_write_verified",
        v12_action="preserve audit rows for inserted, updated, skipped, and failed counts",
        priority=1,
    ),
)


def status_counts(tabs: Iterable[SheetTabStatus]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in tabs:
        counts[item.status] = counts.get(item.status, 0) + 1
    return dict(sorted(counts.items()))


def focus_tabs(tabs: Iterable[SheetTabStatus]) -> list[dict[str, object]]:
    focus_statuses = {"NOT_GENERALIZED", "PLANNER_READY", "FULL_AUTO_WRITE_PATH_READY", "REPORTING_ONLY"}
    return [
        asdict(item)
        for item in sorted(tabs, key=lambda row: (row.priority, row.tab))
        if item.status in focus_statuses
    ]


def payload() -> dict[str, object]:
    tabs = list(SHEET_TABS)
    return {
        "project": "AIRO Finance Sheet Workflow",
        "baseline": "Google Sheet Finance Balanced+ v1.1.8-final",
        "spreadsheet_name": "💰 Airo Personal Finance",
        "tab_count": len(tabs),
        "status_counts": status_counts(tabs),
        "tabs": [asdict(item) for item in tabs],
        "v12_focus": focus_tabs(tabs),
        "safe_next_batch": [
            "preserve current PASS state",
            "inspect mapper internals",
            "patch one missing route at a time",
            "prefer Review Queue or Cash Ledger first",
            "run dry-run/write-preview regression before Telegram smoke",
        ],
        "safety": {
            "google_write_performed": False,
            "sqlite_mutation_performed": False,
            "credential_read_performed": False,
            "openclaw_restart_performed": False,
        },
    }


def render_text(data: dict[str, object]) -> str:
    rows = data["tabs"]
    assert isinstance(rows, list)

    lines: list[str] = []
    lines.append("AIRO Finance Sheet Workflow v1.2 Status")
    lines.append(f"Baseline: {data['baseline']}")
    lines.append(f"Tabs: {data['tab_count']}")
    lines.append("")
    lines.append("Status counts:")
    counts = data["status_counts"]
    assert isinstance(counts, dict)
    for key, value in counts.items():
        lines.append(f"- {key}: {value}")

    lines.append("")
    lines.append("Tab matrix:")
    for row in rows:
        assert isinstance(row, dict)
        lines.append(
            f"- {row['tab']} | {row['status']} | {row['write_mode']} | {row['v12_action']}"
        )

    lines.append("")
    lines.append("v1.2 focus:")
    focus = data["v12_focus"]
    assert isinstance(focus, list)
    for row in focus:
        assert isinstance(row, dict)
        lines.append(f"- {row['tab']}: {row['v12_action']}")

    lines.append("")
    lines.append("Safe next batch:")
    next_batch = data["safe_next_batch"]
    assert isinstance(next_batch, list)
    for item in next_batch:
        lines.append(f"- {item}")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Report AIRO Finance Sheet v1.2 tab status.")
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    parser.add_argument("--text", action="store_true", help="Print text output. Default.")
    args = parser.parse_args()

    data = payload()

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_text(data))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
