"""Recover structured time evidence only. Never posts transactions or logs source bodies."""

import json, hashlib, re
from datetime import datetime, timezone
from . import temporal as t
from .gmail_details import body, facts


def collect(
    db,
    gmail=None,
    telegram_export=None,
    owner_overrides=None,
    expected_telegram_owner=None,
):
    c = db.get_connection()
    changes = []
    errors = []
    c.execute(
        "CREATE TABLE IF NOT EXISTS temporal_recovery_evidence(source_id TEXT PRIMARY KEY, facts TEXT NOT NULL, error_code TEXT, checked_at TEXT NOT NULL)"
    )
    c.commit()
    mail = {
        r["tx_id"]: r["message_id"]
        for r in c.execute(
            "SELECT t.id AS tx_id,e.message_id FROM transactions t JOIN review_queue r ON r.approved_transaction_id=t.id JOIN processed_emails e ON e.review_item_id=r.id WHERE t.status IN ('ACTIVE','CORRECTED')"
        )
    }
    exported = {}
    if telegram_export:
        if not expected_telegram_owner:
            raise ValueError("Telegram export requires verified owner ID")
        for m in telegram_export.get("messages", []):
            if str(m.get("from_id", "")).removeprefix("user") != str(
                expected_telegram_owner
            ):
                continue
            text = m.get("text", "")
            if isinstance(text, list):
                text = "".join(
                    x if isinstance(x, str) else x.get("text", "") for x in text
                )
            if not text or m.get("type") != "message":
                continue
            digest = hashlib.sha256(text.strip().lower().encode()).hexdigest()
            exported.setdefault(digest, []).append(m)
    raw = {}
    raw_by_transaction = {}
    for row in c.execute(
        "SELECT transaction_id,raw_input FROM transaction_metadata WHERE raw_input IS NOT NULL"
    ):
        raw_by_transaction[row["transaction_id"]] = row["raw_input"]
        digest = hashlib.sha256(row["raw_input"].strip().lower().encode()).hexdigest()
        raw.setdefault(digest, []).append(row["transaction_id"])
    chat = {}
    for digest, messages in exported.items():
        ids = raw.get(digest, [])
        if len(messages) == 1 and len(ids) == 1:
            m = messages[0]
            stamp = m.get("date_unixtime")
            if stamp:
                chat[ids[0]] = dict(
                    source_sent_at=datetime.fromtimestamp(
                        int(stamp), timezone.utc
                    ).isoformat(),
                    source_id=f"telegram-export:{telegram_export.get('id')}:{m.get('id')}",
                )
    for row in c.execute(
        "SELECT * FROM transactions WHERE status IN ('ACTIVE','CORRECTED') ORDER BY date,created_at,id"
    ).fetchall():
        d = {k: row[k] for k in t.FIELDS}
        evidence = "RECORDED_TIME_ONLY"
        need = not row["occurred_at"] or row["time_accuracy"] == "UNKNOWN"
        if not need:
            continue
        if row["id"] in (owner_overrides or {}):
            d.update(owner_overrides[row["id"]])
            evidence = "OWNER_CONFIRMED_TIME_QUALITY_CORRECTION"
        elif row["id"] in mail:
            mid = mail[row["id"]]
            source = "gmail:" + mid
            cached = c.execute(
                "SELECT * FROM temporal_recovery_evidence WHERE source_id=?", (source,)
            ).fetchone()
            if cached and not cached["error_code"]:
                f = json.loads(cached["facts"])
            elif gmail:
                try:
                    m = (
                        gmail.users()
                        .messages()
                        .get(userId="me", id=mid, format="full")
                        .execute()
                    )
                    f = facts(body(m))
                    f["source_id"] = source
                    if m.get("internalDate"):
                        f["source_received_at"] = datetime.fromtimestamp(
                            int(m["internalDate"]) / 1000, timezone.utc
                        ).isoformat()
                    with db.atomic():
                        c.execute(
                            "INSERT OR REPLACE INTO temporal_recovery_evidence VALUES (?,?,NULL,?)",
                            (
                                source,
                                json.dumps(f),
                                datetime.now(timezone.utc).isoformat(),
                            ),
                        )
                except Exception as exc:
                    status = getattr(getattr(exc, "resp", None), "status", None)
                    code = (
                        "GMAIL_AUTH_REQUIRED"
                        if status in (401, 403)
                        else "GMAIL_" + type(exc).__name__
                    )
                    if status in (401, 403):
                        gmail = None
                    errors.append({"source_id": source, "code": code})
                    f = {"source_id": source}
                    with db.atomic():
                        c.execute(
                            "INSERT OR REPLACE INTO temporal_recovery_evidence VALUES (?,?,?,?)",
                            (
                                source,
                                json.dumps(f),
                                code,
                                datetime.now(timezone.utc).isoformat(),
                            ),
                        )
            else:
                f = {"source_id": source}
                errors.append({"source_id": source, "code": "GMAIL_NOT_AVAILABLE"})
            if f.get("occurred_at"):
                try:
                    t.normalize(f, row["date"])
                except ValueError:
                    f.pop("occurred_at", None)
                    f.pop("time_precision", None)
                    f.pop("time_accuracy", None)
                    errors.append({"source_id": source, "code": "EVENT_DATE_CONFLICT"})
            d.update(f)
            evidence = (
                "BANK_EVENT_TIME" if f.get("occurred_at") else "EMAIL_RECEIVED_ONLY"
            )
            matching_errors = [e["code"] for e in errors if e["source_id"] == source]
            if matching_errors:
                evidence = "NEEDS_REVIEW:" + matching_errors[-1]
        elif row["id"] in chat:
            d.update(chat[row["id"]])
            evidence = "MATCHED_TELEGRAM_EXPORT_SOURCE_TIME"
            original = raw_by_transaction.get(row["id"], "")
            # Only a matched, single, immediate owner input supplies an estimated event clock.
            # Past/batch inputs retain a separate source timestamp, not a fabricated hour.
            if "\n" not in original and not re.search(
                r"kemarin|kemaren|semalam|lalu|tadi|sebelum|tanggal|\btgl\b",
                original,
                re.I,
            ):
                sent = datetime.fromisoformat(d["source_sent_at"]).astimezone(t.WIB)
                if sent.date().isoformat() == row["date"]:
                    d.update(
                        occurred_at=d["source_sent_at"],
                        time_precision="SECOND",
                        time_accuracy="ESTIMATED",
                        time_source="TELEGRAM_MESSAGE",
                    )
                    evidence = "MATCHED_IMMEDIATE_OWNER_CHAT_ESTIMATE"

        elif row["message_at"]:
            d["source_sent_at"] = row["message_at"]
            evidence = "STORED_MESSAGE_TIME"
        # Source clocks are displayed separately, never silently relabeled as event clocks.
        changes.append(
            dict(entity="transactions", id=row["id"], temporal=d, evidence=evidence)
        )
    posted = {x["id"] for x in changes}
    for table in (
        "credit_card_payments",
        "liability_payments",
        "asset_valuation_history",
    ):
        for row in c.execute(f"SELECT * FROM {table}").fetchall():
            if row["occurred_at"] and row["time_accuracy"] != "UNKNOWN":
                continue
            if "transaction_id" in row.keys() and row["transaction_id"] in posted:
                continue
            d = {k: row[k] for k in t.FIELDS}
            if "transaction_id" in row.keys() and row["transaction_id"]:
                tx = c.execute(
                    "SELECT * FROM transactions WHERE id=?", (row["transaction_id"],)
                ).fetchone()
                if tx:
                    d = {k: tx[k] for k in t.FIELDS}
            changes.append(
                dict(
                    entity=table,
                    id=row["id"],
                    temporal=d,
                    evidence="LINKED_LEDGER_OR_RECORDED_TIME_ONLY",
                )
            )
    result = (
        t.preview(db, changes, "Pemulihan waktu seluruh riwayat Finance")
        if changes
        else {"items": [], "status": "EMPTY"}
    )
    result["recovery_errors"] = errors
    return result
