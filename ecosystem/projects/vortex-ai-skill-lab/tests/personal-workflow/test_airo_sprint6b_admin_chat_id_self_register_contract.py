from pathlib import Path

SRC = Path("scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs")


def read_source():
    return SRC.read_text(encoding="utf-8")


class TestAiroSprint6BAdminChatIdSelfRegisterContract:
    def test_admin_chat_helpers_exist(self):
        text = read_source()
        assert "AIRO_SPRINT6B_ADMIN_CHAT_ID_SELF_REGISTER_HELPER_V1" in text
        assert "function airoSprint6BSetAdminChatId_" in text
        assert "function airoSprint6BGetAdminChatStatus_" in text
        assert "function airoSprint6BMaskChatId_" in text

    def test_admin_chat_routes_exist(self):
        text = read_source()
        assert "AIRO_SPRINT6B_ADMIN_CHAT_ID_SELF_REGISTER_ROUTE_V1" in text
        assert "AIRO_SPRINT6B_ADMIN_CHAT_ID_STATUS_ROUTE_V1" in text
        assert "admin\\s+alerts\\s+set\\s+admin\\s+chat" in text
        assert "admin\\s+alerts\\s+admin\\s+chat\\s+status" in text

    def test_set_route_writes_only_script_property(self):
        text = read_source()
        start = text.index("AIRO_SPRINT6B_ADMIN_CHAT_ID_SELF_REGISTER_ROUTE_V1")
        end = text.index("AIRO_SPRINT6B_ADMIN_CHAT_ID_STATUS_ROUTE_V1")
        block = text[start:end]
        assert "setProperty('ADMIN_CHAT_ID'" in text
        assert "script_property_write_performed: true" in block
        assert "trigger_created: false" in block
        assert "live_switch_mutated: false" in block
        assert "ScriptApp.newTrigger" not in block
        assert "GmailApp" not in block
        assert "getSheetByName" not in block
        assert "appendRow" not in block

    def test_status_route_is_read_only(self):
        text = read_source()
        start = text.index("AIRO_SPRINT6B_ADMIN_CHAT_ID_STATUS_ROUTE_V1")
        end = text.index("AIRO_SPRINT6B_LIVE_ALERT_CONTROL_ROUTE_V1")
        block = text[start:end]
        assert "script_property_write_performed: false" in block
        assert "write_performed: false" in block
        assert "trigger_created: false" in block
        assert "live_switch_mutated: false" in block
        assert "setProperty" not in block
        assert "ScriptApp.newTrigger" not in block
        assert "GmailApp" not in block
        assert "appendRow" not in block

    def test_run_once_passes_request_chat_id(self):
        text = read_source()
        assert "airoSprint6BTriggerHandlerLive_({ targetChatId: chatId })" in text

    def test_live_handler_accepts_options_but_scheduled_fallback_remains_valid(self):
        text = read_source()
        assert "function airoSprint6BTriggerHandlerLive_(options)" in text
        assert "options = options || {}" in text
        assert "targetChatId: options.targetChatId || ''" in text
        assert "const targetChatId = String((options && options.targetChatId) || getProp_('ADMIN_CHAT_ID') || '').trim();" in text

    def test_alert_runner_uses_target_chat_id_not_direct_admin_prop_in_send_loop(self):
        text = read_source()
        start = text.index("function airoSprint6BAlertRunnerSafeMode_")
        end = text.index("function airoBuildSprint6BAlertRunnerSafeModeReply_")
        block = text[start:end]
        assert "sendTelegram_(\n        targetChatId," in block
        send_loop = block[block.index("if (shouldSend)"):block.index("if (shouldWriteAudit)")]
        assert "getProp_('ADMIN_CHAT_ID')" not in send_loop
        assert "target_chat_id_source" in block
        assert "request_chat_id" in block
        assert "ADMIN_CHAT_ID" in block

    def test_no_destructive_or_email_mutations_added_near_new_routes(self):
        text = read_source()
        start = text.index("AIRO_SPRINT6B_ADMIN_CHAT_ID_SELF_REGISTER_ROUTE_V1")
        end = text.index("AIRO_SPRINT6B_LIVE_ALERT_CONTROL_ROUTE_V1")
        block = text[start:end]
        forbidden = [
            "deleteSheet",
            "showSheet",
            "hideSheet",
            "GmailApp",
            "markRead",
            "moveToTrash",
            "ScriptApp.newTrigger",
            "ScriptApp.deleteTrigger",
            "airoSprint6BSetLiveEnabled_(true)",
        ]
        for needle in forbidden:
            assert needle not in block

    def test_live_switch_default_remains_false_helper_behavior(self):
        text = read_source()
        start = text.index("function airoSprint6BIsLiveEnabled_")
        end = text.index("function airoSprint6BSetLiveEnabled_")
        block = text[start:end]
        assert "return false" in block
        assert "AIRO_ALERT_ENGINE_LIVE_ENABLED" in block
