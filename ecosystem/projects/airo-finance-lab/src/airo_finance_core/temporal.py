"""Event clocks, source clocks and metadata-only recovery. Business calendar is WIB."""

import json, uuid, hashlib, inspect
from functools import wraps
from contextvars import ContextVar
from contextlib import contextmanager
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

WIB = ZoneInfo("Asia/Jakarta")
CONTEXT = ContextVar("finance_temporal", default={})
FIELDS = (
    "occurred_at",
    "time_precision",
    "time_accuracy",
    "time_source",
    "message_at",
    "source_sent_at",
    "source_received_at",
    "source_id",
)
EVENTS = {
    "transactions": "date",
    "credit_card_payments": "payment_date",
    "liability_payments": "payment_date",
    "asset_valuation_history": "valuation_date",
}


def iso(value):
    if not value:
        return None
    dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if dt.tzinfo is None:
        raise ValueError("Waktu harus menyertakan zona waktu")
    return dt.astimezone(timezone.utc).isoformat()


def init(db):
    c = db.get_connection()
    for table in EVENTS:
        existing = {r["name"] for r in c.execute(f"PRAGMA table_info({table})")}
        if not existing:
            continue
        for key in FIELDS:
            if key not in existing:
                default = (
                    " DEFAULT 'DATE'"
                    if key == "time_precision"
                    else " DEFAULT 'UNKNOWN'" if key == "time_accuracy" else ""
                )
                c.execute(f"ALTER TABLE {table} ADD COLUMN {key} TEXT{default}")
    c.executescript("""
    CREATE TABLE IF NOT EXISTS temporal_proposals(id TEXT PRIMARY KEY, label TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'PREVIEW', created_at TEXT NOT NULL, applied_at TEXT);
    CREATE TABLE IF NOT EXISTS temporal_proposal_items(proposal_id TEXT NOT NULL REFERENCES temporal_proposals(id), entity TEXT NOT NULL, entity_id TEXT NOT NULL, before_hash TEXT NOT NULL, before_json TEXT NOT NULL, after_json TEXT NOT NULL, evidence TEXT NOT NULL, group_name TEXT NOT NULL, applied_at TEXT, PRIMARY KEY(proposal_id,entity,entity_id));
    CREATE TABLE IF NOT EXISTS temporal_audit(id TEXT PRIMARY KEY, proposal_id TEXT, entity TEXT NOT NULL, entity_id TEXT NOT NULL, before_json TEXT NOT NULL, after_json TEXT NOT NULL, evidence TEXT NOT NULL, recorded_at TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS temporal_sources(source_id TEXT PRIMARY KEY, channel TEXT NOT NULL, source_sent_at TEXT, source_received_at TEXT NOT NULL);
    """)
    db._ensure_column_exists(c, "temporal_proposal_items", "applied_at", "TEXT")
    c.commit()


def normalize(data, event_date=None):
    d = dict(data or {})
    occurred = iso(d.get("occurred_at"))
    precision = d.get("time_precision", "MINUTE" if occurred else "DATE")
    accuracy = d.get("time_accuracy") or (
        "ESTIMATED"
        if precision == "ESTIMATED"
        or d.get("time_source") in ("TELEGRAM_MESSAGE", "EMAIL_RECEIVED", "WEB_NOW")
        else (
            "CONFIRMED"
            if occurred and d.get("time_source") in ("OWNER", "BANK_RECEIPT")
            else "UNKNOWN"
        )
    )
    if precision == "ESTIMATED":
        precision = "SECOND"
    if precision not in ("DATE", "MINUTE", "SECOND"):
        raise ValueError("Ketelitian waktu tidak valid")
    if accuracy not in ("CONFIRMED", "ESTIMATED", "UNKNOWN"):
        raise ValueError("Kepastian waktu tidak valid")
    if occurred:
        if precision == "DATE" or accuracy == "UNKNOWN":
            raise ValueError("Jam harus memiliki ketelitian dan kepastian")
        if (
            event_date
            and datetime.fromisoformat(occurred).astimezone(WIB).date().isoformat()
            != event_date
        ):
            raise ValueError(
                "Tanggal kejadian WIB berbeda dari tanggal buku besar; perlu diperiksa"
            )
    else:
        precision, accuracy = "DATE", "UNKNOWN"
    return dict(
        occurred_at=occurred,
        time_precision=precision,
        time_accuracy=accuracy,
        time_source=d.get("time_source"),
        message_at=iso(d.get("message_at")),
        source_sent_at=iso(
            d.get("source_sent_at")
            or (
                None
                if d.get("source_received_at")
                or str(d.get("source_id", "")).startswith("gmail:")
                or d.get("time_source") == "BANK_RECEIPT"
                else d.get("message_at")
            )
        ),
        source_received_at=iso(d.get("source_received_at")),
        source_id=d.get("source_id"),
    )


