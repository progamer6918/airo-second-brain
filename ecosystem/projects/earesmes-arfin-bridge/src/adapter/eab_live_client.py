# -*- coding: utf-8 -*-
"""
ecosystem/projects/earesmes-arfin-bridge/src/adapter/eab_live_client.py
Production Signed EAB Client for Cloudflare Worker Transport.
Fail-closed configuration, 4 bounded operations, canonical envelope parsing, User-Agent header.
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

WORKER_HOST = "airo-finance-telegram-proxy.progamer6918.workers.dev"
KEY_ID = "EAB_KEY_2026_V1"

class EABLiveSignedClient:
    def __init__(self, service_secret: Optional[str] = None, fake_mode: bool = False):
        sec = service_secret or os.environ.get("EAB_SERVICE_SECRET")
        if not sec and not fake_mode:
            raise ValueError("EAB_SERVICE_SECRET missing in environment! Fail closed.")
        self.service_secret = sec or ""
        self.fake_mode = fake_mode

    def _send_signed_request(self, operation_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if self.fake_mode:
            return {"status": "ok", "fake": True, "operation_id": operation_id, "payload": payload}

        now_ts = str(int(time.time()))
        nonce_hex = secrets.token_bytes(8).hex()
        req_id = payload.get("request_id") or f"req_{int(time.time())}"

        body_str = json.dumps(payload, separators=(',', ':'))
        body_sha256 = hashlib.sha256(body_str.encode('utf-8')).hexdigest()

        canonical_sig_str = f"v=1.0&op={operation_id}&req_id={req_id}&ts={now_ts}&nonce={nonce_hex}&body_sha256={body_sha256}"
        signature = hmac.new(
            self.service_secret.encode('utf-8'),
            canonical_sig_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        headers = {
            "User-Agent": "AIRO-EAB-Client/1.0",
            "Content-Type": "application/json",
            "X-EAB-Key-ID": KEY_ID,
            "X-EAB-Timestamp": now_ts,
            "X-EAB-Nonce": nonce_hex,
            "X-EAB-Signature": signature
        }

        url = f"https://{WORKER_HOST}/eab"
        req = urllib.request.Request(url, data=body_str.encode('utf-8'), headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                if not isinstance(data, dict):
                    return {"status": "error", "message": "Invalid non-dict response envelope"}
                return data
        except urllib.error.HTTPError as e:
            return {"status": "error", "http_code": e.code, "message": f"HTTP Error {e.code}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_pending(self, pending_id: str, owner_chat_id: str) -> Dict[str, Any]:
        payload = {
            "schema_version": "1.0",
            "request_id": f"req_get_{int(time.time())}",
            "operation_id": "EAB_GET_PENDING",
            "owner_chat_id": owner_chat_id,
            "pending_id": pending_id
        }
        return self._send_signed_request("EAB_GET_PENDING", payload)

    def list_pending(self, owner_chat_id: str) -> Dict[str, Any]:
        payload = {
            "schema_version": "1.0",
            "request_id": f"req_list_{int(time.time())}",
            "operation_id": "EAB_LIST_PENDING",
            "owner_chat_id": owner_chat_id
        }
        return self._send_signed_request("EAB_LIST_PENDING", payload)

    def submit_batch_clarification(self, items: List[Dict[str, Any]], owner_chat_id: str) -> Dict[str, Any]:
        payload = {
            "schema_version": "1.0",
            "request_id": f"req_batch_{int(time.time())}",
            "operation_id": "EAB_SUBMIT_BATCH_CLARIFICATION",
            "owner_chat_id": owner_chat_id,
            "items": items
        }
        return self._send_signed_request("EAB_SUBMIT_BATCH_CLARIFICATION", payload)

    def create_manual_transaction(self, amount: float, category: str, description: str, owner_chat_id: str) -> Dict[str, Any]:
        payload = {
            "schema_version": "1.0",
            "request_id": f"req_manual_{int(time.time())}",
            "operation_id": "EAB_CREATE_MANUAL_TRANSACTION",
            "owner_chat_id": owner_chat_id,
            "amount": amount,
            "category": category,
            "description": description
        }
        return self._send_signed_request("EAB_CREATE_MANUAL_TRANSACTION", payload)
