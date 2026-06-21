from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "scripts" / "personal-workflow" / "apps-script" / "airo_finance_multitab_final_v1.gs"

def read_src() -> str:
    return SRC.read_text(encoding="utf-8")

class TestAiroSprint6BActiveAlertCalculationsContract:
    def test_quiet_hours_helper_exists(self):
        text = read_src()
        assert "function airoSprint6BIsQuietHours_" in text
        assert "Asia/Jakarta" in text
        assert "Utilities.formatDate" in text

    def test_quiet_hours_suppression_logic(self):
        text = read_src()
        assert "suppressed_by_quiet_hours" in text
        assert "quiet_hours_active" in text

    def test_cc_due_candidate_calculation_source_driven(self):
        text = read_src()
        assert "ccTab.exists" in text
        assert "source_missing" in text
        assert "findCcHeaderRow_" in text
        assert "ccBillingCycle_" in text
        assert "ccDueDateForCycle_" in text

    def test_cash_threshold_candidate_calculation_source_driven(self):
        text = read_src()
        assert "accountTab.exists" in text
        assert "findHeader_" in text
        assert "Cash Umum" in text
        assert "Cash Bensin" in text
        assert "Cash" in text
        assert "Settings" in text

    def test_dirty_status_partial_write_missing_category_checks(self):
        text = read_src()
        assert "data_status_dirty" in text
        assert "data_status_warning" in text
        assert "partial_write_failure" in text
        assert "missing_category" in text

    def test_safe_runner_respects_cooldown_and_duplicate(self):
        text = read_src()
        assert "cooldown_suppressed_count" in text
        assert "quiet_hours_suppressed_count" in text
        assert "suppressed_by_cooldown" in text

    def test_safe_trigger_does_not_perform_live_sends(self):
        text = read_src()
        start = text.index("function airoSprint6BTriggerHandlerSafe_")
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
        assert "sendTelegram_(" not in body

    def test_no_hardcoded_cooldown_date_keys(self):
        text = read_src()
        assert "data_status_warning:20260527" not in text

    def test_cooldown_readback_logic(self):
        text = read_src()
        assert "targetKey || null" in text
        assert "status: hasSuppressed ? 'OK' : 'NO_SUPPRESSED_CANDIDATE'" in text

    def test_duplicate_suppression_runner_logic(self):
        text = read_src()
        assert "targetDecision = 'NO_SUPPRESSED_CANDIDATE'" in text

    def test_no_live_send_and_trigger_in_cooldown_duplicate(self):
        text = read_src()
        for fn in ["airoSprint6BDuplicateSuppressionRunner_", "airoSprint6BCooldownSuppressionReadback_"]:
            start = text.index(f"function {fn}")
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
            assert "sendTelegram_" not in body
            assert "ScriptApp.newTrigger" not in body
