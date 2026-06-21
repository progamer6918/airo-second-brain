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


class AccountLedgerAssetPurchaseOutflowContractTest(unittest.TestCase):
    def setUp(self):
        self.source = read_source()

    def test_asset_writer_mirrors_asset_purchase_to_account_ledger(self):
        body = extract_function(self.source, "writeAssetSafely_")

        self.assertIn("writeAccountLedgerMirror_", body)
        self.assertIn("asset_purchase", body)
        self.assertRegex(body, r"type\s*:\s*['\"]asset_purchase['\"]")
        self.assertRegex(body, r"category\s*:\s*parsed\.category\s*\|\|\s*['\"]Aset['\"]")
        self.assertRegex(body, r"account\s*:\s*parsed\.account\s*\|\|\s*['\"]Unknown['\"]")
        self.assertRegex(body, r"linked_txn_id\s*:\s*common\.linked_txn_id\s*\|\|\s*makeTxnId_\(\{\},\s*rawText\)")
        self.assertRegex(body, r"writeAccountLedgerMirror_\(ss,\s*accountParsed,\s*rawText,\s*accountCommon,\s*AIRO_CONFIG\.tabs\.aset\)")

    def test_account_ledger_mirror_treats_asset_purchase_as_outflow_type(self):
        mirror_body = extract_function(self.source, "writeAccountLedgerMirror_")

        self.assertIn("asset_purchase", mirror_body)
        self.assertIn("debt_payment", mirror_body)
        self.assertIn("cc_payment", mirror_body)
        self.assertIn("amount_out", mirror_body)
        self.assertIn("linked_txn_id", mirror_body)

    def test_asset_section_writers_are_not_rewritten_by_outflow_patch(self):
        savings_body = extract_function(self.source, "appendToAssetSection_")
        gold_body = extract_function(self.source, "appendGoldAssetRow_")

        self.assertIn("linked_txn_id", savings_body)
        self.assertIn("linked_txn_id", gold_body)
        self.assertNotIn("writeAccountLedgerMirror_", savings_body)
        self.assertNotIn("writeAccountLedgerMirror_", gold_body)


if __name__ == "__main__":
    unittest.main()
