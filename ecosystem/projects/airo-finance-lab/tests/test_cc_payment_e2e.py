import os
import sys
import json
import unittest
import threading
import socket
import time
from urllib.request import Request, urlopen

CORE_SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
WEB_SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "../web"))

sys.path.insert(0, CORE_SRC)
sys.path.insert(0, WEB_SRC)

from app import get_engine, DashboardRequestHandler
from http.server import ThreadingHTTPServer


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


class TestCCPaymentE2E(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = "/tmp/airo_cc_payment_test.db"

        if os.path.exists(cls.db):
            os.remove(cls.db)

        cls.engine = get_engine(cls.db)

        # seed account
        cls.account = cls.engine.get_account_by_name("BCA Utama")
        if cls.account is None:
            raise RuntimeError("Seed account BCA Utama not found")

        # seed credit card
        conn = cls.engine.db.get_connection()

        conn.execute(
            """
            INSERT INTO credit_cards
            (id,name,bank_name,credit_limit,current_balance,
             billing_cycle_day,payment_due_day)
            VALUES
            ('tokopedia-test',
             'Tokopedia Card',
             'BRI',
             5000000,
             1200000,
             15,
             28)
            """
        )

        conn.execute(
            """
            INSERT INTO credit_card_statements
            (id,card_id,statement_period,
             statement_date,due_date,
             total_amount,unpaid_amount,status)
            VALUES
            ('stmt-test',
             'tokopedia-test',
             '16 Agu 2026 - 15 Sep 2026',
             '2026-09-15',
             '2026-09-28',
             1200000,
             1200000,
             'ISSUED')
            """
        )

        conn.commit()

        cls.port = free_port()
        DashboardRequestHandler.engine = cls.engine

        cls.server = ThreadingHTTPServer(
            ("127.0.0.1", cls.port),
            DashboardRequestHandler
        )

        cls.thread = threading.Thread(
            target=cls.server.serve_forever,
            daemon=True
        )
        cls.thread.start()
        time.sleep(0.2)


    def test_cc_payment_route(self):

        payload = json.dumps({
            "amount": 1200000,
            "source_account_id": self.account.id,
            "payment_date": "2026-09-15",
            "note": "Bayar Tokopedia Card"
        }).encode()

        req = Request(
            f"http://127.0.0.1:{self.port}/api/credit-cards/tokopedia-card/pay-statement",
            data=payload,
            headers={"Content-Type":"application/json"},
            method="POST"
        )

        with urlopen(req) as r:
            body = json.loads(r.read())

        self.assertTrue(body["success"])

        conn = self.engine.db.get_connection()

        stmt = conn.execute(
            """
            SELECT unpaid_amount,status
            FROM credit_card_statements
            WHERE id='stmt-test'
            """
        ).fetchone()

        self.assertEqual(float(stmt["unpaid_amount"]),0)
        self.assertEqual(stmt["status"],"PAID")

        payment = conn.execute(
            """
            SELECT amount
            FROM credit_card_payments
            WHERE statement_id='stmt-test'
            """
        ).fetchone()

        self.assertIsNotNone(payment)
        self.assertEqual(float(payment["amount"]),1200000)


if __name__ == "__main__":
    unittest.main()
