import os
import sys
import time
import json
import logging
from .gmail_reliability import receipt, deliver_receipt
import re
import urllib.request
import urllib.parse
import urllib.error
from typing import Optional, Dict, Any, Tuple, Callable, List
from .engine import FinanceCoreEngine
from .telegram_capture import InteractiveConfirmationHandler, SimpleTransactionParser, TransactionCandidate

logger = logging.getLogger("airo_finance_core.telegram_ingress")

def load_telegram_credentials(env_path: Optional[str] = None) -> Tuple[str, str]:
    """
    Safely loads Telegram Bot Token and Owner Chat ID from environment variables
    or from the canonical env file (~/.config/airo/airo-hermes-telegram.env).
    Does NOT store or hardcode secrets in code or git.
    """
    token = os.environ.get("AIRO_HERMES_TELEGRAM_BOT_TOKEN", "").strip()
    owner_id = (
        os.environ.get("OWNER_TELEGRAM_ID") or 
        os.environ.get("AIRO_TELEGRAM_CHAT_ID", "")
    ).strip()

    if not env_path:
        env_path = os.path.expanduser("~/.config/airo/airo-hermes-telegram.env")

    if (not token or not owner_id) and os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("export "):
                        line = line[7:]
                    if "=" in line and not line.startswith("#"):
                        k, v = line.split("=", 1)
                        v = v.strip('"\'')
                        if k == "AIRO_HERMES_TELEGRAM_BOT_TOKEN" and not token:
                            token = v
                        elif k in ("OWNER_TELEGRAM_ID", "AIRO_TELEGRAM_CHAT_ID") and not owner_id:
                            owner_id = v
        except Exception as e:
            logger.warning(f"Could not read env file {env_path}: {e}")

    # Fallback to default canonical owner chat id if unspecified
    if not owner_id:
        owner_id = "8482041086,8263476434"

    return token, str(owner_id)


# Canonical Telegram Bot Commands definition for AIRO Hermes & AIRO Finance
CANONICAL_BOT_COMMANDS = [
    {"command": "help", "description": "Cara menggunakan AIRO Hermes"},
    {"command": "reset", "description": "Mulai percakapan baru"},
    {"command": "about", "description": "Tentang AIRO Hermes"},
    {"command": "memory", "description": "Status memory AIRO Hermes"},
    {"command": "review", "description": "Lihat transaksi yang menunggu review"},
    {"command": "pending", "description": "Kelola transaksi pending AIRO"},
    {"command": "domain", "description": "Catat transaksi manual berdasarkan domain"}
]


