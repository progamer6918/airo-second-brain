from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[2]
ACTIVE_APPS_SCRIPT = REPO_ROOT / "scripts" / "personal-workflow" / "apps-script" / "airo_finance_multitab_final_v1.gs"
AUDIT_DOC = REPO_ROOT / "docs" / "AIRO_FINANCE_SPRINT_4_FINANCE_EVENTS_AUDIT_SCHEMA_PLAN.md"


def read_source() -> str:
    return ACTIVE_APPS_SCRIPT.read_text(encoding="utf-8", errors="replace")


def read_audit_doc() -> str:
    return AUDIT_DOC.read_text(encoding="utf-8", errors="replace")


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


class FinanceEventsSchemaContractTest(unittest.TestCase):
    def setUp(self):
        self.source = read_source()
        self.doc = read_audit_doc()

    def test_audit_schema_plan_exists_and_is_doc_only(self):
        for expected in [
            "Status: EXACT AUDIT / SCHEMA PLAN",
            "Sprint: Sprint 4 - Finance Events",
            "No runtime patch is made in this micro-step.",
            "Runtime scope: Read-only audit / documentation only",
            "Add the smallest test-only Finance Events schema contract first.",
        ]:
            self.assertIn(expected, self.doc)

    def test_proposed_schema_fields_are_locked_in_doc(self):
        required_fields = [
            "event_id",
            "event_ts",
            "event_type",
            "event_source",
            "source_tab",
            "source_row",
            "linked_txn_id",
            "account",
            "category",
            "amount",
            "direction",
            "status",
            "reason",
            "payload_json",
            "notes",
        ]

        for field in required_fields:
            self.assertIn(f"`{field}`", self.doc)

    def test_allowed_event_types_and_sources_are_locked_in_doc(self):
        for expected in [
            "`transaction_created`",
            "`account_mirror_written`",
            "`domain_row_written`",
            "`review_approved`",
            "`compatibility_skipped`",
            "`write_failed`",
            "`telegram`",
            "`review_queue`",
            "`admin`",
            "`system`",
        ]:
            self.assertIn(expected, self.doc)

    def test_privacy_policy_blocks_sensitive_payloads(self):
        for expected in [
            "full raw email body",
            "OTP/security content",
            "bank OTP",
            "passwords",
            "access tokens",
            "full sensitive message dumps",
            "No full email body, no OTP/security content.",
        ]:
            self.assertIn(expected, self.doc)

    def test_finance_events_schema_tab_and_manual_writer_exist_but_emission_is_not_wired_yet(self):
        for expected in [
            "financeEvents:",
            "AIRO_CONFIG.tabs.financeEvents",
            "function getFinanceEventsHeaders_(",
            "function ensureFinanceEventsSheet_(",
            "function buildFinanceEvent_(",
            "function writeFinanceEvent_(",
            "function appendFinanceEvent_(",
        ]:
            self.assertIn(expected, self.source)

        forbidden_runtime_markers = [
            "function emitFinanceEvent_(",
            "function logFinanceEvent_(",
        ]

        for marker in forbidden_runtime_markers:
            self.assertNotIn(marker, self.source)

    def test_candidate_emission_surfaces_exist_but_do_not_emit_events_yet(self):
        write_routed = extract_function(self.source, "writeRouted_")
        account_mirror = extract_function(self.source, "writeAccountLedgerMirror_")
        review_approved = extract_function(self.source, "processReviewQueueApproved")

        for expected in [
            "appendByHeader_",
            "writeAccountLedgerMirror_",
            "writeCashLedgerCompatibility_",
        ]:
            self.assertIn(expected, write_routed)

        for expected in [
            "source_tab: sourceTab",
            "linked_txn_id: common.linked_txn_id || entryId",
            "AIRO_CONFIG.tabs.accountLedger",
            "appendByHeader_",
        ]:
            self.assertIn(expected, account_mirror)

        for expected in [
            "routeReviewApprovedTab_(parsed, rawText)",
            "writeRouted_(ss, plannedTab, parsed, rawText, stagingResult)",
            "review_status",
            "issue_reason",
        ]:
            self.assertIn(expected, review_approved)

        self.assertIn("recordFinanceEventForWriteResult_(", write_routed)
        self.assertNotIn("writeFinanceEvent_", write_routed)
        self.assertNotIn("appendFinanceEvent_", write_routed)
        self.assertNotIn("emitFinanceEvent_", write_routed)

        for body in [account_mirror, review_approved]:
            self.assertNotIn("recordFinanceEventForWriteResult_", body)
            self.assertNotIn("writeFinanceEvent_", body)
            self.assertNotIn("appendFinanceEvent_", body)
            self.assertNotIn("emitFinanceEvent_", body)

    def test_account_ledger_and_cash_ledger_sprint3_guards_remain_source_of_truth(self):
        account_mirror = extract_function(self.source, "writeAccountLedgerMirror_")
        cash_flag = extract_function(self.source, "isCashLedgerCompatibilityWriteEnabled_")
        cash_compat = extract_function(self.source, "writeCashLedgerCompatibility_")

        for expected in [
            "amount_in",
            "amount_out",
            "source_tab",
            "linked_txn_id",
            "AIRO_CONFIG.tabs.accountLedger",
        ]:
            self.assertIn(expected, account_mirror)

        for expected in [
            "AIRO_CASH_LEDGER_COMPAT_WRITES_ENABLED",
            "return false",
        ]:
            self.assertIn(expected, cash_flag)

        for expected in [
            "cash_ledger_compat_writes_disabled",
            "return writeCashLedger_(ss, parsed, rawText, common);",
        ]:
            self.assertIn(expected, cash_compat)

    def test_no_email_ingestion_runtime_is_introduced_by_sprint4_schema_contract(self):
        forbidden_email_runtime = [
            "GmailApp",
            "Gmail.Users",
            "MailApp",
            "function ingestEmail",
            "function processEmail",
            "function handleGmail",
            "createDraft",
            "getInboxThreads",
        ]

        for marker in forbidden_email_runtime:
            self.assertNotIn(marker, self.source)

        self.assertIn("Email Ingestion remains out of runtime scope for Sprint 4.", self.doc)

    def test_doc_declares_finance_events_as_append_only_not_ledger_replacement(self):
        for expected in [
            "Finance Events is not a replacement for:",
            "Account Ledger",
            "domain tabs",
            "Review Queue",
            "Finance Events is an append-only observability and lineage surface.",
        ]:
            self.assertIn(expected, self.doc)


if __name__ == "__main__":
    unittest.main()
