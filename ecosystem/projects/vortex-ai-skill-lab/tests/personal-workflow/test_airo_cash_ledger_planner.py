#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import pathlib
import subprocess
import sys
import unittest

REPO = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts/personal-workflow/airo_cash_ledger_planner.py"


def load_module():
    spec = importlib.util.spec_from_file_location("airo_cash_ledger_planner", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class AiroCashLedgerPlannerTest(unittest.TestCase):
    def test_cash_session_candidate(self) -> None:
        module = load_module()
        plan = module.plan_cash_ledger("saya hari ini pegang cash 100rb", now_iso="2026-05-11T00:00:00+00:00")
        self.assertFalse(plan["route_to_review"])
        self.assertEqual(plan["target_tab"], "💵 Cash Ledger")
        self.assertEqual(plan["cash_type"], "cash_session")
        self.assertEqual(plan["operation"], "cash_session_candidate")
        self.assertEqual(plan["normalized"]["amount"], 100000)
        self.assertEqual(plan["normalized"]["account"], "Cash")

    def test_cash_entry_candidate(self) -> None:
        module = load_module()
        plan = module.plan_cash_ledger("hari ini cash kepake beli makan 20rb", now_iso="2026-05-11T00:00:00+00:00")
        self.assertFalse(plan["route_to_review"])
        self.assertEqual(plan["target_tab"], "💵 Cash Ledger")
        self.assertEqual(plan["cash_type"], "cash_entry")
        self.assertEqual(plan["operation"], "cash_entry_candidate")
        self.assertEqual(plan["normalized"]["amount"], 20000)
        self.assertEqual(plan["normalized"]["category"], "Makan")

    def test_cash_entry_missing_category_routes_to_review(self) -> None:
        module = load_module()
        plan = module.plan_cash_ledger("cash kepake 20rb", now_iso="2026-05-11T00:00:00+00:00")
        self.assertTrue(plan["route_to_review"])
        self.assertEqual(plan["target_tab"], "🧾 Review Queue")
        self.assertIn("missing_cash_entry_category", plan["ambiguity_reasons"])

    def test_cash_unknown_routes_to_review(self) -> None:
        module = load_module()
        plan = module.plan_cash_ledger("cash tadi gimana ya", now_iso="2026-05-11T00:00:00+00:00")
        self.assertTrue(plan["route_to_review"])
        self.assertEqual(plan["target_tab"], "🧾 Review Queue")
        self.assertIn("cash_intent_unclear", plan["ambiguity_reasons"])

    def test_json_cli_is_safe_and_valid(self) -> None:
        proc = subprocess.run([sys.executable, str(SCRIPT), "cash kepake beli makan 20rb", "--json"], check=True, text=True, stdout=subprocess.PIPE)
        data = json.loads(proc.stdout)
        self.assertFalse(data["route_to_review"])
        self.assertEqual(data["target_tab"], "💵 Cash Ledger")
        self.assertFalse(data["google_write_performed"])
        self.assertFalse(data["sqlite_mutation_performed"])
        self.assertFalse(data["credential_read_performed"])
        self.assertFalse(data["openclaw_restart_performed"])


if __name__ == "__main__":
    unittest.main()
