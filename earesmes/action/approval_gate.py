"""
EARESMES Action Approval Gate — P2.2
===================================
Enforces strict state transitions and replay protection for all actions:
  REQUESTED -> PROPOSED -> APPROVED -> EXECUTED -> VERIFIED
                |
                v
        REJECTED / EXPIRED

Forbidden Transitions:
  REQUESTED -> EXECUTED (Strictly Blocked)
  Any reuse of already EXECUTED actions (Replay Protection)
"""

import time
import uuid
from enum import Enum
from pathlib import Path
from typing import Dict, Any, Optional, Tuple


class ActionState(str, Enum):
    REQUESTED = "REQUESTED"
    PROPOSED = "PROPOSED"
    APPROVED = "APPROVED"
    EXECUTED = "EXECUTED"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


class ActionApprovalGate:
    """Manages action lifecycle, approval validation, and replay protection."""

    def __init__(self, state_dir: Optional[Path] = None):
        self.state_dir = state_dir
        self._actions: Dict[str, Dict[str, Any]] = {}

    def register_request(self, action_type: str, request_text: str, owner_id: str) -> str:
        """Create new action in REQUESTED state."""
        action_id = f"ACT-{int(time.time())}-{uuid.uuid4().hex[:6].upper()}"
        self._actions[action_id] = {
            "action_id": action_id,
            "owner_id": owner_id,
            "action_type": action_type,
            "request": request_text,
            "state": ActionState.REQUESTED,
            "created_at": time.time(),
            "history": [(ActionState.REQUESTED, time.time())]
        }
        return action_id

    def propose_action(self, action_id: str, proposal_details: Dict[str, Any]) -> bool:
        """Transition action from REQUESTED to PROPOSED."""
        act = self._actions.get(action_id)
        if not act or act["state"] != ActionState.REQUESTED:
            return False

        act["state"] = ActionState.PROPOSED
        act["proposal"] = proposal_details
        act["history"].append((ActionState.PROPOSED, time.time()))
        return True

    def approve_action(self, action_id: str, owner_id: str) -> Tuple[bool, str]:
        """Validate owner approval and transition to APPROVED."""
        act = self._actions.get(action_id)
        if not act:
            return False, f"Action ID '{action_id}' tidak ditemukan."

        if act["state"] == ActionState.EXECUTED:
            return False, f"Replay rejected: Action '{action_id}' sudah pernah dieksekusi."

        if act["state"] != ActionState.PROPOSED:
            return False, f"Invalid transition: Action '{action_id}' dalam state '{act['state']}', bukan PROPOSED."

        if act["owner_id"] != owner_id:
            return False, "Otorisasi ditolak: Owner ID tidak cocok."

        act["state"] = ActionState.APPROVED
        act["approved_by"] = owner_id
        act["approved_at"] = time.time()
        act["history"].append((ActionState.APPROVED, time.time()))
        return True, "Approval valid."

    def execute_action(self, action_id: str) -> Tuple[bool, str]:
        """Execute approved action and transition to EXECUTED."""
        act = self._actions.get(action_id)
        if not act:
            return False, f"Action ID '{action_id}' tidak ditemukan."

        # Guard against direct execution without proposal/approval
        if act["state"] == ActionState.REQUESTED:
            return False, "FORBIDDEN TRANSITION: REQUESTED -> EXECUTED diblokir oleh tata kelola."

        if act["state"] != ActionState.APPROVED:
            return False, f"Action '{action_id}' belum di-approve (state={act['state']})."

        act["state"] = ActionState.EXECUTED
        act["executed_at"] = time.time()
        act["history"].append((ActionState.EXECUTED, time.time()))
        return True, "Eksekusi berhasil."

    def verify_action(self, action_id: str, result_data: Any) -> bool:
        """Transition action to VERIFIED after receipt creation."""
        act = self._actions.get(action_id)
        if not act or act["state"] != ActionState.EXECUTED:
            return False

        act["state"] = ActionState.VERIFIED
        act["result"] = result_data
        act["verified_at"] = time.time()
        act["history"].append((ActionState.VERIFIED, time.time()))
        return True

    def get_action(self, action_id: str) -> Optional[Dict[str, Any]]:
        return self._actions.get(action_id)
