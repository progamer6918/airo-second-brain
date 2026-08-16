# -*- coding: utf-8 -*-
"""
ecosystem/projects/earesmes-arfin-bridge/src/adapter/eab_live_client.py
Production Signed EAB Client supporting Direct Apps Script Transport (AIRO_EAB_DIRECT_V1).
"""

import os
import json
import time
import hmac
import secrets
import hashlib
import urllib.request
import urllib.parse
import urllib.error
from typing import Dict, Any, List, Optional

APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxzalMbtiHNHUFaWhZcaEBupMfxfXzqlTwrjhDmovUayZnSv-Z-kRmN6MPjq1ncv7nq0g/exec"
WORKER_HOST = "airo-finance-telegram-proxy.progamer6918.workers.dev"
KEY_ID = "EAB_KEY_2026_V1"

class EABLiveSignedClient:
    def __init__(self, service_secret: Optional[str] = None, fake_mode: bool = False, direct_mode: bool = True):
        self.service_secret = service_secret or os.environ.get("EAB_SERVICE_SECRET", "")
        self.fake_mode = fake_mode
        self.direct_mode = direct_mode

    def _send_signed_request(self, operation_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if self.fake_mode:
            return {"status": "ok", "fake": True, "operation_id": operation_id, "payload": payload}

        now_ts = str(int(time.time()))
        nonce_hex = secrets.token_bytes(8).hex()
        req_id = payload.get("request_id") or f"req_{int(time.time())}"
        owner_chat_id = str(payload.get("owner_chat_id", ""))

        body_str = json.dumps(payload, separators=(',', ':'))
        body_sha256 = hashlib.sha256(body_str.encode('utf-8')).hexdigest()

        canonical_sig_str = f"v=1.0&op={operation_id}&req_id={req_id}&owner_chat_id={owner_chat_id}&key_id={KEY_ID}&nonce={nonce_hex}&ts={now_ts}&body_sha256={body_sha256}"
        signature = hmac.new(
            self.service_secret.encode('utf-8'),
            canonical_sig_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        if self.direct_mode:
            direct_envelope = {
                "_eab_direct": {
                    "marker": "AIRO_EAB_DIRECT_V1",
                    "schema_version": "1.0",
                    "request_id": req_id,
                    "operation_id": operation_id,
                    "owner_chat_id": owner_chat_id,
                    "key_id": KEY_ID,
                    "issued_at": int(now_ts),
                    "nonce": nonce_hex,
                    "body_sha256": body_sha256,
                    "mac": signature
                },
                "payload": payload
            }
            post_body = json.dumps(direct_envelope, separators=(',', ':')).encode('utf-8')
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AIRO-EAB-Client/1.0"
            }
            url = APPS_SCRIPT_URL
        else:
            headers = {
                "Content-Type": "application/json",
                "X-EAB-Key-ID": KEY_ID,
                "X-EAB-Timestamp": now_ts,
                "X-EAB-Nonce": nonce_hex,
                "X-EAB-Signature": signature
            }
            url = f"https://{WORKER_HOST}/eab"
            post_body = body_str.encode('utf-8')

        req = urllib.request.Request(url, data=post_body, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                return data
        except urllib.error.HTTPError as e:
            return {"status": "error", "http_code": e.code, "message": f"HTTP Error {e.code}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def list_pending(self, owner_chat_id: str) -> Dict[str, Any]:
        payload = {
            "schema_version": "1.0",
            "request_id": f"req_list_{int(time.time())}",
            "operation_id": "EAB_LIST_PENDING",
            "owner_chat_id": owner_chat_id
        }
        return self._send_signed_request("EAB_LIST_PENDING", payload)

    def submit_clarification(self, pending_id: str, pending_version: int, clarification_text: str, owner_chat_id: str) -> Dict[str, Any]:
        payload = {
            "schema_version": "1.0",
            "request_id": f"req_submit_{int(time.time())}",
            "operation_id": "EAB_SUBMIT_CLARIFICATION",
            "owner_chat_id": owner_chat_id,
            "pending_id": pending_id,
            "expected_pending_version": pending_version,
            "clarification_text": clarification_text
        }
        return self._send_signed_request("EAB_SUBMIT_CLARIFICATION", payload)

    def create_manual(
        self,
        owner_chat_id: str,
        description: str,
        amount: Optional[float] = None,
        funding_account: Optional[str] = None,
        category: Optional[str] = None,
        subcategory: Optional[str] = None,
        direction: str = "EXPENSE",
        request_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        EAB_CREATE_MANUAL operation: Intake manual natural-language transactions.
        Incomplete requests return application_status="NEEDS_CLARIFICATION".
        Complete requests stage to Review Queue only (zero direct Account Ledger write).
        """
        req_id = request_id or f"req_create_{int(time.time())}"
        payload = {
            "schema_version": "1.0",
            "request_id": req_id,
            "operation_id": "EAB_CREATE_MANUAL",
            "owner_chat_id": owner_chat_id,
            "description": description,
            "amount": amount,
            "funding_account": funding_account,
            "category": category,
            "subcategory": subcategory,
            "direction": direction
        }
        return self._send_signed_request("EAB_CREATE_MANUAL", payload)

    @classmethod
    def get_tool_schema(cls) -> Dict[str, Any]:
        """Expose EAB manual create tool schema to Earesmes/Hermes tool registry."""
        return {
            "name": "eab_create_manual",
            "description": "Log manual finance transaction or request clarification via Earesmes EAB bridge.",
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {"type": "string", "description": "Transaction raw text or description"},
                    "amount": {"type": "number", "description": "Transaction amount in IDR"},
                    "funding_account": {"type": "string", "description": "Funding account name"},
                    "category": {"type": "string", "description": "Budget category"},
                    "subcategory": {"type": "string", "description": "Budget subcategory"},
                    "direction": {"type": "string", "enum": ["EXPENSE", "INCOME"], "default": "EXPENSE"}
                },
                "required": ["description"]
            }
        }
