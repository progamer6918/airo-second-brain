from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs" / "AIRO_FINANCE_SPRINT_7_EMAIL_INGESTION_DECISION_GATE.md"
CURRENT = ROOT / "docs" / "AIRO_FINANCE_CURRENT_STATE.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestSprint7EmailIngestionDecisionGate:
    def test_doc_exists(self):
        assert DOC.exists()

    def test_records_default_off(self):
        text = read(DOC)
        assert "NOT STARTED" in text
        assert "default OFF" in text
        assert "email_ingestion_enabled = false by default" in text

    def test_records_no_live_ingestion(self):
        text = read(DOC)
        for item in [
            "Do not enable Email Ingestion yet",
            "no trigger install at first step",
            "no email read/write side effect at first step",
            "no automatic Finance Event creation at first step",
            "dry-run only until approved",
        ]:
            assert item in text

    def test_records_required_guardrails(self):
        text = read(DOC)
        for item in [
            "source allowlist",
            "sender allowlist",
            "duplicate detection",
            "review queue fallback",
            "audit log coverage",
            "kill-switch",
        ]:
            assert item in text

    def test_records_non_goals(self):
        text = read(DOC)
        for item in [
            "read Gmail live",
            "install Gmail trigger",
            "create finance transaction from email",
            "write to Account Ledger from email",
            "write to Finance Events from email",
        ]:
            assert item in text

    def test_current_state_records_decision_gate(self):
        text = read(CURRENT)
        assert "Sprint 7 Email Ingestion decision gate" in text
        assert "Email Ingestion remains" in text
        assert "default OFF" in text
        assert "Implement Sprint 7 dry-run source contract and property guard" in text
