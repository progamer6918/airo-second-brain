import re
import uuid
import time
import calendar
from datetime import datetime, date
from dataclasses import dataclass
from typing import Optional, Dict, Any, Tuple, List
from .engine import FinanceCoreEngine
from .models import Transaction

def format_idr(amount: float) -> str:
    val = int(round(amount))
    sign = "-" if val < 0 else ""
    val_str = f"{abs(val):,}".replace(",", ".")
    return f"{sign}Rp{val_str}"

@dataclass
class TransactionCandidate:
    candidate_id: str
    raw_text: str
    amount: float
    direction: str
    account_id: str
    account_name: str
    category_id: Optional[str]
    category_name: Optional[str]
    note: str
    destination_account_id: Optional[str] = None
    destination_account_name: Optional[str] = None
    status: str = "PENDING"  # PENDING, CONFIRMED, CANCELLED
    created_at: float = 0.0
    subcategory_id: Optional[str] = None
    subcategory_name: Optional[str] = None
    date: Optional[str] = None
    tx_type: str = "EXPENSE"
    original_state: Optional[Dict[str, Any]] = None

    def get_domain(self, engine: Optional[Any] = None) -> str:
        """
        Detects transaction domain:
        - TRANSFER
        - CREDIT_CARD_PURCHASE
        - CC_PAYMENT
        - EXPENSE / INCOME
        """
        if self.direction == "TRANSFER":
            return "TRANSFER"

        lower_note = (self.note or "").lower()
        if getattr(self, "tx_type", None) == "CC_PAYMENT" or any(k in lower_note for k in ("bayar kartu kredit", "bayar cc", "tagihan cc", "pembayaran cc")):
            return "CC_PAYMENT"

        if getattr(self, "tx_type", None) == "CREDIT_CARD_PURCHASE":
            return "CREDIT_CARD_PURCHASE"

        if engine and self.account_id:
            try:
                acc = engine.get_account(self.account_id)
                if acc and (acc.type == "CREDIT_CARD" or getattr(acc, "account_class", "") == "LIABILITY"):
                    return "CREDIT_CARD_PURCHASE"
            except Exception:
                pass

        if any(k in (self.account_name or "").lower() for k in ("tokopedia card", "kartu kredit", "cc bri", "cc bca", "credit card")):
            return "CREDIT_CARD_PURCHASE"

        return self.direction

