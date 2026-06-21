from pathlib import Path
import unittest

SOURCE = Path("scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs")

class Sprint6ReconciliationChecksVerifierTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SOURCE.read_text(encoding="utf-8")

    def test_reconciliation_contains_new_metrics(self):
        required_metrics = [
            "review_queue_pending_count",
            "review_queue_missing_status_count",
            "blank_category_count",
            "blank_category_count_active",
            "blank_category_count_legacy",
            "cc_unprepared_count",
            "unmatched_cc_payment_count",
            "cc_unprepared_count_active",
            "cc_unprepared_count_legacy",
            "unmatched_cc_payment_count_active",
            "unmatched_cc_payment_count_legacy",
            "overdue_unmatched_cc_payment_count",
            "overdue_unmatched_cc_payment_count_active",
            "overdue_unmatched_cc_payment_count_legacy",
            "cutover_date"
        ]
        for metric in required_metrics:
            self.assertIn(metric, self.source)

    def test_reconciliation_uses_reconciliation_cutover_date(self):
        self.assertIn("reconciliationCutoverDate = '2026-05-15'", self.source)

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
