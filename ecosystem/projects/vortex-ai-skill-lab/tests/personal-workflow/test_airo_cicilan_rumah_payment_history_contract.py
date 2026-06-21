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


class CicilanRumahPaymentHistoryContractTest(unittest.TestCase):
    def setUp(self):
        self.source = read_source()

    def test_config_contains_cicilan_rumah_tab(self):
        self.assertIn("cicilanRumah:", self.source)
        self.assertIn("Cicilan Rumah", self.source)

    def test_review_queue_router_routes_cicilan_rumah_terms_to_domain_tab(self):
        body = extract_function(self.source, "routeReviewApprovedTab_")

        for expected in [
            "cicilan rumah",
            "kpr",
            "angsuran rumah",
            "bayar rumah",
            "parsed.category === 'Cicilan Rumah'",
            "AIRO_CONFIG.tabs.cicilanRumah",
        ]:
            self.assertIn(expected, body)

    def test_review_queue_approval_uses_router_before_write(self):
        body = extract_function(self.source, "processReviewQueueApproved")

        for expected in [
            "routeReviewApprovedTab_(parsed, rawText)",
            "writeRouted_(ss, plannedTab, parsed, rawText, stagingResult)",
            "issue_reason",
            "processed_to_",
            "process_failed_",
        ]:
            self.assertIn(expected, body)

    def test_generic_tab_inference_detects_cicilan_rumah_terms(self):
        self.assertIn("cicilan rumah|kpr|angsuran rumah|bayar rumah", self.source)
        self.assertIn("return AIRO_CONFIG.tabs.cicilanRumah", self.source)
        self.assertIn("if (/\\b(cicilan rumah|kpr|angsuran rumah)\\b/i.test(t)) return 'Cicilan Rumah';", self.source)

    def test_runtime_audit_command_checks_cicilan_rumah_payment_header(self):
        for expected in [
            "cicilan_rumah_rows_runtime_audit",
            "Cicilan Rumah audit gagal: sheet Cicilan Rumah tidak ditemukan.",
            "Cicilan Rumah audit gagal: header payment history tidak ditemukan.",
            "Cicilan Rumah runtime audit selesai.",
            "payment_id",
            "cicilan_ke",
            "amount",
            "remaining",
        ]:
            self.assertIn(expected, self.source)

    def test_runtime_audit_payment_history_columns_use_aliases(self):
        for expected in [
            "payment_id: findCol_(['payment_id', 'payment id', 'id_pembayaran'])",
            "date: findCol_(['date', 'tanggal', 'payment_date', 'tanggal_bayar', 'date_paid', 'paid_date'])",
            "amount: findCol_(['amount', 'nominal', 'jumlah', 'payment_amount', 'amount_paid', 'paid_amount', 'angsuran'])",
            "cicilan_ke: findCol_(['cicilan_ke', 'cicilan ke', 'angsuran_ke', 'installment_no'])",
            "remaining: findCol_(['remaining_after_payment', 'remaining', 'sisa_cicilan', 'sisa'])",
        ]:
            self.assertIn(expected, self.source)

    def test_current_sprint_does_not_add_unverified_cicilan_runtime_writer(self):
        # Sprint 2 currently locks routing/audit behavior. A full Cicilan Rumah writer
        # must be added only after a separate test-first runtime patch.
        for missing_runtime_writer in [
            "function writeCicilanRumahSafely_(",
            "function appendCicilanRumahPayment_(",
            "function appendCicilanRumahPaymentLog_(",
            "function updateCicilanRumahMaster_(",
        ]:
            self.assertNotIn(missing_runtime_writer, self.source)


if __name__ == "__main__":
    unittest.main()
