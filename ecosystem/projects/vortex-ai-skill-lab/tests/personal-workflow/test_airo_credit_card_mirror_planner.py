from pathlib import Path
import importlib.util
import sys

MODULE = Path(__file__).resolve().parents[2] / "scripts/personal-workflow/airo_credit_card_mirror_planner.py"
spec = importlib.util.spec_from_file_location("airo_credit_card_mirror_planner", MODULE)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def test_tokopedia_credit_card_mirror_cycle_after_16th():
    ops = [
        {
            "target_tab": "💸 Transactions",
            "source_table": "transactions",
            "source_rowid": 99,
            "entity_id": "trx_tokped_001",
            "duplicate_key": "transactions:trx_tokped_001",
            "action": "insert_or_update",
            "sync_hash": "abc",
            "row_preview": {
                "transaction_id": "trx_tokped_001",
                "date": "2026-05-16",
                "merchant": "Tokopedia",
                "amount": 100000,
                "account": "Tokopedia Credit Card",
                "raw_text": "beli barang 100rb pakai tokopedia credit card",
            },
        }
    ]

    mirrors = mod.build_credit_card_mirror_operations(ops)
    assert len(mirrors) == 1

    row = mirrors[0]["row_preview"]
    assert mirrors[0]["target_tab"] == "💳 Credit Card"
    assert mirrors[0]["duplicate_key"] == "trx_tokped_001"
    assert row["billing_cycle_id"] == "TOKPED_CC_2026-06"
    assert row["billing_start"] == "2026-05-16"
    assert row["billing_end"] == "2026-06-15"
    assert row["statement_month"] == "2026-06"
    assert row["linked_txn_id"] == "trx_tokped_001"


def test_skip_no_write_validation_marker_even_if_tokopedia_text():
    ops = [
        {
            "target_tab": "NO_WRITE",
            "action": "skip_validation_marker",
            "duplicate_key": "transactions:trx_marker",
            "row_preview": {
                "date": "2026-05-10",
                "account": "Tokopedia Credit Card",
                "raw_text": "validasi-persistent-db pakai tokopedia credit card",
            },
        }
    ]

    assert mod.build_credit_card_mirror_operations(ops) == []
