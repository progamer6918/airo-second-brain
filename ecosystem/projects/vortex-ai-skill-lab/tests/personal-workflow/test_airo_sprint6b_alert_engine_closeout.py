from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs" / "AIRO_FINANCE_SPRINT_6B_ALERT_ENGINE_CLOSEOUT.md"
CURRENT = ROOT / "docs" / "AIRO_FINANCE_CURRENT_STATE.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestSprint6BAlertEngineCloseout:
    def test_doc_exists(self):
        assert DOC.exists()

    def test_records_closed_status(self):
        text = read(DOC)
        assert "Status: Sprint 6B closed" in text
        assert "Sprint 6B Alert Engine is closed" in text

    def test_records_final_trigger_on_state(self):
        text = read(DOC)
        assert "Trigger: ON" in text
        assert "airoSprint6BTriggerHandlerSafe_" in text
        assert "Active trigger count: 1" in text
        assert "Status: installed" in text
        assert "Proactive send: false" in text

    def test_records_completed_scope(self):
        text = read(DOC)
        for item in [
            "Alert planner dry-run",
            "Alert runner safe mode",
            "Controlled one-alert send test",
            "ACK route",
            "Cooldown suppression readback",
            "Duplicate suppression runner",
            "Guarded trigger lifecycle",
            "Trigger uninstall kill-switch",
            "Final trigger ON state",
        ]:
            assert item in text

    def test_records_duplicate_suppression(self):
        text = read(DOC)
        assert "data_status_warning:20260527:WARNING" in text
        assert "Decision: BLOCK_DUPLICATE" in text
        assert "Target suppressed: true" in text

    def test_records_sprint7_guardrail(self):
        text = read(DOC)
        assert "Sprint 7 Email Ingestion remains NOT STARTED and default OFF" in text

    def test_current_state_records_closeout(self):
        text = read(CURRENT)
        assert "Sprint 6B Alert Engine closeout" in text
        assert "Sprint 6B is closed" in text
        assert "Trigger: ON" in text
        assert "Sprint 7 Email Ingestion remains NOT STARTED and default OFF" in text
