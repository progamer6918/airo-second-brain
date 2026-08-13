# -*- coding: utf-8 -*-
"""
ecosystem/projects/earesmes-arfin-bridge/src/adapter/eab_live_client.py
Production Signed EAB Client for Cloudflare Worker Transport.
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

WORKER_HOST = "airo-finance-telegram-proxy.egitaristorandas.workers.dev"
KEY_ID = "EAB_KEY_2026_V1"

class EABLiveSignedClient:
    def __init__(self, service_secret: Optional[str] = None, fake_mode: bool = False):
        self.service_secret = service_secret or os.environ.get("EAB_SERVICE_SECRET", "eab_secret_canary_key_v1")
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
