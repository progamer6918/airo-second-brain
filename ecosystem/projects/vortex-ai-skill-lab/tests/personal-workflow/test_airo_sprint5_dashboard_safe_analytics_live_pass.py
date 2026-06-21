from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs" / "AIRO_FINANCE_SPRINT_5_DASHBOARD_SAFE_ANALYTICS_LIVE_PASS.md"
CURRENT = ROOT / "docs" / "AIRO_FINANCE_CURRENT_STATE.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestSprint5DashboardSafeAnalyticsLivePass:
    def test_doc_exists(self):
        assert DOC.exists()

    def test_records_live_command(self):
        text = read(DOC)
        assert "admin audit sprint5 reconciliation" in text
        assert "Mode: read-only" in text
        assert "Write performed: false" in text

    def test_records_dashboard_analytics(self):
        text = read(DOC)
        assert "Dashboard Analytics" in text
        assert "Data Status: Warning" in text
        assert "Active issues: 24" in text
        assert "Legacy issues: 98" in text
        assert "Critical: 0" in text
        assert "Warnings: 25" in text

    def test_records_action_required(self):
        text = read(DOC)
        assert "24 Account Ledger rows use kategori Lainnya" in text
        assert "61 Account Ledger rows without Finance Event" in text
        assert "37 Account Ledger rows missing linked_txn_id" in text

    def test_next_step_is_cutover_aware_classification(self):
        text = read(DOC)
        assert "cutover-aware classification" in text
        assert "post-cutover missing Finance Event as Dirty" in text

    def test_current_state_records_live_pass(self):
        text = read(CURRENT)
        assert "Sprint 5 dashboard-safe analytics live pass" in text
        assert "Data Status: Warning" in text
        assert "Critical: 0" in text
        assert "cutover-aware classification" in text
