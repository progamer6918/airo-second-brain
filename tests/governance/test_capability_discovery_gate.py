from pathlib import Path
import subprocess
import unittest
import json

ROOT = Path(__file__).resolve().parents[2]


class CapabilityDiscoveryGateTest(unittest.TestCase):
    def run_gate(self, args: list[str]):
        script = ROOT / "scripts/airo-capability-discovery-gate"
        cmd = [str(script)] + args
        result = subprocess.run(
            cmd,
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        return result

    def test_case_1_question_no_discovery(self):
        result = self.run_gate(["--intent-type", "question", "--format", "json"])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertFalse(data["discovery_required"])
        self.assertEqual(data["discovery_status"], "SKIPPED")
        self.assertEqual(data["validation"], "PASS")

    def test_case_2_bug_investigation_no_capability_artifact(self):
        result = self.run_gate(["--intent-type", "bug_investigation", "--format", "json"])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertFalse(data["capability_artifact_required"])
        self.assertFalse(data["discovery_required"])
        self.assertEqual(data["discovery_status"], "SKIPPED")
        self.assertEqual(data["validation"], "PASS")

    def test_case_3_small_change_no_technical_design(self):
        result = self.run_gate(["--intent-type", "small_change", "--format", "json"])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertFalse(data["technical_design_required"])
        self.assertFalse(data["discovery_required"])
        self.assertEqual(data["discovery_status"], "SKIPPED")
        self.assertEqual(data["validation"], "PASS")

    def test_case_4_new_capability_context_required(self):
        result = self.run_gate(["--intent-type", "new_capability", "--format", "json"])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertTrue(data["discovery_required"])
        self.assertTrue(data["capability_context_required"])
        self.assertTrue(data["capability_artifact_required"])
        self.assertEqual(data["discovery_status"], "REQUIRED")

    def test_case_5_multi_system_capability_technical_design_required(self):
        result = self.run_gate(["--intent-type", "new_capability", "--multiple-subsystems", "--format", "json"])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertTrue(data["technical_design_required"])

    def test_technical_design_triggers(self):
        # Boundary change triggers technical design
        res_b = self.run_gate(["--intent-type", "new_capability", "--boundary-change", "--format", "json"])
        self.assertTrue(json.loads(res_b.stdout)["technical_design_required"])

        # External integration triggers technical design
        res_e = self.run_gate(["--intent-type", "new_capability", "--external-integration", "--format", "json"])
        self.assertTrue(json.loads(res_e.stdout)["technical_design_required"])

        # Significant data model change triggers technical design
        res_d = self.run_gate(["--intent-type", "new_capability", "--data-model-change", "--format", "json"])
        self.assertTrue(json.loads(res_d.stdout)["technical_design_required"])

    def test_capability_context_payload_validation_with_unknowns(self):
        # Missing required field
        incomplete = json.dumps({"problem": "Automate reports"})
        res_fail = self.run_gate(["--intent-type", "new_capability", "--payload-json", incomplete, "--format", "json"])
        self.assertEqual(res_fail.returncode, 1)

        # Complete fields with UNKNOWN where clarification needed
        valid_with_unknown = json.dumps({
            "problem": "Automate reports",
            "primary_user": "Owner",
            "current_workflow": "Manual export",
            "desired_outcome": "Weekly summary receipt",
            "constraints": "UNKNOWN",
        })
        res_pass = self.run_gate(["--intent-type", "new_capability", "--payload-json", valid_with_unknown, "--format", "json"])
        self.assertEqual(res_pass.returncode, 0)
        self.assertEqual(json.loads(res_pass.stdout)["validation"], "PASS")

    def test_optional_design_context_validation(self):
        # Valid design context
        valid_design = json.dumps({
            "problem": "Add dashboard chart",
            "primary_user": "Owner",
            "current_workflow": "CLI query",
            "desired_outcome": "Interactive web chart",
            "constraints": "No external CDNs",
            "design_context": {
                "user_flow": "1. Open dashboard -> 2. View chart",
                "ui_impact": "Summary panel on index.html",
                "interaction_notes": "Hover shows tooltip with amount"
            }
        })
        res_pass = self.run_gate(["--intent-type", "new_capability", "--payload-json", valid_design, "--format", "json"])
        self.assertEqual(res_pass.returncode, 0)

        # Invalid external design tool rejection (Penpot)
        invalid_design = json.dumps({
            "problem": "Add dashboard chart",
            "primary_user": "Owner",
            "current_workflow": "CLI query",
            "desired_outcome": "Interactive web chart",
            "constraints": "No external CDNs",
            "design_context": {
                "user_flow": "1. Open dashboard",
                "ui_impact": "Penpot design board link",
                "interaction_notes": "Follow penpot mockup"
            }
        })
        res_tool_fail = self.run_gate(["--intent-type", "new_capability", "--payload-json", invalid_design, "--format", "json"])
        self.assertEqual(res_tool_fail.returncode, 1)
        self.assertIn("INVALID_EXTERNAL_DESIGN_TOOL_DETECTED", json.loads(res_tool_fail.stdout)["missing_fields"])

    def test_contract_file_conformance(self):
        contract_path = ROOT / "docs/contracts/AIRO_CAPABILITY_DISCOVERY_GATE_CONTRACT.md"
        self.assertTrue(contract_path.exists(), "Contract file must exist")
        content = contract_path.read_text(encoding="utf-8")

        # Verify target lifecycle
        self.assertIn("Capability Brief", content)
        self.assertIn("(Optional Technical Design)", content)

        # Verify Capability Context 5 fields
        self.assertIn("1. **Problem:**", content)
        self.assertIn("2. **Primary User:**", content)
        self.assertIn("3. **Current Workflow:**", content)
        self.assertIn("4. **Desired Outcome:**", content)
        self.assertIn("5. **Constraints:**", content)

        # Verify Acceptance criteria and UNKNOWN rule
        self.assertIn("Acceptance Criteria", content)
        self.assertIn("UNKNOWN", content)

        # Verify Design Context
        self.assertIn("Design Context", content)
        self.assertIn("User Flow", content)
        self.assertIn("UI Impact", content)
        self.assertIn("Interaction Notes", content)
        self.assertIn("Do NOT introduce Penpot", content)

        # Verify Technical Design Decision Gate
        self.assertIn("Technical Design Decision Gate", content)
        self.assertIn("Multiple Subsystem Impact", content)
        self.assertIn("Architecture Boundary Change", content)
        self.assertIn("External Integration", content)
        self.assertIn("Significant Data Model Change", content)
        self.assertIn("Simple local changes", content)
        self.assertIn("Isolated bug fixes", content)


if __name__ == "__main__":
    unittest.main()
