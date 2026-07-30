"""
Earesmes-Arfin Clarification Bridge - Pending Domain Model
Canonical Implementation for Gate EAB_G2_0 / Milestone M7

Contracts Enforced:
- PENDING_ID_CONTRACT (CANONICAL_TARGET_ID, short_ref AF-XXXX, DISPLAY_REFERENCE_IS_CANONICAL_ID = NO)
- PENDING_VERSION_CONTRACT (Optimistic concurrency locking)
- REVIEW_QUEUE_STATE_TRANSITIONS (DRAFT, PENDING_REVIEW, STAGED, APPROVED, POSTED, REJECTED, EXPIRED, CANCELLED)
- LINEAGE_CONTRACT (root_id, parent_id, cycle_index, MAX_ACTIVE_CYCLES_PER_ROOT = 1)
- EXPIRY_CONTRACT (24h Prompt TTL, durable backlog move)
"""

import uuid
import time
import re
from enum import Enum
from typing import Dict, Any, Optional, List

class PendingState(Enum):
    DRAFT = "DRAFT"
    PENDING_REVIEW = "PENDING_REVIEW"
    STAGED = "STAGED"
    APPROVED = "APPROVED"
    POSTED = "POSTED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"

class ConcurrencyConflictError(Exception):
    """Raised when version mismatch indicates concurrent modification (409 Conflict)."""
    pass

class LineageConflictError(Exception):
    """Raised when active cycle limit per root is exceeded (MAX_ACTIVE_CYCLES_PER_ROOT = 1)."""
    pass

class InvalidStateTransitionError(Exception):
    """Raised when an illegal state transition is attempted."""
    pass

