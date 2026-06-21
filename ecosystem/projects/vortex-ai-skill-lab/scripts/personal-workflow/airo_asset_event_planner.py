"""Airo asset-event planner v1.2A.

Pure planner for Google Sheet tab `🥇 Aset`.

Safety:
- no Google Sheets access
- no credential/token/env access
- no SQLite access
- no writes

The full-auto sync pipeline should pass already-loaded transaction dictionaries
into `plan_asset_events_from_transactions`.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import hashlib
import re
from typing import Any, Iterable

ASSET_TAB = "🥇 Aset"
SAVINGS_LEDGER_SECTION = "savings_transfer_ledger"
GOLD_LEDGER_SECTION = "gold_ledger"

SAVINGS_HEADERS = [
    "savings_event_id",
    "date",
    "type",
    "from_account",
    "to_account",
    "purpose",
    "amount",
    "source",
    "raw_text",
    "linked_transaction_id",
    "sync_hash",
    "notes",
]

GOLD_HEADERS = [
    "gold_event_id",
    "date",
    "action",
    "grams_in",
    "grams_out",
    "price_per_gram",
    "fee",
    "total_amount",
    "source_account",
    "source",
    "raw_text",
    "sync_hash",
    "notes",
]

ACCOUNT_ALIASES = {
    "bca": "BCA",
    "blu": "BLU BCA",
    "blubca": "BLU BCA",
    "blu bca": "BLU BCA",
    "mandiri": "Mandiri",
    "gopay": "GoPay",
    "go pay": "GoPay",
    "shopeepay": "ShopeePay",
    "shopee pay": "ShopeePay",
    "cash": "Cash",
    "tunai": "Cash",
}

_AMOUNT_WORDS = {
    "rb": Decimal("1000"),
    "ribu": Decimal("1000"),
    "k": Decimal("1000"),
    "jt": Decimal("1000000"),
    "juta": Decimal("1000000"),
    "m": Decimal("1000000"),
}


def _text(row: dict[str, Any]) -> str:
    parts: list[str] = []
    for key in (
        "raw_text",
        "note",
        "notes",
        "description",
        "merchant",
        "payment_method",
        "from_account",
        "to_account",
        "transfer_purpose",
        "asset_bucket",
        "pocket_name",
        "cashflow_treatment",
    ):
        value = row.get(key)
        if value is not None:
            parts.append(str(value))
    return " ".join(parts).strip()


def _lower(row: dict[str, Any]) -> str:
    return _text(row).lower()


def _clean(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _date(row: dict[str, Any]) -> str:
    for key in ("transaction_date", "date", "created_at", "updated_at"):
        value = _clean(row.get(key))
        if value:
            return value[:10]
    return ""


def _source(row: dict[str, Any]) -> str:
    return _clean(row.get("source")) or "airo"


def _transaction_id(row: dict[str, Any]) -> str:
    for key in ("transaction_id", "id", "rowid"):
        value = _clean(row.get(key))
        if value:
            return value
    return ""


def _decimal(value: Any) -> Decimal | None:
    if value is None:
        return None
    s = str(value).strip().replace("_", "").replace("Rp", "").replace("rp", "")
    if not s:
        return None
    s = s.replace(".", "").replace(",", ".") if "," in s and "." in s else s.replace(",", ".")
    try:
        return Decimal(s)
    except InvalidOperation:
        return None


def _format_decimal(value: Decimal | None) -> str:
    if value is None:
        return ""
    if value == value.to_integral():
        return str(value.quantize(Decimal("1")))
    return str(value.normalize())


def _amount_from_text(text: str) -> Decimal | None:
    # examples: 5 juta, 500rb, 1.5 jt, 1500000
    m = re.search(r"\b(\d+(?:[.,]\d+)?)\s*(juta|jt|rb|ribu|k|m)?\b", text, re.I)
    if not m:
        return None
    number = _decimal(m.group(1))
    if number is None:
        return None
    suffix = (m.group(2) or "").lower()
    return number * _AMOUNT_WORDS.get(suffix, Decimal("1"))


def _amount(row: dict[str, Any]) -> Decimal | None:
    for key in ("amount", "total_amount", "nominal"):
        value = _decimal(row.get(key))
        if value is not None:
            return value
    return _amount_from_text(_lower(row))


def _normalize_account(value: Any) -> str:
    s = _clean(value).lower()
    if not s:
        return ""
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    if s in ACCOUNT_ALIASES:
        return ACCOUNT_ALIASES[s]
    for token, canonical in ACCOUNT_ALIASES.items():
        if re.search(rf"\b{re.escape(token)}\b", s):
            return canonical
    return _clean(value)


def _hash(prefix: str, *parts: Any) -> str:
    payload = "|".join(_clean(p) for p in parts)
    return f"{prefix}_{hashlib.sha256(payload.encode('utf-8')).hexdigest()[:12]}"


def _sync_hash(*parts: Any) -> str:
    payload = "|".join(_clean(p) for p in parts)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def _extract_after(text: str, markers: tuple[str, ...]) -> str:
    marker_re = "|".join(re.escape(m) for m in markers)
    m = re.search(rf"\b(?:{marker_re})\s+([a-zA-Z0-9 ]+?)(?:\s+(?:ke|dari|untuk|buat|pakai|via)\b|$)", text, re.I)
    if not m:
        return ""
    return _normalize_account(m.group(1))


def _extract_transfer_accounts(text: str) -> tuple[str, str]:
    # transfer 1 juta dari bca ke blu
    m = re.search(r"\bdari\s+([a-zA-Z0-9 ]+?)\s+ke\s+([a-zA-Z0-9 ]+?)(?:\s|$)", text, re.I)
    if m:
        return _normalize_account(m.group(1)), _normalize_account(m.group(2))
    return "", ""


def _extract_to_account(text: str) -> str:
    m = re.search(r"\bke\s+([a-zA-Z0-9 ]+?)(?:\s|$)", text, re.I)
    return _normalize_account(m.group(1)) if m else ""


def _extract_from_account(text: str) -> str:
    m = re.search(r"\bdari\s+([a-zA-Z0-9 ]+?)(?:\s|$)", text, re.I)
    return _normalize_account(m.group(1)) if m else ""


def _grams_from_text(text: str) -> Decimal | None:
    m = re.search(r"\b(\d+(?:[.,]\d+)?)\s*(?:gram|gr|g)\b", text, re.I)
    if not m:
        return None
    return _decimal(m.group(1))


@dataclass(frozen=True)
class AssetPlan:
    target_tab: str
    section: str
    duplicate_key: str
    sync_hash: str
    row: dict[str, str]
    reason: str

    def asdict(self) -> dict[str, Any]:
        return asdict(self)


def plan_asset_events_from_transactions(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    plans: list[AssetPlan] = []
    for row in rows:
        plans.extend(_plan_row(row))
    return [p.asdict() for p in plans]


def _plan_row(row: dict[str, Any]) -> list[AssetPlan]:
    if row.get("deleted_at"):
        return []

    text = _lower(row)
    plans: list[AssetPlan] = []

    savings = _plan_savings(row, text)
    if savings is not None:
        plans.append(savings)

    gold = _plan_gold(row, text)
    if gold is not None:
        plans.append(gold)

    return plans


def _plan_savings(row: dict[str, Any], text: str) -> AssetPlan | None:
    explicit_from = _normalize_account(row.get("from_account"))
    explicit_to = _normalize_account(row.get("to_account"))
    purpose = _clean(row.get("transfer_purpose")) or _clean(row.get("pocket_name"))

    event_type = ""
    from_account = explicit_from
    to_account = explicit_to

    if explicit_from or explicit_to:
        event_type = "transfer" if explicit_from and explicit_to else ("savings_in" if explicit_to else "savings_out")
    elif re.search(r"\b(nabung|tabung|simpan|saving|savings)\b", text):
        event_type = "savings_in"
        to_account = _extract_to_account(text)
        from_account = _normalize_account(row.get("payment_method"))
    elif re.search(r"\b(transfer|pindah|mutasi)\b", text) and re.search(r"\bdari\b.*\bke\b", text):
        event_type = "transfer"
        from_account, to_account = _extract_transfer_accounts(text)
    elif re.search(r"\b(tarik|withdraw|ambil)\b", text):
        event_type = "savings_out"
        from_account = explicit_from or _extract_from_account(text)
        to_account = explicit_to or _extract_to_account(text) or "Cash"

    if not event_type:
        return None

    amount = _amount(row)
    if amount is None:
        return None

    raw = _text(row)
    trx_id = _transaction_id(row)
    sync_hash = _sync_hash("savings", trx_id, _date(row), event_type, from_account, to_account, amount, raw)
    event_id = _hash("sav", trx_id or raw, _date(row), event_type, from_account, to_account, amount)

    out = {
        "savings_event_id": event_id,
        "date": _date(row),
        "type": event_type,
        "from_account": from_account,
        "to_account": to_account,
        "purpose": purpose or ("tabungan" if event_type == "savings_in" else event_type),
        "amount": _format_decimal(amount),
        "source": _source(row),
        "raw_text": raw,
        "linked_transaction_id": trx_id,
        "sync_hash": sync_hash,
        "notes": "planned_by_airo_asset_event_planner_v1_2A",
    }
    return AssetPlan(ASSET_TAB, SAVINGS_LEDGER_SECTION, event_id, sync_hash, out, "savings movement detected")


def _plan_gold(row: dict[str, Any], text: str) -> AssetPlan | None:
    asset_bucket = _clean(row.get("asset_bucket")).lower()
    if "emas" not in text and "gold" not in text and asset_bucket not in {"emas", "gold"}:
        return None

    grams = _grams_from_text(text)
    if grams is None:
        return None

    action = "buy"
    if re.search(r"\b(jual|sell)\b", text):
        action = "sell"
    elif re.search(r"\b(beli|buy|tambah|nabun[g]? emas)\b", text):
        action = "buy"

    total = _amount(row)
    price_per_gram = None
    if total is not None and grams and grams != Decimal("0"):
        price_per_gram = (total / grams).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    raw = _text(row)
    trx_id = _transaction_id(row)
    source_account = _normalize_account(row.get("payment_method") or row.get("from_account"))
    sync_hash = _sync_hash("gold", trx_id, _date(row), action, grams, total, raw)
    event_id = _hash("gold", trx_id or raw, _date(row), action, grams, total)

    out = {
        "gold_event_id": event_id,
        "date": _date(row),
        "action": action,
        "grams_in": _format_decimal(grams if action == "buy" else Decimal("0")),
        "grams_out": _format_decimal(grams if action == "sell" else Decimal("0")),
        "price_per_gram": _format_decimal(price_per_gram),
        "fee": "",
        "total_amount": _format_decimal(total),
        "source_account": source_account,
        "source": _source(row),
        "raw_text": raw,
        "sync_hash": sync_hash,
        "notes": "planned_by_airo_asset_event_planner_v1_2A; gram_is_canonical_quantity",
    }
    return AssetPlan(ASSET_TAB, GOLD_LEDGER_SECTION, event_id, sync_hash, out, "gold event detected")


def main() -> int:
    sample = [
        {"id": "trx_demo_1", "transaction_date": "2026-05-10", "note": "nabung 5 juta ke blu", "source": "demo"},
        {"id": "trx_demo_2", "transaction_date": "2026-05-10", "note": "transfer 1 juta dari bca ke blu", "source": "demo"},
        {"id": "trx_demo_3", "transaction_date": "2026-05-10", "note": "beli emas 1 gram 1800000 pakai bca", "source": "demo"},
    ]
    import json
    print(json.dumps(plan_asset_events_from_transactions(sample), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
