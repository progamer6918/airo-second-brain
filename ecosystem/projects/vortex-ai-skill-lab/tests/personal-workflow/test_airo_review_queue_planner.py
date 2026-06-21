#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import pathlib
import subprocess
import sys
import unittest

REPO = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts/personal-workflow/airo_review_queue_planner.py"


def load_module():
    spec = importlib.util.spec_from_file_location("airo_review_queue_planner", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class AiroReviewQueuePlannerTest(unittest.TestCase):
    def test_clear_transaction_does_not_need_review(self) -> None:
        module = load_module()
        plan = module.plan_review_queue("catat beli makan 50k pakai blu", confidence=0.95, now_iso="2026-05-11T00:00:00+00:00")
        self.assertFalse(plan["route_to_review"])
        self.assertEqual(plan["target_tab"], "💸 Transactions")
        self.assertEqual(plan["normalized"]["amount"], 50000)
        self.assertEqual(plan["normalized"]["account"], "BLU BCA")
        self.assertEqual(plan["normalized"]["category"], "Makan")

    def test_low_confidence_routes_to_review_queue(self) -> None:
        module = load_module()
        plan = module.plan_review_queue("kayaknya bayar sesuatu kemarin", confidence=0.30, now_iso="2026-05-11T00:00:00+00:00")
        self.assertTrue(plan["route_to_review"])
        self.assertEqual(plan["target_tab"], "🧾 Review Queue")
        self.assertIn("low_confidence", plan["ambiguity_reasons"])
        self.assertIn("missing_amount", plan["ambiguity_reasons"])

    def test_hutang_without_person_routes_to_review(self) -> None:
        module = load_module()
        plan = module.plan_review_queue("bayar hutang 1 juta pakai bca", confidence=0.95, now_iso="2026-05-11T00:00:00+00:00")
        self.assertTrue(plan["route_to_review"])
        self.assertEqual(plan["suggested_domain"], "🤝 Hutang")
        self.assertIn("debt_person_unclear", plan["ambiguity_reasons"])

    def test_cash_session_can_be_suggested(self) -> None:
        module = load_module()
        plan = module.plan_review_queue("saya hari ini pegang cash 100rb", confidence=0.95, now_iso="2026-05-11T00:00:00+00:00")
        self.assertFalse(plan["route_to_review"])
        self.assertEqual(plan["target_tab"], "💵 Cash Ledger")
        self.assertEqual(plan["normalized"]["amount"], 100000)
        self.assertEqual(plan["normalized"]["account"], "Cash")

    def test_json_cli_is_safe_and_valid(self) -> None:
        proc = subprocess.run([sys.executable, str(SCRIPT), "bayar hutang 1 juta", "--confidence", "0.40", "--json"], check=True, text=True, stdout=subprocess.PIPE)
        data = json.loads(proc.stdout)
        self.assertTrue(data["route_to_review"])
        self.assertEqual(data["target_tab"], "🧾 Review Queue")
        self.assertFalse(data["google_write_performed"])
        self.assertFalse(data["sqlite_mutation_performed"])
        self.assertFalse(data["credential_read_performed"])
        self.assertFalse(data["openclaw_restart_performed"])


if __name__ == "__main__":
    unittest.main()
