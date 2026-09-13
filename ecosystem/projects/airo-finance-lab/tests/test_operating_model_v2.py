import unittest
import os
import json
from datetime import datetime, timezone, date
from airo_finance_core.db import DatabaseManager
from airo_finance_core.engine import FinanceCoreEngine
from airo_finance_core.insights import FinanceInsightsService
from airo_finance_core.telegram_capture import TelegramCaptureAdapter, format_idr
from airo_finance_core.telegram_ingress import FinanceTelegramIngressRouter


class MockOutbound:
    def __init__(self):
        self.sent_messages = []
        self.edited_messages = []
        self.answered_callbacks = []

    def send_message(self, chat_id, text, reply_markup=None, parse_mode="HTML"):
        self.sent_messages.append({"chat_id": chat_id, "text": text, "reply_markup": reply_markup})
        return {"ok": True, "result": {"message_id": len(self.sent_messages)}}

    def edit_message_text(self, chat_id, message_id, text, reply_markup=None, parse_mode="HTML"):
        self.edited_messages.append({"chat_id": chat_id, "message_id": message_id, "text": text, "reply_markup": reply_markup})
        return {"ok": True, "result": {"message_id": message_id}}

    def answer_callback_query(self, callback_query_id, text=None, show_alert=False):
        self.answered_callbacks.append({"id": callback_query_id, "text": text, "show_alert": show_alert})
        return {"ok": True}


