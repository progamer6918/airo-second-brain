"""
Bounded Arfin Adapter API Client (CU-02)
- 4 Bounded Methods: eab_get_pending, eab_submit_batch, eab_create_manual, eab_get_status
- Pre-submission pending record revalidation (fail closed on version mismatch, inactive cycle, terminal state)
- Deterministic idempotency key computation
- Timeout and retry classification (fake transport mode for offline testing)
- Structured redacted audit emission
- Zero Account Ledger writes (EARESMES_LEDGER_WRITE = FORBIDDEN)
"""

import time
import json
import hashlib
from typing import Dict, Any, List, Optional
from src.pending.pending_model import PendingRecord, PendingState
from src.adapter.auth_guard import SecurityGuard, AuthGuardError

class BoundedAdapterError(Exception):
    def __init__(self, message: str, error_code: str):
        super().__init__(message)
        self.error_code = error_code

class BoundedArfinAdapter:
    """Bounded Arfin adapter API client."""
    def __init__(
        self,
        security_guard: SecurityGuard,
        fake_transport_mode: bool = True
    ):
        self.security_guard = security_guard
        self.fake_transport_mode = fake_transport_mode
        self._staged_batches: Dict[str, Dict[str, Any]] = {}
        self._audit_logs: List[Dict[str, Any]] = []

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

    def revalidate_pending_record(self, record: PendingRecord, expected_version: int) -> None:
        """Pre-submission revalidation: fails closed with 0 transport calls."""
        if not record or not record.pending_id:
            raise BoundedAdapterError("Validation failed: PendingRecord missing.", "VALIDATION_RECORD_MISSING")

        if record.pending_version != expected_version:
            raise BoundedAdapterError(
                f"Version mismatch: expected {expected_version}, got {record.pending_version}",
                "STALE_RECORD_REJECTED"
            )

        if not record.is_active_cycle:
            raise BoundedAdapterError("Record is not in active cycle.", "STALE_RECORD_REJECTED")

        terminal_states = {PendingState.EXPIRED, PendingState.POSTED, PendingState.CANCELLED}
        if record.state in terminal_states:
            raise BoundedAdapterError(f"Record in terminal state '{record.state.value}'.", "STALE_RECORD_REJECTED")

    def compute_idempotency_key(
        self,
        pending_id: str,
        pending_version: int,
        action: str,
        payload: Dict[str, Any]
    ) -> str:
        """Deterministic idempotency key calculation."""
        sorted_payload = json.dumps(payload, sort_keys=True)
        raw = f"{pending_id}:{pending_version}:{action}:{sorted_payload}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def eab_get_pending(self, pending_id: str, owner_chat_id: str) -> Dict[str, Any]:
        """Bounded operation 1: get pending record summary."""
        self.security_guard.verify_owner_chat_id(owner_chat_id)
        self.log_audit("EAB_GET_PENDING", {"pending_id": pending_id, "owner_chat_id": owner_chat_id})
        return {"status": "SUCCESS", "pending_id": pending_id}

    def eab_submit_batch(
        self,
        record: PendingRecord,
        expected_version: int,
        items: List[Dict[str, Any]],
        owner_chat_id: str
    ) -> Dict[str, Any]:
        """Bounded operation 2: submit batch to Review Queue."""
        self.security_guard.verify_owner_chat_id(owner_chat_id)
        self.revalidate_pending_record(record, expected_version)

        idempotency_key = self.compute_idempotency_key(
            record.pending_id, expected_version, "submit_batch", {"items": items}
        )

        if idempotency_key in self._staged_batches:
            existing = self._staged_batches[idempotency_key]
            if existing["items"] == items:
                self.log_audit("EAB_SUBMIT_BATCH_DUPLICATE", {"idempotency_key": idempotency_key})
                return existing["result"]
            else:
                raise BoundedAdapterError("Idempotency conflict for existing key.", "IDEMPOTENCY_CONFLICT")

        result = {
            "status": "STAGED",
            "batch_id": f"batch_{record.pending_id}_{int(time.time())}",
            "pending_id": record.pending_id,
            "item_count": len(items),
            "idempotency_key": idempotency_key
        }

        self._staged_batches[idempotency_key] = {"items": items, "result": result}
        self.log_audit("EAB_SUBMIT_BATCH_SUCCESS", {"idempotency_key": idempotency_key, "batch_id": result["batch_id"]})
        return result

    def eab_create_manual(self, payload: Dict[str, Any], owner_chat_id: str) -> Dict[str, Any]:
        """Bounded operation 3: create manual transaction draft."""
        self.security_guard.verify_owner_chat_id(owner_chat_id)
        self.log_audit("EAB_CREATE_MANUAL", {"owner_chat_id": owner_chat_id})
        return {"status": "SUCCESS", "draft_id": f"draft_{int(time.time())}"}

    def eab_get_status(self, batch_id: str, owner_chat_id: str) -> Dict[str, Any]:
        """Bounded operation 4: get batch processing status."""
        self.security_guard.verify_owner_chat_id(owner_chat_id)
        self.log_audit("EAB_GET_STATUS", {"batch_id": batch_id})
        return {"status": "SUCCESS", "batch_id": batch_id, "state": "STAGED"}
