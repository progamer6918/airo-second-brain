from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs" / "AIRO_FINANCE_SPRINT_6B_FINAL_TRIGGER_ON_STATE.md"
CURRENT = ROOT / "docs" / "AIRO_FINANCE_CURRENT_STATE.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestSprint6BFinalTriggerOnState:
    def test_doc_exists(self):
        assert DOC.exists()

    def test_records_install_and_status_commands(self):
        text = read(DOC)
        assert "admin alerts sprint6b trigger install" in text
        assert "admin alerts sprint6b trigger status" in text

    def test_records_final_on_state(self):
        text = read(DOC)
        assert "Trigger created: true" in text
        assert "Active trigger count: 1" in text
        assert "Status: installed" in text
        assert "active_trigger_count = 1" in text
        assert "status = installed" in text

    def test_records_safe_handler(self):
        text = read(DOC)
        assert "airoSprint6BTriggerHandlerSafe_" in text
        assert "proactive_send_performed = false" in text
        assert "does not send proactive Telegram alerts" in text

    def test_records_guardrail_and_next(self):
        text = read(DOC)
        assert "uninstall kill-switch has already been validated" in text
        assert "Sprint 7 Email Ingestion remains default OFF" in text
        assert "Close Sprint 6B Alert Engine" in text

    def test_current_state_records_final_on(self):
        text = read(CURRENT)
        assert "Sprint 6B final trigger ON state" in text
        assert "Final trigger count: 1" in text
        assert "Close Sprint 6B Alert Engine" in text
        assert "Sprint 7 Email Ingestion remains default OFF" in text
