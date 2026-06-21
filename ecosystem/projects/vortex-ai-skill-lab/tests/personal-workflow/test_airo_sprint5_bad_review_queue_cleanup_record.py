from pathlib import Path
import unittest


DOC = Path("docs/AIRO_FINANCE_SPRINT_5_BAD_REVIEW_QUEUE_CLEANUP.md")
CURRENT = Path("docs/AIRO_FINANCE_CURRENT_STATE.md")


class Sprint5BadReviewQueueCleanupRecordTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = DOC.read_text(encoding="utf-8")
        cls.current = CURRENT.read_text(encoding="utf-8")

    def test_cleanup_doc_records_bad_rows(self):
        for phrase in [
            "Review Queue row 50",
            "Review Queue row 51",
            "Review Queue row 52",
            "admin audit sprint5 reconciliation",
            "Amount: Rp5",
        ]:
            self.assertIn(phrase, self.doc)

    def test_cleanup_doc_preserves_finance_events_trail(self):
        for phrase in [
            "Finance Events row 9",
            "Finance Events row 10",
            "Finance Events row 11",
            "Do not delete Finance Events rows 9, 10, or 11",
        ]:
            self.assertIn(phrase, self.doc)

    def test_current_state_records_cleanup(self):
        self.assertIn("Sprint 5 bad Review Queue cleanup recorded", self.current)
        self.assertIn("No Review Queue rows are returned by the readback", self.current)
        self.assertIn("Preserve them as incident/audit trail", self.current)

    def test_next_step_is_reconciliation_dashboard_layer(self):
        self.assertIn("reconciliation dashboard layer design", self.doc)
        self.assertIn("Sprint 5 Dashboard Analytics", self.doc)


if __name__ == "__main__":
    unittest.main()
