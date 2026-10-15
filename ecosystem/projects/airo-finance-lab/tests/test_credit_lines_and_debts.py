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
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CORE_SRC = os.path.join(REPO_ROOT, "src")
WEB_SRC = os.path.join(REPO_ROOT, "web")
for p in [CORE_SRC, WEB_SRC]:
    if p not in sys.path:
        sys.path.insert(0, p)

from airo_finance_core import (
    DatabaseManager,
    FinanceCoreEngine,
    FinanceInsightsService,
    CreditCard,
    CreditLineInstallment,
    Liability,
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

class TestCreditLinesAndDebts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "test_credit_lines_debts.db"))
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
            try:
                os.remove(cls.test_db_path)
            except Exception:
                pass

    def _url(self, path: str) -> str:
        return f"http://127.0.0.1:{self.port}{path}"

    def _get_json(self, path: str) -> dict:
        req = Request(self._url(path), headers={"Accept": "application/json"})
        with urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def _post_json(self, path: str, payload: dict) -> dict:
        data = json.dumps(payload).encode("utf-8")
        req = Request(self._url(path), data=data, headers={"Content-Type": "application/json"})
        with urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def _put_json(self, path: str, payload: dict) -> dict:
        data = json.dumps(payload).encode("utf-8")
        req = Request(self._url(path), data=data, headers={"Content-Type": "application/json"}, method="PUT")
        with urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))

    # ----------------------------------------------------
    # 1. Schema & Migration 008 Verification
    # ----------------------------------------------------
    def test_01_schema_migration_columns_and_tables(self):
        conn = self.engine.db.get_connection()
        
        # Check credit_cards columns
        cc_cols = {r["name"] for r in conn.execute("PRAGMA table_info(credit_cards)").fetchall()}
        self.assertIn("credit_type", cc_cols)
        self.assertIn("provider", cc_cols)
        self.assertIn("billing_model", cc_cols)
        self.assertIn("icon", cc_cols)

        # Check credit_line_installments table
        inst_cols = {r["name"] for r in conn.execute("PRAGMA table_info(credit_line_installments)").fetchall()}
        self.assertIn("id", inst_cols)
        self.assertIn("card_id", inst_cols)
        self.assertIn("description", inst_cols)
        self.assertIn("original_amount", inst_cols)
        self.assertIn("remaining_amount", inst_cols)
        self.assertIn("monthly_installment", inst_cols)
        self.assertIn("tenor_months", inst_cols)
        self.assertIn("remaining_tenor", inst_cols)
        self.assertIn("start_date", inst_cols)
        self.assertIn("next_due_date", inst_cols)
        self.assertIn("status", inst_cols)

        # Check liabilities columns
        liab_cols = {r["name"] for r in conn.execute("PRAGMA table_info(liabilities)").fetchall()}
        self.assertIn("lender_name", liab_cols)
        self.assertIn("repayment_type", liab_cols)
        self.assertIn("maturity_date", liab_cols)
        self.assertIn("interest_rate_annual", liab_cols)

    # ----------------------------------------------------
    # 2. Credit Line & PayLater Installment Engine CRUD
    # ----------------------------------------------------
    def test_02_credit_line_and_installment_crud(self):
        # Create Kredivo PayLater facility
        card = self.engine.create_credit_card(
            name="Kredivo PayLater",
            bank_name="Kredivo",
            credit_limit=6000000.0,
            billing_cycle_day=20,
            payment_due_day=5,
            credit_type="PAYLATER",
            provider="Kredivo",
            billing_model="PER_TRANSACTION_INSTALLMENT",
            icon="kredivo"
        )
        self.assertIsNotNone(card.id)
        self.assertEqual(card.credit_type, "PAYLATER")
        self.assertEqual(card.billing_model, "PER_TRANSACTION_INSTALLMENT")

        # Create installment
        inst = self.engine.create_credit_line_installment(
            card_id=card.id,
            description="Smart TV Xiaomi",
            original_amount=3000000.0,
            monthly_installment=1000000.0,
            tenor_months=3,
            start_date="2026-10-05",
            next_due_date="2026-10-05"
        )
        self.assertIsNotNone(inst.id)
        self.assertEqual(inst.description, "Smart TV Xiaomi")
        self.assertEqual(inst.monthly_installment, 1000000.0)
        self.assertEqual(inst.status, "ACTIVE")

        # Get installment
        fetched = self.engine.get_credit_line_installment(inst.id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.original_amount, 3000000.0)

        # List installments
        installments = self.engine.list_credit_line_installments(card_id=card.id)
        self.assertEqual(len(installments), 1)

        # Update status
        self.engine.update_credit_line_installment_status(inst.id, "COMPLETED")
        updated = self.engine.get_credit_line_installment(inst.id)
        self.assertEqual(updated.status, "COMPLETED")

    # ----------------------------------------------------
    # 3. Personal Debt CRUD & Non-Operational Loan Inflow
    # ----------------------------------------------------
    def test_03_personal_debt_and_loan_disbursement(self):
        # Create bank account for disbursement
        bank = self.engine.create_account(
            name="BCA Checking",
            account_type="BANK",
            initial_balance=5000000.0
        )
        self.assertEqual(bank.balance, 5000000.0)

        # Create liability with disbursement to BCA
        debt = self.engine.create_liability(
            name="Pinjaman Modal Kerja",
            liability_type="PERSONAL_LOAN",
            original_amount=10000000.0,
            remaining_amount=10000000.0,
            monthly_payment=2000000.0,
            due_day=15,
            lender_name="Om Hendra",
            repayment_type="INSTALLMENT",
            maturity_date="2027-03-15",
            interest_rate_annual=0.0,
            disbursement_account_id=bank.id
        )
        self.assertIsNotNone(debt.id)
        self.assertEqual(debt.lender_name, "Om Hendra")
        self.assertEqual(debt.repayment_type, "INSTALLMENT")

        # Verify bank balance increased from 5M to 15M
        refreshed_bank = self.engine.get_account(bank.id)
        self.assertEqual(refreshed_bank.balance, 15000000.0)

        # Verify loan disbursement is EXCLUDED from operational income in insights
        insights = FinanceInsightsService(self.engine.db)
        summary = insights.get_monthly_summary(date(2026, 9, 19))
        self.assertEqual(summary.total_income, 0.0, "Loan disbursement must NOT count as operational income!")

    # ----------------------------------------------------
    # 4. Atomic Debt Repayment
    # ----------------------------------------------------
    def test_04_atomic_debt_repayment(self):
        # Create bank account and debt
        bank = self.engine.create_account(
            name="Mandiri Utama",
            account_type="BANK",
            initial_balance=10000000.0
        )
        debt = self.engine.create_liability(
            name="Talangan Teman",
            liability_type="PERSONAL_LOAN",
            original_amount=4000000.0,
            remaining_amount=4000000.0,
            monthly_payment=1000000.0,
            due_day=20,
            lender_name="Rudi",
            repayment_type="INSTALLMENT"
        )
        self.assertEqual(debt.remaining_amount, 4000000.0)

        # Record repayment of 1,000,000 from Mandiri
        pmt = self.engine.record_liability_payment(
            liability_id=debt.id,
            amount=1000000.0,
            payment_date="2026-09-19",
            source_account_id=bank.id,
            principal_portion=1000000.0,
            interest_portion=0.0,
            notes="Cicilan 1/4"
        )
        self.assertIsNotNone(pmt.id)

        # Verify bank balance decreased by 1,000,000
        refreshed_bank = self.engine.get_account(bank.id)
        self.assertEqual(refreshed_bank.balance, 9000000.0)

        # Verify liability remaining amount decreased to 3,000,000
        refreshed_debt = self.engine.get_liability(debt.id)
        self.assertEqual(refreshed_debt.remaining_amount, 3000000.0)

    # ----------------------------------------------------
    # 5. Multi-Card Shortage Isolation (Zero Cross-Card Subsidy)
    # ----------------------------------------------------
    def test_05_safe_to_spend_isolation_no_cross_card_subsidy(self):
        # Clean setup for isolation test
        # Create Liquid Account
        main_bank = self.engine.create_account(name="BCA Operasional", account_type="BANK", initial_balance=10000000.0)

        # Card A: Limit used 3M, Reserve 2M -> Shortage = 1M
        card_a = self.engine.create_credit_card(name="Card A", bank_name="Bank BCA", credit_limit=10000000.0, billing_cycle_day=20, payment_due_day=10)
        reserve_a = self.engine.create_account(
            name="Reserve Card A",
            account_type="BANK",
            initial_balance=2000000.0,
            account_class="RESERVE",
            reserve_target_id=card_a.id,
            parent_account_id=main_bank.id
        )
        # Create statement for Card A with 3M unpaid
        self.engine.create_credit_card_statement(
            card_id=card_a.id,
            statement_period="2026-09",
            total_amount=3000000.0,
            statement_date="2026-09-20",
            due_date="2026-10-10"
        )

        # Card B: Limit used 1M, Reserve 3M (Surplus 2M) -> Shortage = 0
        card_b = self.engine.create_credit_card(name="Card B", bank_name="Bank BCA", credit_limit=10000000.0, billing_cycle_day=20, payment_due_day=10)
        reserve_b = self.engine.create_account(
            name="Reserve Card B",
            account_type="BANK",
            initial_balance=3000000.0,
            account_class="RESERVE",
            reserve_target_id=card_b.id,
            parent_account_id=main_bank.id
        )
        # Create statement for Card B with 1M unpaid
        self.engine.create_credit_card_statement(
            card_id=card_b.id,
            statement_period="2026-09",
            total_amount=1000000.0,
            statement_date="2026-09-20",
            due_date="2026-10-10"
        )

        insights = FinanceInsightsService(self.engine.db)
        report = insights.get_safe_to_spend_report(as_of_date=date(2026, 9, 21))

        # Check dedicated reserves and uncovered CC debt:
        self.assertGreaterEqual(report.dedicated_reserve, 5000000.0)

        # Check CC Shortage:
        # Card A shortage = 3M - 2M = 1M
        # Card B shortage = max(0, 1M - 3M) = 0
        # Total shortage MUST be 1,000,000! Card B's surplus 2M must NOT offset Card A's shortage!
        self.assertEqual(report.uncovered_cc_debt, 1000000.0)

    # ----------------------------------------------------
    # 6. Anti-Double-Count in Cycle Obligations & PayLater
    # ----------------------------------------------------
    def test_06_cycle_obligations_anti_double_count_and_paylater(self):
        # Set config payday to 25
        self.engine.set_config("payday_day", "25")

        # Create liability due on day 24 (before payday)
        debt = self.engine.create_liability(
            name="Cicilan Koperasi",
            liability_type="PERSONAL_LOAN",
            original_amount=6000000.0,
            remaining_amount=6000000.0,
            monthly_payment=1000000.0,
            due_day=24,
            repayment_type="INSTALLMENT"
        )

        # Before payment: obligations includes 1M
        insights = FinanceInsightsService(self.engine.db)
        report_before = insights.get_safe_to_spend_report(as_of_date=date(2026, 9, 21))
        koperasi_obls = [o for o in report_before.obligations if "Cicilan Koperasi" in o.name]
        self.assertEqual(len(koperasi_obls), 1)
        self.assertEqual(koperasi_obls[0].amount, 1000000.0)
        self.assertEqual(koperasi_obls[0].status, "UNPAID")

        # Pay 600,000 on 2026-09-22
        bank = self.engine.list_accounts()[0]
        self.engine.record_liability_payment(
            liability_id=debt.id,
            amount=600000.0,
            payment_date="2026-09-22",
            source_account_id=bank.id,
            principal_portion=600000.0,
            interest_portion=0.0
        )

        # After partial payment: cycle obligations status reflects payment
        report_after = insights.get_safe_to_spend_report(as_of_date=date(2026, 9, 22))
        koperasi_obls_after = [o for o in report_after.obligations if "Cicilan Koperasi" in o.name]
        self.assertEqual(len(koperasi_obls_after), 1)
        self.assertFalse(koperasi_obls_after[0].is_paid_this_cycle)

    # ----------------------------------------------------
    # 7. HTTP API Endpoints for Credit Lines & Debts
    # ----------------------------------------------------
    def test_07_http_api_endpoints(self):
        # 1. GET /api/credit-lines
        lines_resp = self._get_json("/api/credit-lines")
        self.assertIn("cards", lines_resp)
        self.assertIsInstance(lines_resp["cards"], list)

        # 2. POST /api/credit-lines
        new_card_resp = self._post_json("/api/credit-lines", {
            "name": "Shopee PayLater",
            "bank_name": "Shopee",
            "credit_limit": 4000000,
            "billing_cycle_day": 25,
            "payment_due_day": 5,
            "credit_type": "PAYLATER",
            "provider": "Shopee",
            "billing_model": "PER_TRANSACTION_INSTALLMENT",
            "icon": "shopee"
        })
        self.assertTrue(new_card_resp.get("success", False))
        card_data = new_card_resp["card"]
        self.assertIn("id", card_data)
        self.assertEqual(card_data["provider"], "Shopee")

        # 3. GET /api/debts
        debts_resp = self._get_json("/api/debts")
        self.assertIn("debts", debts_resp)
        self.assertIsInstance(debts_resp["debts"], list)

        # 4. POST /api/debts
        new_debt_resp = self._post_json("/api/debts", {
            "name": "Pinjaman Sepupu",
            "original_amount": 2000000,
            "monthly_payment": 500000,
            "due_day": 12,
            "lender_name": "Doni",
            "repayment_type": "INSTALLMENT"
        })
        self.assertTrue(new_debt_resp.get("success", False))
        debt_data = new_debt_resp["debt"]
        self.assertIn("id", debt_data)
        self.assertEqual(debt_data["lender_name"], "Doni")

        # 5. POST /api/debts/<id>/pay
        bank = self.engine.list_accounts()[0]
        pay_res = self._post_json(f"/api/debts/{debt_data['id']}/pay", {
            "amount": 500000,
            "payment_date": "2026-09-19",
            "source_account_id": bank.id,
            "notes": "Cicilan 1 Doni"
        })
        self.assertTrue(pay_res.get("success", False))

        # 6. POST /api/credit-lines/<id>/installments
        inst_res = self._post_json(f"/api/credit-lines/{card_data['id']}/installments", {
            "description": "Headphones Sony",
            "original_amount": 1500000,
            "monthly_installment": 500000,
            "tenor_months": 3,
            "start_date": "2026-10-05",
            "next_due_date": "2026-11-05"
        })
        self.assertTrue(inst_res.get("success", False))
        inst_data = inst_res["installment"]
        self.assertEqual(inst_data["monthly_installment"], 500000.0)

        # 7. GET /api/dashboard contains credit_lines and debts
        dash = self._get_json("/api/dashboard")
        self.assertIn("credit_lines", dash)
        self.assertIn("debts", dash)

    # ----------------------------------------------------
    # 8. Credit Line Statement Lifecycle & 'stmt_new' Fallback
    # ----------------------------------------------------
    def test_08_credit_line_statement_lifecycle_and_fallback(self):
        # Create new credit line with 0 statements
        card_res = self._post_json("/api/credit-lines", {
            "name": "Kredivo Bayar 30 Hari",
            "provider": "Kredivo",
            "credit_type": "PAYLATER",
            "billing_model": "STATEMENT_CYCLE",
            "credit_limit": 10900000,
            "billing_cycle_day": 19,
            "payment_due_day": 19
        })
        self.assertTrue(card_res.get("success", False))
        card_id = card_res["card"]["id"]

        # Detail initially has 0 statements
        detail_0 = self._get_json(f"/api/credit-lines/{card_id}/detail")
        self.assertEqual(len(detail_0["statements"]), 0)

        # 1. Post statement with statement_id="stmt_new" (Previously caused ValueError "Statement stmt_new tidak ditemukan")
        res1 = self._post_json(f"/api/credit-lines/{card_id}/update-statement", {
            "card_id": card_id,
            "statement_id": "stmt_new",
            "total_amount": 4502940,
            "unpaid_amount": 4502940,
            "statement_period": "19 Sep 2026 - 19 Okt 2026",
            "statement_date": "2026-09-19",
            "due_date": "2026-10-19",
            "status": "ISSUED"
        })
        self.assertTrue(res1.get("success", False))
        self.assertIn("statement_id", res1)
        created_stmt_id_1 = res1["statement_id"]
        self.assertTrue(created_stmt_id_1.startswith(f"stmt_{card_id}_"))

        # Verify in detail
        detail_1 = self._get_json(f"/api/credit-lines/{card_id}/detail")
        self.assertEqual(len(detail_1["statements"]), 1)
        self.assertEqual(detail_1["statements"][0]["total_amount"], 4502940.0)

        # 2. Update existing statement
        res2 = self._post_json(f"/api/credit-lines/{card_id}/update-statement", {
            "card_id": card_id,
            "statement_id": created_stmt_id_1,
            "total_amount": 4600000,
            "unpaid_amount": 4600000,
            "statement_period": "19 Sep 2026 - 19 Okt 2026 (Updated)",
            "statement_date": "2026-09-19",
            "due_date": "2026-10-19",
            "status": "ISSUED"
        })
        self.assertTrue(res2.get("success", False))
        self.assertEqual(res2["statement_id"], created_stmt_id_1)

        detail_2 = self._get_json(f"/api/credit-lines/{card_id}/detail")
        self.assertEqual(len(detail_2["statements"]), 1)
        self.assertEqual(detail_2["statements"][0]["total_amount"], 4600000.0)
        self.assertEqual(detail_2["statements"][0]["statement_period"], "19 Sep 2026 - 19 Okt 2026 (Updated)")

        # 3. Post new statement with statement_id="new"
        res3 = self._post_json(f"/api/credit-lines/{card_id}/update-statement", {
            "card_id": card_id,
            "statement_id": "new",
            "total_amount": 1200000,
            "unpaid_amount": 1200000,
            "statement_period": "19 Okt 2026 - 19 Nov 2026",
            "statement_date": "2026-10-19",
            "due_date": "2026-11-19",
            "status": "ISSUED"
        })
        self.assertTrue(res3.get("success", False))
        created_stmt_id_2 = res3["statement_id"]
        self.assertNotEqual(created_stmt_id_1, created_stmt_id_2)

        detail_3 = self._get_json(f"/api/credit-lines/{card_id}/detail")
        self.assertEqual(len(detail_3["statements"]), 2)

        print("\nALL CREDIT LINES & PERSONAL DEBTS TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    unittest.main()

