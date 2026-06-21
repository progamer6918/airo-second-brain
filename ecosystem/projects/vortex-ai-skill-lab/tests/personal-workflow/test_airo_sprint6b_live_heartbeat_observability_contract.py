from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "scripts" / "personal-workflow" / "apps-script" / "airo_finance_multitab_final_v1.gs"

def read_src() -> str:
    return SRC.read_text(encoding="utf-8")


class TestAiroSprint6BLiveHeartbeatObservabilityContract:
    """Phase 5B-2a: Verify that live and safe heartbeat logs are separated."""

    def test_distinct_live_disabled_heartbeat_action_exists(self):
        """Live handler should write sprint6b_trigger_live_disabled_heartbeat when live is disabled."""
        text = read_src()
        assert "sprint6b_trigger_live_disabled_heartbeat" in text

    def test_distinct_live_enabled_heartbeat_action_exists(self):
        """Live handler should write sprint6b_trigger_live_enabled_heartbeat when live is enabled."""
        text = read_src()
        assert "sprint6b_trigger_live_enabled_heartbeat" in text

    def test_disabled_heartbeat_records_fail_closed_fields(self):
        """Disabled heartbeat path must record live_enabled=false, sent_count=0, proactive_send_performed=false."""
        text = read_src()
        # Extract the live handler body (not the readback scanner)
        fn_start = text.index("function airoSprint6BTriggerHandlerLive_")
        brace = text.index("{", fn_start)
        depth = 0
        end = fn_start
        for i in range(brace, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        body = text[fn_start:end]
        # Verify disabled path exists with correct sentinel fields
        assert "sprint6b_trigger_live_disabled_heartbeat" in body
        assert "live_enabled: false" in body
        assert "sent_count: 0" in body
        assert "proactive_send_performed: false" in body

    def test_enabled_heartbeat_records_live_enabled_true_fields(self):
        """Enabled heartbeat path must record live_enabled=true."""
        text = read_src()
        # Extract the live handler body (not the readback scanner)
        fn_start = text.index("function airoSprint6BTriggerHandlerLive_")
        brace = text.index("{", fn_start)
        depth = 0
        end = fn_start
        for i in range(brace, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        body = text[fn_start:end]
        assert "sprint6b_trigger_live_enabled_heartbeat" in body
        assert "live_enabled: true" in body

    def test_get_live_status_returns_separate_safe_and_live_summary_fields(self):
        """airoSprint6BGetLiveStatus_ must return both last_safe_summary and last_live_summary."""
        text = read_src()
        assert "last_safe_summary" in text
        assert "last_live_summary" in text

    def test_get_live_status_reads_safe_heartbeat_for_safe_summary(self):
        """GetLiveStatus must scan for sprint6b_trigger_safe_heartbeat for safe summary."""
        text = read_src()
        fn_start = text.index("function airoSprint6BGetLiveStatus_")
        brace = text.index("{", fn_start)
        depth = 0
        end = fn_start
        for i in range(brace, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        body = text[fn_start:end]
        assert "sprint6b_trigger_safe_heartbeat" in body
        assert "lastSafeSummary" in body

    def test_get_live_status_reads_live_heartbeat_for_live_summary(self):
        """GetLiveStatus must scan for live heartbeat action types for live summary."""
        text = read_src()
        fn_start = text.index("function airoSprint6BGetLiveStatus_")
        brace = text.index("{", fn_start)
        depth = 0
        end = fn_start
        for i in range(brace, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        body = text[fn_start:end]
        assert "sprint6b_trigger_live_disabled_heartbeat" in body or "sprint6b_trigger_live_enabled_heartbeat" in body
        assert "lastLiveSummary" in body

    def test_admin_live_status_reply_shows_last_safe_heartbeat(self):
        """admin alerts live status reply must include Last Safe Heartbeat field."""
        text = read_src()
        assert "Last Safe Heartbeat" in text

    def test_admin_live_status_reply_shows_last_live_heartbeat(self):
        """admin alerts live status reply must include Last Live Heartbeat field."""
        text = read_src()
        assert "Last Live Heartbeat" in text

    def test_live_handler_disabled_path_does_not_call_sendtelegram(self):
        """Disabled live heartbeat path must not call sendTelegram_ directly."""
        text = read_src()
        fn_start = text.index("function airoSprint6BTriggerHandlerLive_")
        brace = text.index("{", fn_start)
        depth = 0
        fn_body_end = fn_start
        for i in range(brace, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    fn_body_end = i + 1
                    break
        full_body = text[fn_start:fn_body_end]
        # The disabled path ends at 'return result;' before the live-enabled block
        # Find disabled block: from start to first 'return result;'
        first_return = full_body.index("return result;")
        disabled_block = full_body[:first_return]
        assert "sendTelegram_" not in disabled_block

    def test_no_new_delete_sheet_calls(self):
        """No deleteSheet calls must be present anywhere in the source."""
        text = read_src()
        assert "deleteSheet" not in text

    def test_no_new_show_sheet_calls_beyond_baseline(self):
        """showSheet call count must not increase beyond prior baseline (≤1)."""
        text = read_src()
        assert text.count("showSheet") <= 1

    def test_safe_trigger_handler_still_writes_safe_heartbeat_action(self):
        """Safe handler must still write sprint6b_trigger_safe_heartbeat."""
        text = read_src()
        fn_start = text.index("function airoSprint6BTriggerHandlerSafe_")
        brace = text.index("{", fn_start)
        depth = 0
        end = fn_start
        for i in range(brace, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        body = text[fn_start:end]
        assert "sprint6b_trigger_safe_heartbeat" in body
