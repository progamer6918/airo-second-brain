from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "scripts" / "personal-workflow" / "apps-script" / "airo_finance_multitab_final_v1.gs"


def read_src() -> str:
    return SRC.read_text(encoding="utf-8")


def extract_function(text: str, name: str) -> str:
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
    raise AssertionError(f"Function {name} not found")


class TestAiroDashboardV2Contract(unittest.TestCase):
    def test_do_post_routes_dashboard_v2_commands(self):
        text = read_src()
        # Verify route pattern for admin dashboard v2 build
        self.assertIn("admin\\s+(dashboard\\s+)?v2\\s+build\\s*$", text)
        self.assertIn("sprint6_dashboard_v2_build", text)
        
        # Verify route pattern for admin dashboard v2 readback
        self.assertIn("admin\\s+(dashboard\\s+)?v2\\s+(readback|verify|check)\\s*$", text)
        self.assertIn("sprint6_dashboard_v2_readback", text)

        # Verify route pattern for admin promote dashboard
        self.assertIn("admin\\s+promote\\s+dashboard\\s*$", text)
        self.assertIn("dashboard_promote", text)

        # Verify route pattern for admin dashboard build
        self.assertIn("admin\\s+dashboard\\s+build\\s*$", text)
        self.assertIn("dashboard_build", text)

        # Verify route pattern for admin dashboard readback
        self.assertIn("admin\\s+dashboard\\s+(readback|verify|check)\\s*$", text)
        self.assertIn("dashboard_readback", text)

        # Verify route pattern for admin cleanup tabs
        self.assertIn("admin\\s+cleanup\\s+tabs\\s*$", text)
        self.assertIn("dashboard_cleanup_tabs", text)

    def test_dashboard_v2_build_uses_preview_tab(self):
        body = extract_function(read_src(), "airoSprint6DashboardV2Build_")
        
        # Must only build in '🏠 Dashboard v2'
        self.assertIn("🏠 Dashboard v2", body)
        self.assertNotIn("insertSheet('Dashboard')", body)
        self.assertNotIn("insertSheet(\"Dashboard\")", body)
        self.assertNotIn("sheetName = '🏠 Dashboard'", body)
        
        # Check size configuration
        self.assertIn("41", body)
        self.assertIn("26", body)
        
        # Should set Arial font
        self.assertIn("'Arial'", read_src())
        
        # Should NOT contain technical ops details
        self.assertNotIn("Live Trigger Count", body)
        self.assertNotIn("Safe Trigger Count", body)
        self.assertNotIn("Apps Script Runtime", body)
        self.assertNotIn("Deployment ID", body)
        
        # Must build key user-facing sections and cards
        self.assertIn("⚡ ACTION REQUIRED", body)
        self.assertIn("🎯 EXECUTIVE COMMAND CENTER", body)
        self.assertIn("Net worth", body)
        self.assertIn("Cash tersedia", body)
        self.assertIn("Cashflow bln ini", body)
        self.assertIn("Critical alerts", body)
        self.assertIn("Total aset", body)
        self.assertIn("Total hutang", body)
        self.assertIn("Saving rate", body)
        self.assertIn("Cicilan rumah", body)
        
        self.assertIn("WALLET & CASHFLOW", body)
        self.assertIn("DOMAIN HEALTH", body)
        self.assertIn("SPENDING INTELLIGENCE", body)
        self.assertIn("DATA QUALITY CENTER", body)
        self.assertIn("SMART INSIGHT PANEL", body)

    def test_dashboard_v2_build_ops_center_handles_technical_details(self):
        body = extract_function(read_src(), "airoSprint6DashboardV2BuildOpsCenter_")
        
        # Writes to the background ops tab
        self.assertIn("_AIRO_Ops_Center", body)
        
        # Handles operational metrics
        self.assertIn("Deployment ID", body)
        self.assertIn("Apps Script Runtime", body)
        self.assertIn("Live Switch Status", body)
        self.assertIn("ADMIN_CHAT_ID", body)
        self.assertIn("Live Trigger Count", body)
        self.assertIn("Safe Trigger Count", body)
        self.assertIn("Last Live Heartbeat", body)
        self.assertIn("Last Safe Heartbeat", body)

    def test_dashboard_v2_readback_markers(self):
        body = extract_function(read_src(), "airoSprint6DashboardV2Readback_")
        
        self.assertIn("🏠 Dashboard v2", body)
        self.assertIn("ACTION REQUIRED", body)
        self.assertIn("EXECUTIVE COMMAND CENTER", body)
        self.assertIn("WALLET & CASHFLOW", body)
        self.assertIn("DOMAIN HEALTH", body)
        self.assertIn("SPENDING", body)
        self.assertIn("DATA QUALITY", body)
        self.assertIn("SMART INSIGHT", body)

    def test_on_edit_watches_both_dashboards(self):
        body = extract_function(read_src(), "onEdit")
        self.assertIn("sheetName === '🏠 Dashboard v2'", body)
        self.assertIn("sheetName === '🏠 Dashboard'", body)
        self.assertIn("G2", body)

    def test_dashboard_promotion_functions_exist(self):
        text = read_src()
        self.assertIn("function airoDashboardPromoteToMain_", text)
        self.assertIn("function airoDashboardCleanupTabs_", text)


if __name__ == "__main__":
    unittest.main()
