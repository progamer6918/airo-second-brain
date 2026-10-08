import base64, json, os, sys, tempfile, time, unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
os.environ["AIRO_FINANCE_OFFLINE_TEST"] = "1"
from airo_finance_core import (
    DatabaseManager,
    FinanceCoreEngine,
    GmailIntelligenceService,
)
from airo_finance_core.intake_service import IntakeService
from airo_finance_core.intake_parser import parse_line, parse_batch, time_in, ZONE
from airo_finance_core.intake_semantic import enrich
from airo_finance_core.intake_learning import chronological_evaluation, activate
from airo_finance_core.telegram_ingress import (
    FinanceTelegramIngressRouter,
    TelegramOutboundAdapter,
)
from airo_finance_core import gmail_reliability as rel
from airo_finance_core.gmail_details import body, facts


class Intake(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = self.tmp.name + "/db.sqlite"
        self.db = DatabaseManager(self.path)
        self.db.init_schema()
        self.e = FinanceCoreEngine(self.db)
        self.accounts = {
            n: self.e.create_account(n, "BANK", 1000000)
            for n in ["Blu", "Blu Saving", "Blu Gether", "Cash Bensin", "Cash Umum"]
        }
        for cat, subs in [
            ("Makanan & Minuman", ["Makan Siang", "Makan Malam"]),
            ("Transportasi", ["BBM"]),
            ("Personal Care", ["Barber"]),
            ("Gaji & Pemasukan", ["Salary", "Refund"]),
        ]:
            c = self.e.create_category(
                cat, event_type="INCOME" if cat == "Gaji & Pemasukan" else "EXPENSE"
            )
            for sub in subs:
                self.e.create_subcategory(c.id, sub)
        with self.db.atomic():
            rel.put(
                self.db,
                "intake_owner_context",
                {"excluded_personal_income_names": ["nora"]},
            )
        self.s = IntakeService(self.e)
        self.calls = []
        self.out = TelegramOutboundAdapter(
            "mock",
            lambda m, p: self.calls.append((m, p))
            or {"ok": True, "result": {"message_id": len(self.calls) + 10}},
        )

    def tearDown(self):
        self.db.close()
        self.tmp.cleanup()

    def draft(self, text="blu bayar 12rb makan siang", key="1"):
        return self.s.create(
            "1", "tg:" + key, text, now=datetime(2026, 10, 7, 12, 0, 0, tzinfo=ZONE)
        )

    def balances(self):
        return {a.name: a.balance for a in self.e.list_accounts()}

    def email_fixture(self, key, amount=26000):
        return self.e.enqueue_review_item("Synthetic reference: " + key, {
            "message_id": key, "amount": amount, "account_id": self.accounts["Blu"].id,
            "account_name": "Blu", "direction": "EXPENSE", "direction_known": True,
            "date": "2026-10-08", "merchant": "Transaksimu Pakai blu Berhasil",
        }, 0.45)

    def card_click(self, router, action, review, mid=80):
        return router.handle_update({"callback_query": {"id": "mock-callback", "from": {"id": 1},
            "data": action + ":" + review.id, "message": {"message_id": mid, "chat": {"id": 1}}}})

    def test_email_note_survives_rejection_other_card_and_restart(self):
        router = FinanceTelegramIngressRouter(self.e, owner_chat_id="1", outbound=self.out)
        dinner = self.email_fixture("dinner")
        junk = self.email_fixture("promotion", amount=0)
        self.card_click(router, "gsp", dinner)
        batch = self.s.conn.execute("SELECT batch_id FROM intake_context WHERE owner='1'").fetchone()[0]
        self.card_click(router, "gin", junk, 81)
        self.assertEqual(self.s.conn.execute("SELECT batch_id FROM intake_context WHERE owner='1'").fetchone()[0], batch)
        self.assertEqual(self.s.conn.execute("SELECT COUNT(*) FROM intake_batches WHERE source_key=?", ("review:"+junk.id,)).fetchone()[0], 0)
        router = FinanceTelegramIngressRouter(self.e, owner_chat_id="1", outbound=self.out)
        result = router.handle_update({"message": {"message_id": 99, "from": {"id": 1}, "chat": {"id": 1}, "text": "no 1 makan malam dari blu gether"}})
        self.assertTrue(result[0])
        data = self.s.rows(batch)[0]["data"]
        self.assertEqual(data["amount"], 26000)
        self.assertEqual(data["subcategory_name"], "Makan Malam")
        self.assertEqual(data["account_id"], self.accounts["Blu"].id)
        self.assertEqual(data["funding_account_id"], self.accounts["Blu Gether"].id)
        self.assertNotIn("tujuan belanja", self.s.issues(data))
        self.assertTrue(any("pendanaan" in x or "sumber" in x for x in self.s.issues(data)))
        self.assertEqual(self.s.conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0], 0)

    def test_reject_existing_note_draft_closes_card_and_clears_context(self):
        router = FinanceTelegramIngressRouter(self.e, owner_chat_id="1", outbound=self.out)
        junk = self.email_fixture("not-event", amount=0)
        self.card_click(router, "gsp", junk)
        batch = self.s.conn.execute("SELECT batch_id FROM intake_context WHERE owner='1'").fetchone()[0]
        for _ in range(2): self.card_click(router, "gin", junk)
        self.assertEqual(self.e.get_review_queue_item(junk.id).status, "IGNORED")
        self.assertFalse(self.s.conn.execute("SELECT 1 FROM intake_context WHERE owner='1'").fetchone())
        self.assertNotIn("Transaksimu", self.s.preview(batch))
        closed = [p for m,p in self.calls if m == "editMessageText"][-1]
        self.assertIn("Kartu ditutup", closed["text"])
        self.assertEqual(closed["reply_markup"]["inline_keyboard"], [])
        self.assertEqual(self.s.conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0], 0)

    def test_existing_email_draft_reselect_restores_context(self):
        router = FinanceTelegramIngressRouter(self.e, owner_chat_id="1", outbound=self.out)
        first, second = self.email_fixture("first"), self.email_fixture("second")
        self.card_click(router, "gsp", first)
        old = self.s.conn.execute("SELECT batch_id FROM intake_context WHERE owner='1'").fetchone()[0]
        self.card_click(router, "gsp", second)
        self.card_click(router, "gsp", first)
        self.assertEqual(self.s.conn.execute("SELECT batch_id FROM intake_context WHERE owner='1'").fetchone()[0], old)
        self.assertEqual(self.s.conn.execute("SELECT COUNT(*) FROM intake_batches").fetchone()[0], 2)

    def test_one_correction_reads_account_and_purpose_together(self):
        batch = self.draft("blu bayar 26rb", key="purpose-account")
        self.s.update_text(batch, "no 1 makan malam dari blu gether")
        data = self.s.rows(batch)[0]["data"]
        self.assertEqual(data["account_id"], self.accounts["Blu Gether"].id)
        self.assertEqual(data["subcategory_name"], "Makan Malam")

    def test_email_card_buttons_are_full_width_and_readable(self):
        svc = GmailIntelligenceService(self.e, outbound=self.out, owner_chat_id="1")
        svc.process_email("Rp26.000", "Transaksimu Pakai blu Berhasil", "notice@blubybcadigital.id", "mock-button-fixture", received_date="2026-10-08")
        card = next(p for m,p in self.calls if m=="sendMessage" and "inline_keyboard" in p.get("reply_markup", {}))
        rows = card["reply_markup"]["inline_keyboard"]
        self.assertEqual(len(rows), 4)
        self.assertTrue(all(len(row)==1 for row in rows))
        self.assertEqual([row[0]["text"] for row in rows], ["✅ Setujui", "📝 Catatan / pecah", "🔗 Sudah tercatat", "🚫 Bukan transaksi"])

    def test_confirmed_transfer_without_ledger_is_not_asked_again_or_created(self):
        review = self.email_fixture("funding-ack")
        batch = self.s.from_review("1", review.id)
        self.s.update_text(batch, "no 1 makan malam dari blu gether")
        self.s.update_text(batch, "no 1 sudah ditransfer")
        row = self.s.rows(batch)[0]
        self.assertEqual(row["data"]["funding_mode"], "TRANSFER_CONFIRMED")
        self.assertIsNone(row["data"].get("funding_date"))
        issues = self.s.issues(row["data"], row["id"])
        self.assertTrue(any("menunggu rekonsiliasi" in x for x in issues))
        self.assertFalse(any(x.startswith("bukti pendanaan") for x in issues))
        preview = self.s.preview(batch)
        self.assertNotIn("sudah transfer atau", preview)
        self.assertEqual(self.s.commit(batch, "1")["new_transactions"], [])
        self.assertEqual(self.s.conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0], 0)

    def test_instruction_wrapped_numbered_batch_has_exactly_twenty_rows(self):
        text = (
            "Buat draft batch berikut. Semua transaksi tanggal 7 Oktober 2026; jam tidak diketahui.\n"
            "Tampilkan satu rekapan sebelum menyimpan. Kalau ada detail belum jelas, tanyakan sekaligus. Jangan simpan sebelum persetujuan.\n"
            + "\n".join(
                f"{i}. Blu terima Rp{100+i}.000 dari Nora untuk rumah."
                for i in range(1, 21)
            )
            + "\nPenerimaan dari Nora adalah kontribusi rumah tangga, bukan pencatatan gaji. Alokasi anggaran bukan bukti pengeluaran sudah terjadi."
        )
        b = self.draft(text)
        rows = self.s.rows(b)
        self.assertEqual([r["number"] for r in rows], list(range(1, 21)))
        self.assertEqual(
            [r["data"]["amount"] for r in rows],
            [(100 + i) * 1000 for i in range(1, 21)],
        )
        self.assertTrue(all(r["data"]["date"] == "2026-10-07" for r in rows))
        self.assertTrue(all(r["data"]["occurred_at"] is None for r in rows))
        self.assertEqual(
            self.s.conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0], 0
        )

    def test_incomplete_numbered_transactions_are_not_context(self):
        entries = parse_batch(
            self.e,
            "Buat draft batch berikut\n1. Blu bayar makan malam\n2. terima 99rb dari Nora",
        )
        self.assertEqual(len(entries), 2)
        self.assertIsNone(entries[0]["amount"])
        self.assertIsNone(entries[1]["account_id"])

    def test_shared_natural_time_header(self):
        entries = parse_batch(
            self.e,
            "Semua transaksi tanggal 7 Oktober 2026 jam 5 sore\n1. Blu bayar 12rb makan siang\n2. Gether bayar 22rb makan malam",
        )
        self.assertEqual(len(entries), 2)
        self.assertTrue(
            all(d["occurred_at"] == "2026-10-07T17:00:00+07:00" for d in entries)
        )
        self.assertTrue(
            all(
                d["time_precision"] == "MINUTE" and d["time_source"] == "OWNER"
                for d in entries
            )
        )

    def test_shared_time_answer_and_numbered_exception_survive_restart(self):
        b = self.draft(
            "tanggal 7 Oktober 2026\nBlu bayar 12rb makan siang\nGether bayar 22rb makan malam"
        )
        before = [
            (
                r["data"]["amount"],
                r["data"]["account_id"],
                r["data"]["subcategory_name"],
            )
            for r in self.s.rows(b)
        ]
        self.assertTrue(
            self.s.update_text(
                b, "untuk jam samakan semua jam 5 sore; no. 2 jam 18:04:09"
            )
        )
        self.db.close()
        self.db = DatabaseManager(self.path)
        self.e = FinanceCoreEngine(self.db)
        self.s = IntakeService(self.e)
        rows = self.s.rows(b)
        self.assertEqual(rows[0]["data"]["occurred_at"], "2026-10-07T17:00:00+07:00")
        self.assertEqual(rows[1]["data"]["occurred_at"], "2026-10-07T18:04:09+07:00")
        self.assertEqual(rows[1]["data"]["time_precision"], "SECOND")
        after = [
            (
                r["data"]["amount"],
                r["data"]["account_id"],
                r["data"]["subcategory_name"],
            )
            for r in rows
        ]
        self.assertEqual(before, after)
        self.assertEqual(
            self.s.conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0], 0
        )

    def test_noon_and_night_natural_time(self):
        for text, expected in [
            ("jam 11 siang", "11:00:00"),
            ("jam 1 malam", "01:00:00"),
            ("jam 12 malam", "00:00:00"),
        ]:
            data = parse_line(
                self.e, "Blu bayar 12rb makan siang tanggal 7 Oktober 2026 " + text
            )
            self.assertEqual(data["occurred_at"], "2026-10-07T" + expected + "+07:00")

    def test_single_transaction_with_draft_instructions_needs_preview(self):
        router = FinanceTelegramIngressRouter(
            self.e, self.out, "1", auto_register_commands=False
        )
        with patch("airo_finance_core.intake_semantic.enrich", return_value=False):
            result = router.handle_update(
                {
                    "message": {
                        "message_id": 88,
                        "from": {"id": 1},
                        "chat": {"id": 1},
                        "text": "Buat draft batch berikut tanggal 7 Oktober 2026\nJangan simpan sebelum persetujuan.\n1. Blu bayar 12rb makan siang",
                    }
                }
            )
        self.assertEqual(result[1], "BATCH_DRAFT_UPDATED")
        batch = self.s.conn.execute("SELECT id FROM intake_batches").fetchone()[0]
        self.assertEqual(len(self.s.rows(batch)), 1)
        self.assertEqual(
            self.s.conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0], 0
        )
        self.assertEqual(
            len(
                self.s.commit(batch, "1", confirm_suggestions=True)["new_transactions"]
            ),
            1,
        )

    def test_natural_time_reply_uses_existing_batch_without_posting(self):
        b = self.draft(
            "tanggal 7 Oktober 2026\nBlu bayar 12rb makan siang\nGether bayar 22rb makan malam"
        )
        router = FinanceTelegramIngressRouter(
            self.e, self.out, "1", auto_register_commands=False
        )
        result = router.handle_update(
            {
                "message": {
                    "message_id": 89,
                    "from": {"id": 1},
                    "chat": {"id": 1},
                    "text": "samakan aja jam 5 sore",
                }
            }
        )
        self.assertEqual(result[1], "BATCH_DRAFT_UPDATED")
        self.assertTrue(
            all(
                r["data"]["occurred_at"] == "2026-10-07T17:00:00+07:00"
                for r in self.s.rows(b)
            )
        )
        self.assertEqual(
            self.s.conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0], 0
        )

    def test_dotted_owner_time_formats_and_money_boundary(self):
        for phrase in (
            "semua jam jd 17.30",
            "semua jam jadi 17.30",
            "no. 2 pukul 17.30",
            "semua jam 17:30",
        ):
            self.assertEqual(time_in(phrase), (17, 30, 0, "MINUTE"))
        self.assertIsNone(time_in("nominal Rp17.300"))
        self.assertIsNone(time_in("jam 17.300"))
        self.assertIsNone(time_in("semua jam jd 17.99"))

    def test_edit_button_opens_guidance_then_dotted_reply_updates_and_receipts(self):
        b = self.draft(
            "tanggal 7 Oktober 2026\nBlu bayar 12rb makan siang\nGether bayar 22rb makan malam"
        )
        self.s.update_text(b, "semua jam 17:00")
        router = FinanceTelegramIngressRouter(
            self.e, self.out, "1", auto_register_commands=False
        )
        result = router.handle_update(
            {
                "callback_query": {
                    "id": "edit-now",
                    "data": "bi:edit:" + b,
                    "from": {"id": 1},
                    "message": {"message_id": 77, "chat": {"id": 1}},
                }
            }
        )
        self.assertEqual(result[1], "BATCH_EDIT")
        prompts = [p for method, p in self.calls if method == "editMessageText"]
        self.assertEqual(len(prompts), 1)
        self.assertIn("Balas pesan ini", prompts[0]["text"])
        self.assertIn("Semua jam jadi 17.30", prompts[0]["text"])
        self.assertNotIn("1. 2026-10-07", prompts[0]["text"])
        self.assertTrue(
            all(
                "bi:save:" not in button["callback_data"]
                for row in prompts[0]["reply_markup"]["inline_keyboard"]
                for button in row
            )
        )
        reply_id = int(
            self.s.conn.execute(
                "SELECT message_id FROM intake_prompts WHERE batch_id=?", (b,)
            ).fetchone()[0]
        )
        self.db.close()
        self.db = DatabaseManager(self.path)
        self.e = FinanceCoreEngine(self.db)
        self.s = IntakeService(self.e)
        router = FinanceTelegramIngressRouter(
            self.e, self.out, "1", auto_register_commands=False
        )
        self.calls.clear()
        result = router.handle_update(
            {
                "message": {
                    "message_id": 90,
                    "from": {"id": 1},
                    "chat": {"id": 1},
                    "reply_to_message": {"message_id": reply_id},
                    "text": "semua jam jd 17.30",
                }
            }
        )
        self.assertEqual(result[1], "BATCH_DRAFT_UPDATED")
        self.assertTrue(
            all(
                r["data"]["occurred_at"] == "2026-10-07T17:30:00+07:00"
                for r in self.s.rows(b)
            )
        )
        messages = [p for method, p in self.calls if method == "sendMessage"]
        self.assertEqual(len(messages), 1)
        self.assertIn(
            "Semua 2 transaksi: jam 17.00 WIB → 17.30 WIB", messages[0]["text"]
        )
        self.assertIn("17:30 ·", messages[0]["text"])
        self.assertNotIn("17:30:00", messages[0]["text"])
        self.assertIn("Pengeluaran", messages[0]["text"])
        self.assertEqual(
            messages[0]["reply_markup"]["inline_keyboard"][0][0]["text"],
            "✅ Simpan 2 transaksi",
        )
        self.assertEqual(
            self.s.conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0], 0
        )
        self.s.commit(b, "1", confirm_suggestions=True)
        self.assertEqual(
            {r[0] for r in self.s.conn.execute("SELECT occurred_at FROM transactions")},
            {"2026-10-07T10:30:00+00:00"},
        )

    def test_invalid_time_has_explicit_feedback_and_no_mutation(self):
        b = self.draft(
            "tanggal 7 Oktober 2026\nBlu bayar 12rb makan siang\nGether bayar 22rb makan malam"
        )
        self.s.update_text(b, "semua jam 17:00")
        before = self.s.rows(b)
        router = FinanceTelegramIngressRouter(
            self.e, self.out, "1", auto_register_commands=False
        )
        with patch("airo_finance_core.intake_semantic.enrich") as model:
            result = router.handle_update(
                {
                    "message": {
                        "message_id": 91,
                        "from": {"id": 1},
                        "chat": {"id": 1},
                        "text": "semua jam jd 17.99",
                    }
                }
            )
            model.assert_not_called()
        self.assertEqual(result[1], "BATCH_TIME_NEEDS_DETAIL")
        self.assertEqual(before, self.s.rows(b))
        self.assertIn(
            "Jam belum terbaca; belum ada perubahan", self.calls[-1][1]["text"]
        )

    def test_unrecognized_edit_does_not_claim_update(self):
        b = self.draft(
            "tanggal 7 Oktober 2026\nBlu bayar 12rb makan siang\nGether bayar 22rb makan malam"
        )
        router = FinanceTelegramIngressRouter(
            self.e, self.out, "1", auto_register_commands=False
        )
        with patch("airo_finance_core.intake_semantic.enrich", return_value=False):
            router.handle_update(
                {
                    "message": {
                        "message_id": 92,
                        "from": {"id": 1},
                        "chat": {"id": 1},
                        "text": "no. 1 blablabla",
                    }
                }
            )
        self.assertIn("Belum ada perubahan", self.calls[-1][1]["text"])
        self.assertEqual(
            self.s.conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0], 0
        )

    def test_twenty_rows_no_loss_dates_and_no_salary(self):
        text = "\n".join(
            "blu terima " + str(100 + i) + "rb dari Nora untuk rumah" for i in range(20)
        )
        b = self.draft(text)
        self.assertEqual(len(self.s.rows(b)), 20)
        self.assertEqual(self.s.commit(b, "1")["new_transactions"], [])
        self.s.update_text(b, "semua tanggal 3 Oktober 2026")
        self.s.update_text(b, "no. 4 tanggal 5 Oktober 2026")
        result = self.s.commit(b, "1")
        self.assertEqual(len(result["new_transactions"]), 20)
        self.assertEqual(self.s.rows(b)[3]["data"]["date"], "2026-10-05")
        cats = [
            r[0]
            for r in self.s.conn.execute(
                "SELECT s.name FROM transactions t JOIN subcategories s ON s.id=t.subcategory_id"
            )
        ]
        self.assertEqual(set(cats), {"Kontribusi Rumah Tangga"})

    def test_partial_commit_restart_and_retry(self):
        b = self.draft(
            "tanggal 3 Oktober 2026\nblu bayar 12rb makan siang\nterima 99rb dari Nora"
        )
        self.assertEqual(len(self.s.commit(b, "1")["new_transactions"]), 1)
        self.db.close()
        self.db = DatabaseManager(self.path)
        self.db.init_schema()
        self.e = FinanceCoreEngine(self.db)
        self.s = IntakeService(self.e)
        self.assertEqual(self.s.commit(b, "1")["new_transactions"], [])
        self.s.update_text(b, "no. 2 dari gether")
        self.assertEqual(len(self.s.commit(b, "1")["new_transactions"]), 1)
        self.assertEqual(
            self.s.conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0], 2
        )

    def test_idempotent_source(self):
        b = self.draft()
        self.assertEqual(b, self.draft())
        self.s.commit(b, "1")
        self.assertEqual(self.s.commit(b, "1")["new_transactions"], [])

    def test_shared_date_and_exception_one_message(self):
        b = self.draft("blu bayar 12rb makan siang\ngether bayar 22rb makan malam")
        self.s.update_text(
            b, "semua tanggal 3 Oktober 2026; no. 2 tanggal 5 Oktober 2026"
        )
        self.assertEqual(
            [r["data"]["date"] for r in self.s.rows(b)], ["2026-10-03", "2026-10-05"]
        )

    def test_atomic_failure_after_first_post(self):
        b = self.draft(
            "tanggal 3 Oktober 2026\nblu bayar 12rb makan siang\ngether bayar 22rb makan malam"
        )
        before = self.balances()
        original = self.e.create_transaction

        def fail(*args, **kwargs):
            if args[0] == self.accounts["Blu Gether"].id:
                raise RuntimeError("simulated write failure")
            return original(*args, **kwargs)

        with patch.object(self.e, "create_transaction", side_effect=fail):
            with self.assertRaises(RuntimeError):
                self.s.commit(b, "1")
        self.assertEqual(self.balances(), before)
        self.assertEqual(
            self.s.conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0], 0
        )
        self.assertTrue(all(r["status"] == "DRAFT" for r in self.s.rows(b)))

    def test_receipt_failure_does_not_repost(self):
        b = self.draft()
        r = self.s.commit(b, "1")
        balance = self.balances()
        rel.dispatch(
            self.db,
            TelegramOutboundAdapter(
                "mock", lambda m, p: {"ok": False, "error_code": 429}
            ),
        )
        self.assertEqual(self.s.commit(b, "1")["new_transactions"], [])
        self.assertEqual(self.balances(), balance)

    def test_receipt_outbox_failure_rolls_back(self):
        b = self.draft()
        before = self.balances()
        with patch(
            "airo_finance_core.intake_service.enqueue",
            side_effect=RuntimeError("outbox unavailable"),
        ):
            with self.assertRaises(RuntimeError):
                self.s.commit(b, "1")
        self.assertEqual(self.balances(), before)

    def test_cross_account_split_existing_funding(self):
        for source in ["Blu Saving", "Blu Gether"]:
            self.e.transfer_funds(
                self.accounts[source].id,
                self.accounts["Blu"].id,
                12000,
                tx_date="2026-10-03",
            )
        b = self.draft("blu bayar 24rb makan siang tanggal 3 Oktober 2026")
        self.s.update_text(
            b, "pecah: makan siang 12rb dari saving; makan malam 12rb dari gether"
        )
        before = self.balances()
        r = self.s.commit(b, "1")
        self.assertEqual(len(r["new_transactions"]), 2)
        self.assertEqual(
            self.e.get_account(self.accounts["Blu"].id).balance, before["Blu"] - 24000
        )
        self.assertEqual(
            self.e.get_account(self.accounts["Blu Saving"].id).balance,
            before["Blu Saving"],
        )
        self.assertEqual(
            self.s.conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0], 6
        )

    def test_split_mismatch_and_missing_funding_block_whole_group(self):
        b = self.draft("blu bayar 24rb makan siang")
        self.s.update_text(
            b, "pecah: makan siang 12rb dari saving; makan malam 10rb dari gether"
        )
        self.assertEqual(self.s.commit(b, "1")["new_transactions"], [])
        self.assertIn(
            "total pecahan tidak sama", self.s.issues(self.s.rows(b)[0]["data"])
        )

    def test_purpose_not_account(self):
        d = parse_line(self.e, "cash bensin bayar 24rb makan malam")
        self.assertEqual(d["subcategory_name"], "Makan Malam")
        self.assertTrue(d["replacement_pending"])
        b = self.draft("cash bensin bayar 24rb makan malam")
        self.s.commit(b, "1")
        self.assertEqual(
            self.s.conn.execute("SELECT status FROM intake_replacements").fetchone()[0],
            "PENDING",
        )
        self.s.update_text(b, "no. 1 sudah diganti")
        self.assertEqual(
            self.s.conn.execute("SELECT status FROM intake_replacements").fetchone()[0],
            "RESOLVED",
        )

    def test_precise_and_estimated_time(self):
        now = datetime(2026, 10, 7, 12, 2, 3, tzinfo=ZONE)
        d = parse_line(self.e, "blu bayar 12rb makan siang", now=now)
        self.assertEqual(d["occurred_at"], now.isoformat())
        self.assertEqual(d["time_precision"], "ESTIMATED")
        d = parse_line(self.e, "blu bayar 12rb makan siang kemarin", now=now)
        self.assertIsNone(d["occurred_at"])
        self.assertEqual(d["date"], "2026-10-06")
        d = parse_line(
            self.e, "blu bayar 12rb makan siang 3 Oktober 2026 jam 12:01:02", now=now
        )
        self.assertEqual(d["time_precision"], "SECOND")

    def test_email_body_and_no_full_body_persistence(self):
        raw = "Pembayaran QRIS\nNominal Transaksi: Rp24.000\nNama Merchant: Warung Example\n3 Oktober 2026 12:01:02 WIB\nNo Referensi: ABC12345\nprivate body sentinel"
        encoded = base64.urlsafe_b64encode(raw.encode()).decode().rstrip("=")
        self.assertEqual(
            body({"payload": {"mimeType": "text/plain", "body": {"data": encoded}}}),
            raw,
        )
        svc = GmailIntelligenceService(self.e, outbound=self.out, owner_chat_id="1")
        svc.defer_delivery = True
        r = svc.process_email(
            raw,
            "Transaksimu Pakai blu Berhasil",
            "receipts@blubybcadigital.id",
            "receipt1",
        )
        q = self.e.get_review_queue_item(r["review_id"])
        self.assertNotIn("private body sentinel", q.raw_text + q.parsed_result)
        p = json.loads(q.parsed_result)
        self.assertEqual(p["occurred_at"], "2026-10-03T12:01:02+07:00")
        self.assertEqual(p["bank_reference"], "ABC12345")

    def test_generic_alias_quarantined(self):
        c = self.e.list_categories()[0]
        self.e.add_category_alias("transaksimu pakai blu berhasil", category_id=c.id)
        self.db.init_schema()
        self.assertIsNone(
            self.e.find_category_by_keyword("Transaksimu Pakai blu Berhasil")
        )

    def test_equal_amount_not_dropped(self):
        one = self.draft()
        self.s.commit(one, "1")
        two = self.draft(key="2")
        self.assertIn(
            "kemungkinan sudah tercatat", self.s.issues(self.s.rows(two)[0]["data"])
        )
        self.s.update_text(two, "no. 1 ini kejadian baru")
        self.assertEqual(len(self.s.commit(two, "1")["new_transactions"]), 1)

    def test_semantic_injection_invalid_output_no_write(self):
        b = self.draft("blu bayar 12rb barang baru")
        before = self.s.rows(b)
        self.assertFalse(
            enrich(
                self.s,
                b,
                "text",
                resolver=lambda c: {
                    "patches": [{"number": 1, "fields": {"sql": "delete"}}]
                },
            )
        )
        self.assertEqual(self.s.rows(b), before)
        self.assertEqual(
            self.s.conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0], 0
        )

    def test_semantic_cannot_overwrite_explicit_account(self):
        b = self.draft("blu bayar 12rb barang baru")
        self.assertTrue(
            enrich(
                self.s,
                b,
                "text",
                resolver=lambda c: {
                    "patches": [
                        {
                            "number": 1,
                            "fields": {
                                "account_id": self.accounts["Blu Gether"].id,
                                "category_name": "Belanja Kebutuhan",
                                "subcategory_name": "Elektronik",
                            },
                        }
                    ]
                },
            )
        )
        self.assertEqual(
            self.s.rows(b)[0]["data"]["account_id"], self.accounts["Blu"].id
        )

    def test_foreign_owner_blocked(self):
        b = self.draft()
        with self.assertRaises(PermissionError):
            self.s.commit(b, "2")

    def test_new_category_one_approval(self):
        b = self.draft("blu bayar 20rb listrik")
        self.assertIn("Usul klasifikasi", self.s.preview(b))
        self.assertEqual(len(self.s.commit(b, "1")["new_transactions"]), 1)
        self.assertTrue(
            any(c.name == "Tagihan & Utilitas" for c in self.e.list_categories())
        )

    def test_receipt_balances_and_references(self):
        b = self.draft()
        r = self.s.commit(b, "1")
        self.assertIn("Rp988.000", r["receipt"])
        self.assertIn(r["new_transactions"][0], r["receipt"])
        self.assertIn("Blu", r["receipt"])

    def test_learning_gate_and_no_future_labels(self):
        b = self.draft()
        self.s.commit(b, "1")
        rule = self.s.conn.execute("SELECT id FROM intake_rules").fetchone()[0]
        with self.assertRaises(ValueError):
            activate(self.s, rule)
        records = [
            {
                "observed_at": i,
                "feature_key": "x",
                "label": label,
                "verified": True,
                "status": "ACTIVE",
            }
            for i, label in enumerate(["A", "A", "B"])
        ]
        self.assertEqual(
            chronological_evaluation(records),
            {"evaluated": 3, "suggestions": 2, "correct": 1},
        )

    def test_router_batch_persisted_and_no_twenty_cards(self):
        router = FinanceTelegramIngressRouter(
            self.e, self.out, "1", auto_register_commands=False
        )
        with patch("airo_finance_core.intake_semantic.enrich", return_value=False):
            result = router.handle_update(
                {
                    "message": {
                        "message_id": 1,
                        "from": {"id": 1},
                        "chat": {"id": 1},
                        "text": "blu bayar 12rb makan siang\ngether bayar 22rb makan malam",
                    }
                }
            )
        self.assertEqual(result[1], "BATCH_DRAFT_UPDATED")
        self.assertEqual(len([x for x in self.calls if x[0] == "sendMessage"]), 1)
        self.assertEqual(
            self.s.conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0], 0
        )

    def test_hypothetical_is_not_posted(self):
        b = self.draft("jangan catat dulu blu bayar 12rb makan siang")
        self.assertEqual(self.s.commit(b, "1")["new_transactions"], [])

    def test_posted_correction_replaces_once(self):
        b = self.draft()
        self.s.commit(b, "1")
        revision = self.s.revise(
            b, "1", 1, "no. 1 bayar 22rb makan malam", "correction1"
        )
        self.assertEqual(self.e.get_account(self.accounts["Blu"].id).balance, 988000)
        self.s.commit(revision, "1")
        self.assertEqual(self.e.get_account(self.accounts["Blu"].id).balance, 978000)
        self.assertEqual(self.s.commit(revision, "1")["new_transactions"], [])

    def test_exact_pair_undo_with_identical_transfers(self):
        one = self.e.transfer_funds(
            self.accounts["Blu Saving"].id,
            self.accounts["Blu"].id,
            12000,
            tx_date="2026-10-03",
        )
        two = self.e.transfer_funds(
            self.accounts["Blu Gether"].id,
            self.accounts["Blu"].id,
            12000,
            tx_date="2026-10-03",
        )
        self.e.void_transaction(one[0].id, scope="event")
        self.assertEqual(self.e.get_transaction(two[0].id).status, "ACTIVE")
        self.assertEqual(self.e.get_transaction(two[1].id).status, "ACTIVE")
        self.assertEqual(
            self.e.get_account(self.accounts["Blu Gether"].id).balance, 988000
        )

    def test_funding_not_reused_beyond_capacity(self):
        self.e.transfer_funds(
            self.accounts["Blu Saving"].id,
            self.accounts["Blu"].id,
            12000,
            tx_date="2026-10-03",
        )
        b = self.draft("blu bayar 24rb makan siang tanggal 3 Oktober 2026")
        self.s.update_text(
            b, "pecah: makan siang 12rb dari saving; makan malam 12rb dari saving"
        )
        self.assertEqual(self.s.commit(b, "1")["new_transactions"], [])

    def test_confirmed_missing_funding_created_once(self):
        b = self.draft("blu bayar 24rb makan siang tanggal 3 Oktober 2026")
        self.s.update_text(
            b, "pecah: makan siang 12rb dari saving; makan malam 12rb dari gether"
        )
        self.s.update_text(
            b,
            "no. 1 bagian 1 sudah ditransfer tanggal 3 Oktober 2026; no. 1 bagian 2 sudah ditransfer tanggal 3 Oktober 2026",
        )
        r = self.s.commit(b, "1")
        self.assertEqual(len(r["new_transactions"]), 2)
        self.assertEqual(
            self.s.conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0], 6
        )
        self.assertEqual(
            self.e.get_account(self.accounts["Blu Saving"].id).balance, 988000
        )
        self.assertEqual(
            self.e.get_account(self.accounts["Blu Gether"].id).balance, 988000
        )
        self.assertEqual(self.e.get_account(self.accounts["Blu"].id).balance, 1000000)

    def test_generic_email_reply_attaches_to_existing_payment(self):
        svc = GmailIntelligenceService(self.e, outbound=self.out, owner_chat_id="1")
        svc.defer_delivery = True
        r = svc.process_email(
            "Pembayaran QRIS Rp24.000",
            "Transaksimu Pakai blu Berhasil",
            "receipts@blubybcadigital.id",
            "email-demo",
            received_date="2026-10-03",
        )
        b = self.s.from_review("1", r["review_id"])
        self.assertIn("tujuan belanja", self.s.issues(self.s.rows(b)[0]["data"]))
        self.s.update_text(b, "ini makan siang")
        self.assertEqual(len(self.s.commit(b, "1")["new_transactions"]), 1)
        self.assertEqual(
            self.e.get_review_queue_item(r["review_id"]).status, "APPROVED"
        )

    def test_twenty_preview_contains_all_rows_and_unique_proposal(self):
        b = self.draft(
            "\n".join(
                "blu terima " + str(100 + i) + "rb dari Nora untuk rumah"
                for i in range(20)
            )
        )
        text = self.s.preview(b)
        self.assertLess(len(text), 4096)
        self.assertIn("20.", text)
        self.assertEqual(text.count("Usul klasifikasi"), 1)

    def test_timestamp_stored_on_ledger(self):
        b = self.draft()
        r = self.s.commit(b, "1")
        row = self.s.conn.execute(
            "SELECT occurred_at,time_precision,time_accuracy,time_source FROM transactions WHERE id=?",
            (r["new_transactions"][0],),
        ).fetchone()
        self.assertEqual(row["time_precision"], "SECOND")
        self.assertEqual(row["time_accuracy"], "ESTIMATED")
        self.assertTrue(row["occurred_at"].endswith("+00:00"))

    def test_batch_callback_restart_and_owner_check(self):
        router = FinanceTelegramIngressRouter(
            self.e, self.out, "1", auto_register_commands=False
        )
        b = self.draft()
        router = FinanceTelegramIngressRouter(
            self.e, self.out, "1", auto_register_commands=False
        )
        upd = {
            "callback_query": {
                "id": "cb",
                "data": "bi:save:" + b,
                "from": {"id": 2},
                "message": {"chat": {"id": 1}, "message_id": 10},
            }
        }
        self.assertEqual(router.handle_update(upd)[1], "BLOCKED_NON_OWNER_CALLBACK")
        upd["callback_query"]["from"]["id"] = 1
        router.handle_update(upd)
        router.handle_update(upd)
        self.assertEqual(
            self.s.conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0], 1
        )

    def test_approved_rule_requires_full_email_proof_and_disables_on_conflict(self):
        for i in range(5):
            b = self.draft(key="learn" + str(i))
            self.s.update_text(b, "no. 1 jam 12:01:02")
            self.s.update_text(b, "no. 1 ini kejadian baru")
            self.s.commit(b, "1")
        rule = self.s.conn.execute("SELECT id FROM intake_rules").fetchone()[0]
        with self.db.atomic():
            rel.put(self.db, "intake_observation_started", time.time() - 8 * 86400)
            self.s.conn.execute(
                "UPDATE intake_rules SET first_at=?", (time.time() - 8 * 86400,)
            )
        activate(self.s, rule)
        svc = GmailIntelligenceService(self.e, outbound=self.out, owner_chat_id="1")
        svc.defer_delivery = True
        raw = "Pembayaran QRIS\nNominal Transaksi: Rp12.000\nNama Merchant: makan siang\n2 September 2026 12:01:02 WIB\nNo Referensi: MOCK00001"
        before = self.e.get_account(self.accounts["Blu"].id).balance
        r = svc.process_email(
            raw, "Transaksimu Pakai blu Berhasil", "receipt@blubybcadigital.id", "auto1"
        )
        self.assertTrue(r.get("auto_recorded"))
        self.assertEqual(
            self.e.get_account(self.accounts["Blu"].id).balance, before - 12000
        )
        self.assertEqual(
            svc.process_email(
                raw,
                "Transaksimu Pakai blu Berhasil",
                "receipt@blubybcadigital.id",
                "auto1",
            )["status"],
            "DUPLICATE_SKIPPED",
        )
        unproven = svc.process_email(
            raw.replace("No Referensi: MOCK00001", ""),
            "Transaksimu Pakai blu Berhasil",
            "receipt@blubybcadigital.id",
            "no-proof",
        )
        self.assertFalse(unproven.get("auto_recorded", False))
        from airo_finance_core.intake_learning import observe

        row = self.s.rows(b)[0]
        data = dict(row["data"])
        data.update(subcategory_id="conflicting-final", subcategory_name="Makan Malam")
        with self.db.atomic():
            observe(self.s, row, data)
        self.assertEqual(
            self.s.conn.execute(
                "SELECT enabled FROM intake_rules WHERE id=?", (rule,)
            ).fetchone()[0],
            0,
        )

    def test_new_rule_cannot_borrow_old_observation_window(self):
        for i in range(5):
            b = self.draft(key="newrule" + str(i))
            self.s.update_text(b, "no. 1 ini kejadian baru")
            self.s.commit(b, "1")
        rule = self.s.conn.execute("SELECT id FROM intake_rules").fetchone()[0]
        with self.db.atomic():
            rel.put(self.db, "intake_observation_started", time.time() - 8 * 86400)
        with self.assertRaises(ValueError):
            activate(self.s, rule)

    def test_undo_releases_funding_and_does_not_void_original_transfer(self):
        original = self.e.transfer_funds(
            self.accounts["Blu Saving"].id,
            self.accounts["Blu"].id,
            12000,
            tx_date="2026-10-03",
        )
        b = self.draft("blu bayar 12rb makan siang tanggal 3 Oktober 2026")
        self.s.update_text(b, "pecah: makan siang 12rb dari saving")
        self.s.commit(b, "1")
        router = FinanceTelegramIngressRouter(
            self.e, self.out, "1", auto_register_commands=False
        )
        router.handle_update(
            {
                "callback_query": {
                    "id": "undo",
                    "from": {"id": 1},
                    "data": "bi:undo:" + b,
                    "message": {"message_id": 99, "chat": {"id": 1}},
                }
            }
        )
        self.assertEqual(self.e.get_transaction(original[0].id).status, "ACTIVE")
        self.assertEqual(
            self.s.conn.execute("SELECT COUNT(*) FROM intake_funding").fetchone()[0], 0
        )

    def test_existing_link_wrong_date_is_rejected(self):
        tx = self.e.create_transaction(
            self.accounts["Blu"].id, 12000, "EXPENSE", tx_date="2026-10-02"
        )
        b = self.draft("blu bayar 12rb makan siang tanggal 3 Oktober 2026")
        with self.assertRaises(ValueError):
            self.s.link_existing(b, "1", tx.id)

    def test_prior_day_funding_is_linked_without_changing_payment_date(self):
        original = self.e.transfer_funds(
            self.accounts["Blu Saving"].id,
            self.accounts["Blu"].id,
            12000,
            tx_date="2026-10-02",
        )
        b = self.draft("blu bayar 12rb makan siang dari saving tanggal 3 Oktober 2026")
        self.s.update_text(b, "no. 1 sudah ditransfer tanggal 2 Oktober 2026")
        self.assertEqual(self.s.rows(b)[0]["data"]["date"], "2026-10-03")
        self.assertEqual(len(self.s.commit(b, "1")["new_transactions"]), 1)
        self.assertEqual(
            self.s.conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0], 3
        )
        self.assertEqual(
            self.s.conn.execute("SELECT transaction_id FROM intake_funding").fetchone()[
                0
            ],
            original[0].id,
        )

    def test_internal_receipt_does_not_become_income(self):
        d = parse_line(self.e, "blu terima 50rb dari saving")
        self.assertEqual(d["direction"], "TRANSFER")
        self.assertEqual(d["account_id"], self.accounts["Blu Saving"].id)
        self.assertEqual(d["destination_account_id"], self.accounts["Blu"].id)

    def test_refund_and_excluded_salary_scope(self):
        d = parse_line(self.e, "saving terima 224rb dari Nora untuk ganti uang belanja")
        self.assertEqual(d["subcategory_name"], "Refund")
        b = self.draft("blu terima 1jt gaji Nora")
        self.assertFalse(self.s.commit(b, "1")["new_transactions"])

    def test_card_payment_uses_core_and_receipt_liability(self):
        card = self.e.create_credit_card("Example Card", "Mock Bank", 2000000)
        self.e.create_transaction(
            card.account_id, 100000, "EXPENSE", tx_date="2026-10-01"
        )
        b = self.draft("blu bayar Example Card 50rb tanggal 3 Oktober 2026")
        r = self.s.commit(b, "1")
        self.assertEqual(len(r["new_transactions"]), 1)
        self.assertEqual(self.e.get_credit_card(card.id).current_balance, 50000)
        self.assertIn("sisa kewajiban Rp50.000", r["receipt"])

    def test_separate_message_event_and_capture_times(self):
        b = self.draft("blu bayar 12rb makan siang tanggal 3 Oktober 2026")
        self.s.update_text(b, "no. 1 jam 12:04:09")
        r = self.s.commit(b, "1")
        tx = self.s.conn.execute(
            "SELECT occurred_at,message_at,created_at,time_precision FROM transactions WHERE id=?",
            (r["new_transactions"][0],),
        ).fetchone()
        self.assertEqual(tx["occurred_at"], "2026-10-03T05:04:09+00:00")
        self.assertEqual(tx["message_at"], "2026-10-07T05:00:00+00:00")
        self.assertEqual(tx["time_precision"], "SECOND")
        self.assertNotEqual(tx["created_at"], tx["message_at"])

    def test_shadow_monitor_persists_without_automatic_enable(self):
        rel.watchdog(self.db, None, "1", deliver=False)
        shadow = rel.state(self.db, "intake_shadow")
        self.assertEqual(shadow["status"], "observing")
        self.assertGreaterEqual(shadow["samples"], 1)
        self.assertEqual(
            self.s.conn.execute(
                "SELECT COUNT(*) FROM intake_rules WHERE enabled=1"
            ).fetchone()[0],
            0,
        )

    def test_multiple_amounts_never_silently_post_first(self):
        b = self.draft("blu bayar 24rb makan 12rb ongkir 12rb")
        self.assertFalse(self.s.commit(b, "1")["new_transactions"])
        self.assertIn(
            "beberapa nominal satu baris; pisahkan atau pecah pembayaran",
            self.s.issues(self.s.rows(b)[0]["data"]),
        )
        entries = parse_batch(
            self.e, "blu bayar 12rb makan siang dan gether bayar 22rb makan malam"
        )
        self.assertEqual(len(entries), 2)

    def test_legacy_generic_email_cannot_approve_polluted_category(self):
        svc = GmailIntelligenceService(self.e, outbound=self.out, owner_chat_id="1")
        svc.defer_delivery = True
        result = svc.process_email(
            "Pembayaran QRIS Rp12.000",
            "Transaksimu Pakai blu Berhasil",
            "receipt@blubybcadigital.id",
            "legacy-generic",
            received_date="2026-10-03",
        )
        item = self.e.get_review_queue_item(result["review_id"])
        p = json.loads(item.parsed_result)
        p.update(
            category_id=self.e.list_categories()[0].id,
            merchant="transaksimu pakai blu berhasil",
        )
        with self.db.atomic():
            self.s.conn.execute(
                "UPDATE review_queue SET parsed_result=? WHERE id=?",
                (json.dumps(p), item.id),
            )
        with self.assertRaises(ValueError):
            self.e.approve_review_item(item.id)
        router = FinanceTelegramIngressRouter(
            self.e, self.out, "1", auto_register_commands=False
        )
        result = router.handle_update(
            {
                "callback_query": {
                    "id": "legacy",
                    "from": {"id": 1},
                    "data": "gma:" + item.id,
                    "message": {"message_id": 99, "chat": {"id": 1}},
                }
            }
        )
        self.assertEqual(result[1], "BATCH_EMAIL_NEEDS_PURPOSE")
        self.assertEqual(
            self.s.conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0], 0
        )

    def test_budget_purpose_alias_is_not_inbound_funding_account(self):
        with self.db.atomic():
            self.s.conn.execute(
                "UPDATE accounts SET aliases='bensin' WHERE id=?",
                (self.accounts["Cash Bensin"].id,),
            )
        data = parse_line(self.e, "gether terima 200rb dari Nora untuk bensin")
        self.assertEqual(data["account_id"], self.accounts["Blu Gether"].id)
        self.assertEqual(data["direction"], "INCOME")
        self.assertIn("bensin", data["purpose"])

    def test_funded_correction_reuses_existing_evidence(self):
        original = self.e.transfer_funds(
            self.accounts["Blu Saving"].id,
            self.accounts["Blu"].id,
            12000,
            tx_date="2026-10-03",
        )
        b = self.draft("blu bayar 12rb makan siang tanggal 3 Oktober 2026")
        self.s.update_text(b, "pecah: makan siang 12rb dari saving")
        self.s.commit(b, "1")
        revision = self.s.revise(b, "1", 1, "no. 1 jam 12:03:04", "funded-correction")
        result = self.s.commit(revision, "1")
        self.assertEqual(len(result["new_transactions"]), 1)
        self.assertEqual(
            self.e.get_account(self.accounts["Blu Saving"].id).balance, 988000
        )
        self.assertEqual(self.e.get_transaction(original[0].id).status, "ACTIVE")
        self.assertEqual(
            self.s.conn.execute("SELECT COUNT(*) FROM intake_funding").fetchone()[0], 1
        )

    def test_unchanged_email_approval_is_not_verified_training(self):
        category = self.e.get_category_by_name("Makanan & Minuman")
        sub = next(
            x for x in self.e.list_subcategories(category.id) if x.name == "Makan Siang"
        )
        review = self.e.enqueue_review_item(
            "Gmail reference: synthetic",
            {
                "amount": 12000,
                "account_id": self.accounts["Blu"].id,
                "account_name": "Blu",
                "direction": "EXPENSE",
                "direction_known": True,
                "date": "2026-10-03",
                "note": "Example Merchant",
                "merchant": "Example Merchant",
                "category_id": category.id,
                "category_name": category.name,
                "subcategory_id": sub.id,
                "subcategory_name": sub.name,
            },
            0.8,
        )
        batch = self.s.from_review("1", review.id)
        self.assertEqual(
            len(
                self.s.commit(batch, "1", confirm_suggestions=True)["new_transactions"]
            ),
            1,
        )
        self.assertEqual(
            self.s.conn.execute("SELECT COUNT(*) FROM intake_rules").fetchone()[0], 0
        )
        self.assertEqual(
            self.s.conn.execute(
                "SELECT COUNT(*) FROM intake_observations WHERE final IS NOT NULL"
            ).fetchone()[0],
            0,
        )

    def test_same_amount_distinct_monthly_purposes_save_together(self):
        b = self.draft(
            "tanggal 3 Oktober 2026\ngether terima 50rb dari Nora untuk listrik\ngether terima 50rb dari Nora untuk darurat\ngether terima 50rb dari Nora untuk barber"
        )
        self.assertEqual(len(self.s.commit(b, "1")["new_transactions"]), 3)
        self.assertEqual(
            self.e.get_account(self.accounts["Blu Gether"].id).balance, 1150000
        )
        repeated = self.draft(
            "tanggal 4 Oktober 2026\nblu bayar 12rb makan siang\nblu bayar 12rb makan siang",
            key="repeat",
        )
        self.assertEqual(len(self.s.commit(repeated, "1")["new_transactions"]), 1)
        self.s.update_text(repeated, "no. 2 ini kejadian baru")
        self.assertEqual(len(self.s.commit(repeated, "1")["new_transactions"]), 1)

    def test_web_approval_between_draft_and_save_cannot_repost_source(self):
        category = self.e.get_category_by_name("Makanan & Minuman")
        review = self.e.enqueue_review_item(
            "Gmail reference: synthetic",
            {
                "amount": 12000,
                "account_id": self.accounts["Blu"].id,
                "account_name": "Blu",
                "direction": "EXPENSE",
                "direction_known": True,
                "date": "2026-10-03",
                "note": "Example Merchant",
                "merchant": "Example Merchant",
                "category_id": category.id,
                "category_name": category.name,
            },
            0.8,
        )
        batch = self.s.from_review("1", review.id)
        self.e.approve_review_item(review.id)
        self.s.update_text(batch, "no. 1 ini kejadian baru")
        self.assertFalse(
            self.s.commit(batch, "1", confirm_suggestions=True)["new_transactions"]
        )
        self.assertEqual(self.s.rows(batch)[0]["status"], "LINKED")
        self.assertEqual(
            self.s.conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0], 1
        )


if __name__ == "__main__":
    unittest.main()
