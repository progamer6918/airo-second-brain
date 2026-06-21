from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[2]
ACTIVE_APPS_SCRIPT = REPO_ROOT / "scripts" / "personal-workflow" / "apps-script" / "airo_finance_multitab_final_v1.gs"
AUDIT_DOC = REPO_ROOT / "docs" / "AIRO_FINANCE_SPRINT_5_DASHBOARD_ANALYTICS_AUDIT.md"


def read_source() -> str:
    return ACTIVE_APPS_SCRIPT.read_text(encoding="utf-8", errors="replace")


def read_audit_doc() -> str:
    return AUDIT_DOC.read_text(encoding="utf-8", errors="replace")


def extract_function(source: str, function_name: str) -> str:
    marker = f"function {function_name}("
    start = source.find(marker)
    if start < 0:
        raise AssertionError(f"Missing function: {function_name}")

    brace_start = source.find("{", start)
    if brace_start < 0:
        raise AssertionError(f"Missing opening brace for function: {function_name}")

    depth = 0
    for index in range(brace_start, len(source)):
        char = source[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return source[start : index + 1]

    raise AssertionError(f"Could not extract function body: {function_name}")


class DashboardAnalyticsContractTest(unittest.TestCase):
    def setUp(self):
        self.source = read_source()
        self.doc = read_audit_doc()

    def test_sprint5_audit_doc_exists_and_requires_test_first_contract(self):
        for expected in [
            "Status: EXACT AUDIT",
            "Sprint: Sprint 5 - Dashboard / Analytics",
            "No runtime patch is made in this micro-step.",
            "Add the smallest test-only Dashboard / Analytics contract.",
            "Dashboard / Analytics Surface Matrix",
        ]:
            self.assertIn(expected, self.doc)

    def test_monthly_review_and_cash_aktif_formulas_read_account_ledger(self):
        wrapper = extract_function(self.source, "refreshCashMonthlyReviewFormulas")
        body = extract_function(self.source, "refreshCashReportingFormulas")

        self.assertIn("return refreshCashReportingFormulas();", wrapper)

        for expected in [
            "monthlyCashInFormula",
            "monthlyCashOutFormula",
            "monthlyNetFormula",
            "dashboardCashAktifFormula",
            "monthly.getRange('B6').setFormula(monthlyCashInFormula)",
            "monthly.getRange('E6').setFormula(monthlyCashOutFormula)",
            "monthly.getRange('B8').setFormula(monthlyNetFormula)",
            "setFormulaOnCellContaining_(dashboard, ['cash aktif'], dashboardCashAktifFormula)",
            "Account Ledger'!D:D",
            "Account Ledger'!E:E",
            "FILTER",
            "SUMIFS",
        ]:
            self.assertIn(expected, body)

        self.assertNotIn("Cash Ledger'!", body)

    def test_dashboard_net_worth_panel_reads_account_ledger_and_aset_sources(self):
        body = extract_function(self.source, "setupDashboardNetWorthPanel")

        for expected in [
            "safeClearRange_(dashboard, 'B16:G24')",
            "dashboard.getRange('B16:G16').merge()",
            "dashboard.getRange('D17').setFormula",
            "dashboard.getRange('D19').setFormula('=IFERROR(D17-D18;0)')",
            "dashboard.getRange('D21').setFormula('=IFERROR(D19+D20;0)')",
            "Account Ledger",
            "SUMIFS",
            "Cash Umum",
            "Cash Bensin",
            "Aset'!B17",
            "Aset'!B18",
            "Aset'!AB21",
            "dashboard_panel: 'B16:G23'",
        ]:
            self.assertIn(expected, body)

        self.assertNotIn("Cash Ledger'!", body)

    def test_credit_card_cycle_dashboard_panel_is_present_but_not_refactored(self):
        body = extract_function(self.source, "setupDashboardCreditCardCyclePanel")

        for expected in [
            "safeClearRange_(dashboard, 'B25:G34')",
            "dashboard.getRange('B25:G25').merge()",
            "CREDIT CARD",
            "TOKOPEDIA CC",
            "Tagihan Jatuh Tempo",
            "Total Tagihan",
            "Belum ke Blu",
            "Periode Berjalan / Unbilled",
            "dashboard_panel: 'B25:G33'",
        ]:
            self.assertIn(expected, body)

    def test_dashboard_layout_read_only_audit_surface_is_present(self):
        body = extract_function(self.source, "dashboardLayoutReadOnlyAudit_")

        for expected in [
            "dashboard_sheet_missing",
            "Net Worth",
            "Credit Card",
            "Hutang",
            "Review Queue",
            "dashboard_layout_read_only_audit",
            "sheet_name: dashboard.getName()",
        ]:
            self.assertIn(expected, body)

    def test_finance_events_exists_but_dashboard_analytics_is_not_implemented_yet(self):
        for expected in [
            "financeEvents:",
            "function getFinanceEventsHeaders_(",
            "function writeFinanceEvent_(",
            "function recordFinanceEventForWriteResult_(",
        ]:
            self.assertIn(expected, self.source)

        forbidden_markers = [
            "function setupFinanceEventsAnalyticsPanel(",
            "function setupDashboardAnalyticsPanel(",
            "function refreshAnalyticsDashboard(",
            "function buildFinanceEventsDashboard(",
            "finance_events_analytics_refresh",
        ]

        for marker in forbidden_markers:
            self.assertNotIn(marker, self.source)

    def test_sprint4_finance_events_emission_scope_remains_write_routed_generic_only(self):
        write_routed = extract_function(self.source, "writeRouted_")

        self.assertIn("recordFinanceEventForWriteResult_(ss, result, common, parsed, rawText", write_routed)
        self.assertIn("event_type: 'transaction_created'", write_routed)
        self.assertIn("event_source: 'telegram'", write_routed)

        for function_name in [
            "doPost",
            "writeAccountLedgerMirror_",
            "processReviewQueueApproved",
            "writeInternalTransferToAccountLedger_",
            "writeCreditCardSafely_",
            "writeHutangSafely_",
            "writeAssetSafely_",
        ]:
            body = extract_function(self.source, function_name)
            for forbidden in [
                "recordFinanceEventForWriteResult_(",
                "writeFinanceEvent_(",
                "appendFinanceEvent_(",
                "emitFinanceEvent_(",
                "logFinanceEvent_(",
            ]:
                self.assertNotIn(forbidden, body, msg=f"Unexpected Finance Events emission in {function_name}")

    def test_no_email_ingestion_or_destructive_dashboard_change_is_present(self):
        forbidden_markers = [
            "GmailApp",
            "Gmail.Users",
            "MailApp",
            "getInboxThreads",
            "deleteSheet(",
            "deleteRows(",
        ]

        for marker in forbidden_markers:
            self.assertNotIn(marker, self.source)

    def test_audit_doc_defers_runtime_dashboard_analytics_changes(self):
        for expected in [
            "dashboard layout refactor",
            "formula rewrite",
            "chart creation",
            "analytics automation",
            "Finance Events event emission expansion",
            "Email Ingestion implementation",
            "destructive sheet or row operations",
        ]:
            self.assertIn(expected, self.doc)


if __name__ == "__main__":
    unittest.main()
