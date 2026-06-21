import json
import sqlite3
from uuid import uuid4

from airo_personal_workflow.core.config import DB_PATH
from airo_personal_workflow.db.init_db import init_db
from airo_personal_workflow.intents.parser import parse_user_message

def connect() -> sqlite3.Connection:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def _id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"

def audit(
    conn: sqlite3.Connection,
    action: str,
    entity_type: str,
    entity_id: str,
    after: dict,
    risk_level: str = "L1_safe_write",
) -> None:
    conn.execute(
        """
        INSERT INTO audit_log (
          id, action, entity_type, entity_id, before_json, after_json, risk_level, approval_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            _id("aud"),
            action,
            entity_type,
            entity_id,
            None,
            json.dumps(after, ensure_ascii=False),
            risk_level,
            "auto",
        ),
    )

def get_or_create_account(conn: sqlite3.Connection, name: str | None, account_type: str = "unknown") -> str | None:
    if not name:
        return None

    existing = conn.execute(
        "SELECT id FROM accounts WHERE lower(name) = lower(?) LIMIT 1",
        (name,),
    ).fetchone()

    if existing:
        return existing["id"]

    account_id = _id("acct")
    conn.execute(
        """
        INSERT INTO accounts (id, name, type, provider)
        VALUES (?, ?, ?, ?)
        """,
        (account_id, name, account_type, name),
    )
    audit(conn, "create_account", "account", account_id, {"name": name, "type": account_type})
    return account_id

def get_or_create_installment(conn: sqlite3.Connection, name: str) -> str:
    existing = conn.execute(
        "SELECT id FROM installments WHERE lower(name) = lower(?) AND deleted_at IS NULL LIMIT 1",
        (name,),
    ).fetchone()

    if existing:
        return existing["id"]

    installment_id = _id("inst")
    conn.execute(
        """
        INSERT INTO installments (id, name, status, note)
        VALUES (?, ?, 'active', ?)
        """,
        (installment_id, name, "Auto-created from Telegram payment. Detail can be completed later."),
    )
    audit(conn, "create_installment", "installment", installment_id, {"name": name})
    return installment_id


# AIRO_FINANCE_CONTRACT_V1_1
def _airo_fc_v1_1_amount(raw_text: str):
    import re

    text = str(raw_text or "").lower()
    m = re.search(r"(?<!\d)(\d+(?:[.,]\d+)?)(?:\s*)(rb|ribu|k)\b", text)
    if m:
        base = float(m.group(1).replace(",", "."))
        return int(base * 1000)

    m = re.search(r"(?<!\d)(\d{1,3}(?:\.\d{3})+)(?!\d)", text)
    if m:
        return int(m.group(1).replace(".", ""))

    m = re.search(r"(?<!\d)(\d+)(?!\d)", text)
    if not m:
        return None

    n = int(m.group(1))
    if n < 1000 and any(w in text for w in ["nabung", "tabung", "saving", "simpan"]):
        return n * 1000
    return n


def _airo_fc_v1_1_account(raw_text: str) -> str:
    text = str(raw_text or "").lower()
    if "blu" in text or "blubca" in text or "blu bca" in text:
        return "BLU BCA"
    if "gopay" in text or "go pay" in text:
        return "GoPay"
    if "ovo" in text:
        return "OVO"
    if "dana" in text:
        return "DANA"
    if "cash" in text or "tunai" in text:
        return "Cash"
    return "uncategorized"


def apply_finance_contract_v1_1(parsed: dict, raw_text: str) -> dict:
    import hashlib
    from datetime import date

    text = str(raw_text or "").strip()
    low = text.lower()
    out = dict(parsed or {})

    finance_keywords = [
        "nabung", "tabung", "saving", "simpan",
        "tarik cash", "tarik tunai", "ambil cash", "ambil tunai",
        "topup", "top up", "isi gopay", "isi ovo", "isi dana",
        "transfer", "pindah", "pindahin",
    ]
    if not any(k in low for k in finance_keywords):
        return out

    amount = _airo_fc_v1_1_amount(low)
    if not amount:
        return out

    source_account = _airo_fc_v1_1_account(low)

    if any(k in low for k in ["nabung", "tabung", "saving", "simpan"]):
        category = "tabungan"
        account_name = source_account
        payment_method = source_account
    elif any(k in low for k in ["tarik cash", "tarik tunai", "ambil cash", "ambil tunai"]):
        category = "cash_withdrawal"
        account_name = "Cash"
        payment_method = source_account if source_account != "Cash" else "Cash"
    elif any(k in low for k in ["topup", "top up", "isi gopay", "isi ovo", "isi dana"]):
        category = "ewallet_topup"
        if "gopay" in low or "go pay" in low:
            account_name = "GoPay"
        elif "ovo" in low:
            account_name = "OVO"
        elif "dana" in low:
            account_name = "DANA"
        else:
            account_name = "e-wallet"
        payment_method = source_account if source_account not in {"GoPay", "OVO", "DANA", "Cash"} else "uncategorized"
    else:
        category = out.get("category") or "transfer"
        account_name = source_account
        payment_method = source_account

    stable = hashlib.sha1(f"{date.today()}|{low}|{amount}|{category}|{payment_method}".encode()).hexdigest()[:12]

    out.update({
        "id": out.get("id") or f"trx_{stable}",
        "intent": "record_transaction",
        "transaction_date": out.get("transaction_date") or str(date.today()),
        "account_name": account_name,
        "category": category,
        "amount": amount,
        "currency": "IDR",
        "payment_method": payment_method,
        "source": out.get("source") or "telegram",
        "raw_text": text,
        "status": out.get("status") or "parsed",
        "finance_contract": "v1.1",
    })
    return out


def _active_transaction_semantic_duplicate(conn: sqlite3.Connection, parsed: dict, text: str):
    """Find an active transaction that represents the same user command.

    This prevents repeated Telegram/OpenClaw retries from inserting new rows
    when the earlier write already succeeded but the reply path failed.
    """
    account = parsed.get("account_name") or parsed.get("payment_method") or ""
    category = parsed.get("category") or ""
    transaction_date = parsed.get("transaction_date") or ""

    return conn.execute(
        """
        SELECT rowid, id, transaction_date, account_id, merchant, category, amount,
               currency, payment_method, status, source, note, created_at, updated_at
        FROM transactions
        WHERE deleted_at IS NULL
          AND lower(COALESCE(note, '')) = lower(?)
          AND amount = ?
          AND lower(COALESCE(payment_method, '')) = lower(?)
          AND lower(COALESCE(category, '')) = lower(?)
          AND COALESCE(transaction_date, '') = COALESCE(?, '')
        ORDER BY rowid ASC
        LIMIT 1
        """,
        (
            str(text or "").strip(),
            parsed.get("amount"),
            str(account or "").strip(),
            str(category or "").strip(),
            str(transaction_date or "").strip(),
        ),
    ).fetchone()


def record_transaction(text: str) -> dict:
    parsed = parse_user_message(text)
    parsed = apply_finance_contract_v1_1(parsed, text)

    if parsed["intent"] != "record_transaction":
        return {"ok": False, "reason": "not_transaction", "parsed": parsed}

    if not parsed.get("amount"):
        return {"ok": False, "reason": "amount_missing", "parsed": parsed}

    with connect() as conn:
        existing = _active_transaction_semantic_duplicate(conn, parsed, text)
        if existing:
            out = dict(parsed)
            out.update(
                {
                    "id": existing["id"],
                    "account_id": existing["account_id"],
                    "transaction_id": existing["id"],
                    "persist_action": "skip_duplicate",
                    "action": "skip_duplicate",
                    "already_recorded": True,
                    "rowid": existing["rowid"],
                }
            )
            return out

        account_id = get_or_create_account(conn, parsed.get("account_name"), "credit_or_payment")

        conn.execute(
            """
            INSERT INTO transactions (
              id, transaction_date, account_id, merchant, category, amount, currency,
              payment_method, status, source, note
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                parsed["id"],
                parsed["transaction_date"],
                account_id,
                parsed.get("account_name"),
                parsed.get("category"),
                parsed["amount"],
                parsed.get("currency", "IDR"),
                parsed.get("payment_method"),
                parsed.get("status", "parsed"),
                parsed.get("source", "telegram"),
                text,
            ),
        )
        audit(conn, "record_transaction", "transaction", parsed["id"], parsed, "L1_safe_write")

    parsed["account_id"] = account_id
    parsed["transaction_id"] = parsed["id"]
    parsed["persist_action"] = "insert"
    return parsed

