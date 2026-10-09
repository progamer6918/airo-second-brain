import os
import sys
import unittest
from datetime import datetime, timezone

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from airo_finance_core.db import DatabaseManager
from airo_finance_core.engine import FinanceCoreEngine
from airo_finance_core.insights import FinanceInsightsService
from airo_finance_core.gmail_intelligence import GmailIntelligenceService
from airo_finance_core.telegram_ingress import FinanceTelegramIngressRouter, TelegramOutboundAdapter


class TestGmailHermesRealEventCanary(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseManager(":memory:")
        self.db.init_schema()
        self.engine = FinanceCoreEngine(self.db)
        self.insights = FinanceInsightsService(self.db)

        # Seed test accounts
        self.acc_blu = self.engine.create_account(
            name="Blu",
            account_type="BANK",
            initial_balance=100000.0,
            account_class="LIQUID",
            dashboard_group="CASH"
        )
        self.acc_pocket = self.engine.create_account(
            name="Blu Saving",
            account_type="POCKET",
            initial_balance=50000.0,
            account_class="POCKET",
            dashboard_group="CASH",
            parent_account_id=self.acc_blu.id
        )

        # Mock Telegram Outbound transport
        self.outbound_calls = []
        def mock_transport(method, payload):
            self.outbound_calls.append({"method": method, "payload": payload})
            return {"ok": True, "result": {"message_id": 998877}}

        self.mock_outbound = TelegramOutboundAdapter(token="MOCK_TOKEN", transport=mock_transport)
        self.owner_chat_id = "12345678"

        self.service = GmailIntelligenceService(
            self.engine,
            token_path="nonexistent_token.json",
            outbound=self.mock_outbound,
            owner_chat_id=self.owner_chat_id
        )

        self.router = FinanceTelegramIngressRouter(
            self.engine,
            outbound=self.mock_outbound,
            owner_chat_id=self.owner_chat_id
        )

    def test_01_canary_parsing_and_detection(self):
        """Phase 2: Canary event parsing, financial detection, amount Rp1, date, type Antar blu, source Blu"""
        raw_email = (
            "Transaksimu Pakai blu Berhasil\n"
            "Detail Transaksi:\n"
            "Tanggal: 13 Sep 2026 13:55:41 WIB\n"
            "Tipe Transaksi: Antar blu\n"
            "Nominal: Rp1\n"
            "Sumber Rekening: bluAccount\n"
            "Tujuan: Rekening blu Lainnya\n"
        )
        subject = "Transaksimu Pakai blu Berhasil"
        sender = "receipts@blubybcadigital.id"

        # 1. Verify Financial Detection Layer
        is_fin, cat = self.service.is_financial_email(sender, subject, raw_email)
        self.assertTrue(is_fin)
        self.assertEqual(cat, "BANK")

        # 2. Verify Parsing
        parsed = self.service.parse_email(raw_email, subject, sender)
        self.assertEqual(parsed["amount"], 1.0)
        self.assertEqual(parsed["date"], "2026-09-13")
        self.assertEqual(parsed["account_source"], "Blu")
        self.assertEqual(parsed["direction"], "TRANSFER")
        self.assertEqual(parsed["tx_type"], "Antar blu")

        # 3. Process email and verify review queue entry
        res = self.service.process_email(
            email_text=raw_email,
            subject=subject,
            sender=sender,
            message_id="canary_msg_001"
        )
        self.assertEqual(res["status"], "QUEUED_FOR_REVIEW")
        review_id = res["review_id"]
        self.assertIsNotNone(review_id)

        # Check queue item status
        q_item = self.engine.get_review_queue_item(review_id)
        self.assertEqual(q_item.status, "PENDING")

        # Check Finance Inbox grouping -> must be in needs_review
        inbox = self.engine.get_finance_inbox()
        self.assertTrue(any(item["id"] == review_id for item in inbox["needs_review"]))

    def test_02_hermes_notification_trigger_and_payload(self):
        """Phase 3: Telegram notification delivered via Hermes with required summary & inline buttons"""
        raw_email = (
            "Transaksimu Pakai blu Berhasil\n"
            "Tanggal: 13 Sep 2026 13:55:41 WIB\n"
            "Tipe: Antar blu\n"
            "Nominal: Rp 1\n"
        )
        res = self.service.process_email(
            email_text=raw_email,
            subject="Transaksimu Pakai blu Berhasil",
            sender="receipts@blubybcadigital.id",
            message_id="canary_msg_002"
        )
        self.assertEqual(res["telegram_delivery"], "PASS")
        self.assertEqual(res["telegram_message_id"], "998877")
        self.assertTrue(res["payload_verified"])

        # Inspect outbound payload
        self.assertTrue(len(self.outbound_calls) > 0)
        sent = self.outbound_calls[-1]
        self.assertEqual(sent["method"], "sendMessage")
        payload = sent["payload"]
        self.assertEqual(payload["chat_id"], self.owner_chat_id)
        self.assertIn("Rp 1", payload["text"])
        self.assertIn("Blu", payload["text"])
        self.assertIn("Antar blu", payload["text"])

        # Inspect Inline Buttons: [Approve], [Edit], [Ignore]
        rows = payload.get("reply_markup", {}).get("inline_keyboard", [])
        self.assertEqual([len(row) for row in rows], [1, 1, 1, 1])
        buttons = [button for row in rows for button in row]
        self.assertEqual(len(buttons), 4)
        self.assertTrue(any("Setujui" in b["text"] and b["callback_data"].startswith("gma:") for b in buttons))
        self.assertTrue(any("Catatan" in b["text"] and b["callback_data"].startswith("gsp:") for b in buttons))
        self.assertTrue(any("Bukan transaksi" in b["text"] and b["callback_data"].startswith("gin:") for b in buttons))

    def test_03_internal_transfer_ledger_protection(self):
        """Phase 4: Approving Antar blu transfer preserves Net Worth and does NOT mutate Expense or Income"""
        nw_before = self.insights.get_net_worth_report().net_worth
        monthly_before = self.insights.get_monthly_summary(2026, 9)
        exp_before = monthly_before.total_expense
        inc_before = monthly_before.total_income

        raw_email = "Transaksimu Pakai blu Berhasil\nTanggal: 13 Sep 2026 13:55:41 WIB\nTipe: Antar blu\nNominal: Rp 1\n"
        res = self.service.process_email(
            email_text=raw_email,
            subject="Transaksimu Pakai blu Berhasil",
            sender="receipts@blubybcadigital.id",
            message_id="canary_msg_003"
        )
        review_id = res["review_id"]

        # Approve review item
        updated_item, tx = self.engine.approve_review_item(review_id, {"destination_account_id": self.acc_pocket.id})
        self.assertEqual(updated_item.status, "APPROVED")
        self.assertEqual(tx.direction, "TRANSFER")
        self.assertEqual(tx.amount, 1.0)

        # Verify Balances: Source decreased by 1, target pocket increased by 1
        acc_blu = self.engine.get_account(self.acc_blu.id)
        acc_pocket = self.engine.get_account(self.acc_pocket.id)
        self.assertEqual(acc_blu.balance, 99999.0)
        self.assertEqual(acc_pocket.balance, 50001.0)

        # Verify Net Worth unchanged: DELTA_NET_WORTH = 0
        nw_after = self.insights.get_net_worth_report().net_worth
        self.assertEqual(nw_after - nw_before, 0.0)

        # Verify Expense and Income unchanged: DELTA_EXPENSE = 0, DELTA_INCOME = 0
        monthly_after = self.insights.get_monthly_summary(2026, 9)
        self.assertEqual(monthly_after.total_expense - exp_before, 0.0)
        self.assertEqual(monthly_after.total_income - inc_before, 0.0)

    def test_04_duplicate_protection(self):
        """Phase 5: Rescanning same email message_id or duplicate transaction returns DUPLICATE_SKIPPED"""
        raw_email = "Transaksimu Pakai blu Berhasil\nTanggal: 13 Sep 2026 13:55:41 WIB\nTipe: Antar blu\nNominal: Rp 1\n"
        res1 = self.service.process_email(
            email_text=raw_email,
            subject="Transaksimu Pakai blu Berhasil",
            sender="receipts@blubybcadigital.id",
            message_id="canary_msg_004"
        )
        self.assertEqual(res1["status"], "QUEUED_FOR_REVIEW")

        # Second scan with exact same message_id
        res2 = self.service.process_email(
            email_text=raw_email,
            subject="Transaksimu Pakai blu Berhasil",
            sender="receipts@blubybcadigital.id",
            message_id="canary_msg_004"
        )
        self.assertEqual(res2["status"], "DUPLICATE_SKIPPED")
        self.assertEqual(res2["action"], "SKIPPED")

        # Second scan with different message_id but identical transaction fingerprint
        res3 = self.service.process_email(
            email_text=raw_email,
            subject="Transaksimu Pakai blu Berhasil",
            sender="receipts@blubybcadigital.id",
            message_id="canary_msg_004_alt"
        )
        self.assertEqual(res3["status"], "QUEUED_FOR_REVIEW")
        self.assertIn("Kemungkinan duplikat", " ".join(res3["parsed"]["review_reasons"]))

    def test_05_telegram_callback_approval_flow(self):
        """Phase 3 & 4: Telegram inline callback 'gma:<id>' successfully approves transfer and updates message"""
        raw_email = "Transaksimu Pakai blu Berhasil\nTanggal: 13 Sep 2026 13:55:41 WIB\nTipe: Antar blu\nNominal: Rp 1\n"
        res = self.service.process_email(
            email_text=raw_email,
            subject="Transaksimu Pakai blu Berhasil",
            sender="receipts@blubybcadigital.id",
            message_id="canary_msg_005"
        )
        review_id = res["review_id"]
        with self.db.get_connection():
            row = self.db.get_connection().execute("SELECT parsed_result FROM review_queue WHERE id=?", (review_id,)).fetchone()
            import json
            parsed = json.loads(row[0]); parsed["destination_account_id"] = self.acc_pocket.id
            self.db.get_connection().execute("UPDATE review_queue SET parsed_result=? WHERE id=?", (json.dumps(parsed),review_id))


        # Simulate Owner clicking [Approve] button
        callback_update = {
            "callback_query": {
                "id": "cb_001",
                "from": {"id": int(self.owner_chat_id)},
                "data": f"gma:{review_id}",
                "message": {
                    "message_id": 998877,
                    "chat": {"id": int(self.owner_chat_id)}
                }
            }
        }
        handled, reason = self.router.handle_update(callback_update)
        self.assertTrue(handled)
        self.assertTrue(reason.startswith("GMAIL_CONFIRMED:tx_"))

        # Verify message was edited to show confirmation receipt
        edit_calls = [c for c in self.outbound_calls if c["method"] == "editMessageText"]
        self.assertTrue(len(edit_calls) > 0)
        last_edit = edit_calls[-1]["payload"]
        self.assertIn("Transfer Berhasil Disetujui", last_edit["text"])
        self.assertIn("Net Worth tidak berubah", last_edit["text"])


if __name__ == "__main__":
    unittest.main()
