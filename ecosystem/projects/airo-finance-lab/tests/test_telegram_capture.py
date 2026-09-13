import os
import sys
import unittest

CORE_SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
if CORE_SRC not in sys.path:
    sys.path.insert(0, CORE_SRC)

from airo_finance_core import (
    DatabaseManager,
    FinanceCoreEngine,
    TelegramCaptureAdapter,
    SimpleTransactionParser,
    TransactionCandidate
)

class TestTelegramCaptureVerticalSlice(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseManager(":memory:")
        self.db.init_schema()
        self.engine = FinanceCoreEngine(self.db)
        
        # Seed MVP accounts
        self.acc_bca = self.engine.create_account("BCA Utama", "BANK", 1500000.0)
        self.acc_blu = self.engine.create_account("Blu BCA", "BANK", 500000.0)
        self.acc_mandiri = self.engine.create_account("Mandiri", "BANK", 250000.0)
        self.acc_cash = self.engine.create_account("Cash Dompet", "CASH", 100000.0)
        
        # Seed MVP categories
        self.cat_food = self.engine.create_category("Makanan & Minuman")
        self.cat_transport = self.engine.create_category("Transportasi")
        self.cat_bills = self.engine.create_category("Tagihan & Utilitas")
        self.cat_groceries = self.engine.create_category("Belanja Kebutuhan")
        self.cat_income = self.engine.create_category("Gaji & Pemasukan")
        
        self.adapter = TelegramCaptureAdapter(self.engine)
        self.parser = self.adapter.parser

    def tearDown(self):
        self.db.close()

    # ==========================================
    # 1. PARSER TESTS
    # ==========================================
    def test_01_parser_success_makan_35k_bca(self):
        raw_text = "makan 35k bca"
        candidate = self.parser.parse(raw_text)
        
        self.assertIsInstance(candidate, TransactionCandidate)
        self.assertEqual(candidate.amount, 35000.0)
        self.assertEqual(candidate.direction, "EXPENSE")
        self.assertEqual(candidate.account_id, self.acc_bca.id)
        self.assertEqual(candidate.account_name, "BCA Utama")
        self.assertEqual(candidate.category_id, self.cat_food.id)
        self.assertEqual(candidate.category_name, "Makanan & Minuman")
        self.assertEqual(candidate.note, "makan")
        self.assertEqual(candidate.status, "PENDING")
        print("PARSER_TEST_01: PASS ('makan 35k bca' parsed accurately)")

    def test_02_parser_various_amount_formats(self):
        test_cases = [
            ("kopi 25rb blu", 25000.0, "Blu BCA", "Makanan & Minuman"),
            ("bensin 50000", 50000.0, "BCA Utama", "Transportasi"),
            ("servis 1.5jt mandiri", 1500000.0, "Mandiri", "Transaksi"),
            ("parkir 5k cash", 5000.0, "Cash Dompet", "Transportasi"),
            ("wifi 350.000", 350000.0, "BCA Utama", "Tagihan & Utilitas")
        ]
        
        for text, exp_amount, exp_acc_name, exp_cat_or_note in test_cases:
            cand = self.parser.parse(text)
            self.assertEqual(cand.amount, exp_amount)
            self.assertEqual(cand.account_name, exp_acc_name)
        print("PARSER_TEST_02: PASS (Various IDR formats: 25rb, 50000, 1.5jt, 5k, 350.000)")

    def test_03_parser_income_detection(self):
        cand = self.parser.parse("gaji 5jt mandiri")
        self.assertEqual(cand.amount, 5000000.0)
        self.assertEqual(cand.direction, "INCOME")
        self.assertEqual(cand.account_name, "Mandiri")
        self.assertEqual(cand.category_name, "Gaji & Pemasukan")
        print("PARSER_TEST_03: PASS (Income keyword 'gaji' triggers direction=INCOME)")

    def test_04_parser_sane_default(self):
        cand = self.parser.parse("sarapan bubur 15k")
        # Should default to primary BCA account without prompting or failing
        self.assertEqual(cand.amount, 15000.0)
        self.assertEqual(cand.account_name, "BCA Utama")
        self.assertEqual(cand.category_name, "Makanan & Minuman")
        print("PARSER_TEST_04: PASS (Sane default applied when account omitted)")

    def test_05_parser_invalid_inputs(self):
        with self.assertRaises(ValueError):
            self.parser.parse("")
            
        with self.assertRaises(ValueError):
            self.parser.parse("hallo bot selamat pagi")
        print("PARSER_TEST_05: PASS (Empty and non-numeric inputs raise ValueError)")

    # ==========================================
    # 2. TELEGRAM FLOW & SHORT CALLBACK TESTS
    # ==========================================
    def test_06_telegram_confirmation_card_and_short_callbacks(self):
        cand = self.adapter.stage_input("makan 35k bca")
        card = self.adapter.format_confirmation_card(cand)
        
        self.assertIn("Konfirmasi Transaksi", card["text"])
        self.assertIn("Rp35.000", card["text"])
        self.assertIn("BCA Utama", card["text"])
        
        keyboard = card["reply_markup"]["inline_keyboard"]
        self.assertEqual(len(keyboard), 1)
        self.assertEqual(len(keyboard[0]), 3)
        
        btn_confirm = keyboard[0][0]
        btn_edit = keyboard[0][1]
        btn_cancel = keyboard[0][2]
        
        # Verify Short Callback ID Rule (<= 64 bytes)
        self.assertLessEqual(len(btn_confirm["callback_data"].encode('utf-8')), 64)
        self.assertLessEqual(len(btn_edit["callback_data"].encode('utf-8')), 64)
        self.assertLessEqual(len(btn_cancel["callback_data"].encode('utf-8')), 64)
        self.assertTrue(btn_confirm["callback_data"].startswith(f"cfm:{cand.candidate_id}"))
        self.assertTrue(btn_edit["callback_data"].startswith(f"ced:{cand.candidate_id}"))
        self.assertTrue(btn_cancel["callback_data"].startswith(f"ccl:{cand.candidate_id}"))
        print("FLOW_TEST_06: PASS (Confirmation card formatted with Simpan, Edit, Batal compliant short callback IDs)")

    def test_07_telegram_cancel_flow(self):
        cand = self.adapter.stage_input("batal 20k cash")
        ok, msg = self.adapter.cancel_candidate(cand.candidate_id)
        
        self.assertTrue(ok)
        self.assertIn("dibatalkan", msg)
        self.assertEqual(cand.status, "CANCELLED")
        
        # Verify no transactions written and cash balance untouched
        acc = self.engine.get_account(self.acc_cash.id)
        self.assertEqual(acc.balance, 100000.0)
        self.assertEqual(len(self.engine.list_transactions()), 0)
        print("FLOW_TEST_07: PASS (Cancel flow sets status=CANCELLED and leaves ledger untouched)")

    def test_08_telegram_idempotency_guard(self):
        cand = self.adapter.stage_input("makan 35k bca")
        ok1, tx1, msg1 = self.adapter.confirm_candidate(cand.candidate_id)
        self.assertTrue(ok1)
        self.assertIsNotNone(tx1)
        
        # Re-confirming should be rejected without adding duplicate ledger rows
        ok2, tx2, msg2 = self.adapter.confirm_candidate(cand.candidate_id)
        self.assertFalse(ok2)
        self.assertIsNone(tx2)
        self.assertIn("sudah pernah dicatat", msg2)
        
        txs = self.engine.list_transactions()
        self.assertEqual(len(txs), 1)
        print("FLOW_TEST_08: PASS (Idempotency guard prevents duplicate writes on repeated callbacks)")

    def test_09_telegram_handle_update_integration(self):
        # Simulate Telegram Message Update
        msg_update = {
            "update_id": 1001,
            "message": {
                "message_id": 55,
                "chat": {"id": 12345},
                "text": "makan siang 40k bca"
            }
        }
        res_msg = self.adapter.handle_update(msg_update)
        self.assertEqual(res_msg["action"], "PROMPT_CONFIRMATION")
        self.assertEqual(res_msg["status"], "SUCCESS")
        cand_id = res_msg["card"]["candidate_id"]
        
        # Simulate Telegram CallbackQuery Update
        cb_update = {
            "update_id": 1002,
            "callback_query": {
                "id": "cb_99",
                "chat_instance": "12345",
                "data": f"cfm:{cand_id}"
            }
        }
        res_cb = self.adapter.handle_update(cb_update)
        self.assertEqual(res_cb["action"], "TRANSACTION_COMMITTED")
        self.assertEqual(res_cb["status"], "SUCCESS")
        self.assertIsNotNone(res_cb["transaction_id"])
        print("FLOW_TEST_09: PASS (Telegram Update dispatcher handles Message & CallbackQuery)")

    # ==========================================
    # 3. TRANSACTION PERSISTENCE & LEDGER TESTS
    # ==========================================
    def test_10_transaction_persistence_and_ledger_verification(self):
        # Input: "makan 35k bca"
        cand = self.adapter.stage_input("makan 35k bca")
        ok, tx, receipt = self.adapter.confirm_candidate(cand.candidate_id)
        
        self.assertTrue(ok)
        self.assertIsNotNone(tx)
        
        # 1. Verify Transaction attributes in Ledger
        read_tx = self.engine.get_transaction(tx.id)
        self.assertIsNotNone(read_tx)
        self.assertEqual(read_tx.amount, 35000.0)
        self.assertEqual(read_tx.direction, "EXPENSE")
        self.assertEqual(read_tx.source, "TELEGRAM")
        self.assertEqual(read_tx.account_id, self.acc_bca.id)
        self.assertEqual(read_tx.category_id, self.cat_food.id)
        
        # 2. Verify Balance Deduction
        bca_after = self.engine.get_account(self.acc_bca.id)
        # 1,500,000 - 35,000 = 1,465,000
        self.assertEqual(bca_after.balance, 1465000.0)
        
        # 3. Verify Audit Log
        audit_logs = self.engine.get_audit_logs()
        tx_audit = next((a for a in audit_logs if a.entity == "transactions" and a.entity_id == tx.id), None)
        self.assertIsNotNone(tx_audit)
        self.assertEqual(tx_audit.action, "CREATE")
        
        print("PERSISTENCE_TEST_10: PASS (Transaction, balance deduction, and audit log fully verified)")

if __name__ == "__main__":
    unittest.main()