def record_installment_payment(text: str) -> dict:
    parsed = parse_user_message(text)

    if parsed["intent"] != "record_installment_payment":
        raise ValueError(f"Not an installment payment intent: {parsed['intent']}")

    if not parsed.get("amount"):
        raise ValueError("Amount not found")

    with connect() as conn:
        installment_id = get_or_create_installment(conn, parsed["installment_name"])
        payment_id = parsed["id"]

        current = conn.execute(
            "SELECT paid_installments FROM installments WHERE id = ?",
            (installment_id,),
        ).fetchone()
        next_number = int(current["paid_installments"] or 0) + 1

        conn.execute(
            """
            INSERT INTO installment_payments (
              id, installment_id, payment_date, installment_number, amount, method, verified, note
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payment_id,
                installment_id,
                parsed["payment_date"],
                next_number,
                parsed["amount"],
                parsed.get("method"),
                "no",
                parsed.get("raw_text"),
            ),
        )

        conn.execute(
            """
            UPDATE installments
            SET paid_installments = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (next_number, installment_id),
        )

        enriched = dict(parsed)
        enriched["installment_number"] = next_number
        audit(conn, "record_installment_payment", "installment_payment", payment_id, enriched, "L2_audit_write")
        return enriched

def record_from_text(text: str) -> dict:
    parsed = parse_user_message(text)

    if parsed["intent"] == "record_transaction":
        return record_transaction(text)

    if parsed["intent"] == "record_installment_payment":
        return record_installment_payment(text)

    return parsed

