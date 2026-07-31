"""
Earesmes Telegram Gateway & Hermes Orchestration Bridge (CU-03)
- Canonical identity, version, and owner_chat_id propagation
- Short-reference resolution without using short_ref as canonical identity
- Pre-submission pending record revalidation (fail closed on stale/terminal state)
- Idempotency key construction & propagation to BoundedArfinAdapter
- Fail-closed error handling and queue message retention
- Structured audit logging with secret redaction
- Zero Account Ledger writes (EARESMES_LEDGER_WRITE = FORBIDDEN)
- Direct Arfin fallback route preserved
"""

import time
import json
import hashlib
from typing import Dict, Any, List, Optional
from src.pending.pending_model import PendingRecord, PendingState
from src.adapter.auth_guard import SecurityGuard, AuthGuardError
from src.adapter.bounded_adapter import BoundedArfinAdapter, BoundedAdapterError

class GatewayBridgeError(Exception):
    def __init__(self, message: str, error_code: str):
        super().__init__(message)
        self.error_code = error_code

class GatewayBridge:
    """
    Bridge orchestrator between Telegram Gateway / Hermes input and BoundedArfinAdapter.
    """
    def __init__(
        self,
        security_guard: SecurityGuard,
        bounded_adapter: BoundedArfinAdapter,
        pending_records: Optional[Dict[str, PendingRecord]] = None
    ):
        self.security_guard = security_guard
        self.bounded_adapter = bounded_adapter
        self.pending_records: Dict[str, PendingRecord] = pending_records if pending_records is not None else {}
        self.short_ref_map: Dict[str, str] = {}
        self._audit_logs: List[Dict[str, Any]] = []

        for pid, rec in self.pending_records.items():
            if hasattr(rec, 'display_short_reference') and rec.display_short_reference:
                self.short_ref_map[rec.display_short_reference] = pid

    def register_pending_record(self, record: PendingRecord) -> None:
        """Register or update a pending record in bridge memory."""
        if not record or not record.pending_id:
            raise GatewayBridgeError("Cannot register record missing pending_id.", "VALIDATION_RECORD_MISSING")
        self.pending_records[record.pending_id] = record
        if hasattr(record, 'display_short_reference') and record.display_short_reference:
            self.short_ref_map[record.display_short_reference] = record.pending_id

    def resolve_short_reference(self, short_ref: str) -> Optional[PendingRecord]:
        """
        Resolve a short reference string (e.g. AF-1001) to canonical PendingRecord.
        Short reference is a display alias ONLY, never used as canonical pending_id.
        """
        pid = self.short_ref_map.get(short_ref)
        if not pid:
            return self.pending_records.get(short_ref)
        return self.pending_records.get(pid)

    def log_audit(self, event_type: str, details: Dict[str, Any]) -> None:
        redacted_details = {}
        for k, v in details.items():
            if isinstance(v, str):
                redacted_details[k] = self.security_guard.redact_secrets(v)
            else:
                redacted_details[k] = v
        self._audit_logs.append({
            "timestamp": time.time(),
            "event_type": event_type,
            "details": redacted_details
        })

    def process_telegram_update(
        self,
        update_dict: Dict[str, Any],
        current_time: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Process incoming Telegram update dictionary.
        Extracts chat_id, reply_to_message_id / short_ref, items, signature, timestamp, nonce.
        Propagates owner_chat_id, pending_id, and pending_version to adapter.
        """
        now = current_time if current_time is not None else time.time()
        
        message = update_dict.get("message", {})
        chat = message.get("chat", {})
        owner_chat_id = str(chat.get("id", ""))

        try:
            self.security_guard.verify_owner_chat_id(owner_chat_id)
        except AuthGuardError as e:
            self.log_audit("BRIDGE_AUTH_UNAUTHORIZED", {"owner_chat_id": owner_chat_id, "error": str(e)})
            return {
                "status": "REJECTED",
                "error_code": e.error_code,
                "message": str(e),
                "queue_message_effect": "REJECTED"
            }

        short_ref = update_dict.get("short_ref") or message.get("short_ref")
        items = update_dict.get("items", [])
        expected_version = update_dict.get("expected_version", 1)

        record = None
        if short_ref:
            record = self.resolve_short_reference(short_ref)

        if not record:
            self.log_audit("BRIDGE_RECORD_NOT_FOUND", {"short_ref": short_ref, "owner_chat_id": owner_chat_id})
            return {
                "status": "REJECTED",
                "error_code": "PENDING_NOT_FOUND",
                "message": f"Pending record not found for reference '{short_ref}'.",
                "queue_message_effect": "REJECTED"
            }

        try:
            self.bounded_adapter.revalidate_pending_record(record, expected_version)
        except BoundedAdapterError as e:
            self.log_audit("BRIDGE_STALE_RECORD_REJECTED", {"pending_id": record.pending_id, "error": str(e)})
            return {
                "status": "REJECTED",
                "error_code": e.error_code,
                "message": str(e),
                "queue_message_effect": "REJECTED"
            }

        signature = update_dict.get("signature")
        nonce = update_dict.get("nonce")
        ts = update_dict.get("timestamp", now)
        if signature and nonce:
            try:
                payload_str = json.dumps({"items": items}, sort_keys=True)
                self.security_guard.verify_service_auth(signature, payload_str, ts, nonce, current_time=now)
            except AuthGuardError as e:
                self.log_audit("BRIDGE_AUTH_FAIL", {"pending_id": record.pending_id, "error": str(e)})
                return {
                    "status": "REJECTED",
                    "error_code": e.error_code,
                    "message": str(e),
                    "queue_message_effect": "REJECTED"
                }

        try:
            adapter_res = self.bounded_adapter.eab_submit_batch(
                record=record,
                expected_version=expected_version,
                items=items,
                owner_chat_id=owner_chat_id
            )
            self.log_audit("BRIDGE_SUBMIT_SUCCESS", {"pending_id": record.pending_id, "batch_id": adapter_res.get("batch_id")})
            return {
                "status": "SUCCESS",
                "pending_id": record.pending_id,
                "batch_id": adapter_res.get("batch_id"),
                "result": adapter_res,
                "queue_message_effect": "REMOVED"
            }
        except BoundedAdapterError as e:
            retryable_codes = {"TIMEOUT_BEFORE_ACCEPTANCE", "ADAPTER_RETRYABLE_ERROR", "TIMEOUT_UNKNOWN_ACCEPTANCE"}
            is_retryable = e.error_code in retryable_codes
            queue_effect = "RETAINED" if is_retryable else "REJECTED"

            self.log_audit("BRIDGE_ADAPTER_ERROR", {"pending_id": record.pending_id, "error_code": e.error_code, "queue_effect": queue_effect})
            return {
                "status": "RETRYING" if is_retryable else "REJECTED",
                "error_code": e.error_code,
                "message": str(e),
                "queue_message_effect": queue_effect
            }

    def process_hermes_payload(
        self,
        payload_dict: Dict[str, Any],
        current_time: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Process incoming Hermes orchestration payload.
        Extracts correlation_id, owner_chat_id, pending_id, expected_version, items.
        """
        now = current_time if current_time is not None else time.time()
        correlation_id = payload_dict.get("correlation_id", "")
        owner_chat_id = str(payload_dict.get("owner_chat_id", ""))
        pending_id = payload_dict.get("pending_id", "")
        expected_version = payload_dict.get("expected_version", 1)
        items = payload_dict.get("items", [])

        try:
            self.security_guard.verify_owner_chat_id(owner_chat_id)
        except AuthGuardError as e:
            self.log_audit("HERMES_AUTH_UNAUTHORIZED", {"owner_chat_id": owner_chat_id, "correlation_id": correlation_id})
            return {
                "status": "REJECTED",
                "error_code": e.error_code,
                "message": str(e),
                "queue_message_effect": "REJECTED"
            }

        record = self.pending_records.get(pending_id)
        if not record:
            self.log_audit("HERMES_RECORD_NOT_FOUND", {"pending_id": pending_id, "correlation_id": correlation_id})
            return {
                "status": "REJECTED",
                "error_code": "PENDING_NOT_FOUND",
                "message": f"Pending record '{pending_id}' not found.",
                "queue_message_effect": "REJECTED"
            }

        try:
            adapter_res = self.bounded_adapter.eab_submit_batch(
                record=record,
                expected_version=expected_version,
                items=items,
                owner_chat_id=owner_chat_id
            )
            self.log_audit("HERMES_SUBMIT_SUCCESS", {"pending_id": pending_id, "correlation_id": correlation_id})
            return {
                "status": "SUCCESS",
                "correlation_id": correlation_id,
                "pending_id": pending_id,
                "batch_id": adapter_res.get("batch_id"),
                "result": adapter_res,
                "queue_message_effect": "REMOVED"
            }
        except BoundedAdapterError as e:
            retryable_codes = {"TIMEOUT_BEFORE_ACCEPTANCE", "ADAPTER_RETRYABLE_ERROR", "TIMEOUT_UNKNOWN_ACCEPTANCE"}
            is_retryable = e.error_code in retryable_codes
            queue_effect = "RETAINED" if is_retryable else "REJECTED"

            self.log_audit("HERMES_ADAPTER_ERROR", {"pending_id": pending_id, "correlation_id": correlation_id, "error_code": e.error_code})
            return {
                "status": "RETRYING" if is_retryable else "REJECTED",
                "error_code": e.error_code,
                "message": str(e),
                "queue_message_effect": queue_effect
            }
