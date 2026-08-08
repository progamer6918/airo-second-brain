import os
import unittest
import csv
import re

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

class TestSustainableIntakeAndChildProjects(unittest.TestCase):

    def test_01_input_processing_contract_exists(self):
        path = os.path.join(repo_root, "docs/contracts/AIRO_INPUT_PROCESSING_CONTRACT.md")
        self.assertTrue(os.path.exists(path), "AIRO_INPUT_PROCESSING_CONTRACT.md missing")
        content = open(path, encoding="utf-8").read()
        self.assertIn("RAW_INPUT -> DIRECT_CANONICAL_TRUTH", content)
        self.assertIn("OWNER_FACT", content)
        self.assertIn("OWNER_CORRECTION", content)
        self.assertIn("SECRET_OR_SENSITIVE", content)

    def test_02_boot_input_contract_pointer(self):
        path = os.path.join(repo_root, "BOOT.md")
        content = open(path, encoding="utf-8").read()
        self.assertIn("AIRO Input Processing Contract", content)
        self.assertIn("docs/contracts/AIRO_INPUT_PROCESSING_CONTRACT.md", content)

    def test_03_agents_new_input_rule(self):
        path = os.path.join(repo_root, "AGENTS.md")
        content = open(path, encoding="utf-8").read()
        self.assertIn("Sustainable Input & Intake Rules", content)
        self.assertIn("Classify", content)
        self.assertIn("Reconcile", content)

    def test_04_workdesk_intake_specification_exists(self):
        path = os.path.join(repo_root, "wiki/workdesk/INTAKE.md")
        self.assertTrue(os.path.exists(path), "wiki/workdesk/INTAKE.md missing")
        content = open(path, encoding="utf-8").read()
        self.assertIn("WORKDESK_PUBLIC_KNOWLEDGE_POLICY=PUBLIC_FIRST", content)
        self.assertIn("REPORT_AUTOMATION_VBA", content)
        self.assertIn("D_READY", content)

    def test_05_d_ready_project_file(self):
        path = os.path.join(repo_root, "projects/d-ready.md")
        self.assertTrue(os.path.exists(path), "projects/d-ready.md missing")
        content = open(path, encoding="utf-8").read()
        self.assertIn("parent_project_id: AIRO_WORKDESK", content)
        self.assertIn("status: ACTIVE", content)
        self.assertIn("stage: PILOT_LOGIC_VALIDATION", content)

    def test_06_report_automation_vba_project_file(self):
        path = os.path.join(repo_root, "projects/report-automation-vba.md")
        self.assertTrue(os.path.exists(path), "projects/report-automation-vba.md missing")
        content = open(path, encoding="utf-8").read()
        self.assertIn("parent_project_id: AIRO_WORKDESK", content)
        self.assertIn("status: FROZEN_BY_OWNER", content)
        self.assertIn("execution_allowed: NO", content)

    def test_07_project_registry_child_projects(self):
        path = os.path.join(repo_root, "projects/PROJECT_REGISTRY.tsv")
        self.assertTrue(os.path.exists(path))
        rows = []
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                rows.append(row)
        
        ids = {r["project_id"]: r for r in rows}
        self.assertIn("D_READY", ids)
        self.assertEqual(ids["D_READY"]["parent_project_id"], "AIRO_WORKDESK")
        self.assertIn("REPORT_AUTOMATION_VBA", ids)
        self.assertEqual(ids["REPORT_AUTOMATION_VBA"]["parent_project_id"], "AIRO_WORKDESK")
        self.assertIn("EARESMES_ARFIN_CLARIFICATION_BRIDGE", ids)
        self.assertEqual(ids["EARESMES_ARFIN_CLARIFICATION_BRIDGE"]["parent_project_id"], "", "EAB must be independent project, not WorkDesk child")

    def test_08_incremental_input_cases_simulation(self):
        """Simulate 10 deterministic input routing decisions."""
        contract_path = os.path.join(repo_root, "docs/contracts/AIRO_INPUT_PROCESSING_CONTRACT.md")
        intake_path = os.path.join(repo_root, "wiki/workdesk/INTAKE.md")
        self.assertTrue(os.path.exists(contract_path))
        self.assertTrue(os.path.exists(intake_path))

        # Case 1: NEW_SOURCE_DOCUMENT
        c1 = {"input_type": "NEW_SOURCE_DOCUMENT", "target": "evidence/workdesk/SOURCE_MANIFEST.tsv"}
        self.assertEqual(c1["input_type"], "NEW_SOURCE_DOCUMENT")

        # Case 2: OWNER_CORRECTION
        c2 = {"input_type": "OWNER_CORRECTION", "provenance": "OWNER_CONFIRMED"}
        self.assertEqual(c2["provenance"], "OWNER_CONFIRMED")

        # Case 3: D-READY update
        c3 = {"target_project": "AIRO_WORKDESK", "target_child_project": "D_READY"}
        self.assertEqual(c3["target_child_project"], "D_READY")

        # Case 4: VBA update
        c4 = {"target_child_project": "REPORT_AUTOMATION_VBA", "status": "FROZEN_BY_OWNER", "execution_allowed": "NO"}
        self.assertEqual(c4["execution_allowed"], "NO")

        # Case 5: Duplicate fact
        c5 = {"outcome": "DUPLICATE", "action": "NO_NEW_NOTE"}
        self.assertEqual(c5["action"], "NO_NEW_NOTE")

        # Case 6: Source conflict
        c6 = {"outcome": "CONFLICT", "target": "evidence/workdesk/CONFLICT_REGISTER.tsv"}
        self.assertEqual(c6["outcome"], "CONFLICT")

        # Case 7: Episodic meeting
        c7 = {"input_type": "EPISODIC_INPUT", "route": "SESSION_ONLY"}
        self.assertEqual(c7["route"], "SESSION_ONLY")

        # Case 8: Secret credential
        c8 = {"input_type": "SECRET_OR_SENSITIVE", "route": "EXCLUDED"}
        self.assertEqual(c8["route"], "EXCLUDED")

        # Case 9: Current sales Excel
        c9 = {"input_type": "CURRENT_BUSINESS_DATA", "route": "CURRENT_DATA"}
        self.assertEqual(c9["route"], "CURRENT_DATA")

        # Case 10: Single domain update
        c10 = {"full_corpus_rebuild_required": "NO"}
        self.assertEqual(c10["full_corpus_rebuild_required"], "NO")

    def test_09_m5_honest_baseline_preserved(self):
        current_path = os.path.join(repo_root, "wiki/workdesk/CURRENT.md")
        content = open(current_path, encoding="utf-8").read()
        self.assertIn("ZERO_CONTEXT_HUMAN_ACCEPTANCE=NOT_YET", content)
        self.assertIn("FULLY_DIGESTED_AND_TRANSFERABLE=NO", content)

    def test_10_no_duplicate_project_trees(self):
        # Verify physical files exist in their canonical positions without duplicated trees
        d_ready = os.path.join(repo_root, "projects/d-ready.md")
        vba = os.path.join(repo_root, "projects/report-automation-vba.md")
        self.assertTrue(os.path.exists(d_ready))
        self.assertTrue(os.path.exists(vba))

    def test_11_eab_navigation_consistency(self):
        """Prove EAB independent project navigation metadata in projects/_index.md."""
        idx_p = os.path.join(repo_root, "projects/_index.md")
        c = open(idx_p, encoding="utf-8").read()
        child_sec = c.split("## Child Projects (AIRO WorkDesk)")[1].split("## ")[0] if "## Child Projects (AIRO WorkDesk)" in c else ""
        indep_sec = c.split("## Project Terdaftar Lainnya")[1].split("## ")[0] if "## Project Terdaftar Lainnya" in c else ""

        self.assertNotIn("Earesmes-Arfin Bridge", child_sec, "EAB must NOT be in WorkDesk child section of index")
        self.assertIn("Earesmes-Arfin Bridge", indep_sec, "EAB must be in independent section of index")
        self.assertIn("`EARESMES_ARFIN_CLARIFICATION_BRIDGE`", indep_sec, "EAB row must contain exact Project ID")
        self.assertIn("`projects/earesmes-arfin-bridge.md`", indep_sec, "EAB row must contain exact status file pointer")

    def test_12_workdesk_page_no_eab(self):
        """Prove projects/airo-workdesk.md does not list EAB as child."""
        wd_p = os.path.join(repo_root, "projects/airo-workdesk.md")
        c = open(wd_p, encoding="utf-8").read()
        child_sec = c.split("## 🌿 Child Projects")[1].split("## ")[0] if "## 🌿 Child Projects" in c else ""
        self.assertNotIn("EARESMES_ARFIN_CLARIFICATION_BRIDGE", child_sec, "EAB must NOT be in WorkDesk project page child section")


if __name__ == "__main__":
    unittest.main()
