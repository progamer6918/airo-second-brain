from pathlib import Path
import unittest

SOURCE = Path("scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs")

class Sprint6ReconciliationDashboardWiringVerifierTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SOURCE.read_text(encoding="utf-8")

    def test_dashboard_analytics_contains_wiring_variables(self):
        body = self._function_body(self.source, "airoBuildSprint5DashboardAnalytics_")
        required_wiring = [
            "review_queue_pending_count_active",
            "review_queue_pending_count_legacy",
            "review_queue_missing_status_count_active",
            "review_queue_missing_status_count_legacy",
            "blank_category_count_active",
            "blank_category_count_legacy",
            "cc_unprepared_count_active",
            "cc_unprepared_count_legacy",
            "overdue_unmatched_cc_payment_count_active",
            "overdue_unmatched_cc_payment_count_legacy",
        ]
        for key in required_wiring:
            self.assertIn(key, body)

    def test_dashboard_analytics_defines_expected_action_keys(self):
        body = self._function_body(self.source, "airoBuildSprint5DashboardAnalytics_")
        required_actions = [
            "active_cc_overdue_unmatched",
            "active_cc_unprepared",
            "active_review_queue_pending",
            "active_review_queue_missing_status",
            "active_blank_category",
        ]
        for key in required_actions:
            self.assertIn(key, body)

    def test_wiring_has_correct_severity_classifications(self):
        body = self._function_body(self.source, "airoBuildSprint5DashboardAnalytics_")
        # Overdue unmatched CC must be CRITICAL
        self.assertIn("key: 'active_cc_overdue_unmatched'", body)
        self.assertIn("severity: 'CRITICAL'", body)
        
        # CC Unprepared, RQ Pending, RQ Missing Status, Blank Category must be WARNING
        self.assertIn("key: 'active_cc_unprepared'", body)
        self.assertIn("key: 'active_review_queue_pending'", body)
        self.assertIn("key: 'active_review_queue_missing_status'", body)
        self.assertIn("key: 'active_blank_category'", body)
        self.assertIn("severity: 'WARNING'", body)

    def test_helper_body_has_no_write_operations(self):
        body = self._function_body(self.source, "airoBuildSprint5DashboardAnalytics_")
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
