#!/usr/bin/env python3
"""
AIRO transaction persistence helper v0.6.

Persists record_transaction payloads into canonical Airo SQLite DB:
~/.local/share/airo-personal-workflow/airo.sqlite3

No Google write. No credential read.
"""

from __future__ import annotations

import json
import hashlib
import importlib.util
import re
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_DB_PATH = Path.home() / ".local/share/airo-personal-workflow/airo.sqlite3"

_ALIAS_PATH = Path(__file__).resolve().with_name("airo_account_aliases.py")
if _ALIAS_PATH.exists():
    _spec = importlib.util.spec_from_file_location("airo_account_aliases", _ALIAS_PATH)
    _alias_mod = importlib.util.module_from_spec(_spec)
    assert _spec is not None and _spec.loader is not None
    _spec.loader.exec_module(_alias_mod)
    normalize_account_alias = _alias_mod.normalize_account_alias
    extract_account_from_text = _alias_mod.extract_account_from_text
else:
    normalize_account_alias = None
    extract_account_from_text = None


CATEGORY_MAP = {
    "makanan": "makan",
    "makan": "makan",
    "food": "makan",
    "belanja": "belanja",
    "transport": "transport",
    "tagihan": "tagihan",
    "digital": "digital",
    "cicilan": "cicilan",
    "hutang": "hutang",
    "aset": "aset",
    "tabungan": "tabungan",
}


def canonical_category(value: Any) -> str:
    raw = str(value or "").strip().lower()
    return CATEGORY_MAP.get(raw, raw or "lainnya")


def extract_payload_value(payload: dict[str, Any], *keys: str) -> Any:
    """Return first non-empty payload value for any alias key."""
    for key in keys:
        if key in payload and payload.get(key) not in (None, ""):
            return payload.get(key)
    return None


