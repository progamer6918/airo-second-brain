from pathlib import Path
import unittest


SOURCE = Path("scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs")
V2_SOURCE = Path("apps-script-prod-v2/AIRO_Finance_Multitab_Final_v1.js")
DOC = Path("docs/AIRO_FINANCE_SPRINT_5_READ_ONLY_RECONCILIATION_HELPER.md")
CURRENT = Path("docs/AIRO_FINANCE_CURRENT_STATE.md")


class Sprint5ReadOnlyReconciliationHelperTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SOURCE.read_text(encoding="utf-8")
        cls.v2 = V2_SOURCE.read_text(encoding="utf-8")
        cls.doc = DOC.read_text(encoding="utf-8")
        cls.current = CURRENT.read_text(encoding="utf-8")

    def test_helper_marker_exists_in_canonical_and_v2_source(self):
        marker = "AIRO_SPRINT5_READ_ONLY_RECONCILIATION_HELPER_V1"
        self.assertIn(marker, self.source)
        self.assertIn(marker, self.v2)

    def test_admin_route_marker_exists_in_canonical_and_v2_source(self):
        marker = "AIRO_SPRINT5_READ_ONLY_RECONCILIATION_ADMIN_ROUTE_V1"
        self.assertIn(marker, self.source)
        self.assertIn(marker, self.v2)
        self.assertIn("admin\\s+(audit|check|cek)\\s+(sprint5\\s+)?reconciliation", self.source)

    def test_helper_is_declared_read_only(self):
        required = [
            "function airoSprint5ReconciliationReadOnly_",
            "write_performed: false",
            "google_write_performed: false",
            "duplicate_linked_txn_id_candidates",
            "account_without_finance_event",
            "finance_event_without_account",
            "lainnya_category_rows",
        ]
        for phrase in required:
            self.assertIn(phrase, self.source)

    def test_helper_body_has_no_write_operations(self):
        body = self._function_body(self.source, "airoSprint5ReconciliationReadOnly_")
        forbidden = [
            ".setValue(",
            ".setValues(",
            ".setFormula(",
            ".appendRow(",
            "appendByHeader_(",
            "writeFinanceEvent_(",
            "writeAccountLedgerMirror_(",
            "safeClearRange_(",
            ".clearContent(",
            ".clearFormat(",
            ".clearDataValidations(",
        ]
        for phrase in forbidden:
            self.assertNotIn(phrase, body)

    def test_reply_builder_exists(self):
        self.assertIn("function airoBuildSprint5ReconciliationReply_", self.source)
        self.assertIn("Sprint 5 reconciliation audit selesai", self.source)
        self.assertIn("Mode: read-only", self.source)

    def test_route_is_inside_special_command_handler_before_lowercase_text(self):
        handler = self._function_body(self.source, "handleSpecialFinanceCommand_")
        self.assertIn("AIRO_SPRINT5_READ_ONLY_RECONCILIATION_ADMIN_ROUTE_V1", handler)
        self.assertIn("airoSprint5ReconciliationReadOnly_", handler)
        self.assertIn("sendTelegram_", handler)

    def test_doc_records_not_deployed(self):
        self.assertIn("Status: ACTIVE - LOCAL PATCH, NOT DEPLOYED", self.doc)
        self.assertIn("The helper must not write to Google Sheets", self.doc)
        self.assertIn("A separate deploy step is required", self.doc)
        self.assertIn("No deploy in this step", self.current)

    @staticmethod
    def _function_body(source: str, name: str) -> str:
        marker = f"function {name}("
        start = source.index(marker)
        brace = source.index("{", start)
        depth = 0
        in_single = False
        in_double = False
        in_backtick = False
        escaped = False

        for i in range(brace, len(source)):
            ch = source[i]

            if escaped:
                escaped = False
                continue

            if ch == "\\":
                escaped = True
                continue

            if ch == "'" and not in_double and not in_backtick:
                in_single = not in_single
                continue

            if ch == '"' and not in_single and not in_backtick:
                in_double = not in_double
                continue

            if ch == "`" and not in_single and not in_double:
                in_backtick = not in_backtick
                continue

            if in_single or in_double or in_backtick:
                continue

            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return source[start : i + 1]

        raise AssertionError(f"Function not closed: {name}")


if __name__ == "__main__":
    unittest.main()
