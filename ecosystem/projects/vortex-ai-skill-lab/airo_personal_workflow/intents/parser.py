from __future__ import annotations

import datetime
import hashlib
import re
from typing import Any


AMOUNT_PATTERN = re.compile(r"(?:rp|idr)?\s*(\d+(?:[.,]\d+)*)\s*(rb|ribu|k|jt|juta|m)?\b", re.I)

ACCOUNT_ALIASES = {
    "blu": "BLU BCA",
    "blubca": "BLU BCA",
    "blu bca": "BLU BCA",
    "bca": "BCA",
    "mandiri": "Mandiri",
    "gopay": "GoPay",
    "go pay": "GoPay",
    "shopeepay": "ShopeePay",
    "shopee pay": "ShopeePay",
    "cash": "Cash",
    "tunai": "Cash",
}

EXPENSE_CATEGORY_KEYWORDS = {
    "makan": "makan",
    "makanan": "makan",
    "kopi": "makan",
    "belanja": "belanja",
    "transport": "transport",
    "grab": "transport",
    "gojek": "transport",
    "tagihan": "tagihan",
    "listrik": "tagihan",
    "internet": "tagihan",
    "pulsa": "digital",
    "digital": "digital",
    "cicilan": "cicilan",
    "hutang": "hutang",
}


def _clean_text(text: Any) -> str:
    return str(text or "").strip().lower()


def _parse_number_token(token: str) -> float:
    token = str(token or "").strip().replace("_", "")
    if not token:
        return 0.0

    # Indonesian thousands notation: 5.000, 1.250.000
    if re.fullmatch(r"\d{1,3}(?:\.\d{3})+", token):
        return float(token.replace(".", ""))

    # Decimal comma for suffix amounts: 1,5 juta
    if "," in token and "." not in token:
        return float(token.replace(",", "."))

    return float(token)


def parse_amount(text: Any) -> int | None:
    """Parse amount according to AIRO Finance Language Contract v1.0.

    Bare numbers:
    - 1..999 mean thousands: 5 -> 5000, 50 -> 50000
    - 1000+ are exact rupiah: 5000 -> 5000

    Suffixes:
    - rb/ribu/k => x1000
    - jt/juta/m => x1000000
    """
    raw = _clean_text(text)
    if not raw:
        return None

    match = AMOUNT_PATTERN.search(raw)
    if not match:
        return None

    number = _parse_number_token(match.group(1))
    suffix = (match.group(2) or "").lower()

    if suffix in {"rb", "ribu", "k"}:
        number *= 1000
    elif suffix in {"jt", "juta", "m"}:
        number *= 1000000
    elif number < 1000:
        number *= 1000

    return int(round(number))


def detect_account(text: Any) -> str | None:
    raw = _clean_text(text)
    if not raw:
        return None

    normalized = re.sub(r"[^a-z0-9 ]+", " ", raw)
    normalized = re.sub(r"\s+", " ", normalized).strip()

    # Prefer explicit account markers.
    for marker in ("pakai", "via", "dari", "ke"):
        m = re.search(rf"\b{marker}\s+([a-zA-Z0-9 ]{{2,25}})", normalized)
        if m:
            chunk = m.group(1).strip()
            for alias, canonical in sorted(ACCOUNT_ALIASES.items(), key=lambda x: -len(x[0])):
                if re.search(rf"\b{re.escape(alias)}\b", chunk):
                    return canonical

    for alias, canonical in sorted(ACCOUNT_ALIASES.items(), key=lambda x: -len(x[0])):
        if re.search(rf"\b{re.escape(alias)}\b", normalized):
            return canonical

    return None


def detect_category(text: Any) -> str:
    raw = _clean_text(text)

    if re.search(r"\b(nabung|tabung|simpan)\b", raw):
        return "tabungan"

    if re.search(r"\btransfer\b", raw) and re.search(r"\bdari\b.*\bke\b", raw):
        return "transfer"

    if re.search(r"\b(tarik|withdraw|ambil)\b", raw) and re.search(r"\bdari\b", raw):
        return "transfer"

    if re.search(r"\b(topup|top up|isi saldo)\b", raw):
        return "transfer"

    if "emas" in raw or re.search(r"\bgold\b", raw):
        return "investasi"

    for keyword, category in EXPENSE_CATEGORY_KEYWORDS.items():
        if re.search(rf"\b{re.escape(keyword)}\b", raw):
            return category

    return "uncategorized"


