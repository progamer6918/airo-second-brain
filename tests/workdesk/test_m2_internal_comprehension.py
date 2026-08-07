import os
import unittest

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

class TestM2InternalComprehension(unittest.TestCase):

    def test_q01_ass_role_scope(self):
        path = os.path.join(repo_root, "wiki/workdesk/role/AREA_SALES_SUPERVISOR.md")
        content = open(path, 'r', encoding='utf-8').read()
        self.assertIn("business performance area", content)
        self.assertIn("Understand", content)

    def test_q02_market_share_down_investigation(self):
        path = os.path.join(repo_root, "wiki/workdesk/playbooks/MARKET_SHARE_DOWN.md")
        content = open(path, 'r', encoding='utf-8').read()
        self.assertIn("Validate denominator", content)

    def test_q03_nos_2023_vs_2026(self):
        path = os.path.join(repo_root, "wiki/workdesk/SOURCE_AUTHORITY.md")
        content = open(path, 'r', encoding='utf-8').read()
        self.assertIn("2026", content)

    def test_q04_activity_high_sales_low(self):
        path = os.path.join(repo_root, "wiki/workdesk/playbooks/HIGH_ACTIVITY_LOW_RESULT.md")
        content = open(path, 'r', encoding='utf-8').read()
        self.assertIn("funnel", content)

    def test_q05_people_vs_process_gap(self):
        path = os.path.join(repo_root, "wiki/workdesk/network/NOS_2026_CORE.md")
        content = open(path, 'r', encoding='utf-8').read()
        self.assertIn("People", content)
        self.assertIn("Process", content)

    def test_q06_bwi_external_role(self):
        path = os.path.join(repo_root, "wiki/workdesk/leadership/SUPERVISORY_LEADERSHIP.md")
        content = open(path, 'r', encoding='utf-8').read()
        self.assertIn("BWI", content)

    def test_q07_notion_transcript_treatment(self):
        path = os.path.join(repo_root, "wiki/workdesk/notes/PRESENTER_NOTES_POLICY.md")
        content = open(path, 'r', encoding='utf-8').read()
        self.assertIn("TRANSCRIPTION_RISK", content)

    def test_q08_nms_role(self):
        path = os.path.join(repo_root, "wiki/workdesk/systems/NMS.md")
        content = open(path, 'r', encoding='utf-8').read()
        self.assertIn("NMS", content)

    def test_q09_assdp_progression(self):
        path = os.path.join(repo_root, "wiki/workdesk/role/ASSDP_CAPABILITY_LADDER.md")
        content = open(path, 'r', encoding='utf-8').read()
        self.assertIn("Basic", content)
        self.assertIn("Intermediate", content)
        self.assertIn("Advanced", content)

    def test_q10_owner_applied_projects(self):
        path = os.path.join(repo_root, "wiki/workdesk/owner/OWNER_APPLIED_PROJECTS.md")
        content = open(path, 'r', encoding='utf-8').read()
        self.assertIn("DMAIC", content)

    def test_q11_presentation_task_loading(self):
        path = os.path.join(repo_root, "wiki/workdesk/TASK_ROUTER.md")
        content = open(path, 'r', encoding='utf-8').read()
        self.assertIn("presentation/AHM_REVIEW_AND_PRESENTATION", content)

    def test_q12_dealer_diagnosis_loading(self):
        path = os.path.join(repo_root, "wiki/workdesk/TASK_ROUTER.md")
        content = open(path, 'r', encoding='utf-8').read()
        self.assertIn("playbooks/DEALER_REVIEW", content)

if __name__ == '__main__':
    unittest.main()
