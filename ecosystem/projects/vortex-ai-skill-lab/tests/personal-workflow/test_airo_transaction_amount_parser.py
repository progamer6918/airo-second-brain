from pathlib import Path
import importlib.util
import sys

MODULE = Path(__file__).resolve().parents[2] / "scripts" / "personal-workflow" / "airo_transaction_persistence.py"
spec = importlib.util.spec_from_file_location("airo_transaction_persistence", MODULE)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def test_bare_number_is_exact():
    assert mod.parse_amount("5000") == 5000
    assert mod.parse_amount("15000") == 15000


def test_explicit_suffixes():
    assert mod.parse_amount("5 rb") == 5000
    assert mod.parse_amount("5 ribu") == 5000
    assert mod.parse_amount("5k") == 5000
    assert mod.parse_amount("5 juta") == 5000000
    assert mod.parse_amount("1,5 juta") == 1500000


def test_correct_upstream_scaled_bare_number():
    assert mod.correct_amount_against_raw_text(5000000, "nabung 5000 ke blu") == 5000
    assert mod.correct_amount_against_raw_text(15000000, "beli kopi 15000 pakai blu") == 15000


def test_do_not_correct_explicit_suffix():
    assert mod.correct_amount_against_raw_text(5000000, "nabung 5 juta ke blu") == 5000000
    assert mod.correct_amount_against_raw_text(5000, "nabung 5 ribu ke blu") == 5000
