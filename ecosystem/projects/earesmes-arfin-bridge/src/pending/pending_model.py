# -*- coding: utf-8 -*-
"""
ecosystem/projects/earesmes-arfin-bridge/src/pending/pending_model.py
Canonical EAB Pending Transaction Data Model.
Supports opaque pending_id, stable AF-XXXX short ref, versioning, multi-pending, and lifecycle.
"""

import time
import uuid
import secrets
from typing import Dict, Any, List, Optional

def secrets_rand_digits() -> str:
    return f"{secrets.randbelow(10000):04d}"

class EABPendingItem:
    def __init__(self, owner_chat_id: str, amount: float, description: str, pending_id: Optional[str] = None, short_ref: Optional[str] = None, pending_version: int = 1):
        self.pending_id = pending_id or f"pend_{uuid.uuid4().hex[:12]}"
        self.short_ref = short_ref or f"AF-{secrets_rand_digits()}"
        self.owner_chat_id = owner_chat_id
        self.amount = amount
        self.description = description
        self.pending_version = pending_version
        self.status = "pending"  # pending, resolved, expired, ignored
        self.created_at = int(time.time())
        self.updated_at = int(time.time())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pending_id": self.pending_id,
            "short_ref": self.short_ref,
            "owner_chat_id": self.owner_chat_id,
            "amount": self.amount,
            "description": self.description,
            "pending_version": self.pending_version,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
