from pathlib import Path
import subprocess
import unittest
import json

ROOT = Path(__file__).resolve().parents[2]


class ProductBuildWorkflowTest(unittest.TestCase):
    def run_workflow(self, args: list[str]):
        script = ROOT / "scripts/airo-product-build-workflow"
        cmd = [str(script)] + args
        result = subprocess.run(
            cmd,
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        return result

    def test_case_1_simple_question_no_interview(self):
        result = self.run_workflow(["--intent", "simple_question", "--format", "json"])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["intent"], "SIMPLE_QUESTION")
        self.assertEqual(data["route"], "DIRECT_ANSWER")
        self.assertFalse(data["interview_required"])
        self.assertFalse(data["capability_artifact_required"])
        self.assertFalse(data["technical_design_required"])
        self.assertFalse(data["council_required"])

    def test_case_2_bug_investigation_no_capability_artifact(self):
        result = self.run_workflow(["--intent", "bug_investigation", "--format", "json"])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["intent"], "BUG_INVESTIGATION")
        self.assertEqual(data["route"], "DIAGNOSTIC_FIX")
        self.assertFalse(data["capability_artifact_required"])
        self.assertFalse(data["interview_required"])
        self.assertFalse(data["prd_required"])

    def test_case_3_small_ui_text_change_no_prd_no_technical_design(self):
        result = self.run_workflow(["--intent", "small_change", "--ui-text-change", "--format", "json"])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["intent"], "SMALL_CHANGE")
        self.assertEqual(data["route"], "DIRECT_EXECUTION")
        self.assertFalse(data["prd_required"])
        self.assertFalse(data["technical_design_required"])
        self.assertFalse(data["interview_required"])
        self.assertFalse(data["capability_artifact_required"])

    def test_case_4_new_capability_interview_and_capability_artifact_required(self):
        result = self.run_workflow(["--intent", "new_capability", "--format", "json"])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["intent"], "NEW_CAPABILITY")
        self.assertEqual(data["route"], "INTERVIEW_CAPABILITY")
        self.assertTrue(data["interview_required"])
        self.assertTrue(data["capability_artifact_required"])
        self.assertTrue(data["prd_required"])

    def test_case_5_ui_heavy_capability_design_context_available(self):
        result = self.run_workflow(["--intent", "new_capability", "--ui-heavy", "--format", "json"])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertTrue(data["design_context_available"])

    def test_case_6_architecture_decision_council_trigger_available(self):
        result = self.run_workflow(["--intent", "architecture_decision", "--format", "json"])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["intent"], "HIGH_IMPACT_DECISION")
        self.assertEqual(data["route"], "COUNCIL_DELIBERATION")
        self.assertTrue(data["council_trigger_available"])
        self.assertTrue(data["council_required"])

    def test_case_7_unknown_information_not_assumption(self):
        # When information is unknown, UNKNOWN must be accepted as valid and not flagged as missing/error
        interview_payload = json.dumps({
            "interview": {
                # Problem Discovery
                "problem": "Provide multi-device sync",
                "current_pain": "Files are local to one machine",
                "expected_improvement": "Seamless cross-device access",
                # Product Discovery
                "primary_user": "Owner",
                "desired_outcome": "Automated sync daemon",
                "scope": "ASB repository",
                "non_scope": "Third party servers",
                # Constraint Discovery
                "business_constraint": "Zero cloud leak",
                "technical_constraint": "UNKNOWN",  # Explicit UNKNOWN
                "resource_constraint": "UNKNOWN",   # Explicit UNKNOWN
            }
        })
        result = self.run_workflow(["--intent", "new_capability", "--payload-json", interview_payload, "--format", "json"])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["validation"], "PASS")
        self.assertEqual(len(data["missing_fields"]), 0)

    def test_council_deliberation_epistemic_preservation(self):
        council_payload = json.dumps({
            "council_deliberation": {
                "fact": "WSL is running on local Windows machine",
                "inference": "Direct filesystem access is fastest via 9P / local paths",
                "assumption": "Owner will continue using Windows + WSL2 hybrid",
                "unknown": "Whether VPS deployment will host background queue",
            }
        })
        result = self.run_workflow(["--intent", "architecture_decision", "--payload-json", council_payload, "--format", "json"])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["validation"], "PASS")

    def test_design_context_tooling_boundary(self):
        # Valid Markdown / text design context
        valid_design = json.dumps({
            "design_context": {
                "user_flow": "1. User opens terminal -> 2. Enters query -> 3. Receives brief",
                "ui_impact": "CLI status and output banner",
                "interaction_notes": "Formatted as clean Markdown table",
                "prototype_required": "NO",
            }
        })
        res_valid = self.run_workflow(["--intent", "new_capability", "--ui-heavy", "--payload-json", valid_design, "--format", "json"])
        self.assertEqual(res_valid.returncode, 0)
        self.assertEqual(json.loads(res_valid.stdout)["validation"], "PASS")

        # Invalid external design tool (Penpot)
        invalid_design = json.dumps({
            "design_context": {
                "user_flow": "Follow Penpot prototype",
                "ui_impact": "Penpot workspace link",
                "interaction_notes": "See mockup",
                "prototype_required": "YES",
            }
        })
        res_invalid = self.run_workflow(["--intent", "new_capability", "--ui-heavy", "--payload-json", invalid_design, "--format", "json"])
        self.assertEqual(res_invalid.returncode, 1)
        self.assertIn("EXTERNAL_DESIGN_TOOL_FORBIDDEN", json.loads(res_invalid.stdout)["missing_fields"])

    def test_contract_conformance(self):
        contract_path = ROOT / "docs/contracts/AIRO_PRODUCT_BUILD_WORKFLOW_CONTRACT.md"
        self.assertTrue(contract_path.exists())
        content = contract_path.read_text(encoding="utf-8")

        # Target workflow
        self.assertIn("OWNER INTENT", content)
        self.assertIn("ADAPTIVE ROUTING", content)
        self.assertIn("Interview Protocol", content)
        self.assertIn("Council Deliberation", content)

        # 3 Interview categories
        self.assertIn("Problem Discovery", content)
        self.assertIn("Product Discovery", content)
        self.assertIn("Constraint Discovery", content)
        self.assertIn("Strict UNKNOWN Rule", content)

        # Technical Design gate
        self.assertIn("Technical Design Gate", content)
        self.assertIn("Multiple Subsystem Impact", content)
        self.assertIn("Architecture Boundary Change", content)
        self.assertIn("External Integration", content)
        self.assertIn("Major Data Model Change", content)

        # Council Integration & Epistemic preservation
        self.assertIn("Council Deliberation Integration", content)
        self.assertIn("FACT:", content)
        self.assertIn("INFERENCE:", content)
        self.assertIn("ASSUMPTION:", content)
        self.assertIn("UNKNOWN:", content)

        # Anti-framework guardrails
        self.assertIn("NO New Framework", content)
        self.assertIn("Do NOT install or fork BMAD", content)
        self.assertIn("NO Duplicate PRD System", content)


if __name__ == "__main__":
    unittest.main()
