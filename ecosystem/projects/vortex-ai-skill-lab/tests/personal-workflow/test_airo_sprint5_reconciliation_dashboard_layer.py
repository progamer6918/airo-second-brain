from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs" / "AIRO_FINANCE_SPRINT_5_RECONCILIATION_DASHBOARD_LAYER.md"
CURRENT = ROOT / "docs" / "AIRO_FINANCE_CURRENT_STATE.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestSprint5ReconciliationDashboardLayer:
    def test_doc_exists(self):
        assert DOC.exists()

    def test_declares_not_dashboard_repaint(self):
        text = read(DOC)
        assert "does not repaint the final dashboard yet" in text
        assert "do not repaint final dashboard" in text

    def test_defines_data_status_mapping(self):
        text = read(DOC)
        assert "Trusted" in text
        assert "Warning" in text
        assert "Dirty" in text
        assert "data_status" in text

    def test_defines_cutover_aware_rule(self):
        text = read(DOC)
        assert "cutover-forward" in text
        assert "Historical Account Ledger rows before Finance Events cutover" in text
        assert "New rows after Finance Events cutover" in text

    def test_defines_legacy_vs_active_classification(self):
        text = read(DOC)
        assert "Legacy Warning" in text
        assert "Active Warning" in text
        assert "Active Dirty" in text

    def test_defines_action_required_mapping(self):
        text = read(DOC)
        assert "Action Required" in text
        assert "24 rows kategori Lainnya" in text
        assert "37 legacy rows missing linked_txn_id" in text
        assert "61 Account Ledger rows without Finance Event" in text

    def test_current_state_records_next_step(self):
        text = read(CURRENT)
        assert "Sprint 5 reconciliation dashboard layer" in text
        assert "Build a reconciliation dashboard layer first" in text
        assert "Separate legacy/pre-cutover issues from active/post-cutover issues" in text
