import importlib.machinery
import importlib.util
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
WORKER_PATH = REPO_ROOT / "scripts/airo-hermes-worker"
CLIENT_DIR = (
    REPO_ROOT
    / "ecosystem/projects/earesmes-arfin-bridge"
)


def load_worker():
    loader = importlib.machinery.SourceFileLoader(
        "airo_hermes_worker_m16_test",
        str(WORKER_PATH),
    )
    spec = importlib.util.spec_from_loader(
        loader.name,
        loader,
    )
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class FakeClient:
    def __init__(
        self,
        *,
        list_response=None,
        get_response=None,
        submit_response=None,
    ):
        self.list_response = list_response or {}
        self.get_response = get_response or {}
        self.submit_response = submit_response or {}
        self.submit_calls = []
        self.get_calls = []

    def list_pending(self, owner_chat_id):
        return self.list_response

    def get_pending(self, pending_id, owner_chat_id):
        self.get_calls.append(
            (pending_id, owner_chat_id)
        )
        return self.get_response

    def submit_clarification(
        self,
        pending_id,
        pending_version,
        clarification_text,
        owner_chat_id,
    ):
        self.submit_calls.append(
            (
                pending_id,
                pending_version,
                clarification_text,
                owner_chat_id,
            )
        )
        return self.submit_response


def success_items(items):
    return {
        "application_status": "SUCCESS",
        "application_error_code": "NONE",
        "payload": {
            "items": items,
        },
    }


def pending_record(version=1):
    return {
        "pending_id": "pending:canonical:123",
        "short_ref": "AF-1234",
        "pending_version": version,
        "type": "missing_account",
        "amount": 125000,
        "description": "Shell",
        "prompt": "Sumber dana / akun yang benar apa?",
    }