@contextmanager
def context(data):
    token = CONTEXT.set(dict(data or {}))
    try:
        yield
    finally:
        CONTEXT.reset(token)


def web_context(payload):
    d = dict(payload.get("temporal") or {})
    mode = d.pop("mode", None)
    now = datetime.now(timezone.utc)
    event_date = (
        payload.get("date")
        or payload.get("payment_date")
        or payload.get("purchase_date")
        or payload.get("valuation_date")
        or payload.get("disbursement_date")
    )
    if mode == "NOW":
        if event_date and event_date != now.astimezone(WIB).date().isoformat():
            raise ValueError("Transaksi lampau: isi jam atau pilih tidak diketahui")
        d.update(
            occurred_at=now.isoformat(),
            time_precision="SECOND",
            time_accuracy="ESTIMATED",
            time_source="WEB_NOW",
        )
    elif mode == "INPUT":
        clock = d.pop("clock", "")
        from datetime import time

        parsed = time.fromisoformat(clock)
        event_date = event_date or now.astimezone(WIB).date().isoformat()
        d.update(
            occurred_at=datetime.combine(
                datetime.fromisoformat(event_date).date(), parsed, WIB
            ).isoformat(),
            time_precision="SECOND" if len(clock) > 5 else "MINUTE",
            time_source="OWNER",
        )
        if d.get("time_accuracy") not in ("CONFIRMED", "ESTIMATED"):
            raise ValueError("Pilih jam pasti atau perkiraan")
    elif mode == "UNKNOWN":
        d.update(
            occurred_at=None,
            time_precision="DATE",
            time_accuracy="UNKNOWN",
            time_source=None,
        )
    d["source_received_at"] = now.isoformat()
    return normalize(d, event_date)


def write(c, table, ident, data, event_date=None):
    if table not in EVENTS:
        raise ValueError("Domain waktu tidak valid")
    values = normalize(data, event_date)
    c.execute(
        f"UPDATE {table} SET " + ",".join(k + "=?" for k in FIELDS) + " WHERE id=?",
        tuple(values[k] for k in FIELDS) + (ident,),
    )
    return values


