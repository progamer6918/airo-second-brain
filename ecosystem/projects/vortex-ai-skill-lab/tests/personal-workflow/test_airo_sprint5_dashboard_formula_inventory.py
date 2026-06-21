from pathlib import Path
import unittest


DOC = Path("docs/AIRO_FINANCE_SPRINT_5_DASHBOARD_FORMULA_INVENTORY.md")
CURRENT = Path("docs/AIRO_FINANCE_CURRENT_STATE.md")
PLAN = Path("docs/AIRO_FINANCE_SPRINT_5_DASHBOARD_FORMULA_AUDIT_PLAN.md")


class Sprint5DashboardFormulaInventoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = DOC.read_text(encoding="utf-8")
        cls.current = CURRENT.read_text(encoding="utf-8")
        cls.plan = PLAN.read_text(encoding="utf-8")

    def test_inventory_is_read_only(self):
        self.assertIn("Status: ACTIVE - READ ONLY INVENTORY", self.doc)
        self.assertIn("No runtime patch", self.doc)
        self.assertIn("Apps Script deploy", self.doc)
        self.assertIn("live Google Sheet formula edit", self.doc)

    def test_inventory_uses_risk_model_from_plan(self):
        required = [
            "safe_account_ledger_based",
            "safe_finance_events_lineage",
            "legacy_cash_ledger_primary_risk",
            "transactions_primary_risk",
            "destructive_sheet_write_risk",
            "unknown_needs_manual_review",
        ]
        for phrase in required:
            self.assertIn(phrase, self.doc)
            self.assertIn(phrase, self.plan)

    def test_inventory_captures_expected_dashboard_functions(self):
        required = [
            "setupDashboardNetWorthPanel",
            "setupDashboardCreditCardCyclePanel",
            "dashboardLayoutReadOnlyAudit_",
        ]
        for phrase in required:
            self.assertIn(phrase, self.doc)

    def test_inventory_captures_account_ledger_formula_direction(self):
        self.assertIn("Monthly Review cash formulas already reference Account Ledger", self.doc)
        self.assertIn("Dashboard Cash Aktif and Net Worth formulas reference Account Ledger", self.doc)

    def test_inventory_identifies_reconciliation_gap(self):
        self.assertIn("Finance Events is not yet used for dashboard lineage analytics formulas", self.doc)
        self.assertIn("Reconciliation status layer is not yet implemented", self.doc)

    def test_current_state_mentions_inventory(self):
        self.assertIn("Sprint 5 dashboard formula inventory", self.current)
        self.assertIn("No runtime patch", self.current)
        self.assertIn("read-only admin helper", self.current)


if __name__ == "__main__":
    unittest.main()
