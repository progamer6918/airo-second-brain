from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "scripts" / "personal-workflow" / "apps-script" / "airo_finance_multitab_final_v1.gs"

def read_src() -> str:
    return SRC.read_text(encoding="utf-8")


def extract_fn(text: str, fn_name: str) -> str:
    """Extract the full body of a named function."""
    start = text.index("function " + fn_name)
    brace = text.index("{", start)
    depth = 0
    for i in range(brace, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    return text[start:]


class TestAiroSprint6BLiveRunOnceAndMaxSendCapContract:
    """Phase 5B-3a: Verify admin alerts live run once and MAX_LIVE_SENDS_PER_RUN=1 cap."""

    # --- run-once route ---

    def test_run_once_route_exists(self):
        text = read_src()
        assert "admin\\s+alerts\\s+live\\s+run\\s+once" in text or "live run once" in text.lower()

    def test_run_once_route_label_present(self):
        text = read_src()
        assert "AIRO_SPRINT6B_LIVE_RUN_ONCE_ROUTE_V1" in text

    def test_run_once_invokes_live_handler(self):
        text = read_src()
        # Route must call airoSprint6BTriggerHandlerLive_
        idx = text.index("AIRO_SPRINT6B_LIVE_RUN_ONCE_ROUTE_V1")
        block = text[idx:idx + 2000]
        assert "airoSprint6BTriggerHandlerLive_" in block

    def test_run_once_does_not_install_trigger(self):
        text = read_src()
        idx = text.index("AIRO_SPRINT6B_LIVE_RUN_ONCE_ROUTE_V1")
        block = text[idx:idx + 3500]
        assert "ScriptApp.newTrigger" not in block
        assert "InstallLiveTrigger" not in block
        assert "trigger_created" in block

    def test_run_once_does_not_change_live_switch(self):
        text = read_src()
        idx = text.index("AIRO_SPRINT6B_LIVE_RUN_ONCE_ROUTE_V1")
        block = text[idx:idx + 3500]
        assert "SetLiveEnabled_" not in block
        assert "live_switch_mutated" in block

    def test_run_once_returns_proactive_send_performed(self):
        text = read_src()
        idx = text.index("AIRO_SPRINT6B_LIVE_RUN_ONCE_ROUTE_V1")
        block = text[idx:idx + 2000]
        assert "proactive_send_performed" in block

    def test_run_once_sends_telegram_reply(self):
        text = read_src()
        idx = text.index("AIRO_SPRINT6B_LIVE_RUN_ONCE_ROUTE_V1")
        block = text[idx:idx + 3500]
        assert "sendTelegram_" in block

    # --- MAX_LIVE_SENDS_PER_RUN cap ---

    def test_max_live_sends_constant_defined(self):
        text = read_src()
        assert "MAX_LIVE_SENDS_PER_RUN = 1" in text

    def test_max_live_sends_cap_only_on_live_mode(self):
        """Cap constant must be inside the runner, conditioned on isLiveSendMode."""
        body = extract_fn(read_src(), "airoSprint6BAlertRunnerSafeMode_")
        assert "MAX_LIVE_SENDS_PER_RUN" in body
        assert "isLiveSendMode" in body

    def test_send_loop_uses_cap_limit(self):
        """Send loop must terminate at sendLimit, not iterate all eligible."""
        body = extract_fn(read_src(), "airoSprint6BAlertRunnerSafeMode_")
        assert "sentCount < sendLimit" in body or "sentCount < MAX_LIVE_SENDS_PER_RUN" in body

    def test_result_exposes_max_live_sends_per_run(self):
        """Result object must include max_live_sends_per_run field."""
        body = extract_fn(read_src(), "airoSprint6BAlertRunnerSafeMode_")
        assert "max_live_sends_per_run" in body

    def test_result_exposes_send_cap_applied(self):
        body = extract_fn(read_src(), "airoSprint6BAlertRunnerSafeMode_")
        assert "send_cap_applied" in body

    def test_result_exposes_eligible_before_cap(self):
        body = extract_fn(read_src(), "airoSprint6BAlertRunnerSafeMode_")
        assert "eligible_before_cap" in body

    def test_cap_not_applied_to_safe_dry_run(self):
        """Non-live send modes must NOT have sendLimit reduced to 1."""
        body = extract_fn(read_src(), "airoSprint6BAlertRunnerSafeMode_")
        # isLiveSendMode is only true when shouldSend=true AND mode='live'
        assert "isLiveSendMode" in body
        # The sendLimit fallback for non-live mode must be eligible.length (i.e. no cap)
        assert "eligible.length" in body

    def test_proactive_send_performed_reflects_actual_sent_count(self):
        """proactive_send_performed in result must be based on sentCount > 0, not shouldSend."""
        body = extract_fn(read_src(), "airoSprint6BAlertRunnerSafeMode_")
        assert "proactive_send_performed: sentCount > 0" in body

    # --- Existing safety contracts remain intact ---

    def test_cooldown_check_still_present_in_runner(self):
        body = extract_fn(read_src(), "airoSprint6BAlertRunnerSafeMode_")
        assert "isCooldownSuppressed" in body

    def test_quiet_hours_check_still_present_in_runner(self):
        body = extract_fn(read_src(), "airoSprint6BAlertRunnerSafeMode_")
        assert "isQuietHoursSuppressed" in body or "isQuietHours" in body

    def test_live_handler_disabled_path_still_no_send(self):
        """Live handler when disabled must still record 0 sent and proactive=false."""
        body = extract_fn(read_src(), "airoSprint6BTriggerHandlerLive_")
        assert "sprint6b_trigger_live_disabled_heartbeat" in body
        assert "sent_count: 0" in body
        assert "proactive_send_performed: false" in body

    def test_no_new_delete_sheet_calls(self):
        text = read_src()
        assert "deleteSheet" not in text

    def test_no_new_show_sheet_calls_beyond_baseline(self):
        text = read_src()
        assert text.count("showSheet") <= 1

    def test_safe_handler_unchanged(self):
        body = extract_fn(read_src(), "airoSprint6BTriggerHandlerSafe_")
        assert "sprint6b_trigger_safe_heartbeat" in body
