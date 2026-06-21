#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import pathlib
import subprocess
import sys
import unittest

REPO = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts/personal-workflow/airo_cicilan_rumah_planner.py"


def load_module():
    spec = importlib.util.spec_from_file_location("airo_cicilan_rumah_planner", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class AiroCicilanRumahPlannerTest(unittest.TestCase):
    def test_default_amount_payment_candidate(self) -> None:
        module = load_module()
        plan = module.plan_cicilan_rumah("hari ini sudah bayar cicilan rumah", now_iso="2026-05-11T00:00:00+00:00")
        self.assertFalse(plan["route_to_review"])
        self.assertEqual(plan["target_tab"], "🏠 Cicilan Rumah")
        self.assertEqual(plan["operation"], "cicilan_rumah_payment_candidate")
        self.assertEqual(plan["normalized"]["amount"], 1570000)
        self.assertTrue(plan["normalized"]["amount_was_defaulted"])
        self.assertEqual(plan["normalized"]["next_cicilan_ke"], 54)

    def test_explicit_amount_payment_candidate(self) -> None:
        module = load_module()
        plan = module.plan_cicilan_rumah("bayar cicilan rumah 1543000", latest_paid_count=60, now_iso="2026-05-11T00:00:00+00:00")
        self.assertFalse(plan["route_to_review"])
        self.assertEqual(plan["normalized"]["amount"], 1543000)
        self.assertFalse(plan["normalized"]["amount_was_defaulted"])
        self.assertEqual(plan["normalized"]["next_cicilan_ke"], 61)

    def test_no_default_amount_routes_to_review_when_amount_missing(self) -> None:
        module = load_module()
        plan = module.plan_cicilan_rumah("bayar cicilan rumah", allow_default_amount=False, now_iso="2026-05-11T00:00:00+00:00")
        self.assertTrue(plan["route_to_review"])
        self.assertEqual(plan["target_tab"], "🧾 Review Queue")
        self.assertIn("missing_amount", plan["ambiguity_reasons"])

    def test_non_cicilan_message_routes_to_review(self) -> None:
        module = load_module()
        plan = module.plan_cicilan_rumah("bayar sesuatu 100rb", now_iso="2026-05-11T00:00:00+00:00")
        self.assertTrue(plan["route_to_review"])
        self.assertIn("not_cicilan_rumah_message", plan["ambiguity_reasons"])

    def test_json_cli_is_safe_and_valid(self) -> None:
        proc = subprocess.run([sys.executable, str(SCRIPT), "hari ini sudah bayar cicilan rumah", "--json"], check=True, text=True, stdout=subprocess.PIPE)
        data = json.loads(proc.stdout)
        self.assertFalse(data["route_to_review"])
        self.assertEqual(data["target_tab"], "🏠 Cicilan Rumah")
        self.assertEqual(data["normalized"]["next_cicilan_ke"], 54)
        self.assertFalse(data["google_write_performed"])
        self.assertFalse(data["sqlite_mutation_performed"])
        self.assertFalse(data["credential_read_performed"])
        self.assertFalse(data["openclaw_restart_performed"])


if __name__ == "__main__":
    unittest.main()
