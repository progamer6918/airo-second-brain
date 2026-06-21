from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[2]
ACTIVE_APPS_SCRIPT = REPO_ROOT / "scripts" / "personal-workflow" / "apps-script" / "airo_finance_multitab_final_v1.gs"


def read_source() -> str:
    return ACTIVE_APPS_SCRIPT.read_text(encoding="utf-8", errors="replace")


def extract_function(source: str, function_name: str) -> str:
    marker = f"function {function_name}("
    start = source.find(marker)
    if start < 0:
        raise AssertionError(f"Missing function: {function_name}")

    brace_start = source.find("{", start)
    if brace_start < 0:
        raise AssertionError(f"Missing opening brace for function: {function_name}")

    depth = 0
    for index in range(brace_start, len(source)):
        char = source[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return source[start : index + 1]

    raise AssertionError(f"Could not extract function body: {function_name}")


class HutangMasterPaymentContractTest(unittest.TestCase):
    def setUp(self):
        self.source = read_source()

    def test_hutang_top_level_routes_payment_increase_piutang_and_unclear_to_safe_paths(self):
        body = extract_function(self.source, "writeHutangSafely_")

        for expected in [
            "appendDebtPaymentAndUpdateMaster_",
            "appendDebtIncreaseAndUpdateMaster_",
            "orang_bayar_hutang_ke_saya_needs_piutang_flow",
            "hutang_intent_unclear",
            "AIRO_CONFIG.tabs.review",
            "AIRO_CONFIG.tabs.hutang",
        ]:
            self.assertIn(expected, body)

    def test_debt_payment_updates_master_logs_payment_and_mirrors_account_ledger(self):
        body = extract_function(self.source, "appendDebtPaymentAndUpdateMaster_")

        for expected in [
            "findHutangMasterHeader_",
            "findHutangPaymentHeader_",
            "parseDebtPerson_",
            "findDebtMasterRowByName_",
            "appendDebtPaymentLog_",
            "writeAccountLedgerMirror_",
            "hutang_payment_person_or_amount_missing",
            "hutang_person_not_found_in_master",
            "type: 'debt_payment'",
            "category: parsed.category || 'Hutang'",
            "account: parsed.account || 'Unknown'",
            "AIRO_CONFIG.tabs.hutang",
        ]:
            self.assertIn(expected, body)

        for expected in [
            "oldPaid + amount",
            "Math.max(0, pokok - newPaid)",
            "map.total_dibayar",
            "map.sisa_hutang",
            "setValue(newPaid)",
            "setValue(sisa)",
            "pay_id: common.linked_txn_id || makeTxnId_({}, rawText)",
            "linked_txn_id: common.linked_txn_id || makeTxnId_({}, rawText)",
        ]:
            self.assertIn(expected, body)

    def test_debt_increase_updates_master_and_log_but_does_not_write_wallet_outflow(self):
        body = extract_function(self.source, "appendDebtIncreaseAndUpdateMaster_")

        for expected in [
            "findHutangMasterHeader_",
            "findHutangPaymentHeader_",
            "parseDebtPerson_",
            "findDebtMasterRowByName_",
            "appendDebtPaymentLog_",
            "hutang_increase_person_or_amount_missing",
            "hutang_person_not_found_in_master",
            "debt_increase:",
            "oldPokok + amount",
            "Math.max(0, newPokok - paid)",
            "map.jumlah_pokok",
            "map.sisa_hutang",
            "setValue(newPokok)",
            "setValue(sisa)",
        ]:
            self.assertIn(expected, body)

        self.assertNotIn("writeAccountLedgerMirror_", body)

    def test_hutang_payment_log_uses_header_based_append_without_rewriting_schema(self):
        body = extract_function(self.source, "appendDebtPaymentLog_")

        for expected in [
            "hutangColMap_(paymentHeader.headers)",
            "findNextSectionRow_",
            "paymentHeader.headers.map",
            "canonicalKey_",
            "data[k] !== undefined ? data[k] : ''",
            "sheet.getRange",
            "setValues",
        ]:
            self.assertIn(expected, body)

    def test_hutang_person_parser_supports_payment_and_borrowing_phrases(self):
        body = extract_function(self.source, "parseDebtPerson_")

        for expected in [
            "bayar",
            "hutang",
            "utang",
            "pinjam",
            "dari",
        ]:
            self.assertIn(expected, body)

    def test_debt_ambiguity_keeps_incomplete_debt_rewrite_safe(self):
        body = extract_function(self.source, "debtAmbiguousClarificationResolvedText_")

        for expected in [
            "DEBT_NEEDS_COMPLETE_REWRITE",
            "DEBT_PIUTANG_HELP_ONLY",
            "isBorrowInText_",
            "isDebtPaymentText_",
            "parseDebtPerson_",
        ]:
            self.assertIn(expected, body)


if __name__ == "__main__":
    unittest.main()
