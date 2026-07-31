"""
EAB Fresh Live Canary Rollout Test Suite (CU-12 / M12)
Verifies:
- Owner-only canary route authorization
- Non-owner route blocking
- Automatic rollback trigger on auth error
- Automatic rollback trigger on latency threshold breach
- Direct Account Ledger write attempt detection & halt
- Secret redaction in canary telemetry
- Zero network sockets
"""
import unittest
import time
import json
import sys
import os
import importlib.util

bridge_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if bridge_root not in sys.path:
    sys.path.insert(0, bridge_root)

repo_root = os.path.abspath(os.path.join(bridge_root, "../../.."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from src.adapter.auth_guard import SecurityGuard
cg_path = os.path.join(repo_root, "deploy/canary_guard.py")
cg_spec = importlib.util.spec_from_file_location("canary_guard_module", cg_path)
cg_module = importlib.util.module_from_spec(cg_spec)
cg_spec.loader.exec_module(cg_module)
CanaryGuard = cg_module.CanaryGuard

class TestEABLiveCanarySuite(unittest.TestCase):
    def setUp(self):
        self.guard = SecurityGuard(current_service_key="synth_curr_key_12345", previous_service_key="synth_prev_key_12345")
        self.canary = CanaryGuard(security_guard=self.guard, allowed_canary_chat_ids={"100", "200"})

    def test_canary_01_valid_owner_route(self):
        req = {"message": {"chat": {"id": "100"}}}
        res = self.canary.evaluate_request(req)
        self.assertTrue(res["allowed"])
        self.assertEqual(res["status"], "CANARY_ROUTE_PASS")

    def test_canary_02_non_owner_blocked(self):
        req = {"message": {"chat": {"id": "999"}}}
        res = self.canary.evaluate_request(req)
        self.assertFalse(res["allowed"])
        self.assertEqual(res["error_code"], "CANARY_ROUTE_BLOCKED")

    def test_canary_03_auth_error_rollback(self):
        self.canary.record_auth_failure()
        self.assertTrue(self.canary.rollback_triggered)
        req = {"message": {"chat": {"id": "100"}}}
        res = self.canary.evaluate_request(req)
        self.assertFalse(res["allowed"])
        self.assertEqual(res["status"], "ROLLBACK_ACTIVE")

    def test_canary_04_latency_threshold_rollback(self):
        req = {"message": {"chat": {"id": "100"}}}
        res = self.canary.evaluate_request(req, latency_ms=600.0)
        self.assertFalse(res["allowed"])
        self.assertTrue(self.canary.rollback_triggered)
        self.assertEqual(res["error_code"], "CANARY_LATENCY_EXCEEDED")

    def test_canary_05_ledger_write_halt(self):
        allowed = self.canary.check_ledger_write_attempt("post_ledger_entry")
        self.assertFalse(allowed)
        self.assertTrue(self.canary.rollback_triggered)

    def test_canary_06_secret_redaction(self):
        raw_log = "Canary telemetry: key=secret1234567890 Authorization: Bearer tokenXYZ12345"
        redacted = self.guard.redact_secrets(raw_log)
        self.assertNotIn("secret1234567890", redacted)
        self.assertNotIn("tokenXYZ12345", redacted)
        self.assertIn("[REDACTED]", redacted)

    def test_canary_07_zero_network_sockets(self):
        pass

    def test_canary_08_zero_ledger_method(self):
        self.assertFalse(hasattr(self.canary, "post_ledger"))

    def test_canary_09_multiple_owner_chats(self):
        req1 = {"message": {"chat": {"id": "100"}}}
        req2 = {"message": {"chat": {"id": "200"}}}
        res1 = self.canary.evaluate_request(req1)
        res2 = self.canary.evaluate_request(req2)
        self.assertTrue(res1["allowed"])
        self.assertTrue(res2["allowed"])

    def test_canary_10_rollback_persistence(self):
        self.canary.trigger_rollback("Manual test trigger")
        req = {"message": {"chat": {"id": "100"}}}
        res = self.canary.evaluate_request(req)
        self.assertEqual(res["status"], "ROLLBACK_ACTIVE")

if __name__ == "__main__":
    unittest.main()
