import os
import sys
import time
import socket
import unittest
import threading
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from datetime import date, timedelta

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
    WeeklyRecapReport,
    LargestExpenseItem,
    DailySpendingItem
)
from app import get_engine, DashboardRequestHandler
from http.server import ThreadingHTTPServer

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


class TestWeeklyRecapPackageA(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "test_weekly_recap.db"))
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)

        cls.port = get_free_port()
        cls.engine = get_engine(cls.test_db_path)
        DashboardRequestHandler.engine = cls.engine

        cls.server = ThreadingHTTPServer(('127.0.0.1', cls.port), DashboardRequestHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()
        time.sleep(0.3)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.engine.db.close()
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)

    def setUp(self):
        # Fresh in-memory DB for pure unit testing
        self.mem_db = DatabaseManager(":memory:")
        self.mem_db.init_schema()
        self.mem_engine = FinanceCoreEngine(self.mem_db)
        self.mem_insights = FinanceInsightsService(self.mem_db)

        # Seed test accounts & categories
        self.acc_bca = self.mem_engine.create_account("BCA Utama", "BANK", 5000000.0)
        self.acc_mandiri = self.mem_engine.create_account("Mandiri Tabungan", "BANK", 2000000.0)
        self.cat_food = self.mem_engine.create_category("Makanan & Minuman")
        self.cat_transport = self.mem_engine.create_category("Transportasi")
        self.cat_bills = self.mem_engine.create_category("Tagihan")
        self.cat_salary = self.mem_engine.create_category("Gaji & Pemasukan")

    def tearDown(self):
        self.mem_db.close()

    # ----------------------------------------------------
    # 1. Empty Week Test
    # ----------------------------------------------------
    def test_01_empty_week(self):
        report = self.mem_insights.get_weekly_recap_report(as_of="2026-09-12")
        self.assertEqual(report.total_expense, 0.0)
        self.assertEqual(report.total_income, 0.0)
        self.assertEqual(report.net_cashflow, 0.0)
        self.assertEqual(report.daily_burn_rate, 0.0)
        self.assertEqual(report.expense_count, 0)
        self.assertEqual(report.income_count, 0)
        self.assertEqual(report.transfer_count, 0)
        self.assertIsNone(report.top_category_name)
        self.assertEqual(report.top_category_amount, 0.0)
        self.assertEqual(report.top_category_percentage, 0.0)
        self.assertIsNone(report.largest_expense)
        self.assertEqual(len(report.categories), 0)
        self.assertEqual(len(report.daily_breakdown), 7)
        self.assertEqual(report.start_date, "2026-09-06")
        self.assertEqual(report.end_date, "2026-09-12")
        print("EMPTY_WEEK_TEST: PASS (Clean zeros, no division errors, 7-day window valid)")

    # ----------------------------------------------------
    # 2. Normal Week Test
    # ----------------------------------------------------
    def test_02_normal_week_aggregation(self):
        # Window: 2026-09-06 to 2026-09-12
        # Income on 2026-09-07: Rp5,000,000
        self.mem_engine.create_transaction(self.acc_bca.id, 5000000.0, "INCOME", self.cat_salary.id, "Bonus", tx_date="2026-09-07")

        # Expenses:
        # Food: Rp100,000 (09-08), Rp150,000 (09-09) -> Total Food = 250,000
        self.mem_engine.create_transaction(self.acc_bca.id, 100000.0, "EXPENSE", self.cat_food.id, "Makan Siang", tx_date="2026-09-08")
        self.mem_engine.create_transaction(self.acc_bca.id, 150000.0, "EXPENSE", self.cat_food.id, "Makan Malam", tx_date="2026-09-09")

        # Transport: Rp50,000 (09-10) -> Total Transport = 50,000
        self.mem_engine.create_transaction(self.acc_mandiri.id, 50000.0, "EXPENSE", self.cat_transport.id, "Bensin", tx_date="2026-09-10")

        # Bills (Largest): Rp500,000 (09-11) -> Total Bills = 500,000
        self.mem_engine.create_transaction(self.acc_bca.id, 500000.0, "EXPENSE", self.cat_bills.id, "Tagihan Listrik", tx_date="2026-09-11")

        # Total Expense = 250k + 50k + 500k = 800,000
        # Net Cashflow = 5,000,000 - 800,000 = 4,200,000
        # Daily Burn Rate = 800,000 / 7 = 114285.71

        report = self.mem_insights.get_weekly_recap_report(as_of="2026-09-12")
        self.assertEqual(report.total_expense, 800000.0)
        self.assertEqual(report.total_income, 5000000.0)
        self.assertEqual(report.net_cashflow, 4200000.0)
        self.assertEqual(report.daily_burn_rate, round(800000.0 / 7.0, 2))
        self.assertEqual(report.expense_count, 4)
        self.assertEqual(report.income_count, 1)

        # Top category should be Bills (500k)
        self.assertEqual(report.top_category_name, "Tagihan")
        self.assertEqual(report.top_category_amount, 500000.0)
        expected_pct = round((500000.0 / 800000.0) * 100.0, 2)
        self.assertEqual(report.top_category_percentage, expected_pct)

        # Largest expense
        self.assertIsNotNone(report.largest_expense)
        self.assertEqual(report.largest_expense.amount, 500000.0)
        self.assertEqual(report.largest_expense.note, "Tagihan Listrik")
        self.assertEqual(report.largest_expense.date, "2026-09-11")

        print("NORMAL_WEEK_TEST: PASS (Expense/income aggregations, net cashflow, top category, and largest expense verified)")

    # ----------------------------------------------------
    # 3. Transfer Exclusion Test
    # ----------------------------------------------------
    def test_03_transfer_exclusion(self):
        # Expense of 100k
        self.mem_engine.create_transaction(self.acc_bca.id, 100000.0, "EXPENSE", self.cat_food.id, "Makan", tx_date="2026-09-10")
        # Transfer of 1,000,000 from BCA to Mandiri
        self.mem_engine.create_transaction(self.acc_bca.id, 1000000.0, "TRANSFER", None, "Pindah dana", tx_date="2026-09-11")

        report = self.mem_insights.get_weekly_recap_report(as_of="2026-09-12")
        self.assertEqual(report.total_expense, 100000.0, "Transfers must NEVER be added to total_expense")
        self.assertEqual(report.total_income, 0.0, "Transfers must NEVER be added to total_income")
        self.assertEqual(report.transfer_count, 1, "Transfer count tracked accurately")
        self.assertEqual(report.expense_count, 1)
        print("TRANSFER_EXCLUSION_TEST: PASS (Transfers tracked without inflating expenses or incomes)")

    # ----------------------------------------------------
    # 4. Date Rollover & Window Boundaries
    # ----------------------------------------------------
    def test_04_date_rollover_boundaries(self):
        # Month crossover: as_of="2026-09-03" -> 7 days rolling is 2026-08-28 to 2026-09-03
        # In-window: 2026-08-28 (boundary start), 2026-08-31, 2026-09-03 (boundary end)
        self.mem_engine.create_transaction(self.acc_bca.id, 50000.0, "EXPENSE", self.cat_food.id, "Tgl 28 Aug", tx_date="2026-08-28")
        self.mem_engine.create_transaction(self.acc_bca.id, 70000.0, "EXPENSE", self.cat_food.id, "Tgl 31 Aug", tx_date="2026-08-31")
        self.mem_engine.create_transaction(self.acc_bca.id, 80000.0, "EXPENSE", self.cat_food.id, "Tgl 3 Sep", tx_date="2026-09-03")

        # Out-of-window: 2026-08-27 (1 day too early), 2026-09-04 (1 day too late)
        self.mem_engine.create_transaction(self.acc_bca.id, 999999.0, "EXPENSE", self.cat_food.id, "Tgl 27 Aug (Out)", tx_date="2026-08-27")
        self.mem_engine.create_transaction(self.acc_bca.id, 999999.0, "EXPENSE", self.cat_food.id, "Tgl 4 Sep (Out)", tx_date="2026-09-04")

        report = self.mem_insights.get_weekly_recap_report(as_of="2026-09-03")
        self.assertEqual(report.start_date, "2026-08-28")
        self.assertEqual(report.end_date, "2026-09-03")
        self.assertEqual(report.total_expense, 200000.0)  # 50k + 70k + 80k
        self.assertEqual(report.expense_count, 3)

        # Year crossover: as_of="2026-01-03" -> 7 days rolling is 2025-12-28 to 2026-01-03
        year_report = self.mem_insights.get_weekly_recap_report(as_of="2026-01-03")
        self.assertEqual(year_report.start_date, "2025-12-28")
        self.assertEqual(year_report.end_date, "2026-01-03")
        print("DATE_ROLLOVER_TEST: PASS (Month transitions and year crossovers correctly bounded)")

    # ----------------------------------------------------
    # 5. SQL Numerical Match
    # ----------------------------------------------------
    def test_05_sql_numerical_exact_match(self):
        # Insert random mix of transactions
        self.mem_engine.create_transaction(self.acc_bca.id, 120000.0, "EXPENSE", self.cat_food.id, "M1", tx_date="2026-09-10")
        self.mem_engine.create_transaction(self.acc_bca.id, 230000.0, "EXPENSE", self.cat_transport.id, "M2", tx_date="2026-09-11")
        self.mem_engine.create_transaction(self.acc_bca.id, 1500000.0, "INCOME", self.cat_salary.id, "Gaji", tx_date="2026-09-12")

        report = self.mem_insights.get_weekly_recap_report(as_of="2026-09-12")

        # Independent SQL queries directly on conn
        conn = self.mem_db.get_connection()
        sql_exp = conn.execute(
            "SELECT SUM(amount) FROM transactions WHERE direction = 'EXPENSE' AND date >= '2026-09-06' AND date <= '2026-09-12'"
        ).fetchone()[0]
        sql_inc = conn.execute(
            "SELECT SUM(amount) FROM transactions WHERE direction = 'INCOME' AND date >= '2026-09-06' AND date <= '2026-09-12'"
        ).fetchone()[0]

        self.assertEqual(report.total_expense, float(sql_exp))
        self.assertEqual(report.total_income, float(sql_inc))
        self.assertEqual(report.net_cashflow, round(float(sql_inc) - float(sql_exp), 2))
        print("SQL_NUMERICAL_MATCH: PASS (100% exact match against independent raw SQL queries)")

    # ----------------------------------------------------
    # 6. Zero Database Writes / Ledger Integrity
    # ----------------------------------------------------
    def test_06_zero_writes_ledger_integrity(self):
        # Count records before
        tx_before = len(self.mem_engine.list_transactions())
        audit_before = len(self.mem_engine.get_audit_logs())
        acc_bca_bal_before = self.mem_engine.get_account(self.acc_bca.id).balance

        # Call get_weekly_recap_report multiple times
        for _ in range(5):
            self.mem_insights.get_weekly_recap_report(as_of="2026-09-12")

        # Count records after
        tx_after = len(self.mem_engine.list_transactions())
        audit_after = len(self.mem_engine.get_audit_logs())
        acc_bca_bal_after = self.mem_engine.get_account(self.acc_bca.id).balance

        self.assertEqual(tx_before, tx_after, "Zero transaction rows created")
        self.assertEqual(audit_before, audit_after, "Zero audit log rows created")
        self.assertEqual(acc_bca_bal_before, acc_bca_bal_after, "Account balances remained untouched")
        print("LEDGER_INTEGRITY_TEST: PASS (Strict read-only, 0 mutations verified)")

    # ----------------------------------------------------
    # 7. REST API Endpoint Test
    # ----------------------------------------------------
    def test_07_api_weekly_recap(self):
        url = f"http://127.0.0.1:{self.port}/api/insights/weekly-recap?as_of=2026-09-12"
        req = Request(url, method="GET")
        with urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            import json
            data = json.loads(resp.read().decode("utf-8"))
            self.assertIn("total_expense", data)
            self.assertIn("total_income", data)
            self.assertIn("net_cashflow", data)
            self.assertIn("daily_burn_rate", data)
            self.assertIn("start_date", data)
            self.assertIn("end_date", data)
            self.assertIn("daily_breakdown", data)
        print("API_WEEKLY_RECAP_TEST: PASS (GET /api/insights/weekly-recap returned 200 with schema)")

    # ----------------------------------------------------
    # 8. Latency Verification (< 150ms)
    # ----------------------------------------------------
    def test_08_latency_benchmark(self):
        start = time.perf_counter()
        for _ in range(20):
            self.mem_insights.get_weekly_recap_report(as_of="2026-09-12")
        elapsed_ms = ((time.perf_counter() - start) / 20.0) * 1000.0
        self.assertLess(elapsed_ms, 150.0, f"Latency {elapsed_ms:.2f}ms must be < 150ms")
        print(f"LATENCY_BENCHMARK: PASS ({elapsed_ms:.2f}ms per report calculation, well below 150ms threshold)")


if __name__ == "__main__":
    unittest.main()
