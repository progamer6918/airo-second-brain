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


class CashLedgerRemovalSafetyContractTest(unittest.TestCase):
    def setUp(self):
        self.source = read_source()

    def test_cash_ledger_writer_still_preserves_compatibility_fields(self):
        body = extract_function(self.source, "writeCashLedger_")

        for expected in [
            "AIRO_CONFIG.tabs.cash",
            "amount_start",
            "amount_remaining",
            "amount_in",
            "amount_out",
            "linked_txn_id",
            "entry_id",
            "appendByHeader_",
            "syncCashLedgerRuntimeAmountColumns_",
        ]:
            self.assertIn(expected, body)

    def test_cash_ledger_writer_is_mirrored_to_account_ledger_before_removal(self):
        body = extract_function(self.source, "writeRouted_")

        for expected in [
            "writeCashLedgerCompatibility_(ss, parsed, rawText, common)",
            "writeAccountLedgerMirror_(ss, parsed, rawText, common, AIRO_CONFIG.tabs.cash)",
            "writtenTab: AIRO_CONFIG.tabs.accountLedger",
        ]:
            self.assertIn(expected, body)

    def test_internal_transfer_keeps_account_ledger_primary_and_cash_compatibility_layer(self):
        body = extract_function(self.source, "writeInternalTransferToAccountLedger_")

        for expected in [
            "writeAccountLedgerMirror_",
            "sharedTxnId + ':in'",
            "sharedTxnId + ':out'",
            "Cash Ledger compatibility layer synchronization",
            "writeCashLedgerCompatibility_",
            "cashLedgerRow",
            "writtenTab: AIRO_CONFIG.tabs.accountLedger",
        ]:
            self.assertIn(expected, body)

    def test_account_ledger_schema_has_cash_replacement_fields(self):
        body = extract_function(self.source, "ensureAccountLedgerSheet_")

        for expected in [
            "entry_id",
            "date",
            "account",
            "amount_in",
            "amount_out",
            "description",
            "source_tab",
            "linked_txn_id",
            "notes",
        ]:
            self.assertIn(expected, body)

    def test_account_ledger_mirror_preserves_direction_source_and_linkage(self):
        body = extract_function(self.source, "writeAccountLedgerMirror_")

        for expected in [
            "cash_in",
            "cash_out",
            "amount_in",
            "amount_out",
            "source_tab: sourceTab",
            "linked_txn_id: common.linked_txn_id || entryId",
            "AIRO_CONFIG.tabs.accountLedger",
        ]:
            self.assertIn(expected, body)

    def test_cash_reporting_formulas_have_account_ledger_replacement_path(self):
        wrapper = extract_function(self.source, "refreshCashMonthlyReviewFormulas")
        body = extract_function(self.source, "refreshCashReportingFormulas")

        self.assertIn("return refreshCashReportingFormulas();", wrapper)

        for expected in [
            "Account Ledger",
            "monthlyCashInFormula",
            "monthlyCashOutFormula",
            "dashboardCashAktifFormula",
            "monthly.getRange('B6')",
            "monthly.getRange('E6')",
            "dashboard",
        ]:
            self.assertIn(expected, body)

    def test_runtime_has_cash_reporting_read_only_audit_before_deletion(self):
        for expected in [
            "monthly_b6_uses_account_ledger",
            "monthly_e6_uses_account_ledger",
            "dashboard_k17_uses_account_ledger",
            "admin\\s+(audit|check|cek)\\s+(cash\\s+)?(reporting|report|formula|formulas|dashboard)",
        ]:
            self.assertIn(expected, self.source)

    def test_no_script_deletes_cash_ledger_tab_during_sprint3_safety_phase(self):
        forbidden_patterns = [
            r"deleteSheet\s*\(\s*AIRO_CONFIG\.tabs\.cash\s*\)",
            r"deleteSheet\s*\(\s*cashSheet\s*\)",
            r"\.deleteSheet\s*\(",
        ]

        for pattern in forbidden_patterns:
            self.assertIsNone(
                re.search(pattern, self.source),
                msg=f"Forbidden Cash Ledger deletion pattern found: {pattern}",
            )


if __name__ == "__main__":
    unittest.main()
