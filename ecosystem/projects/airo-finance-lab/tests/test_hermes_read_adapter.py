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
            "modify_budget",
            "create_obligation",
            "update_obligation",
            "delete_obligation",
            "set_finance_config"
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

    # ==========================================
    # 4. SAFE-TO-SPEND (PHASE 2.2) TESTS
    # ==========================================
    def test_10_safe_to_spend_factual_values(self):
        # Configure test obligations and safety floor via engine
        self.engine.create_fixed_obligation("Kost Bulanan", 1500000.0, due_day=15)
        self.engine.create_fixed_obligation("Internet & Wifi", 350000.0, due_day=20)
        self.engine.set_config("safety_floor", "1000000.0")
        self.engine.set_config("payday_day", "25")

        res = self.adapter.get_safe_to_spend_report(as_of="2026-09-10")
        self.assertEqual(res["intent"], FinanceHermesReadAdapter.INTENT_SAFE_TO_SPEND)
        self.assertEqual(res["status"], "SUCCESS")

        data = res["data"]
        # Required fields in prompt
        required_fields = [
            "liquid_balance",
            "unpaid_obligations",
            "safety_floor",
            "safe_to_spend",
            "payday_runway",
            "daily_allowance"
        ]
        for field in required_fields:
            self.assertIn(field, data, f"Missing required Safe-to-Spend field: {field}")

        # Verify factual values match insights
        raw_report = self.insights.get_safe_to_spend_report(as_of="2026-09-10")
        self.assertEqual(data["liquid_balance"], raw_report.total_liquid_balance)
        self.assertEqual(data["unpaid_obligations"], raw_report.unpaid_obligations_this_cycle)
        self.assertEqual(data["safety_floor"], raw_report.safety_floor)
        self.assertEqual(data["safe_to_spend"], raw_report.safe_to_spend)
        self.assertEqual(data["payday_runway"], raw_report.payday_runway_days)
        self.assertEqual(data["daily_allowance"], raw_report.daily_safe_allowance)

        # Context string check
        self.assertIn("Fakta Posisi Kas & Safe-to-Spend", res["context_for_hermes"])
        self.assertIn(res["data"]["formatted_safe_to_spend"], res["context_for_hermes"])
        print("TEST_10_SAFE_TO_SPEND_FACTUAL: PASS (All 6 core fields matched deterministic calculation)")

    def test_11_query_mapping_safe_to_spend(self):
        test_queries = [
            "berapa uang aman saya",
            "aman tidak sampai gajian",
            "safe to spend",
            "/safetospend",
            "sisa uang aman",
            "berapa sisa uang aman",
            "apakah aman belanja sampai gajian"
        ]
        for q in test_queries:
            intent = self.adapter.resolve_intent(q)
            self.assertEqual(
                intent,
                FinanceHermesReadAdapter.INTENT_SAFE_TO_SPEND,
                f"Query '{q}' should resolve to INTENT_SAFE_TO_SPEND"
            )
            res = self.adapter.handle_query(q)
            self.assertEqual(res["intent"], FinanceHermesReadAdapter.INTENT_SAFE_TO_SPEND)
            self.assertEqual(res["status"], "SUCCESS")
            self.assertIn("safe_to_spend", res["data"])
        print("TEST_11_QUERY_MAPPING_SAFE_TO_SPEND: PASS (7/7 queries mapped correctly)")

    def test_12_telegram_card_formatting(self):
        card = self.adapter.format_safe_to_spend_telegram_card(as_of="2026-09-10")
        self.assertIn("🛡️ <b>Safe-to-Spend Report</b>", card)
        self.assertIn("Saldo Kas Likuid:", card)
        self.assertIn("Tagihan Siklus Ini:", card)
        self.assertIn("Safety Floor:", card)
        self.assertIn("Safe-to-Spend:", card)
        self.assertIn("Jatah Harian:", card)
        self.assertIn("Sisa Hari s.d. Gajian:", card)
        self.assertIn("Payday Runway:", card)
        self.assertIn("Kalkulasi deterministik Python murni", card)
        self.assertNotIn("```", card)
        print("TEST_12_TELEGRAM_CARD_FORMAT: PASS (Compliant HTML single card generated)")

    def test_13_strict_permission_boundary_safe_to_spend(self):
        # 1. Count records before running queries
        tx_count_before = len(self.engine.list_transactions())
        audit_count_before = len(self.engine.get_audit_logs())
        bca_balance_before = self.engine.get_account(self.acc_bca.id).balance

        # 2. Execute safe-to-spend queries multiple times
        self.adapter.handle_query("berapa uang aman saya")
        self.adapter.handle_query("aman tidak sampai gajian")
        self.adapter.handle_query("safe to spend")
        self.adapter.get_safe_to_spend_report()
        self.adapter.format_safe_to_spend_telegram_card()

        # 3. Verify ZERO mutations
        tx_count_after = len(self.engine.list_transactions())
        audit_count_after = len(self.engine.get_audit_logs())
        bca_balance_after = self.engine.get_account(self.acc_bca.id).balance

        self.assertEqual(tx_count_before, tx_count_after, "Zero transaction writes allowed")
        self.assertEqual(audit_count_before, audit_count_after, "Zero audit mutations allowed")
        self.assertEqual(bca_balance_before, bca_balance_after, "Account balances remained untouched")
        print("TEST_13_SAFE_TO_SPEND_ZERO_WRITES: PASS (0 mutations across all Safe-to-Spend read paths)")

    def test_14_telegram_ingress_safetospend_route(self):
        from airo_finance_core.telegram_ingress import FinanceTelegramIngressRouter, TelegramOutboundAdapter

        sent_messages = []
        class MockOutbound(TelegramOutboundAdapter):
            def __init__(self):
                pass
            def send_message(self, chat_id, text, reply_markup=None, parse_mode="HTML"):
                sent_messages.append({"chat_id": chat_id, "text": text})
                return {"ok": True}

        mock_outbound = MockOutbound()
        router = FinanceTelegramIngressRouter(self.engine, outbound=mock_outbound, owner_chat_id="12345678")

        # Case 1: Owner triggers /safetospend
        update = {
            "update_id": 101,
            "message": {
                "message_id": 1,
                "chat": {"id": 12345678},
                "from": {"id": 12345678},
                "text": "/safetospend"
            }
        }
        handled, reason = router.handle_update(update)
        self.assertTrue(handled)
        self.assertEqual(reason, "SAFE_TO_SPEND_CARD_SENT")
        self.assertEqual(len(sent_messages), 1)
        self.assertIn("Safe-to-Spend Report", sent_messages[0]["text"])

        # Case 2: Non-owner triggers /safetospend
        non_owner_update = {
            "update_id": 102,
            "message": {
                "message_id": 2,
                "chat": {"id": 99999999},
                "from": {"id": 99999999},
                "text": "/safetospend"
            }
        }
        handled, reason = router.handle_update(non_owner_update)
        self.assertTrue(handled)
        self.assertEqual(reason, "BLOCKED_NON_OWNER_READ")
        self.assertIn("Akses Ditolak", sent_messages[-1]["text"])
        print("TEST_14_TELEGRAM_INGRESS_SAFETOSPEND: PASS (Authorized owner gets card, non-owner blocked)")

    # ==========================================
    # 5. WEEKLY RECAP (PHASE 2.3) TESTS
    # ==========================================
    def test_15_weekly_recap_factual_values(self):
        res = self.adapter.get_weekly_recap_report(as_of="2026-09-07")
        self.assertEqual(res["intent"], FinanceHermesReadAdapter.INTENT_WEEKLY_RECAP)
        self.assertEqual(res["status"], "SUCCESS")

        data = res["data"]
        raw = self.insights.get_weekly_recap_report(as_of="2026-09-07")

        # Factual value exact match
        self.assertEqual(data["total_expense"], raw.total_expense)
        self.assertEqual(data["total_income"], raw.total_income)
        self.assertEqual(data["net_cashflow"], raw.net_cashflow)
        self.assertEqual(data["daily_burn_rate"], raw.daily_burn_rate)
        self.assertEqual(data["top_category_name"], raw.top_category_name)
        self.assertEqual(data["total_liquid_balance"], raw.total_liquid_balance)
        self.assertEqual(data["safe_to_spend"], raw.safe_to_spend)

        # Context string check (Facts only, zero moralizing)
        self.assertIn("Fakta Rekap Finansial Mingguan", res["context_for_hermes"])
        self.assertIn(data["formatted_total_expense"], res["context_for_hermes"])
        self.assertIn(data["formatted_daily_burn_rate"], res["context_for_hermes"])
        print("TEST_15_WEEKLY_RECAP_FACTUAL: PASS (100% numerical match with raw insights report)")

    def test_16_query_mapping_weekly_recap(self):
        test_queries = [
            "rekap minggu ini",
            "evaluasi mingguan",
            "pengeluaran 7 hari terakhir",
            "/rekap",
            "/weekly",
            "weekly recap",
            "pengeluaran minggu ini"
        ]
        for q in test_queries:
            intent = self.adapter.resolve_intent(q)
            self.assertEqual(
                intent,
                FinanceHermesReadAdapter.INTENT_WEEKLY_RECAP,
                f"Query '{q}' should resolve to INTENT_WEEKLY_RECAP"
            )
            res = self.adapter.handle_query(q)
            self.assertEqual(res["intent"], FinanceHermesReadAdapter.INTENT_WEEKLY_RECAP)
            self.assertEqual(res["status"], "SUCCESS")
            self.assertIn("total_expense", res["data"])
            self.assertIn("daily_burn_rate", res["data"])
        print("TEST_16_QUERY_MAPPING_WEEKLY: PASS (7/7 queries mapped correctly to INTENT_WEEKLY_RECAP)")

    def test_17_weekly_recap_telegram_card_formatting(self):
        card = self.adapter.format_weekly_recap_telegram_card(as_of="2026-09-07")
        self.assertIn("📊 <b>Weekly Finance Recap</b>", card)
        self.assertIn("Total Belanja:", card)
        self.assertIn("Pemasukan:", card)
        self.assertIn("Net Cashflow:", card)
        self.assertIn("Rata-rata Harian:", card)
        self.assertIn("Kategori Terbesar:", card)
        self.assertIn("Transaksi Terbesar:", card)
        self.assertIn("Saldo Kas Likuid:", card)
        self.assertIn("Safe-to-Spend:", card)
        self.assertIn("Kalkulasi deterministik Python murni", card)
        self.assertNotIn("```", card)
        print("TEST_17_WEEKLY_TELEGRAM_CARD: PASS (Structured single HTML card with all required metrics)")

    def test_18_strict_zero_writes_weekly_recap(self):
        # 1. Count records before
        tx_before = len(self.engine.list_transactions())
        audit_before = len(self.engine.get_audit_logs())
        bca_bal_before = self.engine.get_account(self.acc_bca.id).balance

        # 2. Execute multiple weekly recap read paths
        self.adapter.handle_query("rekap minggu ini")
        self.adapter.handle_query("evaluasi mingguan")
        self.adapter.handle_query("pengeluaran 7 hari terakhir")
        self.adapter.get_weekly_recap_report()
        self.adapter.format_weekly_recap_telegram_card()

        # 3. Verify zero mutations
        tx_after = len(self.engine.list_transactions())
        audit_after = len(self.engine.get_audit_logs())
        bca_bal_after = self.engine.get_account(self.acc_bca.id).balance

        self.assertEqual(tx_before, tx_after, "Zero transaction writes allowed")
        self.assertEqual(audit_before, audit_after, "Zero audit mutations allowed")
        self.assertEqual(bca_bal_before, bca_bal_after, "Account balances remained untouched")
        print("TEST_18_WEEKLY_ZERO_WRITES: PASS (0 mutations across all Weekly Recap read paths)")

    def test_19_telegram_ingress_weekly_recap_route(self):
        from airo_finance_core.telegram_ingress import FinanceTelegramIngressRouter, TelegramOutboundAdapter

        sent_messages = []
        class MockOutbound(TelegramOutboundAdapter):
            def __init__(self):
                pass
            def send_message(self, chat_id, text, reply_markup=None, parse_mode="HTML"):
                sent_messages.append({"chat_id": chat_id, "text": text})
                return {"ok": True}

        mock_outbound = MockOutbound()
        router = FinanceTelegramIngressRouter(self.engine, outbound=mock_outbound, owner_chat_id="12345678")

        # Case 1: Owner triggers /rekap
        update = {
            "update_id": 201,
            "message": {
                "message_id": 10,
                "chat": {"id": 12345678},
                "from": {"id": 12345678},
                "text": "/rekap"
            }
        }
        handled, reason = router.handle_update(update)
        self.assertTrue(handled)
        self.assertEqual(reason, "WEEKLY_RECAP_CARD_SENT")
        self.assertEqual(len(sent_messages), 1)
        self.assertIn("Weekly Finance Recap", sent_messages[0]["text"])

        # Case 2: Non-owner triggers /weekly
        non_owner_update = {
            "update_id": 202,
            "message": {
                "message_id": 11,
                "chat": {"id": 99999999},
                "from": {"id": 99999999},
                "text": "/weekly"
            }
        }
        handled, reason = router.handle_update(non_owner_update)
        self.assertTrue(handled)
        self.assertEqual(reason, "BLOCKED_NON_OWNER_READ")
        self.assertIn("Akses Ditolak", sent_messages[-1]["text"])
        print("TEST_19_TELEGRAM_INGRESS_WEEKLY: PASS (Owner /rekap card delivered, non-owner blocked)")


if __name__ == "__main__":
    unittest.main()


