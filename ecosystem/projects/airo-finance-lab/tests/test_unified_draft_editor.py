import os
import unittest
from datetime import datetime, timezone
from airo_finance_core.db import DatabaseManager
from airo_finance_core.engine import FinanceCoreEngine
from airo_finance_core.telegram_capture import TelegramCaptureAdapter, TransactionCandidate
from airo_finance_core.telegram_ingress import FinanceTelegramIngressRouter

class MockOutbound:
    def __init__(self):
        self.sent_messages = []
        self.edited_messages = []
        self.answered_callbacks = []

    def send_message(self, chat_id, text, parse_mode=None, reply_markup=None):
        msg_id = len(self.sent_messages) + 100
        event = {"chat_id": chat_id, "message_id": msg_id, "text": text, "reply_markup": reply_markup}
        self.sent_messages.append(event)
        return {"ok": True, "result": {"message_id": msg_id}}

    def edit_message_text(self, chat_id, message_id, text, parse_mode=None, reply_markup=None):
        event = {"chat_id": chat_id, "message_id": message_id, "text": text, "reply_markup": reply_markup}
        self.edited_messages.append(event)
        return {"ok": True, "result": {"message_id": message_id}}

    def answer_callback_query(self, callback_query_id, text=None, show_alert=False):
        event = {"callback_query_id": callback_query_id, "text": text, "show_alert": show_alert}
        self.answered_callbacks.append(event)
        return {"ok": True, "result": True}


