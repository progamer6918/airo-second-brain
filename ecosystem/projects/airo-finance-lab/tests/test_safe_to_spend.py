import os
import sys
import json
import time
import socket
import unittest
import threading
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from datetime import date

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
    FixedObligation,
    FinanceConfig,
    SafeToSpendReport
)
from app import get_engine, DashboardRequestHandler
from http.server import ThreadingHTTPServer

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]

class TestSafeToSpendPackageA(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "test_safe_to_spend.db"))
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

    # ----------------------------------------------------
    # 1. Database & Schema Migration Tests
    # ----------------------------------------------------
    def test_01_schema_migration_tables_exist(self):
        conn = self.engine.db.get_connection()
        cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('fixed_obligations', 'finance_config')")
        tables = {r["name"] for r in cur.fetchall()}
        self.assertIn("fixed_obligations", tables)
        self.assertIn("finance_config", tables)

        # Check default config values
        cur_cfg = conn.execute("SELECT key, value FROM finance_config")
        cfg_map = {r["key"]: r["value"] for r in cur_cfg.fetchall()}
        self.assertIn("safety_floor", cfg_map)
        self.assertIn("payday_day", cfg_map)
        self.assertEqual(cfg_map["payday_day"], "25")
        print("SCHEMA_TEST: PASS (fixed_obligations and finance_config tables verified with sane defaults)")

    # ----------------------------------------------------
    # 2. Fixed Obligations Engine CRUD Tests
    # ----------------------------------------------------
    def test_02_obligation_crud_and_validations(self):
        # 1. Create category for test
        cat = self.engine.create_category("Tagihan Utilitas")

        # 2. Create valid obligation
        obl = self.engine.create_fixed_obligation(
            name="Sewa Kos Bulanan",
            amount=1500000.0,
            due_day=15,
            category_id=cat.id
        )
        self.assertIsNotNone(obl.id)
        self.assertEqual(obl.name, "Sewa Kos Bulanan")
        self.assertEqual(obl.amount, 1500000.0)
        self.assertEqual(obl.due_day, 15)
        self.assertEqual(obl.is_active, 1)

        # 3. Validation errors
        with self.assertRaises(ValueError):
            self.engine.create_fixed_obligation("", 50000, 10)  # Empty name
        with self.assertRaises(ValueError):
            self.engine.create_fixed_obligation("Test", -100, 10)  # Non-positive amount
        with self.assertRaises(ValueError):
            self.engine.create_fixed_obligation("Test", 50000, 0)   # Invalid due day (0)
        with self.assertRaises(ValueError):
            self.engine.create_fixed_obligation("Test", 50000, 32)  # Invalid due day (32)

        # 4. Read back
        read_obl = self.engine.get_fixed_obligation(obl.id)
        self.assertIsNotNone(read_obl)
        self.assertEqual(read_obl.name, "Sewa Kos Bulanan")

        # 5. Update obligation
        updated = self.engine.update_fixed_obligation(obl.id, amount=1600000.0, due_day=16)
        self.assertEqual(updated.amount, 1600000.0)
        self.assertEqual(updated.due_day, 16)

        # 6. List obligations
        all_obls = self.engine.list_fixed_obligations(active_only=True)
        self.assertGreaterEqual(len(all_obls), 1)

        # 7. Audit log verification
        audit_logs = self.engine.get_audit_logs(limit=10)
        obl_audits = [a for a in audit_logs if a.entity == "fixed_obligations" and a.entity_id == obl.id]
        self.assertGreaterEqual(len(obl_audits), 2)  # CREATE and UPDATE
        print("OBLIGATION_CRUD_TEST: PASS (Validation, persistence, and audit logging verified)")

    # ----------------------------------------------------
    # 3. Finance Config Engine Tests
    # ----------------------------------------------------
    def test_03_config_management(self):
        # Read existing
        sf = self.engine.get_config("safety_floor")
        self.assertIsNotNone(sf)

        # Update
        self.engine.set_config("safety_floor", "1500000.0")
        self.assertEqual(self.engine.get_config("safety_floor"), "1500000.0")

        self.engine.set_config("payday_day", "28")
        self.assertEqual(self.engine.get_config("payday_day"), "28")

        # Reset to defaults for subsequent calculation tests
        self.engine.set_config("safety_floor", "1000000.0")
        self.engine.set_config("payday_day", "25")

        all_cfg = self.engine.get_all_config()
        self.assertEqual(all_cfg["safety_floor"], "1000000.0")
        self.assertEqual(all_cfg["payday_day"], "25")
        print("CONFIG_MANAGEMENT_TEST: PASS (Get, set, and bulk read verified)")

    # ----------------------------------------------------
    # 4. Deterministic Safe-to-Spend Calculation Tests
    # ----------------------------------------------------
    def test_04_safe_to_spend_deterministic_math(self):
        svc = FinanceInsightsService(self.engine.db)

        # Test case: as of 2026-09-12 (Payday is 25th -> 13 days to payday)
        report = svc.get_safe_to_spend_report(as_of="2026-09-12")
        self.assertIsInstance(report, SafeToSpendReport)
        self.assertEqual(report.as_of_date, "2026-09-12")
        self.assertEqual(report.payday_day, 25)
        self.assertEqual(report.days_to_payday, 13)
        self.assertEqual(report.safety_floor, 1000000.0)

        # In seeded database: Total liquid = 1500k + 500k + 250k + 100k = 2,350,000.0
        # Active obligation: Sewa Kos = 1,600,000.0
        # Net = 2,350,000 - 1,600,000 - 1,000,000 = -250,000 -> DEFICIT!
        self.assertEqual(report.status, "DEFICIT")
        self.assertEqual(report.safe_to_spend, 0.0)
        self.assertEqual(report.deficit_amount, 250000.0)
        self.assertEqual(report.daily_safe_allowance, 0.0)

        # Now record an income transaction of Rp 2.000.000 to turn it into SAFE
        acc = self.engine.get_account_by_name("BCA Utama")
        self.engine.create_transaction(
            account_id=acc.id,
            amount=2000000.0,
            direction="INCOME",
            note="Bonus Project",
            tx_date="2026-09-12"
        )

        # Now Total liquid = 4,350,000.0
        # Net = 4,350,000 - 1,600,000 - 1,000,000 = 1,750,000 -> SAFE!
        report_after = svc.get_safe_to_spend_report(as_of="2026-09-12")
        self.assertEqual(report_after.status, "SAFE")
        self.assertEqual(report_after.safe_to_spend, 1750000.0)
        self.assertEqual(report_after.deficit_amount, 0.0)
        self.assertEqual(report_after.daily_safe_allowance, round(1750000.0 / 13, 2))
        print("SAFE_TO_SPEND_MATH_TEST: PASS (Deficit clamping, daily allowance, and surplus transitions verified)")

    def test_05_obligation_paid_detection_in_cycle(self):
        svc = FinanceInsightsService(self.engine.db)
        acc = self.engine.get_account_by_name("BCA Utama")

        # Before paying Sewa Kos: unpaid = 1,600,000.0
        rep_before = svc.get_safe_to_spend_report(as_of="2026-09-12")
        self.assertEqual(rep_before.unpaid_obligations_this_cycle, 1600000.0)

        # Pay Sewa Kos via expense transaction matching the note or category
        self.engine.create_transaction(
            account_id=acc.id,
            amount=1600000.0,
            direction="EXPENSE",
            note="Bayar Sewa Kos Bulanan",
            tx_date="2026-09-12"
        )

        # After paying: Sewa Kos is marked PAID, unpaid = 0.0
        rep_after = svc.get_safe_to_spend_report(as_of="2026-09-12")
        self.assertEqual(rep_after.paid_obligations_this_cycle, 1600000.0)
        self.assertEqual(rep_after.unpaid_obligations_this_cycle, 0.0)

        kos_item = next(o for o in rep_after.obligations if "Kos" in o.name)
        self.assertTrue(kos_item.is_paid_this_cycle)
        self.assertEqual(kos_item.status, "PAID")
        print("OBLIGATION_PAID_DETECTION_TEST: PASS (Cycle matching correctly identifies fulfilled commitments)")

    def test_06_edge_cases_and_zero_division_guard(self):
        svc = FinanceInsightsService(self.engine.db)

        # Day of payday (e.g. 25th)
        rep_payday = svc.get_safe_to_spend_report(as_of="2026-09-25")
        self.assertGreaterEqual(rep_payday.days_to_payday, 1)

        # Leap year Feb 29
        rep_leap = svc.get_safe_to_spend_report(as_of="2024-02-29")
        self.assertIsNotNone(rep_leap.next_payday_date)

        # Month boundary Dec 31
        rep_eoy = svc.get_safe_to_spend_report(as_of="2026-12-31")
        self.assertIn("2027-01-25", rep_eoy.next_payday_date)
        print("EDGE_CASES_TEST: PASS (Payday boundary, leap year, and year crossover handled safely)")

    def test_07_ledger_integrity_zero_mutation_from_insight(self):
        svc = FinanceInsightsService(self.engine.db)
        conn = self.engine.db.get_connection()

        # Capture counts & balances before
        tx_count_before = conn.execute("SELECT count(*) as c FROM transactions").fetchone()["c"]
        audit_count_before = conn.execute("SELECT count(*) as c FROM audit_logs").fetchone()["c"]
        balance_before = conn.execute("SELECT sum(balance) as s FROM accounts").fetchone()["s"]

        # Run safe to spend multiple times
        for d in ["2026-09-01", "2026-09-12", "2026-09-25", "2026-09-30"]:
            svc.get_safe_to_spend_report(as_of=d)
        svc.get_full_insights_overview()

        # Capture counts & balances after
        tx_count_after = conn.execute("SELECT count(*) as c FROM transactions").fetchone()["c"]
        audit_count_after = conn.execute("SELECT count(*) as c FROM audit_logs").fetchone()["c"]
        balance_after = conn.execute("SELECT sum(balance) as s FROM accounts").fetchone()["s"]

        self.assertEqual(tx_count_before, tx_count_after)
        self.assertEqual(audit_count_before, audit_count_after)
        self.assertEqual(balance_before, balance_after)
        print("LEDGER_INTEGRITY_TEST: PASS (Zero mutations from insight service verified)")

    # ----------------------------------------------------
    # 5. REST API Integration Tests
    # ----------------------------------------------------
    def test_08_api_safe_to_spend_endpoint(self):
        url = f"http://127.0.0.1:{self.port}/api/insights/safe-to-spend?as_of=2026-09-12"
        with urlopen(url) as res:
            self.assertEqual(res.status, 200)
            data = json.loads(res.read().decode('utf-8'))
            self.assertIn("safe_to_spend", data)
            self.assertIn("status", data)
            self.assertIn("days_to_payday", data)
            self.assertIn("daily_safe_allowance", data)
            self.assertIn("obligations", data)
        print("API_SAFE_TO_SPEND_TEST: PASS (GET /api/insights/safe-to-spend returned 200 with schema)")

    def test_09_api_obligations_crud(self):
        # 1. GET /api/obligations
        url_get = f"http://127.0.0.1:{self.port}/api/obligations"
        with urlopen(url_get) as res:
            self.assertEqual(res.status, 200)
            data = json.loads(res.read().decode('utf-8'))
            self.assertIn("obligations", data)
            initial_count = len(data["obligations"])

        # 2. POST /api/obligations
        payload = {
            "name": "Paket Internet Rumah",
            "amount": 350000.0,
            "due_day": 20
        }
        req_post = Request(url_get, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'}, method='POST')
        with urlopen(req_post) as res:
            self.assertEqual(res.status, 200)
            data_post = json.loads(res.read().decode('utf-8'))
            self.assertTrue(data_post["success"])
            obl_id = data_post["obligation"]["id"]
            self.assertEqual(data_post["obligation"]["name"], "Paket Internet Rumah")

        # 3. PUT /api/obligations
        update_payload = {
            "id": obl_id,
            "amount": 375000.0,
            "is_active": 1
        }
        req_put = Request(url_get, data=json.dumps(update_payload).encode('utf-8'), headers={'Content-Type': 'application/json'}, method='PUT')
        with urlopen(req_put) as res:
            self.assertEqual(res.status, 200)
            data_put = json.loads(res.read().decode('utf-8'))
            self.assertTrue(data_put["success"])
            self.assertEqual(data_put["obligation"]["amount"], 375000.0)

        # 4. Verify count increment
        with urlopen(url_get) as res:
            data_after = json.loads(res.read().decode('utf-8'))
            self.assertEqual(len(data_after["obligations"]), initial_count + 1)
        print("API_OBLIGATIONS_CRUD_TEST: PASS (GET, POST, PUT /api/obligations verified)")

    def test_10_api_config_endpoints(self):
        url_cfg = f"http://127.0.0.1:{self.port}/api/config"

        # 1. GET /api/config
        with urlopen(url_cfg) as res:
            self.assertEqual(res.status, 200)
            data = json.loads(res.read().decode('utf-8'))
            self.assertIn("config", data)
            self.assertIn("safety_floor", data["config"])

        # 2. PUT /api/config
        put_payload = {
            "safety_floor": 1250000.0,
            "payday_day": 27
        }
        req_put = Request(url_cfg, data=json.dumps(put_payload).encode('utf-8'), headers={'Content-Type': 'application/json'}, method='PUT')
        with urlopen(req_put) as res:
            self.assertEqual(res.status, 200)
            data_put = json.loads(res.read().decode('utf-8'))
            self.assertTrue(data_put["success"])
            self.assertEqual(data_put["config"]["safety_floor"], "1250000.0")
            self.assertEqual(data_put["config"]["payday_day"], "27")

        # Reset
        reset_payload = {"safety_floor": 1000000.0, "payday_day": 25}
        req_reset = Request(url_cfg, data=json.dumps(reset_payload).encode('utf-8'), headers={'Content-Type': 'application/json'}, method='PUT')
        with urlopen(req_reset) as res:
            self.assertEqual(res.status, 200)
        print("API_CONFIG_TEST: PASS (GET, PUT /api/config verified)")

    def test_11_dashboard_ui_renders_safe_to_spend_components(self):
        url = f"http://127.0.0.1:{self.port}/"
        with urlopen(url) as res:
            self.assertEqual(res.status, 200)
            html = res.read().decode('utf-8')
            # Check for Phase 2.2 UI components
            self.assertIn("Safe-to-Spend Intelligence", html)
            self.assertIn("Uang Bebas Belanja", html)
            self.assertIn("Tambah Komitmen Rutin", html)
            self.assertIn("Parameter Keuangan", html)
            self.assertIn("Daftar Komitmen Rutin", html)
        print("DASHBOARD_SAFE_TO_SPEND_UI_TEST: PASS (Dashboard HTML includes all Safe-to-Spend widgets and forms)")

if __name__ == "__main__":
    unittest.main()
