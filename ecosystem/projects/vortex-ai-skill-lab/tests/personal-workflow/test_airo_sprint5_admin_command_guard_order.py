from pathlib import Path
import unittest


SOURCE = Path("scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs")
V2_SOURCE = Path("apps-script-prod-v2/AIRO_Finance_Multitab_Final_v1.js")
DOC = Path("docs/AIRO_FINANCE_SPRINT_5_ADMIN_COMMAND_GUARD_ORDER_FIX.md")


class Sprint5AdminCommandGuardOrderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SOURCE.read_text(encoding="utf-8")
        cls.v2 = V2_SOURCE.read_text(encoding="utf-8")
        cls.doc = DOC.read_text(encoding="utf-8")

    def test_markers_exist(self):
        required = [
            "AIRO_SPRINT5_ADMIN_RECONCILIATION_DOPOST_HARD_GUARD_V1",
            "AIRO_ADMIN_COMMAND_SAFE_REJECT_BEFORE_FINANCE_PARSE_V1",
            "const specialCommand = handleSpecialFinanceCommand_(rawText, chatId);",
            "const parsed = parseFinanceText_(effectiveRawText);",
        ]
        for phrase in required:
            self.assertIn(phrase, self.source)
            self.assertIn(phrase, self.v2)

    def test_order_is_hard_guard_then_special_then_unknown_admin_reject_then_parse(self):
        hard_guard = self.source.index("AIRO_SPRINT5_ADMIN_RECONCILIATION_DOPOST_HARD_GUARD_V1")
        special = self.source.index("const specialCommand = handleSpecialFinanceCommand_(rawText, chatId);")
        safe_reject = self.source.index("AIRO_ADMIN_COMMAND_SAFE_REJECT_BEFORE_FINANCE_PARSE_V1")
        parse = self.source.index("const parsed = parseFinanceText_(effectiveRawText);")

        self.assertLess(hard_guard, special)
        self.assertLess(special, safe_reject)
        self.assertLess(safe_reject, parse)

    def test_v2_order_matches_canonical(self):
        hard_guard = self.v2.index("AIRO_SPRINT5_ADMIN_RECONCILIATION_DOPOST_HARD_GUARD_V1")
        special = self.v2.index("const specialCommand = handleSpecialFinanceCommand_(rawText, chatId);")
        safe_reject = self.v2.index("AIRO_ADMIN_COMMAND_SAFE_REJECT_BEFORE_FINANCE_PARSE_V1")
        parse = self.v2.index("const parsed = parseFinanceText_(effectiveRawText);")

        self.assertLess(hard_guard, special)
        self.assertLess(special, safe_reject)
        self.assertLess(safe_reject, parse)

    def test_known_admin_find_route_still_exists(self):
        self.assertIn("AIRO_ADMIN_FIND_SMOKE_COMMAND_V1", self.source)
        self.assertIn("admin\\s+(find|cari)\\s+(smoke|text)", self.source)

    def test_unknown_admin_reject_still_prevents_finance_parse(self):
        safe_reject = self.source.index("AIRO_ADMIN_COMMAND_SAFE_REJECT_BEFORE_FINANCE_PARSE_V1")
        parse = self.source.index("const parsed = parseFinanceText_(effectiveRawText);")
        block = self.source[safe_reject:parse]
        self.assertIn("unknown_admin_command_safe_reject", block)
        self.assertIn("write_performed: false", block)
        self.assertIn("google_write_performed: false", block)
        self.assertIn("return json_", block)

    def test_doc_records_cleanup_reason(self):
        self.assertIn("known admin commands", self.doc)
        self.assertIn("Three Review Queue rows", self.doc)
        self.assertIn("Do not approve them", self.doc)


if __name__ == "__main__":
    unittest.main()
