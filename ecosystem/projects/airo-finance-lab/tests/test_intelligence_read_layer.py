import os
import sys
import json
import time
import socket
import unittest
import threading
from urllib.request import urlopen

# Ensure paths
CORE_SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
WEB_SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "../web"))
for p in [CORE_SRC, WEB_SRC]:
    if p not in sys.path:
        sys.path.insert(0, p)

from airo_finance_core import (
    DatabaseManager,
    FinanceCoreEngine,
    FinanceInsightsService,
    MonthlySummary,
    CategorySpendingReport,
    AccountOverview
)
from app import DashboardRequestHandler
from http.server import ThreadingHTTPServer

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]

class TestIntelligenceReadLayer(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseManager(":memory:")
        self.db.init_schema()
        self.engine = FinanceCoreEngine(self.db)
        self.insights = FinanceInsightsService(self.db)

    def tearDown(self):
        self.db.close()

    # ==========================================
    # 1. EMPTY DATABASE HANDLING TEST
    # ==========================================
    def test_01_empty_database_handling(self):
        # Empty DB (0 accounts, 0 transactions, 0 categories)
        summary = self.insights.get_monthly_summary(2026, 9)
        self.assertEqual(summary.total_income, 0.0)
        self.assertEqual(summary.total_expense, 0.0)
        self.assertEqual(summary.net_cashflow, 0.0)
        self.assertEqual(summary.transaction_count, 0)

        cat_spending = self.insights.get_category_spending(2026, 9)
        self.assertEqual(cat_spending.total_expense, 0.0)
        self.assertEqual(len(cat_spending.categories), 0)

        acc_overview = self.insights.get_account_overview()
        self.assertEqual(acc_overview.total_liquid_balance, 0.0)
        self.assertEqual(acc_overview.account_count, 0)
        self.assertEqual(len(acc_overview.accounts), 0)

        recent = self.insights.get_recent_activity(limit=10)
        self.assertEqual(len(recent), 0)

        anomalies = self.insights.get_spending_anomalies(2026, 9)
        self.assertEqual(len(anomalies), 0)

        full_ov = self.insights.get_full_insights_overview(2026, 9)
        self.assertIn("monthly_summary", full_ov)
        self.assertIn("category_spending", full_ov)
        print("TEST_01_EMPTY_DB: PASS (ZeroDivisionError prevented, clean zero/empty returns)")

    # ==========================================
    # 2. NUMERICAL ACCURACY TEST
    # ==========================================
    def test_02_numerical_accuracy_and_ledger_reconciliation(self):
        # Setup accounts
        acc_bca = self.engine.create_account("BCA Utama", "BANK", 1000000.0)
        acc_mandiri = self.engine.create_account("Mandiri", "BANK", 500000.0)
        
        # Setup categories
        cat_food = self.engine.create_category("Makanan & Minuman")
        cat_transport = self.engine.create_category("Transportasi")
        cat_income = self.engine.create_category("Gaji & Pemasukan")
        
        # Create transactions for 2026-09
        # Income: Rp5,000,000
        self.engine.create_transaction(acc_bca.id, 5000000.0, "INCOME", cat_income.id, "Gaji", tx_date="2026-09-01")
        
        # Expenses:
        # Food: 50k, 35k -> Total 85,000
        self.engine.create_transaction(acc_bca.id, 50000.0, "EXPENSE", cat_food.id, "Groceries", tx_date="2026-09-02")
        self.engine.create_transaction(acc_bca.id, 35000.0, "EXPENSE", cat_food.id, "Lunch", tx_date="2026-09-03")
        # Transport: 15k -> Total 15,000
        self.engine.create_transaction(acc_mandiri.id, 15000.0, "EXPENSE", cat_transport.id, "Gojek", tx_date="2026-09-04")
        
        # 1. Reconcile Monthly Summary
        summary = self.insights.get_monthly_summary(2026, 9)
        self.assertEqual(summary.total_income, 5000000.0)
        self.assertEqual(summary.total_expense, 100000.0)  # 50k + 35k + 15k
        self.assertEqual(summary.net_cashflow, 4900000.0)  # 5M - 100k
        self.assertEqual(summary.transaction_count, 4)

        # 2. Reconcile Category Spending Breakdown
        cat_rep = self.insights.get_category_spending(2026, 9)
        self.assertEqual(cat_rep.total_expense, 100000.0)
        self.assertEqual(len(cat_rep.categories), 2)
        
        food_cat = next(c for c in cat_rep.categories if c.category_name == "Makanan & Minuman")
        self.assertEqual(food_cat.total_amount, 85000.0)
        self.assertEqual(food_cat.percentage, 85.0)  # 85,000 / 100,000 * 100
        self.assertEqual(food_cat.transaction_count, 2)
        
        trans_cat = next(c for c in cat_rep.categories if c.category_name == "Transportasi")
        self.assertEqual(trans_cat.total_amount, 15000.0)
        self.assertEqual(trans_cat.percentage, 15.0)  # 15,000 / 100,000 * 100
        self.assertEqual(trans_cat.transaction_count, 1)

        # Total percentage check
        total_pct = sum(c.percentage for c in cat_rep.categories)
        self.assertAlmostEqual(total_pct, 100.0, places=1)

        # 3. Reconcile Accounts
        acc_ov = self.insights.get_account_overview()
        # BCA balance: 1M + 5M - 85k = 5,915,000
        # Mandiri balance: 500k - 15k = 485,000
        # Total: 6,400,000
        self.assertEqual(acc_ov.total_liquid_balance, 6400000.0)
        bca_item = next(a for a in acc_ov.accounts if a.account_name == "BCA Utama")
        self.assertEqual(bca_item.balance, 5915000.0)
        mandiri_item = next(a for a in acc_ov.accounts if a.account_name == "Mandiri")
        self.assertEqual(mandiri_item.balance, 485000.0)

        print("TEST_02_NUMERICAL_ACCURACY: PASS (100% exact match against ledger queries)")

    # ==========================================
    # 3. RECENT ACTIVITY ORDERING TEST
    # ==========================================
    def test_03_recent_activity_traceability(self):
        acc = self.engine.create_account("BCA", "BANK", 1000000.0)
        cat = self.engine.create_category("Food")

        tx1 = self.engine.create_transaction(acc.id, 10000.0, "EXPENSE", cat.id, "Tx 1", tx_date="2026-09-01")
        time.sleep(0.01)
        tx2 = self.engine.create_transaction(acc.id, 20000.0, "EXPENSE", cat.id, "Tx 2", tx_date="2026-09-02")
        time.sleep(0.01)
        tx3 = self.engine.create_transaction(acc.id, 30000.0, "EXPENSE", cat.id, "Tx 3", tx_date="2026-09-03")

        recent = self.insights.get_recent_activity(limit=2)
        self.assertEqual(len(recent), 2)
        # Most recent first
        self.assertEqual(recent[0].transaction_id, tx3.id)
        self.assertEqual(recent[0].amount, 30000.0)
        self.assertEqual(recent[1].transaction_id, tx2.id)
        self.assertEqual(recent[1].amount, 20000.0)
        print("TEST_03_RECENT_ACTIVITY: PASS (Correct chronological sorting and attribute traceability)")

    # ==========================================
    # 4. DETERMINISTIC ANOMALY DETECTION TEST
    # ==========================================
    def test_04_anomaly_detection_deterministic(self):
        acc = self.engine.create_account("BCA", "BANK", 10000000.0)
        cat_food = self.engine.create_category("Food")
        cat_bills = self.engine.create_category("Bills")

        # 3 normal food expenses (avg ~30k)
        self.engine.create_transaction(acc.id, 30000.0, "EXPENSE", cat_food.id, "Lunch 1", tx_date="2026-09-01")
        self.engine.create_transaction(acc.id, 25000.0, "EXPENSE", cat_food.id, "Lunch 2", tx_date="2026-09-02")
        self.engine.create_transaction(acc.id, 35000.0, "EXPENSE", cat_food.id, "Lunch 3", tx_date="2026-09-03")
        # 1 very large bill expense (2,500,000)
        large_tx = self.engine.create_transaction(acc.id, 2500000.0, "EXPENSE", cat_bills.id, "Emergency Repair", tx_date="2026-09-05")

        anomalies = self.insights.get_spending_anomalies(2026, 9)
        self.assertGreaterEqual(len(anomalies), 1)

        large_anom = next((a for a in anomalies if a.anomaly_type == "LARGE_EXPENSE"), None)
        self.assertIsNotNone(large_anom)
        self.assertEqual(large_anom.reference_id, large_tx.id)
        self.assertEqual(large_anom.metric_value, 2500000.0)

        dominance_anom = next((a for a in anomalies if a.anomaly_type == "CATEGORY_DOMINANCE"), None)
        self.assertIsNotNone(dominance_anom)
        self.assertEqual(dominance_anom.category_name, "Bills")
        self.assertGreater(dominance_anom.metric_value, 60.0)

        print("TEST_04_ANOMALIES: PASS (Deterministic detection of large expense and category dominance)")

    # ==========================================
    # 5. REST API ENDPOINT INTEGRATION TEST
    # ==========================================
    def test_05_rest_api_endpoints(self):
        port = get_free_port()
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "test_insights_api.db"))
        if os.path.exists(db_path):
            os.remove(db_path)

        test_db = DatabaseManager(db_path)
        test_db.init_schema()
        test_engine = FinanceCoreEngine(test_db)
        
        # Seed test data
        acc = test_engine.create_account("BCA", "BANK", 1000000.0)
        cat = test_engine.create_category("Food")
        test_engine.create_transaction(acc.id, 50000.0, "EXPENSE", cat.id, "Lunch", tx_date="2026-09-01")

        DashboardRequestHandler.engine = test_engine
        server = ThreadingHTTPServer(('127.0.0.1', port), DashboardRequestHandler)
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()
        time.sleep(0.3)

        try:
            # 1. GET /api/insights/monthly-summary
            with urlopen(f"http://127.0.0.1:{port}/api/insights/monthly-summary?year=2026&month=9") as res:
                self.assertEqual(res.status, 200)
                data = json.loads(res.read().decode('utf-8'))
                self.assertEqual(data["total_expense"], 50000.0)
                self.assertEqual(data["transaction_count"], 1)

            # 2. GET /api/insights/category-spending
            with urlopen(f"http://127.0.0.1:{port}/api/insights/category-spending?year=2026&month=9") as res:
                self.assertEqual(res.status, 200)
                data = json.loads(res.read().decode('utf-8'))
                self.assertEqual(data["total_expense"], 50000.0)
                self.assertEqual(len(data["categories"]), 1)

            # 3. GET /api/insights/account-overview
            with urlopen(f"http://127.0.0.1:{port}/api/insights/account-overview") as res:
                self.assertEqual(res.status, 200)
                data = json.loads(res.read().decode('utf-8'))
                self.assertEqual(data["total_liquid_balance"], 950000.0) # 1M - 50k

            # 4. GET /api/insights/overview
            with urlopen(f"http://127.0.0.1:{port}/api/insights/overview?year=2026&month=9") as res:
                self.assertEqual(res.status, 200)
                data = json.loads(res.read().decode('utf-8'))
                self.assertIn("monthly_summary", data)
                self.assertIn("category_spending", data)
                self.assertIn("account_overview", data)
                self.assertIn("recent_activity", data)
                self.assertIn("anomalies", data)

            print("TEST_05_REST_API: PASS (All /api/insights/* endpoints return verified numerical JSON)")
        finally:
            server.shutdown()
            server.server_close()
            test_db.close()
            if os.path.exists(db_path):
                os.remove(db_path)

if __name__ == "__main__":
    unittest.main()
