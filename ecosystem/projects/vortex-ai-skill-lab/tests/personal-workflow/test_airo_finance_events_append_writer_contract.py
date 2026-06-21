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


class FinanceEventsAppendWriterContractTest(unittest.TestCase):
    def setUp(self):
        self.source = read_source()

    def test_build_finance_event_locks_schema_fields(self):
        body = extract_function(self.source, "buildFinanceEvent_")

        expected_fields = [
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

        for field in expected_fields:
            self.assertIn(field + ":", body)

        self.assertIn("Utilities.getUuid()", body)
        self.assertIn("manual_event", body)
        self.assertIn("system", body)

    def test_payload_json_is_small_and_redacted_before_write(self):
        body = extract_function(self.source, "financeEventPayloadJson_")

        for expected in [
            "JSON.stringify",
            "slice(0, 2000)",
            "sensitive_payload_blocked",
            "otp",
            "password",
            "access_token",
            "token",
        ]:
            self.assertIn(expected, body)

    def test_write_finance_event_is_append_only_to_finance_events_tab(self):
        body = extract_function(self.source, "writeFinanceEvent_")

        for expected in [
            "ensureFinanceEventsSheet_(ss)",
            "buildFinanceEvent_(event)",
            "appendByHeader_(ss, AIRO_CONFIG.tabs.financeEvents, row, { createIfMissing: false })",
        ]:
            self.assertIn(expected, body)

        for forbidden in [
            "writeRouted_",
            "writeAccountLedgerMirror_",
            "processReviewQueueApproved",
            "deleteSheet",
            "deleteRows",
            "GmailApp",
            "MailApp",
        ]:
            self.assertNotIn(forbidden, body)

    def test_append_finance_event_delegates_to_write_finance_event(self):
        body = extract_function(self.source, "appendFinanceEvent_")

        self.assertIn("return writeFinanceEvent_(ss, event);", body)

    def test_only_write_routed_generic_path_uses_first_event_recording_wrapper(self):
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
                "recordFinanceEventForWriteResult_(",
                "writeFinanceEvent_(",
                "appendFinanceEvent_(",
                "emitFinanceEvent_(",
                "logFinanceEvent_(",
            ]:
                self.assertNotIn(forbidden, body, msg=f"{function_name} must not emit Finance Events yet")

    def test_no_emit_or_log_helper_exists_yet(self):
        for forbidden in [
            "function emitFinanceEvent_(",
            "function logFinanceEvent_(",
        ]:
            self.assertNotIn(forbidden, self.source)

    def test_finance_events_schema_creation_still_exists(self):
        headers = extract_function(self.source, "getFinanceEventsHeaders_")
        ensure = extract_function(self.source, "ensureFinanceEventsSheet_")

        self.assertIn("event_id", headers)
        self.assertIn("payload_json", headers)
        self.assertIn("AIRO_CONFIG.tabs.financeEvents", ensure)
        self.assertIn("setValues([headers])", ensure)

    def test_account_ledger_and_cash_ledger_guards_remain_unchanged(self):
        account_mirror = extract_function(self.source, "writeAccountLedgerMirror_")
        cash_flag = extract_function(self.source, "isCashLedgerCompatibilityWriteEnabled_")

        for expected in [
            "amount_in",
            "amount_out",
            "source_tab",
            "linked_txn_id",
            "AIRO_CONFIG.tabs.accountLedger",
        ]:
            self.assertIn(expected, account_mirror)

        self.assertIn("AIRO_CASH_LEDGER_COMPAT_WRITES_ENABLED", cash_flag)
        self.assertIn("return false", cash_flag)


if __name__ == "__main__":
    unittest.main()
