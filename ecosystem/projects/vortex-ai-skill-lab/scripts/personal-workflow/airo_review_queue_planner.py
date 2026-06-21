#!/usr/bin/env python3
"""AIRO Review Queue planner v1.2.

Read-only planner for ambiguous finance messages.
No credential read, no SQLite mutation, no Google write, no OpenClaw restart.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from typing import Any

REVIEW_QUEUE_TAB = "🧾 Review Queue"
DEFAULT_CONFIDENCE_THRESHOLD = 0.80

ACCOUNT_ALIASES = {
    "blu bca": "BLU BCA",
    "blu-bca": "BLU BCA",
    "blu_bca": "BLU BCA",
    "blubca": "BLU BCA",
    "blu": "BLU BCA",
    "bca": "BCA",
    "tokopedia credit card": "Tokopedia Credit Card",
    "tokopedia cc": "Tokopedia Credit Card",
    "tokped cc": "Tokopedia Credit Card",
    "mandiri": "Mandiri",
    "gopay": "GoPay",
    "shopeepay": "ShopeePay",
    "tunai": "Cash",
    "cash": "Cash",
}

CATEGORY_HINTS = {
    "tarik cash": "Cash",
    "makan": "Makan",
    "jajan": "Makan",
    "bensin": "Transport",
    "parkir": "Transport",
    "wifi": "Tagihan",
    "pdam": "Tagihan",
    "listrik": "Tagihan",
    "belanja": "Belanja",
    "cicilan": "Cicilan",
    "hutang": "Hutang",
    "emas": "Aset",
    "nabung": "Tabungan",
    "tabungan": "Tabungan",
    "topup": "E-Wallet",
    # AIRO_PATCH_BEVERAGE_KEYWORD_MAPPING_v3
    "minum": "Makan",
    "minuman": "Makan",
    "kopi": "Makan",
    "air": "Makan",
    "teh": "Makan",
    "es": "Makan",
    "jus": "Makan",
    "boba": "Makan",
    "susu": "Makan",
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
            return int(number * 1_000_000)
        if unit in {"ribu", "rb", "k"}:
            return int(number * 1_000)
        return int(number)
    return None


def detect_account(raw_text: str) -> str | None:
    text = normalize_text(raw_text)
    for alias, canonical in sorted(ACCOUNT_ALIASES.items(), key=lambda item: len(item[0]), reverse=True):
        if re.search(r"(^|[^a-z0-9])" + re.escape(alias) + r"([^a-z0-9]|$)", text):
            return canonical
    return None


def detect_category(raw_text: str) -> str | None:
    text = normalize_text(raw_text)
    for hint, category in sorted(CATEGORY_HINTS.items(), key=lambda item: len(item[0]), reverse=True):
        if hint in text:
            return category
    return None


def infer_target_domain(raw_text: str) -> str:
    text = normalize_text(raw_text)
    if "cash" in text or "tunai" in text:
        return "💵 Cash Ledger"
    if "cicilan rumah" in text:
        return "🏠 Cicilan Rumah"
    if "hutang" in text:
        return "🤝 Hutang"
    if "emas" in text or "nabung" in text or "tabungan" in text or "pocket" in text:
        return "🥇 Aset"
    if "tokopedia credit card" in text or "tokopedia cc" in text or "tokped cc" in text:
        return "💳 Credit Card"
    return "💸 Transactions"


def review_id_for(raw_text: str, source: str = "telegram") -> str:
    digest = hashlib.sha1((source + "|" + normalize_text(raw_text)).encode("utf-8")).hexdigest()[:12]
    return "rq_" + digest


def ambiguity_reasons(raw_text: str, confidence: float, amount: int | None, account: str | None, category: str | None) -> list[str]:
    text = normalize_text(raw_text)
    reasons: list[str] = []

    if confidence < DEFAULT_CONFIDENCE_THRESHOLD:
        reasons.append("low_confidence")
    if amount is None:
        reasons.append("missing_amount")

    needs_account = any(token in text for token in ["pakai", "dari", "ke ", "tf", "topup", "bayar", "beli"])
    if needs_account and account is None:
        reasons.append("missing_or_unknown_account")

    cash_session = "pegang cash" in text or "pegang tunai" in text
    if category is None and not cash_session:
        reasons.append("missing_or_unknown_category")

    if "hutang" in text and not any(name in text for name in ["mamak egit", "bapak egit", "mamak nurul"]):
        reasons.append("debt_person_unclear")

    if "cicilan rumah" in text and amount is None:
        reasons.append("cicilan_amount_default_needed")

    return list(dict.fromkeys(reasons))


def plan_review_queue(raw_text: str, confidence: float = 0.0, source: str = "telegram", parser_intent: str = "finance_capture", now_iso: str | None = None) -> dict[str, Any]:
    if now_iso is None:
        now_iso = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    amount = detect_amount(raw_text)
    account = detect_account(raw_text)
    category = detect_category(raw_text)
    suggested_domain = infer_target_domain(raw_text)
    reasons = ambiguity_reasons(raw_text, confidence, amount, account, category)
    route_to_review = bool(reasons)
    review_id = review_id_for(raw_text, source)

    return {
        "planner": "airo_review_queue_planner_v1_2",
        "google_write_performed": False,
        "sqlite_mutation_performed": False,
        "credential_read_performed": False,
        "openclaw_restart_performed": False,
        "route_to_review": route_to_review,
        "target_tab": REVIEW_QUEUE_TAB if route_to_review else suggested_domain,
        "suggested_domain": suggested_domain,
        "operation": "review_insert_candidate" if route_to_review else "no_review_needed",
        "review_id": review_id,
        "duplicate_key": "review_queue:" + review_id,
        "status": "pending_review" if route_to_review else "not_required",
        "source": source,
        "parser_intent": parser_intent,
        "confidence": confidence,
        "confidence_threshold": DEFAULT_CONFIDENCE_THRESHOLD,
        "ambiguity_reasons": reasons,
        "normalized": {"amount": amount, "account": account, "category": category},
        "raw_text": raw_text,
        "created_at": now_iso,
        "next_action": "hold_for_review_or_ask_clarification" if route_to_review else "allow_verified_route_to_continue",
    }


def render_text(plan: dict[str, Any]) -> str:
    normalized = plan["normalized"]
    reasons = plan["ambiguity_reasons"]
    lines = [
        "AIRO Review Queue Planner v1.2",
        "Route to review: {}".format(plan["route_to_review"]),
        "Target tab: {}".format(plan["target_tab"]),
        "Suggested domain: {}".format(plan["suggested_domain"]),
        "Operation: {}".format(plan["operation"]),
        "Review ID: {}".format(plan["review_id"]),
        "Confidence: {} / threshold {}".format(plan["confidence"], plan["confidence_threshold"]),
        "Status: {}".format(plan["status"]),
        "",
        "Normalized:",
        "- amount: {}".format(normalized.get("amount")),
        "- account: {}".format(normalized.get("account")),
        "- category: {}".format(normalized.get("category")),
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
    parser = argparse.ArgumentParser(description="Plan Review Queue routing for ambiguous AIRO finance messages.")
    parser.add_argument("message")
    parser.add_argument("--confidence", type=float, default=0.0)
    parser.add_argument("--source", default="telegram")
    parser.add_argument("--intent", default="finance_capture")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    plan = plan_review_queue(args.message, confidence=args.confidence, source=args.source, parser_intent=args.intent)
    if args.json:
        print(json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_text(plan))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
