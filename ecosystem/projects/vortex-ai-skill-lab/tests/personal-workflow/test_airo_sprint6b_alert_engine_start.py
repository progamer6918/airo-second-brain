from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "scripts" / "personal-workflow" / "apps-script" / "airo_finance_multitab_final_v1.gs"
V2_SRC = ROOT / "apps-script-prod-v2" / "AIRO_Finance_Multitab_Final_v1.js"
DOC = ROOT / "docs" / "AIRO_FINANCE_SPRINT_6B_ALERT_ENGINE_START.md"
CURRENT = ROOT / "docs" / "AIRO_FINANCE_CURRENT_STATE.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def function_body(text: str, name: str) -> str:
    start = text.index(f"function {name}")
    brace = text.index("{", start)
    depth = 0
    for i in range(brace, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    raise AssertionError(f"function body not found: {name}")


class TestSprint6BAlertEngineStart:
    def test_doc_exists(self):
        assert DOC.exists()

    def test_source_has_route_and_helper(self):
        text = read(SRC)
        assert "AIRO_SPRINT6B_ALERT_ENGINE_PLAN_ROUTE_V1" in text
        assert "AIRO_SPRINT6B_ALERT_ENGINE_PLAN_HELPER_V1" in text
        assert "airoSprint6BAlertEnginePlan_" in text
        assert "airoBuildSprint6BAlertEnginePlanReply_" in text

    def test_route_is_read_only_and_no_trigger(self):
        text = read(SRC)
        assert "sprint6b_alert_engine_plan" in text
        assert "write_performed: false" in text
        assert "google_write_performed: false" in text
        assert "proactive_send_performed: false" in text
        assert "trigger_created: false" in text

    def test_planner_has_required_alert_types(self):
        body = function_body(read(SRC), "airoSprint6BAlertEnginePlan_")
        for key in [
            "cc_due",
            "data_status_dirty",
            "partial_write_failure",
            "pending_clarification_timeout",
            "cash_threshold",
        ]:
            assert key in body

    def test_planner_has_cooldown_and_ack_foundation(self):
        body = function_body(read(SRC), "airoSprint6BAlertEnginePlan_")
        assert "cooldown_policy" in body
        assert "_AIRO_Audit_Log" in body
        assert "admin alert ack <alert_key>" in body
        assert "default_cooldown_minutes" in body

    def test_planner_reads_required_sources(self):
        body = function_body(read(SRC), "airoSprint6BAlertEnginePlan_")
        for source in [
            "Credit Card",
            "Review Queue",
            "Account Ledger",
            "Finance Events",
            "_AIRO_Audit_Log",
            "Dashboard",
        ]:
            assert source in body

    def test_planner_is_read_only(self):
        body = function_body(read(SRC), "airoSprint6BAlertEnginePlan_")
        forbidden = [
            ".clear(",
            ".clearContent(",
            ".deleteRow(",
            ".deleteRows(",
            ".deleteSheet(",
            ".appendRow(",
            ".setValue(",
            ".setValues(",
            ".insertSheet(",
            ".copyTo(",
            "ScriptApp.newTrigger",
            "sendTelegram_(",
        ]
        for item in forbidden:
            assert item not in body

    def test_v2_source_is_patched_when_present(self):
        if not V2_SRC.exists():
            return
        text = read(V2_SRC)
        assert "AIRO_SPRINT6B_ALERT_ENGINE_PLAN_ROUTE_V1" in text
        assert "AIRO_SPRINT6B_ALERT_ENGINE_PLAN_HELPER_V1" in text

    def test_current_state_records_sprint6b_start(self):
        text = read(CURRENT)
        assert "Sprint 6B Alert Engine official start" in text
        assert "Do not create triggers yet" in text
        assert "Do not send proactive alerts yet" in text
        assert "Run `admin alerts sprint6b plan`" in text
