from pathlib import Path
import importlib.util
import sys

MODULE = Path(__file__).resolve().parents[2] / "scripts" / "personal-workflow" / "airo_asset_event_planner.py"
spec = importlib.util.spec_from_file_location("airo_asset_event_planner", MODULE)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def test_asset_planner_skips_soft_deleted_transaction():
    plans = mod.plan_asset_events_from_transactions([
        {
            "id": "trx_deleted",
            "transaction_date": "2026-05-10",
            "note": "nabung 5000 ke blu",
            "category": "tabungan",
            "amount": 5000,
            "payment_method": "BLU BCA",
            "source": "telegram",
            "deleted_at": "2026-05-10 16:20:20",
        }
    ])
    assert plans == []


def test_asset_planner_keeps_active_transaction():
    plans = mod.plan_asset_events_from_transactions([
        {
            "id": "trx_active",
            "transaction_date": "2026-05-10",
            "note": "nabung 5000 ke blu",
            "category": "tabungan",
            "amount": 5000,
            "payment_method": "BLU BCA",
            "source": "telegram",
            "deleted_at": None,
        }
    ])
    assert len(plans) == 1
    assert plans[0]["row"]["amount"] == "5000"
