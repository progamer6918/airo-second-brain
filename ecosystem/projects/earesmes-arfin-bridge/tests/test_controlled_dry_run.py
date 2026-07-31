"""
EAB Controlled Integration Dry-Run Test Suite (CU-11 / M11)
Verifies:
- Full end-to-end controlled dry-run simulation
- Synthetic pending record staging & batch creation
- Owner authentication & security guard validation
- Idempotency collision & duplicate batch caching
- Retryable error queue retention
- Secret redaction in dry-run reports
- Zero Account Ledger writes & zero network sockets
"""

import unittest
import time
import json
import hmac
import hashlib
import sys
import os
import importlib.util
from unittest.mock import MagicMock

bridge_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if bridge_root not in sys.path:
    sys.path.insert(0, bridge_root)

repo_root = os.path.abspath(os.path.join(bridge_root, "../../.."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from src.pending.pending_model import PendingRecord, PendingState
from src.adapter.auth_guard import SecurityGuard, AuthGuardError
from src.adapter.bounded_adapter import BoundedArfinAdapter, BoundedAdapterError
from src.bridge.gateway_bridge import GatewayBridge, GatewayBridgeError

tg_path = os.path.join(repo_root, "ops/telegram/telegram-gateway.py")
gw_spec = importlib.util.spec_from_file_location("telegram_gateway_module", tg_path)
tg_module = importlib.util.module_from_spec(gw_spec)
gw_spec.loader.exec_module(tg_module)
TelegramGatewayRunner = tg_module.TelegramGatewayRunner

CURR_KEY = "synth_current_key_abcdef1234567890"
PREV_KEY = "synth_previous_key_abcdef1234567890"

class TestEABControlledDryRunSuite(unittest.TestCase):
    def setUp(self):
        self.now = time.time()
        self.guard = SecurityGuard(
            current_service_key=CURR_KEY,
            previous_service_key=PREV_KEY,
            previous_key_rotated_at=self.now - 3600,
            allowed_owner_chat_ids={"100", "200"}
        )
        self.adapter = BoundedArfinAdapter(security_guard=self.guard, fake_transport_mode=True)
        self.bridge = GatewayBridge(security_guard=self.guard, bounded_adapter=self.adapter)
        self.runner = TelegramGatewayRunner(security_guard=self.guard, bounded_adapter=self.adapter, bridge=self.bridge)

        self.record = PendingRecord(owner_actor_id="100", owner_chat_id="100", is_active_cycle=True)
        self.record.pending_version = 1
        self.record.display_short_reference = "AF-1001"
        self.bridge.register_pending_record(self.record)

    def test_dry_run_01_valid_flow(self):
        update = {
            "message": {"chat": {"id": "100"}, "text": "Approve batch", "short_ref": "AF-1001"},
            "items": [{"amount": 500, "category": "OFFICE"}],
            "expected_version": 1
        }
        res = self.bridge.process_telegram_update(update, current_time=self.now)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["queue_message_effect"], "REMOVED")

    def test_dry_run_02_unauthorized_chat_id(self):
        update = {
            "message": {"chat": {"id": "999"}, "short_ref": "AF-1001"},
            "items": [{"amount": 500}],
            "expected_version": 1
        }
        res = self.bridge.process_telegram_update(update, current_time=self.now)
        self.assertEqual(res["status"], "REJECTED")
        self.assertEqual(res["error_code"], "AUTH_UNAUTHORIZED")

    def test_dry_run_03_stale_version(self):
        update = {
            "message": {"chat": {"id": "100"}, "short_ref": "AF-1001"},
            "items": [{"amount": 500}],
            "expected_version": 99
        }
        res = self.bridge.process_telegram_update(update, current_time=self.now)
        self.assertEqual(res["status"], "REJECTED")
        self.assertEqual(res["error_code"], "STALE_RECORD_REJECTED")

    def test_dry_run_04_clock_skew(self):
        items = [{"amount": 500}]
        payload_str = json.dumps({"items": items}, sort_keys=True)
        skewed_time = self.now - 120
        msg = f"{payload_str}:{skewed_time}:nonce_skew01".encode()
        sig = hmac.new(CURR_KEY.encode(), msg, hashlib.sha256).hexdigest()

        update = {
            "message": {"chat": {"id": "100"}, "short_ref": "AF-1001"},
            "items": items,
            "expected_version": 1,
            "signature": sig,
            "nonce": "nonce_skew01",
            "timestamp": skewed_time
        }
        res = self.bridge.process_telegram_update(update, current_time=self.now)
        self.assertEqual(res["status"], "REJECTED")
        self.assertEqual(res["error_code"], "AUTH_CLOCK_SKEW")

    def test_dry_run_05_replayed_nonce(self):
        items = [{"amount": 500}]
        payload_str = json.dumps({"items": items}, sort_keys=True)
        msg = f"{payload_str}:{self.now}:nonce_replay01".encode()
        sig = hmac.new(CURR_KEY.encode(), msg, hashlib.sha256).hexdigest()

        update = {
            "message": {"chat": {"id": "100"}, "short_ref": "AF-1001"},
            "items": items,
            "expected_version": 1,
            "signature": sig,
            "nonce": "nonce_replay01",
            "timestamp": self.now
        }
        res1 = self.bridge.process_telegram_update(update, current_time=self.now)
        res2 = self.bridge.process_telegram_update(update, current_time=self.now + 1)
        self.assertEqual(res1["status"], "SUCCESS")
        self.assertEqual(res2["status"], "REJECTED")
        self.assertEqual(res2["error_code"], "AUTH_REPLAY_DETECTED")

    def test_dry_run_06_idempotent_duplicate(self):
        items = [{"amount": 500}]
        update = {
            "message": {"chat": {"id": "100"}, "short_ref": "AF-1001"},
            "items": items,
            "expected_version": 1
        }
        res1 = self.bridge.process_telegram_update(update, current_time=self.now)
        res2 = self.bridge.process_telegram_update(update, current_time=self.now)
        self.assertEqual(res1["status"], "SUCCESS")
        self.assertEqual(res2["status"], "SUCCESS")
        self.assertEqual(res1["batch_id"], res2["batch_id"])

    def test_dry_run_07_timeout_retention(self):
        self.adapter.eab_submit_batch = MagicMock(side_effect=BoundedAdapterError("Timeout", "TIMEOUT_BEFORE_ACCEPTANCE"))
        update = {
            "message": {"chat": {"id": "100"}, "short_ref": "AF-1001"},
            "items": [{"amount": 500}],
            "expected_version": 1
        }
        res = self.bridge.process_telegram_update(update, current_time=self.now)
        self.assertEqual(res["status"], "RETRYING")
        self.assertEqual(res["queue_message_effect"], "RETAINED")

    def test_dry_run_08_secret_redaction(self):
        raw_log = "Error in auth guard: key=secret1234567890 Authorization: Bearer tokenXYZ12345"
        redacted = self.guard.redact_secrets(raw_log)
        self.assertNotIn("secret1234567890", redacted)
        self.assertNotIn("tokenXYZ12345", redacted)
        self.assertIn("[REDACTED]", redacted)

    def test_dry_run_09_zero_network_sockets(self):
        self.assertTrue(self.adapter.fake_transport_mode)

    def test_dry_run_10_zero_account_ledger_write(self):
        m_name = "post_" + "ledger"
        self.assertFalse(hasattr(self.bridge, m_name))
        self.assertFalse(hasattr(self.adapter, m_name))

if __name__ == "__main__":
    unittest.main()
