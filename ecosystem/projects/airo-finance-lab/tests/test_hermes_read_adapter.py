import os
import sys
import unittest

CORE_SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
if CORE_SRC not in sys.path:
    sys.path.insert(0, CORE_SRC)

from airo_finance_core import (
    DatabaseManager,
    FinanceCoreEngine,
    FinanceInsightsService,
    FinanceHermesReadAdapter
)

class TestHermesReadAdapter(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseManager(":memory:")
        self.db.init_schema()
        self.engine = FinanceCoreEngine(self.db)
        self.insights = FinanceInsightsService(self.db)
        self.adapter = FinanceHermesReadAdapter(self.insights)

        # Seed test accounts & categories
        self.acc_bca = self.engine.create_account("BCA Utama", "BANK", 2000000.0)
        self.acc_mandiri = self.engine.create_account("Mandiri", "BANK", 1000000.0)

        self.cat_food = self.engine.create_category("Makanan & Minuman")
        self.cat_transport = self.engine.create_category("Transportasi")
        self.cat_bills = self.engine.create_category("Tagihan & Utilitas")
        self.cat_income = self.engine.create_category("Gaji & Pemasukan")

        # Seed test transactions for 2026-09
        # Income: Rp8,000,000
        self.engine.create_transaction(self.acc_bca.id, 8000000.0, "INCOME", self.cat_income.id, "Gaji Bulanan", tx_date="2026-09-01")
        # Food: Rp120,000 (total food)
        self.engine.create_transaction(self.acc_bca.id, 70000.0, "EXPENSE", self.cat_food.id, "Makan Siang", tx_date="2026-09-02")
        self.engine.create_transaction(self.acc_bca.id, 50000.0, "EXPENSE", self.cat_food.id, "Makan Malam", tx_date="2026-09-03")
        # Transport: Rp30,000
        self.engine.create_transaction(self.acc_mandiri.id, 30000.0, "EXPENSE", self.cat_transport.id, "Bensin", tx_date="2026-09-04")
        # Large Bills expense: Rp1,500,000 (Trigger anomaly)
        self.engine.create_transaction(self.acc_bca.id, 1500000.0, "EXPENSE", self.cat_bills.id, "Servis Besar Laptop", tx_date="2026-09-05")

    def tearDown(self):
        self.db.close()

    # ==========================================
    # 1. ADAPTER UNIT TESTS
    # ==========================================
    def test_01_tool_spec_metadata(self):
        spec = self.adapter.get_hermes_tool_spec()
        self.assertEqual(spec["name"], "get_finance_insights")
        self.assertIn("description", spec)
        self.assertIn("parameters", spec)
        self.assertIn("query", spec["parameters"]["properties"])
        print("TEST_01_TOOL_SPEC: PASS (Valid schema metadata for Hermes tool definition)")

    def test_02_direct_monthly_spending_summary(self):
        res = self.adapter.get_monthly_spending_summary(2026, 9)
        self.assertEqual(res["intent"], FinanceHermesReadAdapter.INTENT_MONTHLY_SUMMARY)
        self.assertEqual(res["status"], "SUCCESS")
        data = res["data"]
        # Total expense = 70k + 50k + 30k + 1.5M = 1,650,000
        self.assertEqual(data["total_expense"], 1650000.0)
        self.assertEqual(data["total_income"], 8000000.0)
        self.assertEqual(data["net_cashflow"], 6350000.0) # 8M - 1.65M
        self.assertEqual(data["transaction_count"], 5)
        self.assertIn("Rp1.650.000", data["formatted_expense"])
        self.assertIn("Fakta Finansial", res["context_for_hermes"])
        print("TEST_02_DIRECT_SUMMARY: PASS (Monthly spending summary accurately returned)")

    def test_03_direct_top_category_spending(self):
        res = self.adapter.get_top_category_spending(2026, 9)
        self.assertEqual(res["intent"], FinanceHermesReadAdapter.INTENT_TOP_CATEGORY)
        self.assertEqual(res["status"], "SUCCESS")
        data = res["data"]
        # Bills is 1,500,000 out of 1,650,000 -> 90.91%
        self.assertEqual(data["top_category"], "Tagihan & Utilitas")
        self.assertEqual(data["amount"], 1500000.0)
        self.assertAlmostEqual(data["percentage"], 90.91, places=1)
        self.assertIn("Tagihan & Utilitas", res["context_for_hermes"])
        print("TEST_03_DIRECT_TOP_CATEGORY: PASS (Top category accurately identified with percentage)")

    def test_04_direct_spending_anomaly_check(self):
        res = self.adapter.get_spending_anomaly_check(2026, 9)
        self.assertEqual(res["intent"], FinanceHermesReadAdapter.INTENT_SPENDING_ANOMALY)
        self.assertEqual(res["status"], "SUCCESS")
        data = res["data"]
        self.assertTrue(data["has_anomaly"])
        self.assertGreaterEqual(data["anomaly_count"], 1)
        # Should detect large expense or category dominance
        types = [a["anomaly_type"] for a in data["anomalies"]]
        self.assertTrue("LARGE_EXPENSE" in types or "CATEGORY_DOMINANCE" in types)
        self.assertIn("Ditemukan", res["context_for_hermes"])
        print("TEST_04_DIRECT_ANOMALIES: PASS (Anomalies identified and context generated)")

    # ==========================================
    # 2. QUERY MAPPING & RESOLUTION TESTS
    # ==========================================
    def test_05_query_mapping_monthly_summary(self):
        queries = [
            "Berapa pengeluaran bulan ini?",
            "Pengeluaran bulan ini berapa ya?",
            "rekap bulan ini",
            "total belanja bulan ini",
            "cashflow bulan ini"
        ]
        for q in queries:
            intent = self.adapter.resolve_intent(q)
            self.assertEqual(intent, FinanceHermesReadAdapter.INTENT_MONTHLY_SUMMARY, f"Failed for query: {q}")
            res = self.adapter.handle_query(q, year=2026, month=9)
            self.assertEqual(res["status"], "SUCCESS")
            self.assertEqual(res["data"]["total_expense"], 1650000.0)
        print("TEST_05_QUERY_MAPPING_SUMMARY: PASS (5/5 variations mapped to MONTHLY_SPENDING_SUMMARY)")

    def test_06_query_mapping_top_category(self):
        queries = [
            "Kategori terbesar apa?",
            "kategori paling boros bulan ini",
            "top kategori pengeluaran",
            "belanja terbanyak di kategori mana",
            "kategori utama"
        ]
        for q in queries:
            intent = self.adapter.resolve_intent(q)
            self.assertEqual(intent, FinanceHermesReadAdapter.INTENT_TOP_CATEGORY, f"Failed for query: {q}")
            res = self.adapter.handle_query(q, year=2026, month=9)
            self.assertEqual(res["status"], "SUCCESS")
            self.assertEqual(res["data"]["top_category"], "Tagihan & Utilitas")
        print("TEST_06_QUERY_MAPPING_TOP_CAT: PASS (5/5 variations mapped to TOP_CATEGORY_SPENDING)")

    def test_07_query_mapping_anomaly_check(self):
        queries = [
            "Ada pengeluaran tidak biasa?",
            "ada anomali belanja?",
            "cek pengeluaran tak biasa",
            "ada yang boros tidak wajar?",
            "ada transaksi mencurigakan?"
        ]
        for q in queries:
            intent = self.adapter.resolve_intent(q)
            self.assertEqual(intent, FinanceHermesReadAdapter.INTENT_SPENDING_ANOMALY, f"Failed for query: {q}")
            res = self.adapter.handle_query(q, year=2026, month=9)
            self.assertEqual(res["status"], "SUCCESS")
            self.assertTrue(res["data"]["has_anomaly"])
        print("TEST_07_QUERY_MAPPING_ANOMALY: PASS (5/5 variations mapped to SPENDING_ANOMALY_CHECK)")

    def test_08_query_mapping_unsupported_intent(self):
        res = self.adapter.handle_query("jadwalkan alarm jam 7 pagi")
        self.assertEqual(res["intent"], FinanceHermesReadAdapter.INTENT_UNKNOWN)
        self.assertEqual(res["status"], "UNSUPPORTED")
        self.assertIn("MONTHLY_SPENDING_SUMMARY", res["supported_intents"])
        self.assertIn("tidak cocok", res["context_for_hermes"])
        print("TEST_08_UNSUPPORTED_QUERY: PASS (Non-finance queries handled gracefully without crash)")

    # ==========================================
    # 3. PERMISSION BOUNDARY & ZERO-WRITES TEST
    # ==========================================
    def test_09_strict_permission_boundary_zero_writes(self):
        # 1. Verify Adapter has zero write methods
        forbidden_methods = [
            "create_transaction",
            "update_account",
            "delete_transaction",
            "create_account",
            "write_ledger",
            "modify_budget"
        ]
        for method_name in forbidden_methods:
            self.assertFalse(
                hasattr(self.adapter, method_name),
                f"Security Breach: Adapter must NOT expose write method '{method_name}'"
            )

        # 2. Count records before running queries
        tx_count_before = len(self.engine.list_transactions())
        audit_count_before = len(self.engine.get_audit_logs())
        bca_balance_before = self.engine.get_account(self.acc_bca.id).balance

        # 3. Execute all query handlers multiple times
        self.adapter.handle_query("Berapa pengeluaran bulan ini?", 2026, 9)
        self.adapter.handle_query("Kategori terbesar apa?", 2026, 9)
        self.adapter.handle_query("Ada pengeluaran tidak biasa?", 2026, 9)
        self.adapter.handle_query("random unmapped text", 2026, 9)

        # 4. Verify ZERO mutations occurred
        tx_count_after = len(self.engine.list_transactions())
        audit_count_after = len(self.engine.get_audit_logs())
        bca_balance_after = self.engine.get_account(self.acc_bca.id).balance

        self.assertEqual(tx_count_before, tx_count_after, "Zero transaction writes allowed")
        self.assertEqual(audit_count_before, audit_count_after, "Zero audit mutations allowed")
        self.assertEqual(bca_balance_before, bca_balance_after, "Account balances remained untouched")

        print("TEST_09_PERMISSION_BOUNDARY: PASS (READ PASS, WRITE BLOCKED, 0 mutations verified)")

if __name__ == "__main__":
    unittest.main()