def detect_installment_name(text: Any) -> str | None:
    raw = _clean_text(text)
    patterns = [
        r"(?:cicilan|angsuran)\s+([a-zA-Z0-9 _.-]+?)(?:\s+ke[- ]?\d+|\s+rp|\s+\d|$)",
        r"(?:bayar)\s+([a-zA-Z0-9 _.-]+?)\s+(?:cicilan|angsuran)",
    ]
    for pattern in patterns:
        m = re.search(pattern, raw, re.I)
        if m:
            return m.group(1).strip()
    return None


def classify_intent(text: Any) -> str:
    raw = _clean_text(text)
    has_amount = parse_amount(raw) is not None
    has_installment = bool(re.search(r"\b(cicilan|angsuran)\b", raw))
    has_check = bool(re.search(r"\b(cek|check|status|sisa|berapa)\b", raw))
    has_report = bool(re.search(r"\b(laporan|summary|ringkasan|rekap)\b", raw))

    if has_report:
        return "monthly_report"

    if has_installment and has_check and not has_amount:
        return "check_installment"

    if has_installment and has_amount:
        return "record_installment_payment"

    if has_amount:
        return "record_transaction"

    return "unknown"


def _stable_id(prefix: str, text: str, amount: int | None, category: str, account: str | None) -> str:
    basis = "|".join([
        _clean_text(text),
        str(amount or ""),
        category or "",
        account or "",
        datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d%H%M"),
    ])
    return prefix + "_" + hashlib.sha256(basis.encode("utf-8")).hexdigest()[:12]


def parse_transaction(text: Any) -> dict:
    raw = str(text or "").strip()
    amount = parse_amount(raw)
    account = detect_account(raw)
    category = detect_category(raw)

    return {
        "id": _stable_id("trx", raw, amount, category, account),
        "intent": "record_transaction",
        "transaction_date": datetime.date.today().isoformat(),
        "account_name": account,
        "category": category,
        "amount": amount,
        "currency": "IDR",
        "payment_method": account,
        "source": "telegram",
        "raw_text": raw,
        "status": "parsed" if amount else "needs_review",
    }


def parse_installment_payment(text: Any) -> dict:
    raw = str(text or "").strip()
    amount = parse_amount(raw)
    name = detect_installment_name(raw)
    return {
        "id": _stable_id("pay", raw, amount, "cicilan", detect_account(raw)),
        "intent": "record_installment_payment",
        "installment_name": name,
        "payment_date": datetime.date.today().isoformat(),
        "installment_number": None,
        "amount": amount,
        "currency": "IDR",
        "method": detect_account(raw),
        "raw_text": raw,
        "status": "parsed" if amount else "needs_review",
    }


def parse_check_installment(text: Any) -> dict:
    raw = str(text or "").strip()
    return {
        "intent": "check_installment",
        "installment_name": detect_installment_name(raw),
        "raw_text": raw,
    }


def parse_monthly_report(text: Any) -> dict:
    raw = str(text or "").strip()
    m = re.search(r"\b(20\d{2}-\d{2})\b", raw)
    period = m.group(1) if m else datetime.date.today().strftime("%Y-%m")
    return {
        "intent": "monthly_report",
        "period": period,
        "raw_text": raw,
    }


def parse_user_message(text: Any) -> dict:
    intent = classify_intent(text)

    if intent == "record_transaction":
        return parse_transaction(text)
    if intent == "record_installment_payment":
        return parse_installment_payment(text)
    if intent == "check_installment":
        return parse_check_installment(text)
    if intent == "monthly_report":
        return parse_monthly_report(text)

    return {
        "intent": "unknown",
        "raw_text": str(text or "").strip(),
        "status": "needs_review",
    }
