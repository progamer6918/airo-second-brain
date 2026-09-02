"""
Worker lifecycle receipt helper.

Phase 2:
captures state transition evidence only.
"""


def build_state_receipt(job_id, old_state, new_state):
    return {
        "job_id": job_id,
        "previous_state": old_state,
        "current_state": new_state,
        "type": "worker_state_transition",
    }
