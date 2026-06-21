#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import pathlib
import subprocess
import sys
import unittest


REPO = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts/personal-workflow/airo_finance_sheet_v12_status.py"


def load_module():
    spec = importlib.util.spec_from_file_location("airo_finance_sheet_v12_status", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class AiroFinanceSheetV12StatusTest(unittest.TestCase):
    def test_payload_has_exactly_11_tabs(self) -> None:
        module = load_module()
        data = module.payload()
        self.assertEqual(data["tab_count"], 11)
        self.assertEqual(len(data["tabs"]), 11)

    def test_required_tabs_are_present(self) -> None:
        module = load_module()
        tabs = {row["tab"] for row in module.payload()["tabs"]}
        self.assertEqual(
            tabs,
            {
                "🏠 Dashboard",
                "💸 Transactions",
                "💵 Cash Ledger",
                "💳 Credit Card",
                "🏠 Cicilan Rumah",
                "🤝 Hutang",
                "🥇 Aset",
                "📅 Monthly Review",
                "🧾 Review Queue",
                "⚙️ Settings",
                "🔄 Sync Log",
            },
        )

    def test_focus_contains_remaining_completion_tabs(self) -> None:
        module = load_module()
        focus = {row["tab"] for row in module.payload()["v12_focus"]}
        self.assertIn("💵 Cash Ledger", focus)
        self.assertIn("🏠 Cicilan Rumah", focus)
        self.assertIn("🤝 Hutang", focus)
        self.assertIn("🧾 Review Queue", focus)
        self.assertIn("📅 Monthly Review", focus)

    def test_dry_run_mapper_ready_tabs_are_marked(self) -> None:
        module = load_module()
        by_tab = {row["tab"]: row["status"] for row in module.payload()["tabs"]}
        self.assertEqual(by_tab["💵 Cash Ledger"], "FULL_AUTO_WRITE_PATH_READY")
        self.assertEqual(by_tab["🏠 Cicilan Rumah"], "FULL_AUTO_WRITE_PATH_READY")
        self.assertEqual(by_tab["🤝 Hutang"], "FULL_AUTO_WRITE_PATH_READY")
        self.assertEqual(by_tab["🧾 Review Queue"], "FULL_AUTO_WRITE_PATH_READY")


    def test_json_cli_is_valid(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--json"],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )
        data = json.loads(proc.stdout)
        self.assertEqual(data["tab_count"], 11)
        self.assertFalse(data["safety"]["google_write_performed"])
        self.assertFalse(data["safety"]["sqlite_mutation_performed"])
        self.assertFalse(data["safety"]["credential_read_performed"])
        self.assertFalse(data["safety"]["openclaw_restart_performed"])


if __name__ == "__main__":
    unittest.main()
