from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "scripts" / "personal-workflow" / "apps-script" / "airo_finance_multitab_final_v1.gs"
V2_SRC = ROOT / "apps-script-prod-v2" / "AIRO_Finance_Multitab_Final_v1.js"
DOC = ROOT / "docs" / "AIRO_FINANCE_SPRINT_6_DASHBOARD_FINAL_READBACK_VERIFIER.md"
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


class TestSprint6DashboardFinalReadbackVerifier:
    def test_doc_exists(self):
        assert DOC.exists()

    def test_source_has_readback_route_and_helper(self):
        text = read(SRC)
        assert "AIRO_SPRINT6_DASHBOARD_FINAL_READBACK_ROUTE_V1" in text
        assert "AIRO_SPRINT6_DASHBOARD_FINAL_READBACK_HELPER_V1" in text
        assert "airoSprint6DashboardFinalReadback_" in text
        assert "airoBuildSprint6DashboardFinalReadbackReply_" in text

    def test_route_is_read_only(self):
        text = read(SRC)
        assert "dashboard\\s+)?sprint6\\s+(readback|verify|check)" in text
        assert "write_performed: false" in text
        assert "google_write_performed: false" in text

    def test_readback_reads_dashboard_display_values(self):
        body = function_body(read(SRC), "airoSprint6DashboardFinalReadback_")
        assert "airoSprint6FindSheetLoose_(ss, 'Dashboard')" in body
        assert "getDisplayValues()" in body
        assert "marker_status" in body
        assert "required_marker_pass_count" in body

    def test_readback_checks_required_markers(self):
        body = function_body(read(SRC), "airoSprint6DashboardFinalReadback_")
        for marker in [
            "AIRO Finance Command Center",
            "Data Status",
            "Cash Ledger dependency",
            "FORBIDDEN",
            "Action Required",
            "Data Quality Center",
        ]:
            assert marker in body

    def test_readback_checks_backup_and_audit_log(self):
        body = function_body(read(SRC), "airoSprint6DashboardFinalReadback_")
        assert "_AIRO_Dashboard_Backup_" in body
        assert "_AIRO_Audit_Log" in body
        assert "sprint6_dashboard_final_controlled_build" in body
        assert "audit_has_build_event_in_last_rows" in body

    def test_readback_helper_is_read_only(self):
        body = function_body(read(SRC), "airoSprint6DashboardFinalReadback_")
        forbidden = [
            ".clear(",
            ".clearContent(",
            ".deleteRow(",
            ".deleteRows(",
            ".deleteSheet(",
            ".appendRow(",
            ".setValue(",
            ".setValues(",
            ".insertSheet(",
            ".copyTo(",
        ]
        for item in forbidden:
            assert item not in body

    def test_readback_checks_integrity_and_panel_safety(self):
        body = function_body(read(SRC), "airoSprint6DashboardFinalReadback_")
        assert "net_worth_panel_safe" in body
        assert "cc_panel_safe" in body
        assert "old_net_worth_collision_clean" in body
        assert "old_cc_collision_clean" in body
        assert "false_clean_detected" in body
        assert "panel_guard_pass" in body

        reply_body = function_body(read(SRC), "airoBuildSprint6DashboardFinalReadbackReply_")
        assert "Panel Guard & Integrity" in reply_body
        assert "Panel Guard Pass" in reply_body
        assert "Net Worth safe" in reply_body
        assert "Credit Card safe" in reply_body
        assert "Old NW collision clean" in reply_body
        assert "Old CC collision clean" in reply_body
        assert "False-Clean Status" in reply_body

    def test_v2_source_is_patched_when_present(self):
        if not V2_SRC.exists():
            return
        text = read(V2_SRC)
        assert "AIRO_SPRINT6_DASHBOARD_FINAL_READBACK_ROUTE_V1" in text
        assert "AIRO_SPRINT6_DASHBOARD_FINAL_READBACK_HELPER_V1" in text

    def test_current_state_records_readback_verifier(self):
        text = read(CURRENT)
        assert "Sprint 6 Dashboard Final readback verifier" in text
        assert "Do not rebuild Dashboard" in text
        assert "required marker pass is 6/6" in text
