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


class TestDashboardAlertAwareContract(unittest.TestCase):
    def test_analytics_handles_missing_admin_chat_and_warnings(self):
        body = extract_function(read_src(), "airoBuildSprint5DashboardAnalytics_")
        
        # Verify getProp_('ADMIN_CHAT_ID') is checked
        self.assertIn("getProp_('ADMIN_CHAT_ID')", body)
        self.assertIn("!isChatConfigured", body)
        self.assertIn("alert_engine_missing_admin_chat", body)
        self.assertIn("Register Chat", body)
        
        # Verify warnings check
        self.assertIn("alertStatus.warning", body)
        self.assertIn("alert_engine_trigger_mismatch", body)
        self.assertIn("Fix Trigger", body)
        
        # Verify data_status decisions
        self.assertIn("!isChatConfigured ? 'Critical Alert Engine configuration issue detected.'", body)
        self.assertIn("alertStatus.warning ? 'Alert engine trigger mismatch detected.'", body)

    def test_dashboard_build_integrates_observability_rows(self):
        body = extract_function(read_src(), "airoSprint6DashboardFinalBuild_")
        
        # Verify call to get live status
        self.assertIn("airoSprint6BGetLiveStatus_(ss)", body)
        
        # Verify alert engine observability rows in qualityRows
        self.assertIn("Alert Engine State", body)
        self.assertIn("ADMIN_CHAT_ID", body)
        self.assertIn("Live Trigger Count", body)
        self.assertIn("Safe Trigger Count", body)
        self.assertIn("Last Live Heartbeat", body)
        self.assertIn("Last Safe Heartbeat", body)
        
        # Verify Smart Insight Panel shift to row 55
        self.assertIn("airoSprint6WriteRows_(dashboard, 55, 1, insightRows)", body)
        self.assertIn("dashboard.getRange('A55:G55').setFontWeight('bold')", body)
        self.assertNotIn("dashboard.getRange('A50:G50').setFontWeight('bold')", body)


if __name__ == "__main__":
    unittest.main()
