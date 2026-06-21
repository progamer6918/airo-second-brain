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


class CreditCardBillingStatusContractTest(unittest.TestCase):
    def setUp(self):
        self.source = read_source()

    def test_credit_card_purchase_writer_sets_pending_status_and_billing_cycle(self):
        body = extract_function(self.source, "appendCreditCardPurchase_")

        for expected in [
            "status_pocket_blu",
            "Belum",
            "billing_cycle_id",
            "billing_start",
            "billing_end",
            "transferred_at",
            "cc_entry_id",
            "linked_txn_id",
            "cycle.id",
            "cycle.start",
            "cycle.end",
        ]:
            self.assertIn(expected, body)

        self.assertIn("sheet.getRange(targetRow, 1, 1, row.length).setValues([row])", body)

    def test_credit_card_payment_marker_requires_status_and_amount_columns(self):
        body = extract_function(self.source, "markCreditCardPocketBluTransfer_")

        for expected in [
            "status_pocket_blu",
            "amount",
            "cc_payment_amount_or_columns_missing",
            "cc_payment_no_matching_pending_purchase",
            "Sudah",
            "pocket_blu_transfer",
        ]:
            self.assertIn(expected, body)

    def test_credit_card_payment_marker_updates_account_ledger_outflow(self):
        body = extract_function(self.source, "markCreditCardPocketBluTransfer_")

        for expected in [
            "writeAccountLedgerMirror_",
            "account_ledger_result",
            "cc_payment",
            "AIRO_CONFIG.tabs.creditCard",
        ]:
            self.assertIn(expected, body)

    def test_credit_card_header_detection_and_column_map_are_canonical(self):
        header_body = extract_function(self.source, "findCcHeaderRow_")
        map_body = extract_function(self.source, "ccColMap_")

        for expected in ["cc_entry_id", "amount", "status_pocket_blu"]:
            self.assertIn(expected, header_body)

        self.assertIn("canonicalKey_", map_body)
        self.assertIn("map[canonicalKey_(h)] = i + 1", map_body)
        self.assertIn("return map", map_body)

    def test_credit_card_billing_cycle_runtime_surfaces_are_present(self):
        for function_name in [
            "setupCreditCardTabCycleHeader_",
            "setupDashboardCreditCardCyclePanel",
        ]:
            self.assertIn(f"function {function_name}(", self.source)

        for expected in [
            "cc_cycle_runtime_audit",
            "Credit Card cycle audit selesai",
            "billing_cycle_id",
            "billing_start",
            "billing_end",
            "status_pocket_blu",
        ]:
            self.assertIn(expected, self.source)


if __name__ == "__main__":
    unittest.main()
