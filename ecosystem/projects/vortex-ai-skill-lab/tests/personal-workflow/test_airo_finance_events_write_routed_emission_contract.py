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


class FinanceEventsWriteRoutedEmissionContractTest(unittest.TestCase):
    def setUp(self):
        self.source = read_source()

    def test_write_routed_generic_append_success_records_finance_event(self):
        body = extract_function(self.source, "writeRouted_")

        for expected in [
            "const result = appendByHeader_(ss, tabName, common, { createIfMissing: false });",
            "recordFinanceEventForWriteResult_(",
            "event_type: 'transaction_created'",
            "event_source: 'telegram'",
            "source_tab: result.writtenTab || tabName",
            "source_row: result.row || ''",
            "linked_txn_id: common.linked_txn_id || common.rowId || ''",
            "return result;",
        ]:
            self.assertIn(expected, body)

    def test_finance_event_record_helper_is_best_effort_and_non_blocking(self):
        body = extract_function(self.source, "recordFinanceEventForWriteResult_")

        for expected in [
            "if (!result || result.status !== 'written') return result;",
            "try {",
            "writeFinanceEvent_(ss,",
            "event_type: event.event_type || 'transaction_created'",
            "event_source: event.event_source || 'telegram'",
            "source_tab: event.source_tab || result.writtenTab || ''",
            "source_row: event.source_row || result.row || ''",
            "linked_txn_id: event.linked_txn_id || common.linked_txn_id || common.rowId || result.rowId || ''",
            "status: 'ok'",
            "payload: {",
            "write_verified: result.writeVerified === true",
            "return result;",
            "catch (err)",
        ]:
            self.assertIn(expected, body)

        self.assertNotIn("throw", body)

    def test_first_emission_does_not_change_special_domain_or_ledger_branches(self):
        body = extract_function(self.source, "writeRouted_")

        special_branch_tokens = [
            "return writeCreditCardSafely_(ss, parsed, rawText, common);",
            "return writeHutangSafely_(ss, parsed, rawText, common);",
            "return writeAssetSafely_(ss, parsed, rawText, common);",
            "return writeInternalTransferToAccountLedger_(ss, parsed, rawText, common, transfer);",
            "const cashResult = writeCashLedgerCompatibility_(ss, parsed, rawText, common);",
            "writeAccountLedgerMirror_(ss, parsed, rawText, common, AIRO_CONFIG.tabs.cash)",
            "const result = writeAccountLedgerMirror_(ss, parsed, rawText, common, sourceTab);",
        ]

        for token in special_branch_tokens:
            self.assertIn(token, body)

    def test_no_event_emission_is_added_to_core_domain_functions_yet(self):
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
                self.assertNotIn(forbidden, body, msg=f"{function_name} must not emit Finance Events in this micro-step")

    def test_finance_event_writer_and_schema_remain_append_only(self):
        writer = extract_function(self.source, "writeFinanceEvent_")
        build = extract_function(self.source, "buildFinanceEvent_")
        headers = extract_function(self.source, "getFinanceEventsHeaders_")

        for expected in [
            "ensureFinanceEventsSheet_(ss)",
            "buildFinanceEvent_(event)",
            "appendByHeader_(ss, AIRO_CONFIG.tabs.financeEvents, row, { createIfMissing: false })",
        ]:
            self.assertIn(expected, writer)

        for expected in [
            "event_id",
            "event_ts",
            "event_type",
            "event_source",
            "source_tab",
            "source_row",
            "linked_txn_id",
            "payload_json",
        ]:
            self.assertIn(expected, build)
            self.assertIn(expected, headers)

        for forbidden in [
            "deleteSheet",
            "deleteRows",
            "clearContents",
            "GmailApp",
            "MailApp",
        ]:
            self.assertNotIn(forbidden, writer)

    def test_email_ingestion_and_cash_ledger_guards_remain_unchanged(self):
        cash_flag = extract_function(self.source, "isCashLedgerCompatibilityWriteEnabled_")
        cash_compat = extract_function(self.source, "writeCashLedgerCompatibility_")

        self.assertIn("AIRO_CASH_LEDGER_COMPAT_WRITES_ENABLED", cash_flag)
        self.assertIn("return false", cash_flag)
        self.assertIn("cash_ledger_compat_writes_disabled", cash_compat)

        for forbidden in [
            "GmailApp",
            "Gmail.Users",
            "MailApp",
            "getInboxThreads",
            "deleteSheet(",
            "deleteRows(",
        ]:
            self.assertNotIn(forbidden, self.source)


if __name__ == "__main__":
    unittest.main()
