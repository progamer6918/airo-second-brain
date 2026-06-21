from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs" / "AIRO_FINANCE_SPRINT_7_EMAIL_SOURCE_CONTRACT_GUARD_LIVE_PASS.md"
CURRENT = ROOT / "docs" / "AIRO_FINANCE_CURRENT_STATE.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestSprint7EmailSourceContractGuardLivePass:
    def test_doc_exists(self):
        assert DOC.exists()

    def test_records_command_and_dry_run(self):
        text = read(DOC)
        assert "admin email sprint7 guard" in text
        assert "Mode: dry-run" in text
        assert "Write performed: false" in text
        assert "Email ingestion enabled: false" in text
        assert "Email default OFF: true" in text
        assert "Dry-run only: true" in text

    def test_records_no_gmail_or_finance_side_effects(self):
        text = read(DOC)
        for item in [
            "Gmail read performed: false",
            "Gmail trigger created: false",
            "Finance write performed: false",
            "Account Ledger write performed: false",
            "Finance Events write performed: false",
            "Review Queue write performed: false",
        ]:
            assert item in text

    def test_records_source_contract_and_blockers(self):
        text = read(DOC)
        for item in [
            "Allowed senders configured: false",
            "Label configured: false",
            "Review Queue fallback required: true",
            "Audit Log required: true",
            "Duplicate detection required: true",
            "Kill-switch required: true",
            "blocked_for_live_ingestion",
        ]:
            assert item in text

    def test_records_guardrails(self):
        text = read(DOC)
        assert "Do not enable live Gmail ingestion" in text
        assert "Do not install Gmail trigger" in text
        assert "Do not create transactions from email" in text
        assert "dry-run parser plan only" in text

    def test_current_state_records_live_pass(self):
        text = read(CURRENT)
        assert "Sprint 7 email source contract guard live pass" in text
        assert "Status: blocked_for_live_ingestion" in text
        assert "Do not read Gmail live" in text
        assert "Implement Sprint 7 dry-run parser plan only" in text
