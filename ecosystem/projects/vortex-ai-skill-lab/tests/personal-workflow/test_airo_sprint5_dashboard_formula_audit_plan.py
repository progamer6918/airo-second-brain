from pathlib import Path
import unittest


DOC = Path("docs/AIRO_FINANCE_SPRINT_5_DASHBOARD_FORMULA_AUDIT_PLAN.md")
CURRENT = Path("docs/AIRO_FINANCE_CURRENT_STATE.md")
CONTRACT = Path("docs/AIRO_FINANCE_SPRINT_5_RECONCILIATION_CONTRACT.md")
SOURCE = Path("scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs")


class Sprint5DashboardFormulaAuditPlanTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = DOC.read_text(encoding="utf-8")
        cls.current = CURRENT.read_text(encoding="utf-8")
        cls.contract = CONTRACT.read_text(encoding="utf-8")
        cls.source = SOURCE.read_text(encoding="utf-8")

    def test_plan_declares_audit_only(self):
        self.assertIn("Sprint: Sprint 5 - Dashboard Analytics", self.doc)
        self.assertIn("Status: ACTIVE - AUDIT PLAN ONLY", self.doc)
        self.assertIn("This step must not edit runtime writer behavior", self.doc)
        self.assertIn("This step does not deploy", self.doc)

    def test_plan_preserves_source_of_truth_contract(self):
        required = [
            "Account Ledger is the primary source for wallet movement analytics",
            "Finance Events is the event index and lineage source",
            "Legacy Cash Ledger must not be the primary source",
            "Transactions must not replace Finance Events",
        ]
        for phrase in required:
            self.assertIn(phrase, self.doc)

    def test_plan_defines_formula_risk_classification(self):
        required = [
            "safe_account_ledger_based",
            "safe_finance_events_lineage",
            "domain_supporting_metric",
            "legacy_cash_ledger_primary_risk",
            "transactions_primary_risk",
            "unreconciled_formula_risk",
            "destructive_sheet_write_risk",
            "unknown_needs_manual_review",
        ]
        for phrase in required:
            self.assertIn(phrase, self.doc)

    def test_plan_defines_dashboard_layers(self):
        required = [
            "Layer 1 - Reconciliation Status",
            "Layer 2 - Wallet Movement",
            "Layer 3 - Spending Analytics",
            "Layer 4 - Lineage Analytics",
            "Layer 5 - Final Dashboard Visuals",
        ]
        for phrase in required:
            self.assertIn(phrase, self.doc)

    def test_current_state_mentions_formula_audit_plan(self):
        self.assertIn("Sprint 5 dashboard formula audit plan", self.current)
        self.assertIn("No runtime patch", self.current)
        self.assertIn("No Apps Script deploy", self.current)

    def test_reconciliation_contract_exists_and_is_referenced(self):
        self.assertIn("Sprint 5 Reconciliation Contract", self.contract)
        self.assertIn("Source of Truth Rules", self.contract)
        self.assertIn("Dashboard Analytics must follow the Sprint 5 reconciliation contract", self.doc)

    def test_source_has_dashboard_formula_surface_to_audit(self):
        indicators = [
            "setFormula",
            "getRange",
            "SUMIFS",
        ]
        self.assertTrue(any(indicator in self.source for indicator in indicators))


if __name__ == "__main__":
    unittest.main()
