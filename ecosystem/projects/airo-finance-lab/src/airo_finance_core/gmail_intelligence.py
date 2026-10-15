"""
AIRO Finance Lab — Gmail Finance Intelligence Service (v2.0)
Strictly Read-Only Email Ingestion & Transaction Candidate Detection.

Core Principles:
- Gmail is an INPUT SOURCE only.
- NEVER deletes, modifies, sends, or archives emails.
- ZERO direct ledger writes without Owner approval.
- Complete duplicate prevention via message_id and transaction fingerprint.
- Auto-learning system from Owner corrections.
"""

import os
import re
import json
import hashlib
import time
from . import gmail_reliability as reliability
from datetime import datetime, date, timezone
from typing import Dict, Any, Optional, Tuple, List
from .engine import FinanceCoreEngine
from .models import Transaction, ReviewQueueItem

DEFAULT_TOKEN_PATH = os.path.expanduser("~/.hermes/google_token.json")


class GmailIntelligenceService:
    def __init__(
        self,
        engine: FinanceCoreEngine,
        token_path: Optional[str] = None,
        outbound: Optional[Any] = None,
        owner_chat_id: Optional[str] = None
    ):
        self.engine = engine
        self.db = engine.db
        self.token_path = token_path or DEFAULT_TOKEN_PATH
        self._gmail_service = None
        self.outbound = outbound
        self.owner_chat_id = owner_chat_id

    def get_outbound(self) -> Tuple[Optional[Any], Optional[str]]:
        if self.outbound is not None and self.owner_chat_id is not None:
            return self.outbound, self.owner_chat_id
        if os.environ.get("AIRO_FINANCE_OFFLINE_TEST") == "1":
            return None, None
        try:
            from .telegram_ingress import load_telegram_credentials, TelegramOutboundAdapter
            token, chat_id = load_telegram_credentials()
            if token and not self.outbound:
                self.outbound = TelegramOutboundAdapter(token)
            if chat_id and not self.owner_chat_id:
                self.owner_chat_id = chat_id
            return self.outbound, self.owner_chat_id
        except Exception:
            return self.outbound, self.owner_chat_id

    # ====================================================
    # Phase 1: Gmail Connection (Strictly Read-Only)
    # ====================================================
    def connect_gmail(self, token_path: Optional[str] = None):
        """
        Builds Gmail v1 service in strictly READ-ONLY mode using authorized user credentials.
        """
        path = token_path or self.token_path
        if not os.path.exists(path):
            raise FileNotFoundError(f"Google token file not found at {path}")

        try:
            from google.oauth2.credentials import Credentials
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build

            creds = Credentials.from_authorized_user_file(path)
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
                try:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(creds.to_json())
                except Exception:
                    pass

            candidate_service = build("gmail", "v1", credentials=creds, cache_discovery=False)
            candidate_service._http.timeout = 20
            profile = candidate_service.users().getProfile(userId="me").execute()
            if profile.get("emailAddress", "").lower() != "progamer6918@gmail.com":
                raise RuntimeError("Gmail identity mismatch")
            self._gmail_service = candidate_service
            return self._gmail_service
        except ImportError:
            raise RuntimeError("Google API client libraries (google-api-python-client, google-auth) not installed.")

    def get_service(self):
        if not self._gmail_service:
            self.connect_gmail()
        return self._gmail_service

    # ====================================================
    # Phase 2: Email Filtering (Financial Detection Layer)
    # ====================================================
    def is_financial_email(self, sender: str, subject: str, snippet: str = "") -> Tuple[bool, str]:
        """
        Determines whether an email is a financial transaction or payment notification.
        Returns (is_financial, sender_category).
        """
        combined = f"{sender} {subject} {snippet}".lower()

        # 1. Bank senders
        if any(b in combined for b in [
            "blubybcadigital.id", "bcadigital.co.id", "blu",
            "klikbca.com", "bca.co.id", "m-bca", "mybca",
            "bank mandiri", "mandiriglobal.com", "livin",
            "bri.co.id", "bank bri", "brimo",
            "cimb niaga", "octo", "jenius", "btpn"
        ]):
            if any(k in combined for k in [
                "transaksi", "pembayaran", "berhasil", "transfer", "qris",
                "debit", "kartu", "rekening", "saldo", "notifikasi", "receipt"
            ]):
                return True, "BANK"

        # 2. Marketplace & Wallets
        if any(m in combined for m in [
            "tokopedia", "shopee", "gopay", "gojek", "ovo.id",
            "dana.id", "grab", "bukalapak", "blibli"
        ]):
            if any(k in combined for k in [
                "pembayaran", "transaksi", "berhasil", "pesanan", "invoice",
                "receipt", "tagihan", "top up", "order"
            ]):
                return True, "MARKETPLACE"

        # 3. Finance, Utilities, Bills & Subscriptions
        if any(f in combined for f in [
            "pln", "indihome", "telkom", "bpjs", "asuransi",
            "prudential", "allianz", "axa", "google play",
            "netflix", "spotify", "apple.com/bill", "cloud", "aws", "openai"
        ]):
            if any(k in combined for k in [
                "invoice", "receipt", "bukti pembayaran", "tagihan",
                "pembayaran berhasil", "bill", "statement", "subscription"
            ]):
                return True, "FINANCE_UTILITY"

        # 4. Keyword heuristic for any email with clear payment indicator
        if any(w in combined for w in [
            "bukti transfer", "pembayaran qris berhasil", "notifikasi transfer",
            "transaksi berhasil", "payment receipt", "payment confirmation"
        ]):
            return True, "HEURISTIC"

        return False, "NON_FINANCIAL"

    # ====================================================
    # Phase 3: Transaction Extraction
    # ====================================================
    def parse_email(self, email_text: str, subject: Optional[str] = None, sender: Optional[str] = None) -> Dict[str, Any]:
        """
        Extracts financial entities from email text:
        - date (YYYY-MM-DD)
        - merchant / note
        - amount (float)
        - currency (IDR)
        - account source
        - direction (EXPENSE / INCOME / TRANSFER)
        - raw email reference
        """
        text = email_text.strip()
        subj = subject or ""
        send = sender or ""
        combined = f"{send} {subj} {text}".lower()

        # 1. Detect Account Source
        detected_account = "Unknown Account"
        if any(b in combined for b in ["blu", "bca digital", "blubybcadigital"]):
            detected_account = "Blu"
        elif any(b in combined for b in ["bca utama", "m-bca", "klikbca", "mybca", "bca.co.id", "qris bca"]):
            detected_account = "BCA Utama"
        elif any(b in combined for b in ["mandiri", "livin"]):
            detected_account = "Mandiri"
        elif any(b in combined for b in ["tokopedia card", "kartu kredit bri"]):
            detected_account = "Tokopedia Card (BRI)"
        elif "bca" in combined:
            detected_account = "BCA Utama"

        # 2. Extract Amount
        amount = 0.0
        amt_match = re.search(r'(?:rp|idr)\.?\s*([0-9\.,]+)', text, re.IGNORECASE)
        if amt_match:
            raw_amt = amt_match.group(1).replace(".", "").replace(",", ".")
            try:
                amount = float(raw_amt)
            except ValueError:
                amount = 0.0
        else:
            k_match = re.search(r'([0-9]+(?:\.[0-9]+)?)\s*(?:ribu|rb|k\b)', text, re.IGNORECASE)
            if k_match:
                try:
                    amount = float(k_match.group(1)) * 1000.0
                except ValueError:
                    amount = 0.0

        # 3. Extract Direction & Transaction Type
        direction = "EXPENSE"
        tx_type = "Pengeluaran"
        direction_known = any(w in combined for w in ["80777", "tagihan tokopedia card", "bayar tokopedia card", "pembayaran tokopedia card", "pembayaran tagihan cc", "bayar kartu kredit", "pembayaran kartu kredit", "pembayaran kredivo", "antar blu", "antar-blu", "transfer antar rekening", "internal transfer", "transfer masuk", "dana masuk", "penerimaan", "cashback", "gaji", "income", "transfer keluar", "pembayaran", "qris", "debit", "pembelian", "debet"])
        if any(w in combined for w in ["80777", "tagihan tokopedia card", "bayar tokopedia card", "pembayaran tokopedia card", "pembayaran tagihan cc", "bayar kartu kredit", "pembayaran kartu kredit", "pembayaran kredivo"]):
            direction = "CC_PAYMENT"
            tx_type = "Pelunasan Kartu Kredit"
            if "blu" in combined:
                detected_account = "Blu Pocket CC"
        elif any(w in combined for w in ["antar blu", "antar-blu", "transfer antar blu", "bayar kartu kredit", "pembayaran tagihan cc", "transfer antar rekening", "internal transfer"]):
            direction = "TRANSFER"
            if "antar blu" in combined or "antar-blu" in combined:
                tx_type = "Antar blu"
            else:
                tx_type = "Transfer"
        elif any(w in combined for w in ["transfer masuk", "dana masuk", "penerimaan", "cashback", "gaji", "income"]):
            direction = "INCOME"
            tx_type = "Penerimaan Dana"
        elif any(w in combined for w in ["transfer keluar", "pembayaran", "qris", "debit", "pembelian", "debet"]):
            direction = "EXPENSE"
            tx_type = "Pengeluaran"

        # 4. Extract Date
        tx_date = date.today().isoformat()
        date_known = False
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})|(\d{2}[/-]\d{2}[/-]\d{4})', text)
        if date_match:
            date_known = True
            raw_d = date_match.group(0)
            if "-" in raw_d and len(raw_d.split("-")[0]) == 4:
                tx_date = raw_d
            else:
                parts = re.split(r'[/-]', raw_d)
                if len(parts) == 3:
                    tx_date = f"{parts[2]}-{parts[1]}-{parts[0]}"
        else:
            # Check Indonesian textual date formats (e.g. "13 Sep 2026 13:55:41 WIB", "13 September 2026")
            month_map = {
                "jan": "01", "januari": "01",
                "feb": "02", "februari": "02",
                "mar": "03", "maret": "03",
                "apr": "04", "april": "04",
                "mei": "05", "may": "05",
                "jun": "06", "juni": "06",
                "jul": "07", "juli": "07",
                "agu": "08", "agustus": "08", "aug": "08",
                "sep": "09", "september": "09",
                "okt": "10", "oktober": "10", "oct": "10",
                "nov": "11", "november": "11",
                "des": "12", "desember": "12", "dec": "12"
            }
            text_date_match = re.search(r'(\d{1,2})\s+([a-zA-Z]{3,9})\s+(\d{4})', text)
            if text_date_match:
                d_day = text_date_match.group(1).zfill(2)
                m_str = text_date_match.group(2).lower()
                d_year = text_date_match.group(3)
                if m_str in month_map:
                    date_known = True
                    tx_date = f"{d_year}-{month_map[m_str]}-{d_day}"

        # 5. Extract Merchant / Note
        merchant = ""
        if tx_type == "Antar blu":
            merchant = "Antar blu"
        else:
            merchant_patterns = [
                r'(?:merchant|tujuan|pembayaran ke|transaksi di|kepada)\s*[:\-]?\s*([a-zA-Z0-9\s&\'\.\-]+?)(?:\r|\n|\.|\,|$)',
                r'(?:qris|debit|transaksi|pembayaran|transfer|belanja)\s+(?:sebesar\s+[^\s]+\s+)?(?:di|ke)\s+([a-zA-Z0-9\s&\'\.\-]+?)(?:\r|\n|\.|\,|$)'
            ]
            for pat in merchant_patterns:
                m = re.search(pat, text, re.IGNORECASE)
                if m:
                    cand = m.group(1).strip()
                    if cand and len(cand) >= 3 and len(cand) <= 50 and not any(w in cand.lower() for w in ["berhasil", "rekening", "sebesar", "pada tanggal"]):
                        merchant = cand
                        break

        if not merchant and subj:
            clean_subj = re.sub(r'^(re|fwd|notifikasi|pembayaran)\s*[:\-]\s*', '', subj, flags=re.IGNORECASE).strip()
            clean_subj = re.sub(r'\s*\((?:forwarded|fwd|copy)\)', '', clean_subj, flags=re.IGNORECASE).strip()
            if clean_subj:
                merchant = clean_subj[:40]

        if not merchant:
            merchant = "Transaksi Keuangan"

        from .gmail_details import facts
        structured = facts(text)
        return {
            "account_name": detected_account,
            "account_source": detected_account,
            "amount": amount,
            "currency": "IDR",
            "date": tx_date,
            "date_known": date_known,
            "direction": direction,
            "tx_type": tx_type,
            "direction_known": direction_known,
            "destination": "Internal transfer / target pocket" if direction == "TRANSFER" else "",
            "note": merchant,
            "merchant": merchant,
            "raw_text": "",
            **structured
        }

    # ====================================================
    # Phase 4: Classification Engine
    # ====================================================
    def classify(self, note: str, amount: float = 0.0) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str], float]:
        """
        Uses existing Categories, Subcategories, and Aliases in the database.
        Returns: (category_id, category_name, subcategory_id, subcategory_name, confidence)
        """
        lower_note = note.lower().strip()
        words = re.findall(r'\b[a-zA-Z0-9]{3,}\b', lower_note)

        # 1. Exact or Alias Matching
        for word in words:
            matched = self.engine.find_category_by_keyword(word)
            if matched:
                return (
                    matched.get("category_id"),
                    matched.get("category_name"),
                    matched.get("subcategory_id"),
                    matched.get("subcategory_name"),
                    0.92  # High confidence from alias / registered keyword
                )

        # 2. Domain Heuristics
        if any(w in lower_note for w in ["antar blu", "antar-blu", "transfer antar"]):
            return (None, "Transfer", None, "Antar blu", 0.65)
        elif any(w in lower_note for w in ["kopi", "cafe", "coffee", "starbucks", "kenangan", "fore", "janji jiwa"]):
            cat = self.engine.find_category_by_keyword("kopi") or self.engine.find_category_by_keyword("makan")
            if cat:
                return (cat.get("category_id"), cat.get("category_name") or "Makanan & Minuman", cat.get("subcategory_id"), cat.get("subcategory_name") or "Kopi", 0.88)
        elif any(w in lower_note for w in ["makan", "resto", "restaurant", "warung", "bakso", "nasi", "food", "lunch", "dinner"]):
            cat = self.engine.find_category_by_keyword("makan")
            if cat:
                return (cat.get("category_id"), cat.get("category_name") or "Makanan & Minuman", cat.get("subcategory_id"), cat.get("subcategory_name") or "Makan Siang", 0.82)
        elif any(w in lower_note for w in ["bensin", "spbu", "pertamina", "shell", "bbm", "bp akr"]):
            cat = self.engine.find_category_by_keyword("bensin")
            if cat:
                return (cat.get("category_id"), cat.get("category_name") or "Transportasi", cat.get("subcategory_id"), cat.get("subcategory_name") or "Bensin", 0.88)
        elif any(w in lower_note for w in ["grab", "gojek", "goride", "gocar", "maxim", "parkir", "toll"]):
            cat = self.engine.find_category_by_keyword("transportasi") or self.engine.find_category_by_keyword("bensin")
            if cat:
                return (cat.get("category_id"), cat.get("category_name") or "Transportasi", cat.get("subcategory_id"), cat.get("subcategory_name") or "Transport Umum", 0.80)
        elif any(w in lower_note for w in ["listrik", "pln", "token pln", "air", "pdam", "indihome", "wifi", "pulsa", "paket data"]):
            cat = self.engine.find_category_by_keyword("listrik") or self.engine.find_category_by_keyword("tagihan")
            if cat:
                return (cat.get("category_id"), cat.get("category_name") or "Tagihan & Utilitas", cat.get("subcategory_id"), cat.get("subcategory_name") or "Listrik & Air", 0.85)
        elif any(w in lower_note for w in ["80777", "tokopedia card", "kartu kredit", "cc payment", "pembayaran tagihan cc", "kredivo"]):
            cat = self.engine.find_category_by_keyword("tagihan")
            if cat:
                return (cat.get("category_id"), cat.get("category_name") or "Tagihan & Utilitas", cat.get("subcategory_id"), cat.get("subcategory_name") or "Tagihan Kartu Kredit", 0.95)
        elif any(w in lower_note for w in ["tokopedia", "shopee", "indomaret", "alfamart", "supermarket"]):
            cat = self.engine.find_category_by_keyword("belanja")
            if cat:
                return (cat.get("category_id"), cat.get("category_name") or "Belanja Kebutuhan", cat.get("subcategory_id"), cat.get("subcategory_name") or "Supermarket", 0.78)

        # Fallback: General category with lower confidence requiring Owner review
        first_cat = self.db.get_connection().execute("SELECT id, name FROM categories WHERE is_active = 1 LIMIT 1").fetchone()
        if first_cat:
            return (first_cat["id"], first_cat["name"], None, "Umum", 0.45)
        return (None, "Tanpa Kategori", None, "Unclassified", 0.30)

    # ====================================================
    # Phase 6: Duplicate Protection
    # ====================================================
    def calculate_fingerprint(self, account_name: str, tx_date: str, amount: float, merchant: str) -> str:
        """
        Creates a deterministic fingerprint for transaction uniqueness.
        """
        norm = f"{account_name.strip().lower()}_{tx_date}_{float(amount):.2f}_{merchant.strip().lower()}"
        return hashlib.sha256(norm.encode("utf-8")).hexdigest()[:16]

    def check_duplicate(self, message_id: Optional[str], fingerprint: str) -> Tuple[bool, str]:
        """
        Checks if the email or transaction has already been processed or recorded.
        """
        conn = self.db.get_connection()

        # 1. Check message_id in processed_emails
        if message_id:
            row = conn.execute("SELECT message_id, status, review_item_id FROM processed_emails WHERE message_id = ?", (message_id,)).fetchone()
            if row:
                return True, f"Email message_id '{message_id}' already processed (Status: {row['status']})"

        return False, "NOT_DUPLICATE"

    # ====================================================
    # Phase 5: Owner Review & Ingestion Pipeline
    # ====================================================
    def process_email(
        self,
        email_text: str,
        subject: Optional[str] = None,
        sender: Optional[str] = None,
        message_id: Optional[str] = None,
        thread_id: Optional[str] = None,
        auto_ingest: bool = False,
        received_date: Optional[str] = None,
        received_at: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Core Ingestion Pipeline:
        1. Parse email content
        2. Classify candidate
        3. Check duplicate protection
        4. Enqueue into Review Queue
        5. Record into processed_emails
        6. Format Telegram notification card
        """
        parsed = self.parse_email(email_text, subject, sender)
        if received_date and not parsed.get("date_known"):
            parsed["date"] = received_date
            parsed["date_inferred_from_email"] = True
        cat_id, cat_name, subcat_id, subcat_name, confidence = self.classify(parsed["note"], parsed["amount"])

        parsed["category_id"] = cat_id
        parsed["category_name"] = cat_name
        parsed["subcategory_id"] = subcat_id
        parsed["subcategory_name"] = subcat_name
        parsed["confidence"] = confidence
        parsed["sender"] = sender or ""
        parsed["subject"] = subject or ""
        parsed["message_id"] = message_id or f"local_{hashlib.sha256(email_text.encode()).hexdigest()[:12]}"

        # Calculate fingerprint
        fingerprint = self.calculate_fingerprint(parsed["account_name"], parsed["date"], parsed["amount"], parsed["note"])
        parsed["fingerprint"] = fingerprint
        parsed["message_at"] = received_at
        parsed["source_received_at"] = received_at
        parsed["source_id"] = "gmail:" + parsed["message_id"]

        # Duplicate check
        is_dup, dup_reason = self.check_duplicate(message_id, fingerprint)
        if is_dup:
            return {
                "status": "DUPLICATE_SKIPPED",
                "action": "SKIPPED",
                "reason": dup_reason,
                "confidence": confidence,
                "parsed": parsed
            }

        # Resolve Account ID
        conn = self.db.get_connection()
        acc_row = conn.execute(
            "SELECT id, name FROM accounts WHERE name = ? OR name LIKE ?",
            (parsed["account_name"], f"%{parsed['account_name']}%")
        ).fetchone()
        account_id = acc_row["id"] if acc_row else None
        parsed["account_id"] = account_id
        from .intake_service import IntakeService
        from .intake_learning import suggest
        learned=suggest(IntakeService(self.engine),parsed)
        for field in ('category_id','category_name','subcategory_id','subcategory_name','suggested_rule'):
            if field in learned:parsed[field]=learned[field]
        reasons = []
        if parsed.get("temporal_issue"): reasons.append("Ada beberapa waktu transaksi pada email; perlu diperiksa")
        if parsed.get("date_inferred_from_email"): reasons.append("Tanggal mengikuti waktu email; periksa tanggal transaksi")
        if not account_id: reasons.append("Akun belum diketahui; pilih akun sebelum approve")
        if parsed["amount"] <= 0: reasons.append("Nominal belum valid")
        if parsed.get("merchant", "").lower() in ("transaksimu pakai blu berhasil", "internet transaction journal", "info transaksi masuk ke blu kamu"):
            reasons.append("Tujuan transaksi belum jelas; balas kartu dengan catatan atau pecahan")
            parsed.update(category_id=None,category_name=None,subcategory_id=None,subcategory_name=None)
        if not parsed.get("direction_known", False): reasons.append("Jenis transaksi belum jelas")
        if parsed["direction"] == "TRANSFER" and not parsed.get("destination_account_id"):
            reasons.append("Akun tujuan transfer perlu diperiksa")
        fp_match = conn.execute("SELECT message_id FROM processed_emails WHERE fingerprint=? AND message_id!=?", (fingerprint,parsed["message_id"])).fetchone()
        if fp_match: reasons.append("Kemungkinan duplikat transaksi; periksa sebelum approve")
        # A ledger match is a warning, never proof that two different emails are identical.
        if account_id and conn.execute("SELECT id FROM transactions WHERE account_id=? AND amount=? AND date=? AND status='ACTIVE' LIMIT 1", (account_id,parsed["amount"],parsed["date"])).fetchone():
            reasons.append("Ada transaksi ledger dengan akun/nominal/tanggal sama; rekonsiliasi dahulu")
        parsed["review_reasons"] = reasons
        if reasons: confidence = min(confidence,0.49)
        parsed["confidence"] = confidence
        outbound, owner_id = self.get_outbound()
        with self.db.atomic():
            # Recheck under database write lock.
            if conn.execute("SELECT 1 FROM processed_emails WHERE message_id=?",(parsed["message_id"],)).fetchone():
                return {"status":"DUPLICATE_SKIPPED","action":"SKIPPED","parsed":parsed}
            q_item = self.engine.enqueue_review_item(raw_text="Gmail reference: "+parsed["message_id"], parsed_result=parsed,
                confidence=confidence, issue_reason="; ".join(reasons) or "Menunggu persetujuan Owner")
            conn.execute("INSERT INTO processed_emails (message_id,thread_id,sender,subject,received_date,fingerprint,status,review_item_id) VALUES (?,?,?,?,?,?,?,?)",(parsed["message_id"],thread_id,sender or "Unknown",subject or "No Subject",parsed["date"],fingerprint,"CANDIDATE_CREATED",q_item.id))
            rule=conn.execute("SELECT enabled,owner_approved FROM intake_rules WHERE id=?",(parsed.get('suggested_rule',''),)).fetchone()
            if rule and rule['enabled'] and rule['owner_approved'] and not reasons and parsed.get('bank_reference') and parsed.get('occurred_at') and parsed.get('date_known') and parsed.get('direction_known') and parsed['direction'] in ('EXPENSE','INCOME'):
                item,tx=self.engine.approve_review_item(q_item.id)
                for oid in str(owner_id or '').split(','):
                    if oid.strip():reliability.enqueue(self.db,'auto_receipt',q_item.id,oid.strip(),'sendMessage',{'chat_id':oid.strip(),'text':reliability.receipt(self.engine,tx),'parse_mode':'HTML'})
                return {'status':'QUEUED_FOR_REVIEW','review_id':q_item.id,'parsed':parsed,'confidence':confidence,'auto_recorded':True}
            telegram_card = self.format_telegram_review_card(parsed,q_item.id)
            for oid in str(owner_id or "").split(","):
                if oid.strip():
                    reliability.enqueue(self.db,"candidate",q_item.id,oid.strip(),"sendMessage", {
                        "chat_id":oid.strip(),"text":telegram_card,"parse_mode":"HTML",
                        "reply_markup":{"inline_keyboard":[[{"text":"✅ Setujui","callback_data":f"gma:{q_item.id}"}], [{"text":"📝 Catatan / pecah","callback_data":f"gsp:{q_item.id}"}], [{"text":"🔗 Sudah tercatat","callback_data":f"gln:{q_item.id}"}], [{"text":"🚫 Bukan transaksi","callback_data":f"gin:{q_item.id}"}]]}})
        # Network transport is outside the atomic SQLite transaction.
        if not getattr(self,"defer_delivery",False): reliability.dispatch(self.db,outbound)
        delivery = conn.execute("SELECT status,message_id FROM finance_outbox WHERE kind='candidate' AND ref=?",(q_item.id,)).fetchone()
        return {"status":"QUEUED_FOR_REVIEW","action":"REVIEW_QUEUE","review_id":q_item.id,
            "confidence":confidence,"fingerprint":fingerprint,"parsed":parsed,"telegram_card":telegram_card,
            "telegram_delivery":"PASS" if delivery and delivery[0]=="SENT" else "PENDING",
            "telegram_message_id":delivery[1] if delivery else None,
            "payload_verified":bool(delivery and delivery[0]=="SENT")}

    # ====================================================
    # Phase 5: Telegram Notification Formatting
    # ====================================================
    def format_telegram_review_card(self, candidate: Dict[str, Any], review_id: str) -> str:
        """
        Formats single HTML review card per specification:
        Supports both Expense and Internal Transfer (Antar blu) format.
        """
        import html
        candidate = {k: html.escape(v) if isinstance(v,str) else v for k,v in candidate.items()}
        amt = candidate.get("amount", 0.0)
        acc = candidate.get("account_name", "Rekening")
        note = candidate.get("note", "Transaksi")
        direction = candidate.get("direction", "EXPENSE")
        tx_type = candidate.get("tx_type", "Antar blu" if direction == "TRANSFER" else "Transaksi")
        tx_date = candidate.get("date", date.today().isoformat())

        if direction == "TRANSFER":
            card = (
                f"🧭 <b>AIRO Finance: Deteksi Transaksi Gmail</b>\n\n"
                f"💰 <b>Rp {amt:,.0f}</b>\n"
                f"🏦 Akun Sumber: <b>{acc}</b>\n"
                f"🔄 Tipe: <b>{tx_type}</b>\n"
                f"🎯 Tujuan: <b>Internal transfer / target pocket</b>\n"
                f"📅 Tanggal: <b>{tx_date}</b>\n\n"
                f"<i>Pilih tindakan di bawah untuk memproses transaksi:</i>\n"
                f"<code>ID: {review_id}</code>"
            )
        else:
            cat = candidate.get("category_name") or "Umum"
            sub = candidate.get("subcategory_name") or "Lainnya"
            conf = int(candidate.get("confidence", 0.5) * 100)
            card = (
                f"🧭 <b>AIRO Finance: Deteksi Transaksi Gmail</b>\n\n"
                f"💰 <b>Rp {amt:,.0f}</b>\n"
                f"🏦 Akun: <b>{acc}</b>\n"
                f"📝 Catatan: <b>{note}</b>\n"
                f"📅 Tanggal: <b>{tx_date}</b>\n\n"
                f"<b>Prediksi Kategori:</b>\n"
                f"{cat} → {sub} ({conf}%)\n\n"
                f"<i>Pilih tindakan di bawah untuk memproses transaksi:</i>\n"
                f"<code>ID: {review_id}</code>"
            )
        if candidate.get("review_reasons"):
            import html
            card += "\n⚠️ " + html.escape("; ".join(candidate["review_reasons"]))
        return card

    # ====================================================
    # Phase 1 & 8: Inbox Scanning (Read-Only)
    # ====================================================
    def scan_inbox(self, query=None, max_results=50, dry_run=False, job_key="routine", budget_seconds=220):
        query = query or "newer_than:7d"
        conn=self.db.get_connection()
        with reliability.lock(self.db) as acquired:
            if not acquired:
                return {"status":"already_running","scanned":0,"processed":0,"pending_notifications":reliability.health(self.db)['pending_notifications']}
            now=time.time();deadline=time.monotonic()+budget_seconds
            saved=reliability.state(self.db,'job:'+job_key,{}) if not dry_run else {}
            if not saved or saved.get('query')!=query or saved.get('complete'):
                saved={'query':query,'api_query':('after:'+str(int(now)-7*86400) if query=='newer_than:7d' else query)+' before:'+str(int(now)+1),'page_token':None,'pending':[{'id':r[0]} for r in conn.execute('SELECT message_id FROM gmail_errors')], 'fetched':False,'complete':False,'started_at':now,'scanned_total':0,'created_total':0}
            h=reliability.state(self.db,'health',{'monitor_started_at':now})
            h.update(last_started_at=now,last_status='running')
            if not dry_run:
                with conn:reliability.put(self.db,'health',h)
            result={'status':'completed','query':query,'scanned':0,'scanned_count':0,'detected_financial':0,'financial_detected':0,'candidates_created':0,'processed':0,'duplicates_skipped':0,'skipped':0,'errors':0,'dry_run':dry_run,'results':[],'items':[],'reconciliation':{'already_recorded':0,'new_candidates':0,'needs_review':0,'parse_failed':0}}
            self.defer_delivery=True
            stage='connect'
            try:
                service=self.get_service()
                if hasattr(service,'_http'):service._http.timeout=20
                while time.monotonic()<deadline:
                    if not saved['pending']:
                        if saved['fetched'] and not saved['page_token']:
                            saved['complete']=True;break
                        stage='list'
                        args={'userId':'me','q':saved['api_query'],'maxResults':min(50,max(1,int(max_results)))}
                        if saved['page_token']:args['pageToken']=saved['page_token']
                        page=service.users().messages().list(**args).execute()
                        saved['pending']=page.get('messages',[]);saved['page_token']=page.get('nextPageToken');saved['fetched']=True
                        if not dry_run:
                            with conn:reliability.put(self.db,'job:'+job_key,saved)
                        if not saved['pending']:continue
                    m=saved['pending'][0];mid=m['id'];result['scanned']+=1;saved['scanned_total']+=1
                    row=conn.execute('SELECT status FROM processed_emails WHERE message_id=?',(mid,)).fetchone()
                    if row:
                        result['duplicates_skipped']+=1;result['reconciliation']['already_recorded']+=1
                        if not dry_run:
                            with conn:conn.execute('DELETE FROM gmail_errors WHERE message_id=?',(mid,))
                    else:
                        stage='fetch'
                        try:
                            msg=service.users().messages().get(userId='me',id=mid,format='full').execute()
                            headers={v['name'].lower():v['value'] for v in msg.get('payload',{}).get('headers',[])}
                            sender=headers.get('from','');subject=headers.get('subject','')
                            from .gmail_details import body
                            snippet=body(msg)
                        except Exception as exc:
                            status=getattr(getattr(exc,'resp',None),'status',None)
                            if status!=404 and not isinstance(exc,(KeyError,TypeError,ValueError)):raise
                            result['errors']+=1;result['reconciliation']['parse_failed']+=1
                            saved['pending'].pop(0)
                            if not dry_run:
                                with conn:
                                    reliability.error(self.db,mid,'fetch',exc)
                                    reliability.put(self.db,'job:'+job_key,saved)
                            continue
                        stage='parse'
                        from zoneinfo import ZoneInfo
                        from email.utils import parsedate_to_datetime
                        received=None;received_at=None
                        try:
                            dt=datetime.fromtimestamp(int(msg['internalDate'])/1000,timezone.utc) if msg.get('internalDate') else parsedate_to_datetime(headers.get('date',''))
                            received=dt.astimezone(ZoneInfo('Asia/Jakarta')).date().isoformat();received_at=dt.astimezone(ZoneInfo('Asia/Jakarta')).isoformat()
                        except (ValueError,TypeError,KeyError):pass
                        try:
                            is_fin,_=self.is_financial_email(sender,subject,snippet)
                            if is_fin:
                                result['detected_financial']+=1
                                if dry_run:
                                    parsed=self.parse_email(snippet,subject,sender)
                                    account=conn.execute('SELECT id FROM accounts WHERE name=?',(parsed['account_name'],)).fetchone()
                                    ambiguous=not account or parsed['amount']<=0 or not parsed.get('direction_known') or parsed['direction']=='TRANSFER'
                                    fp=self.calculate_fingerprint(parsed['account_name'],parsed['date'],parsed['amount'],parsed['note'])
                                    possible=conn.execute('SELECT 1 FROM processed_emails WHERE fingerprint=?',(fp,)).fetchone()
                                    ledger=account and conn.execute("SELECT 1 FROM transactions WHERE account_id=? AND date=? AND amount=? AND status='ACTIVE'",(account[0],parsed['date'],parsed['amount'])).fetchone()
                                    key='needs_review' if ambiguous or possible or ledger else 'new_candidates'
                                    result['reconciliation'][key]+=1
                                else:
                                    stage='persist'
                                    item=self.process_email(snippet,subject,sender,mid,m.get('threadId'),received_date=received,received_at=received_at)
                                    if item['status']=='QUEUED_FOR_REVIEW':
                                        result['candidates_created']+=1;saved['created_total']+=1
                                        result['reconciliation']['needs_review' if item['parsed'].get('review_reasons') else 'new_candidates']+=1
                                    else:result['duplicates_skipped']+=1
                            elif not dry_run:
                                with conn:conn.execute("INSERT OR IGNORE INTO processed_emails(message_id,thread_id,sender,subject,status) VALUES (?,?,?,?,'SKIPPED_NON_FINANCIAL')",(mid,m.get('threadId'),sender,subject))
                            if not dry_run:
                                with conn:conn.execute('DELETE FROM gmail_errors WHERE message_id=?',(mid,))
                        except Exception as exc:
                            result['errors']+=1;result['reconciliation']['parse_failed']+=1
                            if not dry_run:
                                with conn:reliability.error(self.db,mid,stage,exc)
                    saved['pending'].pop(0)
                    if not dry_run:
                        with conn:reliability.put(self.db,'job:'+job_key,saved)
                if not saved['complete'] or result['errors']:result['status']='partial'
                result.update(scanned_count=result['scanned'],financial_detected=result['detected_financial'],processed=result['candidates_created'],skipped=result['duplicates_skipped'],complete=saved['complete'],scanned_total=saved['scanned_total'],created_total=saved['created_total'])
                if not dry_run:
                    h.update(last_finished_at=time.time(),last_status=result['status'],last_error=None)
                    if saved['complete'] and not reliability.health(self.db)['email_errors']:h['last_success_at']=time.time()
                    with conn:
                        reliability.put(self.db,'health',h);reliability.put(self.db,'job:'+job_key,saved)
                    outbound,owner=self.get_outbound();reliability.watchdog(self.db,outbound,owner,deliver=False)
                result['pending_notifications']=reliability.health(self.db)['pending_notifications']
                return result
            except Exception as exc:
                if not dry_run:
                    h.update(last_finished_at=time.time(),last_status='failed',last_error={'stage':stage,'code':type(exc).__name__})
                    with conn:reliability.put(self.db,'health',h);reliability.put(self.db,'job:'+job_key,saved)
                    outbound,owner=self.get_outbound();reliability.watchdog(self.db,outbound,owner,deliver=False)
                raise RuntimeError('Scan Gmail gagal pada tahap '+stage+' ('+type(exc).__name__+'); periksa status Finance Inbox.') from None
            finally:self.defer_delivery=False