def financial_event(fn):
    """Wrap existing posting ownership once; nested posting stays in the same transaction."""
    sig = inspect.signature(fn)

    @wraps(fn)
    def wrapped(self, *args, **kwargs):
        explicit = kwargs.pop("temporal_context", None)
        d = explicit if explicit is not None else CONTEXT.get()
        bound = sig.bind(self, *args, **kwargs)
        for name in (
            "tx_date",
            "payment_date",
            "purchase_date",
            "valuation_date",
            "disbursement_date",
        ):
            if (
                name in sig.parameters
                and not bound.arguments.get(name)
                and sig.parameters[name].default is not inspect.Parameter.empty
            ):
                bound.arguments[name] = datetime.now(WIB).date().isoformat()
        # Validate before financial writes. Unknown clocks do not invent event times.
        event_date = next(
            (
                bound.arguments[k]
                for k in (
                    "tx_date",
                    "payment_date",
                    "purchase_date",
                    "valuation_date",
                    "disbursement_date",
                )
                if bound.arguments.get(k)
            ),
            None,
        )
        normalized = normalize(d, event_date)
        c = self.db.get_connection()
        with self.db.atomic(), context(normalized):
            marks = {
                t: c.execute(f"SELECT COALESCE(MAX(rowid),0) FROM {t}").fetchone()[0]
                for t in EVENTS
            }
            result = fn(*bound.args, **bound.kwargs)
            for table, mark in marks.items():
                for row in c.execute(
                    f"SELECT * FROM {table} WHERE rowid>?", (mark,)
                ).fetchall():
                    values = normalized
                    if (
                        table != "transactions"
                        and row.keys().__contains__("transaction_id")
                        and row["transaction_id"]
                    ):
                        linked = c.execute(
                            "SELECT * FROM transactions WHERE id=?",
                            (row["transaction_id"],),
                        ).fetchone()
                        if linked:
                            values = {k: linked[k] for k in FIELDS}
                    write(c, table, row["id"], values, row[EVENTS[table]])

            def hydrate(obj):
                if hasattr(obj, "id"):
                    for t in EVENTS:
                        row = c.execute(
                            f"SELECT * FROM {t} WHERE id=?", (obj.id,)
                        ).fetchone()
                        if row:
                            for k in FIELDS:
                                setattr(obj, k, row[k])
                            break
                elif isinstance(obj, (tuple, list)):
                    for x in obj:
                        hydrate(x)
                elif isinstance(obj, dict):
                    for x in obj.values():
                        hydrate(x)

            hydrate(result)
            return result

    return wrapped


def telegram_event(fn):
    @wraps(fn)
    def wrapped(self, update):
        msg = update.get("message") or {}
        sent = (
            datetime.fromtimestamp(msg["date"], timezone.utc).isoformat()
            if msg.get("date")
            else None
        )
        source = (
            f"telegram:{msg.get('chat',{}).get('id')}:{msg.get('message_id')}"
            if msg.get("message_id")
            else None
        )
        d = dict(
            source_sent_at=sent,
            source_received_at=datetime.now(timezone.utc).isoformat(),
            source_id=source,
        )
        sender = (update.get("callback_query") or msg).get("from", {}).get("id")
        if source and self.is_owner(sender):
            with self.engine.db.atomic():
                self.engine.db.get_connection().execute(
                    "INSERT OR IGNORE INTO temporal_sources VALUES (?,?,?,?)",
                    (source, "TELEGRAM", sent, d["source_received_at"]),
                )
        with context(d):
            return fn(self, update)

    return wrapped


def fingerprint(row):
    return hashlib.sha256(
        json.dumps(dict(row), sort_keys=True, default=str).encode()
    ).hexdigest()


def linked(c, table, ident):
    if table not in EVENTS:
        raise ValueError("Domain waktu tidak valid")
    row = c.execute(f"SELECT * FROM {table} WHERE id=?", (ident,)).fetchone()
    if not row:
        raise ValueError("Catatan tidak ditemukan")
    if (
        table != "transactions"
        and "transaction_id" in row.keys()
        and row["transaction_id"]
    ):
        return linked(c, "transactions", row["transaction_id"])
    items = [(table, row)]
    if table == "transactions":
        if row["paired_transaction_id"]:
            pair = c.execute(
                "SELECT * FROM transactions WHERE id=?", (row["paired_transaction_id"],)
            ).fetchone()
            if pair:
                items.append((table, pair))
        # Payment splits share one event, funding entries keep their own clocks.
        keys = [x[1]["id"] for x in items]
        placeholders = ",".join("?" * len(keys))
        batches = c.execute(
            f"SELECT DISTINCT item_id FROM intake_transactions WHERE transaction_id IN ({placeholders}) AND role='POSTING'",
            keys,
        ).fetchall()
        for b in batches:
            for tx in c.execute(
                "SELECT t.* FROM transactions t JOIN intake_transactions i ON i.transaction_id=t.id WHERE i.item_id=? AND i.role='POSTING'",
                (b[0],),
            ):
                if tx["id"] not in keys:
                    items.append(("transactions", tx))
                    keys.append(tx["id"])
        for t in ("credit_card_payments", "liability_payments"):
            for tx in list(items):
                for p in c.execute(
                    f"SELECT * FROM {t} WHERE transaction_id=?", (tx[1]["id"],)
                ):
                    items.append((t, p))
    return items


