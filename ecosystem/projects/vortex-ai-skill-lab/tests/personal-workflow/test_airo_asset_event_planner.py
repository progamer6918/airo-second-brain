from pathlib import Path
import sys
import importlib.util

MODULE = Path(__file__).resolve().parents[2] / "scripts" / "personal-workflow" / "airo_asset_event_planner.py"
spec = importlib.util.spec_from_file_location("airo_asset_event_planner", MODULE)
planner = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = planner
spec.loader.exec_module(planner)


def test_nabung_ke_blu():
    plans = planner.plan_asset_events_from_transactions([
        {"id": "trx_1", "transaction_date": "2026-05-10", "note": "nabung 5 juta ke blu", "source": "telegram"}
    ])
    assert len(plans) == 1
    row = plans[0]["row"]
    assert plans[0]["target_tab"] == "🥇 Aset"
    assert plans[0]["section"] == "savings_transfer_ledger"
    assert row["type"] == "savings_in"
    assert row["to_account"] == "BLU BCA"
    assert row["amount"] == "5000000"
    assert plans[0]["duplicate_key"].startswith("sav_")


def test_transfer_dari_bca_ke_blu():
    plans = planner.plan_asset_events_from_transactions([
        {"id": "trx_2", "transaction_date": "2026-05-10", "note": "transfer 1 juta dari bca ke blu"}
    ])
    row = plans[0]["row"]
    assert row["type"] == "transfer"
    assert row["from_account"] == "BCA"
    assert row["to_account"] == "BLU BCA"
    assert row["amount"] == "1000000"


def test_tarik_dari_blu_ke_cash():
    plans = planner.plan_asset_events_from_transactions([
        {"id": "trx_3", "transaction_date": "2026-05-10", "note": "tarik 500rb dari blu ke cash"}
    ])
    row = plans[0]["row"]
    assert row["type"] == "savings_out"
    assert row["from_account"] == "BLU BCA"
    assert row["to_account"] == "Cash"
    assert row["amount"] == "500000"


def test_gold_buy_gram_canonical():
    plans = planner.plan_asset_events_from_transactions([
        {"id": "trx_4", "transaction_date": "2026-05-10", "amount": 1800000, "note": "beli emas 1 gram pakai bca", "payment_method": "bca"}
    ])
    assert len(plans) == 1
    row = plans[0]["row"]
    assert plans[0]["section"] == "gold_ledger"
    assert row["action"] == "buy"
    assert row["grams_in"] == "1"
    assert row["grams_out"] == "0"
    assert row["total_amount"] == "1800000"
    assert row["source_account"] == "BCA"
    assert plans[0]["duplicate_key"].startswith("gold_")


def test_non_asset_transaction_skipped():
    assert planner.plan_asset_events_from_transactions([
        {"id": "trx_5", "transaction_date": "2026-05-10", "note": "beli kopi 15000 pakai blu", "amount": 15000}
    ]) == []
