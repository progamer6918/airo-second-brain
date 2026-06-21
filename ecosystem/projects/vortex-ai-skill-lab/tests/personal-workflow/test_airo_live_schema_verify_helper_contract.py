from pathlib import Path
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


class LiveSchemaVerifyHelperContractTest(unittest.TestCase):
    def setUp(self):
        self.source = read_source()
        self.body = extract_function(self.source, "airoLiveSchemaVerifyOnly")

    def test_helper_targets_authorized_live_spreadsheet(self):
        self.assertIn("SpreadsheetApp.openById(spreadsheetId)", self.body)
        self.assertIn("SPREADSHEET_ID", self.body)
        self.assertIn("1CKARXGurxZ0Rby3-_iisVS0_r65JM6ZaT6tbAJUF7sU", self.body)

    def test_helper_creates_or_verifies_finance_events_schema(self):
        self.assertIn("ensureFinanceEventsSheet_", self.body)
        self.assertIn("AIRO_LIVE_SCHEMA_VERIFY_FINANCE_EVENTS_STATUS", self.body)
        self.assertIn("AIRO_LIVE_SCHEMA_VERIFY_FINANCE_EVENTS_TAB", self.body)

    def test_helper_refreshes_cash_reporting_formulas_only_best_effort(self):
        self.assertIn("refreshCashReportingFormulas", self.body)
        self.assertIn("try {", self.body)
        self.assertIn("catch (err)", self.body)
        self.assertIn("AIRO_LIVE_SCHEMA_VERIFY_CASH_REPORTING_STATUS", self.body)

    def test_helper_logs_before_after_tabs_without_transaction_smoke(self):
        for expected in [
            "beforeTabs",
            "afterTabs",
            "AIRO_LIVE_SCHEMA_VERIFY_BEFORE_TAB_COUNT",
            "AIRO_LIVE_SCHEMA_VERIFY_AFTER_TAB_COUNT",
            "AIRO_LIVE_SCHEMA_VERIFY_AFTER_TABS",
        ]:
            self.assertIn(expected, self.body)

        for forbidden in [
            "doPost(",
            "writeRouted_(",
            "writeAccountLedgerMirror_(",
            "processReviewQueueApproved(",
            "deleteSheet(",
            "deleteRows(",
            "GmailApp",
            "MailApp",
            "getInboxThreads",
        ]:
            self.assertNotIn(forbidden, self.body)


if __name__ == "__main__":
    unittest.main()
