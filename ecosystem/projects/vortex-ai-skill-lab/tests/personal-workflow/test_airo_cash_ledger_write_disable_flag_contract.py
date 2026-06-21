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


class CashLedgerWriteDisableFlagContractTest(unittest.TestCase):
    def setUp(self):
        self.source = read_source()

    def test_cash_ledger_compat_flag_defaults_disabled(self):
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

    def test_cash_ledger_compat_writer_skips_by_default_and_never_deletes(self):
        body = extract_function(self.source, "writeCashLedgerCompatibility_")

        for expected in [
            "isCashLedgerCompatibilityWriteEnabled_()",
            "cash_ledger_compat_writes_disabled",
            "skipped: true",
            "writeCashLedger_(ss, parsed, rawText, common)",
        ]:
            self.assertIn(expected, body)

        self.assertNotIn("deleteSheet", body)

    def test_write_routed_uses_flagged_cash_compat_writer_and_keeps_account_ledger_primary(self):
        body = extract_function(self.source, "writeRouted_")

        for expected in [
            "writeCashLedgerCompatibility_(ss, parsed, rawText, common)",
            "writeAccountLedgerMirror_(ss, parsed, rawText, common, AIRO_CONFIG.tabs.cash)",
            "writtenTab: AIRO_CONFIG.tabs.accountLedger",
        ]:
            self.assertIn(expected, body)

        self.assertNotIn("writeCashLedger_(ss, parsed, rawText, common)", body)

    def test_internal_transfer_uses_flagged_cash_compat_writer(self):
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

        self.assertNotIn("writeCashLedger_(", body)

    def test_raw_cash_writer_remains_available_only_as_compatibility_layer_target(self):
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

    def test_no_sheet_or_historical_row_deletion_is_added(self):
        forbidden_patterns = [
            r"deleteSheet\s*\(",
            r"deleteRows\s*\(",
            r"clearContents\s*\(",
            r"clear\s*\(",
        ]

        for pattern in forbidden_patterns:
            self.assertIsNone(
                re.search(pattern, self.source),
                msg=f"Forbidden destructive pattern found: {pattern}",
            )


if __name__ == "__main__":
    unittest.main()
