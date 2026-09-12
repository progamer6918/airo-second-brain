import os
import sys
import unittest

# Ensure local package path is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from airo_finance_core import DatabaseManager, FinanceCoreEngine

class TestM1VerticalSlice(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseManager(":memory:")
        self.db.init_schema()
        self.engine = FinanceCoreEngine(self.db)

    def tearDown(self):
        self.db.close()

    def test_schema_tables_exist(self):
        conn = self.db.get_connection()
        cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = [r["name"] for r in cur.fetchall()]
        
        # Verify strictly the 5 MVP tables exist
        self.assertIn("accounts", tables)
        self.assertIn("categories", tables)
        self.assertIn("transactions", tables)
        self.assertIn("budgets", tables)
        self.assertIn("audit_logs", tables)
        print("SCHEMA_VALIDATION: PASS (5/5 tables verified)")

    def test_vertical_slice_transaction_lifecycle(self):
        # 1. Setup Master Data
        acc_bca = self.engine.create_account(name="BCA", account_type="BANK", initial_balance=1000000.0)
        self.assertIsNotNone(acc_bca.id)
        self.assertEqual(acc_bca.name, "BCA")
        self.assertEqual(acc_bca.balance, 1000000.0)
        
        cat_food = self.engine.create_category(name="Food")
        self.assertIsNotNone(cat_food.id)
        self.assertEqual(cat_food.name, "Food")
        
        # 2. CREATE TRANSACTION
        # Example Target: Rp35000, Food, BCA, Makan siang
        tx = self.engine.create_transaction(
            account_id=acc_bca.id,
            category_id=cat_food.id,
            amount=35000.0,
            direction="EXPENSE",
            note="Makan siang",
            source="MANUAL"
        )
        self.assertIsNotNone(tx.id)
        print(f"CREATE PASS: Transaction ID {tx.id} created successfully")

        # 3. READ TRANSACTION BACK
        read_tx = self.engine.get_transaction(tx.id)
        self.assertIsNotNone(read_tx)
        self.assertEqual(read_tx.id, tx.id)
        self.assertEqual(read_tx.amount, 35000.0)
        self.assertEqual(read_tx.account_id, acc_bca.id)
        self.assertEqual(read_tx.category_id, cat_food.id)
        self.assertEqual(read_tx.note, "Makan siang")
        self.assertEqual(read_tx.direction, "EXPENSE")
        self.assertEqual(read_tx.source, "MANUAL")
        print("READ PASS: Transaction readback exact match verified")

        # 4. DATA INTEGRITY PASS
        # Check updated account balance
        updated_acc = self.engine.get_account(acc_bca.id)
        expected_balance = 1000000.0 - 35000.0 # 965000.0
        self.assertEqual(updated_acc.balance, expected_balance)
        
        # Check audit log trail
        audit_logs = self.engine.get_audit_logs()
        tx_audits = [a for a in audit_logs if a.entity == "transactions" and a.entity_id == tx.id]
        self.assertEqual(len(tx_audits), 1)
        self.assertEqual(tx_audits[0].action, "CREATE")
        
        print(f"DATA INTEGRITY PASS: Balance updated correctly (1,000,000 -> {updated_acc.balance:,.0f}) and audit log logged")

    def test_income_transaction(self):
        acc = self.engine.create_account(name="Cash", account_type="CASH", initial_balance=50000.0)
        cat = self.engine.create_category(name="Salary")
        
        tx = self.engine.create_transaction(
            account_id=acc.id,
            category_id=cat.id,
            amount=200000.0,
            direction="INCOME",
            note="Freelance payment"
        )
        
        updated_acc = self.engine.get_account(acc.id)
        self.assertEqual(updated_acc.balance, 250000.0)
        print("INCOME_INTEGRITY: PASS")

if __name__ == "__main__":
    unittest.main()
