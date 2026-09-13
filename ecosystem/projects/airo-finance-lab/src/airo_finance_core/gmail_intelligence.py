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

            self._gmail_service = build("gmail", "v1", credentials=creds, cache_discovery=False)
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
        detected_account = "Blu"  # Default
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
        if any(w in combined for w in ["antar blu", "antar-blu", "transfer antar blu", "bayar kartu kredit", "pembayaran tagihan cc", "transfer antar rekening", "internal transfer"]):
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
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})|(\d{2}[/-]\d{2}[/-]\d{4})', text)
        if date_match:
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

        return {
            "account_name": detected_account,
            "account_source": detected_account,
            "amount": amount,
            "currency": "IDR",
            "date": tx_date,
            "direction": direction,
            "tx_type": tx_type,
            "destination": "Internal transfer / target pocket" if direction == "TRANSFER" else "",
            "note": merchant,
            "merchant": merchant,
            "raw_text": text
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

        # 2. Check fingerprint in processed_emails (excluding rejected)
        fp_row = conn.execute("SELECT message_id, status FROM processed_emails WHERE fingerprint = ? AND status != 'REJECTED'", (fingerprint,)).fetchone()
        if fp_row:
            return True, f"Duplicate transaction fingerprint '{fingerprint}' already exists in processed_emails"

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
        auto_ingest: bool = False
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
        if not account_id:
            fb = conn.execute("SELECT id, name FROM accounts WHERE is_active = 1 ORDER BY balance DESC LIMIT 1").fetchone()
            account_id = fb["id"] if fb else None
            parsed["account_name"] = fb["name"] if fb else "Unknown Account"
        parsed["account_id"] = account_id

        # Enqueue Candidate into Review Queue (Zero direct writes)
        q_item = self.engine.enqueue_review_item(
            raw_text=email_text,
            parsed_result=parsed,
            issue_reason="Transaksi terdeteksi dari Gmail (Menunggu persetujuan Owner)",
            confidence=confidence
        )

        # Record in processed_emails
        with conn:
            conn.execute(
                """INSERT OR REPLACE INTO processed_emails 
                   (message_id, thread_id, sender, subject, received_date, fingerprint, status, review_item_id, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, 'CANDIDATE_CREATED', ?, datetime('now'))""",
                (parsed["message_id"], thread_id, sender or "Unknown", subject or "No Subject", parsed["date"], fingerprint, q_item.id)
            )
        conn.commit()

        # Double check review_queue persistence before Telegram dispatch
        persisted = conn.execute("SELECT id, status FROM review_queue WHERE id = ?", (q_item.id,)).fetchone()
        if not persisted or persisted["status"] != "PENDING":
            logger.error(f"Integrity check failed: review_item {q_item.id} not found in PENDING status in review_queue table.")

        # Format Telegram card
        telegram_card = self.format_telegram_review_card(parsed, q_item.id)

        # Telegram delivery via Hermes Outbound
        telegram_delivery = "NONE"
        telegram_message_id = None
        payload_verified = False

        outbound, owner_id = self.get_outbound()
        if outbound and owner_id:
            reply_markup = {
                "inline_keyboard": [
                    [
                        {"text": "✅ Approve", "callback_data": f"gma:{q_item.id}"},
                        {"text": "✏️ Edit", "callback_data": f"gmc:{q_item.id}"},
                        {"text": "❌ Ignore", "callback_data": f"gmi:{q_item.id}"}
                    ]
                ]
            }
            try:
                owner_ids = [x.strip() for x in str(owner_id).split(",") if x.strip()]
                for oid in owner_ids:
                    tg_res = outbound.send_message(
                        chat_id=str(oid),
                        text=telegram_card,
                        reply_markup=reply_markup
                    )
                    if tg_res and (tg_res.get("ok") or tg_res.get("result")):
                        telegram_delivery = "PASS"
                        telegram_message_id = str(tg_res.get("result", {}).get("message_id", ""))
                        payload_verified = True
            except Exception:
                pass

        return {
            "status": "QUEUED_FOR_REVIEW",
            "action": "REVIEW_QUEUE",
            "review_id": q_item.id,
            "confidence": confidence,
            "fingerprint": fingerprint,
            "parsed": parsed,
            "telegram_card": telegram_card,
            "telegram_delivery": telegram_delivery,
            "telegram_message_id": telegram_message_id,
            "payload_verified": payload_verified,
            "message": f"Kandidat transaksi Rp{parsed['amount']:,.0f} ({parsed['account_name']}) masuk Review Queue."
        }

    # ====================================================
    # Phase 5: Telegram Notification Formatting
    # ====================================================
    def format_telegram_review_card(self, candidate: Dict[str, Any], review_id: str) -> str:
        """
        Formats single HTML review card per specification:
        Supports both Expense and Internal Transfer (Antar blu) format.
        """
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
        return card

    # ====================================================
    # Phase 1 & 8: Inbox Scanning (Read-Only)
    # ====================================================
    def scan_inbox(
        self,
        query: str = "newer_than:7d",
        max_results: int = 20,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Proactively scans Gmail inbox using read-only API calls.
        Identifies financial emails and creates candidate transactions.
        """
        service = self.get_service()
        limit = max(1, min(int(max_results), 50))

        # 1. Search messages (Read-only list)
        list_res = service.users().messages().list(userId="me", q=query, maxResults=limit).execute()
        messages = list_res.get("messages", [])

        scanned = 0
        detected_financial = 0
        candidates_created = 0
        duplicates_skipped = 0
        results = []

        for m in messages:
            scanned += 1
            msg_id = m["id"]
            thread_id = m.get("threadId")

            # Check if already processed before fetching full message
            conn = self.db.get_connection()
            already = conn.execute("SELECT status FROM processed_emails WHERE message_id = ?", (msg_id,)).fetchone()
            if already:
                duplicates_skipped += 1
                continue

            # Fetch message metadata & snippet (Read-only get)
            msg_data = service.users().messages().get(
                userId="me",
                id=msg_id,
                format="metadata",
                metadataHeaders=["From", "Subject", "Date"]
            ).execute()

            headers = {h["name"]: h["value"] for h in msg_data.get("payload", {}).get("headers", [])}
            sender = headers.get("From", "")
            subject = headers.get("Subject", "")
            snippet = msg_data.get("snippet", "")

            # Filter financial emails
            is_fin, s_type = self.is_financial_email(sender, subject, snippet)
            if not is_fin:
                if not dry_run:
                    with conn:
                        conn.execute(
                            """INSERT OR REPLACE INTO processed_emails 
                               (message_id, thread_id, sender, subject, status, created_at)
                               VALUES (?, ?, ?, ?, 'SKIPPED_NON_FINANCIAL', datetime('now'))""",
                            (msg_id, thread_id, sender, subject)
                        )
                continue

            detected_financial += 1

            if dry_run:
                parsed = self.parse_email(snippet, subject, sender)
                results.append({
                    "message_id": msg_id,
                    "sender": sender,
                    "subject": subject,
                    "parsed": parsed,
                    "action": "DRY_RUN_DETECTED"
                })
            else:
                proc = self.process_email(
                    email_text=snippet,
                    subject=subject,
                    sender=sender,
                    message_id=msg_id,
                    thread_id=thread_id
                )
                if proc["status"] == "QUEUED_FOR_REVIEW":
                    candidates_created += 1
                elif proc["status"] == "DUPLICATE_SKIPPED":
                    duplicates_skipped += 1
                results.append(proc)

        return {
            "query": query,
            "scanned": scanned,
            "scanned_count": scanned,
            "detected_financial": detected_financial,
            "financial_detected": detected_financial,
            "candidates_created": candidates_created,
            "processed": candidates_created,
            "duplicates_skipped": duplicates_skipped,
            "skipped": duplicates_skipped,
            "dry_run": dry_run,
            "results": results,
            "items": results
        }
