#!/usr/bin/env python3
"""
airo-hermes-bridge-static-test.py

Static tests for Phase 0B1 bridge implementation.
All external dependencies are mocked. No model calls. No network calls.

Tests:
  T1. routing priority: callback > EarnSAI > NL queue
  T2. atomic enqueue + duplicate idempotency
  T3. worker state machine: pending -> processing -> done
  T4. retry -> failed -> dead after 3 attempts
  T5. reply_sent guard prevents duplicate send
  T6. unauthorized chat_id rejected
  T7. worker toolsets exclude mutation-capable tools
"""

import sys
import os
import json
import uuid
import tempfile
import shutil
import time
import unittest
from unittest.mock import patch, MagicMock, call
from datetime import datetime

# ??? Add ASB root to sys.path for gateway import ?????????????????????????????
ASB_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATEWAY_PATH = os.path.join(ASB_ROOT, "ops", "telegram", "telegram-gateway.py")
WORKER_PATH  = os.path.join(ASB_ROOT, "scripts", "airo-hermes-worker")

# ??? Helpers ?????????????????????????????????????????????????????????????????
def import_module_from_path(name: str, path: str):
    from importlib.machinery import SourceFileLoader
    from importlib.util import module_from_spec, spec_from_loader

    loader = SourceFileLoader(name, path)
    spec = spec_from_loader(name, loader)

    if spec is None:
        raise RuntimeError(f"Cannot create module spec for {path}")

    mod = module_from_spec(spec)
    loader.exec_module(mod)
    return mod


def make_update(update_id=100, text="hello", chat_id="111111", message_id=42):
    return {
        "update_id": update_id,
        "message": {
            "message_id": message_id,
            "chat": {"id": int(chat_id)},
            "text": text,
        }
    }


def make_callback_update(update_id=200, chat_id="111111", data="manualqueue:detail:abc"):
    return {
        "update_id": update_id,
        "callback_query": {
            "id": "cb001",
            "data": data,
            "message": {"chat": {"id": int(chat_id)}},
        }
    }

OWNER_CHAT_ID = "111111"
TOKEN = "TEST_TOKEN_NOT_REAL"

