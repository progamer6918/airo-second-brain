from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "scripts" / "personal-workflow" / "apps-script" / "airo_finance_multitab_final_v1.gs"
V2_SRC = ROOT / "apps-script-prod-v2" / "AIRO_Finance_Multitab_Final_v1.js"
DOC = ROOT / "docs" / "AIRO_FINANCE_SPRINT_6B_CONTROLLED_SEND_TEST.md"
CURRENT = ROOT / "docs" / "AIRO_FINANCE_CURRENT_STATE.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def region_after(text: str, marker: str) -> str:
    start = text.index(marker)
    end = text.find("const specialCommand = handleSpecialFinanceCommand_", start)
    if end == -1:
        return text[start:]
    return text[start:end]


class TestSprint6BControlledSendTest:
    def test_doc_exists(self):
        assert DOC.exists()

    def test_source_has_markers(self):
        text = read(SRC)
        assert "AIRO_SPRINT6B_CONTROLLED_SEND_TEST_ROUTE_V1" in text
        assert "AIRO_SPRINT6B_CONTROLLED_SEND_TEST_HELPER_V1" in text
        assert "airoSprint6BControlledSendTest_" in text
        assert "airoBuildSprint6BControlledSendTestReply_" in text

    def test_route_command_exists(self):
        text = read(SRC)
        assert "sprint6b_controlled_send_test" in text
        assert "send\\s+test" in text
        assert "trigger_created: false" in text

    def test_sends_exactly_one_alert_and_writes_audit(self):
        text = read(SRC)
        assert "sent_count: 1" in text
        assert "sendTelegram_(chatId, alertMessage)" in text
        assert "_AIRO_Audit_Log" in text
        assert "sprint6b_controlled_send_test" in text
        assert "audit.appendRow" in text

    def test_no_trigger_creation_in_route_region(self):
        text = read(SRC)
        route = region_after(text, "AIRO_SPRINT6B_CONTROLLED_SEND_TEST_ROUTE_V1")
        assert "ScriptApp.newTrigger" not in route

    def test_v2_patched(self):
        if V2_SRC.exists():
            text = read(V2_SRC)
            assert "AIRO_SPRINT6B_CONTROLLED_SEND_TEST_ROUTE_V1" in text
            assert "AIRO_SPRINT6B_CONTROLLED_SEND_TEST_HELPER_V1" in text

    def test_current_state_records_controlled_send(self):
        text = read(CURRENT)
        assert "Sprint 6B controlled send test" in text
        assert "Sends exactly one alert" in text
        assert "Does not create trigger" in text
