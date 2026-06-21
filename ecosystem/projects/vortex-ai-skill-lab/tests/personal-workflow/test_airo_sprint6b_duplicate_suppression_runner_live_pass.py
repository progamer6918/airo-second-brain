from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs" / "AIRO_FINANCE_SPRINT_6B_DUPLICATE_SUPPRESSION_RUNNER_LIVE_PASS.md"
CURRENT = ROOT / "docs" / "AIRO_FINANCE_CURRENT_STATE.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestSprint6BDuplicateSuppressionRunnerLivePass:
    def test_doc_exists(self):
        assert DOC.exists()

    def test_records_command_and_safety(self):
        text = read(DOC)
        assert "admin alerts sprint6b duplicate check" in text
        assert "Mode: read-only" in text
        assert "Write performed: false" in text
        assert "Proactive send performed: false" in text
        assert "Trigger created: false" in text

    def test_records_decision_summary(self):
        text = read(DOC)
        assert "Evaluated: 7" in text
        assert "Blocked duplicate: 1" in text
        assert "Would send if trigger enabled: 6" in text
        assert "Sent: 0" in text

    def test_records_target_blocked(self):
        text = read(DOC)
        assert "data_status_warning:20260527:WARNING" in text
        assert "Suppressed: true" in text
        assert "Decision: BLOCK_DUPLICATE" in text

    def test_records_next_guardrail(self):
        text = read(DOC)
        assert "Do not install scheduled trigger" in text
        assert "guarded scheduled trigger installer" in text
        assert "manual trigger uninstall command" in text

    def test_current_state_records_live_pass(self):
        text = read(CURRENT)
        assert "Sprint 6B duplicate suppression runner live pass" in text
        assert "Target decision: BLOCK_DUPLICATE" in text
        assert "Implement guarded scheduled trigger installer" in text
