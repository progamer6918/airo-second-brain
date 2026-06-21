from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "scripts" / "personal-workflow" / "apps-script" / "airo_finance_multitab_final_v1.gs"
V2_SRC = ROOT / "apps-script-prod-v2" / "AIRO_Finance_Multitab_Final_v1.js"
DOC = ROOT / "docs" / "AIRO_FINANCE_SPRINT_5_DASHBOARD_SAFE_ANALYTICS_PATCH.md"
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


class TestSprint5DashboardSafeAnalyticsPatch:
    def test_doc_exists_and_declares_not_repaint(self):
        text = read(DOC)
        assert "Dashboard-Safe Reconciliation Analytics Patch" in text
        assert "This is not Sprint 6 repaint" in text

    def test_canonical_source_has_dashboard_safe_marker(self):
        text = read(SRC)
        assert "AIRO_SPRINT5_DASHBOARD_SAFE_ANALYTICS_V1" in text
        assert "airoBuildSprint5DashboardAnalytics_" in text
        assert "airoApplySprint5DashboardAnalytics_" in text

    def test_canonical_helper_emits_required_fields(self):
        text = read(SRC)
        assert "dashboard_analytics" in text
        assert "data_status" in text
        assert "dashboard_status" in text
        assert "issue_count_active" in text
        assert "issue_count_legacy" in text
        assert "critical_count" in text
        assert "warning_count" in text
        assert "action_required" in text

    def test_read_only_reconciliation_applies_analytics_before_return(self):
        body = function_body(read(SRC), "airoSprint5ReconciliationReadOnly_")
        assert "airoApplySprint5DashboardAnalytics_(result);" in body
        assert body.index("airoApplySprint5DashboardAnalytics_(result);") < body.rindex("return result;")

    def test_reply_builder_includes_dashboard_analytics_section(self):
        body = function_body(read(SRC), "airoBuildSprint5ReconciliationReply_")
        assert "AIRO_SPRINT5_DASHBOARD_SAFE_ANALYTICS_REPLY_V1" in body
        assert "Dashboard Analytics" in body
        assert "Data Status" in body
        assert "Action Required" in body

    def test_analytics_helper_stays_read_only(self):
        body = function_body(read(SRC), "airoBuildSprint5DashboardAnalytics_")
        forbidden = [
            ".appendRow(",
            ".setValue(",
            ".setValues(",
            ".deleteRow(",
            ".deleteRows(",
            ".insertRow",
            ".clearContent(",
            ".clear(",
            "SpreadsheetApp.openById",
        ]
        for item in forbidden:
            assert item not in body

    def test_v2_source_is_patched_when_present(self):
        if not V2_SRC.exists():
            return
        text = read(V2_SRC)
        assert "AIRO_SPRINT5_DASHBOARD_SAFE_ANALYTICS_V1" in text
        assert "AIRO_SPRINT5_DASHBOARD_SAFE_ANALYTICS_REPLY_V1" in text
        assert "airoApplySprint5DashboardAnalytics_(result);" in text

    def test_current_state_records_patch(self):
        text = read(CURRENT)
        assert "Sprint 5 dashboard-safe reconciliation analytics patch" in text
        assert "Add dashboard_analytics to read-only reconciliation output" in text
