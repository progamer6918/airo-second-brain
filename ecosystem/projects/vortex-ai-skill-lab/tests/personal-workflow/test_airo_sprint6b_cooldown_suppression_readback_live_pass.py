from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs" / "AIRO_FINANCE_SPRINT_6B_COOLDOWN_SUPPRESSION_READBACK_LIVE_PASS.md"
CURRENT = ROOT / "docs" / "AIRO_FINANCE_CURRENT_STATE.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestSprint6BCooldownSuppressionReadbackLivePass:
    def test_doc_exists(self):
        assert DOC.exists()

    def test_records_command_and_safety(self):
        text = read(DOC)
        assert "admin alerts sprint6b cooldown check" in text
        assert "Mode: read-only" in text
        assert "Write performed: false" in text
        assert "Proactive send performed: false" in text
        assert "Trigger created: false" in text

    def test_records_audit_log_status(self):
        text = read(DOC)
        assert "Exists: true" in text
        assert "Rows: 6" in text
        assert "Cooldown/ACK records found: 2" in text

    def test_records_suppression_result(self):
        text = read(DOC)
        assert "Evaluated: 7" in text
        assert "Suppressed: 1" in text
        assert "Eligible: 6" in text
        assert "Target suppressed: true" in text

    def test_records_target_key(self):
        text = read(DOC)
        assert "data_status_warning:20260527:WARNING" in text
        assert "Data Status Warning" in text

    def test_records_next_guardrail(self):
        text = read(DOC)
        assert "Do not install scheduled trigger yet" in text
        assert "duplicate suppression runner mode" in text

    def test_current_state_records_live_pass(self):
        text = read(CURRENT)
        assert "Sprint 6B cooldown suppression readback live pass" in text
        assert "Target suppressed: true" in text
        assert "Install trigger only after duplicate suppression pass" in text
