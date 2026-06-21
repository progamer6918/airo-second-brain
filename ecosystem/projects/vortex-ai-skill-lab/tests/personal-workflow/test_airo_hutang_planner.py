#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import pathlib
import subprocess
import sys
import unittest

REPO = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts/personal-workflow/airo_hutang_planner.py"


def load_module():
    spec = importlib.util.spec_from_file_location("airo_hutang_planner", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class AiroHutangPlannerTest(unittest.TestCase):
    def test_mamak_egit_payment_candidate(self) -> None:
        module = load_module()
        plan = module.plan_hutang("hari ini bayar hutang ke mamak egit 1 juta", now_iso="2026-05-11T00:00:00+00:00")
        self.assertFalse(plan["route_to_review"])
        self.assertEqual(plan["target_tab"], "🤝 Hutang")
        self.assertEqual(plan["operation"], "hutang_payment_candidate")
        self.assertEqual(plan["normalized"]["debt_id"], "HT-001")
        self.assertEqual(plan["normalized"]["creditor"], "Mamak Egit")
        self.assertEqual(plan["normalized"]["amount"], 1000000)
        self.assertEqual(plan["normalized"]["balance_before"], 15000000)
        self.assertEqual(plan["normalized"]["balance_after"], 14000000)

    def test_bapak_egit_payment_candidate_with_account(self) -> None:
        module = load_module()
        plan = module.plan_hutang("bayar hutang ke bapak egit 500rb pakai bca", now_iso="2026-05-11T00:00:00+00:00")
        self.assertFalse(plan["route_to_review"])
        self.assertEqual(plan["normalized"]["debt_id"], "HT-002")
        self.assertEqual(plan["normalized"]["account"], "BCA")
        self.assertEqual(plan["normalized"]["balance_after"], 4500000)

    def test_unknown_person_routes_to_review(self) -> None:
        module = load_module()
        plan = module.plan_hutang("bayar hutang 1 juta pakai bca", now_iso="2026-05-11T00:00:00+00:00")
        self.assertTrue(plan["route_to_review"])
        self.assertEqual(plan["target_tab"], "🧾 Review Queue")
        self.assertIn("debt_person_unclear", plan["ambiguity_reasons"])

    def test_missing_amount_routes_to_review(self) -> None:
        module = load_module()
        plan = module.plan_hutang("bayar hutang ke mamak nurul", now_iso="2026-05-11T00:00:00+00:00")
        self.assertTrue(plan["route_to_review"])
        self.assertIn("missing_amount", plan["ambiguity_reasons"])

    def test_json_cli_is_safe_and_valid(self) -> None:
        proc = subprocess.run([sys.executable, str(SCRIPT), "bayar hutang ke mamak egit 1 juta", "--json"], check=True, text=True, stdout=subprocess.PIPE)
        data = json.loads(proc.stdout)
        self.assertFalse(data["route_to_review"])
        self.assertEqual(data["target_tab"], "🤝 Hutang")
        self.assertEqual(data["normalized"]["balance_after"], 14000000)
        self.assertFalse(data["google_write_performed"])
        self.assertFalse(data["sqlite_mutation_performed"])
        self.assertFalse(data["credential_read_performed"])
        self.assertFalse(data["openclaw_restart_performed"])


if __name__ == "__main__":
    unittest.main()
