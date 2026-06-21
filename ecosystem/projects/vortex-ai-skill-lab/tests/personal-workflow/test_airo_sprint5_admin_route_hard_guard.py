from pathlib import Path
import unittest


SOURCE = Path("scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs")
V2_SOURCE = Path("apps-script-prod-v2/AIRO_Finance_Multitab_Final_v1.js")
DOC = Path("docs/AIRO_FINANCE_SPRINT_5_ADMIN_ROUTE_HARD_GUARD.md")
CURRENT = Path("docs/AIRO_FINANCE_CURRENT_STATE.md")


class Sprint5AdminRouteHardGuardTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SOURCE.read_text(encoding="utf-8")
        cls.v2 = V2_SOURCE.read_text(encoding="utf-8")
        cls.doc = DOC.read_text(encoding="utf-8")
        cls.current = CURRENT.read_text(encoding="utf-8")

    def test_hard_guard_marker_exists_in_canonical_and_v2(self):
        marker = "AIRO_SPRINT5_ADMIN_RECONCILIATION_DOPOST_HARD_GUARD_V1"
        self.assertIn(marker, self.source)
        self.assertIn(marker, self.v2)

    def test_unknown_admin_safe_reject_exists(self):
        marker = "AIRO_ADMIN_COMMAND_SAFE_REJECT_BEFORE_FINANCE_PARSE_V1"
        self.assertIn(marker, self.source)
        self.assertIn(marker, self.v2)
        self.assertIn("unknown_admin_command_safe_reject", self.source)

    def test_hard_guard_is_before_special_command_and_before_parse_finance(self):
        hard_guard = self.source.index("AIRO_SPRINT5_ADMIN_RECONCILIATION_DOPOST_HARD_GUARD_V1")
        special = self.source.index("const specialCommand = handleSpecialFinanceCommand_(rawText, chatId);")
        parse = self.source.index("const parsed = parseFinanceText_(effectiveRawText);")
        self.assertLess(hard_guard, special)
        self.assertLess(hard_guard, parse)

    def test_hard_guard_returns_json_without_transaction_write(self):
        block = self.source[
            self.source.index("AIRO_SPRINT5_ADMIN_RECONCILIATION_DOPOST_HARD_GUARD_V1"):
            self.source.index("const specialCommand = handleSpecialFinanceCommand_(rawText, chatId);")
        ]
        self.assertIn("airoSprint5ReconciliationReadOnly_", block)
        self.assertIn("write_performed: false", block)
        self.assertIn("google_write_performed: false", block)
        self.assertIn("return json_", block)
        self.assertNotIn("writeRouted_", block)
        self.assertNotIn("appendByHeader_", block)

    def test_doc_records_live_miss_and_bad_artifact(self):
        self.assertIn("was incorrectly parsed as a normal finance transaction", self.doc)
        self.assertIn("Amount: Rp5", self.doc)
        self.assertIn("Do not approve this row", self.doc)
        self.assertIn("sprint5` became amount Rp5", self.current)


if __name__ == "__main__":
    unittest.main()
