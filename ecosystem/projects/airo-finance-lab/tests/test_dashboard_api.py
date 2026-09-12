import os
import sys
import json
import time
import socket
import unittest
import threading
from urllib.request import urlopen, Request

# Ensure paths
CORE_SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
WEB_SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "../web"))
for p in [CORE_SRC, WEB_SRC]:
    if p not in sys.path:
        sys.path.insert(0, p)

from app import get_engine, DashboardRequestHandler
from http.server import ThreadingHTTPServer

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]

class TestDashboardAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "test_dashboard.db"))
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)
            
        cls.port = get_free_port()
        cls.engine = get_engine(cls.test_db_path)
        DashboardRequestHandler.engine = cls.engine
        
        cls.server = ThreadingHTTPServer(('127.0.0.1', cls.port), DashboardRequestHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()
        time.sleep(0.3)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.engine.db.close()
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)

    def test_01_dashboard_html_serves_ok(self):
        url = f"http://127.0.0.1:{self.port}/"
        with urlopen(url) as res:
            self.assertEqual(res.status, 200)
            html = res.read().decode('utf-8')
            self.assertIn("AIRO Finance Lab Cockpit", html)
            self.assertIn("Catat Transaksi Manual", html)
            self.assertIn("Riwayat Mutasi Buku Besar", html)
        print("DASHBOARD_UI_TEST: PASS (HTML returned 200 with required components)")

    def test_02_get_overview_initial_state(self):
        url = f"http://127.0.0.1:{self.port}/api/overview"
        with urlopen(url) as res:
            self.assertEqual(res.status, 200)
            data = json.loads(res.read().decode('utf-8'))
            self.assertIn("accounts", data)
            self.assertIn("total_balance", data)
            self.assertIn("categories", data)
            self.assertIn("transactions", data)
            
            self.assertEqual(len(data["accounts"]), 4)
            self.assertEqual(data["total_balance"], 2350000.0)
            self.assertEqual(len(data["categories"]), 5)
            self.assertEqual(len(data["transactions"]), 0)
        print("GET_OVERVIEW_TEST: PASS (Initial balances and categories correctly seeded)")

    def test_03_create_manual_transaction(self):
        url_overview = f"http://127.0.0.1:{self.port}/api/overview"
        with urlopen(url_overview) as res:
            data = json.loads(res.read().decode('utf-8'))
            bca_acc = next(a for a in data["accounts"] if a["name"] == "BCA Utama")
            food_cat = next(c for c in data["categories"] if c["name"] == "Makanan & Minuman")

        url_post = f"http://127.0.0.1:{self.port}/api/transactions"
        payload = {
            "account_id": bca_acc["id"],
            "category_id": food_cat["id"],
            "amount": 50000.0,
            "direction": "EXPENSE",
            "note": "Makan siang Soto Ayam"
        }
        req = Request(url_post, data=json.dumps(payload).encode('utf-8'), headers={"Content-Type": "application/json"})
        with urlopen(req) as res:
            self.assertEqual(res.status, 200)
            res_data = json.loads(res.read().decode('utf-8'))
            self.assertTrue(res_data.get("success"))
            self.assertEqual(res_data["transaction"]["amount"], 50000.0)
            self.assertEqual(res_data["transaction"]["direction"], "EXPENSE")
            self.assertEqual(res_data["transaction"]["note"], "Makan siang Soto Ayam")
        print("POST_TRANSACTION_TEST: PASS (Manual transaction recorded)")

    def test_04_verify_balance_and_transaction_update(self):
        url_overview = f"http://127.0.0.1:{self.port}/api/overview"
        with urlopen(url_overview) as res:
            data = json.loads(res.read().decode('utf-8'))
            self.assertEqual(data["total_balance"], 2300000.0)
            
            bca_acc = next(a for a in data["accounts"] if a["name"] == "BCA Utama")
            self.assertEqual(bca_acc["balance"], 1450000.0)
            
            self.assertEqual(len(data["transactions"]), 1)
            tx = data["transactions"][0]
            self.assertEqual(tx["amount"], 50000.0)
            self.assertEqual(tx["direction"], "EXPENSE")
            self.assertEqual(tx["account_name"], "BCA Utama")
            self.assertEqual(tx["category_name"], "Makanan & Minuman")
            self.assertEqual(tx["note"], "Makan siang Soto Ayam")
        print("DATA_UPDATE_VERIFICATION: PASS (Balance deducted and transaction reflected in ledger)")

if __name__ == "__main__":
    unittest.main()
