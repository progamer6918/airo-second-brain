import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from airo_finance_core import DatabaseManager, FinanceCoreEngine, FinanceInsightsService
from airo_finance_core.telegram_capture import SimpleTransactionParser, TelegramCaptureAdapter, format_idr

class TestPhase2TransferFoundation(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseManager(":memory:")
        self.db.init_schema()
        self.engine = FinanceCoreEngine(self.db)
        self.adapter = TelegramCaptureAdapter(self.engine)
        self.insights = FinanceInsightsService(self.db)

        # Seed initial accounts
        self.acc_bca = self.engine.create_account("BCA Utama", "BANK", 5000000.0)
        self.acc_blu = self.engine.create_account("Blu BCA", "BANK", 1000000.0)
        self.acc_mandiri = self.engine.create_account("Mandiri", "BANK", 500000.0)
        self.acc_cash = self.engine.create_account("Cash Dompet", "CASH", 200000.0)

        # Seed initial categories
        self.cat_food = self.engine.create_category("Makanan & Minuman")
        self.cat_salary = self.engine.create_category("Gaji & Pemasukan")

    def tearDown(self):
        self.db.close()

    def test_01_transfer_create_core_engine(self):
        """1. Transfer create test & ACID atomicity in core engine"""
        tx_out, tx_in = self.engine.transfer_funds(
            source_account_id=self.acc_bca.id,
            destination_account_id=self.acc_blu.id,
            amount=2000000.0,
            note="pindah tabungan",
            source="TEST"
        )
        
        self.assertIsNotNone(tx_out.id)
        self.assertIsNotNone(tx_in.id)
        self.assertEqual(tx_out.direction, "TRANSFER")
        self.assertEqual(tx_in.direction, "TRANSFER")
        self.assertEqual(tx_out.amount, 2000000.0)
        self.assertEqual(tx_in.amount, 2000000.0)
        self.assertEqual(tx_out.account_id, self.acc_bca.id)
        self.assertEqual(tx_in.account_id, self.acc_blu.id)

        # Verify Balances
        bca = self.engine.get_account(self.acc_bca.id)
        blu = self.engine.get_account(self.acc_blu.id)
        self.assertEqual(bca.balance, 3000000.0) # 5jt - 2jt
        self.assertEqual(blu.balance, 3000000.0) # 1jt + 2jt

        # Verify Audit Logs
        audits = self.engine.get_audit_logs(limit=10)
        actions = [a.action for a in audits]
        self.assertIn("TRANSFER_OUT", actions)
        self.assertIn("TRANSFER_IN", actions)
        print("TRANSFER_CREATE_CORE_TEST: PASS")

    def test_02_transfer_parser_and_intent_recognition(self):
        """2. Transfer parser recognition across diverse Indonesian phrasings"""
        parser = SimpleTransactionParser(self.engine)

        # Case A: "pindah 2000000 dari BCA ke Blu" (from user prompt)
        cand_a = parser.parse("pindah 2000000 dari BCA ke Blu")
        self.assertEqual(cand_a.direction, "TRANSFER")
        self.assertEqual(cand_a.amount, 2000000.0)
        self.assertEqual(cand_a.account_id, self.acc_bca.id)
        self.assertEqual(cand_a.destination_account_id, self.acc_blu.id)

        # Case B: "trf 500k bca ke mandiri"
        cand_b = parser.parse("trf 500k bca ke mandiri")
        self.assertEqual(cand_b.direction, "TRANSFER")
        self.assertEqual(cand_b.amount, 500000.0)
        self.assertEqual(cand_b.account_id, self.acc_bca.id)
        self.assertEqual(cand_b.destination_account_id, self.acc_mandiri.id)

        # Case C: "transfer 100rb cash ke bca"
        cand_c = parser.parse("transfer 100rb cash ke bca")
        self.assertEqual(cand_c.direction, "TRANSFER")
        self.assertEqual(cand_c.amount, 100000.0)
        self.assertEqual(cand_c.account_id, self.acc_cash.id)
        self.assertEqual(cand_c.destination_account_id, self.acc_bca.id)

        # Case D: Inverted phrasing: "pindah 1.5jt ke blu dari bca tabungan"
        cand_d = parser.parse("pindah 1.5jt ke blu dari bca tabungan")
        self.assertEqual(cand_d.direction, "TRANSFER")
        self.assertEqual(cand_d.amount, 1500000.0)
        self.assertEqual(cand_d.account_id, self.acc_bca.id)
        self.assertEqual(cand_d.destination_account_id, self.acc_blu.id)
        print("TRANSFER_PARSER_RECOGNITION_TEST: PASS")

    def test_03_transfer_confirmation_card_and_lifecycle(self):
        """3. Transfer confirmation card, cancel flow, and confirm flow"""
        cand = self.adapter.stage_input("pindah 2000000 dari BCA ke Blu")
        card = self.adapter.format_confirmation_card(cand)
        
        # Verify card presentation
        self.assertIn("Konfirmasi Transfer Dana", card["text"])
        self.assertIn("BCA Utama", card["text"])
        self.assertIn("Blu BCA", card["text"])
        self.assertIn("Rp2.000.000", card["text"])
        self.assertEqual(len(card["reply_markup"]["inline_keyboard"][0]), 3)
        self.assertTrue(card["reply_markup"]["inline_keyboard"][0][0]["callback_data"].startswith("cfm:"))
        self.assertTrue(card["reply_markup"]["inline_keyboard"][0][1]["callback_data"].startswith("ced:"))
        self.assertTrue(card["reply_markup"]["inline_keyboard"][0][2]["callback_data"].startswith("ccl:"))

        # Confirm Execution
        success, tx, receipt = self.adapter.confirm_candidate(cand.candidate_id)
        self.assertTrue(success)
        self.assertIsNotNone(tx)
        self.assertIn("Transfer Berhasil Dicatat!", receipt)
        self.assertIn("Rp3.000.000", receipt)  # updated balance

        # Verify idempotent confirmation
        dup_success, _, dup_err = self.adapter.confirm_candidate(cand.candidate_id)
        self.assertFalse(dup_success)
        self.assertIn("sudah pernah dicatat", dup_err)
        print("TRANSFER_CONFIRMATION_FLOW_TEST: PASS")

    def test_04_balance_reconciliation_and_net_position_invariant(self):
        """4. Balance reconciliation: Net position must remain UNCHANGED"""
        overview_before = self.insights.get_account_overview()
        total_initial = overview_before.total_liquid_balance
        self.assertEqual(total_initial, 6700000.0) # 5jt + 1jt + 500k + 200k

        # Execute 3 sequential transfers
        self.engine.transfer_funds(self.acc_bca.id, self.acc_blu.id, 1000000.0)
        self.engine.transfer_funds(self.acc_blu.id, self.acc_mandiri.id, 300000.0)
        self.engine.transfer_funds(self.acc_mandiri.id, self.acc_cash.id, 100000.0)

        overview_after = self.insights.get_account_overview()
        total_final = overview_after.total_liquid_balance

        # NET POSITION MUST BE UNCHANGED
        self.assertEqual(total_final, total_initial)
        self.assertEqual(total_final, 6700000.0)

        # Verify individual account mathematical accuracy
        bca = self.engine.get_account(self.acc_bca.id)
        blu = self.engine.get_account(self.acc_blu.id)
        mandiri = self.engine.get_account(self.acc_mandiri.id)
        cash = self.engine.get_account(self.acc_cash.id)

        self.assertEqual(bca.balance, 4000000.0)    # 5jt - 1jt
        self.assertEqual(blu.balance, 1700000.0)    # 1jt + 1jt - 300k
        self.assertEqual(mandiri.balance, 700000.0) # 500k + 300k - 100k
        self.assertEqual(cash.balance, 300000.0)    # 200k + 100k
        print("BALANCE_RECONCILIATION_NET_POSITION_TEST: PASS")

    def test_05_no_double_counting_and_expense_income_regression(self):
        """5. No double counting: Transfer is an asset movement, NOT expense, NOT income"""
        # Create 1 expense
        self.engine.create_transaction(
            account_id=self.acc_bca.id,
            amount=50000.0,
            direction="EXPENSE",
            category_id=self.cat_food.id,
            note="Makan siang"
        )

        # Create 1 income
        self.engine.create_transaction(
            account_id=self.acc_bca.id,
            amount=1000000.0,
            direction="INCOME",
            category_id=self.cat_salary.id,
            note="Bonus proyek"
        )

        # Create 1 transfer of Rp2.000.000
        self.engine.transfer_funds(
            source_account_id=self.acc_bca.id,
            destination_account_id=self.acc_blu.id,
            amount=2000000.0,
            note="Pindah ke tabungan"
        )

        # Evaluate Monthly Summary
        summary = self.insights.get_monthly_summary()
        self.assertEqual(summary.total_expense, 50000.0, "Transfer must NOT be counted in total_expense")
        self.assertEqual(summary.total_income, 1000000.0, "Transfer must NOT be counted in total_income")
        self.assertEqual(summary.net_cashflow, 950000.0, "Net cashflow must be income - expense (transfer is neutral)")

        # Evaluate Category Spending
        cat_report = self.insights.get_category_spending()
        self.assertEqual(cat_report.total_expense, 50000.0)
        self.assertEqual(len(cat_report.categories), 1)
        self.assertEqual(cat_report.categories[0].category_name, "Makanan & Minuman")
        self.assertEqual(cat_report.categories[0].total_amount, 50000.0)
        print("NO_DOUBLE_COUNTING_AND_REGRESSION_TEST: PASS")

    def test_06_edge_cases_and_error_handling(self):
        """6. Validation guards on invalid transfer attempts"""
        parser = SimpleTransactionParser(self.engine)

        # Same account transfer
        with self.assertRaises(ValueError) as ctx1:
            parser.parse("pindah 100k bca ke bca")
        self.assertIn("tidak boleh sama", str(ctx1.exception))

        # Missing destination account
        with self.assertRaises(ValueError) as ctx2:
            parser.parse("pindah 100k bca")
        self.assertIn("rekening tujuan", str(ctx2.exception))

        # Direct engine call with non-existent account
        with self.assertRaises(ValueError):
            self.engine.transfer_funds("acc_nonexistent", self.acc_blu.id, 100000.0)

        # Zero or negative amount
        with self.assertRaises(ValueError):
            self.engine.transfer_funds(self.acc_bca.id, self.acc_blu.id, 0.0)
        print("TRANSFER_EDGE_CASES_TEST: PASS")

if __name__ == "__main__":
    unittest.main()
