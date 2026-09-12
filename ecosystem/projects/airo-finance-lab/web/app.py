import os
import sys
import json
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Ensure finance core package is discoverable
CORE_SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
if CORE_SRC not in sys.path:
    sys.path.insert(0, CORE_SRC)

from airo_finance_core import DatabaseManager, FinanceCoreEngine, FinanceInsightsService

DEFAULT_DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/airo_finance.db"))

def get_engine(db_path=DEFAULT_DB_PATH):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    db = DatabaseManager(db_path)
    db.init_schema()
    engine = FinanceCoreEngine(db)
    
    # Auto-seed initial accounts and categories if empty
    accounts = engine.db.get_connection().execute("SELECT count(*) as c FROM accounts").fetchone()["c"]
    if accounts == 0:
        engine.create_account("BCA Utama", "BANK", 1500000.0)
        engine.create_account("Blu BCA", "BANK", 500000.0)
        engine.create_account("Mandiri", "BANK", 250000.0)
        engine.create_account("Cash Dompet", "CASH", 100000.0)
        
        engine.create_category("Makanan & Minuman")
        engine.create_category("Transportasi")
        engine.create_category("Tagihan & Utilitas")
        engine.create_category("Belanja Kebutuhan")
        engine.create_category("Gaji & Pemasukan")
        
    return engine

class DashboardRequestHandler(BaseHTTPRequestHandler):
    engine = None

    def log_message(self, format, *args):
        # Clean logging
        sys.stderr.write(f"[{self.log_date_time_string()}] {self.command} {self.path} - {format % args}\n")

    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html_content, status=200):
        body = html_content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path == "/" or parsed.path == "/dashboard":
            tpl_path = os.path.join(os.path.dirname(__file__), "templates/dashboard.html")
            with open(tpl_path, "r", encoding="utf-8") as f:
                self._send_html(f.read())
            return
            
        elif parsed.path == "/api/overview":
            conn = self.engine.db.get_connection()
            
            # Accounts
            acc_cur = conn.execute("SELECT id, name, type, balance FROM accounts ORDER BY name")
            accounts = [dict(r) for r in acc_cur.fetchall()]
            total_balance = sum(a["balance"] for a in accounts)
            
            # Categories
            cat_cur = conn.execute("SELECT id, name FROM categories ORDER BY name")
            categories = [dict(r) for r in cat_cur.fetchall()]
            cat_map = {c["id"]: c["name"] for c in categories}
            acc_map = {a["id"]: a["name"] for a in accounts}
            
            # Transactions
            tx_cur = conn.execute("SELECT id, date, account_id, category_id, amount, direction, note, source, created_at FROM transactions ORDER BY created_at DESC LIMIT 50")
            transactions = []
            for r in tx_cur.fetchall():
                tx = dict(r)
                tx["account_name"] = acc_map.get(tx["account_id"], "Akun")
                tx["category_name"] = cat_map.get(tx["category_id"], "Lainnya")
                transactions.append(tx)
                
            self._send_json({
                "accounts": accounts,
                "total_balance": total_balance,
                "categories": categories,
                "transactions": transactions
            })
            return

        elif parsed.path.startswith("/api/insights/"):
            svc = FinanceInsightsService(self.engine.db)
            qs = parse_qs(parsed.query)
            year = int(qs["year"][0]) if "year" in qs and qs["year"][0].isdigit() else None
            month = int(qs["month"][0]) if "month" in qs and qs["month"][0].isdigit() else None

            if parsed.path == "/api/insights/monthly-summary":
                self._send_json(svc.get_monthly_summary(year, month).to_dict())
                return
            elif parsed.path == "/api/insights/category-spending":
                self._send_json(svc.get_category_spending(year, month).to_dict())
                return
            elif parsed.path == "/api/insights/account-overview":
                self._send_json(svc.get_account_overview().to_dict())
                return
            elif parsed.path == "/api/insights/recent-activity":
                limit = int(qs["limit"][0]) if "limit" in qs and qs["limit"][0].isdigit() else 10
                self._send_json([r.to_dict() for r in svc.get_recent_activity(limit)])
                return
            elif parsed.path == "/api/insights/anomalies":
                self._send_json([a.to_dict() for a in svc.get_spending_anomalies(year, month)])
                return
            elif parsed.path == "/api/insights/overview":
                self._send_json(svc.get_full_insights_overview(year, month))
                return
            else:
                self._send_json({"error": "Insights endpoint not found"}, status=404)
                return

        else:
            self._send_json({"error": "Not Found"}, status=404)

    def do_POST(self):
        parsed = urlparse(self.path)
        
        if parsed.path == "/api/transactions":
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length)
            try:
                payload = json.loads(raw_body.decode("utf-8"))
                amount = float(payload.get("amount", 0))
                direction = payload.get("direction", "EXPENSE")
                account_id = payload.get("account_id")
                category_id = payload.get("category_id") or None
                note = payload.get("note", "").strip() or None
                
                tx = self.engine.create_transaction(
                    account_id=account_id,
                    amount=amount,
                    direction=direction,
                    category_id=category_id,
                    note=note,
                    source="DASHBOARD"
                )
                
                self._send_json({
                    "success": True,
                    "transaction": {
                        "id": tx.id,
                        "date": tx.date,
                        "amount": tx.amount,
                        "direction": tx.direction,
                        "note": tx.note
                    }
                })
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return
            
        else:
            self._send_json({"error": "Not Found"}, status=404)

def run_server(host=None, port=8888, db_path=DEFAULT_DB_PATH):
    if host is None:
        host = os.environ.get("AIRO_FINANCE_HOST", "127.0.0.1")
    engine = get_engine(db_path)
    DashboardRequestHandler.engine = engine
    server_address = (host, port)
    httpd = ThreadingHTTPServer(server_address, DashboardRequestHandler)
    print(f"AIRO Finance Lab Dashboard running at http://{host}:{port}/")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8888
    host = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("AIRO_FINANCE_HOST", "127.0.0.1")
    run_server(host=host, port=port)
