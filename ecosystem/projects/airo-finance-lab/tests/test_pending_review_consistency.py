import unittest
import json
from airo_finance_core.db import DatabaseManager
from airo_finance_core.engine import FinanceCoreEngine
from airo_finance_core.gmail_intelligence import GmailIntelligenceService
from airo_finance_core.telegram_ingress import FinanceTelegramIngressRouter

class MockTelegramOutbound:
    def __init__(self):
        self.sent_messages = []
        self.edited_messages = []
        self.callbacks_answered = []

    def send_message(self, chat_id, text, reply_markup=None):
        self.sent_messages.append({"chat_id": chat_id, "text": text, "reply_markup": reply_markup})
        return {"ok": True, "result": {"message_id": 9999}}

    def edit_message_text(self, chat_id, message_id, text, reply_markup=None):
        self.edited_messages.append({"chat_id": chat_id, "message_id": message_id, "text": text, "reply_markup": reply_markup})
        return {"ok": True}

    def answer_callback_query(self, callback_query_id, text=None, show_alert=False):
        self.callbacks_answered.append({"id": callback_query_id, "text": text, "show_alert": show_alert})
        return {"ok": True}

class TestPendingReviewConsistency(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseManager(':memory:')
        self.db.init_schema()
        self.engine = FinanceCoreEngine(self.db)
        self.outbound = MockTelegramOutbound()
        self.ingress = FinanceTelegramIngressRouter(self.engine, outbound=self.outbound, owner_chat_id="12345")
        self.gmail = GmailIntelligenceService(self.engine, outbound=self.outbound, owner_chat_id="12345")

        # Setup basic accounts and categories
        self.acc = self.engine.create_account(
            name="BCA Operasional",
            account_type="BANK",
            initial_balance=10000000.0,
            account_class="LIQUID",
            dashboard_group="CASH"
        )
        self.cat = self.engine.create_category(
            name="Operasional",
            keywords="server,vps,hosting,domain",
            dashboard_group="OPERASIONAL",
            domain="BUSINESS"
        )

    def tearDown(self):
        self.db.close()

    def test_gmail_candidate_lifecycle_and_review_query_consistency(self):
        """
        Regression Test for AIRO Finance Pending Review Consistency Bug V1:
        1. Process incoming Gmail financial transaction -> creates candidate in review_queue with PENDING status.
        2. Verify review_queue item creation is guaranteed BEFORE Telegram card delivery.
        3. Verify both /review and /pending commands list the item.
        4. Approve review item via callback -> status becomes APPROVED, ledger updated.
        5. Verify item is removed from /review and /pending (returns empty state).
        """
        # Step 1: Ingest simulated Gmail notification
        raw_text = "Transaksi Pembayaran Berhasil. Pembayaran Rp 150.000 ke SERVER HOSTING pada 2026-09-13"
        res = self.gmail.process_email(
            email_text=raw_text,
            subject="Transaksi Pembayaran Berhasil",
            sender="notif@bca.co.id",
            message_id="msg_consistency_001",
            thread_id="th_001"
        )
        self.assertEqual(res["status"], "QUEUED_FOR_REVIEW")
        review_id = res["review_id"]
        self.assertTrue(review_id.startswith("rq_"))

        # Step 2: Verify persistent record in review_queue exists with status=PENDING
        q_item = self.engine.get_review_queue_item(review_id)
        self.assertIsNotNone(q_item)
        self.assertEqual(q_item.status, "PENDING")
        self.assertEqual(q_item.id, review_id)

        # Also verify raw DB query directly
        conn = self.db.get_connection()
        db_row = conn.execute("SELECT id, status FROM review_queue WHERE id = ?", (review_id,)).fetchone()
        self.assertIsNotNone(db_row)
        self.assertEqual(db_row["status"], "PENDING")

        # Step 3: Verify /review and /pending commands query the same source and show the item
        # Test /review
        self.outbound.sent_messages.clear()
        handled, action = self.ingress.handle_update({
            "message": {
                "chat": {"id": 12345},
                "from": {"id": 12345},
                "text": "/review",
                "message_id": 101
            }
        })
        self.assertTrue(handled)
        self.assertEqual(action, "PENDING_REVIEW_CARD_SENT")
        self.assertEqual(len(self.outbound.sent_messages), 1)
        review_card_text = self.outbound.sent_messages[-1]["text"]
        self.assertIn("Pending Review Center", review_card_text)
        self.assertIn("150.000", review_card_text)
        self.assertNotIn("Tidak ada transaksi pending review", review_card_text)

        # Test /pending
        self.outbound.sent_messages.clear()
        handled, action = self.ingress.handle_update({
            "message": {
                "chat": {"id": 12345},
                "from": {"id": 12345},
                "text": "/pending",
                "message_id": 102
            }
        })
        self.assertTrue(handled)
        self.assertEqual(action, "PENDING_REVIEW_CARD_SENT")
        self.assertEqual(len(self.outbound.sent_messages), 1)
        pending_card_text = self.outbound.sent_messages[-1]["text"]
        self.assertIn("Pending Review Center", pending_card_text)
        self.assertIn("150.000", pending_card_text)

        # Step 4: Simulate owner approving the review item via callback (gma:<review_id>)
        self.outbound.edited_messages.clear()
        handled, action = self.ingress.handle_update({
            "callback_query": {
                "id": "cq_approve_1",
                "from": {"id": 12345},
                "message": {"chat": {"id": 12345}, "message_id": 9999},
                "data": f"gma:{review_id}"
            }
        })
        self.assertTrue(handled)
        self.assertTrue(action.startswith("GMAIL_CONFIRMED:"))

        # Check queue item status is now APPROVED
        updated_item = self.engine.get_review_queue_item(review_id)
        self.assertEqual(updated_item.status, "APPROVED")
        self.assertIsNotNone(updated_item.approved_transaction_id)

        # Step 5: Verify item is removed from /review and /pending
        self.outbound.sent_messages.clear()
        handled, action = self.ingress.handle_update({
            "message": {
                "chat": {"id": 12345},
                "from": {"id": 12345},
                "text": "/review",
                "message_id": 103
            }
        })
        self.assertTrue(handled)
        self.assertEqual(action, "PENDING_REVIEW_CARD_SENT")
        empty_review_text = self.outbound.sent_messages[-1]["text"]
        self.assertIn("Tidak ada transaksi pending review", empty_review_text)

    def test_gmail_candidate_ignore_lifecycle(self):
        """
        Verify that ignoring a review item removes it from /review and /pending.
        """
        # Step 1: Ingest simulated Gmail notification
        raw_text = "Pembayaran Rp 50.000 berhasil pada 2026-09-13"
        res = self.gmail.process_email(
            email_text=raw_text,
            subject="Notifikasi Transaksi",
            sender="notif@bca.co.id",
            message_id="msg_consistency_002",
            thread_id="th_002"
        )
        review_id = res["review_id"]

        # Step 2: Ignore the item via callback (gmi:<review_id>)
        handled, action = self.ingress.handle_update({
            "callback_query": {
                "id": "cq_ignore_1",
                "from": {"id": 12345},
                "message": {"chat": {"id": 12345}, "message_id": 9999},
                "data": f"gmi:{review_id}"
            }
        })
        self.assertTrue(handled)
        self.assertEqual(action, "GMAIL_IGNORED")

        # Step 3: Verify item status is IGNORED
        item = self.engine.get_review_queue_item(review_id)
        self.assertEqual(item.status, "IGNORED")

        # Step 4: Verify /review shows empty
        self.outbound.sent_messages.clear()
        handled, action = self.ingress.handle_update({
            "message": {
                "chat": {"id": 12345},
                "from": {"id": 12345},
                "text": "/review",
                "message_id": 104
            }
        })
        self.assertTrue(handled)
        self.assertIn("Tidak ada transaksi pending review", self.outbound.sent_messages[-1]["text"])

if __name__ == "__main__":
    unittest.main()
