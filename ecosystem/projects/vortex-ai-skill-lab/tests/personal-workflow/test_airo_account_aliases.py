from pathlib import Path
import importlib.util

MODULE = Path(__file__).resolve().parents[2] / "scripts/personal-workflow/airo_account_aliases.py"
spec = importlib.util.spec_from_file_location("airo_account_aliases", MODULE)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def test_blubca_aliases():
    cases = [
        ("catat beli makan siang 12000 pakai blubca", "BLU BCA"),
        ("catat beli makan siang 12000 pakai blu", "BLU BCA"),
        ("catat beli makan siang 12000 pakai blu bca", "BLU BCA"),
        ("catat beli makan siang 12000 pakai blu-bca", "BLU BCA"),
        ("catat beli makan siang 12000 pakai bank blu", "BLU BCA"),
    ]

    for text, expected in cases:
        assert mod.extract_account_from_text(text) == expected


def test_other_account_aliases():
    assert mod.extract_account_from_text("beli bensin 20000 pakai bca") == "BCA"
    assert mod.extract_account_from_text("jajan 10000 pakai gopay") == "GoPay"
    assert mod.extract_account_from_text("bayar pakai shopeepay") == "ShopeePay"
    assert mod.extract_account_from_text("makan 12000 pakai cash") == "Cash"
    assert mod.extract_account_from_text("beli makan 50000 pakai tokopedia credit card") == "Tokopedia CC"
