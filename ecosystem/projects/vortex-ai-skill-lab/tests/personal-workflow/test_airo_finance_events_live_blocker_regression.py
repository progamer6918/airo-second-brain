from pathlib import Path
import re
import unittest


SOURCE_PATH = Path("scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs")


def source_text() -> str:
    return SOURCE_PATH.read_text(encoding="utf-8")


def function_body(source: str, name: str) -> str:
    marker = f"function {name}("
    start = source.index(marker)
    brace = source.index("{", start)
    depth = 0
    in_single = False
    in_double = False
    in_backtick = False
    escaped = False

    for i in range(brace, len(source)):
        ch = source[i]

        if escaped:
            escaped = False
            continue

        if ch == "\\":
            escaped = True
            continue

        if ch == "'" and not in_double and not in_backtick:
            in_single = not in_single
            continue

        if ch == '"' and not in_single and not in_backtick:
            in_double = not in_double
            continue

        if ch == "`" and not in_single and not in_double:
            in_backtick = not in_backtick
            continue

        if in_single or in_double or in_backtick:
            continue

        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return source[start : i + 1]

    raise AssertionError(f"Function not closed: {name}")


class FinanceEventsLiveBlockerRegressionTest(unittest.TestCase):
    def test_finance_event_failure_is_not_silent(self):
        body = function_body(source_text(), "recordFinanceEventForWriteResult_")

        self.assertNotIn("catch (err) {}", body)
        self.assertIn("financeEventStatus = 'failed'", body)
        self.assertIn("financeEventError", body)
        self.assertIn("console.error('AIRO_FINANCE_EVENT_WRITE_FAILED'", body)

    def test_finance_event_success_status_is_returned_to_caller(self):
        body = function_body(source_text(), "recordFinanceEventForWriteResult_")

        self.assertIn("const financeEventResult = writeFinanceEvent_", body)
        self.assertIn("result.financeEventStatus", body)
        self.assertIn("result.financeEventRow", body)
        self.assertIn("result.financeEventTab = AIRO_CONFIG.tabs.financeEvents", body)

    def test_admin_find_uses_canonical_finance_events_config_in_priority_tabs(self):
        find_body = function_body(source_text(), "airoFindSmokeAcrossWorkbook_")

        self.assertIn("AIRO_CONFIG.tabs.financeEvents", find_body)
        self.assertNotIn("'≡ƒº¡ Finance Events'", find_body)

    def test_cash_route_still_emits_finance_events_after_account_ledger_write(self):
        source = source_text()

        self.assertIn("AIRO_SPRINT4_CASH_ROUTE_FINANCE_EVENT_EMISSION_V1", source)
        self.assertRegex(
            source,
            re.compile(
                r"const ledgerResult = writeAccountLedgerMirror_\(ss, parsed, rawText, common, AIRO_CONFIG\.tabs\.cash\);"
                r".+?recordFinanceEventForWriteResult_\(ss, finalResult, common, parsed, rawText,",
                re.DOTALL,
            ),
        )

    def test_telegram_dedupe_guard_remains_present(self):
        do_post = function_body(source_text(), "doPost")

        self.assertIn("reserveTelegramUpdateOnce_", do_post)
        self.assertIn("duplicate_telegram_update", do_post)
        self.assertIn("dedupe_key", do_post)


if __name__ == "__main__":
    unittest.main()