class SimpleTransactionParser:
    """
    Deterministic, zero-AI single-turn parser for personal finance input.
    Extracts amount, account, category, direction, and note.
    """
    def __init__(self, engine: FinanceCoreEngine):
        self.engine = engine

    def _parse_amount(self, text: str) -> Tuple[Optional[float], Optional[str]]:
        # Matches patterns like 35k, 50rb, 1.5jt, 35000, 35.000, rp 35k
        pattern = re.compile(
            r'(?:^|\s)(?:rp\.?\s*)?(\d+(?:[.,]\d+)?)\s*(k|rb|ribu|jt|juta|m)?(?:\s|$)',
            re.IGNORECASE
        )
        match = pattern.search(text)
        if not match:
            return None, None
            
        raw_num = match.group(1).strip()
        raw_suffix = (match.group(2) or "").lower()
        full_match_token = match.group(0).strip()
        
        multiplier = 1.0
        if raw_suffix in ("k", "rb", "ribu"):
            multiplier = 1000.0
        elif raw_suffix in ("jt", "juta", "m"):
            multiplier = 1000000.0
            
        if multiplier > 1.0:
            cleaned = raw_num.replace(",", ".")
            amount = float(cleaned) * multiplier
        else:
            if "." in raw_num and len(raw_num.split(".")[-1]) == 3:
                cleaned = raw_num.replace(".", "")
            elif "," in raw_num and len(raw_num.split(",")[-1]) == 3:
                cleaned = raw_num.replace(",", "")
            else:
                cleaned = raw_num.replace(",", ".")
            amount = float(cleaned) * multiplier
            
        return amount, full_match_token

    def _match_account_in_text(self, text: str, acc_rows: List[Any]) -> Tuple[Optional[Any], Optional[str]]:
        lower = text.lower()
        # Sort rows such that accounts with more specific names (e.g. "Blu BCA") are evaluated first
        sorted_rows = sorted(acc_rows, key=lambda r: len(r["name"]), reverse=True)
        for row in sorted_rows:
            acc_name_lower = row["name"].lower()
            aliases = []
            if "blu" in acc_name_lower:
                aliases.extend(["blu bca", "blu"])
            elif "bca" in acc_name_lower:
                aliases.extend(["bca utama", "bca"])
            elif "mandiri" in acc_name_lower:
                aliases.extend(["mandiri"])
            elif "cash" in acc_name_lower or "dompet" in acc_name_lower:
                aliases.extend(["cash dompet", "cash", "tunai", "dompet"])
            else:
                aliases.append(acc_name_lower)

            for alias in aliases:
                if re.search(rf'\b{re.escape(alias)}\b', lower):
                    return row, alias
        return None, None

    def parse(self, raw_text: str) -> TransactionCandidate:
        cleaned_text = raw_text.strip()
        if not cleaned_text:
            raise ValueError("Teks input tidak boleh kosong")

        # 1. Extract Amount
        amount, amount_token = self._parse_amount(cleaned_text)
        if amount is None or amount <= 0:
            raise ValueError("Nominal transaksi tidak valid atau tidak ditemukan")

        lower = cleaned_text.lower()
        conn = self.engine.db.get_connection()
        acc_rows = conn.execute("SELECT id, name FROM accounts ORDER BY id").fetchall()
        if not acc_rows:
            raise ValueError("Tidak ada rekening terdaftar di sistem")

        # 2. Check Transfer Intent
        transfer_keywords = ("trf", "transfer", "pindah")
        is_transfer = any(re.search(rf'\b{re.escape(kw)}\b', lower) for kw in transfer_keywords)

        if is_transfer:
            if not re.search(r'\bke\b', lower):
                raise ValueError("Format transfer memerlukan rekening tujuan dengan kata 'ke' (contoh: 'pindah 2jt dari bca ke blu')")

            parts = re.split(r'\bke\b', cleaned_text, flags=re.IGNORECASE, maxsplit=1)
            left_text = parts[0]
            right_text = parts[1]

            # In left_text, find source account
            src_acc, src_token = self._match_account_in_text(left_text, acc_rows)
            # In right_text, find destination account
            dst_acc, dst_token = self._match_account_in_text(right_text, acc_rows)

            # Inverted format check: e.g. "pindah 100k ke blu dari bca"
            if not src_acc and re.search(r'\bdari\b', right_text, re.IGNORECASE):
                sub_parts = re.split(r'\bdari\b', right_text, flags=re.IGNORECASE, maxsplit=1)
                dst_acc, dst_token = self._match_account_in_text(sub_parts[0], acc_rows)
                src_acc, src_token = self._match_account_in_text(sub_parts[1], acc_rows)

            if not src_acc:
                raise ValueError("Rekening asal tidak ditemukan (contoh: 'pindah 2jt dari bca ke blu')")
            if not dst_acc:
                raise ValueError("Rekening tujuan tidak ditemukan (contoh: 'pindah 2jt dari bca ke blu')")
            if src_acc["id"] == dst_acc["id"]:
                raise ValueError("Rekening asal dan tujuan tidak boleh sama")

            # Extract note
            note_tokens = lower.split()
            tokens_to_remove = ["trf", "transfer", "pindah", "dari", "ke"]
            if amount_token:
                tokens_to_remove.extend(amount_token.lower().split())
            if src_token:
                tokens_to_remove.extend(src_token.lower().split())
            if dst_token:
                tokens_to_remove.extend(dst_token.lower().split())

            for tok in tokens_to_remove:
                if tok in note_tokens:
                    note_tokens.remove(tok)

            raw_note = " ".join(note_tokens).strip()
            note = raw_note if raw_note else f"Transfer ke {dst_acc['name']}"

            cand_id = f"cand_{uuid.uuid4().hex[:8]}"
            return TransactionCandidate(
                candidate_id=cand_id,
                raw_text=raw_text,
                amount=amount,
                direction="TRANSFER",
                account_id=src_acc["id"],
                account_name=src_acc["name"],
                destination_account_id=dst_acc["id"],
                destination_account_name=dst_acc["name"],
                category_id=None,
                category_name="Transfer",
                note=note,
                status="PENDING",
                created_at=time.time(),
                date=date.today().isoformat()
            )

        # 3. Extract Direction (INCOME vs EXPENSE)
        income_keywords = ("gaji", "income", "pemasukan", "terima", "diterima", "masuk", "cashback", "bonus", "dividen")
        is_income = any(re.search(rf'\b{re.escape(kw)}\b', lower) for kw in income_keywords)
        direction = "INCOME" if is_income else "EXPENSE"

        # 4. Match Account from DB with Sane Defaults
        chosen_account, matched_account_token = self._match_account_in_text(lower, acc_rows)
        if not chosen_account:
            chosen_account = next((r for r in acc_rows if "bca" in r["name"].lower() and "blu" not in r["name"].lower()), acc_rows[0])

        # 5. Match Category from DB
        cat_rows = conn.execute("SELECT id, name, COALESCE(keywords, '') as keywords FROM categories WHERE is_active = 1 ORDER BY id").fetchall()
        chosen_category = None
        
        category_keyword_map = {
            "Makanan & Minuman": ["makan", "minum", "kopi", "sarapan", "lunch", "dinner", "soto", "bakso", "mie", "nasgor", "cafe", "resto", "food"],
            "Transportasi": ["bensin", "bbm", "pertalite", "pertamax", "solar", "gojek", "gocar", "grab", "maxim", "ojol", "parkir", "tol", "transport"],
            "Tagihan & Utilitas": ["listrik", "pln", "air", "pdam", "wifi", "indihome", "biznet", "pulsa", "kuota", "tagihan", "iuran", "bpjs"],
            "Belanja Kebutuhan": ["belanja", "supermarket", "minimarket", "indomaret", "alfamart", "pasar", "sabun", "shampoo"],
            "Gaji & Pemasukan": ["gaji", "payroll", "salary", "bonus", "thr", "dividen", "proyek", "freelance", "pemasukan", "income"]
        }

        # Check category aliases from DB first
        chosen_subcategory = None
        alias_match = self.engine.find_category_by_keyword(lower)
        if alias_match:
            if alias_match.get("category_id"):
                chosen_category = next((c for c in cat_rows if c["id"] == alias_match["category_id"]), None)
            if alias_match.get("subcategory_id"):
                chosen_subcategory = {
                    "id": alias_match["subcategory_id"],
                    "name": alias_match["subcategory_name"]
                }

        if not chosen_category:
            for cat_row in cat_rows:
                cat_name = cat_row["name"]
                keywords = list(category_keyword_map.get(cat_name, [cat_name.lower()]))
                db_kws = [k.strip().lower() for k in cat_row["keywords"].split(",") if k.strip()]
                for dk in db_kws:
                    if dk not in keywords:
                        keywords.append(dk)
                for kw in keywords:
                    if re.search(rf'\b{re.escape(kw)}\b', lower):
                        chosen_category = cat_row
                        break
                if chosen_category:
                    break

        # If direction is INCOME and no category matched, map to Gaji & Pemasukan if exists
        if direction == "INCOME" and not chosen_category:
            chosen_category = next((c for c in cat_rows if "pemasukan" in c["name"].lower() or "gaji" in c["name"].lower()), None)

        # 6. Extract Note (clean remaining words)
        note_tokens = lower.split()
        if amount_token:
            for piece in amount_token.lower().split():
                if piece in note_tokens:
                    note_tokens.remove(piece)
        if matched_account_token:
            for piece in matched_account_token.lower().split():
                if piece in note_tokens:
                    note_tokens.remove(piece)

        note = " ".join(note_tokens).strip()
        if not note:
            note = chosen_category["name"] if chosen_category else "Transaksi"

        cand_id = f"cand_{uuid.uuid4().hex[:8]}"
        return TransactionCandidate(
            candidate_id=cand_id,
            raw_text=raw_text,
            amount=amount,
            direction=direction,
            account_id=chosen_account["id"],
            account_name=chosen_account["name"],
            category_id=chosen_category["id"] if chosen_category else None,
            category_name=chosen_category["name"] if chosen_category else None,
            note=note,
            status="PENDING",
            created_at=time.time(),
            subcategory_id=chosen_subcategory["id"] if chosen_subcategory else None,
            subcategory_name=chosen_subcategory["name"] if chosen_subcategory else None,
            date=date.today().isoformat()
        )

