#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import pathlib
import subprocess
import sys
import unittest

REPO = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts/personal-workflow/airo_finance_sheet_v12_regression.py"


def load_module():
    spec = importlib.util.spec_from_file_location("airo_finance_sheet_v12_regression", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class AiroFinanceSheetV12RegressionTest(unittest.TestCase):
    def test_regression_passes(self) -> None:
        module = load_module()
        payload = module.run_regression()
        self.assertEqual(payload["status"], "PASS")
        self.assertEqual(payload["checks_failed"], 0)

    def test_json_cli_is_safe_and_valid(self) -> None:
        proc = subprocess.run([sys.executable, str(SCRIPT), "--json"], check=True, text=True, stdout=subprocess.PIPE)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["status"], "PASS")
        self.assertFalse(payload["safety"]["google_write_performed"])
        self.assertFalse(payload["safety"]["sqlite_mutation_performed"])
        self.assertFalse(payload["safety"]["credential_read_performed"])
        self.assertFalse(payload["safety"]["openclaw_restart_performed"])


if __name__ == "__main__":
    unittest.main()
