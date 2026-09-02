"""
Controlled worker queue lifecycle.

Phase 2:
- deterministic state transition only
- no execution
- no model calls
"""

VALID_TRANSITIONS = {
    "approved": ["queued"],
    "queued": ["claimed"],
    "claimed": ["running"],
    "running": ["completed", "failed"],
    "completed": [],
    "failed": [],
}


class WorkerStateMachine:

    def can_transition(self, current, target):
        return target in VALID_TRANSITIONS.get(current, [])

    def transition(self, current, target):
        if not self.can_transition(current, target):
            raise ValueError(
                f"Invalid transition: {current} -> {target}"
            )

        return target
