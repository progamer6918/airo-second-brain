from pathlib import Path
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[2]
ACTIVE_APPS_SCRIPT = REPO_ROOT / "scripts" / "personal-workflow" / "apps-script" / "airo_finance_multitab_final_v1.gs"


def read_source() -> str:
    return ACTIVE_APPS_SCRIPT.read_text(encoding="utf-8", errors="replace")


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


class DashboardMonthlyCashReadContractTest(unittest.TestCase):
    def setUp(self):
        self.source = read_source()

    def test_monthly_cash_refresh_wrapper_delegates_to_reporting_formula_writer(self):
        wrapper = extract_function(self.source, "refreshCashMonthlyReviewFormulas")

        self.assertIn("return refreshCashReportingFormulas();", wrapper)

    def test_reporting_formulas_write_monthly_b6_e6_b8_from_account_ledger(self):
        body = extract_function(self.source, "refreshCashReportingFormulas")

        for expected in [
            "monthlyCashInFormula",
            "monthlyCashOutFormula",
            "monthlyNetFormula",
            "monthly.getRange('B6').setFormula(monthlyCashInFormula)",
            "monthly.getRange('E6').setFormula(monthlyCashOutFormula)",
            "monthly.getRange('B8').setFormula(monthlyNetFormula)",
            "Account Ledger",
            "Account Ledger'!D:D",
            "Account Ledger'!E:E",
            "FILTER",
            "TO_TEXT($B$2)",
        ]:
            self.assertIn(expected, body)

        self.assertNotIn("Cash Ledger'!", body)

    def test_dashboard_cash_aktif_formula_reads_account_ledger_not_cash_ledger(self):
        body = extract_function(self.source, "refreshCashReportingFormulas")

        for expected in [
            "dashboardCashAktifFormula",
            "setFormulaOnCellContaining_(dashboard, ['cash aktif'], dashboardCashAktifFormula)",
            "SUMIFS",
            "Account Ledger",
            "Cash Umum",
            "Cash Bensin",
        ]:
            self.assertIn(expected, body)

        self.assertNotIn("Cash Ledger'!", body)

    def test_net_worth_dashboard_k17_reads_account_ledger_cash_net(self):
        body = extract_function(self.source, "setupDashboardNetWorthPanel")

        for expected in [
            "dashboard.getRange('K17').setFormula",
            "Account Ledger",
            "SUMIFS",
            "Cash Umum",
            "Cash Bensin",
            "Aset'!B17",
            "Aset'!B18",
        ]:
            self.assertIn(expected, body)

        self.assertNotIn("Cash Ledger'!", body)

    def test_admin_read_only_audit_checks_formula_account_ledger_usage(self):
        for expected in [
            "admin\\s+(audit|check|cek)\\s+(cash\\s+)?(reporting|report|formula|formulas|dashboard)",
            "monthlyB6 = monthly ? monthly.getRange('B6').getFormula() : ''",
            "monthlyE6 = monthly ? monthly.getRange('E6').getFormula() : ''",
            "monthlyB8 = monthly ? monthly.getRange('B8').getFormula() : ''",
            "dashboardK17 = dashboard ? dashboard.getRange('K17').getFormula() : ''",
            "monthly_b6_uses_account_ledger",
            "monthly_e6_uses_account_ledger",
            "dashboard_k17_uses_account_ledger",
            "indexOf('Account Ledger') >= 0",
            "cash_reporting_formula_audit",
        ]:
            self.assertIn(expected, self.source)

    def test_admin_refresh_command_refreshes_reporting_and_net_worth_panels(self):
        for expected in [
            "admin\\s+(refresh|sync|update|reload)\\s+(cash\\s+)?(reporting|report|formula|formulas|dashboard)",
            "const reporting = refreshCashReportingFormulas();",
            "const netWorth = setupDashboardNetWorthPanel();",
            "cash_reporting_refresh",
            "Monthly Review dan Dashboard sekarang membaca",
            "Account Ledger",
        ]:
            self.assertIn(expected, self.source)

    def test_this_contract_does_not_disable_cash_ledger_writes(self):
        body = extract_function(self.source, "writeRouted_")

        self.assertIn("writeCashLedgerCompatibility_(ss, parsed, rawText, common)", body)
        self.assertIn("writeAccountLedgerMirror_(ss, parsed, rawText, common, AIRO_CONFIG.tabs.cash)", body)
        self.assertIn("writtenTab: AIRO_CONFIG.tabs.accountLedger", body)

    def test_no_script_deletes_cash_ledger_tab_during_read_contract_phase(self):
        forbidden_patterns = [
            r"deleteSheet\s*\(\s*AIRO_CONFIG\.tabs\.cash\s*\)",
            r"deleteSheet\s*\(\s*cashSheet\s*\)",
            r"\.deleteSheet\s*\(",
        ]

        for pattern in forbidden_patterns:
            self.assertIsNone(
                re.search(pattern, self.source),
                msg=f"Forbidden sheet deletion pattern found: {pattern}",
            )


if __name__ == "__main__":
    unittest.main()
