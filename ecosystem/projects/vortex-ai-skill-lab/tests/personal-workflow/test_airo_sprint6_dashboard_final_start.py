from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs" / "AIRO_FINANCE_SPRINT_6_DASHBOARD_FINAL_START.md"
CURRENT = ROOT / "docs" / "AIRO_FINANCE_CURRENT_STATE.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestSprint6DashboardFinalStart:
    def test_doc_exists(self):
        assert DOC.exists()

    def test_declares_official_sprint6_start(self):
        text = read(DOC)
        assert "Sprint 6 official start" in text
        assert "This is not a new architecture" in text
        assert "follows AIRO Finance Final Kitab" in text

    def test_includes_required_dashboard_sections(self):
        text = read(DOC)
        required = [
            "Topbar",
            "Action Required",
            "Executive Command Center",
            "Wallet & Cashflow",
            "Domain Health",
            "Spending Intelligence",
            "Data Quality Center",
            "Smart Insight Panel",
            "Period selector",
            "Last synced",
            "Data Status",
            "Metric source-of-truth",
            "home_value_mode",
        ]
        for item in required:
            assert item in text

    def test_preserves_dashboard_target_rule(self):
        text = read(DOC)
        assert "existing Dashboard tab" in text
        assert "permanent second dashboard" in text
        assert "staging tab only if needed" in text

    def test_locks_source_of_truth_contract(self):
        text = read(DOC)
        assert "Cash tersedia" in text and "Account Ledger" in text
        assert "CC outstanding" in text and "Credit Card" in text
        assert "Total hutang" in text and "Hutang" in text
        assert "Aset emas" in text and "Aset" in text
        assert "Cicilan progress" in text and "Cicilan Rumah" in text
        assert "Spending category" in text and "Finance Events" in text

    def test_forbids_cash_ledger_and_email_placeholder(self):
        text = read(DOC)
        assert "Dashboard does not read Cash Ledger" in text
        assert "Email Ingestion Status hidden" in text
        assert "email_ingestion_enabled = false" in text

    def test_current_state_records_sprint6_start(self):
        text = read(CURRENT)
        assert "Sprint 6 Dashboard Final official start" in text
        assert "Start Sprint 6 Dashboard Final" in text
        assert "Dashboard must not read Cash Ledger" in text
