from pathlib import Path
import unittest


DOC = Path("docs/AIRO_FINANCE_SPRINT_5_RECONCILIATION_CONTRACT.md")
SOURCE = Path("scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs")


class Sprint5ReconciliationContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = DOC.read_text(encoding="utf-8")
        cls.source = SOURCE.read_text(encoding="utf-8")

    def test_contract_declares_sprint5_active_contract_only(self):
        self.assertIn("Sprint: Sprint 5 - Dashboard Analytics", self.doc)
        self.assertIn("Status: ACTIVE - CONTRACT ONLY", self.doc)
        self.assertIn("Sprint 5 must not start by drawing dashboard panels directly", self.doc)

    def test_contract_locks_source_of_truth_rules(self):
        required = [
            "Primary dashboard metrics must use Account Ledger",
            "Finance Events must be used as the event index",
            "Domain tabs may be used for domain-specific supporting metrics",
            "Dashboard analytics must not read legacy Cash Ledger as the primary source",
            "Dashboard analytics must not use Transactions as a replacement for Finance Events",
        ]
        for phrase in required:
            self.assertIn(phrase, self.doc)

    def test_contract_defines_reconciliation_checks(self):
        required = [
            "Account Ledger rows without linked_txn_id",
            "Account Ledger rows without source_tab",
            "Duplicate Account Ledger candidates by linked_txn_id",
            "Finance Events rows without source_tab",
            "Finance Events rows without linked_txn_id",
            "Account Ledger rows after Sprint 4 cutover with no matching Finance Events event",
            "Finance Events transaction_created rows with no matching Account Ledger row",
        ]
        for phrase in required:
            self.assertIn(phrase, self.doc)

    def test_contract_defines_status_values(self):
        required = [
            "reconciled",
            "missing_finance_event",
            "missing_account_ledger_ref",
            "duplicate_account_ledger_candidate",
            "finance_event_without_source",
            "needs_category",
            "manual_review_required",
        ]
        for phrase in required:
            self.assertIn(phrase, self.doc)

    def test_runtime_surface_contains_required_lineage_fields(self):
        required = [
            "function writeFinanceEvent_",
            "function recordFinanceEventForWriteResult_",
            "linked_txn_id",
            "source_tab",
            "source_row",
            "financeEventStatus",
            "financeEventError",
            "AIRO_FINANCE_EVENT_WRITE_FAILED",
        ]
        for phrase in required:
            self.assertIn(phrase, self.source)

    def test_contract_step_does_not_claim_runtime_deploy(self):
        forbidden = [
            "Sprint 5 closed",
            "deploy completed",
            "runtime writer patch completed",
            "dashboard patch completed",
        ]
        for phrase in forbidden:
            self.assertNotIn(phrase, self.doc)


if __name__ == "__main__":
    unittest.main()
