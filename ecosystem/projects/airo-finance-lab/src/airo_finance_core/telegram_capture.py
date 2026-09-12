import re
import uuid
import time
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
                created_at=time.time()
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
        cat_rows = conn.execute("SELECT id, name FROM categories ORDER BY id").fetchall()
        chosen_category = None
        
        category_keyword_map = {
            "Makanan & Minuman": ["makan", "minum", "kopi", "sarapan", "lunch", "dinner", "soto", "bakso", "mie", "nasgor", "cafe", "resto", "food"],
            "Transportasi": ["bensin", "bbm", "pertalite", "pertamax", "solar", "gojek", "gocar", "grab", "maxim", "ojol", "parkir", "tol", "transport"],
            "Tagihan & Utilitas": ["listrik", "pln", "air", "pdam", "wifi", "indihome", "biznet", "pulsa", "kuota", "tagihan", "iuran", "bpjs"],
            "Belanja Kebutuhan": ["belanja", "supermarket", "minimarket", "indomaret", "alfamart", "pasar", "sabun", "shampoo"],
            "Gaji & Pemasukan": ["gaji", "payroll", "salary", "bonus", "thr", "dividen", "proyek", "freelance", "pemasukan", "income"]
        }

        for cat_row in cat_rows:
            cat_name = cat_row["name"]
            keywords = category_keyword_map.get(cat_name, [cat_name.lower()])
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
            created_at=time.time()
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
                source="TELEGRAM"
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
            source="TELEGRAM"
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
