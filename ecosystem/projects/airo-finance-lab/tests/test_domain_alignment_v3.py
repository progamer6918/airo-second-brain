import os
import sys
import unittest
import sqlite3

# Ensure paths
CORE_SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
if CORE_SRC not in sys.path:
    sys.path.insert(0, CORE_SRC)

from airo_finance_core.db import DatabaseManager
from airo_finance_core.engine import FinanceCoreEngine
from airo_finance_core.insights import FinanceInsightsService
from airo_finance_core.models import Asset, Liability, CreditCard

class TestFinancialDomainModelAlignmentV3(unittest.TestCase):
    def setUp(self):
        self.test_db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "test_domain_v3.db"))
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        self.db = DatabaseManager(self.test_db_path)
        self.db.init_schema()
        self.engine = FinanceCoreEngine(self.db)
        self.insights = FinanceInsightsService(self.db)

    def tearDown(self):
        self.db.close()
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    # 1. ACCOUNT HIERARCHY & SIBLING RULES
    def test_01_account_model_and_hierarchy(self):
        # Create Blu (BANK)
        blu = self.engine.create_account("Blu", "BANK", 67127.0)
        # Create Blu Gether (BANK / Container)
        blu_gether = self.engine.create_account("Blu Gether", "BANK", 4012809.0)
        # Create Blu Saving (POCKET under Blu Gether)
        blu_saving = self.engine.create_account("Blu Saving", "POCKET", 2164805.0, parent_account_id=blu_gether.id)
        # Create Blu Pocket CC (POCKET under Blu Gether, reserve/inactive)
        blu_pocket_cc = self.engine.create_account("Blu Pocket CC", "POCKET", 0.0, parent_account_id=blu_gether.id)
        self.engine.update_account(blu_pocket_cc.id, is_active=0) # inactive

        # Verifications
        self.assertEqual(blu.type, "BANK")
        self.assertIsNone(blu.parent_account_id)
        self.assertEqual(blu.balance, 67127.0)

        self.assertEqual(blu_gether.type, "BANK")
        self.assertIsNone(blu_gether.parent_account_id)
        self.assertEqual(blu_gether.balance, 4012809.0)

        # Sibling check under Blu Gether
        self.assertEqual(blu_saving.parent_account_id, blu_gether.id)
        self.assertEqual(blu_pocket_cc.parent_account_id, blu_gether.id)
        self.assertNotEqual(blu_saving.id, blu_pocket_cc.parent_account_id)
        self.assertNotEqual(blu_pocket_cc.id, blu_saving.parent_account_id)
        
        # Verify inactive
        pocket_cc_reloaded = self.engine.get_account(blu_pocket_cc.id)
        self.assertEqual(pocket_cc_reloaded.is_active, 0)

    # 2. INTERNAL TRANSFER RULES
    def test_02_transfer_rule(self):
        acc_a = self.engine.create_account("Acc A", "BANK", 5000000.0)
        acc_b = self.engine.create_account("Acc B", "BANK", 2000000.0)

        nw_before = self.insights.get_net_worth_report()
        self.assertEqual(nw_before.net_worth, 7000000.0)

        # Execute transfer of 1,000,000
        tx_out, tx_in = self.engine.transfer_funds(acc_a.id, acc_b.id, 1000000.0, note="Internal Transfer")
        
        acc_a_after = self.engine.get_account(acc_a.id)
        acc_b_after = self.engine.get_account(acc_b.id)
        self.assertEqual(acc_a_after.balance, 4000000.0)
        self.assertEqual(acc_b_after.balance, 3000000.0)

        nw_after = self.insights.get_net_worth_report()
        self.assertEqual(nw_after.net_worth, 7000000.0)
        self.assertEqual(nw_after.net_worth - nw_before.net_worth, 0.0)

        # Ensure expense and income deltas are 0
        conn = self.db.get_connection()
        expense_sum = conn.execute("SELECT SUM(amount) FROM transactions WHERE direction = 'EXPENSE'").fetchone()[0] or 0.0
        income_sum = conn.execute("SELECT SUM(amount) FROM transactions WHERE direction = 'INCOME'").fetchone()[0] or 0.0
        self.assertEqual(expense_sum, 0.0)
        self.assertEqual(income_sum, 0.0)

    # 3. CREDIT CARD PURCHASE RULES
    def test_03_cc_purchase_rule(self):
        cash_acc = self.engine.create_account("Checking", "BANK", 5000000.0)
        cc = self.engine.create_credit_card("Tokopedia Card", "BRI", 10000000.0, billing_cycle_day=15, payment_due_day=5)

        nw_before = self.insights.get_net_worth_report()

        # CC Purchase: Rp 500,000
        res = self.engine.record_credit_card_purchase(
            card_id=cc.id,
            amount=500000.0,
            category_id=None,
            note="Belanja Elektronik",
            tx_date="2026-09-13"
        )
        self.assertTrue(res["success"])
        tx = self.engine.get_transaction(res["transaction_id"])
        self.assertEqual(tx.direction, "EXPENSE")
        self.assertEqual(tx.amount, 500000.0)

        # Rule check: Cash accounts UNCHANGED
        cash_acc_after = self.engine.get_account(cash_acc.id)
        self.assertEqual(cash_acc_after.balance, 5000000.0)

        # Rule check: Credit Card liability increased
        cc_after = self.engine.get_credit_card(cc.id)
        self.assertEqual(cc_after.current_balance, 500000.0)
        cc_summary = self.engine.get_credit_card_summary(cc.id)
        self.assertEqual(cc_summary["unbilled_amount"], 500000.0)

        nw_after = self.insights.get_net_worth_report()
        # Cash account unchanged in liquid pool
        self.assertEqual(nw_after.total_liquid_balance, nw_before.total_liquid_balance)

    # 4. CREDIT CARD PAYMENT RULES
    def test_04_cc_payment_rule(self):
        cash_acc = self.engine.create_account("Checking", "BANK", 5000000.0)
        cc = self.engine.create_credit_card("Tokopedia Card", "BRI", 10000000.0, billing_cycle_day=15, payment_due_day=5)
        # Record purchase first
        self.engine.record_credit_card_purchase(cc.id, 1000000.0, category_id=None, note="Belanja", tx_date="2026-09-10")

        # Now pay credit card: Rp 1,000,000 from Checking
        pmt = self.engine.record_credit_card_payment(
            card_id=cc.id,
            amount=1000000.0,
            payment_date="2026-09-12",
            account_id=cash_acc.id,
            notes="Bayar CC Tokopedia"
        )

        # Rule check: Cash account reduced by payment
        cash_acc_after = self.engine.get_account(cash_acc.id)
        self.assertEqual(cash_acc_after.balance, 4000000.0)

        # Rule check: CC liability reduced by payment
        cc_after = self.engine.get_credit_card(cc.id)
        self.assertEqual(cc_after.current_balance, 0.0)

        # Rule check: NO DUPLICATE EXPENSE (payment must not increase expense)
        conn = self.db.get_connection()
        expenses = conn.execute("SELECT SUM(amount) FROM transactions WHERE direction = 'EXPENSE'").fetchone()[0] or 0.0
        # Only the original 1,000,000 purchase is expense, payment transaction is TRANSFER
        self.assertEqual(expenses, 1000000.0)

        # Credit Card Summary check
        summary = self.engine.get_credit_card_summary(cc.id)
        self.assertEqual(summary["card_id"], cc.id)
        self.assertEqual(summary["credit_limit"], 10000000.0)
        self.assertEqual(summary["current_balance"], 0.0)
        self.assertEqual(summary["payment_history_count"], 1)

    # 5. ASSET MODULE RULES
    def test_05_asset_rule(self):
        cash_acc = self.engine.create_account("Checking", "BANK", 100000000.0)
        nw_before = self.insights.get_net_worth_report()
        self.assertEqual(nw_before.net_worth, 100000000.0)

        # Asset Gold created
        gold = self.engine.create_asset(
            name="Emas Antam",
            asset_type="PRECIOUS_METAL",
            current_value=0.0,
            notes="50g Antam LM",
            asset_class="GOLD",
            weight_grams=0.0,
            purchase_cost=0.0,
            current_unit_price=1100000.0
        )

        # Buy Gold: Cash -55jt, Asset +55jt, Net worth unchanged
        res = self.engine.record_asset_purchase(
            account_id=cash_acc.id,
            asset_id=gold.id,
            amount=55000000.0,
            weight_grams=50.0,
            notes="Beli Emas Antam 50g",
            tx_date="2026-09-01"
        )
        self.assertTrue(res["success"])

        # Reload asset
        gold_reloaded = self.engine.get_asset(gold.id)
        # Verify all 7 required fields
        self.assertEqual(gold_reloaded.name, "Emas Antam")
        self.assertEqual(gold_reloaded.quantity_gram, 50.0)
        self.assertEqual(gold_reloaded.purchase_cost, 55000000.0)
        self.assertEqual(gold_reloaded.average_cost_per_gram, 1100000.0)
        self.assertEqual(gold_reloaded.current_value, 55000000.0)
        self.assertEqual(gold_reloaded.unrealized_gain_loss, 0.0)

        # Net worth preserved: Cash was 100jt -> Cash 45jt + Asset 55jt = 100jt
        nw_after = self.insights.get_net_worth_report()
        self.assertEqual(nw_after.total_liquid_balance, 45000000.0)
        self.assertEqual(nw_after.total_assets_value, 55000000.0)
        self.assertEqual(nw_after.net_worth, 100000000.0)

    # 6. GOLD VALUATION TRACKING RULES
    def test_06_gold_valuation_rule(self):
        gold = self.engine.create_asset(
            name="Emas Antam",
            asset_type="PRECIOUS_METAL",
            current_value=55000000.0,
            notes="50g Antam LM",
            asset_class="GOLD",
            weight_grams=50.0,
            purchase_cost=55000000.0,
            average_cost_per_gram=1100000.0,
            current_unit_price=1100000.0
        )

        conn = self.db.get_connection()
        tx_count_before = conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]

        # Daily gold price update to 1,500,000/g on 2026-09-13
        # 50g * 1,500,000 = 75,000,000
        val = self.engine.record_asset_valuation(
            asset_id=gold.id,
            valuation_date="2026-09-13",
            value=75000000.0,
            unit_price=1500000.0,
            reason="Daily market update 1.500.000/g"
        )

        # Rule check: Daily price update is NOT a transaction (0 rows in transactions)
        tx_count_after = conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
        self.assertEqual(tx_count_before, tx_count_after)

        # Valuation record exists in asset_valuation_history
        val_rows = conn.execute("SELECT * FROM asset_valuation_history WHERE asset_id = ?", (gold.id,)).fetchall()
        self.assertGreaterEqual(len(val_rows), 1)

        # Asset current value updated and unrealized gain calculated
        gold_updated = self.engine.get_asset(gold.id)
        self.assertEqual(gold_updated.current_value, 75000000.0)
        self.assertEqual(gold_updated.current_market_price, 1500000.0)
        self.assertEqual(gold_updated.unrealized_gain_loss, 20000000.0)

    # 7. MORTGAGE MODULE RULES
    def test_07_mortgage_rule(self):
        cash_acc = self.engine.create_account("Checking", "BANK", 10000000.0)
        mortgage = self.engine.create_liability(
            name="KPR Rumah",
            liability_type="MORTGAGE",
            original_amount=180000000.0,
            remaining_amount=42000000.0,
            monthly_payment=1500000.0,
            due_day=5
        )

        # Insert 57 historical payments to match reality
        for i in range(57):
            self.engine.record_liability_payment(
                liability_id=mortgage.id,
                payment_date=f"2022-{(i%12)+1:02d}-05",
                amount=1500000.0,
                notes=f"Angsuran ke-{i+1}"
            )

        # In current reality after 57 payments, remaining balance is 42,000,000
        self.engine.update_liability(mortgage.id, remaining_amount=42000000.0)

        # Check mortgage summary
        summary = self.engine.get_mortgage_summary(mortgage.id)
        self.assertEqual(summary["start_date"], "2022-01")
        self.assertEqual(summary["tenor_months"], 120)
        self.assertEqual(summary["paid_installments"], 57)
        self.assertEqual(summary["next_installment"], 58)

        # Advance 58th monthly payment: Rp 1,500,000 from Checking
        # Split is pending
        pmt = self.engine.advance_mortgage_payment(
            liability_id=mortgage.id,
            payment_date="2026-09-13",
            amount=1500000.0,
            account_id=cash_acc.id,
            notes="Angsuran ke-58"
        )

        # Cash reduced by 1.500.000
        cash_after = self.engine.get_account(cash_acc.id)
        self.assertEqual(cash_after.balance, 8500000.0)

        # Mortgage liability reduced by payment
        mort_after = self.engine.get_liability(mortgage.id)
        self.assertEqual(mort_after.remaining_amount, 40500000.0)

        # When principal/interest split is pending, payment must NOT be classified as full expense
        conn = self.db.get_connection()
        tx = conn.execute("SELECT direction FROM transactions WHERE id = ?", (pmt.transaction_id,)).fetchone()
        self.assertEqual(tx["direction"], "TRANSFER")

        # Now summary shows 58 paid, next 59
        summary_after = self.engine.get_mortgage_summary(mortgage.id)
        self.assertEqual(summary_after["paid_installments"], 58)
        self.assertEqual(summary_after["next_installment"], 59)

if __name__ == "__main__":
    unittest.main()
