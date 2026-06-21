from pathlib import Path
import importlib.util
import sys

MODULE = Path(__file__).resolve().parents[2] / "scripts/personal-workflow/airo_credit_card_billing_cycle.py"
spec = importlib.util.spec_from_file_location("airo_credit_card_billing_cycle", MODULE)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
assert spec.loader is not None
spec.loader.exec_module(mod)


def test_tokped_card_billing_cycle_boundaries():
    cases = {
        "2026-04-15": ("2026-03-16", "2026-04-15", "2026-04", "TOKPED_CC_2026-04"),
        "2026-04-16": ("2026-04-16", "2026-05-15", "2026-05", "TOKPED_CC_2026-05"),
        "2026-05-15": ("2026-04-16", "2026-05-15", "2026-05", "TOKPED_CC_2026-05"),
        "2026-05-16": ("2026-05-16", "2026-06-15", "2026-06", "TOKPED_CC_2026-06"),
        "2026-12-16": ("2026-12-16", "2027-01-15", "2027-01", "TOKPED_CC_2027-01"),
        "2027-01-15": ("2026-12-16", "2027-01-15", "2027-01", "TOKPED_CC_2027-01"),
    }

    for tx_date, expected in cases.items():
        result = mod.compute_tokped_card_billing_cycle(tx_date)
        assert (
            result.billing_start,
            result.billing_end,
            result.statement_month,
            result.billing_cycle_id,
        ) == expected
