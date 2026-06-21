from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "scripts" / "personal-workflow" / "apps-script" / "airo_finance_multitab_final_v1.gs"
V2_SRC = ROOT / "apps-script-prod-v2" / "AIRO_Finance_Multitab_Final_v1.js"
DOC = ROOT / "docs" / "AIRO_FINANCE_SPRINT_6B_DUPLICATE_SUPPRESSION_RUNNER.md"
CURRENT = ROOT / "docs" / "AIRO_FINANCE_CURRENT_STATE.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def region_after(text: str, marker: str) -> str:
    start = text.index(marker)
    end = text.find("const specialCommand = handleSpecialFinanceCommand_", start)
    if end == -1:
        return text[start:]
    return text[start:end]


class TestSprint6BDuplicateSuppressionRunner:
    def test_doc_exists(self):
        assert DOC.exists()

    def test_source_has_markers(self):
        text = read(SRC)
        assert "AIRO_SPRINT6B_DUPLICATE_SUPPRESSION_RUNNER_ROUTE_V1" in text
        assert "AIRO_SPRINT6B_DUPLICATE_SUPPRESSION_RUNNER_HELPER_V1" in text
        assert "airoSprint6BDuplicateSuppressionRunner_" in text
        assert "airoBuildSprint6BDuplicateSuppressionRunnerReply_" in text

    def test_route_is_read_only(self):
        text = read(SRC)
        assert "sprint6b_duplicate_suppression_runner" in text
        assert "write_performed: false" in text
        assert "google_write_performed: false" in text
        assert "proactive_send_performed: false" in text
        assert "trigger_created: false" in text

    def test_duplicate_decision_logic_exists(self):
        text = read(SRC)
        assert "BLOCK_DUPLICATE" in text
        assert "WOULD_SEND_IF_TRIGGER_ENABLED" in text
        assert "target_decision" in text
        assert "hasSuppressed" in text

    def test_uses_cooldown_readback(self):
        text = read(SRC)
        assert "airoSprint6BCooldownSuppressionReadback_" in text
        assert "target_suppressed" in text
        assert "blocked_duplicate_count" in text

    def test_no_trigger_creation_in_route_region(self):
        text = read(SRC)
        route = region_after(text, "AIRO_SPRINT6B_DUPLICATE_SUPPRESSION_RUNNER_ROUTE_V1")
        assert "ScriptApp.newTrigger" not in route

    def test_v2_patched(self):
        if V2_SRC.exists():
            text = read(V2_SRC)
            assert "AIRO_SPRINT6B_DUPLICATE_SUPPRESSION_RUNNER_ROUTE_V1" in text
            assert "AIRO_SPRINT6B_DUPLICATE_SUPPRESSION_RUNNER_HELPER_V1" in text

    def test_current_state_records_duplicate_runner(self):
        text = read(CURRENT)
        assert "Sprint 6B duplicate suppression runner" in text
        assert "Proves suppressed alert will not be sent again" in text
        assert "Run duplicate check in Telegram" in text
