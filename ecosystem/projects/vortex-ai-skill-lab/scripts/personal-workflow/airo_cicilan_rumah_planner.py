#!/usr/bin/env python3
"""AIRO Cicilan Rumah planner v1.2.

Read-only planner for 🏠 Cicilan Rumah routing.
No credential read, no SQLite mutation, no Google write, no OpenClaw restart.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from typing import Any

CICILAN_RUMAH_TAB = "🏠 Cicilan Rumah"
REVIEW_QUEUE_TAB = "🧾 Review Queue"

TOTAL_TENOR = 120
KNOWN_PAID_AS_OF_MAY_2026 = 53
STANDARD_INSTALLMENT = 1543000
USUAL_PAID_AMOUNT = 1570000
DUE_DAY = 7


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


def is_cicilan_rumah_message(raw_text: str) -> bool:
    text = normalize_text(raw_text)
    if "cicilan rumah" in text:
        return True
    if "kpr" in text:
        return True
    if "angsuran rumah" in text:
        return True
    return False


def detect_payment_signal(raw_text: str) -> bool:
    text = normalize_text(raw_text)
    return any(marker in text for marker in ["bayar", "sudah bayar", "lunas", "dibayar", "transfer"])


def payment_id_for(raw_text: str, source: str = "telegram") -> str:
    digest = hashlib.sha1((source + "|cicilan_rumah|" + normalize_text(raw_text)).encode("utf-8")).hexdigest()[:12]
    return "cr_pay_" + digest


def ambiguity_reasons(raw_text: str, amount: int | None, allow_default_amount: bool) -> list[str]:
    reasons: list[str] = []
    if not is_cicilan_rumah_message(raw_text):
        reasons.append("not_cicilan_rumah_message")
    if not detect_payment_signal(raw_text):
        reasons.append("missing_payment_signal")
    if amount is None and not allow_default_amount:
        reasons.append("missing_amount")
    return reasons


def plan_cicilan_rumah(
    raw_text: str,
    source: str = "telegram",
    allow_default_amount: bool = True,
    latest_paid_count: int = KNOWN_PAID_AS_OF_MAY_2026,
    now_iso: str | None = None,
) -> dict[str, Any]:
    if now_iso is None:
        now_iso = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    amount = detect_amount(raw_text)
    amount_was_defaulted = False
    if amount is None and allow_default_amount and is_cicilan_rumah_message(raw_text) and detect_payment_signal(raw_text):
        amount = USUAL_PAID_AMOUNT
        amount_was_defaulted = True

    reasons = ambiguity_reasons(raw_text, amount, allow_default_amount)
    route_to_review = bool(reasons)

    next_cicilan_ke = latest_paid_count + 1
    remaining_after_payment = max(TOTAL_TENOR - next_cicilan_ke, 0)
    payment_id = payment_id_for(raw_text, source)

    return {
        "planner": "airo_cicilan_rumah_planner_v1_2",
        "google_write_performed": False,
        "sqlite_mutation_performed": False,
        "credential_read_performed": False,
        "openclaw_restart_performed": False,
        "route_to_review": route_to_review,
        "target_tab": REVIEW_QUEUE_TAB if route_to_review else CICILAN_RUMAH_TAB,
        "operation": "cicilan_rumah_payment_candidate" if not route_to_review else "review_insert_candidate",
        "payment_id": payment_id,
        "duplicate_key": ("cicilan_rumah:" if not route_to_review else "review_queue:") + payment_id,
        "status": "planned" if not route_to_review else "pending_review",
        "source": source,
        "normalized": {
            "amount": amount,
            "amount_was_defaulted": amount_was_defaulted,
            "standard_installment": STANDARD_INSTALLMENT,
            "usual_paid_amount": USUAL_PAID_AMOUNT,
            "latest_paid_count": latest_paid_count,
            "next_cicilan_ke": next_cicilan_ke,
            "total_tenor": TOTAL_TENOR,
            "remaining_after_payment": remaining_after_payment,
            "due_day": DUE_DAY,
        },
        "ambiguity_reasons": reasons,
        "raw_text": raw_text,
        "created_at": now_iso,
        "next_action": "dry_run_cicilan_rumah_mapping" if not route_to_review else "hold_for_review_or_ask_clarification",
    }


def render_text(plan: dict[str, Any]) -> str:
    normalized = plan["normalized"]
    reasons = plan["ambiguity_reasons"]
    lines = [
        "AIRO Cicilan Rumah Planner v1.2",
        "Route to review: {}".format(plan["route_to_review"]),
        "Target tab: {}".format(plan["target_tab"]),
        "Operation: {}".format(plan["operation"]),
        "Payment ID: {}".format(plan["payment_id"]),
        "Status: {}".format(plan["status"]),
        "",
        "Normalized:",
        "- amount: {}".format(normalized.get("amount")),
        "- amount_was_defaulted: {}".format(normalized.get("amount_was_defaulted")),
        "- next_cicilan_ke: {}".format(normalized.get("next_cicilan_ke")),
        "- total_tenor: {}".format(normalized.get("total_tenor")),
        "- remaining_after_payment: {}".format(normalized.get("remaining_after_payment")),
        "- due_day: {}".format(normalized.get("due_day")),
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
    parser = argparse.ArgumentParser(description="Plan Cicilan Rumah routing for AIRO finance messages.")
    parser.add_argument("message")
    parser.add_argument("--source", default="telegram")
    parser.add_argument("--latest-paid-count", type=int, default=KNOWN_PAID_AS_OF_MAY_2026)
    parser.add_argument("--no-default-amount", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    plan = plan_cicilan_rumah(
        args.message,
        source=args.source,
        allow_default_amount=not args.no_default_amount,
        latest_paid_count=args.latest_paid_count,
    )
    if args.json:
        print(json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_text(plan))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
