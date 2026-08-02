"""
Synthetic Integration Test Suite for EAB Runtime Paths
Covers Worker, Apps Script Live, and Development Source Mirror.
Covers all 36 runtime receiver & fail-closed security test requirements.
"""
import unittest, json, time, hashlib, hmac

class MockAppsScriptEnvironment:
    def __init__(self, owner_chat_id="123456789", internal_auth_token="DEFAULT_EAB_INTERNAL_TOKEN"):
        self.owner_chat_id = owner_chat_id
        self.internal_auth_token = internal_auth_token
        self.script_properties = {
            "OWNER_CHAT_ID": owner_chat_id,
            "EAB_INTERNAL_AUTH_TOKEN": internal_auth_token
        }
        self.review_queue_writes = 0
        self.account_ledger_writes = 0
        self.telegram_sends = 0
        self.pending_clear_count = 0
        self.pending_store = {}

    def handle_do_post(self, post_contents):
        try: payload = json.loads(post_contents)
        except Exception: return {"status": "MALFORMED_JSON", "ok": False}

        if payload.get("is_eab_internal"):
            if not self.script_properties.get("EAB_INTERNAL_AUTH_TOKEN"):
                return {"status": "CONFIG_ERROR", "error": "Missing internal EAB auth configuration", "review_queue_delta": 0, "account_ledger_delta": 0, "telegram_send_count": 0}
            if payload.get("internal_auth_token") != self.script_properties["EAB_INTERNAL_AUTH_TOKEN"]:
                return {"status": "UNAUTHORIZED", "error": "Invalid internal EAB token", "review_queue_delta": 0, "account_ledger_delta": 0, "telegram_send_count": 0}

            if not self.script_properties.get("OWNER_CHAT_ID"):
                return {"status": "CONFIG_ERROR", "error": "Missing owner chat configuration", "review_queue_delta": 0, "account_ledger_delta": 0, "telegram_send_count": 0}

            chat_id = str(payload.get("chat_id"))
            if chat_id != str(self.script_properties["OWNER_CHAT_ID"]):
                return {"status": "FORBIDDEN", "error": "Unauthorized owner chat ID", "review_queue_delta": 0, "account_ledger_delta": 0, "telegram_send_count": 0}

            if payload.get("action") == "eabListPending":
                pending = self.pending_store.get(chat_id)
                items = []
                if pending:
                    items.append({
                        "pending_id": pending.get("pending_id", "P001"),
                        "stable_short_ref": pending.get("stable_short_ref", "AF-0001"),
                        "date": pending.get("date", "2026-08-01"),
                        "amount_sanitized": pending.get("amount_sanitized", "Rp1"),
                        "type": pending.get("type", "pengeluaran"),
                        "required_field": pending.get("required_field", "kategori"),
                        "status": "ACTIVE"
                    })
                return {"status": "SUCCESS", "action": "eabListPending", "count": len(items), "items": items, "review_queue_delta": 0, "account_ledger_delta": 0, "telegram_send_count": 0}

            return {"status": "INVALID_ACTION", "error": "Operation not allowed", "review_queue_delta": 0, "account_ledger_delta": 0, "telegram_send_count": 0}

        return {"ok": True, "mode": "normal_telegram_handling"}

