from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "scripts" / "personal-workflow" / "apps-script" / "airo_finance_multitab_final_v1.gs"
V2_SRC = ROOT / "apps-script-prod-v2" / "AIRO_Finance_Multitab_Final_v1.js"
DOC = ROOT / "docs" / "AIRO_FINANCE_SPRINT_6_DASHBOARD_FINAL_CONTROLLED_BUILD.md"
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


class TestSprint6DashboardFinalControlledBuild:
    def test_doc_exists(self):
        assert DOC.exists()

    def test_source_has_build_route_and_helper(self):
        text = read(SRC)
        assert "AIRO_SPRINT6_DASHBOARD_FINAL_CONTROLLED_BUILD_ROUTE_V1" in text
        assert "AIRO_SPRINT6_DASHBOARD_FINAL_CONTROLLED_BUILD_HELPER_V1" in text
        assert "airoSprint6DashboardFinalBuild_" in text
        assert "airoBuildSprint6DashboardFinalBuildReply_" in text

    def test_route_supports_build_command(self):
        text = read(SRC)
        assert "dashboard\\s+)?sprint6\\s+build" in text
        assert "sprint6_dashboard_final_controlled_build" in text
        assert "write_performed: true" in text
        assert "google_write_performed: true" in text

    def test_build_creates_backup_before_clear(self):
        body = function_body(read(SRC), "airoSprint6DashboardFinalBuild_")
        assert "dashboard.copyTo(ss)" in body
        assert "_AIRO_Dashboard_Backup_" in body
        assert "dashboard.clear({ contentsOnly: false })" in body
        assert body.index("dashboard.copyTo(ss)") < body.index("dashboard.clear({ contentsOnly: false })")

    def test_build_uses_existing_dashboard(self):
        body = function_body(read(SRC), "airoSprint6DashboardFinalBuild_")
        assert "airoSprint6FindSheetLoose_(ss, 'Dashboard')" in body
        assert "Existing Dashboard tab not found" in body
        assert "insertSheet('Dashboard')" not in body
        assert 'insertSheet("Dashboard")' not in body

    def test_build_writes_required_sections(self):
        body = function_body(read(SRC), "airoSprint6DashboardFinalBuild_")
        for section in [
            "AIRO Finance Command Center",
            "Executive Command Center",
            "Action Required",
            "Domain Health",
            "Data Quality Center",
            "Smart Insight Panel",
        ]:
            assert section in body

    def test_build_keeps_policy(self):
        body = function_body(read(SRC), "airoSprint6DashboardFinalBuild_")
        assert "Cash Ledger dependency: FORBIDDEN" in body
        assert "Email Ingestion" in body
        assert "HIDDEN" in body
        assert "cash_ledger_dependency: 'forbidden'" in body

    def test_build_logs_to_audit_log(self):
        body = function_body(read(SRC), "airoSprint6DashboardFinalBuild_")
        assert "_AIRO_Audit_Log" in body
        assert "sprint6_dashboard_final_controlled_build" in body
        assert "appendRow" in body

    def test_v2_source_is_patched_when_present(self):
        if not V2_SRC.exists():
            return
        text = read(V2_SRC)
        assert "AIRO_SPRINT6_DASHBOARD_FINAL_CONTROLLED_BUILD_ROUTE_V1" in text
        assert "AIRO_SPRINT6_DASHBOARD_FINAL_CONTROLLED_BUILD_HELPER_V1" in text

    def test_current_state_records_controlled_build(self):
        text = read(CURRENT)
        assert "Sprint 6 Dashboard Final controlled build" in text
        assert "Create backup tab before overwriting Dashboard" in text
        assert "admin dashboard sprint6 build" in text
