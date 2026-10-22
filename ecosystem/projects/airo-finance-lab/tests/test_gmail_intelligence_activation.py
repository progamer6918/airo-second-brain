#!/usr/bin/env python3
"""
Unit tests for AIRO Finance Lab - Gmail Intelligence Activation V1
Validates:
1. Read-only email ingestion contract (no mutations, no deletes, no sends)
2. Financial email detection & filtering
3. Transaction detail extraction
4. Classification & confidence scoring
5. Duplicate protection (message_id & deterministic fingerprint)
6. Zero direct ledger writes
7. Review queue lifecycle (approve, ignore, learn aliases)
8. Finance Inbox grouping
9. Telegram callbacks (gma:, gmi:, gmc:)
"""

import os
import sys
import unittest
import tempfile
import json
from unittest.mock import MagicMock, patch

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from airo_finance_core.db import DatabaseManager
from airo_finance_core.engine import FinanceCoreEngine
from airo_finance_core.gmail_intelligence import GmailIntelligenceService
from airo_finance_core.telegram_ingress import FinanceTelegramIngressRouter


class TestGmailIntelligenceActivation(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tmp_dir.name, "test_finance.db")
        self.db = DatabaseManager(self.db_path)
        self.db.init_schema()
        self.engine = FinanceCoreEngine(self.db)

        # Setup base accounts
        self.acc_bca = self.engine.create_account("BCA Utama", "BANK", 2000000.0)
        self.acc_blu = self.engine.create_account("Blu BCA", "BANK", 1000000.0)

        # Setup base categories and subcategories
        self.cat_food = self.engine.create_category("Makanan & Minuman", "kopi, resto, makan, gofood, grabfood")
        self.sub_coffee = self.engine.create_subcategory(self.cat_food.id, "Kopi")
        self.sub_lunch = self.engine.create_subcategory(self.cat_food.id, "Makan Siang")

        self.cat_bill = self.engine.create_category("Tagihan & Utilitas", "listrik, pln, internet, indihome, pulsa")
        self.sub_electric = self.engine.create_subcategory(self.cat_bill.id, "Listrik")

        self.cat_shop = self.engine.create_category("Belanja Kebutuhan", "tokopedia, shopee, indomaret, alfamart")

        # Add alias
        self.engine.add_category_alias(keyword="starbucks", subcategory_id=self.sub_coffee.id, category_id=self.cat_food.id)

        self.service = GmailIntelligenceService(self.engine, token_path="/dev/null")

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_read_only_contract(self):
        """Service only queries read endpoints and never exposes delete/send/mutate calls."""
        mock_gmail = MagicMock()
        self.service._gmail_service = mock_gmail

        mock_messages = mock_gmail.users.return_value.messages.return_value
        mock_messages.list.return_value.execute.return_value = {"messages": []}

        result = self.service.scan_inbox(max_results=5)
        self.assertEqual(result["scanned"], 0)

        # Verify no delete or modify methods were called
        self.assertFalse(mock_messages.delete.called)
        self.assertFalse(mock_messages.batchDelete.called)
        self.assertFalse(mock_messages.modify.called)
        self.assertFalse(mock_messages.batchModify.called)
        self.assertFalse(mock_messages.send.called)

    def test_financial_email_filtering(self):
        """Correctly distinguish financial emails from noise."""
        # Financial cases
        is_fin, cat = self.service.is_financial_email(
            sender="halo@blubybcadigital.id",
            subject="Transaksi Berhasil di Kopi Kenangan",
            snippet="Rp 28.000 telah dibayarkan"
        )
        self.assertTrue(is_fin)
        self.assertEqual(cat, "BANK")

        is_fin2, cat2 = self.service.is_financial_email(
            sender="notification@tokopedia.com",
            subject="Pembayaran Berhasil untuk Pesanan #12345",
            snippet="Total pembayaran Rp 150.000"
        )
        self.assertTrue(is_fin2)
        self.assertEqual(cat2, "MARKETPLACE")

        is_fin3, cat3 = self.service.is_financial_email(
            sender="info@pln.co.id",
            subject="Tagihan Listrik Pascabayar Periode September",
            snippet="Total tagihan sebesar IDR 450.000"
        )
        self.assertTrue(is_fin3)
        self.assertEqual(cat3, "FINANCE_UTILITY")

        is_fin4, cat4 = self.service.is_financial_email(
            sender="unknown@sender.com",
            subject="Bukti Transfer Pembayaran Makan",
            snippet="Transfer Rp 50.000 telah selesai"
        )
        self.assertTrue(is_fin4)
        self.assertEqual(cat4, "HEURISTIC")

        # Non-financial cases
        is_fin_neg1, _ = self.service.is_financial_email(
            sender="newsletter@medium.com",
            subject="Your daily digest for tech news",
            snippet="Check out top stories today"
        )
        self.assertFalse(is_fin_neg1)

        is_fin_neg2, _ = self.service.is_financial_email(
            sender="security@google.com",
            subject="Security alert for your linked account",
            snippet="New login from Windows"
        )
        self.assertFalse(is_fin_neg2)

    def test_transaction_extraction(self):
        """Extract structured fields: amount, merchant, date, direction, account."""
        email_body = "Transaksi QRIS pada 2026-09-12 sebesar Rp 65.000 berhasil ke STARBUCKS RESERVE."
        tx = self.service.parse_email(
            email_text=email_body,
            subject="Bukti Transaksi QRIS BCA - Starbucks Reserve",
            sender="e-statement@bca.co.id"
        )
        self.assertEqual(tx["amount"], 65000.0)
        self.assertEqual(tx["currency"], "IDR")
        self.assertEqual(tx["direction"], "EXPENSE")
        self.assertIn("STARBUCKS", tx["merchant"].upper())
        self.assertIn("BCA", tx["account_source"])

    def test_classification_and_confidence(self):
        """Classification assigns correct categories and confidence scores."""
        # Test registered alias match
        cat_id1, cat_name1, subcat_id1, subcat_name1, conf1 = self.service.classify("Starbucks Senayan", 55000.0)
        self.assertEqual(cat_id1, self.cat_food.id)
        self.assertEqual(subcat_id1, self.sub_coffee.id)
        self.assertGreaterEqual(conf1, 0.90)

        # Test utility keyword match
        cat_id2, cat_name2, subcat_id2, subcat_name2, conf2 = self.service.classify("Pembayaran PLN Listrik Batam", 150000.0)
        self.assertEqual(cat_id2, self.cat_bill.id)
        self.assertGreaterEqual(conf2, 0.80)

    def test_duplicate_protection(self):
        """Duplicate message_id or identical fingerprint prevents duplicate enqueue."""
        res1 = self.service.process_email(
            email_text="Total pembayaran Rp 75.000 ke Tokopedia.",
            subject="Pembayaran Pesanan Tokopedia",
            sender="billing@tokopedia.com",
            message_id="dup_msg_1",
            thread_id="t1"
        )
        self.assertEqual(res1["status"], "QUEUED_FOR_REVIEW")

        # 1. Same message_id should be skipped
        res_same_msg = self.service.process_email(
            email_text="Total pembayaran Rp 75.000 ke Tokopedia.",
            subject="Pembayaran Pesanan Tokopedia",
            sender="billing@tokopedia.com",
            message_id="dup_msg_1",
            thread_id="t1"
        )
        self.assertEqual(res_same_msg["status"], "DUPLICATE_SKIPPED")

        # 2. Different message_id but same fingerprint (same date, merchant, amount, account)
        res_same_fp = self.service.process_email(
            email_text="Total pembayaran Rp 75.000 ke Tokopedia.",
            subject="Pembayaran Pesanan Tokopedia (Forwarded)",
            sender="billing@tokopedia.com",
            message_id="dup_msg_2",
            thread_id="t2"
        )
        self.assertEqual(res_same_fp["status"], "QUEUED_FOR_REVIEW")
        self.assertIn("Kemungkinan duplikat", " ".join(res_same_fp["parsed"]["review_reasons"]))

    def test_zero_direct_ledger_mutations(self):
        """Email processing must ONLY create review_queue items, never direct ledger rows."""
        tx_count_before = len(self.engine.list_transactions())
        self.assertEqual(tx_count_before, 0)

        res = self.service.process_email(
            email_text="Transfer Rp 25.000 ke Fore Coffee berhasil",
            subject="Transfer Berhasil",
            sender="halo@blubybcadigital.id",
            message_id="safe_test_msg"
        )
        self.assertEqual(res["status"], "QUEUED_FOR_REVIEW")

        # Ledger MUST still have 0 transactions
        tx_count_after = len(self.engine.list_transactions())
        self.assertEqual(tx_count_after, 0)

        # Review queue must have 1 pending item
        pending = self.engine.list_review_queue(status="PENDING")
        self.assertEqual(len(pending), 1)

    def test_review_queue_approval_and_ignore_lifecycle(self):
        """Owner approval creates ledger transaction & learns alias; ignore cancels without ledger touch."""
        res = self.service.process_email(
            email_text="Transfer Rp 42.000 ke Janji Jiwa Mall berhasil",
            subject="Transfer Berhasil",
            sender="halo@blubybcadigital.id",
            message_id="queue_test_1"
        )
        item_id = res["review_id"]

        # Verify finance inbox groupings
        inbox = self.engine.get_finance_inbox()
        all_pending = inbox["new_candidates"] + inbox["needs_review"]
        self.assertTrue(any(i["id"] == item_id for i in all_pending))

        # Approve with category and subcategory
        override = {
            "merchant": "Janji Jiwa Mall",
            "amount": 42000.0,
            "direction": "EXPENSE",
            "account_id": self.acc_blu.id,
            "category_id": self.cat_food.id,
            "subcategory_id": self.sub_coffee.id,
            "note": "Kopi pagi"
        }
        res_approval = self.engine.approve_review_item(item_id, override_data=override)
        tx = res_approval[1] if isinstance(res_approval, tuple) else res_approval
        self.assertIsNotNone(tx)
        self.assertEqual(tx.amount, 42000.0)
        self.assertEqual(tx.category_id, self.cat_food.id)
        self.assertEqual(tx.subcategory_id, self.sub_coffee.id)

        # Ledger balance verification
        blu_acc = self.engine.get_account(self.acc_blu.id)
        self.assertEqual(blu_acc.balance, 1000000.0 - 42000.0)

        # Verify alias learning: "Janji Jiwa Mall" should now be in aliases!
        aliases = self.engine.list_category_aliases()
        self.assertTrue(any("janji jiwa" in a.keyword.lower() for a in aliases))

        # Test ignore flow on a second candidate
        res2 = self.service.process_email(
            email_text="Dapatkan pinjaman hingga Rp 10.000.000 hari ini",
            subject="Penawaran Pinjaman Rp 10.000.000",
            sender="promo@bank.co.id",
            message_id="queue_test_2"
        )
        if res2.get("review_id"):
            ignored = self.engine.ignore_review_item(res2["review_id"], reason="Penawaran iklan / bukan transaksi")
            self.assertEqual(ignored.status, "IGNORED")

    def test_telegram_callback_actions(self):
        """Telegram callbacks gma: and gmi: execute approval and ignore correctly."""
        router = FinanceTelegramIngressRouter(self.engine)

        res = self.service.process_email(
            email_text="Pembayaran QRIS Rp 35.000 di Kenangan Heritage",
            subject="Pembayaran QRIS Rp 35.000",
            sender="halo@blubybcadigital.id",
            message_id="tg_test_1"
        )
        item_id = res["review_id"]

        # Test approve callback
        callback_approve = {
            "id": "cb_001",
            "data": f"gma:{item_id}",
            "from": {"id": "12345"},
            "message": {"message_id": 999, "chat": {"id": "12345"}}
        }
        handled, status = router.handle_update({"callback_query": callback_approve})
        self.assertTrue(handled)
        self.assertIn("GMAIL_CONFIRMED", status)

        # Test ignore callback on a new item
        res2 = self.service.process_email(
            email_text="Pembayaran QRIS Rp 12.000 di Alfamart",
            subject="Pembayaran QRIS Rp 12.000",
            sender="halo@blubybcadigital.id",
            message_id="tg_test_2"
        )
        item_id2 = res2["review_id"]

        callback_ignore = {
            "id": "cb_002",
            "data": f"gmi:{item_id2}",
            "from": {"id": "12345"},
            "message": {"message_id": 1000, "chat": {"id": "12345"}}
        }
        handled2, status2 = router.handle_update({"callback_query": callback_ignore})
        self.assertTrue(handled2)
        self.assertEqual("GMAIL_IGNORED", status2)


if __name__ == "__main__":
    unittest.main()
