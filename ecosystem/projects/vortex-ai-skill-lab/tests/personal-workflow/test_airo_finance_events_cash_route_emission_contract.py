from pathlib import Path

SOURCE = Path("scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs").read_text(encoding="utf-8")


def test_cash_route_emits_finance_event_before_returning_account_ledger_result():
    marker = "AIRO_SPRINT4_CASH_ROUTE_FINANCE_EVENT_EMISSION_V1"
    assert marker in SOURCE

    start = SOURCE.index("if (key.includes('cash ledger')) {")
    end = SOURCE.index("return cashResult;", start)
    cash_block = SOURCE[start:end]

    assert "const finalResult = {" in cash_block
    assert "writtenTab: AIRO_CONFIG.tabs.accountLedger" in cash_block
    assert "recordFinanceEventForWriteResult_(" in cash_block
    assert "event_type: 'transaction_created'" in cash_block
    assert "event_source: 'telegram'" in cash_block
    assert "source_tab: finalResult.writtenTab || AIRO_CONFIG.tabs.accountLedger" in cash_block
    assert "source_row: finalResult.row || ''" in cash_block
    assert "return finalResult;" in cash_block


def test_finance_event_payload_keeps_redacted_raw_text_for_smoke_readback():
    start = SOURCE.index("function recordFinanceEventForWriteResult_")
    end = SOURCE.index("function writeRouted_", start)
    body = SOURCE[start:end]

    assert "raw_text_present: Boolean(rawText)" in body
    assert "raw_text: rawText || ''" in body
    assert "financeEventPayloadJson_" in SOURCE