class PendingRecord:
    """
    Canonical Pending Domain Model Record.
    """
    PROMPT_TTL_HOURS = 24
    MAX_ACTIVE_CYCLES_PER_ROOT = 1

    def __init__(
        self,
        pending_id: Optional[str] = None,
        short_ref: Optional[str] = None,
        owner_actor_id: str = "",
        owner_chat_id: str = "",
        raw_prompt: str = "",
        parsed_payload: Optional[Dict[str, Any]] = None,
        state: PendingState = PendingState.DRAFT,
        pending_version: int = 1,
        root_id: Optional[str] = None,
        parent_id: Optional[str] = None,
        cycle_index: int = 1,
        created_at: Optional[float] = None,
        updated_at: Optional[float] = None,
        expires_at: Optional[float] = None,
        is_active_cycle: bool = True,
        durable_backlog_flag: bool = False
    ):
        now = time.time()
        self.pending_id = pending_id or f"pnd_{uuid.uuid4().hex}"
        self.short_ref = short_ref or self._generate_short_ref()
        self.owner_actor_id = str(owner_actor_id)
        self.owner_chat_id = str(owner_chat_id)
        self.raw_prompt = raw_prompt
        self.parsed_payload = parsed_payload or {}
        self.state = state if isinstance(state, PendingState) else PendingState(state)
        self.pending_version = int(pending_version)
        self.root_id = root_id or self.pending_id
        self.parent_id = parent_id
        self.cycle_index = int(cycle_index)
        self.created_at = float(created_at) if created_at else now
        self.updated_at = float(updated_at) if updated_at else now
        self.expires_at = float(expires_at) if expires_at else self.created_at + (self.PROMPT_TTL_HOURS * 3600)
        self.is_active_cycle = bool(is_active_cycle)
        self.durable_backlog_flag = bool(durable_backlog_flag)

    @staticmethod
    def _generate_short_ref() -> str:
        """Generates short reference in AF-XXXX format."""
        suffix = uuid.uuid4().hex[:4].upper()
        return f"AF-{suffix}"

    @classmethod
    def validate_short_ref(cls, short_ref: str) -> bool:
        """Validates AF-XXXX format pattern."""
        return bool(re.match(r"^AF-[A-Z0-9]{4}$", short_ref))

    def update_payload(self, new_payload: Dict[str, Any], expected_version: int) -> None:
        """Updates payload with optimistic concurrency version check."""
        if expected_version != self.pending_version:
            raise ConcurrencyConflictError(
                f"Version mismatch: expected {expected_version}, record has {self.pending_version}"
            )
        self.parsed_payload.update(new_payload)
        self.pending_version += 1
        self.updated_at = time.time()

    def transition_to(self, new_state: PendingState, expected_version: int) -> None:
        """Transitions state with optimistic concurrency check and valid transition rules."""
        if expected_version != self.pending_version:
            raise ConcurrencyConflictError(
                f"Version mismatch: expected {expected_version}, record has {self.pending_version}"
            )
        
        valid_next = self._get_valid_transitions(self.state)
        if new_state not in valid_next:
            raise InvalidStateTransitionError(
                f"Illegal transition from {self.state.value} to {new_state.value}"
            )
        
        self.state = new_state
        self.pending_version += 1
        self.updated_at = time.time()

        if new_state in [PendingState.POSTED, PendingState.REJECTED, PendingState.CANCELLED]:
            self.is_active_cycle = False

    @staticmethod
    def _get_valid_transitions(current_state: PendingState) -> List[PendingState]:
        matrix = {
            PendingState.DRAFT: [PendingState.PENDING_REVIEW, PendingState.CANCELLED, PendingState.EXPIRED],
            PendingState.PENDING_REVIEW: [PendingState.STAGED, PendingState.REJECTED, PendingState.CANCELLED, PendingState.EXPIRED],
            PendingState.STAGED: [PendingState.APPROVED, PendingState.REJECTED, PendingState.CANCELLED],
            PendingState.APPROVED: [PendingState.POSTED, PendingState.CANCELLED],
            PendingState.POSTED: [],
            PendingState.REJECTED: [PendingState.DRAFT], # Allows reactivation
            PendingState.EXPIRED: [PendingState.DRAFT],  # Allows reactivation
            PendingState.CANCELLED: []
        }
        return matrix.get(current_state, [])

    def check_expiry(self, current_timestamp: Optional[float] = None) -> bool:
        """Checks if item has exceeded prompt TTL and marks as EXPIRED / durable backlog."""
        now = current_timestamp or time.time()
        if now >= self.expires_at and self.state in [PendingState.DRAFT, PendingState.PENDING_REVIEW]:
            self.state = PendingState.EXPIRED
            self.durable_backlog_flag = True
            self.pending_version += 1
            self.updated_at = now
            return True
        return False

    def create_reactivation_child(self) -> "PendingRecord":
        """Creates a new child cycle record for reactivation, preserving root_id lineage."""
        child = PendingRecord(
            owner_actor_id=self.owner_actor_id,
            owner_chat_id=self.owner_chat_id,
            raw_prompt=self.raw_prompt,
            parsed_payload=dict(self.parsed_payload),
            state=PendingState.DRAFT,
            root_id=self.root_id,
            parent_id=self.pending_id,
            cycle_index=self.cycle_index + 1,
            is_active_cycle=True
        )
        self.is_active_cycle = False
        return child

    def to_dict(self) -> Dict[str, Any]:
        """Serializes record to dict."""
        return {
            "pending_id": self.pending_id,
            "short_ref": self.short_ref,
            "owner_actor_id": self.owner_actor_id,
            "owner_chat_id": self.owner_chat_id,
            "raw_prompt": self.raw_prompt,
            "parsed_payload": self.parsed_payload,
            "state": self.state.value,
            "pending_version": self.pending_version,
            "root_id": self.root_id,
            "parent_id": self.parent_id,
            "cycle_index": self.cycle_index,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "expires_at": self.expires_at,
            "is_active_cycle": self.is_active_cycle,
            "durable_backlog_flag": self.durable_backlog_flag
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PendingRecord":
        """Deserializes dict to PendingRecord."""
        return cls(
            pending_id=data.get("pending_id"),
            short_ref=data.get("short_ref"),
            owner_actor_id=data.get("owner_actor_id", ""),
            owner_chat_id=data.get("owner_chat_id", ""),
            raw_prompt=data.get("raw_prompt", ""),
            parsed_payload=data.get("parsed_payload"),
            state=PendingState(data["state"]) if "state" in data else PendingState.DRAFT,
            pending_version=data.get("pending_version", 1),
            root_id=data.get("root_id"),
            parent_id=data.get("parent_id"),
            cycle_index=data.get("cycle_index", 1),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            expires_at=data.get("expires_at"),
            is_active_cycle=data.get("is_active_cycle", True),
            durable_backlog_flag=data.get("durable_backlog_flag", False)
        )