class TestProactiveFrontDesk(unittest.TestCase):
    def setUp(self):
        self.worker = load_worker()
        self.tmp = tempfile.TemporaryDirectory()
        self.worker.EAB_PROACTIVE_STATE_FILE = str(
            Path(self.tmp.name) / "state.json"
        )

    def tearDown(self):
        self.tmp.cleanup()

    def test_get_pending_client_fake_contract(self):
        import sys
        sys.path.insert(0, str(CLIENT_DIR))
        from src.adapter.eab_live_client import EABLiveSignedClient

        client = EABLiveSignedClient(
            service_secret="x",
            fake_mode=True,
        )
        result = client.get_pending(
            "pending:canonical:123",
            "owner",
        )
        self.assertEqual(
            result["operation_id"],
            "EAB_GET_PENDING",
        )
        self.assertEqual(
            result["payload"]["pending_id"],
            "pending:canonical:123",
        )

    def test_new_pending_sends_once_and_dedupes(self):
        client = FakeClient(
            list_response=success_items(
                [pending_record(1)]
            )
        )
        sent = []

        def sender(token, chat, text):
            sent.append((token, chat, text))
            return True

        first = self.worker._eab_proactive_tick(
            "token",
            "owner",
            now_sec=1000,
            client=client,
            sender=sender,
        )
        second = self.worker._eab_proactive_tick(
            "token",
            "owner",
            now_sec=1061,
            client=client,
            sender=sender,
        )

        self.assertEqual(first["status"], "sent")
        self.assertEqual(second["status"], "deduped")
        self.assertEqual(len(sent), 1)

    def test_send_failure_is_not_marked_delivered(self):
        client = FakeClient(
            list_response=success_items(
                [pending_record(1)]
            )
        )
        attempts = []

        def sender(token, chat, text):
            attempts.append(text)
            return len(attempts) > 1

        first = self.worker._eab_proactive_tick(
            "token",
            "owner",
            now_sec=1000,
            client=client,
            sender=sender,
        )
        second = self.worker._eab_proactive_tick(
            "token",
            "owner",
            now_sec=1061,
            client=client,
            sender=sender,
        )

        self.assertEqual(first["status"], "send_failed")
        self.assertEqual(second["status"], "sent")
        self.assertEqual(len(attempts), 2)

    def test_changed_version_reprompts(self):
        sent = []

        def sender(token, chat, text):
            sent.append(text)
            return True

        c1 = FakeClient(
            list_response=success_items(
                [pending_record(1)]
            )
        )
        c2 = FakeClient(
            list_response=success_items(
                [pending_record(2)]
            )
        )

        self.worker._eab_proactive_tick(
            "token",
            "owner",
            now_sec=1000,
            client=c1,
            sender=sender,
        )
        result = self.worker._eab_proactive_tick(
            "token",
            "owner",
            now_sec=1061,
            client=c2,
            sender=sender,
        )

        self.assertEqual(result["status"], "sent")
        self.assertEqual(len(sent), 2)

    def test_no_pending_clears_active_prompt(self):
        state = self.worker._eab_load_proactive_state()
        self.worker._eab_set_active_record(
            state,
            pending_record(1),
            mark_delivered=True,
            now_sec=1,
        )
        self.worker._eab_save_proactive_state(state)

        client = FakeClient(
            list_response=success_items([])
        )

        result = self.worker._eab_proactive_tick(
            "token",
            "owner",
            now_sec=1000,
            client=client,
            sender=lambda *args: True,
        )

        state_after = (
            self.worker._eab_load_proactive_state()
        )

        self.assertEqual(result["status"], "no_pending")
        self.assertIsNone(
            state_after.get("active_prompt")
        )

    def test_active_reply_uses_canonical_identity_version(self):
        state = self.worker._eab_load_proactive_state()
        self.worker._eab_set_active_record(
            state,
            pending_record(3),
            mark_delivered=True,
            now_sec=1,
        )
        self.worker._eab_save_proactive_state(state)

        client = FakeClient(
            get_response={
                "application_status": "SUCCESS",
                "payload": {
                    "found": True,
                    "record": pending_record(3),
                },
            },
            submit_response={
                "application_status": "SUCCESS",
                "payload": {
                    "resolved": True,
                    "pending": None,
                    "completion_message": "✅ selesai",
                    "arfin_telegram_outbound_suppressed": True,
                },
            },
        )

        reply = (
            self.worker._eab_handle_active_prompt_reply(
                "blu",
                "owner",
                client=client,
            )
        )

        self.assertEqual(reply, "✅ selesai")
        self.assertEqual(
            client.submit_calls,
            [
                (
                    "pending:canonical:123",
                    3,
                    "blu",
                    "owner",
                )
            ],
        )

    def test_stale_active_reply_refreshes_without_submit(self):
        state = self.worker._eab_load_proactive_state()
        self.worker._eab_set_active_record(
            state,
            pending_record(2),
            mark_delivered=True,
            now_sec=1,
        )
        self.worker._eab_save_proactive_state(state)

        client = FakeClient(
            get_response={
                "application_status": "SUCCESS",
                "payload": {
                    "found": True,
                    "record": pending_record(3),
                },
            },
        )

        reply = (
            self.worker._eab_handle_active_prompt_reply(
                "blu",
                "owner",
                client=client,
            )
        )

        self.assertIn(
            "berubah sejak prompt terakhir",
            reply,
        )
        self.assertEqual(client.submit_calls, [])

    def test_backend_source_has_distinct_m16_contract(self):
        backend = (
            REPO_ROOT
            / "ecosystem/projects/vortex-ai-skill-lab"
            / "apps-script-live/AIRO_Finance_Multitab_Final_v1.js"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "EAB_M16_PROACTIVE_FRONTDESK_V1",
            backend,
        )
        self.assertIn(
            "airoEabRunCapturedTelegramReply_",
            backend,
        )
        self.assertIn(
            "ERR_STALE_PENDING_VERSION",
            backend,
        )
        self.assertIn(
            "arfin_telegram_outbound_suppressed: true",
            backend,
        )
        self.assertIn(
            "pending.short_ref =",
            backend,
        )
        self.assertIn(
            "pending.pending_version =",
            backend,
        )

        effective = backend[
            backend.rfind(
                "/* EAB_DIRECT_V1_RECEIVER_START */"
            ):
        ]

        self.assertIn(
            "} else if (op === 'EAB_SUBMIT_CLARIFICATION') {",
            effective,
        )
        manual_line = (
            "} else if (op === 'EAB_SUBMIT_BATCH_CLARIFICATION' "
            "|| op === 'EAB_CREATE_MANUAL_TRANSACTION' "
            "|| op === 'EAB_CREATE_MANUAL') {"
        )
        self.assertIn(manual_line, effective)

    def test_worker_repo_root_is_runtime_relative(self):
        worker_source = WORKER_PATH.read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "REPO_DIR       = str(Path(__file__).resolve().parents[1])",
            worker_source,
        )
        self.assertNotIn(
            'REPO_DIR       = "/home/egitaristorandas/AI_WORKSPACES/airo-second-brain"',
            worker_source,
        )


if __name__ == "__main__":
    unittest.main()
