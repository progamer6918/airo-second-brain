import os
import sys
import unittest
import tempfile

CORE_SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
if CORE_SRC not in sys.path:
    sys.path.insert(0, CORE_SRC)

from airo_finance_core import DatabaseManager, FinanceCoreEngine, FinanceInsightsService
from airo_finance_core.hermes_adapter import FinanceHermesReadAdapter

class TestHermesPhase3(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_hermes_p3.db")
        self.db = DatabaseManager(self.db_path)
        self.db.init_schema()
        self.engine = FinanceCoreEngine(self.db)
        self.insights = FinanceInsightsService(self.db)
        self.adapter = FinanceHermesReadAdapter(self.insights)

        # Seed test data
        self.acc = self.engine.create_account("BCA Utama", "BANK", 5000000.0)
        self.cat = self.engine.create_category("Utilitas", "pln, wifi")
        self.asset = self.engine.create_asset("Emas Batangan 10g", "GOLD", 14000000.0, "Disimpan aman")
        self.liab = self.engine.create_liability(
            name="Pinjaman Lunak",
            liability_type="LOAN",
            original_amount=10000000.0,
            remaining_amount=4000000.0,
            monthly_payment=1000000.0,
            due_day=20
        )
        self.obl = self.engine.create_fixed_obligation("Internet", 350000.0, due_day=10, category_id=self.cat.id)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_intent_resolution(self):
        # Net Worth
        self.assertEqual(self.adapter.resolve_intent("berapa kekayaan bersih saya"), FinanceHermesReadAdapter.INTENT_NET_WORTH)
        self.assertEqual(self.adapter.resolve_intent("cek net worth"), FinanceHermesReadAdapter.INTENT_NET_WORTH)
        self.assertEqual(self.adapter.resolve_intent("/networth"), FinanceHermesReadAdapter.INTENT_NET_WORTH)

        # Assets
        self.assertEqual(self.adapter.resolve_intent("tampilkan daftar aset saya"), FinanceHermesReadAdapter.INTENT_ASSETS)
        self.assertEqual(self.adapter.resolve_intent("ringkasan aset"), FinanceHermesReadAdapter.INTENT_ASSETS)
        self.assertEqual(self.adapter.resolve_intent("/assets"), FinanceHermesReadAdapter.INTENT_ASSETS)

        # Liabilities
        self.assertEqual(self.adapter.resolve_intent("berapa total utang saya"), FinanceHermesReadAdapter.INTENT_LIABILITIES)
        self.assertEqual(self.adapter.resolve_intent("daftar liabilitas"), FinanceHermesReadAdapter.INTENT_LIABILITIES)
        self.assertEqual(self.adapter.resolve_intent("posisi cicilan"), FinanceHermesReadAdapter.INTENT_LIABILITIES)
        self.assertEqual(self.adapter.resolve_intent("/liabilities"), FinanceHermesReadAdapter.INTENT_LIABILITIES)

        # Upcoming Commitments
        self.assertEqual(self.adapter.resolve_intent("daftar tagihan mendatang"), FinanceHermesReadAdapter.INTENT_UPCOMING_COMMITMENTS)
        self.assertEqual(self.adapter.resolve_intent("komitmen rutin bulan ini"), FinanceHermesReadAdapter.INTENT_UPCOMING_COMMITMENTS)
        self.assertEqual(self.adapter.resolve_intent("/commitments"), FinanceHermesReadAdapter.INTENT_UPCOMING_COMMITMENTS)

    def test_net_worth_facts_and_formatting(self):
        res = self.adapter.get_net_worth()
        self.assertEqual(res["intent"], FinanceHermesReadAdapter.INTENT_NET_WORTH)
        self.assertEqual(res["status"], "SUCCESS")
        
        # Net worth: 5jt (cash) + 14jt (asset) - 4jt (liab) = 15jt
        data = res["data"]
        self.assertEqual(data["net_worth"], 15000000.0)
        self.assertEqual(data["total_liquid_balance"], 5000000.0)
        self.assertEqual(data["total_assets_value"], 14000000.0)
        self.assertEqual(data["total_liabilities_remaining"], 4000000.0)

        card = self.adapter.format_net_worth_telegram_card()
        self.assertIn("Net Worth Report", card)
        self.assertIn("Rp15.000.000", card)
        self.assertIn("Kalkulasi deterministik Python murni", card)

    def test_assets_facts_and_formatting(self):
        res = self.adapter.get_assets_summary()
        self.assertEqual(res["intent"], FinanceHermesReadAdapter.INTENT_ASSETS)
        data = res["data"]
        self.assertEqual(data["total_assets_value"], 14000000.0)
        self.assertEqual(data["asset_count"], 1)

        card = self.adapter.format_assets_telegram_card()
        self.assertIn("Daftar & Ringkasan Aset", card)
        self.assertIn("Emas Batangan 10g", card)
        self.assertIn("Rp14.000.000", card)

    def test_liabilities_facts_and_formatting(self):
        res = self.adapter.get_liabilities_summary()
        self.assertEqual(res["intent"], FinanceHermesReadAdapter.INTENT_LIABILITIES)
        data = res["data"]
        self.assertEqual(data["total_liabilities_remaining"], 4000000.0)
        self.assertEqual(data["total_monthly_payment"], 1000000.0)

        card = self.adapter.format_liabilities_telegram_card()
        self.assertIn("Daftar & Ringkasan Liabilitas", card)
        self.assertIn("Pinjaman Lunak", card)
        self.assertIn("Rp4.000.000", card)

    def test_upcoming_commitments_facts_and_formatting(self):
        res = self.adapter.get_upcoming_commitments()
        self.assertEqual(res["intent"], FinanceHermesReadAdapter.INTENT_UPCOMING_COMMITMENTS)
        data = res["data"]
        self.assertEqual(data["total_obligations"], 350000.0)

        card = self.adapter.format_upcoming_commitments_telegram_card()
        self.assertIn("Upcoming Commitments", card)
        self.assertIn("Internet", card)
        self.assertIn("Rp350.000", card)

    def test_anti_eab_zero_write_boundary(self):
        # Count rows in all tables before calling hermes
        conn = self.db.get_connection()
        t_before = conn.execute("SELECT count(*) as c FROM transactions").fetchone()["c"]
        a_before = conn.execute("SELECT count(*) as c FROM assets").fetchone()["c"]
        l_before = conn.execute("SELECT count(*) as c FROM liabilities").fetchone()["c"]
        o_before = conn.execute("SELECT count(*) as c FROM fixed_obligations").fetchone()["c"]

        # Call all hermes read tools
        self.adapter.handle_query("berapa kekayaan bersih saya")
        self.adapter.handle_query("daftar aset")
        self.adapter.handle_query("daftar liabilitas")
        self.adapter.handle_query("tagihan rutin")
        self.adapter.handle_query("safe to spend")
        self.adapter.handle_query("rekap minggu ini")

        # Verify exact row counts unchanged
        t_after = conn.execute("SELECT count(*) as c FROM transactions").fetchone()["c"]
        a_after = conn.execute("SELECT count(*) as c FROM assets").fetchone()["c"]
        l_after = conn.execute("SELECT count(*) as c FROM liabilities").fetchone()["c"]
        o_after = conn.execute("SELECT count(*) as c FROM fixed_obligations").fetchone()["c"]

        self.assertEqual(t_before, t_after)
        self.assertEqual(a_before, a_after)
        self.assertEqual(l_before, l_after)
        self.assertEqual(o_before, o_after)

if __name__ == "__main__":
    unittest.main()
