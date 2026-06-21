#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import unittest

REPO = pathlib.Path(__file__).resolve().parents[2]
ROUTER = REPO / "scripts/personal-workflow/airo_intent_router.py"


class AiroIntentRouterV13FinanceForceTest(unittest.TestCase):
    def run_router(self, message: str) -> dict:
        proc = subprocess.run(
            [sys.executable, str(ROUTER), message],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )
        return json.loads(proc.stdout)

    def test_ambiguous_finance_routes_to_review_queue(self) -> None:
        data = self.run_router("kayaknya bayar sesuatu kemarin")
        self.assertEqual(data["intent"], "finance_capture")
        self.assertEqual(data["status"], "routed")
        self.assertEqual(data["target_tab"], "🧾 Review Queue")
        self.assertTrue(data["route_to_review"])

    def test_cash_finance_routes_to_cash_ledger(self) -> None:
        data = self.run_router("hari ini cash kepake beli makan 20rb")
        self.assertEqual(data["intent"], "finance_capture")
        self.assertEqual(data["target_tab"], "💵 Cash Ledger")
        self.assertFalse(data["route_to_review"])


if __name__ == "__main__":
    unittest.main()
