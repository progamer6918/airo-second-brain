import os
import sys
import unittest
import tempfile
import json
import sqlite3
from datetime import datetime, timezone

CORE_SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
if CORE_SRC not in sys.path:
    sys.path.insert(0, CORE_SRC)

from airo_finance_core import (
    DatabaseManager,
    FinanceCoreEngine,
    FinanceInsightsService,
    FinanceHermesReadAdapter
)
from airo_finance_core.telegram_capture import SimpleTransactionParser


class TestPhase31Alignment(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_phase3_1.db")
        self.db = DatabaseManager(self.db_path)
        self.db.init_schema()
        self.engine = FinanceCoreEngine(self.db)
        self.insights = FinanceInsightsService(self.db)
        self.hermes = FinanceHermesReadAdapter(self.insights)

        # Baseline accounts and categories
        self.acc_bca = self.engine.create_account("BCA Tabungan", "BANK", initial_balance=5000000)
        self.cat_food = self.engine.create_category("Makanan & Minuman")
        self.cat_transport = self.engine.create_category("Transportasi")

    def tearDown(self):
        self.db.close()
        self.temp_dir.cleanup()

    # ----------------------------------------------------
    # 1. Subcategories & Aliases
    # ----------------------------------------------------
    def test_subcategories_crud(self):
        sub1 = self.engine.create_subcategory(self.cat_food.id, "Kopi & Cafe")
        self.assertIsNotNone(sub1.id)
        self.assertEqual(sub1.name, "Kopi & Cafe")
        self.assertTrue(sub1.is_active)

        sub2 = self.engine.create_subcategory(self.cat_food.id, "Groceries & Warung")
        subs = self.engine.list_subcategories(category_id=self.cat_food.id)
        self.assertEqual(len(subs), 2)

        # Update
        updated = self.engine.update_subcategory(sub1.id, is_active=False)
        self.assertFalse(updated.is_active)

        # Unique constraint test
        with self.assertRaises((sqlite3.IntegrityError, Exception)):
            self.engine.create_subcategory(self.cat_food.id, "Groceries & Warung")

    def test_category_aliases_and_parser(self):
        alias1 = self.engine.add_category_alias("starbucks", category_id=self.cat_food.id)
        self.assertIsNotNone(alias1.id)

        # Lookup by keyword
        matched = self.engine.find_category_by_keyword("starbucks")
        self.assertIsNotNone(matched)
        self.assertEqual(matched["category_id"], self.cat_food.id)

        # Parser integration
        parser = SimpleTransactionParser(self.engine)
        parsed = parser.parse("50000 starbucks bca")
        self.assertEqual(parsed.amount, 50000.0)
        self.assertEqual(parsed.category_id, self.cat_food.id)

        # Delete alias
        self.assertTrue(self.engine.delete_category_alias(alias1.id))
        self.assertIsNone(self.engine.find_category_by_keyword("starbucks"))

    # ----------------------------------------------------
    # 2. Transaction Metadata & Corrections
    # ----------------------------------------------------
    def test_transaction_metadata_and_correction(self):
        tx = self.engine.create_transaction(
            account_id=self.acc_bca.id,
            amount=50000,
            direction="EXPENSE",
            category_id=self.cat_food.id,
            note="Makan siang",
            source="MANUAL"
        )
        # Add metadata
        sub = self.engine.create_subcategory(self.cat_food.id, "Restoran")
        meta = self.engine.record_transaction_metadata(
            transaction_id=tx.id,
            subcategory_id=sub.id,
            raw_input="Makan siang 50rb di restoran",
            source_type="MANUAL"
        )
        self.assertEqual(meta.subcategory_id, sub.id)

        read_meta = self.engine.get_transaction_metadata(tx.id)
        self.assertIsNotNone(read_meta)
        self.assertEqual(read_meta.subcategory_id, sub.id)

        # Correction
        corrected = self.engine.correct_transaction(
            transaction_id=tx.id,
            amount=60000,
            note="Makan siang berdua",
            reason="Salah input nominal"
        )
        self.assertEqual(corrected.amount, 60000.0)
        self.assertEqual(corrected.note, "Makan siang berdua")

        # Check correction event history
        events = self.engine.list_correction_events(transaction_id=tx.id)
        self.assertTrue(len(events) >= 1)
        reasons = [e.reason for e in events]
        self.assertIn("Salah input nominal", reasons)

    # ----------------------------------------------------
    # 3. Review Queue
    # ----------------------------------------------------
    def test_review_queue_approve_and_reject(self):
        # Item 1: to approve
        item1 = self.engine.enqueue_review_item(
            raw_text="beli bensin 50rb",
            parsed_result={
                "account_id": self.acc_bca.id,
                "amount": 50000,
                "direction": "EXPENSE",
                "category_id": self.cat_transport.id,
                "note": "Bensin"
            },
            issue_reason="Uncertain vehicle or account"
        )
        self.assertEqual(item1.status, "PENDING")

        pending_items = self.engine.list_review_queue(status="PENDING")
        self.assertEqual(len(pending_items), 1)

        # Approve item 1
        approved_item, tx = self.engine.approve_review_item(item1.id)
        self.assertEqual(approved_item.status, "APPROVED")
        self.assertIsNotNone(tx)
        self.assertEqual(tx.amount, 50000.0)
        self.assertEqual(tx.category_id, self.cat_transport.id)

        # Item 2: to reject
        item2 = self.engine.enqueue_review_item(
            raw_text="testing spam invalid",
            parsed_result={},
            issue_reason="Invalid format"
        )
        rejected_item = self.engine.reject_review_item(item2.id, reason="Spam message")
        self.assertEqual(rejected_item.status, "REJECTED")

        # Check queue counts
        self.assertEqual(len(self.engine.list_review_queue(status="PENDING")), 0)
        self.assertEqual(len(self.engine.list_review_queue(status="APPROVED")), 1)
        self.assertEqual(len(self.engine.list_review_queue(status="REJECTED")), 1)

    # ----------------------------------------------------
    # 4. Credit Cards Portfolio
    # ----------------------------------------------------
    def test_credit_card_operations(self):
        card = self.engine.create_credit_card(
            name="BCA Everyday Card",
            bank_name="BCA",
            credit_limit=15000000,
            account_id=self.acc_bca.id,
            billing_cycle_day=1,
            payment_due_day=20
        )
        self.assertIsNotNone(card.id)
        self.assertEqual(card.credit_limit, 15000000.0)

        # Statement
        stmt = self.engine.create_credit_card_statement(
            card_id=card.id,
            statement_period="2026-08",
            statement_date="2026-09-01",
            due_date="2026-09-20",
            total_amount=2500000,
            minimum_payment=250000
        )
        self.assertEqual(stmt.total_amount, 2500000.0)
        self.assertEqual(stmt.unpaid_amount, 2500000.0)

        # Update card balance to match usage
        self.engine.update_credit_card(card.id, current_balance=2500000.0)
        card_reloaded = self.engine.get_credit_card(card.id)
        self.assertEqual(card_reloaded.current_balance, 2500000.0)

        # Payment
        pmt = self.engine.record_credit_card_payment(
            card_id=card.id,
            payment_date="2026-09-10",
            amount=2500000,
            statement_id=stmt.id,
            notes="Pelunasan tagihan full"
        )
        self.assertEqual(pmt.amount, 2500000.0)

        # Card balance should now be 0, statement status PAID
        card_reloaded2 = self.engine.get_credit_card(card.id)
        self.assertEqual(card_reloaded2.current_balance, 0.0)

        stmts = self.engine.list_credit_card_statements(card.id)
        self.assertEqual(stmts[0].status, "PAID")
        self.assertEqual(stmts[0].unpaid_amount, 0.0)

    # ----------------------------------------------------
    # 5. Liability Payments & Asset Valuations
    # ----------------------------------------------------
    def test_liability_payments_and_asset_valuations(self):
        liab = self.engine.create_liability(
            name="KPR Mandiri",
            liability_type="MORTGAGE",
            original_amount=500000000,
            remaining_amount=480000000,
            monthly_payment=4500000,
            due_day=10
        )
        l_pmt = self.engine.record_liability_payment(
            liability_id=liab.id,
            payment_date="2026-09-10",
            amount=4500000,
            principal_portion=3000000,
            interest_portion=1500000,
            notes="Cicilan ke-12"
        )
        self.assertEqual(l_pmt.principal_portion, 3000000.0)
        liab_pmts = self.engine.list_liability_payments(liab.id)
        self.assertEqual(len(liab_pmts), 1)

        # Asset valuation
        ast = self.engine.create_asset("Saham BBCA", "INVESTMENT", 50000000)
        val = self.engine.record_asset_valuation(
            asset_id=ast.id,
            valuation_date="2026-09-12",
            value=52000000,
            reason="Kenaikan IHSG"
        )
        self.assertEqual(val.value, 52000000.0)
        vals = self.engine.list_asset_valuations(ast.id)
        self.assertEqual(len(vals), 1)

    # ----------------------------------------------------
    # 6. Insights & Hermes Adapter
    # ----------------------------------------------------
    def test_insights_and_hermes_read_adapter(self):
        # Create credit card & asset for financial position
        self.engine.create_credit_card("Mandiri CC", "Mandiri", 10000000, billing_cycle_day=5, payment_due_day=25)
        self.engine.create_asset("Emas Antam", "PHYSICAL", 25000000)

        # Financial position
        pos = self.insights.get_financial_position("2026-09-12")
        self.assertIn("net_worth", pos)
        self.assertEqual(pos["net_worth"]["total_liquid_balance"], 5000000.0)

        # Credit card summary
        cc_summary = self.insights.get_credit_card_summary()
        self.assertEqual(cc_summary["card_count"], 1)
        self.assertEqual(cc_summary["total_limit"], 10000000.0)

        # Hermes intent resolution & tool formatting
        intent_pos = self.hermes.resolve_intent("posisi keuangan saat ini")
        self.assertEqual(intent_pos, "FINANCIAL_POSITION")

        intent_cc = self.hermes.resolve_intent("status kartu kredit")
        self.assertEqual(intent_cc, "CREDIT_CARD_STATUS")

        intent_subcat = self.hermes.resolve_intent("pengeluaran per subkategori")
        self.assertEqual(intent_subcat, "SUBCATEGORY_SPENDING")

        # Hermes query response
        res_pos = self.hermes.handle_query("bagaimana posisi keuangan?")
        self.assertEqual(res_pos["status"], "SUCCESS")
        self.assertIn("Fakta Posisi Keuangan", res_pos["context_for_hermes"])

        # Hermes Telegram card formatting
        card_pos = self.hermes.format_financial_position_telegram_card()
        self.assertIn("Posisi Keuangan", card_pos)
        self.assertIn("Kekayaan Bersih", card_pos)

        card_cc = self.hermes.format_credit_card_telegram_card()
        self.assertIn("Portofolio Kartu Kredit", card_cc)


if __name__ == "__main__":
    unittest.main()
