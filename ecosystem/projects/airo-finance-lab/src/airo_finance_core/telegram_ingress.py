import os
import sys
import json
import logging
import urllib.request
import urllib.parse
import urllib.error
from typing import Optional, Dict, Any, Tuple, Callable
from .engine import FinanceCoreEngine
from .telegram_capture import InteractiveConfirmationHandler, SimpleTransactionParser

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
            logger.error(f"Telegram API HTTP error {e.code} on {method}: {raw_err}")
            return {"ok": False, "error_code": e.code, "description": raw_err}
        except Exception as e:
            logger.error(f"Telegram API request failed on {method}: {e}")
            return {"ok": False, "error": str(e)}

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
        owner_chat_id: Optional[str] = None
    ):
        self.engine = engine
        self.outbound = outbound
        self.owner_chat_id = str(owner_chat_id) if owner_chat_id else None
        self.confirmation_handler = InteractiveConfirmationHandler(engine)
        self.parser = self.confirmation_handler.parser

    def is_owner(self, sender_id: Any) -> bool:
        if not self.owner_chat_id:
            return True
        allowed = [x.strip() for x in str(self.owner_chat_id).split(",") if x.strip()]
        return str(sender_id).strip() in allowed

    def is_finance_message(self, text: str) -> bool:
        """
        Determines whether a message is an intended financial transaction input.
        Must contain valid numeric amount and parseable structure.
        Conversational queries (e.g. 'Halo', 'Sisa budget?') return False.
        """
        if not text or not text.strip():
            return False

        stripped = text.strip()
        lower = stripped.lower()

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
        # 1. Handle Callback Query (Confirmation / Cancellation)
        if "callback_query" in update:
            cq = update["callback_query"]
            cq_id = str(cq.get("id", ""))
            data = cq.get("data", "")
            sender_id = str(cq.get("from", {}).get("id", ""))
            msg = cq.get("message", {})
            chat_id = str(msg.get("chat", {}).get("id", sender_id))
            message_id = msg.get("message_id")

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

                elif field_code == "dat":
                    self.confirmation_handler.start_edit_session(chat_id, candidate_id, field="date")
                    prompt_text = (
                        "📅 <b>Koreksi Tanggal</b>\n"
                        "───────────────────\n"
                        "Kirim tanggal baru (format: <code>YYYY-MM-DD</code> atau <code>DD/MM/YYYY</code>):"
                    )
                    back_markup = {"inline_keyboard": [[{"text": "🔙 Kembali", "callback_data": f"ced:{candidate_id}"}]]}
                    if self.outbound and message_id:
                        self.outbound.edit_message_text(chat_id, message_id, prompt_text, reply_markup=back_markup)
                        self.outbound.answer_callback_query(cq_id, text="Kirim tanggal baru")
                    return True, "EDIT_FIELD_PROMPTED:date"

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

            # Account Selection Callback (eda:<candidate_id>:<account_id>)
            if data.startswith("eda:"):
                if not self.is_owner(sender_id):
                    logger.warning(f"BLOCKED: Non-owner callback from {sender_id}")
                    return True, "BLOCKED_NON_OWNER_CALLBACK"
                _, candidate_id, acc_id = data.split(":", 2)
                candidate = self.confirmation_handler.apply_field_update(candidate_id, "account", acc_id)
                if candidate:
                    preview = self.confirmation_handler.format_draft_preview(candidate)
                    if self.outbound and message_id:
                        self.outbound.edit_message_text(chat_id, message_id, preview["text"], reply_markup=preview["reply_markup"])
                        self.outbound.answer_callback_query(cq_id, text="Rekening diperbarui")
                    return True, f"DRAFT_ACCOUNT_UPDATED:{candidate_id}"

            # Destination Account Selection Callback (edd:<candidate_id>:<account_id>)
            if data.startswith("edd:"):
                if not self.is_owner(sender_id):
                    logger.warning(f"BLOCKED: Non-owner callback from {sender_id}")
                    return True, "BLOCKED_NON_OWNER_CALLBACK"
                _, candidate_id, acc_id = data.split(":", 2)
                candidate = self.confirmation_handler.apply_field_update(candidate_id, "dst_account", acc_id)
                if candidate:
                    preview = self.confirmation_handler.format_draft_preview(candidate)
                    if self.outbound and message_id:
                        self.outbound.edit_message_text(chat_id, message_id, preview["text"], reply_markup=preview["reply_markup"])
                        self.outbound.answer_callback_query(cq_id, text="Rekening tujuan diperbarui")
                    return True, f"DRAFT_DST_ACCOUNT_UPDATED:{candidate_id}"

            # Category Selection Callback (edc:<candidate_id>:<category_id>)
            if data.startswith("edc:"):
                if not self.is_owner(sender_id):
                    logger.warning(f"BLOCKED: Non-owner callback from {sender_id}")
                    return True, "BLOCKED_NON_OWNER_CALLBACK"
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

            # Subcategory Selection Callback (eds:<candidate_id>:<subcategory_id>)
            if data.startswith("eds:"):
                if not self.is_owner(sender_id):
                    logger.warning(f"BLOCKED: Non-owner callback from {sender_id}")
                    return True, "BLOCKED_NON_OWNER_CALLBACK"
                _, candidate_id, subc_id = data.split(":", 2)
                candidate = self.confirmation_handler.apply_field_update(candidate_id, "subcategory", subc_id)
                if candidate:
                    preview = self.confirmation_handler.format_draft_preview(candidate)
                    if self.outbound and message_id:
                        self.outbound.edit_message_text(chat_id, message_id, preview["text"], reply_markup=preview["reply_markup"])
                        self.outbound.answer_callback_query(cq_id, text="Subkategori diperbarui")
                    return True, f"DRAFT_SUBCATEGORY_UPDATED:{candidate_id}"

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
                    ok, tx, status_msg = self.confirmation_handler.confirm_candidate(candidate_id)
                    if ok and tx:
                        card_receipt = (
                            f"✅ <b>Transaksi Berhasil Dicatat!</b>\n"
                            f"───────────────────\n"
                            f"💰 <b>Nominal:</b> Rp{int(round(tx.amount)):,}\n"
                            f"📁 <b>Tipe:</b> {tx.direction}\n"
                            f"📝 <b>Catatan:</b> {tx.note or '-'}\n"
                            f"🆔 <b>Ref:</b> <code>{tx.id}</code>\n"
                            f"───────────────────\n"
                            f"<i>Tersimpan di Buku Besar SQLite & Terverifikasi Audit.</i>"
                        ).replace(",", ".")
                        if self.outbound and message_id:
                            self.outbound.edit_message_text(chat_id, message_id, card_receipt, reply_markup={"inline_keyboard": []})
                            self.outbound.answer_callback_query(cq_id, text="✅ Transaksi Tersimpan")
                        return True, f"CONFIRMED:{tx.id}"
                    else:
                        if self.outbound and message_id:
                            self.outbound.answer_callback_query(cq_id, text=f"⚠️ {status_msg}", show_alert=True)
                        return True, f"CONFIRM_FAILED:{status_msg}"

                elif action == "ccl":
                    self.confirmation_handler.clear_edit_session(chat_id)
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
                        item, tx = self.engine.approve_review_item(review_id)
                        if tx.direction == "TRANSFER":
                            card_receipt = (
                                f"✅ <b>Transfer Berhasil Disetujui!</b>\n"
                                f"───────────────────\n"
                                f"💰 <b>Nominal:</b> Rp{int(round(tx.amount)):,}\n"
                                f"🔄 <b>Tipe:</b> Transfer Antar Rekening / Pocket\n"
                                f"📝 <b>Catatan:</b> {tx.note or '-'}\n"
                                f"🆔 <b>Ref:</b> <code>{tx.id}</code>\n"
                                f"───────────────────\n"
                                f"<i>Tercatat di Buku Besar. Net Worth tidak berubah.</i>"
                            ).replace(",", ".")
                        else:
                            card_receipt = (
                                f"✅ <b>Transaksi Gmail Berhasil Disetujui!</b>\n"
                                f"───────────────────\n"
                                f"💰 <b>Nominal:</b> Rp{int(round(tx.amount)):,}\n"
                                f"📝 <b>Catatan:</b> {tx.note or '-'}\n"
                                f"🆔 <b>Ref:</b> <code>{tx.id}</code>\n"
                                f"───────────────────\n"
                                f"<i>Tercatat di Buku Besar.</i>"
                            ).replace(",", ".")
                        if self.outbound and message_id:
                            self.outbound.edit_message_text(chat_id, message_id, card_receipt, reply_markup={"inline_keyboard": []})
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
                    if self.outbound:
                        self.outbound.answer_callback_query(
                            cq_id,
                            text="✏️ Edit Transaksi: Buka Dashboard AIRO Finance atau kirim format koreksi.",
                            show_alert=True
                        )
                    return True, f"GMAIL_CHANGE_PROMPTED:{review_id}"

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
    db_path: Optional[str] = None
) -> FinanceTelegramIngressRouter:
    """
    Factory helper to instantiate a configured FinanceTelegramIngressRouter.
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
    return FinanceTelegramIngressRouter(engine, outbound=outbound, owner_chat_id=actual_owner_id)