class TestOperatingModelV2(unittest.TestCase):
    def setUp(self):
        self.test_db = f"test_opv2_{int(datetime.now(timezone.utc).timestamp()*1000)}.db"
        self.db = DatabaseManager(self.test_db)
        self.db.init_schema()
        self.engine = FinanceCoreEngine(self.db)
        self.outbound = MockOutbound()
        self.owner_id = "8482041086"
        self.router = FinanceTelegramIngressRouter(
            self.engine,
            outbound=self.outbound,
            owner_chat_id=self.owner_id
        )
        self.adapter = TelegramCaptureAdapter(self.engine)
        self.insights = FinanceInsightsService(self.db)

        # Setup accounts
        self.acc_bca = self.engine.create_account("BCA Utama", "BANK", 1000000.0)
        self.acc_blu = self.engine.create_account("Blu BCA", "BANK", 500000.0)
        self.acc_pocket_cc = self.engine.create_account("Blu Pocket CC", "POCKET", 200000.0)
        self.acc_cc = self.engine.create_account("Tokopedia Card", "CREDIT_CARD", 0.0, account_class="LIABILITY")

        # Setup categories
        self.cat_food = self.engine.create_category("Makanan & Minuman")

    def tearDown(self):
        self.db.close()
        if os.path.exists(self.test_db):
            try:
                os.remove(self.test_db)
            except Exception:
                pass

    def test_01_running_balance_replay(self):
        """Feature 1: Transaction running balance calculation in engine"""
        # Create sequence of transactions
        # Initial BCA balance = 1,000,000
        # 1. Expense 100k -> balance after = 900,000
        tx1 = self.engine.create_transaction(self.acc_bca.id, 100000.0, "EXPENSE", category_id=self.cat_food.id, note="Makan siang")
        # 2. Income 50k -> balance after = 950,000
        tx2 = self.engine.create_transaction(self.acc_bca.id, 50000.0, "INCOME", note="Cashback")
        # 3. Transfer 200k from BCA to Blu -> BCA balance after = 750,000
        tx_out, tx_in = self.engine.transfer_funds(self.acc_bca.id, self.acc_blu.id, 200000.0, note="Topup Blu")

        # Query transactions and verify running balances attached
        txs = self.engine.list_transactions(account_id=self.acc_bca.id)
        # Transactions returned desc, let's map by id
        tx_map = {t.id: t.running_balance for t in txs}

        self.assertEqual(tx_map[tx1.id], 900000.0)
        self.assertEqual(tx_map[tx2.id], 950000.0)
        self.assertEqual(tx_map[tx_out.id], 750000.0)

        # Single transaction fetch also has running balance
        single_tx = self.engine.get_transaction(tx1.id)
        self.assertIsNotNone(single_tx)
        self.assertEqual(single_tx.running_balance, 900000.0)

    def test_02_pending_review_center_commands(self):
        """Feature 2: /review and /pending command handling and rendering"""
        # Initially empty review queue
        handled, reason = self.router.handle_update({
            "message": {
                "chat": {"id": self.owner_id},
                "from": {"id": self.owner_id},
                "text": "/review"
            }
        })
        self.assertTrue(handled)
        self.assertEqual(reason, "PENDING_REVIEW_CARD_SENT")
        self.assertIn("Tidak ada transaksi pending", self.outbound.sent_messages[-1]["text"])

        # Add item to review queue
        parsed_data = {
            "account_id": self.acc_bca.id,
            "amount": 45000.0,
            "direction": "EXPENSE",
            "category_id": self.cat_food.id,
            "note": "Kopi Janji Jiwa"
        }
        item = self.engine.enqueue_review_item("Kopi Janji Jiwa 45k", parsed_data, confidence=0.75, issue_reason="Low confidence category")

        # Now trigger /pending
        handled2, reason2 = self.router.handle_update({
            "message": {
                "chat": {"id": self.owner_id},
                "from": {"id": self.owner_id},
                "text": "/pending"
            }
        })
        self.assertTrue(handled2)
        self.assertEqual(reason2, "PENDING_REVIEW_CARD_SENT")
        msg = self.outbound.sent_messages[-1]
        self.assertIn("Pending Review Center", msg["text"])
        self.assertIn("Rp45.000", msg["text"])
        self.assertIn("Kopi Janji Jiwa", msg["text"])
        # Verify review action buttons present
        kb = msg["reply_markup"]["inline_keyboard"]
        self.assertEqual(len(kb), 1)
        self.assertEqual(kb[0][0]["callback_data"], f"gma:{item.id}")
        self.assertEqual(kb[0][1]["callback_data"], f"gmc:{item.id}")
        self.assertEqual(kb[0][2]["callback_data"], f"gmi:{item.id}")

    def test_03_manual_domain_entry_flow(self):
        """Feature 3: Structured manual entry /domain command and callbacks"""
        # User triggers /domain
        handled, reason = self.router.handle_update({
            "message": {
                "chat": {"id": self.owner_id},
                "from": {"id": self.owner_id},
                "text": "/domain"
            }
        })
        self.assertTrue(handled)
        self.assertEqual(reason, "DOMAIN_MENU_SENT")
        msg = self.outbound.sent_messages[-1]
        self.assertIn("Pencatatan Berdasarkan Domain", msg["text"])
        kb = msg["reply_markup"]["inline_keyboard"]
        self.assertTrue(any(btn["callback_data"] == "dom:new:expense" for row in kb for btn in row))
        self.assertTrue(any(btn["callback_data"] == "dom:new:transfer" for row in kb for btn in row))

        # User clicks "💸 Pengeluaran"
        handled_cb, reason_cb = self.router.handle_update({
            "callback_query": {
                "id": "cq_dom_1",
                "from": {"id": self.owner_id},
                "data": "dom:new:expense",
                "message": {"message_id": 101, "chat": {"id": self.owner_id}}
            }
        })
        self.assertTrue(handled_cb)
        self.assertEqual(reason_cb, "DOMAIN_PROMPTED:expense")
        self.assertIn("Pencatatan Pengeluaran", self.outbound.edited_messages[-1]["text"])

    def test_04_credit_card_closing_cycle_15th(self):
        """Feature 4: Credit card summary dynamic cycle with closing on the 15th"""
        # Add credit card
        self.engine.create_credit_card(
            name="Tokopedia Card",
            bank_name="BRI",
            credit_limit=10000000.0,
            account_id=self.acc_cc.id,
            billing_cycle_day=15,
            payment_due_day=30
        )

        cc_summary = self.insights.get_credit_card_summary()
        self.assertEqual(len(cc_summary["cards"]), 1)
        card = cc_summary["cards"][0]
        # Verify dual section closed_statement and current_period
        self.assertIn("closed_statement", card)
        self.assertIn("current_period", card)
        self.assertEqual(card["billing_cycle_day"], 15)
        self.assertEqual(card["payment_due_day"], 30)
        self.assertEqual(card["closed_statement"]["due_date"], "2026-08-30")
        self.assertEqual(card["closed_statement"]["pocket_ready"], 200000.0)
        # Verify reserve pocket tracking
        self.assertEqual(cc_summary["payment_reserve"], 200000.0)


if __name__ == "__main__":
    unittest.main()
