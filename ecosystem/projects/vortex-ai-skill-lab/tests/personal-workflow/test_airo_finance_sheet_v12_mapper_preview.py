#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import pathlib
import subprocess
import sys
import unittest

REPO = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts/personal-workflow/airo_finance_sheet_v12_mapper_preview.py"


def load_module():
    spec = importlib.util.spec_from_file_location("airo_finance_sheet_v12_mapper_preview", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class AiroFinanceSheetV12MapperPreviewTest(unittest.TestCase):
    def test_cash_entry_maps_to_cash_ledger(self) -> None:
        module = load_module()
        payload = module.mapper_preview("hari ini cash kepake beli makan 20rb")
        self.assertEqual(payload["target_tab"], "💵 Cash Ledger")
        self.assertEqual(payload["mapper_operation"], "planner_tab_preview_candidate")
        self.assertFalse(payload["route_to_review"])

    def test_cicilan_maps_to_cicilan_rumah(self) -> None:
        module = load_module()
        payload = module.mapper_preview("hari ini sudah bayar cicilan rumah")
        self.assertEqual(payload["target_tab"], "🏠 Cicilan Rumah")
        self.assertEqual(payload["planner_operation"], "cicilan_rumah_payment_candidate")
        self.assertFalse(payload["route_to_review"])

    def test_hutang_maps_to_hutang(self) -> None:
        module = load_module()
        payload = module.mapper_preview("hari ini bayar hutang ke mamak egit 1 juta")
        self.assertEqual(payload["target_tab"], "🤝 Hutang")
        self.assertEqual(payload["planner_operation"], "hutang_payment_candidate")
        self.assertFalse(payload["route_to_review"])

    def test_ambiguous_maps_to_review_queue(self) -> None:
        module = load_module()
        payload = module.mapper_preview("kayaknya bayar sesuatu kemarin", confidence=0.30)
        self.assertTrue(payload["route_to_review"])
        self.assertEqual(payload["target_tab"], "🧾 Review Queue")
        self.assertEqual(payload["mapper_operation"], "review_queue_preview_candidate")

    def test_existing_core_transaction_preview(self) -> None:
        module = load_module()
        payload = module.mapper_preview("catat beli makan 50k pakai blu", confidence=0.95)
        self.assertFalse(payload["route_to_review"])
        self.assertEqual(payload["target_tab"], "💸 Transactions")
        self.assertEqual(payload["target_tabs"], ["💸 Transactions"])
        self.assertEqual(payload["mapper_operation"], "existing_core_route_preview")

    def test_json_cli_is_safe_and_valid(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "hari ini cash kepake beli makan 20rb", "--json"],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["target_tab"], "💵 Cash Ledger")
        self.assertFalse(payload["google_write_performed"])
        self.assertFalse(payload["sqlite_mutation_performed"])
        self.assertFalse(payload["credential_read_performed"])
        self.assertFalse(payload["openclaw_restart_performed"])


if __name__ == "__main__":
    unittest.main()
