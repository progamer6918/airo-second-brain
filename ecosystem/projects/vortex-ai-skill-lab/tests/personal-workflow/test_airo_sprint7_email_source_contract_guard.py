from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "scripts" / "personal-workflow" / "apps-script" / "airo_finance_multitab_final_v1.gs"
V2_SRC = ROOT / "apps-script-prod-v2" / "AIRO_Finance_Multitab_Final_v1.js"
DOC = ROOT / "docs" / "AIRO_FINANCE_SPRINT_7_EMAIL_SOURCE_CONTRACT_GUARD.md"
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


def route_region(text: str) -> str:
    start = text.index("AIRO_SPRINT7_EMAIL_SOURCE_CONTRACT_GUARD_ROUTE_V1")
    end = text.find("const specialCommand = handleSpecialFinanceCommand_", start)
    if end == -1:
        return text[start:]
    return text[start:end]


class TestSprint7EmailSourceContractGuard:
    def test_doc_exists(self):
        assert DOC.exists()

    def test_source_has_markers(self):
        text = read(SRC)
        assert "AIRO_SPRINT7_EMAIL_SOURCE_CONTRACT_GUARD_HELPER_V1" in text
        assert "AIRO_SPRINT7_EMAIL_SOURCE_CONTRACT_GUARD_ROUTE_V1" in text
        assert "airoSprint7EmailSourceContractGuard_" in text
        assert "airoBuildSprint7EmailSourceContractGuardReply_" in text

    def test_route_is_dry_run_and_safe(self):
        text = read(SRC)
        route = route_region(text)
        assert "mode: 'dry-run'" in route
        assert "write_performed: false" in route
        assert "gmail_read_performed: false" in route
        assert "gmail_trigger_created: false" in route
        assert "finance_write_performed: false" in route
        assert "trigger_created: false" in route

    def test_helper_does_not_read_gmail_or_create_trigger(self):
        text = read(SRC)
        body = function_body(text, "airoSprint7EmailSourceContractGuard_")
        forbidden = [
            "GmailApp",
            "MailApp",
            "ScriptApp.newTrigger",
            ".appendRow(",
            ".setValue(",
            ".setValues(",
            "sendTelegram_(",
        ]
        for item in forbidden:
            assert item not in body

    def test_contract_defaults_off(self):
        text = read(SRC)
        assert "EMAIL_INGESTION_ENABLED" in text
        assert "EMAIL_INGESTION_DRY_RUN_ONLY" in text
        assert "email_ingestion_default_off" in text
        assert "dry_run_only" in text

    def test_contract_requires_guardrails(self):
        text = read(SRC)
        for item in [
            "EMAIL_INGESTION_ALLOWED_SENDERS",
            "EMAIL_INGESTION_LABEL",
            "review_queue_fallback_required",
            "audit_log_required",
            "duplicate_detection_required",
            "kill_switch_required",
            "dashboard_hidden_until_enabled",
        ]:
            assert item in text

    def test_v2_patched_when_present(self):
        if V2_SRC.exists():
            text = read(V2_SRC)
            assert "AIRO_SPRINT7_EMAIL_SOURCE_CONTRACT_GUARD_HELPER_V1" in text
            assert "AIRO_SPRINT7_EMAIL_SOURCE_CONTRACT_GUARD_ROUTE_V1" in text

    def test_current_state_records_guard(self):
        text = read(CURRENT)
        assert "Sprint 7 email source contract guard" in text
        assert "Email Ingestion remains default OFF" in text
        assert "Run guard command in Telegram" in text