def preview(db, changes, label="Koreksi waktu"):
    if not changes:
        raise ValueError("Tidak ada perubahan waktu")
    c = db.get_connection()
    proposal = uuid.uuid4().hex
    now = datetime.now(timezone.utc).isoformat()
    with db.atomic():
        c.execute(
            "INSERT INTO temporal_proposals(id,label,created_at) VALUES (?,?,?)",
            (proposal, label, now),
        )
        seen = {}
        for change in changes:
            for table, row in linked(
                c, change.get("entity", "transactions"), change["id"]
            ):
                previous = {k: row[k] for k in FIELDS}
                requested = dict(previous)
                requested.update(change["temporal"])
                after = normalize(requested, row[EVENTS[table]])
                key = (table, row["id"])
                if key in seen:
                    if seen[key] != after:
                        raise ValueError(
                            "Usulan waktu bertentangan dalam satu kejadian"
                        )
                    continue
                seen[key] = after
                group = (
                    "confirmed"
                    if after["time_accuracy"] == "CONFIRMED"
                    else (
                        "estimated"
                        if after["time_accuracy"] == "ESTIMATED"
                        else (
                            "source_only"
                            if after["source_sent_at"] or after["source_received_at"]
                            else "unknown"
                        )
                    )
                )
                c.execute(
                    "INSERT INTO temporal_proposal_items(proposal_id,entity,entity_id,before_hash,before_json,after_json,evidence,group_name) VALUES (?,?,?,?,?,?,?,?)",
                    (
                        proposal,
                        table,
                        row["id"],
                        fingerprint(row),
                        json.dumps(previous),
                        json.dumps(after),
                        change.get("evidence", "OWNER"),
                        group,
                    ),
                )
    return get_preview(db, proposal)


def summary(c, table, row):
    labels = {
        "transactions": "Transaksi",
        "credit_card_payments": "Pembayaran kartu",
        "liability_payments": "Pembayaran utang",
        "asset_valuation_history": "Valuasi aset",
    }
    d = dict(row)
    account = None
    if d.get("account_id"):
        acc = c.execute(
            "SELECT name FROM accounts WHERE id=?", (d["account_id"],)
        ).fetchone()
        if acc:
            account = acc[0]
    elif d.get("transaction_id"):
        acc = c.execute(
            "SELECT a.name FROM transactions t JOIN accounts a ON a.id=t.account_id WHERE t.id=?",
            (d["transaction_id"],),
        ).fetchone()
        if acc:
            account = acc[0]
    label = d.get("note") or d.get("notes") or d.get("reason") or labels[table]
    return dict(
        domain=labels[table],
        label=label,
        account=account,
        amount=d.get("amount", d.get("value")),
        date=d.get(EVENTS[table]),
    )


def get_preview(db, proposal):
    c = db.get_connection()
    p = c.execute("SELECT * FROM temporal_proposals WHERE id=?", (proposal,)).fetchone()
    if not p:
        raise ValueError("Rekapan tidak ditemukan")
    result = dict(p)
    result["items"] = []
    for row in c.execute(
        "SELECT * FROM temporal_proposal_items WHERE proposal_id=? ORDER BY entity,entity_id",
        (proposal,),
    ):
        item = dict(row)
        item["before"] = json.loads(item.pop("before_json"))
        item["after"] = json.loads(item.pop("after_json"))
        item.pop("before_hash")
        record = c.execute(
            f"SELECT * FROM {item['entity']} WHERE id=?", (item["entity_id"],)
        ).fetchone()
        item["summary"] = (
            summary(c, item["entity"], record)
            if record
            else {"label": "Catatan sudah berubah"}
        )
        result["items"].append(item)
    return result


