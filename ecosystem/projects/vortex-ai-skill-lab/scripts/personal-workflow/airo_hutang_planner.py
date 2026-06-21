#!/usr/bin/env python3
"""AIRO Hutang planner v1.2.

Read-only planner for 🤝 Hutang routing.
No credential read, no SQLite mutation, no Google write, no OpenClaw restart.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from typing import Any

HUTANG_TAB = "🤝 Hutang"
REVIEW_QUEUE_TAB = "🧾 Review Queue"

ACTIVE_DEBTS = {
    "HT-001": {
        "creditor": "Mamak Egit",
        "balance": 15000000,
        "aliases": ["mamak egit", "mama egit", "ibu egit"],
    },
    "HT-002": {
        "creditor": "Bapak Egit",
        "balance": 5000000,
        "aliases": ["bapak egit", "pak egit", "ayah egit"],
    },
    "HT-003": {
        "creditor": "Mamak Nurul",
        "balance": 5000000,
        "aliases": ["mamak nurul", "mama nurul", "ibu nurul"],
    },
}

ACCOUNT_ALIASES = {
    "blu bca": "BLU BCA",
    "blu-bca": "BLU BCA",
    "blu_bca": "BLU BCA",
    "blubca": "BLU BCA",
    "blu": "BLU BCA",
    "bca": "BCA",
    "mandiri": "Mandiri",
    "gopay": "GoPay",
    "shopeepay": "ShopeePay",
    "cash": "Cash",
    "tunai": "Cash",
}


def normalize_text(raw_text: str) -> str:
    return " ".join(raw_text.strip().lower().split())


def detect_amount(raw_text: str) -> int | None:
    text = normalize_text(raw_text)
    patterns = [
        r"(\d+(?:[.,]\d+)?)\s*(juta|jt)\b",
        r"(\d+(?:[.,]\d+)?)\s*(ribu|rb|k)\b",
        r"\b(\d{5,})\b",
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


def detect_account(raw_text: str) -> str | None:
    text = normalize_text(raw_text)
    for alias, canonical in sorted(ACCOUNT_ALIASES.items(), key=lambda item: len(item[0]), reverse=True):
        if re.search(r"(^|[^a-z0-9])" + re.escape(alias) + r"([^a-z0-9]|$)", text):
            return canonical
    return None


def detect_debt(raw_text: str) -> tuple[str | None, dict[str, Any] | None]:
    text = normalize_text(raw_text)
    for debt_id, data in ACTIVE_DEBTS.items():
        aliases = data["aliases"]
        for alias in aliases:
            if alias in text:
                return debt_id, data
    return None, None


def is_hutang_message(raw_text: str) -> bool:
    text = normalize_text(raw_text)
    return "hutang" in text or "utang" in text


def detect_payment_signal(raw_text: str) -> bool:
    text = normalize_text(raw_text)
    markers = ["bayar", "dibayar", "lunas", "nyicil", "cicil", "transfer", "tf"]
    return any(marker in text for marker in markers)


def payment_id_for(raw_text: str, source: str = "telegram") -> str:
    digest = hashlib.sha1((source + "|hutang|" + normalize_text(raw_text)).encode("utf-8")).hexdigest()[:12]
    return "ht_pay_" + digest


def ambiguity_reasons(raw_text: str, amount: int | None, debt_id: str | None) -> list[str]:
    reasons: list[str] = []
    if not is_hutang_message(raw_text):
        reasons.append("not_hutang_message")
    if not detect_payment_signal(raw_text):
        reasons.append("missing_payment_signal")
    if debt_id is None:
        reasons.append("debt_person_unclear")
    if amount is None:
        reasons.append("missing_amount")
    return reasons


def plan_hutang(raw_text: str, source: str = "telegram", now_iso: str | None = None) -> dict[str, Any]:
    if now_iso is None:
        now_iso = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    amount = detect_amount(raw_text)
    account = detect_account(raw_text)
    debt_id, debt_data = detect_debt(raw_text)
    reasons = ambiguity_reasons(raw_text, amount, debt_id)
    route_to_review = bool(reasons)

    creditor = debt_data["creditor"] if debt_data else None
    balance_before = int(debt_data["balance"]) if debt_data else None
    balance_after = None
    if balance_before is not None and amount is not None:
        balance_after = max(balance_before - amount, 0)

    payment_id = payment_id_for(raw_text, source)

    return {
        "planner": "airo_hutang_planner_v1_2",
        "google_write_performed": False,
        "sqlite_mutation_performed": False,
        "credential_read_performed": False,
        "openclaw_restart_performed": False,
        "route_to_review": route_to_review,
        "target_tab": REVIEW_QUEUE_TAB if route_to_review else HUTANG_TAB,
        "operation": "hutang_payment_candidate" if not route_to_review else "review_insert_candidate",
        "payment_id": payment_id,
        "duplicate_key": ("hutang:" if not route_to_review else "review_queue:") + payment_id,
        "status": "planned" if not route_to_review else "pending_review",
        "source": source,
        "normalized": {
            "debt_id": debt_id,
            "creditor": creditor,
            "amount": amount,
            "account": account,
            "balance_before": balance_before,
            "balance_after": balance_after,
        },
        "ambiguity_reasons": reasons,
        "raw_text": raw_text,
        "created_at": now_iso,
        "next_action": "dry_run_hutang_mapping" if not route_to_review else "hold_for_review_or_ask_clarification",
    }


def render_text(plan: dict[str, Any]) -> str:
    normalized = plan["normalized"]
    reasons = plan["ambiguity_reasons"]
    lines = [
        "AIRO Hutang Planner v1.2",
        "Route to review: {}".format(plan["route_to_review"]),
        "Target tab: {}".format(plan["target_tab"]),
        "Operation: {}".format(plan["operation"]),
        "Payment ID: {}".format(plan["payment_id"]),
        "Status: {}".format(plan["status"]),
        "",
        "Normalized:",
        "- debt_id: {}".format(normalized.get("debt_id")),
        "- creditor: {}".format(normalized.get("creditor")),
        "- amount: {}".format(normalized.get("amount")),
        "- account: {}".format(normalized.get("account")),
        "- balance_before: {}".format(normalized.get("balance_before")),
        "- balance_after: {}".format(normalized.get("balance_after")),
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
    parser = argparse.ArgumentParser(description="Plan Hutang routing for AIRO finance messages.")
    parser.add_argument("message")
    parser.add_argument("--source", default="telegram")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    plan = plan_hutang(args.message, source=args.source)
    if args.json:
        print(json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_text(plan))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
