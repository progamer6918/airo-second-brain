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


class AccountLedgerCcPaymentOutflowContractTest(unittest.TestCase):
    def setUp(self):
        self.source = read_source()

    def test_cc_payment_handler_writes_account_ledger_outflow(self):
        body = extract_function(self.source, "markCreditCardPocketBluTransfer_")

        self.assertIn("writeAccountLedgerMirror_", body)
        self.assertIn("cc_payment", body)
        self.assertRegex(body, r"type\s*:\s*['\"]cc_payment['\"]")
        self.assertRegex(body, r"account\s*:\s*parsed\.account\s*\|\|\s*['\"]Blu['\"]")
        self.assertRegex(body, r"linked_txn_id\s*:\s*common\.linked_txn_id\s*\|\|\s*makeTxnId_\(\{\},\s*rawText\)")
        self.assertRegex(body, r"writeAccountLedgerMirror_\(ss,\s*accountParsed,\s*rawText,\s*accountCommon,\s*AIRO_CONFIG\.tabs\.creditCard\)")

    def test_cc_payment_outflow_reuses_account_ledger_mirror_contract(self):
        mirror_body = extract_function(self.source, "writeAccountLedgerMirror_")

        self.assertIn("amount_out", mirror_body)
        self.assertIn("source_tab", mirror_body)
        self.assertIn("linked_txn_id", mirror_body)
        self.assertRegex(mirror_body, r"linked_txn_id\s*:\s*common\.linked_txn_id\s*\|\|\s*entryId")

    def test_cc_purchase_writer_is_not_rewritten_by_payment_patch(self):
        purchase_body = extract_function(self.source, "appendCreditCardPurchase_")

        self.assertIn("status_pocket_blu", purchase_body)
        self.assertIn("transferred_at", purchase_body)
        self.assertNotIn("writeAccountLedgerMirror_", purchase_body)


if __name__ == "__main__":
    unittest.main()
