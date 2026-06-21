from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "scripts" / "personal-workflow" / "apps-script" / "airo_finance_multitab_final_v1.gs"

def read_src() -> str:
    return SRC.read_text(encoding="utf-8")

class TestAiroSprint6BGuardedLiveControlLayerContract:
    def test_live_enabled_key_exists(self):
        text = read_src()
        assert "AIRO_ALERT_ENGINE_LIVE_ENABLED" in text

    def test_helper_functions_exist(self):
        text = read_src()
        assert "function airoSprint6BIsLiveEnabled_" in text
        assert "function airoSprint6BSetLiveEnabled_" in text
        assert "function airoSprint6BGetLiveStatus_" in text

    def test_live_trigger_handler_exists_and_fail_closes(self):
        text = read_src()
        assert "function airoSprint6BTriggerHandlerLive_" in text
        
        # Check fail-safe: if not live enabled, it behaves like safe/heartbeat
        start = text.index("function airoSprint6BTriggerHandlerLive_")
        brace = text.index("{", start)
        depth = 0
        body = ""
        for i in range(brace, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    body = text[start:i + 1]
                    break
        
        assert "airoSprint6BIsLiveEnabled_" in body
        assert "airoSprint6BDuplicateSuppressionRunner_" in body
        # After the observability rename, disabled path writes sprint6b_trigger_live_disabled_heartbeat
        assert "sprint6b_trigger_live_disabled_heartbeat" in body or "sprint6b_trigger_live_heartbeat" in body
        assert "live_enabled: false" in body
        assert "airoSprint6BAlertRunnerSafeMode_" in body

    def test_telegram_admin_commands_exist(self):
        text = read_src()
        assert "admin alerts live status" in text or "admin\\s+alerts\\s+live\\s+(status|enable|disable)" in text
        assert "admin alerts live enable" in text or "sprint6b_live_enable" in text
        assert "admin alerts live disable" in text or "sprint6b_live_disable" in text

    def test_live_trigger_lifecycle_commands_exist(self):
        text = read_src()
        assert "admin alerts live trigger status" in text or "trigger\\s+(status|install|uninstall)" in text
        assert "admin alerts live trigger install" in text or "live_trigger_install" in text
        assert "admin alerts live trigger uninstall" in text or "live_trigger_uninstall" in text

    def test_uninstall_deletes_live_trigger(self):
        text = read_src()
        assert "function airoSprint6BUninstallLiveTrigger_" in text
        assert "ScriptApp.deleteTrigger" in text

    def test_backward_compatibility(self):
        text = read_src()
        assert "function airoSprint6BTriggerHandlerSafe_" in text
        assert "admin alerts sprint6b trigger install" in text or "sprint6b_guarded_trigger_install" in text

    def test_no_destructive_or_email_mutations_added(self):
        text = read_src()
        # Verify no sheets deletion added
        assert "deleteSheet" not in text
        # Verify no new unhiding sheet functions added
        assert text.count("showSheet") <= 1