class TestUnifiedDraftEditorV1(unittest.TestCase):
    def setUp(self):
        self.test_db = f"test_editor_{int(datetime.now(timezone.utc).timestamp()*1000)}.db"
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

        # Setup accounts
        self.acc_bca = self.engine.create_account("BCA Utama", "BANK", 1000000.0)
        self.acc_blu = self.engine.create_account("Blu", "BANK", 500000.0)
        self.acc_cc = self.engine.create_account("Tokopedia Card", "CREDIT_CARD", 0.0)

        # Setup categories and subcategories
        self.cat_food = self.engine.create_category("Food & Drink")
        self.sub_coffee = self.engine.create_subcategory(self.cat_food.id, "Coffee")
        self.sub_meal = self.engine.create_subcategory(self.cat_food.id, "Meal")

        self.cat_shop = self.engine.create_category("Shopping")
        self.sub_market = self.engine.create_subcategory(self.cat_shop.id, "Marketplace")

        self.cat_no_sub = self.engine.create_category("Sedekah")

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_01_entry_edit_button_and_guided_menu(self):
        """ENTRY_EDIT_BUTTON & GUIDED_EDIT_MENU: Clicking ✏️ Edit renders 'Apa yang mau dikoreksi?' with inline options."""
        # Stage candidate
        cand = self.router.confirmation_handler.stage_input("makan siang 75k bca")
        
        # Click Edit (ced:<cand_id>)
        up = {
            "callback_query": {
                "id": "cq_1",
                "data": f"ced:{cand.candidate_id}",
                "from": {"id": int(self.owner_id)},
                "message": {"message_id": 501, "chat": {"id": int(self.owner_id)}}
            }
        }
        handled, reason = self.router.handle_update(up)
        self.assertTrue(handled)
        self.assertEqual(reason, f"GUIDED_EDIT_MENU:{cand.candidate_id}")

        # Verify edited message contains "Apa yang mau dikoreksi?"
        last_edit = self.outbound.edited_messages[-1]
        self.assertIn("Apa yang mau dikoreksi?", last_edit["text"])

        # Verify menu buttons
        buttons = last_edit["reply_markup"]["inline_keyboard"]
        flat_buttons = [b["text"] for row in buttons for b in row]
        self.assertIn("💰 Nominal", flat_buttons)
        self.assertIn("🏦 Akun", flat_buttons)
        self.assertIn("📂 Kategori", flat_buttons)
        self.assertIn("📝 Catatan", flat_buttons)
        self.assertIn("📅 Tanggal", flat_buttons)
        self.assertIn("❌ Batal", flat_buttons)

    def test_02_domain_filtering(self):
        """DOMAIN_FILTERING: Transfer hides Category/Subcategory; CC Purchase hides cash account."""
        # 1. TRANSFER candidate
        cand_trf = self.router.confirmation_handler.stage_input("trf 200k bca ke blu")
        menu_trf = self.router.confirmation_handler.format_guided_edit_menu(cand_trf)
        trf_buttons = [b["text"] for row in menu_trf["reply_markup"]["inline_keyboard"] for b in row]
        self.assertIn("📤 Akun Asal", trf_buttons)
        self.assertIn("📥 Akun Tujuan", trf_buttons)
        self.assertNotIn("📂 Kategori", trf_buttons)

        # 2. CREDIT CARD PURCHASE candidate
        cand_cc = TransactionCandidate(
            candidate_id="cand_cc_test",
            raw_text="kopi 50k cc",
            amount=50000.0,
            direction="EXPENSE",
            account_id=self.acc_cc.id,
            account_name=self.acc_cc.name,
            category_id=self.cat_food.id,
            category_name=self.cat_food.name,
            note="kopi cc",
            tx_type="CREDIT_CARD_PURCHASE"
        )
        menu_cc = self.router.confirmation_handler.format_guided_edit_menu(cand_cc)
        cc_buttons = [b["text"] for row in menu_cc["reply_markup"]["inline_keyboard"] for b in row]
        self.assertIn("💰 Nominal", cc_buttons)
        self.assertIn("📂 Kategori", cc_buttons)
        self.assertNotIn("🏦 Akun", cc_buttons)

    def test_03_category_dropdown_and_dynamic_subcategory(self):
        """CATEGORY_DROPDOWN & DYNAMIC_SUBCATEGORY: Categories from DB, selecting category queries subcategories."""
        cand = self.router.confirmation_handler.stage_input("makan 50k bca")
        
        # 1. Click Category field (edf:<cand_id>:cat)
        up_cat_menu = {
            "callback_query": {
                "id": "cq_cat",
                "data": f"edf:{cand.candidate_id}:cat",
                "from": {"id": int(self.owner_id)},
                "message": {"message_id": 502, "chat": {"id": int(self.owner_id)}}
            }
        }
        h_cat, r_cat = self.router.handle_update(up_cat_menu)
        self.assertTrue(h_cat)
        self.assertEqual(r_cat, f"EDIT_CATEGORY_MENU:{cand.candidate_id}")
        
        last_edit = self.outbound.edited_messages[-1]
        self.assertIn("Pilih Kategori", last_edit["text"])
        cat_buttons = [b["text"] for row in last_edit["reply_markup"]["inline_keyboard"] for b in row]
        self.assertTrue(any("Food & Drink" in b for b in cat_buttons))
        self.assertTrue(any("Shopping" in b for b in cat_buttons))

        # 2. Select Category (edc:<cand_id>:<cat_id>)
        up_select_cat = {
            "callback_query": {
                "id": "cq_sel_cat",
                "data": f"edc:{cand.candidate_id}:{self.cat_food.id}",
                "from": {"id": int(self.owner_id)},
                "message": {"message_id": 502, "chat": {"id": int(self.owner_id)}}
            }
        }
        h_sel, r_sel = self.router.handle_update(up_select_cat)
        self.assertTrue(h_sel)
        self.assertEqual(r_sel, f"SUBCATEGORY_MENU:{self.cat_food.id}")

        # Verify subcategory menu displayed
        last_edit2 = self.outbound.edited_messages[-1]
        self.assertIn("Pilih Subkategori", last_edit2["text"])
        sub_buttons = [b["text"] for row in last_edit2["reply_markup"]["inline_keyboard"] for b in row]
        self.assertTrue(any("Coffee" in b for b in sub_buttons))
        self.assertTrue(any("Meal" in b for b in sub_buttons))
        self.assertTrue(any("Lewati" in b for b in sub_buttons))

        # 3. Select Subcategory (eds:<cand_id>:<subc_id>)
        up_select_sub = {
            "callback_query": {
                "id": "cq_sel_sub",
                "data": f"eds:{cand.candidate_id}:{self.sub_meal.id}",
                "from": {"id": int(self.owner_id)},
                "message": {"message_id": 502, "chat": {"id": int(self.owner_id)}}
            }
        }
        h_sub, r_sub = self.router.handle_update(up_select_sub)
        self.assertTrue(h_sub)
        self.assertEqual(r_sub, f"DRAFT_SUBCATEGORY_UPDATED:{cand.candidate_id}")
        
        # Verify candidate updated
        self.assertEqual(cand.category_id, self.cat_food.id)
        self.assertEqual(cand.category_name, "Food & Drink")
        self.assertEqual(cand.subcategory_id, self.sub_meal.id)
        self.assertEqual(cand.subcategory_name, "Meal")

        # Verify Draft Preview was rendered
        last_edit3 = self.outbound.edited_messages[-1]
        self.assertIn("Review Perubahan Draft", last_edit3["text"])
        self.assertIn("Sebelumnya:", last_edit3["text"])
        self.assertIn("Setelah Koreksi:", last_edit3["text"])
        self.assertIn("Meal", last_edit3["text"])

    def test_04_category_without_subcategories_flows_to_preview(self):
        """If category has no subcategories, selecting category directly renders Draft Preview."""
        cand = self.router.confirmation_handler.stage_input("infak 20k bca")
        up = {
            "callback_query": {
                "id": "cq_nosub",
                "data": f"edc:{cand.candidate_id}:{self.cat_no_sub.id}",
                "from": {"id": int(self.owner_id)},
                "message": {"message_id": 503, "chat": {"id": int(self.owner_id)}}
            }
        }
        h, r = self.router.handle_update(up)
        self.assertTrue(h)
        self.assertEqual(r, f"DRAFT_CATEGORY_UPDATED:{cand.candidate_id}")
        last_edit = self.outbound.edited_messages[-1]
        self.assertIn("Review Perubahan Draft", last_edit["text"])
        self.assertEqual(cand.category_id, self.cat_no_sub.id)
        self.assertIsNone(cand.subcategory_id)

    def test_05_amount_edit_and_preview_before_apply(self):
        """DRAFT_PREVIEW & NO_PREMATURE_MUTATION: Editing amount shows Before vs After with zero ledger mutation."""
        cand = self.router.confirmation_handler.stage_input("belanja 75k bca")
        initial_balance = self.engine.get_account(self.acc_bca.id).balance

        # 1. Click Amount
        self.router.handle_update({
            "callback_query": {
                "id": "cq_amt",
                "data": f"edf:{cand.candidate_id}:amt",
                "from": {"id": int(self.owner_id)},
                "message": {"message_id": 504, "chat": {"id": int(self.owner_id)}}
            }
        })

        # 2. Send new numeric amount
        h_msg, r_msg = self.router.handle_update({
            "message": {
                "message_id": 105,
                "chat": {"id": int(self.owner_id)},
                "from": {"id": int(self.owner_id)},
                "text": "35000"
            }
        })
        self.assertTrue(h_msg)
        self.assertEqual(r_msg, f"DRAFT_AMOUNT_UPDATED:{cand.candidate_id}")
        self.assertEqual(cand.amount, 35000.0)

        # Verify NO ledger mutation occurred
        current_balance = self.engine.get_account(self.acc_bca.id).balance
        self.assertEqual(current_balance, initial_balance)
        self.assertEqual(len(self.engine.list_transactions()), 0)

        # Verify Review Changes text
        last_sent = self.outbound.sent_messages[-1]
        self.assertIn("Review Perubahan Draft", last_sent["text"])
        self.assertIn("Rp75.000", last_sent["text"])
        self.assertIn("Rp35.000", last_sent["text"])

    def test_06_confirm_apply_and_cancel_regression(self):
        """CONFIRM_APPLY & CANCEL_REGRESSION: Confirm applies ledger with edited values; cancel cleanly aborts."""
        # 1. Test Confirm Flow
        cand = self.router.confirmation_handler.stage_input("belanja 100k bca")
        self.router.confirmation_handler.apply_field_update(cand.candidate_id, "amount", 60000.0)
        self.router.confirmation_handler.apply_field_update(cand.candidate_id, "category", self.cat_shop.id)
        self.router.confirmation_handler.apply_field_update(cand.candidate_id, "subcategory", self.sub_market.id)

        up_cfm = {
            "callback_query": {
                "id": "cq_cfm",
                "data": f"cfm:{cand.candidate_id}",
                "from": {"id": int(self.owner_id)},
                "message": {"message_id": 505, "chat": {"id": int(self.owner_id)}}
            }
        }
        h_cfm, r_cfm = self.router.handle_update(up_cfm)
        self.assertTrue(h_cfm)
        self.assertTrue(r_cfm.startswith("CONFIRMED:tx_"))

        # Verify ledger write
        txs = self.engine.list_transactions()
        self.assertEqual(len(txs), 1)
        tx = txs[0]
        self.assertEqual(tx.amount, 60000.0)
        self.assertEqual(tx.category_id, self.cat_shop.id)
        self.assertEqual(tx.subcategory_id, self.sub_market.id)
        self.assertEqual(self.engine.get_account(self.acc_bca.id).balance, 1000000.0 - 60000.0)

        # 2. Test Cancel Flow
        cand2 = self.router.confirmation_handler.stage_input("kopi 25k bca")
        self.router.confirmation_handler.apply_field_update(cand2.candidate_id, "amount", 30000.0)
        up_ccl = {
            "callback_query": {
                "id": "cq_ccl",
                "data": f"ccl:{cand2.candidate_id}",
                "from": {"id": int(self.owner_id)},
                "message": {"message_id": 506, "chat": {"id": int(self.owner_id)}}
            }
        }
        h_ccl, r_ccl = self.router.handle_update(up_ccl)
        self.assertTrue(h_ccl)
        self.assertEqual(r_ccl, "CANCELLED")
        self.assertEqual(len(self.engine.list_transactions()), 1)  # No new transaction
        self.assertEqual(cand2.status, "CANCELLED")

if __name__ == "__main__":
    unittest.main()
