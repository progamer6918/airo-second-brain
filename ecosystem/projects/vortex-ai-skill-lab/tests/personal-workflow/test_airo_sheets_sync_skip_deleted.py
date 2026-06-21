from pathlib import Path
import importlib.util
import sys

MODULE = Path(__file__).resolve().parents[2] / "scripts" / "personal-workflow" / "airo_sheets_sync_dry_run.py"
spec = importlib.util.spec_from_file_location("airo_sheets_sync_dry_run", MODULE)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


class FakeDeletedRow(dict):
    def keys(self):
        return super().keys()


def test_plan_transaction_skips_soft_deleted_row():
    row = FakeDeletedRow({"deleted_at": "2026-05-10 16:20:20"})
    assert mod.plan_transaction(row, {}) == []
