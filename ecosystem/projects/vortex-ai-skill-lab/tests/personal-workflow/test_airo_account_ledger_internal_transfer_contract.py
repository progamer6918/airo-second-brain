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


class AccountLedgerInternalTransferContractTest(unittest.TestCase):
    def setUp(self):
        self.source = read_source()

    def test_internal_transfer_writer_exists_and_is_two_sided(self):
        body = extract_function(self.source, "writeInternalTransferToAccountLedger_")

        self.assertIn("sharedTxnId", body)
        self.assertIn("writeAccountLedgerMirror_", body)
        self.assertGreaterEqual(body.count("writeAccountLedgerMirror_"), 2)

        self.assertRegex(body, r"linked_txn_id\s*:\s*sharedTxnId\s*\+\s*['\"]:in['\"]")
        self.assertRegex(body, r"linked_txn_id\s*:\s*sharedTxnId\s*\+\s*['\"]:out['\"]")

        self.assertIn("transfer_in", body)
        self.assertIn("transfer_out", body)

    def test_internal_transfer_detection_is_limited_to_supported_wallet_accounts(self):
        detect_body = extract_function(self.source, "detectInternalTransfer_")
        normalize_body = extract_function(self.source, "normalizeSupportedAccount_")

        self.assertIn("normalizeSupportedAccount_", detect_body)
        self.assertIn("BCA", normalize_body)
        self.assertIn("Blu", normalize_body)
        self.assertIn("Cash", normalize_body)

    def test_account_ledger_mirror_preserves_direction_source_and_link(self):
        mirror_body = extract_function(self.source, "writeAccountLedgerMirror_")

        self.assertIn("amount_in", mirror_body)
        self.assertIn("amount_out", mirror_body)
        self.assertIn("source_tab", mirror_body)
        self.assertIn("linked_txn_id", mirror_body)

        self.assertRegex(mirror_body, r"amount_in\s*:\s*isInflow\s*\?")
        self.assertRegex(mirror_body, r"amount_out\s*:\s*isInflow\s*\?")
        self.assertRegex(mirror_body, r"source_tab\s*:\s*sourceTab")

    def test_account_ledger_schema_contains_sprint1_required_columns(self):
        ensure_body = extract_function(self.source, "ensureAccountLedgerSheet_")

        for header in [
            "entry_id",
            "date",
            "account",
            "amount_in",
            "amount_out",
            "balance",
            "type",
            "category",
            "description",
            "raw_text",
            "source_tab",
            "linked_txn_id",
            "notes",
        ]:
            self.assertIn(header, ensure_body)

    def test_account_ledger_mirror_uses_entry_id_as_link_fallback(self):
        mirror_body = extract_function(self.source, "writeAccountLedgerMirror_")

        self.assertIn("const entryId = common.rowId || common.linked_txn_id || makeTxnId_({}, rawText);", mirror_body)
        self.assertRegex(mirror_body, r"linked_txn_id\s*:\s*common\.linked_txn_id\s*\|\|\s*entryId")
        self.assertNotRegex(mirror_body, r"linked_txn_id\s*:\s*common\.linked_txn_id\s*\|\|\s*[\'\"]{2}")
        self.assertRegex(mirror_body, r"source_tab\s*:\s*sourceTab")

if __name__ == "__main__":
    unittest.main()
