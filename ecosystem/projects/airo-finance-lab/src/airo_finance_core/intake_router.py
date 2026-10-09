"""Owner-scoped persistent finance conversation, before legacy one-line capture."""

import json, re, time
from datetime import datetime
from .intake_parser import amount, time_in, ZONE
from .telegram_capture import format_idr
from .intake_service import IntakeService
from .gmail_reliability import enqueue, dispatch
from .intake_store import uid


class IntakeRouter:
    def __init__(self, parent):
        self.parent = parent
        self.s = IntakeService(parent.engine)

    def send_preview(
        self, batch, owner, message_id=None, page=0, editing=False, notice=None
    ):
        rows = [r for r in self.s.rows(batch) if r["status"] != "IGNORED"]
        if not rows:
            self.send_closed(owner, message_id, "✅ Bukan transaksi. Kartu ditutup dan tidak masuk buku besar.")
            return
        if all(r["status"] in ("VOID", "REPLACED") for r in rows):
            with self.s.db.atomic():
                self.s.conn.execute("DELETE FROM intake_context WHERE owner=? AND batch_id=?", (str(owner), batch))
            self.send_closed(owner, message_id, "↩️ Pencatatan sudah dibatalkan. Saldo buku besar sudah dipulihkan. Tidak ada transaksi yang menunggu disimpan dari kartu ini.")
            return
        has_draft = any(r["status"] == "DRAFT" for r in rows)
        if not has_draft and not editing:
            self.send_closed(owner, message_id, "✅ Pencatatan selesai.\n\n" + self.s.preview(batch, page) + "\n\nTidak perlu membalas atau menekan tombol lagi.")
            return
        ready = sum(
            r["status"] == "DRAFT" and not self.s.approval_issues(r["data"], r["id"])
            for r in rows
        )
        preview = self.s.preview(batch, page)
        if editing:
            preview = (
                f"✏️ Ubah transaksi — {batch[:6]}\n\n"
                "Balas pesan ini dengan perubahan yang lo mau. Bisa beberapa perubahan sekaligus.\n\n"
                "Contoh:\n• Semua jam jadi 17.30\n• No. 3 nominalnya 25rb\n• No. 4 dari Blu Saving\n• No. 5 tanggal 8 Oktober\n\n"
                "Hermes akan menyebut perubahan yang berhasil diterapkan dan menampilkan rekapan baru untuk dicek. "
                "Belum ada perubahan disimpan."
            )
            if len(rows)==1:
                preview = f"✏️ Ubah transaksi — {batch[:6]}\n\nBalas perubahan dengan bahasa biasa, misalnya: itu untuk makan malam; nominalnya 25rb; atau dari Blu Saving.\n\n" + self.s.preview(batch, page)
        elif notice:
            preview = notice + "\n\n" + preview
        payload = {
            "chat_id": str(owner),
            "text": preview,
            "reply_markup": {
                "inline_keyboard": [
                    [
                        {
                            "text": (
                                f"✅ Simpan {ready} transaksi"
                                if ready
                                else "✅ Simpan yang siap"
                            ),
                            "callback_data": "bi:save:" + batch,
                        },
                        {
                            "text": "🕒 Lanjut nanti",
                            "callback_data": "bi:later:" + batch,
                        },
                    ],
                    [
                        {
                            "text": "✏️ Ubah transaksi",
                            "callback_data": "bi:edit:" + batch,
                        }
                    ],
                ]
            },
        }
        save, pause = payload["reply_markup"]["inline_keyboard"][0]
        edit = payload["reply_markup"]["inline_keyboard"][1]
        payload["reply_markup"]["inline_keyboard"] = ([[save]] if ready else []) + [edit, [pause]]
        if editing:
            payload["reply_markup"]["inline_keyboard"] = [
                [
                    {
                        "text": "↩️ Kembali ke rekapan",
                        "callback_data": f"bi:page:{batch}:0",
                    }
                ],
                [{"text": "🕒 Lanjut nanti", "callback_data": "bi:later:" + batch}],
            ]
        if editing and not has_draft:
            payload["reply_markup"]["inline_keyboard"] = payload["reply_markup"]["inline_keyboard"][:1]
            preview = f"✏️ Koreksi catatan — {batch[:6]}\n\nTransaksi sudah tercatat. Untuk mengoreksi, balas dengan nomor dan perubahan, contoh: no. 1 nominalnya 25rb. Koreksi akan ditampilkan untuk disetujui sebelum disimpan.\n\n" + self.s.preview(batch, page)
            payload["text"] = preview
        if editing and ready and len(rows)==1:
            payload["reply_markup"]["inline_keyboard"].insert(0,[{"text":f"✅ Simpan {ready} transaksi","callback_data":"bi:save:"+batch}])
        size = self.s.page_size(batch)
        pages = max(1, (len(rows) + size - 1) // size)
        if pages > 1 and not editing:
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

    def send_closed(self, owner, message_id, text):
        payload = {"chat_id": str(owner), "text": text, "reply_markup": {"inline_keyboard": []}}
        if message_id:
            payload["message_id"] = int(message_id)
        with self.s.db.atomic():
            enqueue(self.s.db, "card_closed", uid(), owner,
                    "editMessageText" if message_id else "sendMessage", payload)
        dispatch(self.s.db, self.parent.outbound)

    def change_notice(self, before_rows, after_rows):
        before = {r["id"]: r["data"] for r in before_rows}
        changes = {}
        changed_numbers = []
        labels = {
            "occurred_at": "jam",
            "date": "tanggal",
            "amount": "nominal",
            "account_name": "akun",
            "category_name": "kategori",
            "subcategory_name": "subkategori",
            "note": "catatan",
        }
        for row in after_rows:
            old = before.get(row["id"])
            if old is None:
                return "✅ Draft koreksi dibuat. Periksa rekapan; perubahan belum disimpan."
            if old != row["data"]:
                changed_numbers.append(row["number"])
            for field, label in labels.items():
                previous, current = old.get(field), row["data"].get(field)
                if previous == current:
                    continue

                def display(value):
                    if value is None:
                        return "belum diisi"
                    if field == "occurred_at":
                        end = 19 if str(value)[17:19] != "00" else 16
                        return str(value)[11:end].replace(":", ".") + " WIB"
                    if field == "amount":
                        return format_idr(value)
                    return str(value)[:60]

                key = label, display(previous), display(current)
                changes.setdefault(key, []).append(row["number"])
        if not changes and changed_numbers:
            return (
                "✅ Detail draft no. "
                + ", ".join(map(str, changed_numbers))
                + " diperbarui. Periksa rekapan; belum disimpan."
            )
        if not changes:
            return "ℹ️ Belum ada perubahan. Kalau hasilnya belum sesuai, sebut nomor dan detail yang diubah; contoh: no. 3 nominalnya 25rb."
        lines = ["✅ Perubahan diterapkan ke draft:"]
        for (label, previous, current), numbers in changes.items():
            scope = (
                f"Semua {len(numbers)} transaksi"
                if len(numbers) == len(after_rows)
                else "No. " + ", ".join(map(str, numbers))
            )
            lines.append(f"• {scope}: {label} {previous} → {current}")
        lines.append("Belum disimpan. Periksa rekapan di bawah.")
        result = "\n".join(lines)
        if len(result) > 700:
            return f"✅ Detail {len(changed_numbers)} transaksi diperbarui. Periksa perubahan di rekapan; belum disimpan."
        return result

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
                review = self.s.engine.get_review_queue_item(rid)
                if not review:
                    return True, "BATCH_EMAIL_NOT_FOUND"
                if action == "gin":
                    if review.status == "PENDING":
                        with self.s.db.atomic():
                            self.s.engine.ignore_review_item(rid, reason="Bukan transaksi; keputusan Owner")
                            old = self.s.conn.execute("SELECT id FROM intake_batches WHERE owner=? AND source_key=?", (owner, "review:"+rid)).fetchone()
                            if old:
                                self.s.ignore(old[0], owner, "Bukan transaksi; keputusan Owner")
                    self.send_closed(owner, msg.get("message_id"), "✅ Bukan transaksi. Kartu ditutup dan tidak masuk buku besar." if review.status in ("PENDING", "IGNORED") else "ℹ️ Kartu ini sudah diproses. Buku besar tidak diubah.")
                elif review.status != "PENDING":
                    self.send_closed(owner, msg.get("message_id"), "ℹ️ Kartu ini sudah diproses. Tidak ada pencatatan baru.")
                else:
                    batch = self.s.from_review(owner, rid)
                    with self.s.db.atomic():
                        self.s.conn.execute("INSERT INTO intake_context VALUES (?,?,?) ON CONFLICT(owner) DO UPDATE SET batch_id=excluded.batch_id,mode=excluded.mode", (owner,batch,"DETAIL"))
                    note = ("📝 Tulis tujuan dan sumber dana untuk kartu ini. Contoh: no. 1 makan malam dari Blu Gether. Jawaban tetap terhubung meski lo menolak kartu lain. Belum dicatat."
                            if action == "gsp" else "🔗 Sebut referensi transaksi yang sudah tercatat, contoh: sudah tercatat tx_CONTOH. Hermes akan memeriksa kecocokannya.")
                    self.send_preview(batch, owner, msg.get("message_id"), notice=note)
                if self.parent.outbound:
                    self.parent.outbound.answer_callback_query(cq["id"], text="Kartu ditutup" if action=="gin" else "Kirim detail lewat chat")
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
                if not any(r["status"] == "DRAFT" for r in self.s.rows(batch)):
                    self.send_preview(batch, owner, msg.get("message_id"))
                    if self.parent.outbound:
                        self.parent.outbound.answer_callback_query(cq["id"], text="Pencatatan sudah selesai; tidak ada draft menunggu.")
                    return True, "BATCH_ALREADY_COMPLETED"
                with self.s.db.atomic():
                    self.s.conn.execute(
                        "UPDATE intake_context SET mode='PAUSED' WHERE owner=? AND batch_id=?",
                        (owner, batch),
                    )
            else:
                with self.s.db.atomic():
                    self.s.conn.execute(
                        "INSERT INTO intake_context VALUES (?,?,?) ON CONFLICT(owner) DO UPDATE SET batch_id=excluded.batch_id,mode=excluded.mode",
                        (owner, batch, "DETAIL"),
                    )
                self.send_preview(batch, owner, msg.get("message_id"), editing=action != "resume")
            if self.parent.outbound:
                self.parent.outbound.answer_callback_query(
                    cq["id"],
                    text=(
                        "Draft tersimpan; proses selesai"
                        if action == "later"
                        else (
                            "Tulis perubahan lewat balasan chat"
                            if action == "edit"
                            else "Rekapan diperbarui"
                        )
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
        from . import intake_parser as parser
        numbered = re.search(r"\b(?:no\.?|nomor)\s*(\d+)\b", lower)
        explicit_action = bool(numbered or re.search(
            r"\b(?:semua\s+(?:tanggal|jam|akun)|(?:tanggal|jam|pukul)\s+(?:(?:jd|jadi|ke)\s+)?\d|pecah\s*:|sudah tercatat|bukan transaksi|sudah ganti|lanjut batch)\b", lower))
        exact_action = lower in ("rekapan", "rekap", "lihat rekapan", "tampilkan rekapan", "status transaksi", "cek draft", "catat", "simpan", "catat sekarang", "oke simpan", "setuju simpan", "simpan yang siap") or lower.startswith("simpan yang siap kecuali ")
        finance_question = bool(re.search(r"(?:butuh|perlu|kurang|minta).*?(?:konfirmasi|detail|informasi).*?(?:apa|lagi)|(?:konfirmasi|kurang|detail).*?apa.*?lagi|harus.*?(?:jawab|balas)", lower))
        # Conversational questions must reach Hermes, even with a retained card
        # context or a reply to an old receipt. A greeting/yes prefix is not consent.
        general_question = bool(re.search(r"\b(?:model|tutor|tutorial|gimana|kenapa|siapa|kapan)\b|(?:apa|berapa).*\?|apa kabar|terima kasih|makasih", lower)) and not numbered and not re.search(r"\b(?:transaksi|finance|draft|rekapan)\b", lower)
        if general_question and not finance_question and not explicit_action:
            return None
        purpose_answer = bool(re.search(r"\b(?:bayar|beli|makan|laundry|utk|untuk|dari|dr|sudah transfer|sudah ditransfer|alokasi)\b", lower) or parser.account_matches(self.s.engine, lower))
        if not purpose_answer:
            classification = parser.classify(self.s.engine, lower, "EXPENSE")
            purpose_answer = bool(classification.get("category_name"))
        if batch:
            pending = any(x["status"] == "DRAFT" for x in self.s.rows(batch))
            if not (explicit_action or exact_action or (pending and (purpose_answer or finance_question))):
                return None
        if not batch:
            r = self.s.conn.execute(
                "SELECT batch_id,mode FROM intake_context WHERE owner=?", (owner,)
            ).fetchone()
            if r:
                rows = self.s.rows(r[0])
                pending = any(x["status"] == "DRAFT" for x in rows)
                if ((pending and (explicit_action or exact_action or finance_question or (len(rows) == 1 and purpose_answer and amount(text) is None)))
                    or (not pending and (numbered or exact_action))):
                    batch = r[0]
        numbered = re.search(r"\b(?:no\.?|nomor)\s*(\d+)\b", lower)
        if not batch and numbered and self.parent.is_owner(sender):
            candidates = self.s.conn.execute("SELECT DISTINCT b.id FROM intake_batches b JOIN intake_items i ON i.batch_id=b.id WHERE b.owner=? AND i.status='DRAFT' AND i.number=? AND b.updated_at>? ORDER BY b.updated_at DESC", (owner,int(numbered[1]),time.time()-86400)).fetchall()
            if len(candidates) == 1:
                batch = candidates[0][0]
            elif len(candidates) > 1:
                choices=[]
                for candidate in candidates[:6]:
                    row=next(x for x in self.s.rows(candidate[0]) if x["number"]==int(numbered[1]))
                    d=row["data"]
                    label=f"{format_idr(d.get('amount') or 0)} · {d.get('account_name') or '?'} · {str(d.get('purpose') or d.get('note') or '')[:24]}"
                    choices.append([{"text":label,"callback_data":"bi:resume:"+candidate[0]}])
                with self.s.db.atomic():
                    enqueue(self.s.db,"batch_selector",uid(),owner,"sendMessage",{"chat_id":owner,"text":"Ada beberapa draft dengan nomor itu. Pilih transaksi yang dimaksud; jawaban tidak dikirim ke chat umum.","reply_markup":{"inline_keyboard":choices}})
                dispatch(self.s.db,self.parent.outbound)
                return True,"BATCH_SELECTION_REQUIRED"
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
        notice = None
        try:
            if batch:
                if not self.s.owned(batch, owner):
                    return True, "BLOCKED_BATCH_OWNER"
                if lower in ("rekapan", "rekap", "lihat rekapan", "tampilkan rekapan", "status transaksi", "cek draft") or re.search(r"(?:butuh|perlu|kurang|minta).*?(?:konfirmasi|detail|informasi).*?(?:apa|lagi)|(?:konfirmasi|kurang|detail).*?apa.*?lagi|harus.*?(?:jawab|balas)|(?:bingung|cara pakai)", lower):
                    pending = [r for r in self.s.rows(batch) if r["status"] == "DRAFT"]
                    missing = sorted({x for r in pending for x in self.s.approval_issues(r["data"], r["id"])})
                    notice = ("ℹ️ Belum ada perubahan draft. Yang masih kurang: " + ", ".join(missing) + "."
                              if missing else "✅ Detail sudah cukup. Lo tinggal pilih Simpan untuk menyetujui rekapan dan usulan kategori. Belum dicatat.")
                    self.send_preview(batch, owner, notice=notice)
                    return True, "BATCH_STATUS_EXPLAINED"
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
                elif lower in ("simpan", "catat", "catat sekarang", "oke simpan", "setuju simpan") or lower.startswith(
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
                    before_rows = self.s.rows(batch)
                    if re.search(
                        r"\b(?:jam|pukul)\s+(?:(?:jd|jadi|ke)\s+)?\d", lower
                    ) and not time_in(text):
                        self.send_preview(
                            batch,
                            owner,
                            notice="⚠️ Jam belum terbaca; belum ada perubahan. Contoh: semua jam jadi 17.30 atau no. 3 jam 5 sore.",
                        )
                        return True, "BATCH_TIME_NEEDS_DETAIL"
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
                    unresolved_meaning = any(r["status"] == "DRAFT" and r["data"].get("purpose") and
                        not (r["data"].get("category_id") or r["data"].get("proposed_category")) for r in self.s.rows(batch))
                    account_only = text.lower()
                    from . import intake_parser as parser
                    for start,end,account in reversed(parser.account_matches(self.s.engine, text.lower())):
                        account_only=account_only[:start]+" "+account_only[end:]
                    account_only=re.sub(r"\b(?:no\.?|nomor)\s*\d+|\b(?:akun|dari|dr|sumber|dana|pembayaran|lewat|dengan|pakai)\b|[\s:;,.]+", "", account_only)
                    if (unresolved_meaning or (not changed and any(r["status"]=="DRAFT" and (r["data"].get("needs_purpose") or not (r["data"].get("category_id") or r["data"].get("proposed_category"))) for r in self.s.rows(batch)))) and amount(text) is None and account_only and not re.search(r"sudah (?:dipindah|transfer|ditransfer)|\balokasi\b", lower):
                        from .intake_semantic import enrich

                        enrich(self.s, batch, text)
                    notice = self.change_notice(before_rows, self.s.rows(batch))
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
                    and not rows[0]["data"].get("requires_preview")
                    and not self.s.issues(rows[0]["data"], rows[0]["id"])
                    and not rows[0]["data"].get("proposed_category")
                    and not rows[0]["data"].get("proposed_subcategory")
                ):
                    self.s.commit(batch, owner)
                    dispatch(self.s.db, self.parent.outbound)
                    return True, "BATCH_SINGLE_RECORDED"
            self.send_preview(batch, owner, notice=notice)
            return True, "BATCH_DRAFT_UPDATED"
        except (ValueError, KeyError, TypeError) as exc:
            if self.parent.outbound:
                self.parent.outbound.send_message(
                    owner, "Draft tetap tersimpan. " + str(exc)[:180]
                )
            return True, "BATCH_NEEDS_DETAIL"
