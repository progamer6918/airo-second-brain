#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, pathlib, sys, unittest

REPO = pathlib.Path(__file__).resolve().parents[2]
SYNC = REPO / "scripts/personal-workflow/airo_full_auto_sheets_sync.py"

def load_module():
    spec = importlib.util.spec_from_file_location("airo_full_auto_sheets_sync", SYNC)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module

class FakeClient:
    def __init__(self):
        self.appended = []
        self.appended_range = []
        self.updated = []
    def append_values(self, tab, values):
        self.appended.append((tab, values))
    def append_values_to_range(self, tab, range_name, values):
        self.appended_range.append((tab, range_name, values))
    def update_values(self, tab, row_number, values):
        self.updated.append((tab, row_number, values))

class TestV13WritePath(unittest.TestCase):
    def setUp(self):
        self.m = load_module()

    def test_filter_allows_v13_tabs(self):
        preview = {"decisions": [
            {"target_tab": "🧾 Review Queue", "preview_action": "insert_candidate"},
            {"target_tab": "💵 Cash Ledger", "preview_action": "insert_candidate"},
            {"target_tab": "🏠 Cicilan Rumah", "preview_action": "insert_candidate"},
            {"target_tab": "🤝 Hutang", "preview_action": "insert_candidate"},
        ]}
        got = self.m.filter_write_decisions(preview)
        self.assertEqual([x["target_tab"] for x in got], ["🧾 Review Queue","💵 Cash Ledger","🏠 Cicilan Rumah","🤝 Hutang"])

    def test_headers_exist(self):
        self.assertIn("queue_id", self.m.target_headers("🧾 Review Queue"))
        self.assertIn("session_id", self.m.target_headers("💵 Cash Ledger", "cash_session"))
        self.assertIn("entry_id", self.m.target_headers("💵 Cash Ledger", "cash_entry"))
        self.assertIn("payment_id", self.m.target_headers("🏠 Cicilan Rumah"))
        self.assertIn("debt_id", self.m.target_headers("🤝 Hutang"))

    def test_apply_review_queue(self):
        c = FakeClient()
        d = {"target_tab":"🧾 Review Queue","preview_action":"insert_candidate","duplicate_key":"review:test","row_preview":{"queue_id":"rq1","status":"pending_review"}}
        r = self.m.apply_decision(c, {}, d, "run1")
        self.assertEqual(r.status, "success")
        self.assertEqual(c.appended[0][0], "🧾 Review Queue")

    def test_apply_cash_entry_range(self):
        c = FakeClient()
        d = {"target_tab":"💵 Cash Ledger","section":"cash_entry","preview_action":"insert_candidate","duplicate_key":"cash:test","row_preview":{"entry_id":"ce1","amount":20000,"category":"Makan"}}
        r = self.m.apply_decision(c, {}, d, "run1")
        self.assertEqual(r.status, "success")
        self.assertEqual(c.appended_range[0][0], "💵 Cash Ledger")
        self.assertEqual(c.appended_range[0][1], "J2:T")

if __name__ == "__main__":
    unittest.main()
