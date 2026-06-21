from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs" / "AIRO_FINANCE_SPRINT_6B_ALERT_ENGINE_PLANNER_LIVE_PASS.md"
CURRENT = ROOT / "docs" / "AIRO_FINANCE_CURRENT_STATE.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestSprint6BAlertEnginePlannerLivePass:
    def test_doc_exists(self):
        assert DOC.exists()

    def test_records_command_and_safety(self):
        text = read(DOC)
        assert "admin alerts sprint6b plan" in text
        assert "Mode: dry-run" in text
        assert "Write performed: false" in text
        assert "Proactive send performed: false" in text
        assert "Trigger created: false" in text

    def test_records_current_trust(self):
        text = read(DOC)
        assert "Data Status: Warning" in text
        assert "Critical: 0" in text
        assert "Alert candidates: 7" in text

    def test_records_sources_ok(self):
        text = read(DOC)
        for source in [
            "dashboard: OK",
            "account_ledger: OK",
            "finance_events: OK",
            "credit_card: OK",
            "review_queue: OK",
            "audit_log: OK",
        ]:
            assert source in text

    def test_records_alert_types(self):
        text = read(DOC)
        for alert_type in [
            "cc_due",
            "data_status_dirty",
            "partial_write_failure",
            "pending_clarification_timeout",
            "cash_threshold",
        ]:
            assert alert_type in text

    def test_records_cooldown_and_ack(self):
        text = read(DOC)
        assert "Storage: _AIRO_Audit_Log" in text
        assert "ACK planned: admin alert ack <alert_key>" in text

    def test_current_state_records_live_pass(self):
        text = read(CURRENT)
        assert "Sprint 6B Alert Engine planner live pass" in text
        assert "Do not create triggers yet" in text
        assert "Implement scheduled alert runner in safe mode" in text
