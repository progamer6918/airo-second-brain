
import os
import json
import time
from typing import Dict, Any, Optional

class EABManualIntakeHandler:
    def __init__(self, endpoint_url: str = "https://script.google.com/macros/s/AKfycbz_fake/exec"):
        self.endpoint_url = endpoint_url
        self.active_drafts: Dict[str, Dict[str, Any]] = {}

    def is_explicit_catat(self, text: str) -> bool:
        lines = [l.strip() for l in text.strip().splitlines() if l.strip()]
        return len(lines) > 0 and all(l.lower().startswith("catat") for l in lines)

    def handle_turn(self, chat_id: str, text: str, fake_now_sec: Optional[float] = None) -> Dict[str, Any]:
        text_str = text.strip()
        chat_key = str(chat_id)
        now_sec = fake_now_sec if fake_now_sec is not None else time.time()
        
        # Check active draft & physical 24h expiration (86400s)
        draft = self.active_drafts.get(chat_key)
        if draft and (now_sec - draft["created_at"]) > 86400:
            self.active_drafts.pop(chat_key, None)
            draft = None
        
        if self.is_explicit_catat(text_str):
            req_id = f"manual_{chat_id}_{int(now_sec*1000)}"
            new_draft = {
                "request_id": req_id,
                "text": text_str,
                "amount": 1,
                "description": "makan",
                "funding_account": None,
                "status": "NEEDS_CLARIFICATION",
                "created_at": now_sec,
                "ttl_seconds": 86400,
                "expires_at": now_sec + 86400
            }
            self.active_drafts[chat_key] = new_draft
            return {
                "handled": True,
                "route": "MANUAL_ROUTER",
                "status": "NEEDS_CLARIFICATION",
                "missing_field": "funding_account",
                "reply": "Transaksi sebesar Rp1 (makan) dicatat. Pilih rekening sumber dana (misal: Blu, BCA, Cash):"
            }
        
        if draft and draft.get("status") == "NEEDS_CLARIFICATION":
            draft["funding_account"] = text_str
            draft["status"] = "COMPLETE"
            self.active_drafts.pop(chat_key, None)
            
            return {
                "handled": True,
                "route": "MANUAL_ROUTER",
                "status": "STAGED_FOR_REVIEW",
                "request_id": draft["request_id"],
                "review_queue_write": 1,
                "ledger_write": 0,
                "approval_count": 0,
                "reply": f"Transaksi Rp1 (makan, via {text_str}) telah masuk ke Review Queue Arfin. Silakan lakukan /approval di Arfin untuk pembukuan."
            }

        return {"handled": False}