class TelegramCaptureAdapter:
    """
    Adapter for Telegram Quick Capture vertical slice.
    Manages transaction candidate staging, interactive confirmation cards,
    and ledger write execution.
    """
    def __init__(self, engine: FinanceCoreEngine):
        self.engine = engine
        self.parser = SimpleTransactionParser(engine)
        self._candidates: Dict[str, TransactionCandidate] = {}
        self._edit_sessions: Dict[str, Dict[str, Any]] = {}

    def start_edit_session(self, chat_id: str, candidate_id: str, field: Optional[str] = None):
        self._edit_sessions[str(chat_id)] = {
            "candidate_id": candidate_id,
            "field": field,
            "status": "EDITING",
            "created_at": time.time()
        }

    def get_edit_session(self, chat_id: str) -> Optional[Dict[str, Any]]:
        return self._edit_sessions.get(str(chat_id))

    def clear_edit_session(self, chat_id: str):
        self._edit_sessions.pop(str(chat_id), None)

    def apply_field_update(self, candidate_id: str, field: str, value: Any) -> Optional[TransactionCandidate]:
        candidate = self.get_candidate(candidate_id)
        if not candidate:
            return None

        # Snapshot original state if not yet set
        if not candidate.original_state:
            candidate.original_state = {
                "amount": candidate.amount,
                "account_name": candidate.account_name,
                "account_id": candidate.account_id,
                "destination_account_name": candidate.destination_account_name,
                "destination_account_id": candidate.destination_account_id,
                "category_name": candidate.category_name,
                "category_id": candidate.category_id,
                "subcategory_name": candidate.subcategory_name,
                "subcategory_id": candidate.subcategory_id,
                "note": candidate.note,
                "date": getattr(candidate, "date", None)
            }

        if field == "amount":
            try:
                candidate.amount = float(value)
            except (ValueError, TypeError):
                pass
        elif field == "note":
            candidate.note = str(value).strip()
        elif field == "date":
            candidate.date = str(value).strip()
        elif field == "account":
            acc = self.engine.get_account(str(value))
            if acc:
                candidate.account_id = acc.id
                candidate.account_name = acc.name
        elif field == "dst_account":
            acc = self.engine.get_account(str(value))
            if acc:
                candidate.destination_account_id = acc.id
                candidate.destination_account_name = acc.name
        elif field == "category":
            cat = self.engine.get_category(str(value))
            if cat:
                candidate.category_id = cat.id
                candidate.category_name = cat.name
                # Reset subcategory when category changes
                candidate.subcategory_id = None
                candidate.subcategory_name = None
        elif field == "subcategory":
            if str(value).lower() in ("none", "", "skip"):
                candidate.subcategory_id = None
                candidate.subcategory_name = None
            else:
                subc = self.engine.get_subcategory(str(value))
                if subc:
                    candidate.subcategory_id = subc.id
                    candidate.subcategory_name = subc.name

        return candidate

    def format_guided_edit_menu(self, candidate: TransactionCandidate) -> Dict[str, Any]:
        """
        Renders the Guided Edit Menu based on transaction domain filtering.
        """
        domain = candidate.get_domain(self.engine)
        text = (
            "✏️ <b>Edit Draft Transaksi</b>\n"
            "───────────────────\n"
            "Apa yang mau dikoreksi?"
        )

        cand_id = candidate.candidate_id
        if domain == "TRANSFER":
            buttons = [
                [
                    {"text": "💰 Nominal", "callback_data": f"edf:{cand_id}:amt"},
                    {"text": "📝 Catatan", "callback_data": f"edf:{cand_id}:not"}
                ],
                [
                    {"text": "📤 Akun Asal", "callback_data": f"edf:{cand_id}:src"},
                    {"text": "📥 Akun Tujuan", "callback_data": f"edf:{cand_id}:dst"}
                ],
                [
                    {"text": "📅 Tanggal", "callback_data": f"edf:{cand_id}:dat"},
                    {"text": "❌ Batal", "callback_data": f"ccl:{cand_id}"}
                ]
            ]
        elif domain == "CREDIT_CARD_PURCHASE":
            buttons = [
                [
                    {"text": "💰 Nominal", "callback_data": f"edf:{cand_id}:amt"},
                    {"text": "📂 Kategori", "callback_data": f"edf:{cand_id}:cat"}
                ],
                [
                    {"text": "📝 Catatan", "callback_data": f"edf:{cand_id}:not"},
                    {"text": "📅 Tanggal", "callback_data": f"edf:{cand_id}:dat"}
                ],
                [
                    {"text": "❌ Batal", "callback_data": f"ccl:{cand_id}"}
                ]
            ]
        elif domain == "CC_PAYMENT":
            buttons = [
                [
                    {"text": "💰 Nominal", "callback_data": f"edf:{cand_id}:amt"},
                    {"text": "💳 Akun Pembayar", "callback_data": f"edf:{cand_id}:acc"}
                ],
                [
                    {"text": "📅 Tanggal", "callback_data": f"edf:{cand_id}:dat"},
                    {"text": "❌ Batal", "callback_data": f"ccl:{cand_id}"}
                ]
            ]
        else: # EXPENSE / INCOME
            buttons = [
                [
                    {"text": "💰 Nominal", "callback_data": f"edf:{cand_id}:amt"},
                    {"text": "🏦 Akun", "callback_data": f"edf:{cand_id}:acc"}
                ],
                [
                    {"text": "📂 Kategori", "callback_data": f"edf:{cand_id}:cat"},
                    {"text": "📝 Catatan", "callback_data": f"edf:{cand_id}:not"}
                ],
                [
                    {"text": "📅 Tanggal", "callback_data": f"edf:{cand_id}:dat"},
                    {"text": "❌ Batal", "callback_data": f"ccl:{cand_id}"}
                ]
            ]

        return {
            "text": text,
            "reply_markup": {"inline_keyboard": buttons},
            "candidate_id": cand_id
        }

    def format_account_menu(self, candidate: TransactionCandidate, target: str = "src") -> Dict[str, Any]:
        """
        Renders dynamic account dropdown from Finance Core.
        """
        cand_id = candidate.candidate_id
        domain = candidate.get_domain(self.engine)
        accounts = self.engine.list_accounts(active_only=True)

        cb_prefix = "acc:dst" if target == "dst" else "acc:select"
        buttons = []
        row = []
        for acc in accounts:
            if domain == "CREDIT_CARD_PURCHASE" and getattr(acc, "account_class", "") != "LIABILITY" and acc.type != "CREDIT_CARD":
                continue
            if domain == "CC_PAYMENT" and (getattr(acc, "account_class", "") == "LIABILITY" or acc.type == "CREDIT_CARD"):
                continue
            btn_text = f"🏦 {acc.name}"
            cb_data = f"{cb_prefix}:{cand_id}:{acc.id}"
            row.append({"text": btn_text, "callback_data": cb_data})
            if len(row) == 2:
                buttons.append(row)
                row = []
        if row:
            buttons.append(row)

        buttons.append([{"text": "🔙 Kembali", "callback_data": f"ced:{cand_id}"}])

        title_suffix = "Tujuan" if target == "dst" else ("Asal" if domain == "TRANSFER" else "")
        title_str = f" <b>{title_suffix}</b>" if title_suffix else ""
        text = (
            f"🏦 <b>Pilih Rekening{title_str}</b>\n"
            "───────────────────\n"
            "Silakan pilih rekening yang sesuai:"
        )
        return {
            "text": text,
            "reply_markup": {"inline_keyboard": buttons},
            "candidate_id": cand_id
        }

    def format_category_menu(self, candidate: TransactionCandidate) -> Dict[str, Any]:
        """
        Renders dynamic category dropdown from Finance Core (MUST NOT hardcode).
        """
        cand_id = candidate.candidate_id
        categories = self.engine.list_categories(active_only=True)

        buttons = []
        row = []
        for cat in categories:
            btn_text = f"📂 {cat.name}"
            cb_data = f"cat:select:{cand_id}:{cat.id}"
            row.append({"text": btn_text, "callback_data": cb_data})
            if len(row) == 2:
                buttons.append(row)
                row = []
        if row:
            buttons.append(row)

        buttons.append([{"text": "🔙 Kembali", "callback_data": f"ced:{cand_id}"}])

        text = (
            "📂 <b>Pilih Kategori</b>\n"
            "───────────────────\n"
            "Silakan pilih kategori transaksi:"
        )
        return {
            "text": text,
            "reply_markup": {"inline_keyboard": buttons},
            "candidate_id": cand_id
        }

    def format_subcategory_menu(self, candidate: TransactionCandidate, category_id: str) -> Optional[Dict[str, Any]]:
        """
        Renders dynamic subcategory dropdown dependent on category_id.
        """
        cand_id = candidate.candidate_id
        subcategories = self.engine.list_subcategories(category_id=category_id, active_only=True)
        if not subcategories:
            return None

        cat = self.engine.get_category(category_id)
        cat_name = cat.name if cat else "Kategori"

        buttons = []
        row = []
        for sub in subcategories:
            btn_text = f"🏷️ {sub.name}"
            cb_data = f"sub:select:{cand_id}:{sub.id}"
            row.append({"text": btn_text, "callback_data": cb_data})
            if len(row) == 2:
                buttons.append(row)
                row = []
        if row:
            buttons.append(row)

        buttons.append([{"text": "⏭️ Lewati / Tanpa Subkategori", "callback_data": f"sub:select:{cand_id}:none"}])
        buttons.append([{"text": "🔙 Kembali", "callback_data": f"ced:{cand_id}"}])

        text = (
            "🏷️ <b>Pilih Subkategori</b>\n"
            "───────────────────\n"
            f"Kategori: <b>{cat_name}</b>\n"
            "Silakan pilih subkategori yang sesuai:"
        )
        return {
            "text": text,
            "reply_markup": {"inline_keyboard": buttons},
            "candidate_id": cand_id
        }

    def format_date_picker(self, candidate: TransactionCandidate, year: Optional[int] = None, month: Optional[int] = None) -> Dict[str, Any]:
        """
        Renders interactive custom Telegram calendar date picker.
        """
        cand_id = candidate.candidate_id
        today = date.today()

        # Parse reference date
        if year is None or month is None:
            cand_date_str = getattr(candidate, "date", None)
            if cand_date_str:
                try:
                    dt = datetime.strptime(cand_date_str, "%Y-%m-%d").date()
                    year = dt.year
                    month = dt.month
                except Exception:
                    year = today.year
                    month = today.month
            else:
                year = today.year
                month = today.month

        # Month navigation logic
        if month == 1:
            prev_year = year - 1
            prev_month = 12
        else:
            prev_year = year
            prev_month = month - 1

        if month == 12:
            next_year = year + 1
            next_month = 1
        else:
            next_year = year
            next_month = month + 1

        prev_month_str = f"{prev_year:04d}-{prev_month:02d}"
        next_month_str = f"{next_year:04d}-{next_month:02d}"

        month_names_id = [
            "", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
            "Juli", "Agustus", "September", "Oktober", "November", "Desember"
        ]
        header_title = f"{month_names_id[month]} {year}"

        keyboard = []

        # Row 0: Month Navigation
        keyboard.append([
            {"text": "⬅️ Bulan Sebelumnya", "callback_data": f"date:month:{cand_id}:{prev_month_str}"},
            {"text": "Bulan Berikutnya ➡️", "callback_data": f"date:month:{cand_id}:{next_month_str}"}
        ])

        # Row 1: Day Header (Sen, Sel, Rab, Kam, Jum, Sab, Min)
        keyboard.append([
            {"text": "Sen", "callback_data": "date:ignore"},
            {"text": "Sel", "callback_data": "date:ignore"},
            {"text": "Rab", "callback_data": "date:ignore"},
            {"text": "Kam", "callback_data": "date:ignore"},
            {"text": "Jum", "callback_data": "date:ignore"},
            {"text": "Sab", "callback_data": "date:ignore"},
            {"text": "Min", "callback_data": "date:ignore"}
        ])

        # Calendar matrix
        cal = calendar.monthcalendar(year, month)
        for week in cal:
            row = []
            for day in week:
                if day == 0:
                    row.append({"text": " ", "callback_data": "date:ignore"})
                else:
                    date_str = f"{year:04d}-{month:02d}-{day:02d}"
                    btn_text = f"📍{day}" if date_str == getattr(candidate, "date", None) else str(day)
                    row.append({"text": btn_text, "callback_data": f"date:select:{cand_id}:{date_str}"})
            keyboard.append(row)

        # Quick actions
        keyboard.append([
            {"text": "📌 Hari Ini", "callback_data": f"date:today:{cand_id}"},
            {"text": "⬅️ Kembali", "callback_data": f"date:back:{cand_id}"}
        ])

        curr_date_display = getattr(candidate, "date", None) or today.isoformat()
        text = (
            "📅 <b>Koreksi Tanggal</b>\n"
            "───────────────────\n"
            f"Tanggal saat ini: <code>{curr_date_display}</code>\n"
            f"Kalender: <b>{header_title}</b>\n"
            "Silakan pilih tanggal pada kalender di bawah:"
        )

        return {
            "text": text,
            "reply_markup": {"inline_keyboard": keyboard},
            "candidate_id": cand_id
        }

    def format_draft_preview(self, candidate: TransactionCandidate) -> Dict[str, Any]:
        """
        Renders Review Changes (Before vs After) prior to ledger write.
        Never mutates ledger immediately.
        """
        cand_id = candidate.candidate_id
        before = candidate.original_state or {}

        b_amt = format_idr(before.get("amount", candidate.amount))
        b_acc = before.get("account_name", candidate.account_name)
        b_dst = before.get("destination_account_name")
        b_cat = before.get("category_name") or "-"
        b_sub = before.get("subcategory_name")
        b_note = before.get("note", candidate.note) or "-"
        b_date = before.get("date")

        a_amt = format_idr(candidate.amount)
        a_acc = candidate.account_name
        a_dst = candidate.destination_account_name
        a_cat = candidate.category_name or "-"
        a_sub = candidate.subcategory_name
        a_note = candidate.note or "-"
        a_date = getattr(candidate, "date", None)

        is_transfer = candidate.direction == "TRANSFER"

        before_lines = [
            f"• Nominal: {b_amt}",
            f"• Akun{' Asal' if is_transfer else ''}: {b_acc}"
        ]
        if is_transfer and b_dst:
            before_lines.append(f"• Akun Tujuan: {b_dst}")
        if not is_transfer:
            before_lines.append(f"• Kategori: {b_cat}")
            if b_sub:
                before_lines.append(f"• Subkategori: {b_sub}")
        before_lines.append(f"• Catatan: {b_note}")
        if b_date:
            before_lines.append(f"• Tanggal: {b_date}")

        after_lines = [
            f"• Nominal: {a_amt}",
            f"• Akun{' Asal' if is_transfer else ''}: {a_acc}"
        ]
        if is_transfer and a_dst:
            after_lines.append(f"• Akun Tujuan: {a_dst}")
        if not is_transfer:
            after_lines.append(f"• Kategori: {a_cat}")
            if a_sub:
                after_lines.append(f"• Subkategori: {a_sub}")
        after_lines.append(f"• Catatan: {a_note}")
        if a_date:
            after_lines.append(f"• Tanggal: {a_date}")

        before_str = "\n".join(before_lines)
        after_str = "\n".join(after_lines)

        text = (
            "🧾 <b>Review Perubahan Draft</b>\n"
            "───────────────────\n"
            "<b>Sebelumnya:</b>\n"
            f"{before_str}\n\n"
            "<b>Setelah Koreksi:</b>\n"
            f"{after_str}\n"
            "───────────────────\n"
            "Simpan perubahan ini ke Buku Besar?"
        )

        buttons = [
            [
                {"text": "✅ Simpan", "callback_data": f"cfm:{cand_id}"},
                {"text": "❌ Batal", "callback_data": f"ccl:{cand_id}"}
            ],
            [
                {"text": "✏️ Koreksi Lagi", "callback_data": f"ced:{cand_id}"}
            ]
        ]

        return {
            "text": text,
            "reply_markup": {"inline_keyboard": buttons},
            "candidate_id": cand_id
        }

    def apply_edit_text(self, chat_id: str, text: str):
        session = self.get_edit_session(chat_id)

        if not session:
            return None

        candidate = self.get_candidate(session["candidate_id"])

        if not candidate:
            self.clear_edit_session(chat_id)
            return None

        # Snapshot original state if not yet set
        if not candidate.original_state:
            candidate.original_state = {
                "amount": candidate.amount,
                "account_name": candidate.account_name,
                "account_id": candidate.account_id,
                "destination_account_name": candidate.destination_account_name,
                "destination_account_id": candidate.destination_account_id,
                "category_name": candidate.category_name,
                "category_id": candidate.category_id,
                "subcategory_name": candidate.subcategory_name,
                "subcategory_id": candidate.subcategory_id,
                "note": candidate.note,
                "date": getattr(candidate, "date", None)
            }

        import re
        lower = text.lower()

        numbers = re.findall(r"\d+", text)

        if "nominal" in lower and numbers:
            candidate.amount = float(numbers[-1])

        elif "catatan" in lower:
            candidate.note = text.split("catatan", 1)[-1].strip()

        elif "kategori" in lower:
            candidate.category_name = text.split("kategori", 1)[-1].strip()

        return candidate

    def stage_input(self, raw_text: str) -> TransactionCandidate:
        candidate = self.parser.parse(raw_text)
        self._candidates[candidate.candidate_id] = candidate
        return candidate

    def get_candidate(self, candidate_id: str) -> Optional[TransactionCandidate]:
        return self._candidates.get(candidate_id)

    def format_confirmation_card(self, candidate: TransactionCandidate) -> Dict[str, Any]:
        """
        Builds the Telegram confirmation card and short-callback inline keyboard.
        """
        if candidate.direction == "TRANSFER":
            card_text = (
                "🧾 <b>Konfirmasi Transfer Dana</b>\n"
                "───────────────────\n"
                f"💰 <b>Nominal:</b> {format_idr(candidate.amount)}\n"
                "🔄 <b>Jenis:</b> Transfer Antar-Rekening 🔁\n"
                f"📤 <b>Dari Rekening:</b> {candidate.account_name}\n"
                f"📥 <b>Ke Rekening:</b> {candidate.destination_account_name}\n"
                f"📝 <b>Catatan:</b> {candidate.note}\n"
                "───────────────────\n"
                "Pindahkan saldo sekarang?"
            )
            reply_markup = {
                "inline_keyboard": [
                    [
                        {"text": "✅ Pindahkan", "callback_data": f"cfm:{candidate.candidate_id}"},
                        {"text": "✏️ Edit", "callback_data": f"ced:{candidate.candidate_id}"},
                        {"text": "❌ Batal", "callback_data": f"ccl:{candidate.candidate_id}"}
                    ]
                ]
            }
            return {
                "text": card_text,
                "reply_markup": reply_markup,
                "candidate_id": candidate.candidate_id
            }

        dir_label = "Pengeluaran 🔴" if candidate.direction == "EXPENSE" else "Pemasukan 🟢"
        cat_label = candidate.category_name if candidate.category_name else "Tanpa Kategori"
        
        card_text = (
            "🧾 <b>Konfirmasi Transaksi</b>\n"
            "───────────────────\n"
            f"💰 <b>Nominal:</b> {format_idr(candidate.amount)}\n"
            f"🔄 <b>Arah:</b> {dir_label}\n"
            f"🏦 <b>Rekening:</b> {candidate.account_name}\n"
            f"🏷️ <b>Kategori:</b> {cat_label}\n"
            f"📝 <b>Catatan:</b> {candidate.note}\n"
            "───────────────────\n"
            "Simpan transaksi ini ke Buku Besar?"
        )

        reply_markup = {
            "inline_keyboard": [
                [
                    {"text": "✅ Simpan", "callback_data": f"cfm:{candidate.candidate_id}"},
                    {"text": "✏️ Edit", "callback_data": f"ced:{candidate.candidate_id}"},
                    {"text": "❌ Batal", "callback_data": f"ccl:{candidate.candidate_id}"}
                ]
            ]
        }

        return {
            "text": card_text,
            "reply_markup": reply_markup,
            "candidate_id": candidate.candidate_id
        }

    def confirm_candidate(self, candidate_id: str) -> Tuple[bool, Optional[Transaction], str]:
        """
        Executes candidate confirmation: validates state, writes to Finance Core ledger,
        and logs audit trail.
        """
        candidate = self.get_candidate(candidate_id)
        if not candidate:
            return False, None, "Transaksi tidak ditemukan atau sesi telah berakhir."

        if candidate.status == "CONFIRMED":
            return False, None, "Transaksi ini sudah pernah dicatat sebelumnya."

        if candidate.status == "CANCELLED":
            return False, None, "Transaksi ini telah dibatalkan."

        # Handle TRANSFER direction
        if candidate.direction == "TRANSFER":
            if not candidate.destination_account_id:
                return False, None, "Rekening tujuan transfer tidak terdefinisi."
            tx_out, tx_in = self.engine.transfer_funds(
                source_account_id=candidate.account_id,
                destination_account_id=candidate.destination_account_id,
                amount=candidate.amount,
                note=candidate.note,
                source="TELEGRAM",
                tx_date=getattr(candidate, "date", None)
            )
            candidate.status = "CONFIRMED"

            src_acc = self.engine.get_account(candidate.account_id)
            dst_acc = self.engine.get_account(candidate.destination_account_id)
            src_bal_str = format_idr(src_acc.balance) if src_acc else "-"
            dst_bal_str = format_idr(dst_acc.balance) if dst_acc else "-"

            receipt_text = (
                "✅ <b>Transfer Berhasil Dicatat!</b>\n"
                "───────────────────\n"
                f"🆔 <b>Ref:</b> <code>{tx_out.id}</code> / <code>{tx_in.id}</code>\n"
                f"💰 <b>Nominal:</b> {format_idr(candidate.amount)}\n"
                f"📤 <b>Dari:</b> {candidate.account_name} (Sisa: {src_bal_str})\n"
                f"📥 <b>Ke:</b> {candidate.destination_account_name} (Saldo: {dst_bal_str})\n"
                "───────────────────\n"
                "<i>Saldo buku besar telah disinkronkan secara atomik.</i>"
            )
            return True, tx_out, receipt_text

        # Write standard EXPENSE / INCOME to authoritative Finance Core
        tx = self.engine.create_transaction(
            account_id=candidate.account_id,
            amount=candidate.amount,
            direction=candidate.direction,
            category_id=candidate.category_id,
            note=candidate.note,
            source="TELEGRAM",
            tx_date=getattr(candidate, "date", None),
            subcategory_id=getattr(candidate, "subcategory_id", None)
        )

        candidate.status = "CONFIRMED"
        
        # Query updated account balance
        acc = self.engine.get_account(candidate.account_id)
        acc_balance_str = format_idr(acc.balance) if acc else "-"

        receipt_text = (
            "✅ <b>Berhasil Dicatat ke Buku Besar!</b>\n"
            "───────────────────\n"
            f"🆔 <b>Ref:</b> <code>{tx.id}</code>\n"
            f"💰 <b>Nominal:</b> {format_idr(tx.amount)}\n"
            f"🏦 <b>Akun:</b> {candidate.account_name}\n"
            f"💳 <b>Sisa Saldo:</b> {acc_balance_str}\n"
            "───────────────────"
        )
        return True, tx, receipt_text

    def cancel_candidate(self, candidate_id: str) -> Tuple[bool, str]:
        candidate = self.get_candidate(candidate_id)
        if not candidate:
            return False, "Transaksi tidak ditemukan atau sesi telah berakhir."

        if candidate.status == "CONFIRMED":
            return False, "Transaksi sudah tersimpan, gunakan pembatalan mutasi di dashboard."

        candidate.status = "CANCELLED"
        return True, "❌ Pencatatan transaksi dibatalkan."

    def handle_update(self, update: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes standard Telegram update object (Message or CallbackQuery).
        """
        if "message" in update and "text" in update["message"]:
            text = update["message"]["text"]
            try:
                candidate = self.stage_input(text)
                card = self.format_confirmation_card(candidate)
                return {
                    "action": "PROMPT_CONFIRMATION",
                    "status": "SUCCESS",
                    "card": card
                }
            except Exception as e:
                return {
                    "action": "ERROR",
                    "status": "FAILED",
                    "message": f"⚠️ Gagal memproses input: {str(e)}"
                }

        elif "callback_query" in update and "data" in update["callback_query"]:
            cb_data = update["callback_query"]["data"]
            if cb_data.startswith("cfm:"):
                cand_id = cb_data.split(":", 1)[1]
                ok, tx, msg = self.confirm_candidate(cand_id)
                return {
                    "action": "TRANSACTION_COMMITTED" if ok else "CONFIRM_FAILED",
                    "status": "SUCCESS" if ok else "ERROR",
                    "message": msg,
                    "transaction_id": tx.id if tx else None
                }
            elif cb_data.startswith("ccl:"):
                cand_id = cb_data.split(":", 1)[1]
                ok, msg = self.cancel_candidate(cand_id)
                return {
                    "action": "TRANSACTION_CANCELLED",
                    "status": "SUCCESS" if ok else "ERROR",
                    "message": msg
                }

        return {
            "action": "IGNORED",
            "status": "NOOP"
        }

# Backward/forward-compatible alias
InteractiveConfirmationHandler = TelegramCaptureAdapter