def check_installment(name: str) -> dict:
    with connect() as conn:
        row = conn.execute(
            """
            SELECT id, name, total_installments, paid_installments, monthly_amount, next_due_date, status
            FROM installments
            WHERE lower(name) = lower(?) AND deleted_at IS NULL
            LIMIT 1
            """,
            (name,),
        ).fetchone()

        if not row:
            return {
                "found": False,
                "name": name,
                "message": f"{name} belum ada di database.",
            }

        payments = conn.execute(
            """
            SELECT payment_date, installment_number, amount, verified, note
            FROM installment_payments
            WHERE installment_id = ?
            ORDER BY installment_number DESC, created_at DESC
            LIMIT 5
            """,
            (row["id"],),
        ).fetchall()

        return {
            "found": True,
            "installment": dict(row),
            "recent_payments": [dict(p) for p in payments],
        }

def monthly_summary(period: str) -> dict:
    start = f"{period}-01"

    if period.endswith("-12"):
        y = int(period[:4]) + 1
        end = f"{y}-01-01"
    else:
        y = int(period[:4])
        m = int(period[5:7]) + 1
        end = f"{y}-{m:02d}-01"

    with connect() as conn:
        total = conn.execute(
            """
            SELECT COALESCE(SUM(amount), 0) AS total, COUNT(*) AS count
            FROM transactions
            WHERE transaction_date >= ?
              AND transaction_date < ?
              AND deleted_at IS NULL
            """,
            (start, end),
        ).fetchone()

        by_category = conn.execute(
            """
            SELECT category, COALESCE(SUM(amount), 0) AS total, COUNT(*) AS count
            FROM transactions
            WHERE transaction_date >= ?
              AND transaction_date < ?
              AND deleted_at IS NULL
            GROUP BY category
            ORDER BY total DESC
            """,
            (start, end),
        ).fetchall()

        installments = conn.execute(
            """
            SELECT COALESCE(SUM(amount), 0) AS total, COUNT(*) AS count
            FROM installment_payments
            WHERE payment_date >= ?
              AND payment_date < ?
            """,
            (start, end),
        ).fetchone()

        audit_count = conn.execute(
            "SELECT COUNT(*) AS count FROM audit_log WHERE created_at >= ? AND created_at < ?",
            (start, end),
        ).fetchone()

    return {
        "period": period,
        "transactions": dict(total),
        "transactions_by_category": [dict(row) for row in by_category],
        "installment_payments": dict(installments),
        "audit_log": dict(audit_count),
    }
