import os
import unittest

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

class TestM3InternalOperational(unittest.TestCase):

    def test_01_playbooks_reachable(self):
        home_path = os.path.join(repo_root, "wiki/workdesk/HOME.md")
        with open(home_path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn("playbooks/MARKET_SHARE_DOWN", content)
        self.assertIn("playbooks/DEALER_REVIEW", content)

    def test_02_deliverable_blueprints_reachable(self):
        index_path = os.path.join(repo_root, "wiki/workdesk/DELIVERABLE_INDEX.md")
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn("deliverables/DEALER_REVIEW", content)
        self.assertIn("deliverables/PICA", content)
        self.assertIn("deliverables/BUSINESS_CASE", content)
        self.assertIn("deliverables/MANAGEMENT_REVIEW", content)

    def test_03_no_orphan_deliverables(self):
        deliv_files = ["DEALER_REVIEW.md", "PICA.md", "BUSINESS_CASE.md", "MARKET_BRIEF.md", "MANAGEMENT_REVIEW.md", "DATA_VALIDATION.md", "COMMUNICATION.md", "MEETING_PREP.md"]
        for df in deliv_files:
            path = os.path.join(repo_root, "wiki/workdesk/deliverables", df)
            self.assertTrue(os.path.exists(path), f"Blueprint {df} missing")

    def test_04_task_router_routes(self):
        router_path = os.path.join(repo_root, "wiki/workdesk/TASK_ROUTER.md")
        with open(router_path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn("deliverables/DEALER_REVIEW", content)
        self.assertIn("deliverables/MANAGEMENT_REVIEW", content)

    def test_05_home_routes_intents(self):
        home_path = os.path.join(repo_root, "wiki/workdesk/HOME.md")
        with open(home_path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn("DELIVERABLE_INDEX", content)

    def test_06_input_requirements_in_blueprints(self):
        path = os.path.join(repo_root, "wiki/workdesk/deliverables/DEALER_REVIEW.md")
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn("Input Requirements", content)
        self.assertIn("AUTO_RESOLVE_FIRST", content)

    def test_07_diagnosis_before_solution(self):
        path = os.path.join(repo_root, "wiki/workdesk/playbooks/DIAGNOSE_BUSINESS_PROBLEM.md")
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn("Alur Diagnosis Standard", content)

    def test_08_quality_gate_in_blueprints(self):
        path = os.path.join(repo_root, "wiki/workdesk/deliverables/DEALER_REVIEW.md")
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn("Quality Gate", content)

    def test_09_authority_preserved(self):
        path = os.path.join(repo_root, "wiki/workdesk/SOURCE_AUTHORITY.md")
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn("2026", content)

    def test_10_evidence_references(self):
        path = os.path.join(repo_root, "wiki/workdesk/deliverables/PICA.md")
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn("WD-SRC-020", content)

    def test_11_owner_input_contract(self):
        path = os.path.join(repo_root, "wiki/workdesk/deliverables/PICA.md")
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn("OWNER_REQUIRED", content)

    def test_12_no_secrets(self):
        path = os.path.join(repo_root, "wiki/workdesk/KNOWLEDGE_HEALTH.md")
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn("Secret notes excluded", content)

if __name__ == '__main__':
    unittest.main()
