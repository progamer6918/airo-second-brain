from airo_personal_workflow.intents.parser import (
    parse_amount,
    detect_account,
    detect_category,
    parse_user_message,
)


def test_gateway_amount_contract():
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
        assert parse_amount(raw) == expected, raw


def test_gateway_savings_command():
    parsed = parse_user_message("nabung 5000 ke blu")
    assert parsed["intent"] == "record_transaction"
    assert parsed["amount"] == 5000
    assert parsed["category"] == "tabungan"
    assert parsed["account_name"] == "BLU BCA"
    assert parsed["payment_method"] == "BLU BCA"


def test_gateway_short_thousand_command():
    parsed = parse_user_message("nabung 5 ke blu")
    assert parsed["amount"] == 5000
    assert parsed["category"] == "tabungan"


def test_gateway_suffix_command():
    parsed = parse_user_message("nabung 5rb ke blu")
    assert parsed["amount"] == 5000
    assert parsed["category"] == "tabungan"


def test_gateway_transfer_and_expense_categories():
    assert detect_category("transfer 10000 dari bca ke blu") == "transfer"
    assert detect_category("tarik 5000 dari blu ke cash") == "transfer"
    assert detect_category("beli kopi 15000 pakai blu") == "makan"
    assert detect_account("beli kopi 15000 pakai blu") == "BLU BCA"
