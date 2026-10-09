import sys, json, tempfile, unittest, threading, base64
from pathlib import Path
from datetime import datetime
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from airo_finance_core import DatabaseManager, FinanceCoreEngine
from airo_finance_core import temporal as t
from airo_finance_core.temporal_recovery import collect
from airo_finance_core.intake_learning import features
from airo_finance_core.gmail_details import facts
from airo_finance_core.intake_service import IntakeService


class Temporal(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = self.tmp.name + "/db.sqlite"
        self.db = DatabaseManager(self.path)
        self.db.init_schema()
        self.e = FinanceCoreEngine(self.db)
        self.a = self.e.create_account("Bank One", "BANK", 1000000)
        self.b = self.e.create_account("Bank Two", "BANK", 1000000)
        self.clock = dict(
            occurred_at="2026-01-07T17:30:00+07:00",
            time_precision="MINUTE",
            time_accuracy="CONFIRMED",
            time_source="OWNER",
        )

    def tearDown(self):
        self.db.close()
        self.tmp.cleanup()

    def tx(self, clock=None):
        return self.e.create_transaction(
            self.a.id,
            12000,
            "EXPENSE",
            tx_date="2026-01-07",
            temporal_context=clock if clock is not None else self.clock,
        )

    def row(self, ident, table="transactions"):
        return dict(
            self.db.get_connection()
            .execute(f"SELECT * FROM {table} WHERE id=?", (ident,))
            .fetchone()
        )

    def finances(self):
        c = self.db.get_connection()
        return {
            table: [
                {k: r[k] for k in r.keys() if k not in t.FIELDS}
                for r in c.execute(f"SELECT * FROM {table}")
            ]
            for table in [
                "transactions",
                "accounts",
                "credit_cards",
                "liabilities",
                "assets",
                "credit_card_payments",
                "liability_payments",
                "asset_valuation_history",
            ]
        }

    def test_post_model_receipt_and_wib_learning(self):
        tx = self.tx()
        self.assertEqual(tx.occurred_at, "2026-01-07T10:30:00+00:00")
        self.assertEqual(t.display(self.row(tx.id)), "17:30 WIB")
        self.assertEqual(features(self.row(tx.id))["time_slot"], "DINNER")
        from airo_finance_core.gmail_reliability import receipt

        self.assertIn("17:30 WIB", receipt(self.e, tx))

    def test_estimated_excluded_from_hour_learning(self):
        d = dict(self.clock, time_accuracy="ESTIMATED")
        tx = self.tx(d)
        self.assertTrue(t.display(self.row(tx.id)).startswith("≈"))
        self.assertIsNone(features(self.row(tx.id))["time_slot"])

    def test_unknown_and_legacy_clock_not_learned(self):
        tx = self.tx({})
        self.assertIsNone(tx.occurred_at)
        self.assertEqual(tx.time_accuracy, "UNKNOWN")
        self.assertIsNone(
            features(dict(self.clock, time_accuracy="UNKNOWN"))["time_slot"]
        )

    def test_invalid_clock_rolls_back_all_finances(self):
        before = self.finances()
        with self.assertRaises(ValueError):
            self.tx(dict(self.clock, occurred_at="2026-01-08T00:01:00+07:00"))
        self.assertEqual(before, self.finances())

    def test_naive_and_invalid_precision_rejected(self):
        for clock in [
            dict(self.clock, occurred_at="2026-01-07T17:30:00"),
            dict(self.clock, time_precision="MAYBE"),
        ]:
            with self.assertRaises(ValueError):
                self.tx(clock)

    def test_transfer_metadata_atomic_preview_repeat(self):
        a, b = self.e.transfer_funds(
            self.a.id,
            self.b.id,
            10000,
            tx_date="2026-01-07",
            temporal_context=self.clock,
        )
        before = self.finances()
        new = dict(
            self.clock,
            occurred_at="2026-01-07T18:15:00+07:00",
            time_accuracy="ESTIMATED",
        )
        p = t.preview(self.db, [dict(id=a.id, temporal=new)])
        self.assertEqual(len(p["items"]), 2)
        t.apply(self.db, p["id"])
        t.apply(self.db, p["id"])
        self.assertEqual(before, self.finances())
        self.assertEqual(self.row(a.id)["occurred_at"], self.row(b.id)["occurred_at"])
        self.assertEqual(
            self.db.get_connection()
            .execute("SELECT count(*) FROM temporal_audit")
            .fetchone()[0],
            2,
        )

    def test_stale_preview_detects_financial_change(self):
        tx = self.tx()
        p = t.preview(
            self.db,
            [dict(id=tx.id, temporal=dict(self.clock, time_accuracy="ESTIMATED"))],
        )
        self.e.correct_transaction(tx.id, note="New owner detail")
        with self.assertRaises(ValueError):
            t.apply(self.db, p["id"])
        self.assertEqual(self.row(tx.id)["time_accuracy"], "CONFIRMED")

    def test_partial_groups_and_restart_resume(self):
        a = self.tx()
        b = self.tx()
        p = t.preview(
            self.db,
            [
                dict(id=a.id, temporal=dict(self.clock, time_accuracy="ESTIMATED")),
                dict(
                    id=b.id,
                    temporal=dict(
                        occurred_at=None, time_accuracy="UNKNOWN", time_precision="DATE"
                    ),
                ),
            ],
        )
        result = t.apply(self.db, p["id"], ["estimated"])
        self.assertEqual(result["status"], "PARTIAL")
        self.db.close()
        self.db = DatabaseManager(self.path)
        self.db.init_schema()
        self.e = FinanceCoreEngine(self.db)
        result = t.apply(self.db, p["id"], ["unknown"])
        self.assertEqual(result["status"], "APPLIED")

    def test_midnight_wib_and_web_clock_defaults(self):
        d = t.normalize(
            dict(self.clock, occurred_at="2026-01-06T17:01:00+00:00"), "2026-01-07"
        )
        self.assertIn("00:01", t.display(d))
        with self.assertRaises(ValueError):
            t.web_context({"date": "2020-01-01", "temporal": {"mode": "NOW"}})
        self.assertIsNone(
            t.web_context({"date": "2020-01-01", "temporal": {"mode": "UNKNOWN"}})[
                "occurred_at"
            ]
        )
        self.assertEqual(
            t.web_context(
                {
                    "date": "2020-01-01",
                    "temporal": {
                        "mode": "INPUT",
                        "clock": "17:30:12",
                        "time_accuracy": "ESTIMATED",
                    },
                }
            )["time_precision"],
            "SECOND",
        )

    def test_credit_payment_linked_ledger_preview(self):
        cc = self.e.create_credit_card("Card One", "Issuer", 1000000)
        with self.db.atomic():
            self.db.get_connection().execute(
                "UPDATE credit_cards SET current_balance=100000 WHERE id=?", (cc.id,)
            )
        pmt = self.e.record_credit_card_payment(
            cc.id,
            "2026-01-07",
            10000,
            account_id=self.a.id,
            temporal_context=self.clock,
        )
        self.assertEqual(
            self.row(pmt.id, "credit_card_payments")["occurred_at"],
            self.row(pmt.transaction_id)["occurred_at"],
        )
        p = t.preview(
            self.db,
            [
                dict(
                    entity="credit_card_payments",
                    id=pmt.id,
                    temporal=dict(self.clock, time_accuracy="ESTIMATED"),
                )
            ],
        )
        before = self.finances()
        t.apply(self.db, p["id"])
        self.assertEqual(before, self.finances())
        self.assertEqual(len(p["items"]), 2)

    def test_loan_payment_and_asset_events(self):
        liab = self.e.create_liability(
            "Loan", "PERSONAL_LOAN", 100000, 100000, 10000, 10
        )
        pmt = self.e.record_liability_payment(
            liab.id,
            "2026-01-07",
            10000,
            source_account_id=self.a.id,
            temporal_context=self.clock,
        )
        self.assertEqual(pmt.occurred_at, self.row(pmt.transaction_id)["occurred_at"])
        asset = self.e.create_asset("Asset One", "OTHER", 0)
        self.e.record_asset_purchase(
            self.a.id,
            asset.id,
            10000,
            tx_date="2026-01-07",
            temporal_context=self.clock,
        )
        value = self.e.record_asset_valuation(
            asset.id, "2026-01-07", value=11000, temporal_context={}
        )
        self.assertIsNone(value.occurred_at)
        self.assertEqual(value.time_accuracy, "UNKNOWN")
        self.assertEqual(
            next(
                v for v in self.e.list_asset_valuations(asset.id) if v.id == value.id
            ).time_accuracy,
            "UNKNOWN",
        )
        self.assertEqual(
            self.e.list_liability_payments(liab.id)[0].time_accuracy, "CONFIRMED"
        )

    def test_group_split_keeps_funding_clock_independent(self):
        s = IntakeService(self.e)
        data = dict(
            amount=24000,
            account_id=self.a.id,
            direction="EXPENSE",
            date="2026-01-07",
            **self.clock,
            lines=[
                dict(amount=12000, note="Food", category_id=None),
                dict(amount=12000, note="Other", category_id=None),
            ],
        )
        batch = s.create("1", "test-group", "mock", items=[data])
        item = s.rows(batch)[0]
        a = self.tx()
        b = self.tx()
        fund = self.tx(dict(self.clock, occurred_at="2026-01-07T09:00:00+07:00"))
        with self.db.atomic():
            for tx, role in [(a, "POSTING"), (b, "POSTING"), (fund, "FUNDING")]:
                self.db.get_connection().execute(
                    "INSERT INTO intake_transactions VALUES (?,?,?)",
                    (item["id"], tx.id, role),
                )
        p = t.preview(
            self.db,
            [dict(id=a.id, temporal=dict(self.clock, time_accuracy="ESTIMATED"))],
        )
        self.assertEqual(len(p["items"]), 2)
        t.apply(self.db, p["id"])
        self.assertEqual(self.row(fund.id)["time_accuracy"], "CONFIRMED")

    def test_recovery_never_posts_or_applies(self):
        tx = self.tx({})
        before = self.finances()
        p = collect(self.db)
        self.assertTrue(p["items"])
        self.assertEqual(p["status"], "PREVIEW")
        self.assertEqual(before, self.finances())
        self.assertIsNone(self.row(tx.id)["occurred_at"])

    def test_bank_multiple_clocks_and_full_year(self):
        exact = facts("Tanggal transaksi: 7 Januari 2026 jam 17:30 WIB")
        # Supported bank month formats include English/Indonesian numeric or abbreviated names.
        exact = facts("Tanggal transaksi: 07/01/2026 17:30:22 WIB")
        self.assertEqual(exact["time_accuracy"], "CONFIRMED")
        self.assertEqual(exact["time_precision"], "SECOND")
        self.assertNotIn("occurred_at", facts("7 Januari jam 17:30 WIB"))
        self.assertEqual(
            facts(
                "Tanggal transaksi 07/01/2026 17:30 WIB; tanggal transaksi 07/01/2026 18:00 WIB"
            ).get("temporal_issue"),
            "MULTIPLE_BANK_TIMES",
        )

    def test_source_clocks_never_replace_event_clock(self):
        tx = self.tx(
            dict(
                source_sent_at="2026-01-08T09:00:00+07:00",
                source_received_at="2026-01-08T09:01:00+07:00",
            )
        )
        self.assertIsNone(tx.occurred_at)
        self.assertEqual(tx.time_accuracy, "UNKNOWN")

    def test_preview_atomic_failure_does_not_partially_apply(self):
        a = self.tx()
        b = self.tx()
        p = t.preview(
            self.db,
            [
                dict(id=x.id, temporal=dict(self.clock, time_accuracy="ESTIMATED"))
                for x in [a, b]
            ],
        )
        original = t.write
        calls = []

        def fail(c, table, ident, d, event_date=None):
            calls.append(ident)
            if len(calls) == 2:
                raise RuntimeError("mock write failure")
            return original(c, table, ident, d, event_date)

        with patch.object(t, "write", side_effect=fail):
            with self.assertRaises(RuntimeError):
                t.apply(self.db, p["id"])
        self.assertEqual(self.row(a.id)["time_accuracy"], "CONFIRMED")
        self.assertEqual(t.get_preview(self.db, p["id"])["status"], "PREVIEW")

    def test_telegram_preview_repeat_click_and_source_clock(self):
        from airo_finance_core.telegram_ingress import (
            FinanceTelegramIngressRouter,
            TelegramOutboundAdapter,
        )

        calls = []
        out = TelegramOutboundAdapter(
            "mock",
            lambda method, payload: calls.append((method, payload))
            or {"ok": True, "result": {"message_id": len(calls)}},
        )
        router = FinanceTelegramIngressRouter(
            self.e, out, "1", auto_register_commands=False
        )
        tx = self.tx()
        before = self.finances()
        upd = {
            "message": {
                "from": {"id": 1},
                "chat": {"id": 1},
                "message_id": 8,
                "date": 1791340000,
                "text": f"ubah jam transaksi {tx.id} jadi 18.05 perkiraan",
            }
        }
        self.assertEqual(router.handle_update(upd)[1], "TEMPORAL_PREVIEW")
        p = (
            self.db.get_connection()
            .execute("SELECT id FROM temporal_proposals")
            .fetchone()[0]
        )
        self.assertEqual(self.row(tx.id)["time_accuracy"], "CONFIRMED")
        callback = {
            "callback_query": {
                "id": "mock",
                "from": {"id": 1},
                "data": "tm:apply:" + p,
                "message": {"chat": {"id": 1}, "message_id": 9, "date": 1791340000},
            }
        }
        self.assertEqual(router.handle_update(callback)[1], "TEMPORAL_APPLIED")
        router.handle_update(callback)
        self.assertEqual(before, self.finances())
        self.assertEqual(self.row(tx.id)["time_accuracy"], "ESTIMATED")
        callback["callback_query"]["from"]["id"] = 2
        self.assertEqual(
            router.handle_update(callback)[1], "BLOCKED_NON_OWNER_CALLBACK"
        )
        source = (
            self.db.get_connection()
            .execute("SELECT * FROM temporal_sources")
            .fetchone()
        )
        self.assertEqual(source["source_id"], "telegram:1:8")

    def test_legacy_candidate_retains_original_source_after_confirmation(self):
        # Candidate source capture is orthogonal to its category parser.
        from airo_finance_core.temporal import capture_candidate

        class Stub:
            @capture_candidate
            def parse(self):
                class Candidate:
                    pass

                return Candidate()

        with t.context(
            {"source_sent_at": "2026-01-07T10:00:00+00:00", "source_id": "telegram:1:5"}
        ):
            candidate = Stub().parse()
        with t.context({"source_sent_at": "2026-01-08T10:00:00+00:00"}):
            self.assertEqual(
                candidate.temporal["source_sent_at"], "2026-01-07T10:00:00+00:00"
            )

    def test_email_received_clock_is_not_sent_clock(self):
        values = t.normalize(
            dict(
                message_at="2026-01-07T10:00:00+00:00",
                source_received_at="2026-01-07T10:00:00+00:00",
                source_id="gmail:mock",
            )
        )
        self.assertIsNone(values["source_sent_at"])
        self.assertEqual(values["source_received_at"], "2026-01-07T10:00:00+00:00")

    def test_batch_card_payment_preserves_clock_on_payment_model(self):
        cc = self.e.create_credit_card("Fixture Card", "Issuer", 1000000)
        with self.db.atomic():
            self.db.get_connection().execute(
                "UPDATE credit_cards SET current_balance=100000 WHERE id=?", (cc.id,)
            )
        s = IntakeService(self.e)
        batch = s.create(
            "1",
            "batch-clock",
            "mock",
            items=[
                dict(
                    account_id=self.a.id,
                    credit_card_id=cc.id,
                    amount=12000,
                    direction="CC_PAYMENT",
                    date="2026-01-07",
                    note="Payment",
                    facts_confirmed=True,
                    **self.clock,
                )
            ],
        )
        result = s.commit(batch, "1", confirm_suggestions=True)
        self.assertEqual(len(result["new_transactions"]), 1)
        pmt = (
            self.db.get_connection()
            .execute("SELECT * FROM credit_card_payments")
            .fetchone()
        )
        self.assertEqual(pmt["time_accuracy"], "CONFIRMED")
        self.assertEqual(
            pmt["occurred_at"], self.row(pmt["transaction_id"])["occurred_at"]
        )

    def test_shared_clock_header_has_estimated_quality_before_posting(self):
        e = self.e
        cat = e.create_category("Makanan & Minuman")
        e.create_subcategory(cat.id, "Makan Siang")
        s = IntakeService(e)
        text = "semua tanggal 7 Januari 2026 jam 17.30\nBank One bayar 12rb makan siang\nBank Two bayar 13rb makan siang"
        b = s.create("1", "shared-clock-quality", text)
        self.assertEqual({r["data"]["time_accuracy"] for r in s.rows(b)}, {"ESTIMATED"})
        result = s.commit(b, "1", confirm_suggestions=True)
        self.assertEqual(len(result["new_transactions"]), 2)

    def test_export_immediate_chat_clock_is_estimate_and_delayed_chat_source_only(self):
        from datetime import timezone

        tx = self.tx({})
        raw = "Bank One bayar 12rb makan siang"
        self.e.record_transaction_metadata(tx.id, raw_input=raw, source_type="TELEGRAM")
        stamp = int(datetime(2026, 1, 7, 12, 5, 32, tzinfo=t.WIB).timestamp())
        exported = {
            "id": 999,
            "messages": [
                {
                    "id": 1,
                    "from_id": "user1",
                    "type": "message",
                    "date_unixtime": str(stamp),
                    "text": raw,
                }
            ],
        }
        p = collect(self.db, telegram_export=exported, expected_telegram_owner="1")
        after = next(i["after"] for i in p["items"] if i["entity_id"] == tx.id)
        self.assertEqual(after["time_accuracy"], "ESTIMATED")
        self.assertEqual(t.display(after), "≈12:05:32 WIB")
        self.assertIsNone(self.row(tx.id)["occurred_at"])
        exported["messages"][0]["date_unixtime"] = str(stamp + 86400)
        p = collect(self.db, telegram_export=exported, expected_telegram_owner="1")
        after = next(i["after"] for i in p["items"] if i["entity_id"] == tx.id)
        self.assertIsNone(after["occurred_at"])
        self.assertIsNotNone(after["source_sent_at"])
        exported["messages"].append(dict(exported["messages"][0], id=2))
        p = collect(self.db, telegram_export=exported, expected_telegram_owner="1")
        after = next(i["after"] for i in p["items"] if i["entity_id"] == tx.id)
        self.assertIsNone(after["source_sent_at"])

    def test_domain_insights_preserve_event_and_source_metadata(self):
        from airo_finance_core.insights import FinanceInsightsService

        liab = self.e.create_liability(
            "Fixture Mortgage", "MORTGAGE", 100000, 100000, 10000, 10
        )
        payment = self.e.record_liability_payment(
            liab.id, "2026-01-07", 10000, temporal_context=self.clock
        )
        gold = self.e.create_asset(
            "Fixture Emas", "GOLD", 10000, asset_class="GOLD", weight_grams=1
        )
        valuation = self.e.record_asset_valuation(
            gold.id, "2026-01-07", value=11000, temporal_context=self.clock
        )
        service = FinanceInsightsService(self.db)

        def records(value):
            if isinstance(value, dict):
                yield value
                for v in value.values():
                    yield from records(v)
            elif isinstance(value, list):
                for v in value:
                    yield from records(v)

        debt_records = list(records(service.get_liabilities_summary()))
        p = next(x for x in debt_records if x.get("id") == payment.id)
        self.assertEqual(p["time_accuracy"], "CONFIRMED")
        asset_records = list(records(service.get_assets_summary()))
        v = next(x for x in asset_records if x.get("id") == valuation.id)
        self.assertEqual(v["time_accuracy"], "CONFIRMED")


if __name__ == "__main__":
    unittest.main()
