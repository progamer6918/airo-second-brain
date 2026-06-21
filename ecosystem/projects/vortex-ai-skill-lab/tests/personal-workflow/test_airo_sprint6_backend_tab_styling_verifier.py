from pathlib import Path
import unittest

SOURCE = Path("scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs")

class Sprint6BackendTabStylingVerifierTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SOURCE.read_text(encoding="utf-8")

    def test_style_helpers_exist(self):
        for name in [
            "styleFinanceEventsSheet_",
            "styleReviewQueueSheet_",
            "styleAuditLogSheet_",
            "airoStyleBackendTabs_",
        ]:
            self.assertIn(f"function {name}(", self.source)

    def test_style_helpers_are_formatting_only(self):
        forbidden = [
            ".setValue(",
            ".setValues(",
            ".appendRow(",
            ".deleteRow(",
            ".deleteColumn(",
            ".insertRow(",
            ".insertColumn(",
            ".clear(",
            ".clearContent(",
            ".setFormula(",
            "appendByHeader_(",
            "writeFinanceEvent_(",
            "writeAccountLedgerMirror_(",
            "safeClearRange_(",
        ]
        for name in ["styleFinanceEventsSheet_", "styleReviewQueueSheet_", "styleAuditLogSheet_"]:
            body = self._function_body(self.source, name)
            for phrase in forbidden:
                self.assertNotIn(phrase, body, msg=f"Helper {name} contains forbidden write method: {phrase}")

    def test_style_helpers_use_correct_styling_apis(self):
        for name in ["styleFinanceEventsSheet_", "styleReviewQueueSheet_", "styleAuditLogSheet_"]:
            body = self._function_body(self.source, name)
            self.assertIn("setBackground", body)
            self.assertIn("setFontColor", body)
            self.assertIn("setFontWeight", body)
            self.assertIn("setHorizontalAlignment", body)
            self.assertIn("setVerticalAlignment", body)
            self.assertIn("setWrap", body)
            self.assertIn("setColumnWidth", body)
            self.assertIn("setFrozenRows", body)

    def test_style_helpers_use_correct_hex_colors(self):
        fe_body = self._function_body(self.source, "styleFinanceEventsSheet_")
        rq_body = self._function_body(self.source, "styleReviewQueueSheet_")
        au_body = self._function_body(self.source, "styleAuditLogSheet_")

        self.assertIn("#2F5597", fe_body.upper())
        self.assertIn("#C68B2C", rq_body.upper())
        self.assertIn("#5A5A5A", au_body.upper())

    def test_style_helpers_do_not_swallow_errors(self):
        for name in ["styleFinanceEventsSheet_", "styleReviewQueueSheet_", "styleAuditLogSheet_"]:
            body = self._function_body(self.source, name)
            self.assertNotIn("catch", body, msg=f"Helper {name} must propagate errors instead of catching them internally.")

    def test_wrapper_catches_and_reports_errors(self):
        body = self._function_body(self.source, "airoStyleBackendTabs_")
        self.assertIn("catch (e)", body)
        self.assertIn("'error: ' + e.message", body)

    def test_defensive_range_checks_present(self):
        for name in ["styleFinanceEventsSheet_", "styleReviewQueueSheet_", "styleAuditLogSheet_"]:
            body = self._function_body(self.source, name)
            self.assertIn("getMaxColumns()", body)
            self.assertIn("Math.min(", body)
            # Ensure no hardcoded column letter ranges are used
            self.assertNotIn("getRange('", body)
            self.assertNotIn('getRange("', body)

    def test_admin_command_route_matches(self):
        body = self._function_body(self.source, "handleSpecialFinanceCommand_")
        self.assertIn("admin style backend tabs", body)
        self.assertIn("admin format backend tabs", body)
        self.assertIn("airoStyleBackendTabs_", body)

    def test_no_auto_styling_wired_into_write_paths(self):
        for name in ["appendByHeader_", "processReviewQueueApproved"]:
            body = self._function_body(self.source, name)
            for helper in ["styleFinanceEventsSheet_", "styleReviewQueueSheet_", "styleAuditLogSheet_", "airoStyleBackendTabs_"]:
                self.assertNotIn(helper, body, msg=f"Write path function {name} must not call style helper {helper}")

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
