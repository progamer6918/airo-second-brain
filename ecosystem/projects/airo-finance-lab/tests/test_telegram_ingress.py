import unittest
import os
import tempfile
from airo_finance_core.db import DatabaseManager
from airo_finance_core.engine import FinanceCoreEngine
from airo_finance_core.telegram_ingress import (
    TelegramOutboundAdapter,
    FinanceTelegramIngressRouter,
    load_telegram_credentials
)

class MockTelegramTransport:
    def __init__(self):
        self.calls = []

    def __call__(self, method: str, payload: dict) -> dict:
        self.calls.append({"method": method, "payload": payload})
        if method == "sendMessage":
            return {"ok": True, "result": {"message_id": 999}}
        elif method == "editMessageText":
            return {"ok": True, "result": {"message_id": payload.get("message_id")}}
        elif method == "answerCallbackQuery":
            return {"ok": True, "result": True}
        return {"ok": True}

class TestTelegramIngress(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.tmp_dir, "test_ingress.db")
        self.db = DatabaseManager(self.db_path)
        self.db.init_schema()
        self.engine = FinanceCoreEngine(self.db)
        
        # Seed test accounts
        self.bca = self.engine.create_account("BCA Utama", "BANK", 1500000.0)
        self.mandiri = self.engine.create_account("Mandiri", "BANK", 500000.0)
        self.cash = self.engine.create_account("Cash Dompet", "CASH", 100000.0)
        
        # Seed test category
        self.cat_food = self.engine.create_category("Makanan & Minuman", "EXPENSE")
        
        self.owner_id = "12345678"
        self.unauthorized_id = "98765432"
        self.mock_transport = MockTelegramTransport()
        self.outbound = TelegramOutboundAdapter(token="TEST_TOKEN", transport=self.mock_transport)
        self.router = FinanceTelegramIngressRouter(
            engine=self.engine,
            outbound=self.outbound,
            owner_chat_id=self.owner_id
        )

    def tearDown(self):
        self.db.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_01_credentials_loading(self):
        env_file = os.path.join(self.tmp_dir, "test.env")
        with open(env_file, "w") as f:
            f.write("export AIRO_HERMES_TELEGRAM_BOT_TOKEN=\"TEST_SECRET_TOKEN\"\n")
            f.write("OWNER_TELEGRAM_ID=\"99887766\"\n")
            
        token, owner_id = load_telegram_credentials(env_path=env_file)
        self.assertEqual(token, "TEST_SECRET_TOKEN")
        self.assertEqual(owner_id, "99887766")

    def test_02_outbound_adapter_methods(self):
        # Test send_message
        res1 = self.outbound.send_message(self.owner_id, "<b>Halo</b>", reply_markup={"inline_keyboard": []})
        self.assertTrue(res1.get("ok"))
        self.assertEqual(self.mock_transport.calls[-1]["method"], "sendMessage")
        self.assertEqual(self.mock_transport.calls[-1]["payload"]["chat_id"], self.owner_id)

        # Test edit_message_text
        res2 = self.outbound.edit_message_text(self.owner_id, 999, "Updated text")
        self.assertTrue(res2.get("ok"))
        self.assertEqual(self.mock_transport.calls[-1]["method"], "editMessageText")
        self.assertEqual(self.mock_transport.calls[-1]["payload"]["message_id"], 999)

        # Test answer_callback_query
        res3 = self.outbound.answer_callback_query("cq_123", text="Alert text", show_alert=True)
        self.assertTrue(res3.get("ok"))
        self.assertEqual(self.mock_transport.calls[-1]["method"], "answerCallbackQuery")
        self.assertEqual(self.mock_transport.calls[-1]["payload"]["callback_query_id"], "cq_123")

    def test_03_owner_filter_authorization(self):
        self.assertTrue(self.router.is_owner(self.owner_id))
        self.assertFalse(self.router.is_owner(self.unauthorized_id))

    def test_04_non_owner_write_blocked(self):
        # 1. Non-owner sends transaction
        update_msg = {
            "update_id": 101,
            "message": {
                "message_id": 1,
                "chat": {"id": self.unauthorized_id},
                "from": {"id": self.unauthorized_id},
                "text": "makan 35k bca"
            }
        }
        handled, reason = self.router.handle_update(update_msg)
        self.assertTrue(handled)
        self.assertEqual(reason, "BLOCKED_NON_OWNER_WRITE")
        
        # Verify denial message sent
        self.assertEqual(self.mock_transport.calls[-1]["method"], "sendMessage")
        self.assertIn("Akses Ditolak", self.mock_transport.calls[-1]["payload"]["text"])

        # Verify zero ledger mutations
        conn = self.db.get_connection()
        tx_cnt = conn.execute("SELECT count(*) FROM transactions").fetchone()[0]
        self.assertEqual(tx_cnt, 0)
        bca_balance = conn.execute("SELECT balance FROM accounts WHERE id = ?", (self.bca.id,)).fetchone()[0]
        self.assertEqual(bca_balance, 1500000.0)

        # 2. Non-owner attempts to confirm a candidate via callback
        cand = self.router.confirmation_handler.stage_input("makan 35k bca")
        update_cq = {
            "update_id": 102,
            "callback_query": {
                "id": "cq_fake",
                "from": {"id": self.unauthorized_id},
                "message": {"message_id": 99, "chat": {"id": self.unauthorized_id}},
                "data": f"cfm:{cand.candidate_id}"
            }
        }
        handled_cq, reason_cq = self.router.handle_update(update_cq)
        self.assertTrue(handled_cq)
        self.assertEqual(reason_cq, "BLOCKED_NON_OWNER_CALLBACK")
        
        # Verify ledger still untouched
        tx_cnt_after = conn.execute("SELECT count(*) FROM transactions").fetchone()[0]
        self.assertEqual(tx_cnt_after, 0)

    def test_05_transaction_staging_and_card(self):
        update = {
            "update_id": 103,
            "message": {
                "message_id": 5,
                "chat": {"id": self.owner_id},
                "from": {"id": self.owner_id},
                "text": "makan 35k bca"
            }
        }
        handled, reason = self.router.handle_update(update)
        self.assertTrue(handled)
        self.assertTrue(reason.startswith("STAGED_CARD_SENT:cand_"))

        # Verify confirmation card dispatched via outbound client
        last_call = self.mock_transport.calls[-1]
        self.assertEqual(last_call["method"], "sendMessage")
        self.assertIn("Konfirmasi Transaksi", last_call["payload"]["text"])
        self.assertIn("Rp35.000", last_call["payload"]["text"])
        
        # Verify inline keyboard has short callback data
        inline_kb = last_call["payload"]["reply_markup"]["inline_keyboard"][0]
        self.assertTrue(any(btn["callback_data"].startswith("cfm:cand_") for btn in inline_kb))
        self.assertTrue(any(btn["callback_data"].startswith("ccl:cand_") for btn in inline_kb))

        # Verify ledger is not written yet
        conn = self.db.get_connection()
        tx_cnt = conn.execute("SELECT count(*) FROM transactions").fetchone()[0]
        self.assertEqual(tx_cnt, 0)

    def test_06_confirmation_callback_flow(self):
        # 1. Stage candidate
        cand = self.router.confirmation_handler.stage_input("makan 50k bca")
        cand_id = cand.candidate_id

        # 2. Owner clicks confirm
        update = {
            "update_id": 104,
            "callback_query": {
                "id": "cq_confirm_1",
                "from": {"id": self.owner_id},
                "message": {"message_id": 10, "chat": {"id": self.owner_id}},
                "data": f"cfm:{cand_id}"
            }
        }
        handled, reason = self.router.handle_update(update)
        self.assertTrue(handled)
        self.assertTrue(reason.startswith("CONFIRMED:tx_"))

        # 3. Verify ledger write and balance deduction
        conn = self.db.get_connection()
        tx_row = conn.execute("SELECT id, amount, direction, account_id FROM transactions WHERE note = 'makan'").fetchone()
        self.assertIsNotNone(tx_row)
        self.assertEqual(tx_row["amount"], 50000.0)
        self.assertEqual(tx_row["direction"], "EXPENSE")

        bca_balance = conn.execute("SELECT balance FROM accounts WHERE id = ?", (self.bca.id,)).fetchone()[0]
        self.assertEqual(bca_balance, 1450000.0)

        # 4. Verify audit log entry
        audit_row = conn.execute("SELECT id, entity, entity_id, action FROM audit_logs WHERE entity_id = ?", (tx_row["id"],)).fetchone()
        self.assertIsNotNone(audit_row)
        self.assertEqual(audit_row["action"], "CREATE")

        # 5. Verify outbound message edit and answer callback
        calls = [c["method"] for c in self.mock_transport.calls[-2:]]
        self.assertIn("editMessageText", calls)
        self.assertIn("answerCallbackQuery", calls)

    def test_07_cancellation_callback_flow(self):
        cand = self.router.confirmation_handler.stage_input("bensin 100k bca")
        cand_id = cand.candidate_id

        update = {
            "update_id": 105,
            "callback_query": {
                "id": "cq_cancel_1",
                "from": {"id": self.owner_id},
                "message": {"message_id": 12, "chat": {"id": self.owner_id}},
                "data": f"ccl:{cand_id}"
            }
        }
        handled, reason = self.router.handle_update(update)
        self.assertTrue(handled)
        self.assertEqual(reason, "CANCELLED")

        # Verify zero ledger entries
        conn = self.db.get_connection()
        tx_cnt = conn.execute("SELECT count(*) FROM transactions").fetchone()[0]
        self.assertEqual(tx_cnt, 0)
        bca_balance = conn.execute("SELECT balance FROM accounts WHERE id = ?", (self.bca.id,)).fetchone()[0]
        self.assertEqual(bca_balance, 1500000.0)

    def test_08_transfer_transaction_routing(self):
        update_msg = {
            "update_id": 106,
            "message": {
                "message_id": 15,
                "chat": {"id": self.owner_id},
                "from": {"id": self.owner_id},
                "text": "trf 200k bca ke mandiri"
            }
        }
        handled, reason = self.router.handle_update(update_msg)
        self.assertTrue(handled)
        self.assertTrue(reason.startswith("STAGED_CARD_SENT:"))

        cand_id = reason.split(":", 1)[1]

        # Confirm transfer
        update_cq = {
            "update_id": 107,
            "callback_query": {
                "id": "cq_trf",
                "from": {"id": self.owner_id},
                "message": {"message_id": 16, "chat": {"id": self.owner_id}},
                "data": f"cfm:{cand_id}"
            }
        }
        handled_cq, reason_cq = self.router.handle_update(update_cq)
        self.assertTrue(handled_cq)
        self.assertTrue(reason_cq.startswith("CONFIRMED:"))

        # Check balances: BCA -200k (1.3M), Mandiri +200k (700k)
        conn = self.db.get_connection()
        bca_bal = conn.execute("SELECT balance FROM accounts WHERE id = ?", (self.bca.id,)).fetchone()[0]
        mandiri_bal = conn.execute("SELECT balance FROM accounts WHERE id = ?", (self.mandiri.id,)).fetchone()[0]
        self.assertEqual(bca_bal, 1300000.0)
        self.assertEqual(mandiri_bal, 700000.0)

        # Net position invariant: total liquid cash remained exactly unchanged
        total_bal = conn.execute("SELECT sum(balance) FROM accounts").fetchone()[0]
        self.assertEqual(total_bal, 2100000.0)

        # Dual transactions in ledger (transfer-out & transfer-in)
        trf_cnt = conn.execute("SELECT count(*) FROM transactions WHERE direction = 'TRANSFER'").fetchone()[0]
        self.assertEqual(trf_cnt, 2)

    def test_09_conversational_passthrough(self):
        conversational_inputs = [
            "Halo Hermes, selamat pagi",
            "Berapa sisa budget makan bulan ini?",
            "Pengeluaran terbesar minggu ini di mana?",
            "Apa kabar?",
            "Terima kasih Hermes"
        ]
        for idx, text in enumerate(conversational_inputs):
            update = {
                "update_id": 200 + idx,
                "message": {
                    "message_id": 50 + idx,
                    "chat": {"id": self.owner_id},
                    "from": {"id": self.owner_id},
                    "text": text
                }
            }
            handled, reason = self.router.handle_update(update)
            # Must NOT be handled by Finance Ingress router -> passes through to Hermes conversational queue
            self.assertFalse(handled)
            self.assertEqual(reason, "PASSTHROUGH_TO_HERMES")

    def test_10_idempotency_guard(self):
        cand = self.router.confirmation_handler.stage_input("parkir 10k cash")
        cand_id = cand.candidate_id

        update = {
            "update_id": 301,
            "callback_query": {
                "id": "cq_idemp",
                "from": {"id": self.owner_id},
                "message": {"message_id": 88, "chat": {"id": self.owner_id}},
                "data": f"cfm:{cand_id}"
            }
        }
        # First confirmation
        h1, r1 = self.router.handle_update(update)
        self.assertTrue(h1)
        self.assertTrue(r1.startswith("CONFIRMED:"))

        # Second confirmation (duplicate tap)
        h2, r2 = self.router.handle_update(update)
        self.assertTrue(h2)
        self.assertTrue(r2.startswith("CONFIRM_FAILED:"))
        self.assertIn("sudah pernah dicatat", r2)

        # Confirm only 1 transaction recorded
        conn = self.db.get_connection()
        tx_cnt = conn.execute("SELECT count(*) FROM transactions").fetchone()[0]
        self.assertEqual(tx_cnt, 1)

    def test_11_multi_owner_and_gmail_callbacks(self):
        # Configure multi-owner router
        multi_router = FinanceTelegramIngressRouter(
            engine=self.engine,
            outbound=self.outbound,
            owner_chat_id="12345678, 8263476434"
        )
        self.assertTrue(multi_router.is_owner("12345678"))
        self.assertTrue(multi_router.is_owner("8263476434"))
        self.assertTrue(multi_router.is_owner(8263476434))
        self.assertFalse(multi_router.is_owner("99999999"))

        # Create 3 review queue items
        import json
        payload1 = {
            "account_id": self.bca.id,
            "account_name": "BCA",
            "amount": 50000.0,
            "direction": "EXPENSE",
            "date": "2026-09-13",
            "note": "Makan Siang",
            "category_name": "Makanan",
            "category_id": self.cat_food.id
        }
        item_app = self.engine.enqueue_review_item(
            raw_text="Makan Siang 50k",
            parsed_result=payload1,
            confidence=0.9
        )
        item_ign = self.engine.enqueue_review_item(
            raw_text="Promo Email",
            parsed_result=payload1,
            confidence=0.5
        )
        item_edit = self.engine.enqueue_review_item(
            raw_text="Kopi 20k",
            parsed_result=payload1,
            confidence=0.8
        )

        # 1. Test Edit (gmc:) from second owner (8263476434)
        up_edit = {
            "update_id": 401,
            "callback_query": {
                "id": "cq_edit_1",
                "from": {"id": 8263476434},
                "message": {"message_id": 91, "chat": {"id": 8263476434}},
                "data": f"gmc:{item_edit.id}"
            }
        }
        h_edit, r_edit = multi_router.handle_update(up_edit)
        self.assertTrue(h_edit)
        self.assertEqual(r_edit, f"GMAIL_CHANGE_PROMPTED:{item_edit.id}")
        self.assertEqual(self.engine.get_review_queue_item(item_edit.id).status, "PENDING")

        # 2. Test Ignore (gmi:) from second owner (8263476434)
        up_ign = {
            "update_id": 402,
            "callback_query": {
                "id": "cq_ign_1",
                "from": {"id": 8263476434},
                "message": {"message_id": 92, "chat": {"id": 8263476434}},
                "data": f"gmi:{item_ign.id}"
            }
        }
        h_ign, r_ign = multi_router.handle_update(up_ign)
        self.assertTrue(h_ign)
        self.assertEqual(r_ign, "GMAIL_IGNORED")
        self.assertEqual(self.engine.get_review_queue_item(item_ign.id).status, "IGNORED")

        # 3. Test Approve (gma:) from second owner (8263476434)
        up_app = {
            "update_id": 403,
            "callback_query": {
                "id": "cq_app_1",
                "from": {"id": 8263476434},
                "message": {"message_id": 93, "chat": {"id": 8263476434}},
                "data": f"gma:{item_app.id}"
            }
        }
        h_app, r_app = multi_router.handle_update(up_app)
        self.assertTrue(h_app)
        self.assertTrue(r_app.startswith("GMAIL_CONFIRMED:"))
        self.assertEqual(self.engine.get_review_queue_item(item_app.id).status, "APPROVED")

        # Duplicate tap on Approve -> handled gracefully
        h_app2, r_app2 = multi_router.handle_update(up_app)
        self.assertTrue(h_app2)
        self.assertTrue(r_app2.startswith("GMAIL_ALREADY_APPROVED:"))

        # Unknown callback -> answered and handled, never hangs
        up_unk = {
            "update_id": 404,
            "callback_query": {
                "id": "cq_unk",
                "from": {"id": 8263476434},
                "message": {"message_id": 94, "chat": {"id": 8263476434}},
                "data": "unknown_action_xyz"
            }
        }
        h_unk, r_unk = multi_router.handle_update(up_unk)
        self.assertTrue(h_unk)
        self.assertTrue(r_unk.startswith("UNHANDLED_CALLBACK:"))

if __name__ == "__main__":
    unittest.main()
