import os
import sys
import unittest
import tempfile

CORE_SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
if CORE_SRC not in sys.path:
    sys.path.insert(0, CORE_SRC)

from airo_finance_core import DatabaseManager, FinanceCoreEngine, FinanceInsightsService
from airo_finance_core.telegram_capture import SimpleTransactionParser

class TestOwnerRegistries(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_registries.db")
        self.db = DatabaseManager(self.db_path)
        self.db.init_schema()
        self.engine = FinanceCoreEngine(self.db)
        self.insights = FinanceInsightsService(self.db)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_account_registry_crud(self):
        acc = self.engine.create_account("Bank Jago", "BANK", 250000.0)
        self.assertEqual(acc.name, "Bank Jago")
        self.assertEqual(acc.is_active, 1)

        # Rename account
        updated = self.engine.update_account(acc.id, name="Bank Jago Syariah")
        self.assertEqual(updated.name, "Bank Jago Syariah")

        # Archive account
        archived = self.engine.update_account(acc.id, is_active=0)
        self.assertEqual(archived.is_active, 0)

        # Active only filtering
        active_list = self.engine.list_accounts(active_only=True)
        self.assertNotIn(acc.id, [a.id for a in active_list])

        all_list = self.engine.list_accounts(active_only=False)
        self.assertIn(acc.id, [a.id for a in all_list])

    def test_category_registry_and_keywords(self):
        cat = self.engine.create_category("Streaming", "netflix, spotify, youtube, disney")
        self.assertEqual(cat.name, "Streaming")
        self.assertIn("netflix", cat.keywords)

        # Test Parser dynamic keyword mapping
        acc = self.engine.create_account("BCA", "BANK", 1000000.0)
        parser = SimpleTransactionParser(self.engine)

        cand = parser.parse("bayar netflix 186k pake bca")
        self.assertEqual(cand.amount, 186000.0)
        self.assertEqual(cand.category_name, "Streaming")

        # Update keywords
        updated_cat = self.engine.update_category(cat.id, keywords="netflix, spotify, wetv")
        self.assertIn("wetv", updated_cat.keywords)

    def test_asset_registry_crud_and_net_worth(self):
        acc = self.engine.create_account("BCA", "BANK", 10000000.0)
        
        # Add Asset
        asset = self.engine.create_asset("Emas Antam 10g", "GOLD", 14000000.0, "Disimpan di brankas")
        self.assertEqual(asset.current_value, 14000000.0)

        # Net worth before liability: Cash (10jt) + Asset (14jt) = 24jt
        nw = self.insights.get_net_worth_report()
        self.assertEqual(nw.total_liquid_balance, 10000000.0)
        self.assertEqual(nw.total_assets_value, 14000000.0)
        self.assertEqual(nw.total_liabilities_remaining, 0.0)
        self.assertEqual(nw.net_worth, 24000000.0)

        # Revalue Asset
        self.engine.update_asset(asset.id, current_value=15000000.0)
        nw2 = self.insights.get_net_worth_report()
        self.assertEqual(nw2.total_assets_value, 15000000.0)
        self.assertEqual(nw2.net_worth, 25000000.0)

        # Delete Asset
        deleted = self.engine.delete_asset(asset.id)
        self.assertTrue(deleted)
        nw3 = self.insights.get_net_worth_report()
        self.assertEqual(nw3.total_assets_value, 0.0)
        self.assertEqual(nw3.net_worth, 10000000.0)

    def test_liability_registry_crud_and_net_worth(self):
        acc = self.engine.create_account("BCA", "BANK", 20000000.0)
        asset = self.engine.create_asset("Mobil Bekas", "VEHICLE", 100000000.0)

        # Add Liability
        liab = self.engine.create_liability(
            name="Cicilan Mobil",
            liability_type="AUTO",
            original_amount=80000000.0,
            remaining_amount=60000000.0,
            monthly_payment=3000000.0,
            due_day=15,
            notes="Tenor sisa 20 bulan"
        )
        self.assertEqual(liab.remaining_amount, 60000000.0)
        self.assertEqual(liab.monthly_payment, 3000000.0)

        # Net Worth: Liquid (20jt) + Asset (100jt) - Liability (60jt) = 60jt
        nw = self.insights.get_net_worth_report()
        self.assertEqual(nw.net_worth, 60000000.0)
        self.assertEqual(nw.monthly_liability_payments, 3000000.0)

        # Update remaining
        self.engine.update_liability(liab.id, remaining_amount=57000000.0)
        nw2 = self.insights.get_net_worth_report()
        self.assertEqual(nw2.total_liabilities_remaining, 57000000.0)
        self.assertEqual(nw2.net_worth, 63000000.0)

        # Delete liability
        self.engine.delete_liability(liab.id)
        nw3 = self.insights.get_net_worth_report()
        self.assertEqual(nw3.total_liabilities_remaining, 0.0)
        self.assertEqual(nw3.net_worth, 120000000.0)

if __name__ == "__main__":
    unittest.main()