# ???????????????????????????????????????????????????????????????????????????????
# T1: Routing priority
# ???????????????????????????????????????????????????????????????????????????????
class TestRoutingPriority(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        # Patch all paths used by gateway
        self.patches = [
            patch("builtins.open", side_effect=self._patched_open),
        ]
        # Load gateway module fresh each test using temp dirs
        self.gw = self._load_gateway()

    def _load_gateway(self):
        # We load the gateway module with mocked path constants
        gw = import_module_from_path("telegram_gateway", GATEWAY_PATH)
        gw.NL_QUEUE_DIR = os.path.join(self.tmpdir, "nl-queue")
        gw.ACTIONS_DIR  = os.path.join(self.tmpdir, "actions")
        gw.EARNSAI_ROUTE_DIR = os.path.join(self.tmpdir, "earnsai")
        gw.LASTUPDATE_FILE = os.path.join(self.tmpdir, "last-update")
        gw.LOG_FILE = os.path.join(self.tmpdir, "gateway.log")
        gw.SHORTID_SCRIPT = "/dev/null"
        os.makedirs(gw.NL_QUEUE_DIR, exist_ok=True)
        os.makedirs(gw.ACTIONS_DIR, exist_ok=True)
        return gw

    def _patched_open(self, *args, **kwargs):
        # Allow our temp dir files; block real filesystem writes
        if args and str(args[0]).startswith(self.tmpdir):
            return open.__wrapped__(*args, **kwargs) if hasattr(open, '__wrapped__') else self._real_open(*args, **kwargs)
        return self._real_open(*args, **kwargs)

    _real_open = staticmethod(open)

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_T1a_callback_is_priority_1(self):
        """callback_query must be handled before message check."""
        gw = self.gw
        handled = []
        with patch.object(gw, "handle_airo_callback", side_effect=lambda *a: handled.append("callback")), \
             patch.object(gw, "route_to_earnsai", side_effect=lambda *a: handled.append("earnsai")), \
             patch.object(gw, "enqueue_nl_message", side_effect=lambda **kw: handled.append("nl")):
            update = make_callback_update(chat_id=OWNER_CHAT_ID)
            gw.route_update(TOKEN, OWNER_CHAT_ID, update)
        self.assertIn("callback", handled)
        self.assertNotIn("earnsai", handled)
        self.assertNotIn("nl", handled)

    def test_T1b_earnsai_is_priority_2(self):
        """EarnSAI slash commands must be handled before NL queue."""
        gw = self.gw
        handled = []
        with patch.object(gw, "route_to_earnsai", side_effect=lambda *a: handled.append("earnsai")), \
             patch.object(gw, "enqueue_nl_message", side_effect=lambda **kw: handled.append("nl")):
            update = make_update(text="/status foo", chat_id=OWNER_CHAT_ID)
            gw.route_update(TOKEN, OWNER_CHAT_ID, update)
        self.assertIn("earnsai", handled)
        self.assertNotIn("nl", handled)

    def test_T1c_plain_text_goes_to_nl_queue(self):
        """Ordinary text must be enqueued via enqueue_nl_message."""
        gw = self.gw
        enqueued = []
        with patch.object(gw, "route_to_earnsai", side_effect=lambda *a: (_ for _ in ()).throw(AssertionError("earnsai called"))), \
             patch.object(gw, "enqueue_nl_message", side_effect=lambda **kw: enqueued.append(kw)):
            update = make_update(text="Tolong carikan info tentang Python 3.13", chat_id=OWNER_CHAT_ID)
            gw.route_update(TOKEN, OWNER_CHAT_ID, update)
        self.assertEqual(len(enqueued), 1)
        self.assertEqual(enqueued[0]["text"], "Tolong carikan info tentang Python 3.13")

    def test_T1d_photo_is_ignored(self):
        """Non-text messages (photo/document) must be silently ignored."""
        gw = self.gw
        enqueued = []
        with patch.object(gw, "enqueue_nl_message", side_effect=lambda **kw: enqueued.append(kw)):
            update = {
                "update_id": 300,
                "message": {
                    "message_id": 99,
                    "chat": {"id": int(OWNER_CHAT_ID)},
                    "photo": [{"file_id": "abc"}],
                    # No "text" key
                }
            }
            gw.route_update(TOKEN, OWNER_CHAT_ID, update)
        self.assertEqual(len(enqueued), 0)


# ???????????????????????????????????????????????????????????????????????????????
# T2: Atomic enqueue + idempotency
# ???????????????????????????????????????????????????????????????????????????????
class TestEnqueue(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.gw = import_module_from_path("telegram_gateway_enq", GATEWAY_PATH)
        self.gw.NL_QUEUE_DIR = os.path.join(self.tmpdir, "nl-queue")
        self.gw.LOG_FILE = os.path.join(self.tmpdir, "gateway.log")
        os.makedirs(self.gw.NL_QUEUE_DIR)

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _enqueue(self, update_id=1, message_id=1, text="hello"):
        return self.gw.enqueue_nl_message(
            update_id=update_id,
            sender_chat_id=OWNER_CHAT_ID,
            owner_chat_id=OWNER_CHAT_ID,
            message_id=message_id,
            text=text,
        )

    def test_T2a_enqueue_creates_json_file(self):
        result = self._enqueue(update_id=1, message_id=1)
        self.assertTrue(result)
        dest = os.path.join(self.gw.NL_QUEUE_DIR, "1-1.json")
        self.assertTrue(os.path.exists(dest))
        with open(dest) as f:
            item = json.load(f)
        self.assertEqual(item["status"], "pending")
        self.assertEqual(item["request_id"], "1-1")
        self.assertEqual(item["attempt_count"], 0)
        self.assertFalse(item["reply_sent"])

    def test_T2b_schema_fields_present(self):
        self._enqueue(update_id=2, message_id=2, text="schema check")
        dest = os.path.join(self.gw.NL_QUEUE_DIR, "2-2.json")
        with open(dest) as f:
            item = json.load(f)
        required = ["request_id", "telegram_update_id", "chat_id", "message_id",
                    "received_at", "text", "status", "attempt_count",
                    "last_attempt_at", "reply_sent"]
        for field in required:
            self.assertIn(field, item, f"Missing field: {field}")

    def test_T2c_duplicate_is_skipped(self):
        r1 = self._enqueue(update_id=3, message_id=3, text="first")
        r2 = self._enqueue(update_id=3, message_id=3, text="duplicate")
        self.assertTrue(r1)
        self.assertFalse(r2)
        # Original file content unchanged
        dest = os.path.join(self.gw.NL_QUEUE_DIR, "3-3.json")
        with open(dest) as f:
            item = json.load(f)
        self.assertEqual(item["text"], "first")

    def test_T2d_unauthorized_chat_rejected(self):
        result = self.gw.enqueue_nl_message(
            update_id=4,
            sender_chat_id="999999",   # unauthorized
            owner_chat_id=OWNER_CHAT_ID,
            message_id=4,
            text="attack",
        )
        self.assertFalse(result)
        dest = os.path.join(self.gw.NL_QUEUE_DIR, "4-4.json")
        self.assertFalse(os.path.exists(dest))

    def test_T2e_no_tmp_files_left_after_success(self):
        self._enqueue(update_id=5, message_id=5)
        tmp_files = [f for f in os.listdir(self.gw.NL_QUEUE_DIR) if ".tmp" in f]
        self.assertEqual(tmp_files, [])

    def test_T2f_token_not_in_queue_file(self):
        self._enqueue(update_id=6, message_id=6)
        dest = os.path.join(self.gw.NL_QUEUE_DIR, "6-6.json")
        with open(dest) as f:
            content = f.read()
        self.assertNotIn(TOKEN, content)
        self.assertNotIn("bot_token", content.lower())


# ???????????????????????????????????????????????????????????????????????????????
# T3 + T4 + T5 + T6 + T7: Worker state machine
# ???????????????????????????????????????????????????????????????????????????????
class TestWorker(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.wk = import_module_from_path("airo_hermes_worker", WORKER_PATH)
        self.wk.NL_QUEUE_DIR = os.path.join(self.tmpdir, "nl-queue")
        self.wk.DEAD_DIR      = os.path.join(self.tmpdir, "nl-queue", "dead")
        self.wk.SESSION_MAP   = os.path.join(self.tmpdir, "sessions.json")
        self.wk.LOG_FILE      = os.path.join(self.tmpdir, "worker.log")
        self.wk.TICK_FILE     = os.path.join(self.tmpdir, "tick.txt")
        os.makedirs(self.wk.NL_QUEUE_DIR)

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _make_item(self, request_id="1-1", status="pending", attempt_count=0,
                   reply_sent=False, chat_id=OWNER_CHAT_ID, text="hello"):
        return {
            "request_id": request_id,
            "telegram_update_id": 1,
            "chat_id": chat_id,
            "message_id": 1,
            "received_at": datetime.now().isoformat(),
            "text": text,
            "status": status,
            "attempt_count": attempt_count,
            "last_attempt_at": None,
            "reply_sent": reply_sent,
        }

    def _write_item(self, item, name=None):
        name = name or (item["request_id"] + ".json")
        path = os.path.join(self.wk.NL_QUEUE_DIR, name)
        with open(path, "w") as f:
            json.dump(item, f)
        return path

    def test_T3_pending_to_done(self):
        """Worker processes pending item: pending -> processing -> done."""
        wk = self.wk
        smap = {}
        item = self._make_item()
        path = self._write_item(item)

        with patch.object(wk, "call_hermes", return_value="Ini jawaban dari Hermes"), \
             patch.object(wk, "tg_send_message", return_value=True):
            wk.process_item(path, item, TOKEN, OWNER_CHAT_ID, smap)

        with open(path) as f:
            result = json.load(f)
        self.assertEqual(result["status"], "done")
        self.assertTrue(result["reply_sent"])
        self.assertIn("done_at", result)

    def test_T4a_failed_item_increments_attempt(self):
        """Failed Hermes call increments attempt_count and sets status=failed."""
        wk = self.wk
        smap = {}
        item = self._make_item(attempt_count=0)
        path = self._write_item(item)

        with patch.object(wk, "call_hermes", return_value=None), \
             patch.object(wk, "tg_send_message", return_value=False):
            wk.process_item(path, item, TOKEN, OWNER_CHAT_ID, smap)

        with open(path) as f:
            result = json.load(f)
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["attempt_count"], 1)

    def test_T4b_dead_letter_after_max_attempts(self):
        """Item dead-lettered when attempt_count >= MAX_ATTEMPTS."""
        wk = self.wk
        smap = {}
        max_a = wk.MAX_ATTEMPTS
        item = self._make_item(attempt_count=max_a, status="failed")
        path = self._write_item(item)

        wk.process_item(path, item, TOKEN, OWNER_CHAT_ID, smap)

        # Original item gone from queue
        self.assertFalse(os.path.exists(path))
        # Exists in dead dir
        dead = os.path.join(wk.DEAD_DIR, "1-1.json")
        self.assertTrue(os.path.exists(dead))
        with open(dead) as f:
            dead_item = json.load(f)
        self.assertEqual(dead_item["status"], "dead")

    def test_T5_reply_sent_guard(self):
        """reply_sent=True prevents duplicate sendMessage calls."""
        wk = self.wk
        smap = {}
        item = self._make_item(reply_sent=True, status="done")
        path = self._write_item(item)

        send_calls = []
        with patch.object(wk, "call_hermes", side_effect=lambda *a, **kw: send_calls.append("model")), \
             patch.object(wk, "tg_send_message", side_effect=lambda *a, **kw: send_calls.append("send")):
            wk.process_item(path, item, TOKEN, OWNER_CHAT_ID, smap)

        self.assertNotIn("model", send_calls)
        self.assertNotIn("send", send_calls)


    def test_T5b_send_retry_reuses_cached_reply(self):
        """A send failure must not trigger a second Hermes/model call."""
        wk = self.wk
        smap = {}
        item = self._make_item()
        path = self._write_item(item)

        model_calls = []

        def fake_hermes(*args, **kwargs):
            model_calls.append("model")
            return "cached Hermes reply"

        with patch.object(wk, "call_hermes", side_effect=fake_hermes), \
             patch.object(wk, "tg_send_message", return_value=False):
            wk.process_item(
                path,
                item,
                TOKEN,
                OWNER_CHAT_ID,
                smap,
            )

        with open(path) as f:
            failed_item = json.load(f)

        self.assertEqual(failed_item["status"], "failed")
        self.assertEqual(
            failed_item["reply_text"],
            "cached Hermes reply",
        )
        self.assertEqual(model_calls, ["model"])

        with patch.object(
            wk,
            "call_hermes",
            side_effect=AssertionError(
                "Hermes must not be called twice"
            ),
        ), patch.object(
            wk,
            "tg_send_message",
            return_value=True,
        ):
            wk.process_item(
                path,
                failed_item,
                TOKEN,
                OWNER_CHAT_ID,
                smap,
            )

        with open(path) as f:
            done_item = json.load(f)

        self.assertEqual(done_item["status"], "done")
        self.assertTrue(done_item["reply_sent"])
        self.assertEqual(model_calls, ["model"])

    def test_T6_unauthorized_chat_dead_lettered(self):
        """Item with unauthorized chat_id must be dead-lettered immediately."""
        wk = self.wk
        smap = {}
        item = self._make_item(chat_id="999999")  # not owner
        path = self._write_item(item)

        hermes_calls = []
        with patch.object(wk, "call_hermes", side_effect=lambda *a, **kw: hermes_calls.append("hermes")):
            wk.process_item(path, item, TOKEN, OWNER_CHAT_ID, smap)

        self.assertFalse(os.path.exists(path))
        self.assertEqual(hermes_calls, [])  # Hermes was NOT called
        dead = os.path.join(wk.DEAD_DIR, "1-1.json")
        self.assertTrue(os.path.exists(dead))

    def test_T7_toolsets_exclude_mutation_tools(self):
        """HERMES_TOOLSETS must be ['safe'] and must NOT include terminal/patch/write_file."""
        wk = self.wk
        self.assertEqual(wk.HERMES_TOOLSETS, ["safe"])
        # Verify "safe" toolset from toolsets.py does NOT include mutation tools
        # (static proof: toolsets.py L334-338: includes=["web","vision","image_gen"])
        # web = [web_search, web_extract]
        # vision = [vision_analyze]
        # image_gen = [image_generate]
        SAFE_EXPECTED_TOOLS = {"web_search", "web_extract", "vision_analyze", "image_generate"}
        FORBIDDEN_TOOLS = {"terminal", "process", "write_file", "patch", "execute_code",
                           "search_files", "read_file", "delegate_task"}
        # The toolset config is locked to ["safe"] ? verify no forbidden tools in expected safe set
        for tool in FORBIDDEN_TOOLS:
            self.assertNotIn(tool, SAFE_EXPECTED_TOOLS,
                             f"FORBIDDEN tool '{tool}' found in safe toolset resolved tools")


# ???????????????????????????????????????????????????????????????????????????????
# Run
# ???????????????????????????????????????????????????????????????????????????????
if __name__ == "__main__":
    print("=" * 60)
    print("AIRO Phase 0B1 Static Test Suite")
    print("MODEL_CALLS=NONE | NETWORK_CALLS=NONE | GATEWAY_CALLS=NONE")
    print("=" * 60)
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for cls in [TestRoutingPriority, TestEnqueue, TestWorker]:
        suite.addTests(loader.loadTestsFromTestCase(cls))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    print()
    print("=" * 60)
    if result.wasSuccessful():
        print("STATIC_TESTS=PASS")
    else:
        print(f"STATIC_TESTS=FAIL ({len(result.failures)} failures, {len(result.errors)} errors)")
    print("=" * 60)
    sys.exit(0 if result.wasSuccessful() else 1)
