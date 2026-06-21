from pathlib import Path
import importlib.util
import sys

PERSIST = Path(__file__).resolve().parents[2] / "scripts" / "personal-workflow" / "airo_transaction_persistence.py"
spec = importlib.util.spec_from_file_location("airo_transaction_persistence", PERSIST)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def test_amount_contract():
    cases = {
        "5": 5000,
        "50": 50000,
        "500": 500000,
        "5000": 5000,
        "15000": 15000,
        "5rb": 5000,
        "5 rb": 5000,
        "5ribu": 5000,
        "5 ribu": 5000,
        "5k": 5000,
        "5jt": 5000000,
        "5 juta": 5000000,
        "1,5 juta": 1500000,
        "1.5 juta": 1500000,
        "1.250.000": 1250000,
    }
    for raw, expected in cases.items():
        assert mod.parse_amount(raw) == expected, raw


def test_missing_nameerror_helpers_exist():
    assert mod.extract_payload_value({"amount": "5000"}, "amount") == "5000"
    assert mod.resolve_account("nabung 5000 ke blu") == "BLU BCA"


def test_raw_text_correction():
    assert mod.correct_amount_against_raw_text(5000000, "nabung 5000 ke blu") == 5000
    assert mod.correct_amount_against_raw_text(5, "nabung 5 ke blu") == 5000
    assert mod.correct_amount_against_raw_text(5000, "nabung 5rb ke blu") == 5000


def test_language_classification():
    assert mod.classify_finance_language("nabung 5000 ke blu")["category"] == "tabungan"
    assert mod.classify_finance_language("transfer 10000 dari bca ke blu")["cashflow_treatment"] == "internal_transfer"
    assert mod.classify_finance_language("tarik 5000 dari blu ke cash")["cashflow_treatment"] == "internal_transfer"