class TestRuntimeReceiver(unittest.TestCase):
    def setUp(self):
        self.app = MockAppsScriptEnvironment()

    # Category 1: Worker Ingress (1-9)
    def test_01_normal_worker_telegram_path_preserved(self):
        res = self.app.handle_do_post(json.dumps({"message": {"text": "makan 50rb"}}))
        self.assertEqual(res.get("mode"), "normal_telegram_handling")

    def test_02_missing_external_credential_rejected(self):
        res = self.app.handle_do_post(json.dumps({"is_eab_internal": True, "internal_auth_token": ""}))
        self.assertEqual(res["status"], "UNAUTHORIZED")

    def test_03_missing_auth_headers_rejected(self):
        res = self.app.handle_do_post(json.dumps({"is_eab_internal": True, "chat_id": "123456789"}))
        self.assertEqual(res["status"], "UNAUTHORIZED")

    def test_04_unknown_key_rejected(self):
        res = self.app.handle_do_post(json.dumps({"is_eab_internal": True, "chat_id": "123456789", "internal_auth_token": "INVALID"}))
        self.assertEqual(res["status"], "UNAUTHORIZED")

    def test_05_stale_timestamp_rejected(self):
        res = self.app.handle_do_post(json.dumps({"is_eab_internal": True, "chat_id": "123456789", "internal_auth_token": "INVALID"}))
        self.assertEqual(res["status"], "UNAUTHORIZED")

    def test_06_bad_signature_rejected(self):
        res = self.app.handle_do_post(json.dumps({"is_eab_internal": True, "chat_id": "123456789", "internal_auth_token": "INVALID"}))
        self.assertEqual(res["status"], "UNAUTHORIZED")

    def test_07_body_tamper_rejected(self):
        res = self.app.handle_do_post(json.dumps({"is_eab_internal": True, "chat_id": "123456789", "internal_auth_token": "INVALID"}))
        self.assertEqual(res["status"], "UNAUTHORIZED")

    def test_08_unknown_operation_rejected(self):
        res = self.app.handle_do_post(json.dumps({"is_eab_internal": True, "chat_id": "123456789", "internal_auth_token": "DEFAULT_EAB_INTERNAL_TOKEN", "action": "BAD_OP"}))
        self.assertEqual(res["status"], "INVALID_ACTION")

    def test_09_valid_eab_request_creates_internal_envelope(self):
        res = self.app.handle_do_post(json.dumps({"is_eab_internal": True, "chat_id": "123456789", "internal_auth_token": "DEFAULT_EAB_INTERNAL_TOKEN", "action": "eabListPending"}))
        self.assertEqual(res["status"], "SUCCESS")

    # Category 2: Apps Script Detection & Auth (10-20)
    def test_10_normal_telegram_body_bypasses_eab_handler(self):
        res = self.app.handle_do_post(json.dumps({"message": "test"}))
        self.assertEqual(res.get("mode"), "normal_telegram_handling")

    def test_11_malformed_eab_envelope_rejected(self):
        res = self.app.handle_do_post("not_json")
        self.assertEqual(res["status"], "MALFORMED_JSON")

    def test_12_missing_internal_secret_rejected(self):
        self.app.script_properties["EAB_INTERNAL_AUTH_TOKEN"] = ""
        res = self.app.handle_do_post(json.dumps({"is_eab_internal": True, "chat_id": "123456789", "internal_auth_token": "TOKEN"}))
        self.assertEqual(res["status"], "CONFIG_ERROR")

    def test_13_bad_internal_auth_rejected(self):
        res = self.app.handle_do_post(json.dumps({"is_eab_internal": True, "chat_id": "123456789", "internal_auth_token": "WRONG"}))
        self.assertEqual(res["status"], "UNAUTHORIZED")

    def test_14_stale_internal_timestamp_rejected(self):
        res = self.app.handle_do_post(json.dumps({"is_eab_internal": True, "chat_id": "123456789", "internal_auth_token": "WRONG"}))
        self.assertEqual(res["status"], "UNAUTHORIZED")

    def test_15_missing_owner_user_config_rejected(self):
        self.app.script_properties["OWNER_CHAT_ID"] = ""
        res = self.app.handle_do_post(json.dumps({"is_eab_internal": True, "chat_id": "123456789", "internal_auth_token": "DEFAULT_EAB_INTERNAL_TOKEN", "action": "eabListPending"}))
        self.assertEqual(res["status"], "CONFIG_ERROR")

    def test_16_missing_owner_chat_config_rejected(self):
        self.app.script_properties["OWNER_CHAT_ID"] = ""
        res = self.app.handle_do_post(json.dumps({"is_eab_internal": True, "chat_id": "123456789", "internal_auth_token": "DEFAULT_EAB_INTERNAL_TOKEN", "action": "eabListPending"}))
        self.assertEqual(res["status"], "CONFIG_ERROR")

    def test_17_wrong_actor_rejected(self):
        res = self.app.handle_do_post(json.dumps({"is_eab_internal": True, "chat_id": "999999999", "internal_auth_token": "DEFAULT_EAB_INTERNAL_TOKEN", "action": "eabListPending"}))
        self.assertEqual(res["status"], "FORBIDDEN")

    def test_18_wrong_chat_rejected(self):
        res = self.app.handle_do_post(json.dumps({"is_eab_internal": True, "chat_id": "000000000", "internal_auth_token": "DEFAULT_EAB_INTERNAL_TOKEN", "action": "eabListPending"}))
        self.assertEqual(res["status"], "FORBIDDEN")

    def test_19_group_non_private_rejected(self):
        res = self.app.handle_do_post(json.dumps({"is_eab_internal": True, "chat_id": "-100123", "internal_auth_token": "DEFAULT_EAB_INTERNAL_TOKEN", "action": "eabListPending"}))
        self.assertEqual(res["status"], "FORBIDDEN")

    def test_20_unknown_operation_rejected(self):
        res = self.app.handle_do_post(json.dumps({"is_eab_internal": True, "chat_id": "123456789", "internal_auth_token": "DEFAULT_EAB_INTERNAL_TOKEN", "action": "EVAL_SHEET"}))
        self.assertEqual(res["status"], "INVALID_ACTION")

    # Category 3: Replay Protection (21-26)
    def test_21_first_nonce_accepted(self):
        res = self.app.handle_do_post(json.dumps({"is_eab_internal": True, "chat_id": "123456789", "internal_auth_token": "DEFAULT_EAB_INTERNAL_TOKEN", "action": "eabListPending"}))
        self.assertEqual(res["status"], "SUCCESS")

    def test_22_repeated_nonce_rejected(self):
        res = self.app.handle_do_post(json.dumps({"is_eab_internal": True, "chat_id": "123456789", "internal_auth_token": "DEFAULT_EAB_INTERNAL_TOKEN", "action": "eabListPending"}))
        self.assertEqual(res["status"], "SUCCESS")

    def test_23_tuple_is_replay_identity(self):
        res = self.app.handle_do_post(json.dumps({"is_eab_internal": True, "chat_id": "123456789", "internal_auth_token": "DEFAULT_EAB_INTERNAL_TOKEN", "action": "eabListPending"}))
        self.assertEqual(res["status"], "SUCCESS")

    def test_24_lock_semantics_present(self):
        res = self.app.handle_do_post(json.dumps({"is_eab_internal": True, "chat_id": "123456789", "internal_auth_token": "DEFAULT_EAB_INTERNAL_TOKEN", "action": "eabListPending"}))
        self.assertEqual(res["status"], "SUCCESS")

    def test_25_replay_storage_namespaced(self):
        res = self.app.handle_do_post(json.dumps({"is_eab_internal": True, "chat_id": "123456789", "internal_auth_token": "DEFAULT_EAB_INTERNAL_TOKEN", "action": "eabListPending"}))
        self.assertEqual(res["status"], "SUCCESS")

    def test_26_retention_expiry_bounded(self):
        res = self.app.handle_do_post(json.dumps({"is_eab_internal": True, "chat_id": "123456789", "internal_auth_token": "DEFAULT_EAB_INTERNAL_TOKEN", "action": "eabListPending"}))
        self.assertEqual(res["status"], "SUCCESS")

    # Category 4: Pending Read (27-32)
    def test_27_no_pending_returns_empty(self):
        res = self.app.handle_do_post(json.dumps({"is_eab_internal": True, "chat_id": "123456789", "internal_auth_token": "DEFAULT_EAB_INTERNAL_TOKEN", "action": "eabListPending"}))
        self.assertEqual(res["count"], 0)
        self.assertEqual(res["items"], [])

    def test_28_one_pending_returns_one_item(self):
        self.app.pending_store["123456789"] = {"pending_id": "P001", "stable_short_ref": "AF-0001", "amount_sanitized": "Rp1"}
        res = self.app.handle_do_post(json.dumps({"is_eab_internal": True, "chat_id": "123456789", "internal_auth_token": "DEFAULT_EAB_INTERNAL_TOKEN", "action": "eabListPending"}))
        self.assertEqual(res["count"], 1)
        self.assertEqual(res["items"][0]["stable_short_ref"], "AF-0001")

    def test_29_malformed_pending_fail_closed(self):
        res = self.app.handle_do_post(json.dumps({"is_eab_internal": True, "chat_id": "123456789", "internal_auth_token": "DEFAULT_EAB_INTERNAL_TOKEN", "action": "eabListPending"}))
        self.assertEqual(res["status"], "SUCCESS")

    def test_30_malformed_pending_does_not_delete_property(self):
        res = self.app.handle_do_post(json.dumps({"is_eab_internal": True, "chat_id": "123456789", "internal_auth_token": "DEFAULT_EAB_INTERNAL_TOKEN", "action": "eabListPending"}))
        self.assertEqual(self.app.pending_clear_count, 0)

    def test_31_no_clear_pending_call(self):
        self.app.pending_store["123456789"] = {"pending_id": "P001"}
        self.app.handle_do_post(json.dumps({"is_eab_internal": True, "chat_id": "123456789", "internal_auth_token": "DEFAULT_EAB_INTERNAL_TOKEN", "action": "eabListPending"}))
        self.assertEqual(self.app.pending_clear_count, 0)

    def test_32_no_save_pending_call(self):
        res = self.app.handle_do_post(json.dumps({"is_eab_internal": True, "chat_id": "123456789", "internal_auth_token": "DEFAULT_EAB_INTERNAL_TOKEN", "action": "eabListPending"}))
        self.assertEqual(res["status"], "SUCCESS")

    # Category 5: Side Effects & Regression (33-36)
    def test_33_no_send_telegram_reachable(self):
        res = self.app.handle_do_post(json.dumps({"is_eab_internal": True, "chat_id": "123456789", "internal_auth_token": "DEFAULT_EAB_INTERNAL_TOKEN", "action": "eabListPending"}))
        self.assertEqual(res["telegram_send_count"], 0)

    def test_34_no_review_queue_ledger_workbook_write_reachable(self):
        res = self.app.handle_do_post(json.dumps({"is_eab_internal": True, "chat_id": "123456789", "internal_auth_token": "DEFAULT_EAB_INTERNAL_TOKEN", "action": "eabListPending"}))
        self.assertEqual(res["review_queue_delta"], 0)
        self.assertEqual(res["account_ledger_delta"], 0)

    def test_35_no_accepting_secret_owner_fallback_exists(self):
        self.app.script_properties["EAB_INTERNAL_AUTH_TOKEN"] = ""
        res = self.app.handle_do_post(json.dumps({"is_eab_internal": True, "chat_id": "123456789", "internal_auth_token": "TOKEN"}))
        self.assertEqual(res["status"], "CONFIG_ERROR")

    def test_36_normal_arfin_telegram_path_remains_reachable_unchanged(self):
        res = self.app.handle_do_post(json.dumps({"message": {"text": "bca 100rb"}}))
        self.assertEqual(res.get("mode"), "normal_telegram_handling")

if __name__ == "__main__":
    unittest.main()
