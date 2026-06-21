from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "scripts" / "personal-workflow" / "apps-script" / "airo_finance_multitab_final_v1.gs"
V2_SRC = ROOT / "apps-script-prod-v2" / "AIRO_Finance_Multitab_Final_v1.js"
DOC = ROOT / "docs" / "AIRO_FINANCE_SPRINT_6_DASHBOARD_FINAL_BUILDER_CONTROLLED.md"
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


class TestSprint6DashboardFinalBuilderControlled:
    def test_doc_exists(self):
        assert DOC.exists()

    def test_source_has_markers(self):
        text = read(SRC)
        assert "AIRO_SPRINT6_DASHBOARD_FINAL_CONTROLLED_ROUTE_V1" in text
        assert "AIRO_SPRINT6_DASHBOARD_FINAL_CONTROLLED_BUILDER_V1" in text
        assert "airoSprint6DashboardFinalPlan_" in text
        assert "airoBuildSprint6DashboardFinalPlanReply_" in text

    def test_route_is_dry_run_and_no_write(self):
        text = read(SRC)
        assert "admin\\s+(dashboard\\s+)?sprint6\\s+(plan|dryrun|dry-run)" in text
        assert "write_performed: false" in text
        assert "google_write_performed: false" in text
        assert "mode: 'dry-run'" in text

    def test_builder_has_required_sections(self):
        body = function_body(read(SRC), "airoSprint6DashboardFinalPlan_")
        required = [
            "Topbar",
            "Action Required",
            "Executive Command Center",
            "Wallet & Cashflow",
            "Domain Health",
            "Spending Intelligence",
            "Data Quality Center",
            "Smart Insight Panel",
            "Data Status",
        ]
        for item in required:
            assert item in body

    def test_builder_locks_source_of_truth(self):
        body = function_body(read(SRC), "airoSprint6DashboardFinalPlan_")
        assert "cash_tersedia" in body and "📒 Account Ledger" in body
        assert "cc_outstanding" in body and "💳 Credit Card" in body
        assert "total_hutang" in body and "🧾 Hutang" in body
        assert "aset_emas" in body and "🏦 Aset" in body
        assert "cicilan_progress" in body and "🏠 Cicilan Rumah" in body
        assert "spending_category" in body and "🧭 Finance Events clean category" in body

    def test_policy_forbids_cash_ledger_dependency(self):
        body = function_body(read(SRC), "airoSprint6DashboardFinalPlan_")
        assert "cash_ledger_dependency: 'forbidden'" in body
        assert "permanent_second_dashboard: 'forbidden'" in body
        assert "email_ingestion_enabled=false" in body

    def test_builder_is_not_repaint_writer(self):
        body = function_body(read(SRC), "airoSprint6DashboardFinalPlan_")
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
        ]
        for item in forbidden:
            assert item not in body

    def test_reply_mentions_policy(self):
        body = function_body(read(SRC), "airoBuildSprint6DashboardFinalPlanReply_")
        assert "Sprint 6 Dashboard Final plan siap" in body
        assert "Cash Ledger dependency: FORBIDDEN" in body
        assert "Permanent second dashboard: FORBIDDEN" in body
        assert "Email Ingestion Status: HIDDEN by default" in body

    def test_v2_source_is_patched_when_present(self):
        if not V2_SRC.exists():
            return
        text = read(V2_SRC)
        assert "AIRO_SPRINT6_DASHBOARD_FINAL_CONTROLLED_ROUTE_V1" in text
        assert "AIRO_SPRINT6_DASHBOARD_FINAL_CONTROLLED_BUILDER_V1" in text

    def test_current_state_records_controlled_builder(self):
        text = read(CURRENT)
        assert "Sprint 6 Dashboard Final controlled builder" in text
        assert "No dashboard repaint yet" in text
        assert "Cash Ledger dependency remains forbidden" in text
