from pathlib import Path
import unittest


DOC = Path("docs/AIRO_FINANCE_SPRINT_5_RECONCILIATION_LIVE_PASS.md")
CURRENT = Path("docs/AIRO_FINANCE_CURRENT_STATE.md")
WORKER = Path("workers/airo-finance-telegram-proxy/src/index.js")


class Sprint5ReconciliationLivePassRecordTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = DOC.read_text(encoding="utf-8")
        cls.current = CURRENT.read_text(encoding="utf-8")
        cls.worker = WORKER.read_text(encoding="utf-8")

    def test_live_pass_records_read_only_result(self):
        self.assertIn("LIVE PASS - READ-ONLY RECONCILIATION HELPER", self.doc)
        self.assertIn("Mode: read-only", self.doc)
        self.assertIn("Write performed: false", self.doc)

    def test_live_pass_records_current_webhook(self):
        self.assertIn("https://airo-finance-telegram-proxy.earnsai.workers.dev", self.doc)
        self.assertIn("https://airo-finance-telegram-proxy.earnsai.workers.dev", self.current)

    def test_live_pass_records_old_worker_warning(self):
        self.assertIn("https://airo-finance-telegram-proxy.progamer6918.workers.dev", self.doc)
        self.assertIn("target deployment @192", self.doc)

    def test_live_pass_records_audit_numbers(self):
        required = [
            "Rows: 61",
            "Missing linked_txn_id: 37",
            "Lainnya category rows: 24",
            "Rows: 10",
            "Account without Finance Event: 61",
            "Issue count: 98",
            "needs_review",
        ]
        for phrase in required:
            self.assertIn(phrase, self.doc)

    def test_live_pass_records_bad_artifacts(self):
        self.assertIn("three Review Queue rows", self.doc)
        self.assertIn("Amount: Rp5", self.doc)
        self.assertIn("Do not approve those rows", self.doc)
        self.assertIn("Three Review Queue rows", self.current)

    def test_worker_contract_still_async_proxy(self):
        self.assertIn("env.APPS_SCRIPT_URL", self.worker)
        self.assertIn("ctx.waitUntil", self.worker)
        self.assertIn('mode: "async_ack"', self.worker)


if __name__ == "__main__":
    unittest.main()
