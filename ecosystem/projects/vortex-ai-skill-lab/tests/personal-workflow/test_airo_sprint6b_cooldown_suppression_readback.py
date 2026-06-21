from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "scripts" / "personal-workflow" / "apps-script" / "airo_finance_multitab_final_v1.gs"
V2_SRC = ROOT / "apps-script-prod-v2" / "AIRO_Finance_Multitab_Final_v1.js"
DOC = ROOT / "docs" / "AIRO_FINANCE_SPRINT_6B_COOLDOWN_SUPPRESSION_READBACK.md"
CURRENT = ROOT / "docs" / "AIRO_FINANCE_CURRENT_STATE.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def region_after(text: str, marker: str) -> str:
    start = text.index(marker)
    end = text.find("const specialCommand = handleSpecialFinanceCommand_", start)
    if end == -1:
        return text[start:]
    return text[start:end]


class TestSprint6BCooldownSuppressionReadback:
    def test_doc_exists(self):
        assert DOC.exists()

    def test_source_has_markers(self):
        text = read(SRC)
        assert "AIRO_SPRINT6B_COOLDOWN_SUPPRESSION_READBACK_ROUTE_V1" in text
        assert "AIRO_SPRINT6B_COOLDOWN_SUPPRESSION_READBACK_HELPER_V1" in text
        assert "airoSprint6BCooldownSuppressionReadback_" in text
        assert "airoBuildSprint6BCooldownSuppressionReadbackReply_" in text

    def test_route_is_read_only(self):
        text = read(SRC)
        assert "sprint6b_cooldown_suppression_readback" in text
        assert "write_performed: false" in text
        assert "google_write_performed: false" in text
        assert "proactive_send_performed: false" in text
        assert "trigger_created: false" in text

    def test_reads_audit_log_and_alert_key(self):
        text = read(SRC)
        assert "_AIRO_Audit_Log" in text
        assert "alert_key" in text
        assert "target_key_checked" in text
        assert "target_key_suppressed" in text

    def test_no_trigger_creation_in_route_region(self):
        text = read(SRC)
        route = region_after(text, "AIRO_SPRINT6B_COOLDOWN_SUPPRESSION_READBACK_ROUTE_V1")
        assert "ScriptApp.newTrigger" not in route

    def test_v2_patched(self):
        if V2_SRC.exists():
            text = read(V2_SRC)
            assert "AIRO_SPRINT6B_COOLDOWN_SUPPRESSION_READBACK_ROUTE_V1" in text
            assert "AIRO_SPRINT6B_COOLDOWN_SUPPRESSION_READBACK_HELPER_V1" in text

    def test_current_state_records_cooldown_readback(self):
        text = read(CURRENT)
        assert "Sprint 6B cooldown suppression readback" in text
        assert "Read-only cooldown suppression verifier" in text
        assert "Run cooldown check in Telegram" in text
