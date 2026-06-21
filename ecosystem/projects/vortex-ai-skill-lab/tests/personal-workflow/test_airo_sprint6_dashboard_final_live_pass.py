from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs" / "AIRO_FINANCE_SPRINT_6_DASHBOARD_FINAL_LIVE_PASS.md"
CURRENT = ROOT / "docs" / "AIRO_FINANCE_CURRENT_STATE.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestSprint6DashboardFinalLivePass:
    def test_doc_exists(self):
        assert DOC.exists()

    def test_records_readback_command(self):
        text = read(DOC)
        assert "admin dashboard sprint6 readback" in text
        assert "Mode: read-only" in text
        assert "Write performed: false" in text

    def test_records_dashboard_identity(self):
        text = read(DOC)
        assert "Found: true" in text
        assert "Actual tab: 🏠 Dashboard" in text
        assert "Rows: 54" in text
        assert "Cols: 7" in text

    def test_records_required_marker_pass(self):
        text = read(DOC)
        assert "Required marker pass: 6/6" in text
        assert "Data Status: OK" in text
        assert "Cash Ledger dependency: OK" in text
        assert "FORBIDDEN: OK" in text
        assert "Action Required: OK" in text
        assert "Data Quality Center: OK" in text

    def test_records_backup_and_audit(self):
        text = read(DOC)
        assert "Backup tab count: 2" in text
        assert "_AIRO_Dashboard_Backup_20260526_222410" in text
        assert "Audit Log" in text
        assert "Build event in last rows: true" in text

    def test_missing_non_required_marker_is_not_blocker(self):
        text = read(DOC)
        assert "Sprint 6 Dashboard Final: MISSING" in text
        assert "not a blocker" in text
        assert "required marker pass = 6/6" in text

    def test_current_state_records_live_pass(self):
        text = read(CURRENT)
        assert "Sprint 6 Dashboard Final live pass" in text
        assert "Required marker pass: 6/6" in text
        assert "Existing Dashboard tab remains official final dashboard" in text
        assert "Start Sprint 6B Proactive Telegram Alert Engine v1" in text
