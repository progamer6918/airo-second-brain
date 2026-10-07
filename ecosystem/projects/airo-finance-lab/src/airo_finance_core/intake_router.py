"""Owner-scoped persistent finance conversation, before legacy one-line capture."""

import json, re, time
from datetime import datetime
from .intake_parser import amount, ZONE
from .intake_service import IntakeService
from .gmail_reliability import enqueue, dispatch
from .intake_store import uid


class IntakeRouter:
    def __init__(self, parent):
        self.parent = parent
        self.s = IntakeService(parent.engine)

    def send_preview(self, batch, owner, message_id=None, page=0):
        payload = {
            "chat_id": str(owner),
            "text": self.s.preview(batch, page),
            "reply_markup": {
                "inline_keyboard": [
                    [
                        {
                            "text": "✅ Simpan yang siap",
                            "callback_data": "bi:save:" + batch,
                        },
                        {
                            "text": "🕒 Lanjut nanti",
                            "callback_data": "bi:later:" + batch,
                        },
                    ],
                    [{"text": "✏️ Koreksi", "callback_data": "bi:edit:" + batch}],
                ]
            },
        }
        pages = max(1, (len(self.s.rows(batch)) + 19) // 20)
        if pages > 1:
            payload["reply_markup"]["inline_keyboard"].append(
                [
                    {"text": "◀️", "callback_data": f"bi:page:{batch}:{max(0,page-1)}"},
                    {
                        "text": "▶️",
                        "callback_data": f"bi:page:{batch}:{min(pages-1,page+1)}",
                    },
                ]
            )
        if message_id:
            payload["message_id"] = int(message_id)
        ref = batch + ":" + str(time.time_ns())
        with self.s.db.atomic():
            enqueue(
                self.s.db,
                "batch_preview",
                ref,
                owner,
                "editMessageText" if message_id else "sendMessage",
                payload,
            )
            questions = {
                issue
                for r in self.s.rows(batch)
                if r["status"] == "DRAFT"
                for issue in self.s.issues(r["data"], r["id"])
            }
            if questions:
                self.s.conn.execute(
                    "INSERT INTO intake_interactions VALUES (?,?,?,?,?)",
                    (uid(), batch, "QUESTION", len(questions), time.time()),
                )
        dispatch(self.s.db, self.parent.outbound)
        for r in self.s.conn.execute(
            "SELECT message_id,payload FROM finance_outbox WHERE kind='batch_preview' AND ref=? AND status='SENT'",
            (ref,),
        ):
            sent = r["message_id"] or message_id
            if sent:
                with self.s.db.atomic():
                    self.s.conn.execute(
                        "INSERT OR REPLACE INTO intake_prompts VALUES (?,?,?)",
                        (str(owner), str(sent), batch),
                    )

    def handle(self, update):
        cq = update.get("callback_query")
        msg = update.get("message") or (cq or {}).get("message") or {}
        sender = str((cq or msg).get("from", {}).get("id", ""))
        owner = str(msg.get("chat", {}).get("id", sender))
        data = (cq or {}).get("data", "")
        text = (msg.get("text") or "").strip()
        lower = text.lower()
        if not cq and self.parent.confirmation_handler.get_edit_session(owner):
            return None
        if cq:
            if data.startswith("gma:") and self.parent.is_owner(sender):
                item = self.s.engine.get_review_queue_item(data.split(":", 1)[1])
                if (
                    item
                    and item.status == "PENDING"
                    and json.loads(item.parsed_result).get("direction")
                    not in ("TRANSFER", "CC_PAYMENT")
                    and (
                        not json.loads(item.parsed_result).get("category_id")
                        or (
                            json.loads(item.parsed_result).get("merchant") or ""
                        ).lower()
                        in (
                            "transaksimu pakai blu berhasil",
                            "internet transaction journal",
                            "info transaksi masuk ke blu kamu",
                        )
                    )
                ):
                    batch = self.s.from_review(owner, item.id)
                    self.send_preview(batch, owner, msg.get("message_id"))
                    return True, "BATCH_EMAIL_NEEDS_PURPOSE"
            if not data.startswith(("bi:", "gin:", "gsp:", "gln:")):
                return None
            if not self.parent.is_owner(sender):
                return True, "BLOCKED_NON_OWNER_CALLBACK"
            if data.startswith(("gin:", "gsp:", "gln:")):
                action, rid = data.split(":", 1)
                batch = self.s.from_review(owner, rid)
                if action == "gin":
                    self.s.ignore(batch, owner, "Bukan transaksi; keputusan Owner")
                self.send_preview(batch, owner, msg.get("message_id"))
                return True, "BATCH_EMAIL_ACTION"
            pieces = data.split(":")
            action, batch = pieces[1:3]
            if not self.s.owned(batch, owner):
                return True, "BLOCKED_BATCH_OWNER"
            with self.s.db.atomic():
                self.s.conn.execute(
                    "INSERT INTO intake_interactions VALUES (?,?,?,?,?)",
                    (uid(), batch, "CALLBACK", 1, time.time()),
                )
            if action == "page":
                self.send_preview(batch, owner, msg.get("message_id"), int(pieces[3]))
            elif action == "save":
                result = self.s.commit(
                    batch,
                    owner,
                    message_id=msg.get("message_id"),
                    confirm_suggestions=True,
                )
                dispatch(self.s.db, self.parent.outbound)
                if not result["new_transactions"]:
                    self.send_preview(batch, owner, msg.get("message_id"))
            elif action == "undo":
                with self.s.db.atomic():
                    for row in self.s.rows(batch):
                        if row["status"] != "POSTED":
                            continue
                        for t in self.s.conn.execute(
                            "SELECT transaction_id FROM intake_transactions WHERE item_id=? AND role IN ('POSTING','CREATED_FUNDING')",
                            (row["id"],),
                        ).fetchall():
                            if self.s.engine.get_transaction(t[0]).credit_card_id:
                                raise ValueError(
                                    "Pembatalan kartu perlu editor kartu agar kewajiban tetap sesuai"
                                )
                            self.s.engine.void_transaction(
                                t[0], reason="Owner undo batch", scope="event"
                            )
                        self.s.conn.execute(
                            "DELETE FROM intake_funding WHERE item_id=?", (row["id"],)
                        )
                        self.s.conn.execute(
                            "UPDATE intake_replacements SET status='CANCELLED' WHERE item_id=? AND status='PENDING'",
                            (row["id"],),
                        )
                        self.s.conn.execute(
                            "UPDATE intake_items SET status='VOID' WHERE id=?",
                            (row["id"],),
                        )
                self.send_preview(batch, owner, msg.get("message_id"))
            elif action == "later":
                with self.s.db.atomic():
                    self.s.conn.execute(
                        "DELETE FROM intake_context WHERE owner=? AND batch_id=?",
                        (owner, batch),
                    )
            else:
                with self.s.db.atomic():
                    self.s.conn.execute(
                        "INSERT INTO intake_context VALUES (?,?,?) ON CONFLICT(owner) DO UPDATE SET batch_id=excluded.batch_id,mode=excluded.mode",
                        (owner, batch, "DETAIL"),
                    )
                self.send_preview(batch, owner, msg.get("message_id"))
            if self.parent.outbound:
                self.parent.outbound.answer_callback_query(
                    cq["id"],
                    text=(
                        "Draft tersimpan; proses selesai"
                        if action == "later"
                        else "Rekapan diperbarui"
                    ),
                )
            return True, "BATCH_" + action.upper()
        if lower.startswith("aktifkan pola "):
            if not self.parent.is_owner(sender):
                return True, "BLOCKED_NON_OWNER_WRITE"
            from .intake_learning import activate

            try:
                activate(self.s, text.split()[-1])
                message = "Pola email diaktifkan; detail yang belum lengkap tetap perlu konfirmasi."
            except ValueError as exc:
                message = str(exc)
            if self.parent.outbound:
                self.parent.outbound.send_message(owner, message)
            return True, "INTAKE_RULE_ACTIVATION"
        if lower in ("pola finance", "status belajar finance"):
            if not self.parent.is_owner(sender):
                return True, "BLOCKED_NON_OWNER_READ"
            from .intake_learning import metrics

            report = json.dumps(metrics(self.s), ensure_ascii=False)
            for r in self.s.conn.execute(
                "SELECT id,confirmations,conflicts,enabled FROM intake_rules ORDER BY last_at DESC LIMIT 10"
            ):
                report += (
                    "\nPola "
                    + r["id"]
                    + ": "
                    + str(r["confirmations"])
                    + " konfirmasi; "
                    + str(r["conflicts"])
                    + " konflik; aktif="
                    + str(bool(r["enabled"]))
                )
            if self.parent.outbound:
                self.parent.outbound.send_message(owner, report)
            return True, "INTAKE_RULE_STATUS"
        if not text or lower.startswith(
            ("/reset", "/about", "/help", "/saldo", "saldo", "berapa", "cek saldo")
        ):
            return None
        reply_id = msg.get("reply_to_message", {}).get("message_id")
        batch = None
        if reply_id:
            r = self.s.conn.execute(
                "SELECT batch_id FROM intake_prompts WHERE owner=? AND message_id=?",
                (owner, str(reply_id)),
            ).fetchone()
            if r:
                batch = r[0]
            else:
                r = self.s.conn.execute(
                    "SELECT ref FROM finance_outbox WHERE recipient=? AND message_id=? AND kind IN ('candidate','recovery_candidate') AND status='SENT'",
                    (owner, str(reply_id)),
                ).fetchone()
                if r:
                    try:
                        batch = self.s.from_review(owner, r[0])
                    except ValueError:
                        pass
        if not batch:
            r = self.s.conn.execute(
                "SELECT batch_id FROM intake_context WHERE owner=?", (owner,)
            ).fetchone()
            if r and (
                re.search(
                    r"\b(no\.?|nomor|semua|tanggal|pecah|sudah tercatat|bukan transaksi|simpan|sudah ganti|lanjut batch|iya|betul)\b",
                    lower,
                )
                or (
                    len(self.s.rows(r[0])) == 1
                    and amount(text) is None
                    and len(text) < 150
                )
            ):
                batch = r[0]
        is_finance = amount(text) is not None and (
            self.parent.is_finance_message(text) or len(text.splitlines()) > 1
        )
        if not batch and not is_finance:
            return None
        if not self.parent.is_owner(sender):
            if self.parent.outbound:
                self.parent.outbound.send_message(
                    sender,
                    "⛔ Akses Ditolak: hanya Owner yang dapat mencatat transaksi.",
                )
            return True, "BLOCKED_NON_OWNER_WRITE"
        try:
            if batch:
                if not self.s.owned(batch, owner):
                    return True, "BLOCKED_BATCH_OWNER"
                with self.s.db.atomic():
                    self.s.conn.execute(
                        "INSERT INTO intake_interactions VALUES (?,?,?,?,?)",
                        (uid(), batch, "ANSWER", 1, time.time()),
                    )
                if lower.startswith("sudah tercatat"):
                    ids = re.findall(r"\btx_[a-zA-Z0-9]+\b", text)
                    if not ids:
                        rows = [r for r in self.s.rows(batch) if r["status"] == "DRAFT"]
                        matches = []
                        if len(rows) == 1:
                            d = rows[0]["data"]
                            matches = self.s.conn.execute(
                                "SELECT id FROM transactions WHERE account_id=? AND amount=? AND date=? AND direction=? AND status IN ('ACTIVE','CORRECTED')",
                                (
                                    d.get("account_id"),
                                    d.get("amount"),
                                    d.get("date"),
                                    d.get("direction"),
                                ),
                            ).fetchall()
                        if len(matches) == 1:
                            ids = [matches[0]["id"]]
                    if len(ids) != 1:
                        raise ValueError(
                            "Sebut referensi transaksi yang sudah tercatat; tidak ada kecocokan tunggal"
                        )
                    self.s.link_existing(batch, owner, ids[0])
                elif lower == "bukan transaksi":
                    self.s.ignore(batch, owner, "Bukan transaksi; keputusan Owner")
                elif lower.startswith(
                    ("simpan yang siap", "simpan semua", "simpan batch")
                ):
                    exclude = (
                        tuple(
                            map(int, re.findall(r"\b\d+\b", lower.split("kecuali")[-1]))
                        )
                        if "kecuali" in lower
                        else ()
                    )
                    self.s.commit(
                        batch, owner, exclude=exclude, confirm_suggestions=True
                    )
                    dispatch(self.s.db, self.parent.outbound)
                    return True, "BATCH_COMMITTED"
                else:
                    number = re.search(r"\b(?:no\.?|nomor)\s*(\d+)\b", lower)
                    posted = number and any(
                        r["number"] == int(number[1]) and r["status"] == "POSTED"
                        for r in self.s.rows(batch)
                    )
                    if posted and not re.search(r"sudah (?:ganti|diganti)", lower):
                        batch = self.s.revise(
                            batch,
                            owner,
                            int(number[1]),
                            text,
                            str(msg.get("message_id")),
                        )
                    changed = self.s.update_text(
                        batch,
                        text,
                        (
                            datetime.fromtimestamp(msg["date"], ZONE)
                            if msg.get("date")
                            else None
                        ),
                    )
                    if not changed and amount(text) is None:
                        from .intake_semantic import enrich

                        enrich(self.s, batch, text)
            else:
                now = (
                    datetime.fromtimestamp(msg["date"], ZONE)
                    if msg.get("date")
                    else None
                )
                batch = self.s.create(
                    owner,
                    "telegram:"
                    + owner
                    + ":"
                    + str(msg.get("message_id") or update.get("update_id")),
                    text,
                    now,
                )
                rows = self.s.rows(batch)
                if any(
                    "kategori" in self.s.issues(r["data"], r["id"])
                    or r["data"].get("direction_unknown")
                    for r in rows
                ):
                    from .intake_semantic import enrich

                    enrich(self.s, batch, text)
                rows = self.s.rows(batch)
                if (
                    len(rows) == 1
                    and not self.s.issues(rows[0]["data"], rows[0]["id"])
                    and not rows[0]["data"].get("proposed_category")
                    and not rows[0]["data"].get("proposed_subcategory")
                ):
                    self.s.commit(batch, owner)
                    dispatch(self.s.db, self.parent.outbound)
                    return True, "BATCH_SINGLE_RECORDED"
            self.send_preview(batch, owner)
            return True, "BATCH_DRAFT_UPDATED"
        except (ValueError, KeyError, TypeError) as exc:
            if self.parent.outbound:
                self.parent.outbound.send_message(
                    owner, "Draft tetap tersimpan. " + str(exc)[:180]
                )
            return True, "BATCH_NEEDS_DETAIL"
