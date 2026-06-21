from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "scripts" / "personal-workflow" / "apps-script" / "airo_finance_multitab_final_v1.gs"
V2_SRC = ROOT / "apps-script-prod-v2" / "AIRO_Finance_Multitab_Final_v1.js"
DOC = ROOT / "docs" / "AIRO_FINANCE_SPRINT_6B_ACK_ROUTE.md"
CURRENT = ROOT / "docs" / "AIRO_FINANCE_CURRENT_STATE.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def region_after(text: str, marker: str) -> str:
    start = text.index(marker)
    end = text.find("const specialCommand = handleSpecialFinanceCommand_", start)
    if end == -1:
        return text[start:]
    return text[start:end]


class TestSprint6BAlertAckRoute:
    def test_doc_exists(self):
        assert DOC.exists()

    def test_source_has_markers(self):
        text = read(SRC)
        assert "AIRO_SPRINT6B_ALERT_ACK_ROUTE_V1" in text
        assert "AIRO_SPRINT6B_ALERT_ACK_HELPER_V1" in text
        assert "airoSprint6BAckAlert_" in text
        assert "airoBuildSprint6BAckAlertReply_" in text

    def test_route_command_exists(self):
        text = read(SRC)
        assert "sprint6b_alert_ack" in text
        assert "admin\\\\s+alerts?\\\\s+ack" in text or "admin\\s+alerts?\\s+ack" in text or "alerts?\\s+ack" in text or "admin\\s+alerts?\\s+ack" in text or "alerts?\\s+ack" in text
        assert "trigger_created: false" in text

    def test_ack_writes_audit_only(self):
        text = read(SRC)
        assert "_AIRO_Audit_Log" in text
        assert "sprint6b_alert_ack" in text
        assert "audit.appendRow" in text
        assert "proactive_send_performed: false" in text
        assert "google_write_performed: true" in text

    def test_no_trigger_creation_in_route_region(self):
        text = read(SRC)
        route = region_after(text, "AIRO_SPRINT6B_ALERT_ACK_ROUTE_V1")
        assert "ScriptApp.newTrigger" not in route

    def test_v2_patched(self):
        if V2_SRC.exists():
            text = read(V2_SRC)
            assert "AIRO_SPRINT6B_ALERT_ACK_ROUTE_V1" in text
            assert "AIRO_SPRINT6B_ALERT_ACK_HELPER_V1" in text

    def test_current_state_records_ack_route(self):
        text = read(CURRENT)
        assert "Sprint 6B alert ACK route" in text
        assert "Writes ACK record to _AIRO_Audit_Log" in text
        assert "Does not create trigger" in text
