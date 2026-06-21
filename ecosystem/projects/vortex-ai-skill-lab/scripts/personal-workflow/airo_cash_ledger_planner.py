#!/usr/bin/env python3
"""AIRO Cash Ledger planner v1.2.

Read-only planner for Cash Ledger routing.
No credential read, no SQLite mutation, no Google write, no OpenClaw restart.
"""

from __future__ import annotations

# AIRO_PATCH_CASH_LEDGER_BEVERAGE_v1

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from typing import Any

CASH_LEDGER_TAB = "💵 Cash Ledger"
REVIEW_QUEUE_TAB = "🧾 Review Queue"

CATEGORY_HINTS = {
    "makan": "Makan",
    "minum": "Makan",
    "minuman": "Makan",
    "kopi": "Makan",
    "air": "Makan",
    "teh": "Makan",
    "es": "Makan",
    "jus": "Makan",
    "boba": "Makan",
    "susu": "Makan",
    "jajan": "Makan",
    "snack": "Makan",
    "bensin": "Transport",
    "parkir": "Transport",
    "galon": "Belanja",
    "belanja": "Belanja",
    "wifi": "Tagihan",
    "pdam": "Tagihan",
    "listrik": "Tagihan",
    "lain": "Lainnya",
}


def normalize_text(raw_text: str) -> str:
    return " ".join(raw_text.strip().lower().split())


def detect_amount(raw_text: str) -> int | None:
    text = normalize_text(raw_text)
    patterns = [
        r"(\d+(?:[.,]\d+)?)\s*(juta|jt)\b",
        r"(\d+(?:[.,]\d+)?)\s*(ribu|rb|k)\b",
        r"\b(\d{4,})\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if not match:
            continue
        number = float(match.group(1).replace(".", "").replace(",", "."))
        unit = match.group(2) if len(match.groups()) >= 2 else ""
        if unit in {"juta", "jt"}:
            return int(number * 1000000)
        if unit in {"ribu", "rb", "k"}:
            return int(number * 1000)
        return int(number)
    return None


def detect_category(raw_text: str) -> str | None:
    text = normalize_text(raw_text)
    for hint, category in sorted(CATEGORY_HINTS.items(), key=lambda item: len(item[0]), reverse=True):
        if hint in text:
            return category
    return None


def classify_cash_message(raw_text: str) -> str:
    text = normalize_text(raw_text)
    session_markers = [
        "pegang cash",
        "pegang tunai",
        "ada cash",
        "cash di tangan",
        "uang cash",
        "uang tunai",
    ]
    spend_markers = [
        # AIRO_PATCH_CASH_INTENT_SPEND_MARKERS_v1
        "cash beli",
        "tunai beli",
        "cash bayar",
        "tunai bayar",
        "cash jajan",
        "tunai jajan",
        "cash makan",
        "tunai makan",
        "cash minum",
        "tunai minum",
        "cash kopi",
        "tunai kopi",
        "cash air",
        "tunai air",
        "cash kepake",
        "cash kepakai",
        "pakai cash",
        "pake cash",
        "pakai tunai",
        "pake tunai",
        "bayar cash",
        "bayar tunai",
    ]

    if any(marker in text for marker in session_markers):
        return "cash_session"
    if any(marker in text for marker in spend_markers):
        return "cash_entry"
    if "cash" in text or "tunai" in text:
        return "cash_unknown"
    return "not_cash"


def cash_id_for(raw_text: str, operation: str, source: str = "telegram") -> str:
    digest = hashlib.sha1((source + "|" + operation + "|" + normalize_text(raw_text)).encode("utf-8")).hexdigest()[:12]
    prefix = "cash_session" if operation == "cash_session_candidate" else "cash_entry"
    return prefix + "_" + digest


def plan_cash_ledger(raw_text: str, source: str = "telegram", now_iso: str | None = None) -> dict[str, Any]:
    if now_iso is None:
        now_iso = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    cash_type = classify_cash_message(raw_text)
    amount = detect_amount(raw_text)
    category = detect_category(raw_text)
    reasons: list[str] = []

    if cash_type == "not_cash":
        reasons.append("not_cash_message")
    if cash_type == "cash_unknown":
        reasons.append("cash_intent_unclear")
    if amount is None:
        reasons.append("missing_amount")
    if cash_type == "cash_entry" and category is None:
        reasons.append("missing_cash_entry_category")

    route_to_review = bool(reasons)
    if cash_type == "cash_session" and amount is not None:
        operation = "cash_session_candidate"
    elif cash_type == "cash_entry" and amount is not None and category is not None:
        operation = "cash_entry_candidate"
    else:
        operation = "review_insert_candidate"

    target_tab = REVIEW_QUEUE_TAB if route_to_review else CASH_LEDGER_TAB
    entry_id = cash_id_for(raw_text, operation, source)

    return {
        "planner": "airo_cash_ledger_planner_v1_2",
        "google_write_performed": False,
        "sqlite_mutation_performed": False,
        "credential_read_performed": False,
        "openclaw_restart_performed": False,
        "route_to_review": route_to_review,
        "target_tab": target_tab,
        "cash_type": cash_type,
        "operation": operation,
        "cash_id": entry_id,
        "duplicate_key": target_tab + ":" + entry_id,
        "status": "planned" if not route_to_review else "pending_review",
        "source": source,
        "normalized": {
            "amount": amount,
            "category": category,
            "account": "Cash" if cash_type != "not_cash" else None,
        },
        "ambiguity_reasons": reasons,
        "raw_text": raw_text,
        "created_at": now_iso,
        "next_action": "dry_run_cash_ledger_mapping" if not route_to_review else "hold_for_review_or_ask_clarification",
    }


def render_text(plan: dict[str, Any]) -> str:
    normalized = plan["normalized"]
    reasons = plan["ambiguity_reasons"]
    lines = [
        "AIRO Cash Ledger Planner v1.2",
        "Route to review: {}".format(plan["route_to_review"]),
        "Target tab: {}".format(plan["target_tab"]),
        "Cash type: {}".format(plan["cash_type"]),
        "Operation: {}".format(plan["operation"]),
        "Cash ID: {}".format(plan["cash_id"]),
        "Status: {}".format(plan["status"]),
        "",
        "Normalized:",
        "- amount: {}".format(normalized.get("amount")),
        "- category: {}".format(normalized.get("category")),
        "- account: {}".format(normalized.get("account")),
        "",
        "Ambiguity reasons:",
    ]
    if reasons:
        lines.extend("- {}".format(reason) for reason in reasons)
    else:
        lines.append("- none")
    lines.extend([
        "",
        "Next action: {}".format(plan["next_action"]),
        "Safety: no Google write, no SQLite mutation, no credential read, no OpenClaw restart",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan Cash Ledger routing for AIRO finance messages.")
    parser.add_argument("message")
    parser.add_argument("--source", default="telegram")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    plan = plan_cash_ledger(args.message, source=args.source)
    if args.json:
        print(json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_text(plan))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
