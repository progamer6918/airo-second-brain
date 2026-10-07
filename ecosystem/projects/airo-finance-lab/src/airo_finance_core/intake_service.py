"""Draft orchestration and atomic posting; model output never writes the ledger."""

import hashlib
import html
import json
import math
import re
import time
from datetime import datetime, timedelta, date
from . import intake_parser as parser
from .intake_store import dump, uid
from .gmail_reliability import enqueue
from .telegram_capture import format_idr


class IntakeService:
    def __init__(self, engine):
        self.engine = engine
        self.db = engine.db

    @property
    def conn(self):
        return self.db.get_connection()

    def rows(self, batch):
        return [
            {**dict(r), "data": json.loads(r["data"])}
            for r in self.conn.execute(
                "SELECT * FROM intake_items WHERE batch_id=? ORDER BY number", (batch,)
            )
        ]

    def owned(self, batch, owner):
        return bool(
            self.conn.execute(
                "SELECT 1 FROM intake_batches WHERE id=? AND owner=?",
                (batch, str(owner)),
            ).fetchone()
        )

    def create(self, owner, source_key, text, now=None, items=None):
        previous = self.conn.execute(
            "SELECT id FROM intake_batches WHERE source_key=? AND owner=?",
            (source_key, str(owner)),
        ).fetchone()
        if previous:
            return previous[0]
        entries = (
            items if items is not None else parser.parse_batch(self.engine, text, now)
        )
        if not entries:
            raise ValueError("Tidak ada transaksi yang terbaca")
        if items is None:
            from .intake_learning import historical_suggestion, suggest

            entries = [
                suggest(self, historical_suggestion(self.engine, d)) for d in entries
            ]
        from .intake_learning import features

        seen = set()
        for data in entries:
            signature = dump(
                {
                    "features": features(data),
                    "date": data.get("date"),
                    "occurred_at": data.get("occurred_at"),
                }
            )
            if signature in seen:
                data["possible_duplicate_in_batch"] = True
            seen.add(signature)
        batch = uid()
        digest = hashlib.sha256(text.lower().strip().encode()).hexdigest()
        with self.db.atomic():
            self.conn.execute(
                "INSERT INTO intake_batches VALUES (?,?,?,?,?,?,?)",
                (
                    batch,
                    str(owner),
                    source_key,
                    digest,
                    "DRAFT",
                    time.time(),
                    time.time(),
                ),
            )
            for number, data in enumerate(entries, 1):
                item = uid()
                self.conn.execute(
                    "INSERT INTO intake_items VALUES (?,?,?,?,?)",
                    (item, batch, number, dump(data), "DRAFT"),
                )
            self.conn.execute(
                "INSERT INTO intake_context VALUES (?,?,?) ON CONFLICT(owner) DO UPDATE SET batch_id=excluded.batch_id,mode=excluded.mode",
                (str(owner), batch, "DETAIL"),
            )
        return batch

    def from_review(self, owner, review_id):
        review = self.engine.get_review_queue_item(review_id)
        if not review or review.status != "PENDING":
            raise ValueError("Kartu ini sudah diproses")
        p = json.loads(review.parsed_result)
        data = {
            k: p.get(k)
            for k in (
                "amount",
                "account_id",
                "account_name",
                "direction",
                "date",
                "note",
                "merchant",
                "category_id",
                "category_name",
                "subcategory_id",
                "subcategory_name",
                "occurred_at",
                "message_at",
                "time_precision",
                "time_source",
                "destination_account_id",
                "credit_card_id",
            )
        }
        data.update(
            {
                "review_id": review_id,
                "direction_unknown": p.get("direction_known") is False,
                "time_precision": p.get("time_precision", "DATE"),
                "note": p.get("merchant") or p.get("note") or "",
                "facts_confirmed": False,
                "user_labels_verified": False,
            }
        )
        if data.get("direction") not in ("TRANSFER", "CC_PAYMENT") and data[
            "note"
        ].lower() in (
            "transaksimu pakai blu berhasil",
            "internet transaction journal",
            "info transaksi masuk ke blu kamu",
        ):
            data.update(
                category_id=None,
                subcategory_id=None,
                category_name=None,
                subcategory_name=None,
                needs_purpose=True,
            )
        batch = self.create(
            owner, "review:" + review_id, "review:" + review_id, items=[data]
        )
        row = self.rows(batch)[0]
        with self.db.atomic():
            mid = p.get("message_id") or review_id
            existing = self.conn.execute(
                "SELECT item_id FROM intake_sources WHERE kind=? AND source_id=?",
                ("GMAIL", mid),
            ).fetchone()
            if existing and existing[0] != row["id"]:
                raise ValueError("Email ini sudah terhubung ke draft lain")
            self.conn.execute(
                "INSERT OR IGNORE INTO intake_sources VALUES (?,?,?)",
                ("GMAIL", mid, row["id"]),
            )
        return batch

    def _update(self, row, data):
        for key in (
            "account_id",
            "category_id",
            "subcategory_id",
            "date",
            "note",
            "direction",
            "amount",
        ):
            if row["data"].get(key) != data.get(key):
                self.conn.execute(
                    "INSERT INTO intake_feedback VALUES (?,?,?,?,?,?)",
                    (
                        uid(),
                        row["id"],
                        key,
                        dump(row["data"].get(key)),
                        dump(data.get(key)),
                        time.time(),
                    ),
                )
        self.conn.execute(
            "UPDATE intake_items SET data=? WHERE id=?", (dump(data), row["id"])
        )

    def update_text(self, batch, text, now=None):
        lower = text.lower().strip()
        rows = self.rows(batch)
        changed = False
        common = parser.date_in(lower, now)
        explicit = list(re.finditer(r"\b(?:no\.?|nomor)\s*(\d+)\b", lower))
        if len({int(m[1]) for m in explicit}) < len(explicit):
            with self.db.atomic():
                prefix = lower[: explicit[0].start()]
                if prefix.strip():
                    changed = self.update_text(batch, prefix, now) or changed
                for index, m in enumerate(explicit):
                    end = (
                        explicit[index + 1].start()
                        if index + 1 < len(explicit)
                        else len(lower)
                    )
                    changed = (
                        self.update_text(batch, lower[m.start() : end], now) or changed
                    )
            return changed
        with self.db.atomic():
            if explicit and re.search(r"\bsemua\b", lower[: explicit[0].start()]):
                common = parser.date_in(lower[: explicit[0].start()], now)
            if common and (
                not explicit or re.search(r"\bsemua\b", lower[: explicit[0].start()])
            ):
                for row in rows:
                    if row["status"] != "DRAFT":
                        continue
                    data = dict(row["data"])
                    data["date"] = common
                    data["occurred_at"] = None
                    data["time_precision"] = "DATE"
                    self._update(row, data)
                    changed = True
            rows = self.rows(batch)
            for row in rows:
                if row["status"] != "DRAFT":
                    if re.search(r"\b(sudah diganti|sudah ganti)\b", lower) and (
                        not explicit
                        or any(int(v[1]) == row["number"] for v in explicit)
                    ):
                        self.conn.execute(
                            "UPDATE intake_replacements SET status='RESOLVED',resolved_at=? WHERE item_id=?",
                            (time.time(), row["id"]),
                        )
                        changed = True
                    continue
                m = next((m for m in explicit if int(m[1]) == row["number"]), None)
                if explicit and not m:
                    continue
                part = lower[m.end() :] if m else lower
                if m:
                    next_m = next((v for v in explicit if v.start() > m.start()), None)
                    if next_m:
                        part = lower[m.end() : next_m.start()]
                part = part.strip()
                data = json.loads(dump(row["data"]))
                d = parser.date_in(part, now)
                funding_answer = bool(
                    (data.get("funding_account_id") or data.get("lines"))
                    and re.search(
                        r"bagian|sudah (?:dipindah|transfer|ditransfer)|alokasi", part
                    )
                )
                if d and not funding_answer:
                    data.update(date=d, occurred_at=None, time_precision="DATE")
                tm = re.search(
                    r"\b(?:jam\s+)?([01]?\d|2[0-3]):([0-5]\d)(?::([0-5]\d))?\b", part
                )
                if tm and data.get("date") and not funding_answer:
                    data.update(
                        occurred_at=f"{data['date']}T{int(tm[1]):02}:{tm[2]}:{tm[3] or '00'}+07:00",
                        time_precision="SECOND" if tm[3] else "MINUTE",
                        time_source="OWNER",
                    )
                if re.search(
                    r"\b(kejadian baru|transaksi baru|beda transaksi)\b", part
                ):
                    data["duplicate_confirmed"] = True
                if re.search(r"\b(sudah diganti|sudah ganti)\b", part):
                    self.conn.execute(
                        "UPDATE intake_replacements SET status='RESOLVED',resolved_at=? WHERE item_id=?",
                        (time.time(), row["id"]),
                    )
                    data["replacement_pending"] = False
                if part.startswith("pecah"):
                    parts = re.split(r"[;\n]|,(?!\d)", part.split(":", 1)[-1])
                    splits = []
                    for val in parts:
                        if not val.strip():
                            continue
                        line = parser.parse_line(
                            self.engine,
                            val,
                            common_date=data.get("date"),
                            batch=True,
                            now=now,
                        )
                        line["funding_account_id"] = (
                            line.get("account_id")
                            if line.get("account_id") != data.get("account_id")
                            else None
                        )
                        line["funding_account_name"] = (
                            line.get("account_name")
                            if line.get("funding_account_id")
                            else None
                        )
                        line.update(
                            account_id=data.get("account_id"),
                            account_name=data.get("account_name"),
                            direction="EXPENSE",
                            date=data.get("date"),
                        )
                        splits.append(line)
                    data["lines"] = splits
                    data["needs_purpose"] = False
                    data["direction_unknown"] = False
                    data["direction"] = "EXPENSE"
                elif part.strip() in ("iya", "ya", "betul", "benar", "simpan"):
                    data["facts_confirmed"] = True
                    data["needs_purpose"] = False
                    data["semantic_review_required"] = False
                elif (
                    data.get("funding_account_id")
                    and funding_answer
                    and not data.get("lines")
                ):
                    if "alokasi" in part:
                        data["funding_mode"] = "ALLOCATION"
                    elif re.search(r"sudah (?:dipindah|transfer|ditransfer)", part):
                        data.update(funding_mode="TRANSFER_CONFIRMED", funding_date=d)
                elif data.get("lines") and re.search(r"\bbagian\s+(\d+)\b", part):
                    index = int(re.search(r"\bbagian\s+(\d+)\b", part)[1]) - 1
                    if index < 0 or index >= len(data["lines"]):
                        raise ValueError("Nomor pecahan tidak ditemukan")
                    line = dict(data["lines"][index])
                    accounts = parser.account_matches(self.engine, part)
                    if accounts:
                        line.update(
                            funding_account_id=accounts[0][2].id,
                            funding_account_name=accounts[0][2].name,
                        )
                    if "alokasi" in part:
                        line["funding_mode"] = "ALLOCATION"
                    elif re.search(r"sudah (?:dipindah|transfer|ditransfer)", part):
                        line.update(
                            funding_mode="TRANSFER_CONFIRMED",
                            funding_date=parser.date_in(part, now),
                        )
                    data["lines"][index] = line
                elif (
                    re.search(r"\b(akun|dari|dr)\b", part)
                    and parser.amount(part) is None
                    and len(parser.account_matches(self.engine, part)) == 1
                ):
                    a = parser.account_matches(self.engine, part)[0][2]
                    data.update(account_id=a.id, account_name=a.name)
                elif m or data.get("needs_purpose"):
                    if parser.amount(part):
                        data["amount"] = parser.amount(part)
                    if re.search(r"\b(terima|masuk)\b", part):
                        data["direction"] = "INCOME"
                        data["direction_unknown"] = False
                    elif re.search(r"\b(bayar|beli|keluar)\b", part):
                        data["direction"] = "EXPENSE"
                        data["direction_unknown"] = False
                    classification = parser.classify(
                        self.engine,
                        part,
                        data.get("direction", "EXPENSE"),
                        data.get("counterparty"),
                    )
                    if classification.get("category_name"):
                        data.update(classification)
                        data["note"] = part.strip()
                        data["needs_purpose"] = False
                        data["facts_confirmed"] = True
                        data["user_labels_verified"] = True
                    if data.get("requires_explanation") and re.search(
                        r"\b(ganti|refund|utang|pokok|cicilan|belanja)\b", part
                    ):
                        data["requires_explanation"] = False
                        data["note"] = part.strip()
                if data != row["data"]:
                    self._update(row, data)
                    changed = True
            self.conn.execute(
                "UPDATE intake_batches SET updated_at=? WHERE id=?",
                (time.time(), batch),
            )
        return changed

    def funding_match(self, item, line, index):
        source = line.get("funding_account_id")
        if not source or source == item.get("account_id"):
            return None
        target = line.get("funding_date") or item.get("date")
        if not target:
            return None
        try:
            start = (
                target
                if line.get("funding_date")
                else (date.fromisoformat(target) - timedelta(days=7)).isoformat()
            )
        except ValueError:
            return None
        candidates = self.conn.execute(
            "SELECT t.id,t.amount FROM transactions t JOIN transactions u ON t.paired_transaction_id=u.id WHERE t.account_id=? AND u.account_id=? AND t.direction='TRANSFER' AND t.transfer_side='OUT' AND t.status IN ('ACTIVE','CORRECTED') AND u.status IN ('ACTIVE','CORRECTED') AND t.date BETWEEN ? AND ? AND t.amount>=?",
            (source, item.get("account_id"), start, target, line.get("amount") or 0),
        ).fetchall()
        if len(candidates) != 1:
            return None
        used = self.conn.execute(
            "SELECT COALESCE(SUM(amount),0) FROM intake_funding WHERE transaction_id=? AND item_id!=?",
            (candidates[0]["id"], item.get("replaces_item", "")),
        ).fetchone()[0]
        return (
            candidates[0]["id"]
            if used + float(line.get("amount") or 0) <= candidates[0]["amount"] + 0.01
            else None
        )

    def issues(self, data, item_id=None):
        reasons = []
        if (
            not isinstance(data.get("amount"), (int, float))
            or not math.isfinite(data["amount"])
            or data["amount"] <= 0
        ):
            reasons.append("nominal")
        acc = (
            self.engine.get_account(data.get("account_id"))
            if data.get("account_id")
            else None
        )
        if not acc or not acc.is_active:
            reasons.append("akun")
        if data.get("possible_duplicate_in_batch") and not data.get(
            "duplicate_confirmed"
        ):
            reasons.append("kemungkinan baris berulang; konfirmasi kejadian berbeda")
        if data.get("multiple_amounts") and not data.get("lines"):
            reasons.append(
                "beberapa nominal satu baris; pisahkan atau pecah pembayaran"
            )
        if data.get("outside_scope"):
            reasons.append(
                "keuangan pribadi orang lain di luar lingkup; perjelas kontribusi rumah tangga"
            )
        if data.get("instruction_hold"):
            reasons.append("menunggu izin pencatatan")
        if data.get("semantic_review_required") and not data.get("facts_confirmed"):
            reasons.append("konfirmasi usulan Hermes")
        if not data.get("date"):
            reasons.append("tanggal")
        if data.get("direction_unknown") or data.get("direction") not in (
            "EXPENSE",
            "INCOME",
            "TRANSFER",
            "CC_PAYMENT",
        ):
            reasons.append("jenis transaksi")
        if data.get("direction") == "TRANSFER" and not data.get(
            "destination_account_id"
        ):
            reasons.append("akun tujuan")
        if data.get("direction") == "CC_PAYMENT" and not data.get("credit_card_id"):
            reasons.append("kartu tujuan")
        if data.get("needs_purpose"):
            reasons.append("tujuan belanja")
        if data.get("requires_explanation"):
            reasons.append("penjelasan penggantian/utang")
        lines = data.get("lines") or [data]
        if data.get("lines") and (
            not all(
                isinstance(x.get("amount"), (int, float)) and x["amount"] > 0
                for x in lines
            )
            or abs(
                sum(x.get("amount") or 0 for x in lines)
                - float(data.get("amount") or 0)
            )
            > 0.01
        ):
            reasons.append("total pecahan tidak sama")
        for index, line in enumerate(lines):
            if (
                data.get("direction") not in ("TRANSFER", "CC_PAYMENT")
                and not line.get("category_id")
                and not line.get("proposed_category")
            ):
                reasons.append("kategori")
            if (
                line.get("funding_account_id")
                and not self.funding_match(data, line, index)
                and line.get("funding_mode") != "ALLOCATION"
                and not (
                    line.get("funding_mode") == "TRANSFER_CONFIRMED"
                    and line.get("funding_date")
                )
            ):
                reasons.append("bukti pendanaan " + str(index + 1))
        funding_totals = {}
        for index, line in enumerate(lines):
            fid = self.funding_match(data, line, index)
            if fid:
                funding_totals[fid] = funding_totals.get(fid, 0) + (
                    line.get("amount") or 0
                )
        for fid, total in funding_totals.items():
            available = (
                self.conn.execute(
                    "SELECT amount FROM transactions WHERE id=?", (fid,)
                ).fetchone()[0]
                - self.conn.execute(
                    "SELECT COALESCE(SUM(amount),0) FROM intake_funding WHERE transaction_id=? AND item_id!=?",
                    (fid, data.get("replaces_item", "")),
                ).fetchone()[0]
            )
            if total > available + 0.01:
                reasons.append("pendanaan sudah dipakai / nominal tidak cukup")
        if (
            data.get("account_id")
            and data.get("date")
            and data.get("amount")
            and not data.get("duplicate_confirmed")
        ):
            existing = self.conn.execute(
                "SELECT t.id FROM transactions t WHERE account_id=? AND date=? AND amount=? AND direction=? AND status IN ('ACTIVE','CORRECTED')",
                (
                    data["account_id"],
                    data["date"],
                    data["amount"],
                    data.get("direction"),
                ),
            ).fetchall()
            own = set(data.get("replaces", [])) | {
                r[0]
                for r in self.conn.execute(
                    "SELECT transaction_id FROM intake_transactions WHERE item_id=?",
                    (item_id or "",),
                )
            }
            # Distinct numbered rows from this same message are separate declared events.
            # Exact repeated rows were flagged before any posting, above.
            if item_id:
                own.update(
                    r[0]
                    for r in self.conn.execute(
                        "SELECT t.transaction_id FROM intake_transactions t JOIN intake_items i ON i.id=t.item_id WHERE i.batch_id=(SELECT batch_id FROM intake_items WHERE id=?)",
                        (item_id,),
                    )
                )
            if any(r["id"] not in own for r in existing):
                reasons.append("kemungkinan sudah tercatat")
        return sorted(set(reasons))

    def classify_create(self, line, direction):
        name = line.get("category_name") or line.get("proposed_category")
        cat = None
        sub = None
        if name:
            cat = next(
                (
                    c
                    for c in self.engine.list_categories(active_only=True)
                    if c.name.casefold() == name.casefold()
                ),
                None,
            )
            if not cat:
                cat = self.engine.create_category(name, event_type=direction)
        if cat and line.get("subcategory_name"):
            name = line["subcategory_name"]
            sub = next(
                (
                    s
                    for s in self.engine.list_subcategories(cat.id, active_only=True)
                    if s.name.casefold() == name.casefold()
                ),
                None,
            )
            if not sub:
                sub = self.engine.create_subcategory(cat.id, name)
        return cat.id if cat else None, sub.id if sub else None

    def preview(self, batch, page=0):
        all_rows = self.rows(batch)
        visible = all_rows[page * 20 : (page + 1) * 20]
        proposals = {}
        out = ["🧾 Rekapan transaksi — " + batch[:6]]
        questions = {}
        ready = 0
        for row in visible:
            d = row["data"]
            issues = self.issues(d, row["id"]) if row["status"] == "DRAFT" else []
            if row["status"] == "POSTED":
                label = "✅ tercatat"
            elif row["status"] == "LINKED":
                label = "🔗 sudah tercatat"
            elif row["status"] == "IGNORED":
                label = "diabaikan"
            elif row["status"] in ("VOID", "REPLACED"):
                label = "dibatalkan" if row["status"] == "VOID" else "sudah dikoreksi"
            else:
                label = "⚠️ perlu detail" if issues else "siap"
                ready += not issues
                for issue in issues:
                    questions.setdefault(issue, []).append(row["number"])
            amount = (
                format_idr(d["amount"])
                if isinstance(d.get("amount"), (int, float))
                else "?"
            )
            stamp = (
                (
                    ("~" if d.get("time_precision") == "ESTIMATED" else "")
                    + (d.get("occurred_at") or "")[11:19]
                )
                if d.get("occurred_at")
                else "jam tidak diketahui"
            )
            cat = d.get("subcategory_name") or d.get("category_name") or "?"
            out.append(
                f"{row['number']}. {d.get('date') or '? tanggal'} {stamp} · {amount} · {d.get('account_name') or '? akun'} · {d.get('direction')} · {str(cat)[:25]} · {str(d.get('purpose') or d.get('note') or '')[:40]} — {label}"
            )
            if d.get("proposed_category") or d.get("proposed_subcategory"):
                proposals.setdefault(
                    str(d.get("category_name"))
                    + " / "
                    + str(d.get("subcategory_name")),
                    [],
                ).append(row["number"])
            if d.get("lines"):
                for line in d["lines"]:
                    out.append(
                        "   ↳ "
                        + format_idr(line.get("amount") or 0)
                        + " "
                        + str(line.get("subcategory_name") or line.get("note", ""))[:50]
                        + "; sumber "
                        + str(line.get("funding_account_name") or d.get("account_name"))
                    )
        for name, numbers in proposals.items():
            out.append(
                "Usul klasifikasi no. " + ", ".join(map(str, numbers)) + ": " + name
            )
        if questions:
            out.append("\nLengkapi sekaligus:")
            for issue, numbers in questions.items():
                out.append("• No. " + ", ".join(map(str, numbers)) + ": " + issue)
            out.append(
                "Contoh: semua tanggal 3 Oktober; no. 4 dari Saving; no. 8 ini transaksi baru."
            )
        out.append(
            f"\n{ready} siap. Simpan yang siap juga menyetujui usulan klasifikasi yang ditampilkan."
        )
        out.append(
            f"Halaman {page+1}/{max(1,(len(all_rows)+19)//20)}; total {len(all_rows)} transaksi."
        )
        return "\n".join(out)

    def commit(
        self, batch, owner, exclude=(), message_id=None, confirm_suggestions=False
    ):
        if not self.owned(batch, owner):
            raise PermissionError("Batch bukan milik akun ini")
        new = []
        events = 0
        totals = {"INCOME": 0, "EXPENSE": 0}
        accounts = set()
        with self.db.atomic():
            for row in self.rows(batch):
                d = row["data"]
                if row["status"] != "DRAFT" or row["number"] in exclude:
                    continue
                # Web approval and chat drafts share the same source guard under this write lock.
                if d.get("review_id"):
                    source = self.engine.get_review_queue_item(d["review_id"])
                    if not source or source.status != "PENDING":
                        if (
                            source
                            and source.status == "APPROVED"
                            and source.approved_transaction_id
                        ):
                            self.conn.execute(
                                "INSERT OR IGNORE INTO intake_transactions VALUES (?,?,?)",
                                (row["id"], source.approved_transaction_id, "EXISTING"),
                            )
                            self.conn.execute(
                                "UPDATE intake_items SET status='LINKED' WHERE id=?",
                                (row["id"],),
                            )
                        else:
                            self.conn.execute(
                                "UPDATE intake_items SET status='IGNORED' WHERE id=?",
                                (row["id"],),
                            )
                        continue
                if confirm_suggestions:
                    d = dict(d, facts_confirmed=True, semantic_review_required=False)
                if self.issues(d, row["id"]):
                    continue
                for previous in d.get("replaces", []):
                    previous_tx = self.engine.get_transaction(previous)
                    if previous_tx and previous_tx.credit_card_id:
                        raise ValueError(
                            "Koreksi kartu memakai editor kartu agar kewajiban tetap sesuai"
                        )
                    self.engine.void_transaction(
                        previous,
                        reason="Owner correction through persistent draft",
                        scope="event",
                    )
                if d.get("replaces_item"):
                    self.conn.execute(
                        "UPDATE intake_items SET status='REPLACED' WHERE id=?",
                        (d["replaces_item"],),
                    )
                    self.conn.execute(
                        "DELETE FROM intake_funding WHERE item_id=?",
                        (d["replaces_item"],),
                    )
                    self.conn.execute(
                        "UPDATE intake_replacements SET status='CANCELLED' WHERE item_id=? AND status='PENDING'",
                        (d["replaces_item"],),
                    )
                if d["direction"] == "TRANSFER":
                    txs = list(
                        self.engine.transfer_funds(
                            d["account_id"],
                            d["destination_account_id"],
                            d["amount"],
                            note=d.get("note"),
                            source="TELEGRAM_BATCH",
                            tx_date=d["date"],
                        )
                    )
                elif d["direction"] == "CC_PAYMENT":
                    pay = self.engine.record_credit_card_payment(
                        card_id=d["credit_card_id"],
                        payment_date=d["date"],
                        amount=d["amount"],
                        account_id=d["account_id"],
                        notes=d.get("note"),
                    )
                    txs = [self.engine.get_transaction(pay.transaction_id)]
                else:
                    txs = []
                    for index, line in enumerate(d.get("lines") or [d]):
                        cat, sub = self.classify_create(line, d["direction"])
                        line.update(
                            category_id=cat,
                            subcategory_id=sub,
                            proposed_category=None,
                            proposed_subcategory=None,
                        )
                        tx = self.engine.create_transaction(
                            d["account_id"],
                            line["amount"],
                            d["direction"],
                            category_id=cat,
                            subcategory_id=sub,
                            note=line.get("note"),
                            source="TELEGRAM_BATCH",
                            tx_date=d["date"],
                        )
                        txs.append(tx)
                        funding = self.funding_match(d, line, index)
                        if (
                            not funding
                            and line.get("funding_mode") == "TRANSFER_CONFIRMED"
                        ):
                            outgoing, incoming = self.engine.transfer_funds(
                                line["funding_account_id"],
                                d["account_id"],
                                line["amount"],
                                note="Pendanaan pembayaran terkonfirmasi Owner",
                                source="TELEGRAM_BATCH",
                                tx_date=line["funding_date"],
                            )
                            funding = outgoing.id
                            for fundtx in (outgoing, incoming):
                                self.conn.execute(
                                    "INSERT INTO intake_transactions VALUES (?,?,?)",
                                    (row["id"], fundtx.id, "CREATED_FUNDING"),
                                )
                        if funding:
                            self.conn.execute(
                                "INSERT OR IGNORE INTO intake_transactions VALUES (?,?,?)",
                                (row["id"], funding, "FUNDING"),
                            )
                            self.conn.execute(
                                "INSERT INTO intake_funding VALUES (?,?,?,?)",
                                (row["id"], index, funding, line["amount"]),
                            )
                        self.conn.execute(
                            "UPDATE transactions SET occurred_at=?,time_precision=?,time_source=?,message_at=? WHERE id=?",
                            (
                                d.get("occurred_at"),
                                d.get("time_precision", "DATE"),
                                d.get("time_source"),
                                d.get("message_at"),
                                tx.id,
                            ),
                        )
                        totals[d["direction"]] += line["amount"]
                for tx in txs:
                    self.conn.execute(
                        "UPDATE transactions SET occurred_at=?,time_precision=?,time_source=?,message_at=? WHERE id=?",
                        (
                            d.get("occurred_at"),
                            d.get("time_precision", "DATE"),
                            d.get("time_source"),
                            d.get("message_at"),
                            tx.id,
                        ),
                    )
                    self.conn.execute(
                        "INSERT INTO intake_transactions VALUES (?,?,?)",
                        (row["id"], tx.id, "POSTING"),
                    )
                    new.append(tx.id)
                    accounts.add(tx.account_id)
                events += 1
                for line in d.get("lines") or []:
                    if line.get("funding_account_id"):
                        accounts.add(line["funding_account_id"])
                self.conn.execute(
                    "UPDATE intake_items SET status='POSTED',data=? WHERE id=?",
                    (dump(d), row["id"]),
                )
                if d.get("review_id"):
                    self.conn.execute(
                        "UPDATE review_queue SET status='APPROVED',approved_transaction_id=?,updated_at=datetime('now') WHERE id=? AND status='PENDING'",
                        (txs[0].id, d["review_id"]),
                    )
                if d.get("replacement_pending"):
                    self.conn.execute(
                        "INSERT OR IGNORE INTO intake_replacements VALUES (?,?,?,?,?,?)",
                        (
                            uid(),
                            row["id"],
                            d["amount"],
                            d.get("purpose") or d.get("note"),
                            "PENDING",
                            None,
                        ),
                    )
                from .intake_learning import observe

                observe(self, row, d)
            remaining = sum(r["status"] == "DRAFT" for r in self.rows(batch))
            self.conn.execute(
                "UPDATE intake_batches SET status=?,updated_at=? WHERE id=?",
                ("PARTIAL" if remaining else "COMPLETED", time.time(), batch),
            )
            lines = [
                f"✅ Batch {batch[:6]}: {events} transaksi tersimpan ({len(new)} catatan buku besar);  {remaining} transaksi masih draft.",
                f"Masuk {format_idr(totals['INCOME'])} · Keluar {format_idr(totals['EXPENSE'])}",
            ]
            for aid in sorted(accounts):
                a = self.engine.get_account(aid)
                lines.append(
                    f"{a.name}: saldo buku besar setelah transaksi {format_idr(a.balance)}"
                )
            for row in self.rows(batch):
                d = row["data"]
                if d.get("credit_card_id") and row["status"] == "POSTED":
                    card = self.engine.get_credit_card(d["credit_card_id"])
                    if card:
                        lines.append(
                            card.name
                            + ": sisa kewajiban "
                            + format_idr(card.current_balance)
                        )
            lines.append("Ref: " + ", ".join(new))
            receipt = html.escape("\n".join(lines))
            if new:
                ref = (
                    batch
                    + ":"
                    + hashlib.sha256("|".join(new).encode()).hexdigest()[:12]
                )
                payload = {
                    "chat_id": str(owner),
                    "text": receipt,
                    "parse_mode": "HTML",
                    "reply_markup": {
                        "inline_keyboard": [
                            [
                                {
                                    "text": "✏️ Lihat / lanjut",
                                    "callback_data": "bi:edit:" + batch,
                                },
                                {
                                    "text": "↩️ Batal pencatatan",
                                    "callback_data": "bi:undo:" + batch,
                                },
                            ]
                        ]
                    },
                }
                if message_id:
                    payload.update(message_id=int(message_id))
                enqueue(
                    self.db,
                    "batch_receipt",
                    ref,
                    owner,
                    "editMessageText" if message_id else "sendMessage",
                    payload,
                )
        return {"new_transactions": new, "remaining": remaining, "receipt": receipt}

    def link_existing(self, batch, owner, txid):
        if not self.owned(batch, owner):
            raise PermissionError("Batch bukan milik akun ini")
        rows = [r for r in self.rows(batch) if r["status"] == "DRAFT"]
        tx = self.engine.get_transaction(txid)
        if len(rows) != 1 or not tx or tx.status not in ("ACTIVE", "CORRECTED"):
            raise ValueError("Balas dengan referensi transaksi yang sudah tercatat")
        row = rows[0]
        d = row["data"]
        if (
            tx.account_id != d.get("account_id")
            or tx.amount != d.get("amount")
            or tx.direction != d.get("direction")
            or (d.get("date") and tx.date != d["date"])
        ):
            raise ValueError(
                "Referensi berbeda akun, nominal, tanggal, atau jenis; periksa kembali"
            )
        with self.db.atomic():
            self.conn.execute(
                "INSERT OR IGNORE INTO intake_transactions VALUES (?,?,?)",
                (row["id"], txid, "EXISTING"),
            )
            self.conn.execute(
                "UPDATE intake_items SET status='LINKED' WHERE id=?", (row["id"],)
            )
            if d.get("review_id"):
                self.conn.execute(
                    "UPDATE review_queue SET status='IGNORED',issue_reason='Sudah tercatat; terkait referensi ledger' WHERE id=?",
                    (d["review_id"],),
                )

    def ignore(self, batch, owner, reason):
        if not self.owned(batch, owner):
            raise PermissionError("Batch bukan milik akun ini")
        with self.db.atomic():
            for row in self.rows(batch):
                if row["status"] != "DRAFT":
                    continue
                self.conn.execute(
                    "UPDATE intake_items SET status='IGNORED' WHERE id=?", (row["id"],)
                )
                if row["data"].get("review_id"):
                    self.engine.ignore_review_item(
                        row["data"]["review_id"], reason=reason
                    )

    def revise(self, batch, owner, number, text, source_key):
        if not self.owned(batch, owner):
            raise PermissionError("Batch bukan milik akun ini")
        row = next(
            (
                r
                for r in self.rows(batch)
                if r["number"] == number and r["status"] == "POSTED"
            ),
            None,
        )
        if not row:
            raise ValueError("Nomor transaksi belum tercatat atau tidak ditemukan")
        txids = [
            r[0]
            for r in self.conn.execute(
                "SELECT transaction_id FROM intake_transactions WHERE item_id=? AND role IN ('POSTING','CREATED_FUNDING')",
                (row["id"],),
            )
        ]
        if any(self.engine.get_transaction(t).credit_card_id for t in txids):
            raise ValueError(
                "Koreksi kartu memakai editor kartu agar kewajiban tetap sesuai"
            )
        data = json.loads(dump(row["data"]))
        data.update(replaces=txids, replaces_item=row["id"], duplicate_confirmed=True)
        data.pop("review_id", None)
        revision = self.create(
            owner,
            "revision:" + str(owner) + ":" + source_key,
            "revision:" + str(owner) + ":" + source_key,
            items=[data],
        )
        text = re.sub(
            r"\b(?:no\.?|nomor)\s*" + str(number) + r"\b", "no. 1", text, flags=re.I
        )
        self.update_text(revision, text)
        return revision