_ACCOUNT_ALIASES = {
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


def _fallback_normalize_account(value: Any) -> str:
    raw = str(value or "").strip()
    key = re.sub(r"[^a-z0-9 ]+", " ", raw.lower())
    key = re.sub(r"\s+", " ", key).strip()

    if key in _ACCOUNT_ALIASES:
        return _ACCOUNT_ALIASES[key]

    for alias, canonical in _ACCOUNT_ALIASES.items():
        if re.search(rf"\b{re.escape(alias)}\b", key):
            return canonical

    return raw


def resolve_account(raw_text: Any = None, account: Any = None, payment_method: Any = None) -> str:
    """Resolve account alias from structured payload first, then raw text."""
    for value in (payment_method, account):
        if value:
            if normalize_account_alias is not None:
                resolved = normalize_account_alias(str(value))
                if resolved:
                    return resolved
            return _fallback_normalize_account(value)

    if raw_text and extract_account_from_text is not None:
        resolved = extract_account_from_text(str(raw_text))
        if resolved:
            return resolved

    if raw_text:
        resolved = _fallback_normalize_account(raw_text)
        if resolved != str(raw_text).strip():
            return resolved

    return ""


def _parse_number_token(token: str) -> float:
    token = str(token or "").strip().replace("_", "")
    if not token:
        return 0.0

    # Indonesian thousands style: 5.000, 1.250.000
    if re.fullmatch(r"\d{1,3}(?:\.\d{3})+", token):
        return float(token.replace(".", ""))

    # Decimal comma for compact suffixes: 1,5 juta / 2,5 rb
    if "," in token and "." not in token:
        return float(token.replace(",", "."))

    # Decimal dot for compact suffixes: 1.5 juta
    return float(token)


def _format_amount_int(value: float) -> int:
    return int(round(value))


def parse_amount(value: Any) -> int:
    """Parse IDR amount per AIRO Finance Language Contract v1.0.

    Rules:
    - 1..999 bare number means thousands: 5 -> 5000, 50 -> 50000
    - 1000+ bare number is exact rupiah: 5000 -> 5000
    - rb/ribu/k suffix means thousands
    - juta/jt/m suffix means millions
    - 1.250.000 is Indonesian thousands notation
    """
    if value is None:
        return 0

    text = str(value).strip().lower()
    if not text:
        return 0

    text = text.replace("rp", " ").replace("idr", " ")
    text = re.sub(r"\s+", " ", text)

    match = re.search(r"(\d+(?:[.,]\d+)*)\s*(juta|jt|m|rb|ribu|k)?\b", text)
    if not match:
        return 0

    token = match.group(1)
    suffix = (match.group(2) or "").lower()
    number = _parse_number_token(token)

    if suffix in {"rb", "ribu", "k"}:
        number *= 1000
    elif suffix in {"juta", "jt", "m"}:
        number *= 1000000
    elif number < 1000:
        number *= 1000

    return _format_amount_int(number)


def _amount_candidate_from_raw_text(raw_text: Any) -> tuple[int, bool]:
    """Return amount from user raw text and whether it had explicit suffix."""
    text = str(raw_text or "").strip().lower()
    if not text:
        return 0, False

    text = text.replace("rp", " ").replace("idr", " ")
    text = re.sub(r"\s+", " ", text)

    preferred = re.search(
        r"\b(?:catat|beli|bayar|transfer|nabung|tabung|simpan|tarik|jual|topup|isi|setor)\b"
        r"[^0-9]{0,40}"
        r"(\d+(?:[.,]\d+)*)\s*(juta|jt|m|rb|ribu|k)?\b",
        text,
    )
    match = preferred or re.search(r"(\d+(?:[.,]\d+)*)\s*(juta|jt|m|rb|ribu|k)?\b", text)
    if not match:
        return 0, False

    amount_text = match.group(1) + ((" " + match.group(2)) if match.group(2) else "")
    return parse_amount(amount_text), bool(match.group(2))


def correct_amount_against_raw_text(amount: int, raw_text: Any) -> int:
    """Use user's literal amount expression when upstream parsing disagrees."""
    try:
        parsed = int(amount)
    except Exception:
        return amount

    raw_amount, _raw_has_suffix = _amount_candidate_from_raw_text(raw_text)

    if raw_amount <= 0:
        return parsed

    if parsed != raw_amount:
        return raw_amount

    return parsed


def classify_finance_language(raw_text: Any) -> dict[str, str]:
    """Classify routing/category defaults per Finance Language Contract v1.0."""
    text = str(raw_text or "").strip().lower()

    if re.search(r"\b(nabung|tabung|simpan)\b", text):
        return {
            "intent": "savings_in",
            "category": "tabungan",
            "merchant": "Savings Movement",
            "cashflow_treatment": "asset_transfer",
        }

    if re.search(r"\btransfer\b", text) and re.search(r"\bdari\b.*\bke\b", text):
        return {
            "intent": "internal_transfer",
            "category": "transfer",
            "merchant": "Internal Transfer",
            "cashflow_treatment": "internal_transfer",
        }

    if re.search(r"\b(tarik|withdraw|ambil)\b", text) and re.search(r"\bdari\b", text):
        return {
            "intent": "cash_withdrawal",
            "category": "transfer",
            "merchant": "Cash Withdrawal",
            "cashflow_treatment": "internal_transfer",
        }

    if re.search(r"\b(topup|top up|isi saldo)\b", text):
        return {
            "intent": "conditional_topup",
            "category": "transfer",
            "merchant": "Top Up",
            "cashflow_treatment": "internal_transfer",
        }

    if "emas" in text or re.search(r"\bgold\b", text):
        return {
            "intent": "gold_asset",
            "category": "investasi",
            "merchant": "Gold Asset",
            "cashflow_treatment": "asset_purchase",
        }

    return {
        "intent": "expense",
        "category": "",
        "merchant": "",
        "cashflow_treatment": "operating_expense",
    }

def stable_transaction_id(raw_text: str, amount: int, category: str, payment_method: str) -> str:
    basis = "|".join([
        raw_text.strip().lower(),
        str(amount),
        category.strip().lower(),
        payment_method.strip().lower(),
        datetime.now(timezone.utc).strftime("%Y%m%d%H%M"),
    ])
    return "trx_" + hashlib.sha256(basis.encode("utf-8")).hexdigest()[:12]


# AIRO_V13_REVIEW_QUEUE_PERSISTENCE
def should_review_queue_ambiguous_finance(raw_text: str, amount: int, account: str | None, category: str | None) -> bool:
    text = " ".join(str(raw_text or "").strip().lower().split())
    finance_terms = ("bayar", "dibayar", "membayar", "belanja", "beli", "transfer", "uang", "keluar", "pengeluaran", "tagihan")
    ambiguity_terms = ("kayaknya", "mungkin", "sepertinya", "sesuatu", "lupa", "kurang ingat", "ga ingat", "gak ingat", "nggak ingat", "tidak ingat", "kemarin")
    return amount <= 0 and any(x in text for x in finance_terms) and any(x in text for x in ambiguity_terms)


def persist_review_queue_candidate(raw_text: str, db_path: str | Path, source: str = "telegram") -> dict[str, Any]:
    db_path = Path(db_path).expanduser()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    review_id = "rq_" + hashlib.sha256((source + "|" + str(raw_text).strip().lower()).encode("utf-8")).hexdigest()[:12]
    payload = {
        "schema_version": "airo.finance.v1.3.review_queue.persistence",
        "target_tab": "🧾 Review Queue",
        "queue_id": review_id,
        "raw_text": raw_text,
        "intent": "finance_capture",
        "source": source,
        "status": "pending_review",
        "duplicate_key": "review_queue:" + review_id,
        "google_write_performed": False,
    }

    con = sqlite3.connect(str(db_path))
    con.row_factory = sqlite3.Row
    try:
        existing_table = con.execute("SELECT name FROM sqlite_master WHERE type=\"table\" AND name=\"approval_queue\"").fetchone()
        if not existing_table:
            con.execute("""
            CREATE TABLE approval_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                source TEXT NOT NULL,
                action_type TEXT NOT NULL,
                title TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                risk_level TEXT NOT NULL,
                status TEXT NOT NULL,
                approval_note TEXT NOT NULL
            )
            """)
        title = "AIRO Finance Review Queue " + review_id
        cols = [r["name"] for r in con.execute("PRAGMA table_info(approval_queue)").fetchall()]

        if "payload_json" in cols:
            existing = con.execute("SELECT id FROM approval_queue WHERE title=? LIMIT 1", (title,)).fetchone()
            if existing:
                return {"ok": True, "action": "skip_duplicate_review_queue_candidate", "target_tab": "🧾 Review Queue", "queue_row_id": existing["id"], "duplicate_key": payload["duplicate_key"], "google_write_performed": False, "sqlite_mutation_performed": False}
            con.execute("""
            INSERT INTO approval_queue
            (created_at, updated_at, source, action_type, title, payload_json, risk_level, status, approval_note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (now, now, source, "google_sheets_write", title, json.dumps(payload, ensure_ascii=False, sort_keys=True), "low", "pending", "ambiguous finance needs review"))
        else:
            existing = con.execute("SELECT id FROM approval_queue WHERE entity_id=? LIMIT 1", (review_id,)).fetchone()
            if existing:
                return {"ok": True, "action": "skip_duplicate_review_queue_candidate", "target_tab": "🧾 Review Queue", "queue_row_id": existing["id"], "duplicate_key": payload["duplicate_key"], "google_write_performed": False, "sqlite_mutation_performed": False}

            data = {
                "created_at": now,
                "updated_at": now,
                "request_type": "google_sheets_write",
                "entity_type": "review_queue",
                "entity_id": review_id,
                "proposed_change_json": json.dumps(payload, ensure_ascii=False, sort_keys=True),
                "status": "pending",
                "reason": "ambiguous finance needs review",
                "decided_at": None,
                "source": source,
                "action_type": "google_sheets_write",
                "title": title,
                "risk_level": "low",
                "approval_note": "ambiguous finance needs review",
            }
            insert_cols = [c for c in data if c in cols]
            values = [data[c] for c in insert_cols]
            con.execute("INSERT INTO approval_queue (" + ", ".join(insert_cols) + ") VALUES (" + ", ".join(["?"] * len(insert_cols)) + ")", values)
        con.commit()
        rowid = con.execute("SELECT last_insert_rowid()").fetchone()[0]
        return {"ok": True, "action": "persist_review_queue_candidate", "target_tab": "🧾 Review Queue", "queue_row_id": rowid, "duplicate_key": payload["duplicate_key"], "google_write_performed": False, "sqlite_mutation_performed": True}
    finally:
        con.close()


def ensure_account(con: sqlite3.Connection, account_name: str) -> str | None:
    if not account_name:
        return None

    con.row_factory = sqlite3.Row
    row = con.execute(
        "SELECT id FROM accounts WHERE lower(name)=lower(?) LIMIT 1",
        (account_name,),
    ).fetchone()

    if row:
        return row["id"]

    account_id = "acct_" + hashlib.sha256(account_name.lower().encode("utf-8")).hexdigest()[:10]
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    con.execute(
        """
        INSERT OR IGNORE INTO accounts (id, name, type, provider, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (account_id, account_name, "asset", account_name, "active", now, now),
    )

    row = con.execute(
        "SELECT id FROM accounts WHERE lower(name)=lower(?) LIMIT 1",
        (account_name,),
    ).fetchone()

    return row["id"] if row else account_id


def persist_transaction(payload: dict[str, Any], db_path: str | Path = DEFAULT_DB_PATH) -> dict[str, Any]:
    raw_text = str(extract_payload_value(payload, "raw_text", "text", "message", "body") or "")
    amount_payload = extract_payload_value(payload, "amount", "nominal", "value")
    amount = parse_amount(amount_payload)
    amount = correct_amount_against_raw_text(amount, raw_text)
    language_route = classify_finance_language(raw_text)
    category_payload = extract_payload_value(payload, "category", "kategori")
    category = canonical_category(category_payload)
    if language_route.get("category") and category in {"", "lainnya", "uncategorized"}:
        category = canonical_category(language_route["category"])

    merchant = str(extract_payload_value(payload, "merchant", "description", "deskripsi") or category or "").strip()
    if language_route.get("merchant") and (not merchant or merchant.strip().lower() in {"lainnya", "uncategorized"}):
        merchant = language_route["merchant"]

    payment_method_raw = extract_payload_value(payload, "payment_method", "account", "akun", "account_name")
    payment_method = resolve_account(raw_text, account=extract_payload_value(payload, "account_name"), payment_method=payment_method_raw)

    if amount <= 0:
        if should_review_queue_ambiguous_finance(raw_text, amount, payment_method, category):
            return persist_review_queue_candidate(
                raw_text,
                db_path,
                source=str(extract_payload_value(payload, "source") or "telegram"),
            )
        return {
            "ok": False,
            "reason": "invalid_amount",
            "amount": amount,
            "payment_method": payment_method,
        }

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transaction_date = str(extract_payload_value(payload, "transaction_date", "date", "tanggal") or now[:10])
    currency = str(extract_payload_value(payload, "currency", "mata_uang") or "IDR")
    source = str(extract_payload_value(payload, "source") or "telegram")
    status = str(extract_payload_value(payload, "status") or "paid")
    txid = str(extract_payload_value(payload, "id", "transaction_id") or stable_transaction_id(raw_text, amount, category, payment_method))

    db_path = Path(db_path).expanduser()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    con = sqlite3.connect(str(db_path))
    con.row_factory = sqlite3.Row

    try:
        account_id = ensure_account(con, payment_method)

        existing = con.execute("SELECT id FROM transactions WHERE id=? LIMIT 1", (txid,)).fetchone()
        if existing:
            return {
                "ok": True,
                "action": "skip_duplicate",
                "transaction_id": txid,
                "payment_method": payment_method,
                "account_name": payment_method,
                "account_id": account_id,
                "amount": amount,
                "category": category,
            }

        con.execute(
            """
            INSERT INTO transactions (
              id, transaction_date, account_id, merchant, category, amount,
              currency, payment_method, billing_cycle, due_date, status, source,
              evidence_attachment_id, note, deleted_at, deleted_reason,
              created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL, ?, ?, NULL, ?, NULL, NULL, ?, ?)
            """,
            (
                txid,
                transaction_date,
                account_id,
                merchant,
                category,
                amount,
                currency,
                payment_method,
                status,
                source,
                raw_text,
                now,
                now,
            ),
        )

        try:
            con.execute(
                """
                INSERT INTO audit_log (id, entity_type, entity_id, action, before_json, after_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "audit_" + uuid.uuid4().hex[:12],
                    "transaction",
                    txid,
                    "insert",
                    None,
                    str({"amount": amount, "category": category, "payment_method": payment_method}),
                    now,
                ),
            )
        except Exception:
            pass

        con.commit()

        return {
            "ok": True,
            "action": "insert",
            "transaction_id": txid,
            "payment_method": payment_method,
            "account_name": payment_method,
            "account_id": account_id,
            "amount": amount,
            "category": category,
            "db_path": str(db_path),
        }
    finally:
        con.close()
