from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "scripts" / "personal-workflow" / "apps-script" / "airo_finance_multitab_final_v1.gs"
V2_SRC = ROOT / "apps-script-prod-v2" / "AIRO_Finance_Multitab_Final_v1.js"
DOC = ROOT / "docs" / "AIRO_FINANCE_SPRINT_6_ENSURE_AUDIT_LOG_TAB.md"
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


class TestSprint6EnsureAuditLogTab:
    def test_doc_exists(self):
        assert DOC.exists()

    def test_source_has_route_and_helper(self):
        text = read(SRC)
        assert "AIRO_SPRINT6_ENSURE_AUDIT_LOG_ROUTE_V1" in text
        assert "AIRO_SPRINT6_ENSURE_AUDIT_LOG_HELPER_V1" in text
        assert "airoSprint6EnsureAuditLogTab_" in text
        assert "airoBuildSprint6EnsureAuditLogReply_" in text

    def test_route_supports_commands(self):
        text = read(SRC)
        assert "admin\\s+(ensure\\s+)?audit\\s+log" in text
        assert "admin\\s+sprint6\\s+ensure\\s+audit\\s+log" in text
        assert "sprint6_ensure_audit_log" in text

    def test_helper_creates_or_verifies_audit_log(self):
        body = function_body(read(SRC), "airoSprint6EnsureAuditLogTab_")
        assert "_AIRO_Audit_Log" in body
        assert "insertSheet(tabName)" in body
        assert "setValues([headers])" in body
        assert "appendRow" in body
        assert "write_performed: true" in body
        assert "google_write_performed: true" in body

    def test_headers_are_defined(self):
        body = function_body(read(SRC), "airoSprint6EnsureAuditLogTab_")
        for header in [
            "timestamp",
            "actor",
            "event_type",
            "severity",
            "source",
            "message",
            "ref",
            "metadata_json",
        ]:
            assert header in body

    def test_v2_source_is_patched_when_present(self):
        if not V2_SRC.exists():
            return
        text = read(V2_SRC)
        assert "AIRO_SPRINT6_ENSURE_AUDIT_LOG_ROUTE_V1" in text
        assert "AIRO_SPRINT6_ENSURE_AUDIT_LOG_HELPER_V1" in text

    def test_current_state_records_ensure_audit_log(self):
        text = read(CURRENT)
        assert "Sprint 6 ensure Audit Log tab" in text
        assert "_AIRO_Audit_Log" in text
        assert "Run ensure command in Telegram" in text
