import os
import unittest
import csv

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

class TestM5HumanTransferabilitySignoff(unittest.TestCase):

    def test_01_human_test_script_exists(self):
        """The test script for human testers exists and is ready."""
        path = os.path.join(repo_root, "tests/workdesk/HUMAN_TEST_SCRIPT.md")
        self.assertTrue(os.path.exists(path), "Human test script missing")

    def test_02_no_fabricated_receipt(self):
        """
        The AI-proxy fabricated receipt must NOT exist.
        ZERO_CONTEXT_HUMAN_ACCEPTANCE=PASS is only valid after a real human test.
        """
        path = os.path.join(repo_root, "evidence/workdesk/HUMAN_USABILITY_TEST_RECEIPT.tsv")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            # If receipt exists, it must have SOURCE=ACTUAL_HUMAN to be valid
            self.assertIn("SOURCE=ACTUAL_HUMAN", content,
                "Human test receipt exists but missing SOURCE=ACTUAL_HUMAN — AI proxy results not acceptable")

    def test_03_current_md_honest_state(self):
        """CURRENT.md must not claim FULLY_DIGESTED_AND_TRANSFERABLE=YES before human test."""
        path = os.path.join(repo_root, "wiki/workdesk/CURRENT.md")
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Either NOT_YET or evidence that human test was run
        if "FULLY_DIGESTED_AND_TRANSFERABLE=YES" in content:
            self.assertIn("ZERO_CONTEXT_HUMAN_ACCEPTANCE=PASS", content,
                "Cannot claim FULLY_DIGESTED_AND_TRANSFERABLE=YES without ZERO_CONTEXT_HUMAN_ACCEPTANCE=PASS")

    def test_04_knowledge_health_honest_state(self):
        """KNOWLEDGE_HEALTH.md must not claim YES before human test is done."""
        path = os.path.join(repo_root, "wiki/workdesk/KNOWLEDGE_HEALTH.md")
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if "FULLY_DIGESTED_AND_TRANSFERABLE=YES" in content:
            self.assertIn("ZERO_CONTEXT_HUMAN_ACCEPTANCE=PASS", content,
                "Cannot claim FULLY_DIGESTED_AND_TRANSFERABLE=YES without ZERO_CONTEXT_HUMAN_ACCEPTANCE=PASS")

if __name__ == '__main__':
    unittest.main()
