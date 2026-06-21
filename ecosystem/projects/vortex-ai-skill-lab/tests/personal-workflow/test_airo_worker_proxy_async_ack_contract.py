from pathlib import Path
import unittest


WORKER = Path("workers/airo-finance-telegram-proxy/src/index.js")
DOC = Path("docs/AIRO_FINANCE_WORKER_PROXY_REPAIR_2026-05-26.md")
CURRENT = Path("docs/AIRO_FINANCE_CURRENT_STATE.md")


class AiroWorkerProxyAsyncAckContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.worker = WORKER.read_text(encoding="utf-8")
        cls.doc = DOC.read_text(encoding="utf-8")
        cls.current = CURRENT.read_text(encoding="utf-8")

    def test_worker_source_exists_and_uses_modules_syntax(self):
        self.assertIn("export default", self.worker)
        self.assertIn("async fetch(request, env, ctx)", self.worker)

    def test_worker_uses_apps_script_url_secret(self):
        self.assertIn("env.APPS_SCRIPT_URL", self.worker)
        self.assertIn("missing_apps_script_url", self.worker)

    def test_worker_forwards_post_body_without_finance_parsing(self):
        self.assertIn("const body = await request.text()", self.worker)
        self.assertIn("fetch(target", self.worker)
        self.assertIn("body,", self.worker)
        self.assertNotIn("parseFinanceText_", self.worker)
        self.assertNotIn("Review Queue", self.worker)
        self.assertNotIn("writeRouted_", self.worker)

    def test_worker_returns_async_ack(self):
        self.assertIn("ctx.waitUntil", self.worker)
        self.assertIn('mode: "async_ack"', self.worker)

    def test_doc_records_repair_and_bad_artifacts(self):
        self.assertIn("Worker proxy repair", self.doc)
        self.assertIn("Two Review Queue rows", self.doc)
        self.assertIn("Do not approve them", self.doc)
        self.assertIn("Sprint 5 Worker proxy repair", self.current)


if __name__ == "__main__":
    unittest.main()
