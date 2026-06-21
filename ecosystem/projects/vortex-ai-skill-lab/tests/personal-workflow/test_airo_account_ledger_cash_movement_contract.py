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


class AccountLedgerCashMovementContractTest(unittest.TestCase):
    def setUp(self):
        self.source = read_source()

    def test_cash_route_mirrors_cash_movement_to_account_ledger(self):
        self.assertRegex(
            self.source,
            r"const\s+cashResult\s*=\s*writeCashLedgerCompatibility_\(ss,\s*parsed,\s*rawText,\s*common\);[\s\S]{0,260}writeAccountLedgerMirror_\(ss,\s*parsed,\s*rawText,\s*common,\s*AIRO_CONFIG\.tabs\.cash\)"
        )

    def test_account_ledger_mirror_has_independent_account_ledger_target(self):
        body = extract_function(self.source, "writeAccountLedgerMirror_")

        self.assertIn("ensureAccountLedgerSheet_(ss)", body)
        self.assertIn("appendByHeader_", body)
        self.assertIn("applyAccountLedgerRowStyle_", body)
        self.assertIn("source_tab", body)
        self.assertIn("linked_txn_id", body)

    def test_account_ledger_mirror_preserves_cash_direction(self):
        body = extract_function(self.source, "writeAccountLedgerMirror_")

        self.assertIn("isInflow", body)
        self.assertRegex(body, r"amount_in\s*:\s*isInflow\s*\?\s*amount\s*:\s*['\"]['\"]")
        self.assertRegex(body, r"amount_out\s*:\s*isInflow\s*\?\s*['\"]['\"]\s*:\s*amount")

    def test_cash_movement_keeps_cash_ledger_as_source_tab_not_source_of_truth(self):
        mirror_body = extract_function(self.source, "writeAccountLedgerMirror_")

        self.assertRegex(
            self.source,
            r"writeAccountLedgerMirror_\(ss,\s*parsed,\s*rawText,\s*common,\s*AIRO_CONFIG\.tabs\.cash\)"
        )
        self.assertRegex(mirror_body, r"source_tab\s*:\s*sourceTab")
        self.assertRegex(mirror_body, r"linked_txn_id\s*:\s*common\.linked_txn_id\s*\|\|\s*entryId")

    def test_no_cash_ledger_deletion_is_present_in_sprint1_surface(self):
        forbidden = [
            "deleteSheet",
            "moveToTrash",
            "Cash Ledger removal",
            "delete Cash Ledger",
        ]

        active_surface = (
            extract_function(self.source, "writeCashLedger_")
            + "\n"
            + extract_function(self.source, "writeAccountLedgerMirror_")
        )

        for token in forbidden:
            self.assertNotIn(token, active_surface)


if __name__ == "__main__":
    unittest.main()
