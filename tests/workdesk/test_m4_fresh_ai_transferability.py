import os
import unittest

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

class TestM4FreshAITransferability(unittest.TestCase):

    def test_q01_fresh_ai_ass_role(self):
        path = os.path.join(repo_root, "wiki/workdesk/role/AREA_SALES_SUPERVISOR.md")
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        self.assertIn("business performance area", c)
        self.assertIn("Operating Cycle", c)

    def test_q02_fresh_ai_market_share_down_diagnosis(self):
        path = os.path.join(repo_root, "wiki/workdesk/playbooks/MARKET_SHARE_DOWN.md")
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        self.assertIn("Validate denominator", c)
        self.assertIn("competitor movement", c)

    def test_q03_fresh_ai_nos_authority_supersession(self):
        path = os.path.join(repo_root, "wiki/workdesk/SOURCE_AUTHORITY.md")
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        self.assertIn("2026 checklist", c)

    def test_q04_fresh_ai_high_activity_low_result(self):
        path = os.path.join(repo_root, "wiki/workdesk/playbooks/HIGH_ACTIVITY_LOW_RESULT.md")
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        self.assertIn("funnel", c)

    def test_q05_fresh_ai_productivity_manpower(self):
        path = os.path.join(repo_root, "wiki/workdesk/business/SALES_FORCE_PRODUCTIVITY.md")
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        self.assertIn("sales force", c)

    def test_q06_fresh_ai_bwi_external_leadership(self):
        path = os.path.join(repo_root, "wiki/workdesk/leadership/SUPERVISORY_LEADERSHIP.md")
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        self.assertIn("BWI", c)

    def test_q07_fresh_ai_notion_authority_policy(self):
        path = os.path.join(repo_root, "wiki/workdesk/notes/PRESENTER_NOTES_POLICY.md")
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        self.assertIn("TRANSCRIPTION_RISK", c)

    def test_q08_fresh_ai_nms_system_integration(self):
        path = os.path.join(repo_root, "wiki/workdesk/systems/NMS.md")
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        self.assertIn("NMS", c)

    def test_q09_fresh_ai_assdp_capability_progression(self):
        path = os.path.join(repo_root, "wiki/workdesk/role/ASSDP_CAPABILITY_LADDER.md")
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        self.assertIn("Basic", c)
        self.assertIn("Advanced", c)

    def test_q10_fresh_ai_owner_applied_projects(self):
        path = os.path.join(repo_root, "wiki/workdesk/owner/OWNER_APPLIED_PROJECTS.md")
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        self.assertIn("DMAIC", c)

    def test_case_a_dealer_diagnosis_blueprint(self):
        path = os.path.join(repo_root, "wiki/workdesk/playbooks/DIAGNOSE_BUSINESS_PROBLEM.md")
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        self.assertIn("Alur Diagnosis Standard", c)

    def test_case_b_build_dealer_review_blueprint(self):
        path = os.path.join(repo_root, "wiki/workdesk/deliverables/DEALER_REVIEW.md")
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        self.assertIn("Quality Gate", c)

    def test_case_c_market_brief_blueprint(self):
        path = os.path.join(repo_root, "wiki/workdesk/deliverables/MARKET_BRIEF.md")
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        self.assertIn("Market & Area Intelligence Brief", c)

    def test_case_d_management_presentation_blueprint(self):
        path = os.path.join(repo_root, "wiki/workdesk/deliverables/MANAGEMENT_REVIEW.md")
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        self.assertIn("9 Slide", c)

    def test_case_e_nos_mandatory_gating(self):
        path = os.path.join(repo_root, "wiki/workdesk/network/NOS_2026_CORE.md")
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        self.assertIn("NOS", c)

    def test_provenance_drilldown(self):
        path = os.path.join(repo_root, "wiki/workdesk/KNOWLEDGE_HEALTH.md")
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        self.assertIn("Atomic evidence claims in ledger", c)

    def test_unknown_ambiguity_handling(self):
        path = os.path.join(repo_root, "wiki/workdesk/BOOT.md")
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        self.assertIn("Source guard", c)

if __name__ == '__main__':
    unittest.main()
