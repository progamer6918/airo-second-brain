from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs" / "AIRO_FINANCE_SPRINT_6B_ALERT_RUNNER_SAFE_MODE_LIVE_PASS.md"
CURRENT = ROOT / "docs" / "AIRO_FINANCE_CURRENT_STATE.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestSprint6BAlertRunnerSafeModeLivePass:
    def test_doc_exists(self):
        assert DOC.exists()

    def test_records_command_and_safety(self):
        text = read(DOC)
        assert "admin alerts sprint6b run safe" in text
        assert "Mode: safe" in text
        assert "Write performed: false" in text
        assert "Proactive send performed: false" in text
        assert "Trigger created: false" in text

    def test_records_evaluation_counts(self):
        text = read(DOC)
        assert "Evaluated: 7" in text
        assert "Eligible: 7" in text
        assert "Suppressed by cooldown: 0" in text
        assert "Sent: 0" in text

    def test_records_ack_and_cooldown(self):
        text = read(DOC)
        assert "admin alert ack data_status_warning:20260526:WARNING" in text
        assert "Storage: _AIRO_Audit_Log" in text
        assert "ACK supported: true" in text

    def test_records_next_guardrails(self):
        text = read(DOC)
        assert "Do not install trigger yet" in text
        assert "controlled send test" in text
        assert "ACK route" in text
        assert "cooldown write mode" in text

    def test_current_state_records_live_pass(self):
        text = read(CURRENT)
        assert "Sprint 6B Alert Runner safe mode live pass" in text
        assert "Evaluated: 7" in text
        assert "Do not install trigger yet" in text
        assert "Implement controlled send test" in text
