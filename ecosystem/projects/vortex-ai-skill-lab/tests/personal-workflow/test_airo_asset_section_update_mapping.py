from pathlib import Path
import importlib.util
import sys

MODULE = Path(__file__).resolve().parents[2] / "scripts" / "personal-workflow" / "airo_full_auto_sheets_sync.py"
spec = importlib.util.spec_from_file_location("airo_full_auto_sheets_sync", MODULE)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def test_asset_snapshot_lookup_key_uses_section():
    assert mod.snapshot_lookup_key("🥇 Aset", "savings_transfer_ledger") == "🥇 Aset::savings_transfer_ledger"
    assert mod.snapshot_lookup_key("🥇 Aset", "gold_ledger") == "🥇 Aset::gold_ledger"
    assert mod.snapshot_lookup_key("💸 Transactions", "") == "💸 Transactions"


def test_find_existing_row_for_asset_section():
    snapshot = {
        "tabs": {
            "🥇 Aset::savings_transfer_ledger": [
                {"duplicate_key": "sav_d78b1a231bb6", "row_number": 6, "sync_hash": "old"},
            ],
            "🥇 Aset": [],
        }
    }
    assert mod.find_existing_row(snapshot, "🥇 Aset", "sav_d78b1a231bb6", "savings_transfer_ledger") == 6
    assert mod.find_existing_row(snapshot, "🥇 Aset", "sav_d78b1a231bb6", "") is None


def test_asset_update_range():
    assert mod.asset_update_range("savings_transfer_ledger", 6) == "O6:Z6"
    assert mod.asset_update_range("gold_ledger", 25) == "A25:M25"


def test_filter_write_decisions_includes_asset_update_candidate():
    preview = {
        "decisions": [
            {"target_tab": "🥇 Aset", "preview_action": "update_candidate", "duplicate_key": "sav_x"},
            {"target_tab": "🥇 Aset", "preview_action": "skip_duplicate", "duplicate_key": "sav_y"},
        ]
    }
    out = mod.filter_write_decisions(preview)
    assert len(out) == 1
    assert out[0]["duplicate_key"] == "sav_x"
