from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "scripts" / "personal-workflow" / "apps-script" / "airo_finance_multitab_final_v1.gs"
V2_SRC = ROOT / "apps-script-prod-v2" / "AIRO_Finance_Multitab_Final_v1.js"
DOC = ROOT / "docs" / "AIRO_FINANCE_SPRINT_6B_ALERT_RUNNER_SAFE_MODE.md"
CURRENT = ROOT / "docs" / "AIRO_FINANCE_CURRENT_STATE.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestSprint6BAlertRunnerSafeMode:
    def test_doc_exists(self):
        assert DOC.exists()

    def test_source_has_markers(self):
        text = read(SRC)
        assert "AIRO_SPRINT6B_ALERT_RUNNER_SAFE_MODE_ROUTE_V1" in text
        assert "AIRO_SPRINT6B_ALERT_RUNNER_SAFE_MODE_HELPER_V1" in text
        assert "airoSprint6BAlertRunnerSafeMode_" in text
        assert "airoBuildSprint6BAlertRunnerSafeModeReply_" in text

    def test_default_route_is_safe(self):
        text = read(SRC)
        assert "write_performed: false" in text
        assert "google_write_performed: false" in text
        assert "proactive_send_performed: false" in text
        assert "trigger_created: false" in text

    def test_runner_uses_planner_and_ack(self):
        text = read(SRC)
        assert "airoSprint6BAlertEnginePlan_" in text
        assert "alert_candidates" in text
        assert "ACK: admin alert ack" in text
        assert "_AIRO_Audit_Log" in text

    def test_no_trigger_install(self):
        text = read(SRC)
        assert "ScriptApp.newTrigger" not in text[text.index("AIRO_SPRINT6B_ALERT_RUNNER_SAFE_MODE_ROUTE_V1"):text.index("const specialCommand = handleSpecialFinanceCommand_")]

    def test_v2_patched(self):
        if V2_SRC.exists():
            text = read(V2_SRC)
            assert "AIRO_SPRINT6B_ALERT_RUNNER_SAFE_MODE_ROUTE_V1" in text
            assert "AIRO_SPRINT6B_ALERT_RUNNER_SAFE_MODE_HELPER_V1" in text

    def test_current_state_records_runner(self):
        text = read(CURRENT)
        assert "Sprint 6B Alert Runner safe mode" in text
        assert "No proactive send" in text
        assert "No trigger creation" in text
