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

    def test_case_1_simple_question_no_discovery(self):
        result = self.run_gate(["--intent-type", "simple_question", "--format", "json"])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertFalse(data["discovery_required"])
        self.assertEqual(data["discovery_status"], "SKIPPED")
        self.assertEqual(data["validation"], "PASS")

    def test_case_2_bug_investigation_no_discovery(self):
        result = self.run_gate(["--intent-type", "bug_investigation", "--format", "json"])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertFalse(data["discovery_required"])
        self.assertEqual(data["discovery_status"], "SKIPPED")
        self.assertEqual(data["validation"], "PASS")

    def test_case_3_small_change_no_discovery(self):
        result = self.run_gate(["--intent-type", "small_change", "--format", "json"])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertFalse(data["discovery_required"])
        self.assertEqual(data["discovery_status"], "SKIPPED")
        self.assertEqual(data["validation"], "PASS")

    def test_case_4_new_capability_discovery_required(self):
        result = self.run_gate(["--intent-type", "new_capability", "--format", "json"])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertTrue(data["discovery_required"])
        self.assertEqual(data["discovery_status"], "REQUIRED")

    def test_discovery_payload_validation(self):
        # Missing fields should fail
        incomplete_payload = json.dumps({"problem": "Need regional weather"})
        res_fail = self.run_gate(["--intent-type", "new_capability", "--payload-json", incomplete_payload, "--format", "json"])
        self.assertEqual(res_fail.returncode, 1)
        data_fail = json.loads(res_fail.stdout)
        self.assertEqual(data_fail["validation"], "FAIL")
        self.assertIn("primary_user", data_fail["missing_fields"])

        # Complete 5-point fields should pass
        complete_payload = json.dumps({
            "problem": "Need regional weather",
            "primary_user": "Hermes",
            "current_workflow": "Manual query",
            "desired_outcome": "Automated regional weather adapter",
            "constraints": "Stateless, no background daemon"
        })
        res_pass = self.run_gate(["--intent-type", "new_capability", "--payload-json", complete_payload, "--format", "json"])
        self.assertEqual(res_pass.returncode, 0)
        data_pass = json.loads(res_pass.stdout)
        self.assertEqual(data_pass["validation"], "PASS")

    def test_tech_spec_threshold_rules(self):
        # Simple change: no tech spec
        res1 = self.run_gate(["--intent-type", "small_change", "--format", "json"])
        data1 = json.loads(res1.stdout)
        self.assertFalse(data1["technical_spec_required"])

        # Multi-subsystem impact: tech spec required
        res2 = self.run_gate(["--intent-type", "new_capability", "--multiple-subsystems", "--format", "json"])
        data2 = json.loads(res2.stdout)
        self.assertTrue(data2["technical_spec_required"])

        # Boundary change: tech spec required
        res3 = self.run_gate(["--intent-type", "new_capability", "--boundary-change", "--format", "json"])
        data3 = json.loads(res3.stdout)
        self.assertTrue(data3["technical_spec_required"])

        # External integration change: tech spec required
        res4 = self.run_gate(["--intent-type", "new_capability", "--external-integration", "--format", "json"])
        data4 = json.loads(res4.stdout)
        self.assertTrue(data4["technical_spec_required"])

    def test_contract_file_conformance(self):
        contract_path = ROOT / "docs/contracts/AIRO_CAPABILITY_DISCOVERY_GATE_CONTRACT.md"
        self.assertTrue(contract_path.exists(), "Contract file must exist")
        content = contract_path.read_text(encoding="utf-8")

        # Verify mandatory 5 fields
        self.assertIn("1. **Problem:**", content)
        self.assertIn("2. **Primary User:**", content)
        self.assertIn("3. **Current Workflow:**", content)
        self.assertIn("4. **Desired Outcome:**", content)
        self.assertIn("5. **Constraints:**", content)

        # Verify gating rules
        self.assertIn("When Discovery is Required", content)
        self.assertIn("When Discovery is Skipped", content)
        self.assertIn("Simple Questions", content)
        self.assertIn("Bug Investigations", content)
        self.assertIn("Small Changes", content)

        # Verify technical spec rules
        self.assertIn("Technical Specification Threshold Rule", content)
        self.assertIn("Multiple Subsystem Impact", content)
        self.assertIn("Architecture Boundary Changes", content)
        self.assertIn("External Integration Changes", content)

        # Verify anti-bloat guardrails
        self.assertIn("NO New Framework", content)
        self.assertIn("NO BMAD Fork", content)
        self.assertIn("NO OpenSpec / Spec Kit", content)
        self.assertIn("NO Parallel PRD System", content)
        self.assertIn("NO Duplicate Authority", content)


if __name__ == "__main__":
    unittest.main()
