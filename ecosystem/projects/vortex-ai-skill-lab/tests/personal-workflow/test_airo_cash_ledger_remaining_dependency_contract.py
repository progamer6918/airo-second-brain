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


class CashLedgerRemainingDependencyContractTest(unittest.TestCase):
    def setUp(self):
        self.source = read_source()

    def test_cash_compatibility_flag_stays_default_off(self):
        body = extract_function(self.source, "isCashLedgerCompatibilityWriteEnabled_")

        for expected in [
            "AIRO_CASH_LEDGER_COMPAT_WRITES_ENABLED",
            "return false",
            "true",
            "yes",
            "on",
            "1",
        ]:
            self.assertIn(expected, body)

    def test_raw_cash_writer_is_only_called_by_compatibility_wrapper(self):
        wrapper = extract_function(self.source, "writeCashLedgerCompatibility_")

        self.assertIn("cash_ledger_compat_writes_disabled", wrapper)
        self.assertIn("return writeCashLedger_(ss, parsed, rawText, common);", wrapper)

        direct_calls = re.findall(r"(?<!function )\bwriteCashLedger_\(", self.source)
        self.assertEqual(
            len(direct_calls),
            1,
            msg="Raw writeCashLedger_ must only be called by writeCashLedgerCompatibility_.",
        )

    def test_normal_telegram_write_path_does_not_call_legacy_cash_maintenance_or_backfill(self):
        try:
            do_post = extract_function(self.source, "airoOriginalDoPostForSprint7ParserPlan_")
        except AssertionError:
            do_post = extract_function(self.source, "doPost")

        forbidden = [
            "refreshCashLedgerMaintenance",
            "migrateCashLedgerToAccountLedger",
            "auditAccountLedgerMigration",
            "cleanupAccountLedgerMigrationIssues",
            "cash_ledger_account_parity_audit",
            "cash_ledger_account_parity_detail_audit",
            "writeCashLedger_(",
        ]

        for token in forbidden:
            self.assertNotIn(token, do_post)

        self.assertIn("writeRouted_", do_post)

    def test_cash_route_and_review_queue_cash_route_go_through_write_routed_compatibility(self):
        route_planned = extract_function(self.source, "routePlannedTab_")
        route_review = extract_function(self.source, "routeReviewApprovedTab_")
        process_review = extract_function(self.source, "processReviewQueueApproved")
        write_routed = extract_function(self.source, "writeRouted_")

        self.assertIn("return AIRO_CONFIG.tabs.cash", route_planned)
        self.assertIn("return AIRO_CONFIG.tabs.cash", route_review)
        self.assertIn("writeRouted_(ss, plannedTab, parsed, rawText, stagingResult)", process_review)

        self.assertIn("writeCashLedgerCompatibility_(ss, parsed, rawText, common)", write_routed)
        self.assertIn("writeAccountLedgerMirror_(ss, parsed, rawText, common, AIRO_CONFIG.tabs.cash)", write_routed)
        self.assertNotIn("writeCashLedger_(ss, parsed, rawText, common)", write_routed)

    def test_internal_transfer_cash_sync_uses_compatibility_wrapper_only(self):
        body = extract_function(self.source, "writeInternalTransferToAccountLedger_")

        for expected in [
            "writeAccountLedgerMirror_",
            "sharedTxnId + ':in'",
            "sharedTxnId + ':out'",
            "Cash Ledger compatibility layer synchronization",
            "writeCashLedgerCompatibility_",
            "writtenTab: AIRO_CONFIG.tabs.accountLedger",
        ]:
            self.assertIn(expected, body)

        self.assertNotIn("writeCashLedger_(", body)

    def test_legacy_cash_maintenance_is_not_called_by_core_write_paths(self):
        maintenance = extract_function(self.source, "refreshCashLedgerMaintenance")
        write_routed = extract_function(self.source, "writeRouted_")
        internal_transfer = extract_function(self.source, "writeInternalTransferToAccountLedger_")
        process_review = extract_function(self.source, "processReviewQueueApproved")

        for expected in [
            "AIRO_CONFIG.tabs.cash",
            "amount_start",
            "amount_remaining",
            "amount_in",
            "amount_out",
            "clearContent",
            "refreshCashMonthlyReviewFormulas",
        ]:
            self.assertIn(expected, maintenance)

        for body in [write_routed, internal_transfer, process_review]:
            self.assertNotIn("refreshCashLedgerMaintenance", body)

    def test_cash_backfill_and_parity_surfaces_are_manual_admin_only_not_auto_path(self):
        handle_admin = extract_function(self.source, "handleSpecialFinanceCommand_")
        do_post = extract_function(self.source, "doPost")
        write_routed = extract_function(self.source, "writeRouted_")

        for expected in [
            "cash_ledger_account_parity_audit",
            "cash_ledger_account_parity_detail_audit",
            "Account Ledger Cash",
            "Cash Ledger",
        ]:
            self.assertIn(expected, handle_admin)

        self.assertIn("Manual backfill function to migrate historical data", self.source)
        self.assertIn("source_tab: AIRO_CONFIG.tabs.cash", self.source)
        self.assertIn("appendByHeader_(ss, AIRO_CONFIG.tabs.accountLedger", self.source)

        for forbidden in [
            "cash_ledger_account_parity_audit",
            "cash_ledger_account_parity_detail_audit",
            "Manual backfill function to migrate historical data",
        ]:
            self.assertNotIn(forbidden, do_post)
            self.assertNotIn(forbidden, write_routed)

    def test_dashboard_monthly_cash_reads_stay_on_account_ledger(self):
        reporting = extract_function(self.source, "refreshCashReportingFormulas")
        net_worth = extract_function(self.source, "setupDashboardNetWorthPanel")

        for expected in [
            "Account Ledger",
            "monthlyCashInFormula",
            "monthlyCashOutFormula",
            "dashboardCashAktifFormula",
            "Account Ledger'!D:D",
            "Account Ledger'!E:E",
        ]:
            self.assertIn(expected, reporting)

        for expected in [
            "dashboard.getRange('K17').setFormula",
            "Account Ledger",
            "Cash Umum",
            "Cash Bensin",
        ]:
            self.assertIn(expected, net_worth)

        self.assertNotIn("Cash Ledger'!", reporting)
        self.assertNotIn("Cash Ledger'!", net_worth)

    def test_no_cash_ledger_sheet_or_bulk_row_deletion_is_introduced(self):
        forbidden_patterns = [
            r"deleteSheet\s*\(",
            r"deleteRows\s*\(",
            r"cashSheet\s*\.\s*deleteRow\s*\(",
            r"getSheetLoose_\(ss,\s*AIRO_CONFIG\.tabs\.cash\)[\s\S]{0,300}deleteRow\s*\(",
        ]

        for pattern in forbidden_patterns:
            self.assertIsNone(
                re.search(pattern, self.source),
                msg=f"Forbidden Cash Ledger destructive pattern found: {pattern}",
            )


if __name__ == "__main__":
    unittest.main()
