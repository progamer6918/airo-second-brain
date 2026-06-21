from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs" / "AIRO_FINANCE_SPRINT_6B_GUARDED_TRIGGER_LIFECYCLE_LIVE_PASS.md"
CURRENT = ROOT / "docs" / "AIRO_FINANCE_CURRENT_STATE.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestSprint6BGuardedTriggerLifecycleLivePass:
    def test_doc_exists(self):
        assert DOC.exists()

    def test_records_plan_status_install_uninstall(self):
        text = read(DOC)
        assert "admin alerts sprint6b trigger plan" in text
        assert "admin alerts sprint6b trigger status" in text
        assert "admin alerts sprint6b trigger install" in text
        assert "admin alerts sprint6b trigger uninstall" in text

    def test_records_install_success(self):
        text = read(DOC)
        assert "Trigger created: true" in text
        assert "Active trigger count: 1" in text
        assert "Status: installed" in text

    def test_records_uninstall_success(self):
        text = read(DOC)
        assert "Deleted count: 1" in text
        assert "Status: uninstalled" in text
        assert "Status: not_installed" in text

    def test_records_safe_handler_guardrail(self):
        text = read(DOC)
        assert "airoSprint6BTriggerHandlerSafe_" in text
        assert "safe handler performs no proactive send" in text

    def test_records_current_trigger_state_off(self):
        text = read(DOC)
        assert "active_trigger_count = 0" in text
        assert "status = not_installed" in text

    def test_current_state_records_live_pass(self):
        text = read(CURRENT)
        assert "Sprint 6B guarded trigger lifecycle live pass" in text
        assert "Kill-switch works" in text
        assert "Current final trigger state after validation is OFF" in text