class TelegramOutboundAdapter:
    """
    Outbound Telegram HTTP Client for sending cards, editing messages,
    and acknowledging inline callback queries.
    Supports a mock transport function for offline deterministic testing.
    """
    def __init__(self, token: str, transport: Optional[Callable[[str, Dict[str, Any]], Dict[str, Any]]] = None):
        self.token = token
        self.transport = transport or self._default_http_transport

    def _default_http_transport(self, method: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self.token:
            raise ValueError("Telegram Bot Token is required for HTTP transport")

        url = f"https://api.telegram.org/bot{self.token}/{method}"
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=body,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "AIRO-Finance-Lab/1.0"
            }
        )

        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data
        except urllib.error.HTTPError as e:
            raw_err = e.read().decode("utf-8") if e.fp else ""
            logger.error("Telegram API HTTP error %s on %s", e.code, method)
            return {"ok": False, "error_code": e.code, "description": raw_err}
        except Exception as e:
            logger.error("Telegram API request failed on %s: %s", method, type(e).__name__)
            return {"ok": False, "error": type(e).__name__, "uncertain": method == "sendMessage"}

    def send_message(
        self,
        chat_id: str,
        text: str,
        reply_markup: Optional[Dict[str, Any]] = None,
        parse_mode: str = "HTML"
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "chat_id": str(chat_id),
            "text": text,
            "parse_mode": parse_mode
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup
        return self.transport("sendMessage", payload)

    def edit_message_text(
        self,
        chat_id: str,
        message_id: int,
        text: str,
        reply_markup: Optional[Dict[str, Any]] = None,
        parse_mode: str = "HTML"
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "chat_id": str(chat_id),
            "message_id": int(message_id),
            "text": text,
            "parse_mode": parse_mode
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup
        return self.transport("editMessageText", payload)

    def answer_callback_query(
        self,
        callback_query_id: str,
        text: Optional[str] = None,
        show_alert: bool = False
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "callback_query_id": str(callback_query_id),
            "show_alert": show_alert
        }
        if text:
            payload["text"] = text
        return self.transport("answerCallbackQuery", payload)

    def set_my_commands(self, commands: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Registers bot commands with Telegram API via setMyCommands.
        """
        payload: Dict[str, Any] = {
            "commands": commands
        }
        return self.transport("setMyCommands", payload)


class FinanceTelegramIngressRouter:
    """
    Finance Transaction Routing Boundary for Telegram updates.
    Enforces OWNER_TELEGRAM_ID authorization, isolates transaction staging,
    and guarantees all ledger writes route through FinanceCoreEngine via confirmation callbacks.
    """
    def __init__(
        self,
        engine: FinanceCoreEngine,
        outbound: Optional[TelegramOutboundAdapter] = None,
        owner_chat_id: Optional[str] = None,
        auto_register_commands: bool = False
    ):
        self.engine = engine
        self.outbound = outbound
        self.owner_chat_id = str(owner_chat_id) if owner_chat_id else None
        self.confirmation_handler = InteractiveConfirmationHandler(engine)
        self.parser = self.confirmation_handler.parser
        self._card_choices = {}
        from .intake_router import IntakeRouter
        self.intake = IntakeRouter(self)

        if auto_register_commands and self.outbound:
            self.register_bot_commands()

    def register_bot_commands(self, commands: Optional[List[Dict[str, str]]] = None) -> bool:
        """
        Registers canonical bot commands with Telegram Bot API so they appear
        in the command menu (/help, /reset, /about, /memory, /review, /pending, /domain).
        """
        if not self.outbound:
            logger.warning("Cannot register bot commands: outbound adapter is None")
            return False

        cmds = commands or CANONICAL_BOT_COMMANDS
        try:
            res = self.outbound.set_my_commands(cmds)
            if res.get("ok"):
                logger.info(f"Registered {len(cmds)} Telegram bot commands successfully.")
                return True
            else:
                logger.warning(f"Failed to register Telegram bot commands: {res}")
                return False
        except Exception as e:
            logger.error(f"Error registering Telegram bot commands: {e}")
            return False

    def is_owner(self, sender_id: Any) -> bool:
        if not self.owner_chat_id:
            return True
        allowed = [x.strip() for x in str(self.owner_chat_id).split(",") if x.strip()]
        return str(sender_id).strip() in allowed

    def is_finance_message(self, text: str) -> bool:
        """
        Determines whether a message is an intended financial transaction input.
        Must contain valid numeric amount and parseable structure.
        Conversational queries (e.g. 'Halo', 'Sisa budget?') and PC/Office commands return False.
        """
        if not text or not text.strip():
            return False

        stripped = text.strip()
        lower = stripped.lower()

        # 0. Immediate rejection for PC / Office / Media / Assistant automation commands
        non_finance_command_verbs = (
            "buat ", "bikin ", "buka ", "tutup ", "jalankan ", "run ", "start ",
            "play ", "putar ", "cari ", "search ", "browse ", "ketik ", "klik ",
            "tekan ", "scroll ", "screenshot ", "ss ", "tangkap layar ", "tampilkan "
        )
        non_finance_targets = (
            "ppt", "powerpoint", "slide", "slides", "presentasi", "presentation",
            "excel", "spreadsheet", "sheet", "word", "dokumen", "document", "docx",
            "youtube", "yt", "video", "lagu", "musik", "podcast", "browser", "chrome",
            "pc", "laptop", "komputer", "monitor", "layar"
        )
        
        # If it starts with non-finance command verb and contains a non-finance target or 'live'
        if any(lower.startswith(v) for v in non_finance_command_verbs):
            if any(re.search(rf'\b{re.escape(t)}\b', lower) for t in non_finance_targets) or "live" in lower:
                return False

        # If it has PC / Office references combined with personal pronoun or 'live' or action verbs
        if re.search(r'\b(pc|laptop|monitor|browser|youtube|ppt|excel|word)\b', lower) and re.search(r'\b(gw|saya|aku|live|buka|buat|putar)\b', lower):
            return False

        # Check explicit transfer or recording keywords
        if lower.startswith(("trf ", "transfer ", "pindah ", "catat ")):
            return True

        # Try parsing via SimpleTransactionParser
        try:
            amount, _ = self.parser._parse_amount(stripped)
            if amount is None or amount <= 0:
                return False

            # If it has an amount, verify it can produce a candidate
            self.parser.parse(stripped)
            return True
        except Exception:
            return False

    def handle_update(self, update: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Dispatches incoming Telegram update.
        Returns:
            (handled: bool, reason: str)
            If handled is True, update was consumed by Finance Ingress and should NOT route to Hermes LLM.
            If handled is False, update is non-financial and should pass through to Hermes LLM queue.
        """
        result = self.intake.handle(update)
        if result is not None:
            return result

        # 1. Handle Callback Query (Confirmation / Cancellation)
        if "callback_query" in update:
            cq = update["callback_query"]
            cq_id = str(cq.get("id", ""))
            data = cq.get("data", "")
            sender_id = str(cq.get("from", {}).get("id", ""))
            msg = cq.get("message", {})
            chat_id = str(msg.get("chat", {}).get("id", sender_id))
            message_id = msg.get("message_id")

            if data.startswith("dtype:") or data.startswith("ccpick:"):
                if not self.is_owner(sender_id): return True, "BLOCKED_NON_OWNER_CALLBACK"
                if data.startswith("dtype:"):
                    _, candidate_id, direction = data.split(":",2)
                    candidate=self.confirmation_handler.get_candidate(candidate_id)
                    if direction not in ("EXPENSE","INCOME","TRANSFER","CC_PAYMENT"): return True,"INVALID_DIRECTION"
                    if not candidate or candidate.status!='PENDING': return True,"STALE_DRAFT"
                    candidate.direction=direction;candidate.direction_confirmed=True
                else:
                    choice=self._card_choices.get(data.split(":",1)[1])
                    if not choice:return True,"STALE_CARD_CHOICE"
                    candidate=self.confirmation_handler.get_candidate(choice[0])
                    if not candidate or candidate.status!='PENDING':return True,"STALE_DRAFT"
                    candidate.credit_card_id=choice[1]
                menu=self.confirmation_handler.format_guided_edit_menu(candidate)
                if self.outbound and message_id:
                    self.outbound.edit_message_text(chat_id,message_id,menu['text'],reply_markup=menu['reply_markup'])
                    self.outbound.answer_callback_query(cq_id,text="Pilihan disimpan")
                return True,"EDIT_SELECTION_UPDATED"

            # Check if this is a finance confirmation callback
            # Check if this is a finance draft edit callback (Unified Draft Editor V1)
            if data.startswith("ced:"):
                if not self.is_owner(sender_id):
                    logger.warning(f"BLOCKED: Non-owner edit attempt from {sender_id}")
                    if self.outbound:
                        self.outbound.answer_callback_query(
                            cq_id,
                            text="⛔ Akses ditolak: Hanya Owner yang berhak mengedit transaksi.",
                            show_alert=True
                        )
                    return True, "BLOCKED_NON_OWNER_CALLBACK"

                action, candidate_id = data.split(":", 1)
                candidate = self.confirmation_handler.get_candidate(candidate_id)

                if not candidate:
                    if self.outbound:
                        self.outbound.answer_callback_query(
                            cq_id,
                            text="⚠️ Draft transaksi tidak ditemukan.",
                            show_alert=True
                        )
                    return True, f"EDIT_FAILED_NOT_FOUND:{candidate_id}"

                if candidate.status != "PENDING":
                    if self.outbound:
                        self.outbound.answer_callback_query(
                            cq_id,
                            text="⚠️ Draft sudah tidak aktif.",
                            show_alert=True
                        )
                    return True, f"EDIT_FAILED_STATUS:{candidate.status}"

                self.confirmation_handler.start_edit_session(
                    chat_id,
                    candidate_id,
                    field=None
                )

                menu = self.confirmation_handler.format_guided_edit_menu(candidate)
                if self.outbound and message_id:
                    self.outbound.edit_message_text(
                        chat_id,
                        message_id,
                        menu["text"],
                        reply_markup=menu["reply_markup"]
                    )
                    self.outbound.answer_callback_query(
                        cq_id,
                        text="Apa yang mau dikoreksi?"
                    )

                return True, f"GUIDED_EDIT_MENU:{candidate_id}"

            # Field Selection Callback (edf:<candidate_id>:<field_code>)
            if data.startswith("edf:"):
                if not self.is_owner(sender_id):
                    logger.warning(f"BLOCKED: Non-owner edit attempt from {sender_id}")
                    if self.outbound:
                        self.outbound.answer_callback_query(
                            cq_id,
                            text="⛔ Akses ditolak: Hanya Owner yang berhak mengedit transaksi.",
                            show_alert=True
                        )
                    return True, "BLOCKED_NON_OWNER_CALLBACK"

                _, candidate_id, field_code = data.split(":", 2)
                candidate = self.confirmation_handler.get_candidate(candidate_id)
                if not candidate or candidate.status != "PENDING":
                    if self.outbound:
                        self.outbound.answer_callback_query(cq_id, text="⚠️ Draft tidak aktif.", show_alert=True)
                    return True, f"EDIT_FAILED_STATUS:{candidate_id}"

                if field_code == "amt":
                    self.confirmation_handler.start_edit_session(chat_id, candidate_id, field="amount")
                    prompt_text = (
                        "💰 <b>Koreksi Nominal</b>\n"
                        "───────────────────\n"
                        "Kirim nominal baru (contoh: <code>50000</code>, <code>75k</code>, <code>1.5jt</code>):"
                    )
                    back_markup = {"inline_keyboard": [[{"text": "🔙 Kembali", "callback_data": f"ced:{candidate_id}"}]]}
                    if self.outbound and message_id:
                        self.outbound.edit_message_text(chat_id, message_id, prompt_text, reply_markup=back_markup)
                        self.outbound.answer_callback_query(cq_id, text="Kirim nominal baru")
                    return True, "EDIT_FIELD_PROMPTED:amount"

                elif field_code == "not":
                    self.confirmation_handler.start_edit_session(chat_id, candidate_id, field="note")
                    prompt_text = (
                        "📝 <b>Koreksi Catatan</b>\n"
                        "───────────────────\n"
                        "Kirim catatan baru untuk transaksi ini:"
                    )
                    back_markup = {"inline_keyboard": [[{"text": "🔙 Kembali", "callback_data": f"ced:{candidate_id}"}]]}
                    if self.outbound and message_id:
                        self.outbound.edit_message_text(chat_id, message_id, prompt_text, reply_markup=back_markup)
                        self.outbound.answer_callback_query(cq_id, text="Kirim catatan baru")
                    return True, "EDIT_FIELD_PROMPTED:note"

                elif field_code in ("typ","cc"):
                    rows=[]
                    if field_code=='typ':
                        rows=[[{'text':direction,'callback_data':f'dtype:{candidate_id}:{direction}'}] for direction in ('EXPENSE','INCOME','TRANSFER','CC_PAYMENT')]
                    else:
                        import uuid
                        for card in self.engine.db.get_connection().execute('SELECT id,name FROM credit_cards WHERE is_active=1'):
                            token=uuid.uuid4().hex[:12];self._card_choices[token]=(candidate_id,card['id'])
                            rows.append([{'text':card['name'],'callback_data':'ccpick:'+token}])
                    if self.outbound and message_id:
                        self.outbound.edit_message_text(chat_id,message_id,'Pilih jenis transaksi / kartu tujuan:',reply_markup={'inline_keyboard':rows})
                        self.outbound.answer_callback_query(cq_id,text="Pilih opsi")
                    return True,"EDIT_TYPE_OR_CARD_MENU"

                elif field_code == "dat":
                    self.confirmation_handler.clear_edit_session(chat_id)
                    picker = self.confirmation_handler.format_date_picker(candidate)
                    if self.outbound and message_id:
                        self.outbound.edit_message_text(chat_id, message_id, picker["text"], reply_markup=picker["reply_markup"])
                        self.outbound.answer_callback_query(cq_id, text="Pilih tanggal transaksi")
                    return True, f"DATE_PICKER_OPEN:{candidate_id}"

                elif field_code in ("acc", "src"):
                    acc_menu = self.confirmation_handler.format_account_menu(candidate, target="src")
                    if self.outbound and message_id:
                        self.outbound.edit_message_text(chat_id, message_id, acc_menu["text"], reply_markup=acc_menu["reply_markup"])
                        self.outbound.answer_callback_query(cq_id, text="Pilih rekening")
                    return True, f"EDIT_ACCOUNT_MENU:{candidate_id}"

                elif field_code == "dst":
                    acc_menu = self.confirmation_handler.format_account_menu(candidate, target="dst")
                    if self.outbound and message_id:
                        self.outbound.edit_message_text(chat_id, message_id, acc_menu["text"], reply_markup=acc_menu["reply_markup"])
                        self.outbound.answer_callback_query(cq_id, text="Pilih rekening tujuan")
                    return True, f"EDIT_DST_ACCOUNT_MENU:{candidate_id}"

                elif field_code == "cat":
                    cat_menu = self.confirmation_handler.format_category_menu(candidate)
                    if self.outbound and message_id:
                        self.outbound.edit_message_text(chat_id, message_id, cat_menu["text"], reply_markup=cat_menu["reply_markup"])
                        self.outbound.answer_callback_query(cq_id, text="Pilih kategori")
                    return True, f"EDIT_CATEGORY_MENU:{candidate_id}"

            # Account Selection Callback (acc:select:<candidate_id>:<account_id> or eda:<candidate_id>:<account_id>)
            if data.startswith("acc:select:") or data.startswith("eda:"):
                if not self.is_owner(sender_id):
                    logger.warning(f"BLOCKED: Non-owner callback from {sender_id}")
                    return True, "BLOCKED_NON_OWNER_CALLBACK"
                if data.startswith("acc:select:"):
                    parts = data.split(":")
                    candidate_id = parts[2]
                    acc_id = parts[3]
                else:
                    _, candidate_id, acc_id = data.split(":", 2)
                candidate = self.confirmation_handler.apply_field_update(candidate_id, "account", acc_id)
                if candidate:
                    preview = self.confirmation_handler.format_draft_preview(candidate)
                    if self.outbound and message_id:
                        self.outbound.edit_message_text(chat_id, message_id, preview["text"], reply_markup=preview["reply_markup"])
                        self.outbound.answer_callback_query(cq_id, text="Rekening diperbarui")
                    return True, f"DRAFT_ACCOUNT_UPDATED:{candidate_id}"

            # Destination Account Selection Callback (acc:dst:<candidate_id>:<account_id> or edd:<candidate_id>:<account_id>)
            if data.startswith("acc:dst:") or data.startswith("edd:"):
                if not self.is_owner(sender_id):
                    logger.warning(f"BLOCKED: Non-owner callback from {sender_id}")
                    return True, "BLOCKED_NON_OWNER_CALLBACK"
                if data.startswith("acc:dst:"):
                    parts = data.split(":")
                    candidate_id = parts[2]
                    acc_id = parts[3]
                else:
                    _, candidate_id, acc_id = data.split(":", 2)
                candidate = self.confirmation_handler.apply_field_update(candidate_id, "dst_account", acc_id)
                if candidate:
                    preview = self.confirmation_handler.format_draft_preview(candidate)
                    if self.outbound and message_id:
                        self.outbound.edit_message_text(chat_id, message_id, preview["text"], reply_markup=preview["reply_markup"])
                        self.outbound.answer_callback_query(cq_id, text="Rekening tujuan diperbarui")
                    return True, f"DRAFT_DST_ACCOUNT_UPDATED:{candidate_id}"

            # Category Selection Callback (cat:select:<candidate_id>:<category_id> or edc:<candidate_id>:<category_id>)
            if data.startswith("cat:select:") or data.startswith("edc:"):
                if not self.is_owner(sender_id):
                    logger.warning(f"BLOCKED: Non-owner callback from {sender_id}")
                    return True, "BLOCKED_NON_OWNER_CALLBACK"
                if data.startswith("cat:select:"):
                    parts = data.split(":")
                    candidate_id = parts[2]
                    cat_id = parts[3]
                else:
                    _, candidate_id, cat_id = data.split(":", 2)
                candidate = self.confirmation_handler.apply_field_update(candidate_id, "category", cat_id)
                if candidate:
                    sub_menu = self.confirmation_handler.format_subcategory_menu(candidate, cat_id)
                    if sub_menu:
                        if self.outbound and message_id:
                            self.outbound.edit_message_text(chat_id, message_id, sub_menu["text"], reply_markup=sub_menu["reply_markup"])
                            self.outbound.answer_callback_query(cq_id, text="Pilih subkategori")
                        return True, f"SUBCATEGORY_MENU:{cat_id}"
                    else:
                        preview = self.confirmation_handler.format_draft_preview(candidate)
                        if self.outbound and message_id:
                            self.outbound.edit_message_text(chat_id, message_id, preview["text"], reply_markup=preview["reply_markup"])
                            self.outbound.answer_callback_query(cq_id, text="Kategori diperbarui")
                        return True, f"DRAFT_CATEGORY_UPDATED:{candidate_id}"

            # Subcategory Selection Callback (sub:select:<candidate_id>:<subcategory_id> or eds:<candidate_id>:<subcategory_id>)
            if data.startswith("sub:select:") or data.startswith("eds:"):
                if not self.is_owner(sender_id):
                    logger.warning(f"BLOCKED: Non-owner callback from {sender_id}")
                    return True, "BLOCKED_NON_OWNER_CALLBACK"
                if data.startswith("sub:select:"):
                    parts = data.split(":")
                    candidate_id = parts[2]
                    subc_id = parts[3]
                else:
                    _, candidate_id, subc_id = data.split(":", 2)
                candidate = self.confirmation_handler.apply_field_update(candidate_id, "subcategory", subc_id)
                if candidate:
                    preview = self.confirmation_handler.format_draft_preview(candidate)
                    if self.outbound and message_id:
                        self.outbound.edit_message_text(chat_id, message_id, preview["text"], reply_markup=preview["reply_markup"])
                        self.outbound.answer_callback_query(cq_id, text="Subkategori diperbarui")
                    return True, f"DRAFT_SUBCATEGORY_UPDATED:{candidate_id}"

            # Interactive Date Picker Callbacks (date:select, date:month, date:today, date:back, date:ignore)
            if data.startswith("date:"):
                if not self.is_owner(sender_id):
                    logger.warning(f"BLOCKED: Non-owner date callback from {sender_id}")
                    return True, "BLOCKED_NON_OWNER_CALLBACK"

                parts = data.split(":")
                action = parts[1]

                if action == "ignore":
                    if self.outbound:
                        self.outbound.answer_callback_query(cq_id)
                    return True, "DATE_IGNORE"

                candidate_id = parts[2]
                candidate = self.confirmation_handler.get_candidate(candidate_id)
                if not candidate or candidate.status != "PENDING":
                    if self.outbound:
                        self.outbound.answer_callback_query(cq_id, text="⚠️ Draft tidak aktif atau sudah selesai.", show_alert=True)
                    return True, "DATE_FAILED_STATUS"

                if action == "month":
                    year_str, month_str = parts[3].split("-")
                    picker = self.confirmation_handler.format_date_picker(candidate, year=int(year_str), month=int(month_str))
                    if self.outbound and message_id:
                        self.outbound.edit_message_text(chat_id, message_id, picker["text"], reply_markup=picker["reply_markup"])
                        self.outbound.answer_callback_query(cq_id)
                    return True, f"DATE_MONTH_CHANGED:{parts[3]}"

                elif action == "today":
                    from datetime import date as dt_date
                    today_str = dt_date.today().isoformat()
                    candidate = self.confirmation_handler.apply_field_update(candidate_id, "date", today_str)
                    if candidate:
                        preview = self.confirmation_handler.format_draft_preview(candidate)
                        if self.outbound and message_id:
                            self.outbound.edit_message_text(chat_id, message_id, preview["text"], reply_markup=preview["reply_markup"])
                            self.outbound.answer_callback_query(cq_id, text="Tanggal diset hari ini")
                        return True, f"DRAFT_DATE_UPDATED:{candidate_id}"

                elif action == "select":
                    selected_date = parts[3]
                    candidate = self.confirmation_handler.apply_field_update(candidate_id, "date", selected_date)
                    if candidate:
                        preview = self.confirmation_handler.format_draft_preview(candidate)
                        if self.outbound and message_id:
                            self.outbound.edit_message_text(chat_id, message_id, preview["text"], reply_markup=preview["reply_markup"])
                            self.outbound.answer_callback_query(cq_id, text=f"Tanggal dipilih: {selected_date}")
                        return True, f"DRAFT_DATE_UPDATED:{candidate_id}"

                elif action == "back":
                    menu = self.confirmation_handler.format_guided_edit_menu(candidate)
                    if self.outbound and message_id:
                        self.outbound.edit_message_text(chat_id, message_id, menu["text"], reply_markup=menu["reply_markup"])
                        self.outbound.answer_callback_query(cq_id)
                    return True, f"GUIDED_EDIT_MENU:{candidate_id}"

            # Domain Selection Callbacks (dom:new:<type>, dom:cancel)
            if data.startswith("dom:"):
                if not self.is_owner(sender_id):
                    logger.warning(f"BLOCKED: Non-owner domain callback from {sender_id}")
                    if self.outbound:
                        self.outbound.answer_callback_query(cq_id, text="⛔ Akses ditolak: Hanya Owner yang berhak.", show_alert=True)
                    return True, "BLOCKED_NON_OWNER_CALLBACK"

                if data == "dom:cancel":
                    if self.outbound and message_id:
                        self.outbound.edit_message_text(chat_id, message_id, "❌ Pencatatan domain dibatalkan.", reply_markup={"inline_keyboard": []})
                        self.outbound.answer_callback_query(cq_id, text="Dibatalkan")
                    return True, "DOMAIN_ENTRY_CANCELLED"

                if data.startswith("dom:new:"):
                    dom_type = data.split(":", 2)[2]
                    dom_names = {
                        "expense": ("Pengeluaran", "EXPENSE", "Contoh: <code>makan siang 35k bca</code>"),
                        "income": ("Pemasukan", "INCOME", "Contoh: <code>gaji masuk 15jt mandiri</code>"),
                        "transfer": ("Transfer Saldo", "TRANSFER", "Contoh: <code>trf 500k dari bca ke blu</code>"),
                        "credit_card": ("Kartu Kredit", "CREDIT_CARD", "Contoh: <code>tokopedia belanja 250k</code>"),
                        "debt": ("Utang / Piutang", "DEBT", "Contoh: <code>pinjam uang 1jt</code> atau <code>bayar cicilan 500k</code>"),
                        "asset": ("Aset Investasi", "ASSET", "Contoh: <code>beli emas 2 gram 2.6jt</code>")
                    }
                    info = dom_names.get(dom_type, ("Transaksi", "EXPENSE", "Kirim detail transaksi"))
                    title, _, example = info
                    text_msg = (
                        f"📝 <b>Pencatatan {title}</b>\n"
                        "───────────────────\n"
                        f"Silakan kirim detail {title.lower()}.\n"
                        f"{example}"
                    )
                    if self.outbound and message_id:
                        self.outbound.edit_message_text(chat_id, message_id, text_msg, reply_markup={"inline_keyboard": [[{"text": "❌ Batal", "callback_data": "dom:cancel"}]]})
                        self.outbound.answer_callback_query(cq_id, text=f"Domain {title} dipilih")
                    return True, f"DOMAIN_PROMPTED:{dom_type}"

            if data.startswith("cfm:") or data.startswith("ccl:"):
                # Enforce Owner Authorization
                if not self.is_owner(sender_id):
                    logger.warning(f"BLOCKED: Non-owner callback from {sender_id}")
                    if self.outbound:
                        self.outbound.answer_callback_query(
                            cq_id,
                            text="⛔ Akses ditolak: Hanya Owner yang berhak mengonfirmasi transaksi.",
                            show_alert=True
                        )
                    return True, "BLOCKED_NON_OWNER_CALLBACK"

                action, candidate_id = data.split(":", 1)
                
                if action == "cfm":
                    self.confirmation_handler.clear_edit_session(chat_id)
                    cand = self.confirmation_handler.get_candidate(candidate_id)
                    if candidate_id.startswith("rq_") and cand:
                        try:
                            override_data = {
                                "amount": cand.amount,
                                "direction": cand.direction,
                                "credit_card_id": cand.credit_card_id,
                                "account_id": cand.account_id,
                                "category_id": cand.category_id,
                                "subcategory_id": getattr(cand, "subcategory_id", None),
                                "note": cand.note,
                                "date": getattr(cand, "date", None),
                            }
                            if not cand.direction_confirmed:
                                override_data.pop("direction", None)
                            if cand.destination_account_id:
                                override_data["destination_account_id"] = cand.destination_account_id
                            item, tx = self.engine.approve_review_item(candidate_id, override_data=override_data, receipt_target=(chat_id, message_id) if self.outbound and message_id else None)
                            cand.status = "CONFIRMED"
                            acc = self.engine.get_account(cand.account_id)
                            acc_balance_str = f"Rp{int(round(acc.balance)):,}".replace(",", ".") if acc else "-"
                            card_receipt = receipt(self.engine, tx)
                            if self.outbound and message_id:
                                deliver_receipt(self.engine, self.outbound, chat_id, message_id, tx)
                                self.outbound.answer_callback_query(cq_id, text="✅ Transaksi Disetujui & Disimpan")
                            return True, f"GMAIL_CONFIRMED:{tx.id}"
                        except Exception as e:
                            logger.error(f"Error approving review queue candidate {candidate_id}: {e}")
                            if self.outbound and message_id:
                                self.outbound.answer_callback_query(cq_id, text=f"⚠️ {e}", show_alert=True)
                            return True, f"CONFIRM_FAILED:{e}"

                    ok, tx, status_msg = self.confirmation_handler.confirm_candidate(candidate_id, receipt_target=(chat_id, message_id) if self.outbound and message_id else None)
                    if ok and tx:
                        card_receipt = receipt(self.engine, tx)
                        if self.outbound and message_id:
                            deliver_receipt(self.engine, self.outbound, chat_id, message_id, tx)
                            self.outbound.answer_callback_query(cq_id, text="✅ Transaksi Tersimpan")
                        return True, f"CONFIRMED:{tx.id}"
                    else:
                        if self.outbound and message_id:
                            self.outbound.answer_callback_query(cq_id, text=f"⚠️ {status_msg}", show_alert=True)
                        return True, f"CONFIRM_FAILED:{status_msg}"

                elif action == "ccl":
                    self.confirmation_handler.clear_edit_session(chat_id)
                    if candidate_id.startswith("rq_"):
                        try:
                            self.engine.ignore_review_item(candidate_id, reason="Dibatalkan via editor Telegram")
                        except Exception as ex:
                            logger.warning(f"Could not ignore review item {candidate_id}: {ex}")
                    ok, status_msg = self.confirmation_handler.cancel_candidate(candidate_id)
                    cancel_receipt = (
                        "❌ <b>Pencatatan Dibatalkan</b>\n"
                        "───────────────────\n"
                        "Transaksi ini telah dibatalkan tanpa mutasi saldo."
                    )
                    if self.outbound and message_id:
                        self.outbound.edit_message_text(chat_id, message_id, cancel_receipt, reply_markup={"inline_keyboard": []})
                        self.outbound.answer_callback_query(cq_id, text="❌ Transaksi Dibatalkan")
                    return True, "CANCELLED"

            # Check if this is a Gmail candidate review callback (Phase 5)
            elif data.startswith("gma:") or data.startswith("gmi:") or data.startswith("gmc:"):
                if not self.is_owner(sender_id):
                    logger.warning(f"BLOCKED: Non-owner callback from {sender_id}")
                    if self.outbound:
                        self.outbound.answer_callback_query(
                            cq_id,
                            text="⛔ Akses ditolak: Hanya Owner yang berhak mengonfirmasi transaksi.",
                            show_alert=True
                        )
                    return True, "BLOCKED_NON_OWNER_CALLBACK"

                action, review_id = data.split(":", 1)
                if action == "gma":
                    current_item = self.engine.get_review_queue_item(review_id)

                    if current_item is None:
                        if self.outbound:
                            self.outbound.answer_callback_query(
                                cq_id,
                                text="⚠️ Review transaksi ini sudah tidak aktif.",
                                show_alert=True
                            )
                        return True, f"GMAIL_STALE_REVIEW:{review_id}"

                    if current_item.status != "PENDING":
                        if self.outbound:
                            self.outbound.answer_callback_query(
                                cq_id,
                                text=f"ℹ️ Transaksi ini sudah {current_item.status.lower()}.",
                                show_alert=True
                            )
                        return True, f"GMAIL_ALREADY_{current_item.status}:{review_id}"

                    try:
                        item, tx = self.engine.approve_review_item(review_id, receipt_target=(chat_id, message_id) if self.outbound and message_id else None)
                        if tx.direction == "TRANSFER":
                            card_receipt = receipt(self.engine, tx)
                        else:
                            card_receipt = receipt(self.engine, tx)
                        if self.outbound and message_id:
                            deliver_receipt(self.engine, self.outbound, chat_id, message_id, tx)
                            self.outbound.answer_callback_query(cq_id, text="✅ Transaksi Disetujui")
                        return True, f"GMAIL_CONFIRMED:{tx.id}"
                    except Exception as e:
                        if "already" in str(e).lower():
                            if self.outbound:
                                self.outbound.answer_callback_query(cq_id, text="ℹ️ Transaksi ini sudah diproses sebelumnya.", show_alert=True)
                            return True, f"GMAIL_ALREADY_PROCESSED:{review_id}"
                        if self.outbound:
                            self.outbound.answer_callback_query(cq_id, text=f"⚠️ {e}", show_alert=True)
                        return True, "GMAIL_CONFIRM_FAILED:Review item sudah tidak aktif. Kemungkinan sudah diproses atau expired."

                elif action == "gmi":
                    try:
                        self.engine.ignore_review_item(review_id, reason="Diabaikan via Telegram")
                        ignore_receipt = (
                            "❌ <b>Transaksi Gmail Diabaikan</b>\n"
                            "───────────────────\n"
                            "Transaksi ini tidak dicatat ke buku besar."
                        )
                        if self.outbound and message_id:
                            self.outbound.edit_message_text(chat_id, message_id, ignore_receipt, reply_markup={"inline_keyboard": []})
                            self.outbound.answer_callback_query(cq_id, text="❌ Transaksi Diabaikan")
                        return True, "GMAIL_IGNORED"
                    except Exception as e:
                        if "already" in str(e).lower():
                            if self.outbound:
                                self.outbound.answer_callback_query(cq_id, text="ℹ️ Transaksi ini sudah diproses sebelumnya.", show_alert=True)
                            return True, f"GMAIL_ALREADY_PROCESSED:{review_id}"
                        if self.outbound:
                            self.outbound.answer_callback_query(cq_id, text=f"⚠️ {e}", show_alert=True)
                        return True, f"GMAIL_IGNORE_FAILED:{e}"

                elif action == "gmc":
                    current_item = self.engine.get_review_queue_item(review_id)
                    if not current_item or current_item.status != "PENDING":
                        if self.outbound:
                            self.outbound.answer_callback_query(
                                cq_id,
                                text="⚠️ Transaksi review ini sudah tidak aktif atau sudah diproses.",
                                show_alert=True
                            )
                        return True, f"GMAIL_REVIEW_NOT_PENDING:{review_id}"

                    parsed = {}
                    try:
                        parsed = json.loads(current_item.parsed_result)
                    except Exception:
                        pass

                    cand = TransactionCandidate(
                        candidate_id=review_id,
                        raw_text=current_item.raw_text or "",
                        amount=float(parsed.get("amount") or 0.0),
                        direction=str(parsed.get("direction") or "EXPENSE").upper(),
                        account_id=str(parsed.get("account_id") or ""),
                        account_name=str(parsed.get("account_name") or ""),
                        category_id=parsed.get("category_id"),
                        category_name=parsed.get("category_name"),
                        subcategory_id=parsed.get("subcategory_id"),
                        subcategory_name=parsed.get("subcategory_name"),
                        note=str(parsed.get("note") or parsed.get("merchant") or "Deteksi Gmail"),
                        status="PENDING",
                        created_at=time.time(),
                        date=parsed.get("date"),
                        tx_type=str(parsed.get("tx_type") or "EXPENSE"),
                        original_state=dict(parsed),
                        direction_confirmed=parsed.get("direction_known", True),
                        destination_account_id=parsed.get("destination_account_id"),
                        destination_account_name=parsed.get("destination_account_name"),
                        credit_card_id=parsed.get("credit_card_id")
                    )

                    if cand.account_id and not cand.account_name:
                        acc = self.engine.get_account(cand.account_id)
                        if acc:
                            cand.account_name = acc.name
                    elif cand.account_name and not cand.account_id:
                        for acc in self.engine.list_accounts():
                            if acc.name.lower() == cand.account_name.lower():
                                cand.account_id = acc.id
                                break
                    if cand.category_id and not cand.category_name:
                        cat = self.engine.get_category(cand.category_id)
                        if cat:
                            cand.category_name = cat.name
                    elif cand.category_name and not cand.category_id:
                        for cat in self.engine.list_categories():
                            if cat.name.lower() == cand.category_name.lower():
                                cand.category_id = cat.id
                                break

                    # Save candidate to confirmation handler
                    self.confirmation_handler._candidates[review_id] = cand
                    self.confirmation_handler.start_edit_session(chat_id, review_id, field=None)
                    menu = self.confirmation_handler.format_guided_edit_menu(cand)
                    if self.outbound and message_id:
                        self.outbound.edit_message_text(chat_id, message_id, menu["text"], reply_markup=menu["reply_markup"])
                        self.outbound.answer_callback_query(cq_id, text="✏️ Membuka mode edit...")
                    return True, f"GMAIL_EDIT_STARTED:{review_id}"

            else:
                logger.warning(f"Unhandled callback data: {data}")
                if self.outbound:
                    self.outbound.answer_callback_query(cq_id, text="⚠️ Aksi tidak dikenali")
                return True, f"UNHANDLED_CALLBACK:{data}"

        # 2. Handle Message (Quick Capture Transaction Input)
        if "message" in update:
            msg = update["message"]
            chat_id = str(msg.get("chat", {}).get("id", ""))
            sender_id = str(msg.get("from", {}).get("id", chat_id))
            message_id = msg.get("message_id")
            text = msg.get("text", "")

            if not text or not text.strip():
                return False, "EMPTY_MESSAGE"

            # Check if user is in an active edit session
            edit_session = self.confirmation_handler.get_edit_session(chat_id)
            if edit_session:
                if not self.is_owner(sender_id):
                    logger.warning(f"BLOCKED: Non-owner edit attempt from {sender_id}")
                    if self.outbound:
                        self.outbound.send_message(
                            sender_id,
                            "⛔ <b>Akses Ditolak</b>: Anda tidak memiliki izin untuk mengubah draft transaksi."
                        )
                    return True, "BLOCKED_NON_OWNER_WRITE"

                cand_id = edit_session.get("candidate_id")
                active_field = edit_session.get("field")

                try:
                    if active_field == "amount":
                        amt, _ = self.parser._parse_amount(text)
                        if amt is None or amt <= 0:
                            if self.outbound:
                                self.outbound.send_message(chat_id, "⚠️ Nominal tidak valid. Masukkan angka (misal 50000 atau 50k):")
                            return True, "EDIT_AMOUNT_INVALID"
                        edited_candidate = self.confirmation_handler.apply_field_update(cand_id, "amount", amt)
                        edit_session["field"] = None
                        if edited_candidate:
                            preview = self.confirmation_handler.format_draft_preview(edited_candidate)
                            if self.outbound:
                                self.outbound.send_message(chat_id, preview["text"], reply_markup=preview["reply_markup"])
                            return True, f"DRAFT_AMOUNT_UPDATED:{cand_id}"

                    elif active_field == "note":
                        edited_candidate = self.confirmation_handler.apply_field_update(cand_id, "note", text)
                        edit_session["field"] = None
                        if edited_candidate:
                            preview = self.confirmation_handler.format_draft_preview(edited_candidate)
                            if self.outbound:
                                self.outbound.send_message(chat_id, preview["text"], reply_markup=preview["reply_markup"])
                            return True, f"DRAFT_NOTE_UPDATED:{cand_id}"

                    elif active_field == "date":
                        edited_candidate = self.confirmation_handler.apply_field_update(cand_id, "date", text)
                        edit_session["field"] = None
                        if edited_candidate:
                            preview = self.confirmation_handler.format_draft_preview(edited_candidate)
                            if self.outbound:
                                self.outbound.send_message(chat_id, preview["text"], reply_markup=preview["reply_markup"])
                            return True, f"DRAFT_DATE_UPDATED:{cand_id}"

                    else:
                        edited_candidate = self.confirmation_handler.apply_edit_text(
                            str(chat_id),
                            text
                        )
                        if edited_candidate:
                            preview = self.confirmation_handler.format_draft_preview(edited_candidate)
                            if self.outbound:
                                self.outbound.send_message(
                                    chat_id,
                                    preview["text"],
                                    reply_markup=preview["reply_markup"]
                                )
                            return True, f"DRAFT_EDIT_UPDATED:{edited_candidate.candidate_id}"
                except Exception as e:
                    logger.error(f"Error applying draft edit: {e}")
                    if self.outbound:
                        self.outbound.send_message(
                            chat_id,
                            f"⚠️ <b>Format Koreksi Kurang Tepat</b>: {e}"
                        )
                    return True, f"DRAFT_EDIT_ERROR:{e}"

            # Check for Safe-to-Spend on-demand command (Phase 2.2)
            lower_text = text.strip().lower()
            if lower_text in ("/safetospend", "safe to spend") or lower_text.startswith(("/safetospend", "uang aman")):
                if not self.is_owner(sender_id):
                    logger.warning(f"BLOCKED: Non-owner read attempt from {sender_id}")
                    if self.outbound:
                        self.outbound.send_message(
                            sender_id,
                            "⛔ <b>Akses Ditolak</b>: Anda tidak memiliki izin untuk melihat data keuangan."
                        )
                    return True, "BLOCKED_NON_OWNER_READ"

                from .insights import FinanceInsightsService
                from .hermes_adapter import FinanceHermesReadAdapter
                insights_svc = FinanceInsightsService(self.engine.db)
                adapter = FinanceHermesReadAdapter(insights_svc)
                card_text = adapter.format_safe_to_spend_telegram_card()
                if self.outbound:
                    self.outbound.send_message(sender_id, card_text)
                return True, "SAFE_TO_SPEND_CARD_SENT"

            # Check for Weekly Recap on-demand command (Phase 2.3)
            if lower_text in ("/rekap", "/weekly", "rekap minggu ini", "evaluasi mingguan", "pengeluaran 7 hari terakhir") or lower_text.startswith(("/rekap", "/weekly", "rekap minggu")):
                if not self.is_owner(sender_id):
                    logger.warning(f"BLOCKED: Non-owner read attempt from {sender_id}")
                    if self.outbound:
                        self.outbound.send_message(
                            sender_id,
                            "⛔ <b>Akses Ditolak</b>: Anda tidak memiliki izin untuk melihat data keuangan."
                        )
                    return True, "BLOCKED_NON_OWNER_READ"

                from .insights import FinanceInsightsService
                from .hermes_adapter import FinanceHermesReadAdapter
                insights_svc = FinanceInsightsService(self.engine.db)
                adapter = FinanceHermesReadAdapter(insights_svc)
                card_text = adapter.format_weekly_recap_telegram_card()
                if self.outbound:
                    self.outbound.send_message(sender_id, card_text)
                return True, "WEEKLY_RECAP_CARD_SENT"

            # Check for /domain command (Operating Model V2 Feature 3)
            if lower_text in ("/domain", "domain", "tambah transaksi", "catat manual"):
                if not self.is_owner(sender_id):
                    logger.warning(f"BLOCKED: Non-owner domain attempt from {sender_id}")
                    if self.outbound:
                        self.outbound.send_message(
                            sender_id,
                            "⛔ <b>Akses Ditolak</b>: Anda tidak memiliki izin untuk mencatat transaksi."
                        )
                    return True, "BLOCKED_NON_OWNER_WRITE"

                menu = self.confirmation_handler.format_domain_menu()
                if self.outbound:
                    self.outbound.send_message(sender_id, menu["text"], reply_markup=menu["reply_markup"])
                return True, "DOMAIN_MENU_SENT"

            # Check for /review and /pending commands (Operating Model V2 Feature 2)
            if lower_text in ("/review", "/pending", "review pending", "antrean review"):
                if not self.is_owner(sender_id):
                    logger.warning(f"BLOCKED: Non-owner review attempt from {sender_id}")
                    if self.outbound:
                        self.outbound.send_message(
                            sender_id,
                            "⛔ <b>Akses Ditolak</b>: Anda tidak memiliki izin untuk mereview transaksi."
                        )
                    return True, "BLOCKED_NON_OWNER_READ"

                pending_items = self.engine.list_review_queue(status="PENDING")
                review_card = self.confirmation_handler.format_pending_reviews_card(pending_items)
                if self.outbound:
                    self.outbound.send_message(sender_id, review_card["text"], reply_markup=review_card["reply_markup"])
                return True, "PENDING_REVIEW_CARD_SENT"

            # Check if this is a finance transaction input
            if self.is_finance_message(text):
                # Enforce Owner Authorization Filter
                if not self.is_owner(sender_id):
                    logger.warning(f"BLOCKED: Non-owner transaction attempt from {sender_id}")
                    if self.outbound:
                        self.outbound.send_message(
                            sender_id,
                            "⛔ <b>Akses Ditolak</b>: Anda tidak memiliki izin untuk mencatat transaksi keuangan."
                        )
                    return True, "BLOCKED_NON_OWNER_WRITE"

                # Parse and stage candidate
                try:
                    candidate = self.confirmation_handler.stage_input(text)
                    card = self.confirmation_handler.format_confirmation_card(candidate)

                    if self.outbound:
                        self.outbound.send_message(
                            sender_id,
                            card["text"],
                            reply_markup=card["reply_markup"]
                        )
                    return True, f"STAGED_CARD_SENT:{candidate.candidate_id}"
                except Exception as e:
                    logger.error(f"Error staging finance transaction: {e}")
                    if self.outbound:
                        self.outbound.send_message(
                            sender_id,
                            f"⚠️ <b>Format Transaksi Kurang Tepat</b>: {e}\n<i>Contoh valid: 'makan siang 35k bca' atau 'trf 500k bca ke mandiri'</i>"
                        )
                    return True, f"STAGE_ERROR:{e}"

        # Passthrough to Hermes conversational queue
        return False, "PASSTHROUGH_TO_HERMES"


def get_ingress_router(
    engine: Optional[FinanceCoreEngine] = None,
    token: Optional[str] = None,
    owner_chat_id: Optional[str] = None,
    outbound_transport: Optional[Callable[[str, Dict[str, Any]], Dict[str, Any]]] = None,
    db_path: Optional[str] = None,
    auto_register_commands: bool = True
) -> FinanceTelegramIngressRouter:
    """
    Factory helper to instantiate a configured FinanceTelegramIngressRouter.
    Automatically registers canonical bot commands on initialization if auto_register_commands is True.
    """
    if engine is None:
        from .db import DatabaseManager
        if not db_path:
            db_path = os.environ.get("AIRO_FINANCE_DB_PATH")
        if not db_path:
            vps_db = os.path.expanduser("~/AI_WORKSPACES/airo-second-brain/ecosystem/projects/airo-finance-lab/data/airo_finance.db")
            if os.path.exists(vps_db):
                db_path = vps_db
            else:
                db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/airo_finance.db"))
        
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        db = DatabaseManager(db_path)
        db.init_schema()
        engine = FinanceCoreEngine(db)

    loaded_token, loaded_owner_id = load_telegram_credentials()
    actual_token = token or loaded_token
    actual_owner_id = owner_chat_id or loaded_owner_id

    outbound = TelegramOutboundAdapter(actual_token, transport=outbound_transport)
    return FinanceTelegramIngressRouter(
        engine,
        outbound=outbound,
        owner_chat_id=actual_owner_id,
        auto_register_commands=auto_register_commands
    )

