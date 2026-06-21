import csv
import json
import sqlite3
from pathlib import Path

from airo_personal_workflow.core.config import DB_PATH

EXPORT_DIR = Path("exports/personal-workflow")

def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def export_transactions_csv(period: str) -> str:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    out = EXPORT_DIR / f"transactions_{period}.csv"

    start = f"{period}-01"
    y = int(period[:4])
    m = int(period[5:7])
    end = f"{y + 1}-01-01" if m == 12 else f"{y}-{m + 1:02d}-01"

    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT
              t.id,
              t.transaction_date,
              COALESCE(a.name, '') AS account,
              t.merchant,
              t.category,
              t.amount,
              t.currency,
              t.status,
              t.source,
              t.note
            FROM transactions t
            LEFT JOIN accounts a ON a.id = t.account_id
            WHERE t.transaction_date >= ?
              AND t.transaction_date < ?
              AND t.deleted_at IS NULL
            ORDER BY t.transaction_date ASC, t.created_at ASC
            """,
            (start, end),
        ).fetchall()

    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "id", "transaction_date", "account", "merchant", "category",
                "amount", "currency", "status", "source", "note"
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(dict(row))

    return str(out)

def export_installments_csv(period: str) -> str:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    out = EXPORT_DIR / f"installment_payments_{period}.csv"

    start = f"{period}-01"
    y = int(period[:4])
    m = int(period[5:7])
    end = f"{y + 1}-01-01" if m == 12 else f"{y}-{m + 1:02d}-01"

    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT
              p.id,
              i.name AS installment_name,
              p.payment_date,
              p.installment_number,
              p.amount,
              p.method,
              p.verified,
              p.note
            FROM installment_payments p
            JOIN installments i ON i.id = p.installment_id
            WHERE p.payment_date >= ?
              AND p.payment_date < ?
            ORDER BY p.payment_date ASC, p.installment_number ASC
            """,
            (start, end),
        ).fetchall()

    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "id", "installment_name", "payment_date", "installment_number",
                "amount", "method", "verified", "note"
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(dict(row))

    return str(out)

def export_summary_json(summary: dict, period: str) -> str:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    out = EXPORT_DIR / f"summary_{period}.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(out)
