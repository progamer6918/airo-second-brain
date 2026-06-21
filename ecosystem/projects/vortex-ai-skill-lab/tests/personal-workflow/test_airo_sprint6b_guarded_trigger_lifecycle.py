from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "scripts" / "personal-workflow" / "apps-script" / "airo_finance_multitab_final_v1.gs"
V2_SRC = ROOT / "apps-script-prod-v2" / "AIRO_Finance_Multitab_Final_v1.js"
DOC = ROOT / "docs" / "AIRO_FINANCE_SPRINT_6B_GUARDED_TRIGGER_LIFECYCLE.md"
CURRENT = ROOT / "docs" / "AIRO_FINANCE_CURRENT_STATE.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def region_after(text: str, marker: str) -> str:
    start = text.index(marker)
    end = text.find("const specialCommand = handleSpecialFinanceCommand_", start)
    if end == -1:
        return text[start:]
    return text[start:end]


class TestSprint6BGuardedTriggerLifecycle:
    def test_doc_exists(self):
        assert DOC.exists()

    def test_source_has_markers(self):
        text = read(SRC)
        assert "AIRO_SPRINT6B_GUARDED_TRIGGER_LIFECYCLE_ROUTE_V1" in text
        assert "AIRO_SPRINT6B_GUARDED_TRIGGER_LIFECYCLE_HELPER_V1" in text
        assert "airoSprint6BTriggerHandlerSafe_" in text
        assert "airoSprint6BInstallGuardedTrigger_" in text
        assert "airoSprint6BUninstallGuardedTrigger_" in text

    def test_route_has_lifecycle_commands(self):
        text = read(SRC)
        for word in ["plan", "status", "install", "uninstall"]:
            assert word in text
        assert "sprint6b_guarded_trigger_" in text

    def test_install_is_guarded_max_one(self):
        text = read(SRC)
        assert "ScriptApp.newTrigger" in text
        assert "existing.length === 0" in text
        assert "active_trigger_count" in text
        assert "max one trigger" in text

    def test_safe_handler_does_not_send(self):
        text = read(SRC)
        start = text.index("function airoSprint6BTriggerHandlerSafe_")
        end = text.index("function airoSprint6BTriggerHandlerName_", start)
        body = text[start:end]
        assert "sendTelegram_(" not in body
        assert "proactive_send_performed: false" in body
        assert "sprint6b_trigger_safe_heartbeat" in body

    def test_uninstall_kill_switch_exists(self):
        text = read(SRC)
        assert "ScriptApp.deleteTrigger" in text
        assert "sprint6b_guarded_trigger_uninstall" in text
        assert "deleted_count" in text

    def test_plan_status_readonly(self):
        text = read(SRC)
        assert "sprint6b_guarded_trigger_plan" in text
        assert "sprint6b_guarded_trigger_status" in text
        assert "write_performed: false" in text
        assert "google_write_performed: false" in text

    def test_no_trigger_creation_in_plan_status_route_region_only(self):
        text = read(SRC)
        route = region_after(text, "AIRO_SPRINT6B_GUARDED_TRIGGER_LIFECYCLE_ROUTE_V1")
        assert "ScriptApp.newTrigger" not in route

    def test_v2_patched(self):
        if V2_SRC.exists():
            text = read(V2_SRC)
            assert "AIRO_SPRINT6B_GUARDED_TRIGGER_LIFECYCLE_ROUTE_V1" in text
            assert "AIRO_SPRINT6B_GUARDED_TRIGGER_LIFECYCLE_HELPER_V1" in text

    def test_current_state_records_trigger_lifecycle(self):
        text = read(CURRENT)
        assert "Sprint 6B guarded trigger lifecycle" in text
        assert "Uninstall removes trigger as kill-switch" in text
        assert "Run trigger plan in Telegram" in text