def apply(db, proposal, groups=None):
    c = db.get_connection()
    with db.atomic():
        p = c.execute(
            "SELECT * FROM temporal_proposals WHERE id=?", (proposal,)
        ).fetchone()
        if not p:
            raise ValueError("Rekapan tidak ditemukan")
        if p["status"] == "APPLIED":
            return get_preview(db, proposal)
        rows = c.execute(
            "SELECT * FROM temporal_proposal_items WHERE proposal_id=?", (proposal,)
        ).fetchall()
        selected = [
            r
            for r in rows
            if not r["applied_at"] and (groups is None or r["group_name"] in groups)
        ]
        if not selected:
            return get_preview(db, proposal)
        for r in selected:
            row = c.execute(
                f"SELECT * FROM {r['entity']} WHERE id=?", (r["entity_id"],)
            ).fetchone()
            if not row or fingerprint(row) != r["before_hash"]:
                raise ValueError("Data berubah sejak rekapan; buat rekapan baru")
        now = datetime.now(timezone.utc).isoformat()
        for r in selected:
            write(c, r["entity"], r["entity_id"], json.loads(r["after_json"]))
            c.execute(
                "INSERT INTO temporal_audit VALUES (?,?,?,?,?,?,?,?)",
                (
                    uuid.uuid4().hex,
                    proposal,
                    r["entity"],
                    r["entity_id"],
                    r["before_json"],
                    r["after_json"],
                    r["evidence"],
                    now,
                ),
            )
            c.execute(
                "UPDATE temporal_proposal_items SET applied_at=? WHERE proposal_id=? AND entity=? AND entity_id=?",
                (now, proposal, r["entity"], r["entity_id"]),
            )
        remaining = c.execute(
            "SELECT count(*) FROM temporal_proposal_items WHERE proposal_id=? AND applied_at IS NULL",
            (proposal,),
        ).fetchone()[0]
        c.execute(
            "UPDATE temporal_proposals SET status=?,applied_at=? WHERE id=?",
            ("PARTIAL" if remaining else "APPLIED", now, proposal),
        )
        if any(
            json.loads(r["before_json"]).get("occurred_at")
            != json.loads(r["after_json"]).get("occurred_at")
            or json.loads(r["before_json"]).get("time_accuracy")
            != json.loads(r["after_json"]).get("time_accuracy")
            for r in selected
        ):
            for rule in c.execute("SELECT * FROM intake_rules").fetchall():
                payload = json.loads(rule["payload"])
                if payload.get("features", {}).get("time_slot"):
                    c.execute(
                        "UPDATE intake_rules SET enabled=0,owner_approved=0,conflicts=conflicts+1 WHERE id=?",
                        (rule["id"],),
                    )
    return get_preview(db, proposal)


def display(data):
    d = dict(data)
    v = d.get("occurred_at")
    if not v:
        return "jam tidak diketahui"
    dt = datetime.fromisoformat(v).astimezone(WIB)
    clock = dt.strftime("%H:%M:%S" if d.get("time_precision") == "SECOND" else "%H:%M")
    return (
        (
            "≈"
            if d.get("time_accuracy") == "ESTIMATED"
            or d.get("time_precision") == "ESTIMATED"
            else ""
        )
        + clock
        + " WIB"
    )


def capture_candidate(fn):
    @wraps(fn)
    def wrapped(self, *args, **kwargs):
        candidate = fn(self, *args, **kwargs)
        candidate.temporal = {
            k: CONTEXT.get().get(k)
            for k in ("source_sent_at", "source_received_at", "source_id")
        }
        return candidate

    return wrapped


def owner_accuracy(text, shared=False):
    import re

    if re.search(r"patokan|perkiraan|samakan|kira.kira", text, re.I):
        return "ESTIMATED"
    if re.search(r"\bpasti\b|sebenarnya|jam asli|tepat jam", text, re.I):
        return "CONFIRMED"
    return "ESTIMATED" if shared else "CONFIRMED"
