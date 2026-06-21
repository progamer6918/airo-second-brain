from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs" / "AIRO_FINANCE_SPRINT_6B_CONTROLLED_SEND_TEST_LIVE_PASS.md"
CURRENT = ROOT / "docs" / "AIRO_FINANCE_CURRENT_STATE.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestSprint6BControlledSendTestLivePass:
    def test_doc_exists(self):
        assert DOC.exists()

    def test_records_command(self):
        text = read(DOC)
        assert "admin alerts sprint6b send test" in text
        assert "AIRO Controlled Alert Test" in text

    def test_records_send_result(self):
        text = read(DOC)
        assert "Write performed: true" in text
        assert "Proactive send performed: true" in text
        assert "Trigger created: false" in text
        assert "Sent count: 1" in text
        assert "Audit written: true" in text

    def test_records_alert_key_and_ack(self):
        text = read(DOC)
        assert "data_status_warning:20260527:WARNING" in text
        assert "admin alert ack data_status_warning:20260527:WARNING" in text

    def test_records_guardrails(self):
        text = read(DOC)
        assert "Do not install scheduled trigger yet" in text
        assert "ACK route" in text
        assert "duplicate suppression test" in text

    def test_current_state_records_live_pass(self):
        text = read(CURRENT)
        assert "Sprint 6B controlled send test live pass" in text
        assert "Sent count: 1" in text
        assert "Audit written: true" in text
        assert "Install trigger only after ACK and cooldown pass" in text
