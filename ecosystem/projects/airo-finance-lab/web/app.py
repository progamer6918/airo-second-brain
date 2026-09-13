import os
import sys
import json
import csv
import io
from datetime import datetime, date, timezone
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Ensure finance core package is discoverable
CORE_SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
if CORE_SRC not in sys.path:
    sys.path.insert(0, CORE_SRC)

from airo_finance_core import DatabaseManager, FinanceCoreEngine, FinanceInsightsService, GmailIntelligenceService

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
        
        engine.create_category("Makanan & Minuman", "makan, minum, kopi, resto, cafe")
        engine.create_category("Transportasi", "bensin, bbm, gojek, grab, toll, parkir")
        engine.create_category("Tagihan & Utilitas", "listrik, pln, wifi, indihome, pulsa")
        engine.create_category("Belanja Kebutuhan", "belanja, supermarket, indomaret, alfamart")
        engine.create_category("Gaji & Pemasukan", "gaji, payroll, transfer masuk, bonus")
        
    return engine

class DashboardRequestHandler(BaseHTTPRequestHandler):
    engine = None

    def log_message(self, format, *args):
        # Clean logging
        sys.stderr.write(f"[{self.log_date_time_string()}] {self.command} {self.path} - {format % args}\n")

    def _get_cookie(self, name: str):
        cookie_header = self.headers.get("Cookie", "")
        for part in cookie_header.split(";"):
            part = part.strip()
            if "=" in part:
                k, v = part.split("=", 1)
                if k.strip() == name:
                    return v.strip()
        return None

    def _send_json(self, data, status=200, set_cookies=None):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        if set_cookies:
            for c in set_cookies:
                self.send_header("Set-Cookie", c)
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html_content, status=200, set_cookies=None):
        body = html_content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        if set_cookies:
            for c in set_cookies:
                self.send_header("Set-Cookie", c)
        self.end_headers()
        self.wfile.write(body)

    def _send_csv(self, csv_content, filename="airo_finance_export.csv"):
        body = csv_content.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/csv; charset=utf-8")
        self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length <= 0:
            return {}
        raw_body = self.rfile.read(content_length)
        return json.loads(raw_body.decode("utf-8"))

    # ====================================================
    # GET Handlers
    # ====================================================
    def do_GET(self):
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)

        if parsed.path == "/" or parsed.path == "/dashboard":
            tpl_path = os.path.join(os.path.dirname(__file__), "templates/dashboard.html")
            with open(tpl_path, "r", encoding="utf-8") as f:
                content = f.read()
            token = self._get_cookie("airo_session_token")
            session = self.engine.verify_owner_session(token) if token else None
            set_cookies = None
            if not session:
                _, raw_token = self.engine.create_owner_session(device_name="Owner Browser Auto", expires_in_days=30)
                set_cookies = [f"airo_session_token={raw_token}; Path=/; Max-Age={30*86400}; HttpOnly; SameSite=Lax"]
            self._send_html(content, set_cookies=set_cookies)
            return

        elif parsed.path == "/api/auth/session":
            token = self._get_cookie("airo_session_token")
            session = self.engine.verify_owner_session(token) if token else None
            if session:
                self._send_json({
                    "authenticated": True,
                    "session": {
                        "id": session.id,
                        "device_name": session.device_name,
                        "created_at": session.created_at,
                        "expires_at": session.expires_at,
                        "last_used_at": session.last_used_at
                    }
                })
            else:
                self._send_json({"authenticated": False, "session": None})
            return

        elif parsed.path == "/api/overview":
            conn = self.engine.db.get_connection()
            svc = FinanceInsightsService(self.engine.db)
            
            # Accounts
            accounts = [
                {"id": a.id, "name": a.name, "type": a.type, "balance": a.balance, "is_active": a.is_active}
                for a in self.engine.list_accounts(active_only=False)
            ]
            total_balance = sum(a["balance"] for a in accounts if a["is_active"] == 1)
            
            # Categories
            categories = [
                {"id": c.id, "name": c.name, "keywords": c.keywords, "is_active": c.is_active}
                for c in self.engine.list_categories(active_only=False)
            ]

            # Subcategories
            subcategories = [
                {"id": s.id, "category_id": s.category_id, "name": s.name, "display_order": s.display_order, "is_active": s.is_active}
                for s in self.engine.list_subcategories(active_only=False)
            ]

            # Obligations
            obligations = [
                {"id": o.id, "name": o.name, "amount": o.amount, "due_day": o.due_day, "category_id": o.category_id, "is_active": o.is_active}
                for o in self.engine.list_fixed_obligations(active_only=False)
            ]

            # Credit cards
            cc_summary = svc.get_credit_card_summary()
            credit_cards = cc_summary.get("cards", [])

            # Aliases
            aliases = [
                {"id": al.id, "keyword": al.keyword, "category_id": al.category_id, "subcategory_id": al.subcategory_id}
                for al in self.engine.list_category_aliases()
            ]

            cat_map = {c["id"]: c["name"] for c in categories}
            subcat_map = {s["id"]: s["name"] for s in subcategories}
            acc_map = {a["id"]: a["name"] for a in accounts}
            
            # Transactions with Running Balance
            rb_map = self.engine.calculate_running_balances()
            tx_cur = conn.execute("SELECT * FROM transactions ORDER BY date DESC, created_at DESC, id DESC LIMIT 500")
            transactions = []
            for r in tx_cur.fetchall():
                tx = dict(r)
                tx["account_name"] = acc_map.get(tx.get("account_id"), "Akun")
                tx["category_name"] = cat_map.get(tx.get("category_id"), "Lainnya")
                sub_id = tx.get("subcategory_id")
                tx["subcategory_name"] = subcat_map.get(sub_id, "Belum diisi") if sub_id else "Belum diisi"
                if "status" not in tx or not tx["status"]:
                    tx["status"] = "ACTIVE"
                tx["running_balance"] = rb_map.get(tx["id"])
                transactions.append(tx)
                
            safe_to_spend = svc.get_safe_to_spend_report().to_dict()
            weekly_recap = svc.get_weekly_recap_report().to_dict()
            net_worth = svc.get_net_worth_report().to_dict()
            assets_summary = svc.get_assets_summary()
            assets = assets_summary.get("assets", [])
            liabilities_summary = svc.get_liabilities_summary()
            liabilities = liabilities_summary.get("liabilities", [])
            configs = self.engine.get_all_config()
                
            self._send_json({
                "accounts": accounts,
                "total_balance": total_balance,
                "categories": categories,
                "subcategories": subcategories,
                "obligations": obligations,
                "credit_cards": credit_cards,
                "aliases": aliases,
                "transactions": transactions,
                "transactions_complete": True,
                "safe_to_spend": safe_to_spend,
                "weekly_recap": weekly_recap,
                "net_worth": net_worth,
                "assets": assets,
                "liabilities": liabilities,
                "config": configs
            })
            return

        elif parsed.path == "/api/accounts":
            active_only = qs.get("active_only", ["0"])[0] in ("1", "true", "True")
            accounts = [
                {"id": a.id, "name": a.name, "type": a.type, "balance": a.balance, "is_active": a.is_active}
                for a in self.engine.list_accounts(active_only=active_only)
            ]
            self._send_json({"accounts": accounts})
            return

        elif parsed.path == "/api/categories":
            active_only = qs.get("active_only", ["0"])[0] in ("1", "true", "True")
            categories = [
                {"id": c.id, "name": c.name, "keywords": c.keywords, "is_active": c.is_active}
                for c in self.engine.list_categories(active_only=active_only)
            ]
            self._send_json({"categories": categories})
            return

        elif parsed.path == "/api/subcategories":
            cat_id = qs.get("category_id", [None])[0]
            active_only = qs.get("active_only", ["0"])[0] in ("1", "true", "True")
            subcats = [
                {"id": s.id, "category_id": s.category_id, "name": s.name, "display_order": s.display_order, "is_active": s.is_active, "created_at": s.created_at}
                for s in self.engine.list_subcategories(category_id=cat_id, active_only=active_only)
            ]
            self._send_json({"subcategories": subcats})
            return

        elif parsed.path == "/api/category-aliases":
            cat_id = qs.get("category_id", [None])[0]
            subcat_id = qs.get("subcategory_id", [None])[0]
            aliases = [
                {"id": a.id, "keyword": a.keyword, "subcategory_id": a.subcategory_id, "category_id": a.category_id, "priority": a.priority, "created_at": a.created_at}
                for a in self.engine.list_category_aliases(category_id=cat_id, subcategory_id=subcat_id)
            ]
            self._send_json({"aliases": aliases})
            return

        elif parsed.path == "/api/review-queue":
            status = qs.get("status", [None])[0]
            items = [
                {"id": i.id, "raw_text": i.raw_text, "parsed_result": json.loads(i.parsed_result), "confidence": i.confidence, "issue_reason": i.issue_reason, "status": i.status, "approved_transaction_id": i.approved_transaction_id, "created_at": i.created_at, "updated_at": i.updated_at}
                for i in self.engine.list_review_queue(status=status)
            ]
            self._send_json({"review_queue": items})
            return

        elif parsed.path == "/api/credit-cards":
            svc = FinanceInsightsService(self.engine.db)
            self._send_json(svc.get_credit_card_summary())
            return

        elif parsed.path == "/api/credit-cards/statements":
            card_id = qs.get("card_id", [None])[0]
            stmts = [
                {"id": s.id, "card_id": s.card_id, "statement_period": s.statement_period, "statement_date": s.statement_date, "due_date": s.due_date, "total_amount": s.total_amount, "minimum_payment": s.minimum_payment, "unpaid_amount": s.unpaid_amount, "status": s.status, "created_at": s.created_at, "updated_at": s.updated_at}
                for s in self.engine.list_credit_card_statements(card_id=card_id)
            ]
            self._send_json({"statements": stmts})
            return

        elif parsed.path == "/api/credit-cards/payments":
            card_id = qs.get("card_id", [None])[0]
            pmts = [
                {"id": p.id, "card_id": p.card_id, "statement_id": p.statement_id, "transaction_id": p.transaction_id, "payment_date": p.payment_date, "amount": p.amount, "notes": p.notes, "created_at": p.created_at}
                for p in self.engine.list_credit_card_payments(card_id=card_id)
            ]
            self._send_json({"payments": pmts})
            return

        elif parsed.path == "/api/assets":
            svc = FinanceInsightsService(self.engine.db)
            self._send_json(svc.get_assets_summary())
            return

        elif parsed.path == "/api/liabilities":
            svc = FinanceInsightsService(self.engine.db)
            self._send_json(svc.get_liabilities_summary())
            return

        elif parsed.path == "/api/obligations":
            active_only = qs.get("active_only", ["0"])[0] in ("1", "true", "True")
            conn = self.engine.db.get_connection()
            cat_cur = conn.execute("SELECT id, name FROM categories")
            cat_map = {r["id"]: r["name"] for r in cat_cur.fetchall()}
            obligations = self.engine.list_fixed_obligations(active_only=active_only)
            obl_list = []
            for o in obligations:
                obl_list.append({
                    "id": o.id,
                    "name": o.name,
                    "amount": o.amount,
                    "due_day": o.due_day,
                    "category_id": o.category_id,
                    "category_name": cat_map.get(o.category_id, "Umum"),
                    "is_active": o.is_active,
                    "created_at": o.created_at,
                    "updated_at": o.updated_at
                })
            self._send_json({"obligations": obl_list})
            return

        elif parsed.path == "/api/config":
            configs = self.engine.get_all_config()
            self._send_json({"config": configs})
            return

        elif parsed.path == "/api/export/csv":
            conn = self.engine.db.get_connection()
            acc_cur = conn.execute("SELECT id, name FROM accounts")
            acc_map = {r["id"]: r["name"] for r in acc_cur.fetchall()}
            cat_cur = conn.execute("SELECT id, name FROM categories")
            cat_map = {r["id"]: r["name"] for r in cat_cur.fetchall()}

            cur = conn.execute(
                "SELECT id, date, account_id, category_id, amount, direction, note, source, created_at "
                "FROM transactions ORDER BY date DESC, created_at DESC"
            )
            rows = cur.fetchall()

            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["id", "date", "direction", "amount", "account", "category", "note", "source", "created_at"])
            for r in rows:
                writer.writerow([
                    r["id"],
                    r["date"],
                    r["direction"],
                    r["amount"],
                    acc_map.get(r["account_id"], ""),
                    cat_map.get(r["category_id"], ""),
                    r["note"] or "",
                    r["source"] or "",
                    r["created_at"] or ""
                ])
            self._send_csv(output.getvalue(), "airo_finance_export.csv")
            return

        elif parsed.path.startswith("/api/insights/"):
            svc = FinanceInsightsService(self.engine.db)
            year = int(qs["year"][0]) if "year" in qs and qs["year"][0].isdigit() else None
            month = int(qs["month"][0]) if "month" in qs and qs["month"][0].isdigit() else None

            if parsed.path == "/api/insights/net-worth":
                as_of = qs.get("as_of", [None])[0]
                self._send_json(svc.get_net_worth_report(as_of).to_dict())
                return
            elif parsed.path == "/api/insights/monthly-summary":
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
            elif parsed.path == "/api/insights/safe-to-spend":
                as_of = qs.get("as_of", [None])[0]
                self._send_json(svc.get_safe_to_spend_report(as_of).to_dict())
                return
            elif parsed.path == "/api/insights/weekly-recap":
                as_of = qs.get("as_of", [None])[0]
                self._send_json(svc.get_weekly_recap_report(as_of).to_dict())
                return
            elif parsed.path == "/api/insights/spending-by-subcategory":
                period = qs.get("period", [None])[0]
                self._send_json(svc.get_spending_by_subcategory(period))
                return
            elif parsed.path == "/api/insights/credit-cards":
                self._send_json(svc.get_credit_card_summary())
                return
            elif parsed.path == "/api/insights/financial-position":
                as_of = qs.get("as_of", [None])[0]
                self._send_json(svc.get_financial_position(as_of))
                return
            elif parsed.path == "/api/insights/overview":
                self._send_json(svc.get_full_insights_overview(year, month))
                return
            elif parsed.path == "/api/insights/cashflow-trend":
                p = qs.get("period", [None])[0]
                s_d = qs.get("start_date", [None])[0]
                e_d = qs.get("end_date", [None])[0]
                self._send_json(svc.get_cashflow_trend(p, s_d, e_d))
                return
            else:
                self._send_json({"error": "Insights endpoint not found"}, status=404)
                return

        elif parsed.path == "/api/gmail/review-queue":
            status = qs.get("status", ["PENDING"])[0]
            items = [
                {
                    "id": i.id,
                    "raw_text": i.raw_text,
                    "parsed_result": json.loads(i.parsed_result) if isinstance(i.parsed_result, str) else i.parsed_result,
                    "confidence": i.confidence,
                    "issue_reason": i.issue_reason,
                    "status": i.status,
                    "created_at": i.created_at
                }
                for i in self.engine.list_review_queue(status=status)
            ]
            self._send_json({"review_queue": items})
            return

        elif parsed.path == "/api/gmail/inbox":
            inbox_data = self.engine.get_finance_inbox()
            self._send_json({"success": True, "inbox": inbox_data})
            return

        else:
            self._send_json({"error": "Not Found"}, status=404)

    # ====================================================
    # POST Handlers
    # ====================================================
    def do_POST(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/auth/login":
            try:
                payload = self._read_json_body()
                device_name = payload.get("device_name", "Owner Browser").strip() or "Owner Browser"
                session, raw_token = self.engine.create_owner_session(device_name=device_name, expires_in_days=30)
                cookie_str = f"airo_session_token={raw_token}; Path=/; Max-Age={30*86400}; HttpOnly; SameSite=Lax"
                self._send_json({
                    "success": True,
                    "token": raw_token,
                    "session": {
                        "id": session.id,
                        "device_name": session.device_name,
                        "created_at": session.created_at,
                        "expires_at": session.expires_at
                    }
                }, set_cookies=[cookie_str])
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        elif parsed.path == "/api/auth/logout":
            token = self._get_cookie("airo_session_token")
            if token:
                self.engine.revoke_owner_session(token)
            clear_cookie = "airo_session_token=; Path=/; Max-Age=0; HttpOnly; SameSite=Lax"
            self._send_json({"success": True}, set_cookies=[clear_cookie])
            return

        elif parsed.path == "/api/auth/logout-all":
            count = self.engine.revoke_all_owner_sessions()
            clear_cookie = "airo_session_token=; Path=/; Max-Age=0; HttpOnly; SameSite=Lax"
            self._send_json({"success": True, "revoked_count": count}, set_cookies=[clear_cookie])
            return

        elif parsed.path == "/api/transactions":
            try:
                payload = self._read_json_body()
                amount = float(payload.get("amount", 0))
                direction = payload.get("direction", "EXPENSE")
                account_id = payload.get("account_id")
                category_id = payload.get("category_id") or None
                subcategory_id = payload.get("subcategory_id") or None
                note = payload.get("note", "").strip() or None
                
                tx = self.engine.create_transaction(
                    account_id=account_id,
                    amount=amount,
                    direction=direction,
                    category_id=category_id,
                    subcategory_id=subcategory_id,
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
                        "account_id": tx.account_id,
                        "category_id": tx.category_id,
                        "subcategory_id": tx.subcategory_id,
                        "note": tx.note,
                        "status": tx.status
                    }
                })
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        elif parsed.path == "/api/accounts":
            try:
                payload = self._read_json_body()
                name = payload.get("name", "").strip()
                account_type = payload.get("type", "BANK").strip()
                initial_balance = float(payload.get("initial_balance", 0.0))
                acc = self.engine.create_account(name=name, account_type=account_type, initial_balance=initial_balance)
                self._send_json({
                    "success": True,
                    "account": {
                        "id": acc.id,
                        "name": acc.name,
                        "type": acc.type,
                        "balance": acc.balance,
                        "is_active": acc.is_active
                    }
                })
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        elif parsed.path == "/api/categories":
            try:
                payload = self._read_json_body()
                name = payload.get("name", "").strip()
                keywords = payload.get("keywords", "").strip()
                cat = self.engine.create_category(name=name, keywords=keywords)
                self._send_json({
                    "success": True,
                    "category": {
                        "id": cat.id,
                        "name": cat.name,
                        "keywords": cat.keywords,
                        "is_active": cat.is_active
                    }
                })
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        elif parsed.path == "/api/assets":
            try:
                payload = self._read_json_body()
                name = payload.get("name", "").strip()
                asset_type = payload.get("type", "OTHER").strip()
                current_value = float(payload.get("current_value", 0.0))
                notes = payload.get("notes", "").strip() or None
                ast = self.engine.create_asset(
                    name=name,
                    asset_type=asset_type,
                    current_value=current_value,
                    notes=notes
                )
                self._send_json({
                    "success": True,
                    "asset": {
                        "id": ast.id,
                        "name": ast.name,
                        "type": ast.type,
                        "current_value": ast.current_value,
                        "notes": ast.notes,
                        "is_active": ast.is_active
                    }
                })
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        elif parsed.path == "/api/liabilities":
            try:
                payload = self._read_json_body()
                name = payload.get("name", "").strip()
                liability_type = payload.get("type", "OTHER").strip()
                original_amount = float(payload.get("original_amount", 0.0))
                remaining_amount = float(payload.get("remaining_amount", original_amount))
                monthly_payment = float(payload.get("monthly_payment", 0.0))
                due_day = int(payload.get("due_day", 1))
                notes = payload.get("notes", "").strip() or None
                liab = self.engine.create_liability(
                    name=name,
                    liability_type=liability_type,
                    original_amount=original_amount,
                    remaining_amount=remaining_amount,
                    monthly_payment=monthly_payment,
                    due_day=due_day,
                    notes=notes
                )
                self._send_json({
                    "success": True,
                    "liability": {
                        "id": liab.id,
                        "name": liab.name,
                        "type": liab.type,
                        "original_amount": liab.original_amount,
                        "remaining_amount": liab.remaining_amount,
                        "monthly_payment": liab.monthly_payment,
                        "due_day": liab.due_day,
                        "notes": liab.notes,
                        "is_active": liab.is_active
                    }
                })
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        elif parsed.path == "/api/obligations":
            try:
                payload = self._read_json_body()
                name = payload.get("name", "").strip()
                amount = float(payload.get("amount", 0))
                due_day = int(payload.get("due_day", 1))
                category_id = payload.get("category_id") or None
                
                obl = self.engine.create_fixed_obligation(
                    name=name,
                    amount=amount,
                    due_day=due_day,
                    category_id=category_id
                )
                self._send_json({
                    "success": True,
                    "obligation": {
                        "id": obl.id,
                        "name": obl.name,
                        "amount": obl.amount,
                        "due_day": obl.due_day,
                        "category_id": obl.category_id,
                        "is_active": obl.is_active
                    }
                })
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        elif parsed.path == "/api/subcategories":
            try:
                payload = self._read_json_body()
                cat_id = payload.get("category_id")
                name = payload.get("name")
                order = int(payload.get("display_order", 0))
                subcat = self.engine.create_subcategory(category_id=cat_id, name=name, display_order=order)
                self._send_json({
                    "success": True,
                    "subcategory": {
                        "id": subcat.id,
                        "category_id": subcat.category_id,
                        "name": subcat.name,
                        "display_order": subcat.display_order,
                        "is_active": subcat.is_active
                    }
                })
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        elif parsed.path == "/api/category-aliases":
            try:
                payload = self._read_json_body()
                keyword = payload.get("keyword")
                subcat_id = payload.get("subcategory_id")
                cat_id = payload.get("category_id")
                priority = int(payload.get("priority", 10))
                alias = self.engine.add_category_alias(keyword=keyword, subcategory_id=subcat_id, category_id=cat_id, priority=priority)
                self._send_json({
                    "success": True,
                    "alias": {
                        "id": alias.id,
                        "keyword": alias.keyword,
                        "subcategory_id": alias.subcategory_id,
                        "category_id": alias.category_id,
                        "priority": alias.priority
                    }
                })
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        elif parsed.path == "/api/review-queue/approve":
            try:
                payload = self._read_json_body()
                item_id = payload.get("id")
                override = payload.get("override_data")
                item, tx = self.engine.approve_review_item(item_id, override)
                self._send_json({
                    "success": True,
                    "transaction_id": tx.id,
                    "item": {
                        "id": item.id,
                        "status": item.status,
                        "approved_transaction_id": item.approved_transaction_id
                    }
                })
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        elif parsed.path == "/api/review-queue/reject":
            try:
                payload = self._read_json_body()
                item_id = payload.get("id")
                reason = payload.get("reason")
                item = self.engine.reject_review_item(item_id, reason)
                self._send_json({
                    "success": True,
                    "item": {
                        "id": item.id,
                        "status": item.status
                    }
                })
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        elif parsed.path == "/api/credit-cards":
            try:
                payload = self._read_json_body()
                card = self.engine.create_credit_card(
                    name=payload["name"],
                    bank_name=payload["bank_name"],
                    credit_limit=float(payload["credit_limit"]),
                    account_id=payload.get("account_id"),
                    billing_cycle_day=int(payload.get("billing_cycle_day", 1)),
                    payment_due_day=int(payload.get("payment_due_day", 15))
                )
                self._send_json({
                    "success": True,
                    "card": {
                        "id": card.id,
                        "name": card.name,
                        "bank_name": card.bank_name,
                        "credit_limit": card.credit_limit,
                        "current_balance": card.current_balance,
                        "billing_cycle_day": card.billing_cycle_day,
                        "payment_due_day": card.payment_due_day,
                        "is_active": card.is_active
                    }
                })
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        elif parsed.path == "/api/credit-cards/statements":
            try:
                payload = self._read_json_body()
                stmt = self.engine.create_credit_card_statement(
                    card_id=payload["card_id"],
                    statement_period=payload["statement_period"],
                    statement_date=payload["statement_date"],
                    due_date=payload["due_date"],
                    total_amount=float(payload["total_amount"]),
                    minimum_payment=float(payload.get("minimum_payment", 0.0))
                )
                self._send_json({
                    "success": True,
                    "statement": {
                        "id": stmt.id,
                        "card_id": stmt.card_id,
                        "statement_period": stmt.statement_period,
                        "statement_date": stmt.statement_date,
                        "due_date": stmt.due_date,
                        "total_amount": stmt.total_amount,
                        "unpaid_amount": stmt.unpaid_amount,
                        "status": stmt.status
                    }
                })
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        elif parsed.path == "/api/credit-cards/payments":
            try:
                payload = self._read_json_body()
                amt = float(payload["amount"])
                from_acc_id = payload.get("from_account_id")
                tx_id = payload.get("transaction_id")
                if from_acc_id:
                    # Cash decreases, Credit card liability decreases, NOT classified as expense (TRANSFER)
                    tx = self.engine.create_transaction(
                        account_id=from_acc_id,
                        amount=amt,
                        direction="TRANSFER",
                        note=payload.get("notes") or "Pembayaran Kartu Kredit",
                        source="CC_PAYMENT"
                    )
                    tx_id = tx.id

                pmt = self.engine.record_credit_card_payment(
                    card_id=payload["card_id"],
                    payment_date=payload["payment_date"],
                    amount=amt,
                    statement_id=payload.get("statement_id"),
                    transaction_id=tx_id,
                    notes=payload.get("notes")
                )
                self._send_json({
                    "success": True,
                    "payment": {
                        "id": pmt.id,
                        "card_id": pmt.card_id,
                        "amount": pmt.amount,
                        "payment_date": pmt.payment_date,
                        "transaction_id": tx_id
                    }
                })
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        elif parsed.path == "/api/accounts/pocket-transfer":
            try:
                payload = self._read_json_body()
                res = self.engine.internal_pocket_transfer(
                    from_account_id=payload["from_account_id"],
                    to_account_id=payload["to_account_id"],
                    amount=float(payload["amount"]),
                    notes=payload.get("notes"),
                    tx_date=payload.get("date")
                )
                self._send_json(res)
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        elif parsed.path == "/api/assets/purchase":
            try:
                payload = self._read_json_body()
                res = self.engine.record_asset_purchase(
                    account_id=payload["account_id"],
                    asset_id=payload["asset_id"],
                    amount=float(payload["amount"]),
                    notes=payload.get("notes"),
                    tx_date=payload.get("date"),
                    weight_grams=float(payload["weight_grams"]) if "weight_grams" in payload and payload["weight_grams"] is not None else None
                )
                self._send_json(res)
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        elif parsed.path == "/api/liabilities/mortgage-payment":
            try:
                payload = self._read_json_body()
                pmt = self.engine.advance_mortgage_payment(
                    liability_id=payload["liability_id"],
                    payment_number=int(payload.get("payment_number", 58)),
                    amount=float(payload["amount"]),
                    principal_portion=float(payload.get("principal_portion", 0.0)),
                    interest_portion=float(payload.get("interest_portion", 0.0)),
                    payment_date=payload.get("payment_date"),
                    notes=payload.get("notes")
                )
                self._send_json({
                    "success": True,
                    "payment": {
                        "id": pmt.id,
                        "liability_id": pmt.liability_id,
                        "amount": pmt.amount,
                        "principal_portion": pmt.principal_portion,
                        "interest_portion": pmt.interest_portion,
                        "payment_date": pmt.payment_date,
                        "notes": pmt.notes
                    }
                })
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        elif parsed.path == "/api/credit-cards/purchase":
            try:
                payload = self._read_json_body()
                res = self.engine.record_credit_card_purchase(
                    card_id=payload["card_id"],
                    amount=float(payload["amount"]),
                    category_id=payload.get("category_id"),
                    subcategory_id=payload.get("subcategory_id"),
                    note=payload.get("note"),
                    tx_date=payload.get("date")
                )
                self._send_json(res)
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        elif parsed.path == "/api/gmail/ingest":
            try:
                payload = self._read_json_body()
                svc = GmailIntelligenceService(self.engine)
                res = svc.process_email(
                    email_text=payload.get("email_text", ""),
                    subject=payload.get("subject"),
                    auto_post_threshold=float(payload.get("auto_post_threshold", 0.85))
                )
                self._send_json({"success": True, "result": res})
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        elif parsed.path == "/api/gmail/review-queue/action":
            try:
                payload = self._read_json_body()
                item_id = payload.get("id")
                action = payload.get("action", "APPROVE").upper()
                if action == "APPROVE":
                    approved_item, tx = self.engine.approve_review_item(item_id, payload.get("overrides"))
                    self._send_json({"success": True, "status": "APPROVED", "transaction_id": tx.id if tx else None})
                else:
                    rej = self.engine.reject_review_item(item_id, payload.get("reason", "Owner rejected"))
                    self._send_json({"success": True, "status": "REJECTED"})
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        elif parsed.path == "/api/assets/gold/update-price":
            try:
                payload = self._read_json_body()
                price = float(payload.get("price_per_gram", 1500000.0))
                weight = float(payload.get("weight_grams", 50.0))
                reason = payload.get("reason", f"Update harga emas harian Rp {price:,.0f}/g")
                new_val = price * weight
                
                conn = self.engine.db.get_connection()
                cur = conn.execute("SELECT id FROM assets WHERE name LIKE '%Emas%' OR name LIKE '%Logam Mulia%' LIMIT 1")
                row = cur.fetchone()
                if row:
                    self.engine.update_asset(row["id"], current_value=new_val, notes=f"Emas Antam: {weight}g @ Rp {price:,.0f}/g (valuasi Rp {new_val:,.0f})")
                    self.engine.record_asset_valuation(row["id"], date.today().isoformat(), new_val, reason)
                    self._send_json({"success": True, "asset_id": row["id"], "valuation": new_val, "price_per_gram": price})
                else:
                    self._send_json({"success": False, "error": "Gold asset not found"}, status=404)
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        elif parsed.path == "/api/transactions/correct":
            try:
                payload = self._read_json_body()
                tx = self.engine.correct_transaction(
                    transaction_id=payload["id"],
                    account_id=payload.get("account_id"),
                    amount=float(payload["amount"]) if "amount" in payload and payload["amount"] is not None else None,
                    direction=payload.get("direction"),
                    category_id=payload.get("category_id"),
                    subcategory_id=payload.get("subcategory_id"),
                    note=payload.get("note"),
                    tx_date=payload.get("date"),
                    reason=payload.get("reason", "Owner correction"),
                    scope=payload.get("scope", "transaction")
                )
                self._send_json({
                    "success": True,
                    "transaction": {
                        "id": tx.id,
                        "account_id": tx.account_id,
                        "amount": tx.amount,
                        "direction": tx.direction,
                        "category_id": tx.category_id,
                        "subcategory_id": tx.subcategory_id,
                        "note": tx.note,
                        "date": tx.date,
                        "status": tx.status
                    }
                })
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        elif parsed.path == "/api/transactions/void":
            try:
                payload = self._read_json_body()
                tx_id = payload.get("id")
                if not tx_id:
                    self._send_json({"success": False, "error": "Transaction ID is required"}, status=400)
                    return
                reason = payload.get("reason", "Voided by owner")
                scope = payload.get("scope", "transaction")
                res = self.engine.void_transaction(transaction_id=tx_id, reason=reason, scope=scope)
                self._send_json(res)
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        else:
            self._send_json({"error": "Not Found"}, status=404)

    # ====================================================
    # PUT Handlers
    # ====================================================
    def do_PUT(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/accounts":
            try:
                payload = self._read_json_body()
                acc_id = payload.get("id")
                if not acc_id:
                    self._send_json({"success": False, "error": "Account ID is required"}, status=400)
                    return
                name = payload.get("name")
                account_type = payload.get("type") or payload.get("account_type")
                is_active = payload.get("is_active")
                acc = self.engine.update_account(account_id=acc_id, name=name, account_type=account_type, is_active=is_active)
                if not acc:
                    self._send_json({"success": False, "error": "Account not found"}, status=404)
                    return
                self._send_json({
                    "success": True,
                    "account": {
                        "id": acc.id,
                        "name": acc.name,
                        "type": acc.type,
                        "balance": acc.balance,
                        "is_active": acc.is_active
                    }
                })
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        elif parsed.path == "/api/categories":
            try:
                payload = self._read_json_body()
                cat_id = payload.get("id")
                if not cat_id:
                    self._send_json({"success": False, "error": "Category ID is required"}, status=400)
                    return
                name = payload.get("name")
                keywords = payload.get("keywords")
                is_active = payload.get("is_active")
                cat = self.engine.update_category(category_id=cat_id, name=name, keywords=keywords, is_active=is_active)
                if not cat:
                    self._send_json({"success": False, "error": "Category not found"}, status=404)
                    return
                self._send_json({
                    "success": True,
                    "category": {
                        "id": cat.id,
                        "name": cat.name,
                        "keywords": cat.keywords,
                        "is_active": cat.is_active
                    }
                })
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        elif parsed.path == "/api/assets":
            try:
                payload = self._read_json_body()
                ast_id = payload.get("id")
                if not ast_id:
                    self._send_json({"success": False, "error": "Asset ID is required"}, status=400)
                    return
                ast = self.engine.update_asset(
                    asset_id=ast_id,
                    name=payload.get("name"),
                    asset_type=payload.get("type"),
                    current_value=payload.get("current_value"),
                    notes=payload.get("notes"),
                    is_active=payload.get("is_active")
                )
                if not ast:
                    self._send_json({"success": False, "error": "Asset not found"}, status=404)
                    return
                self._send_json({
                    "success": True,
                    "asset": {
                        "id": ast.id,
                        "name": ast.name,
                        "type": ast.type,
                        "current_value": ast.current_value,
                        "notes": ast.notes,
                        "is_active": ast.is_active
                    }
                })
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        elif parsed.path == "/api/liabilities":
            try:
                payload = self._read_json_body()
                liab_id = payload.get("id")
                if not liab_id:
                    self._send_json({"success": False, "error": "Liability ID is required"}, status=400)
                    return
                liab = self.engine.update_liability(
                    liability_id=liab_id,
                    name=payload.get("name"),
                    liability_type=payload.get("type"),
                    original_amount=payload.get("original_amount"),
                    remaining_amount=payload.get("remaining_amount"),
                    monthly_payment=payload.get("monthly_payment"),
                    due_day=payload.get("due_day"),
                    notes=payload.get("notes"),
                    is_active=payload.get("is_active")
                )
                if not liab:
                    self._send_json({"success": False, "error": "Liability not found"}, status=404)
                    return
                self._send_json({
                    "success": True,
                    "liability": {
                        "id": liab.id,
                        "name": liab.name,
                        "type": liab.type,
                        "original_amount": liab.original_amount,
                        "remaining_amount": liab.remaining_amount,
                        "monthly_payment": liab.monthly_payment,
                        "due_day": liab.due_day,
                        "notes": liab.notes,
                        "is_active": liab.is_active
                    }
                })
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        elif parsed.path == "/api/obligations":
            try:
                payload = self._read_json_body()
                obl_id = payload.get("id")
                if not obl_id:
                    self._send_json({"success": False, "error": "Obligation ID is required"}, status=400)
                    return
                name = payload.get("name")
                amount = float(payload["amount"]) if "amount" in payload and payload["amount"] is not None else None
                due_day = int(payload["due_day"]) if "due_day" in payload and payload["due_day"] is not None else None
                category_id = payload.get("category_id")
                is_active = int(payload["is_active"]) if "is_active" in payload and payload["is_active"] is not None else None

                obl = self.engine.update_fixed_obligation(
                    obligation_id=obl_id,
                    name=name,
                    amount=amount,
                    due_day=due_day,
                    category_id=category_id,
                    is_active=is_active
                )
                if not obl:
                    self._send_json({"success": False, "error": f"Obligation not found: {obl_id}"}, status=404)
                    return

                self._send_json({
                    "success": True,
                    "obligation": {
                        "id": obl.id,
                        "name": obl.name,
                        "amount": obl.amount,
                        "due_day": obl.due_day,
                        "category_id": obl.category_id,
                        "is_active": obl.is_active
                    }
                })
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        elif parsed.path == "/api/config":
            try:
                payload = self._read_json_body()
                updated = {}
                if "key" in payload and "value" in payload:
                    cfg = self.engine.set_config(str(payload["key"]), str(payload["value"]))
                    updated[cfg.key] = cfg.value
                else:
                    for k, v in payload.items():
                        cfg = self.engine.set_config(str(k), str(v))
                        updated[cfg.key] = cfg.value
                self._send_json({"success": True, "config": updated})
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        elif parsed.path == "/api/subcategories":
            try:
                payload = self._read_json_body()
                subcat_id = payload.get("id")
                if not subcat_id:
                    self._send_json({"success": False, "error": "Subcategory ID is required"}, status=400)
                    return
                subcat = self.engine.update_subcategory(
                    subcategory_id=subcat_id,
                    name=payload.get("name"),
                    display_order=int(payload["display_order"]) if "display_order" in payload and payload["display_order"] is not None else None,
                    is_active=int(payload["is_active"]) if "is_active" in payload and payload["is_active"] is not None else None
                )
                if not subcat:
                    self._send_json({"success": False, "error": "Subcategory not found"}, status=404)
                    return
                self._send_json({
                    "success": True,
                    "subcategory": {
                        "id": subcat.id,
                        "category_id": subcat.category_id,
                        "name": subcat.name,
                        "display_order": subcat.display_order,
                        "is_active": subcat.is_active
                    }
                })
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        elif parsed.path == "/api/credit-cards":
            try:
                payload = self._read_json_body()
                card_id = payload.get("id")
                if not card_id:
                    self._send_json({"success": False, "error": "Credit Card ID is required"}, status=400)
                    return
                card = self.engine.update_credit_card(
                    card_id=card_id,
                    name=payload.get("name"),
                    bank_name=payload.get("bank_name"),
                    credit_limit=float(payload["credit_limit"]) if "credit_limit" in payload and payload["credit_limit"] is not None else None,
                    current_balance=float(payload["current_balance"]) if "current_balance" in payload and payload["current_balance"] is not None else None,
                    billing_cycle_day=int(payload["billing_cycle_day"]) if "billing_cycle_day" in payload and payload["billing_cycle_day"] is not None else None,
                    payment_due_day=int(payload["payment_due_day"]) if "payment_due_day" in payload and payload["payment_due_day"] is not None else None,
                    is_active=int(payload["is_active"]) if "is_active" in payload and payload["is_active"] is not None else None
                )
                if not card:
                    self._send_json({"success": False, "error": "Credit card not found"}, status=404)
                    return
                self._send_json({
                    "success": True,
                    "card": {
                        "id": card.id,
                        "name": card.name,
                        "bank_name": card.bank_name,
                        "credit_limit": card.credit_limit,
                        "current_balance": card.current_balance,
                        "billing_cycle_day": card.billing_cycle_day,
                        "payment_due_day": card.payment_due_day,
                        "is_active": card.is_active
                    }
                })
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        elif parsed.path == "/api/gmail/scan":
            try:
                payload = self._read_json_body() or {}
                query = payload.get("query")
                max_results = int(payload.get("max_results", 20))
                dry_run = bool(payload.get("dry_run", False))
                service = GmailIntelligenceService(self.engine)
                result = service.scan_inbox(query=query, max_results=max_results, dry_run=dry_run)
                self._send_json({"success": True, "result": result})
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=500)
            return

        elif parsed.path == "/api/gmail/review-queue/approve":
            try:
                payload = self._read_json_body()
                item_id = payload.get("item_id")
                override_data = payload.get("override_data")
                if not item_id:
                    self._send_json({"success": False, "error": "item_id is required"}, status=400)
                    return
                tx = self.engine.approve_review_item(item_id=item_id, override_data=override_data)
                self._send_json({"success": True, "transaction_id": tx.id if tx else None})
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        elif parsed.path == "/api/gmail/review-queue/ignore":
            try:
                payload = self._read_json_body()
                item_id = payload.get("item_id")
                reason = payload.get("reason", "Ignored by owner")
                if not item_id:
                    self._send_json({"success": False, "error": "item_id is required"}, status=400)
                    return
                item = self.engine.ignore_review_item(item_id=item_id, reason=reason)
                self._send_json({"success": True, "item_id": item.id if item else None, "status": "IGNORED"})
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        else:
            self._send_json({"error": "Not Found"}, status=404)

    # ====================================================
    # DELETE Handlers
    # ====================================================
    def do_DELETE(self):
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)

        if parsed.path == "/api/category-aliases":
            alias_id = qs.get("id", [None])[0]
            if not alias_id:
                try:
                    payload = self._read_json_body()
                    alias_id = payload.get("id")
                except Exception:
                    pass
            if not alias_id:
                self._send_json({"success": False, "error": "Alias ID is required"}, status=400)
                return
            ok = self.engine.delete_category_alias(alias_id)
            if not ok:
                self._send_json({"success": False, "error": "Category alias not found"}, status=404)
                return
            self._send_json({"success": True, "deleted_id": alias_id})
            return

        elif parsed.path == "/api/assets":
            asset_id = qs.get("id", [None])[0]
            if not asset_id:
                try:
                    payload = self._read_json_body()
                    asset_id = payload.get("id")
                except Exception:
                    pass
            if not asset_id:
                self._send_json({"success": False, "error": "Asset ID is required"}, status=400)
                return
            ok = self.engine.delete_asset(asset_id)
            if not ok:
                self._send_json({"success": False, "error": "Asset not found"}, status=404)
                return
            self._send_json({"success": True, "deleted_id": asset_id})
            return

        elif parsed.path == "/api/liabilities":
            liab_id = qs.get("id", [None])[0]
            if not liab_id:
                try:
                    payload = self._read_json_body()
                    liab_id = payload.get("id")
                except Exception:
                    pass
            if not liab_id:
                self._send_json({"success": False, "error": "Liability ID is required"}, status=400)
                return
            ok = self.engine.delete_liability(liab_id)
            if not ok:
                self._send_json({"success": False, "error": "Liability not found"}, status=404)
                return
            self._send_json({"success": True, "deleted_id": liab_id})
            return

        elif parsed.path == "/api/obligations":
            obl_id = qs.get("id", [None])[0]
            if not obl_id:
                try:
                    payload = self._read_json_body()
                    obl_id = payload.get("id")
                except Exception:
                    pass
            if not obl_id:
                self._send_json({"success": False, "error": "Obligation ID is required"}, status=400)
                return
            ok = self.engine.delete_fixed_obligation(obl_id)
            if not ok:
                self._send_json({"success": False, "error": "Obligation not found"}, status=404)
                return
            self._send_json({"success": True, "deleted_id": obl_id})
            return

        elif parsed.path == "/api/credit-cards":
            card_id = qs.get("id", [None])[0]
            if not card_id:
                try:
                    payload = self._read_json_body()
                    card_id = payload.get("id")
                except Exception:
                    pass
            if not card_id:
                self._send_json({"success": False, "error": "Credit card ID is required"}, status=400)
                return
            ok = self.engine.delete_credit_card(card_id)
            if not ok:
                self._send_json({"success": False, "error": "Credit card not found"}, status=404)
                return
            self._send_json({"success": True, "deleted_id": card_id})
            return

        elif parsed.path == "/api/subcategories":
            subcat_id = qs.get("id", [None])[0]
            if not subcat_id:
                try:
                    payload = self._read_json_body()
                    subcat_id = payload.get("id")
                except Exception:
                    pass
            if not subcat_id:
                self._send_json({"success": False, "error": "Subcategory ID is required"}, status=400)
                return
            ok = self.engine.delete_subcategory(subcat_id)
            if not ok:
                self._send_json({"success": False, "error": "Subcategory not found"}, status=404)
                return
            self._send_json({"success": True, "deleted_id": subcat_id})
            return

        elif parsed.path == "/api/categories":
            cat_id = qs.get("id", [None])[0]
            if not cat_id:
                try:
                    payload = self._read_json_body()
                    cat_id = payload.get("id")
                except Exception:
                    pass
            if not cat_id:
                self._send_json({"success": False, "error": "Category ID is required"}, status=400)
                return
            ok = self.engine.delete_category(cat_id)
            if not ok:
                self._send_json({"success": False, "error": "Category not found"}, status=404)
                return
            self._send_json({"success": True, "deleted_id": cat_id})
            return

        elif parsed.path == "/api/accounts":
            acc_id = qs.get("id", [None])[0]
            if not acc_id:
                try:
                    payload = self._read_json_body()
                    acc_id = payload.get("id")
                except Exception:
                    pass
            if not acc_id:
                self._send_json({"success": False, "error": "Account ID is required"}, status=400)
                return
            ok = self.engine.delete_account(acc_id)
            if not ok:
                self._send_json({"success": False, "error": "Account not found"}, status=404)
                return
            self._send_json({"success": True, "deleted_id": acc_id})
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
