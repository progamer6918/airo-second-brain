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


class FinanceEventsRuntimeSchemaContractTest(unittest.TestCase):
    def setUp(self):
        self.source = read_source()

    def test_finance_events_tab_config_exists(self):
        self.assertIn("financeEvents:", self.source)
        self.assertIn("Finance Events", self.source)
        self.assertIn("AIRO_CONFIG.tabs.financeEvents", self.source)

    def test_finance_events_headers_helper_locks_schema_order(self):
        body = extract_function(self.source, "getFinanceEventsHeaders_")

        expected_headers = [
            "event_id",
            "event_ts",
            "event_type",
            "event_source",
            "source_tab",
            "source_row",
            "linked_txn_id",
            "account",
            "category",
            "amount",
            "direction",
            "status",
            "reason",
            "payload_json",
            "notes",
        ]

        last_pos = -1
        for header in expected_headers:
            pos = body.find(f"'{header}'")
            self.assertGreater(pos, last_pos, msg=f"Header out of order or missing: {header}")
            last_pos = pos

    def test_ensure_finance_events_sheet_creates_tab_and_header_only(self):
        body = extract_function(self.source, "ensureFinanceEventsSheet_")

        for expected in [
            "AIRO_CONFIG.tabs.financeEvents",
            "getFinanceEventsHeaders_()",
            "getSheetLoose_",
            "insertSheet",
            "setValues([headers])",
            "setFrozenRows(1)",
            "tabName: AIRO_CONFIG.tabs.financeEvents",
            "headers: headers",
        ]:
            self.assertIn(expected, body)

        for forbidden in [
            "writeFinanceEvent_",
            "appendFinanceEvent_",
            "emitFinanceEvent_",
            "logFinanceEvent_",
            "writeRouted_",
            "writeAccountLedgerMirror_",
        ]:
            self.assertNotIn(forbidden, body)

    def test_manual_finance_event_writer_exists_but_emission_helpers_do_not_exist_yet(self):
        for expected in [
            "function buildFinanceEvent_(",
            "function writeFinanceEvent_(",
            "function appendFinanceEvent_(",
        ]:
            self.assertIn(expected, self.source)

        forbidden_runtime_markers = [
            "function emitFinanceEvent_(",
            "function logFinanceEvent_(",
        ]

        for marker in forbidden_runtime_markers:
            self.assertNotIn(marker, self.source)

    def test_only_write_routed_has_first_event_recording_wrapper(self):
        write_routed = extract_function(self.source, "writeRouted_")
        self.assertIn("recordFinanceEventForWriteResult_(", write_routed)

        for function_name in [
            "doPost",
            "writeAccountLedgerMirror_",
            "processReviewQueueApproved",
            "writeInternalTransferToAccountLedger_",
        ]:
            body = extract_function(self.source, function_name)
            for forbidden in [
                "recordFinanceEventForWriteResult_",
                "writeFinanceEvent_",
                "appendFinanceEvent_",
                "emitFinanceEvent_",
                "logFinanceEvent_",
                "ensureFinanceEventsSheet_",
            ]:
                self.assertNotIn(forbidden, body)

    def test_account_ledger_remains_primary_wallet_source(self):
        body = extract_function(self.source, "writeAccountLedgerMirror_")

        for expected in [
            "amount_in",
            "amount_out",
            "source_tab",
            "linked_txn_id",
            "AIRO_CONFIG.tabs.accountLedger",
        ]:
            self.assertIn(expected, body)

    def test_cash_ledger_compatibility_flag_remains_default_off(self):
        flag_body = extract_function(self.source, "isCashLedgerCompatibilityWriteEnabled_")
        compat_body = extract_function(self.source, "writeCashLedgerCompatibility_")

        self.assertIn("AIRO_CASH_LEDGER_COMPAT_WRITES_ENABLED", flag_body)
        self.assertIn("return false", flag_body)
        self.assertIn("cash_ledger_compat_writes_disabled", compat_body)

    def test_no_email_ingestion_or_destructive_cash_ledger_behavior_added(self):
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


if __name__ == "__main__":
    unittest.main()
