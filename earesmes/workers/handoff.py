"""
Worker handoff boundary.

Phase 3:
creates controlled handoff evidence only.
"""


def build_handoff_record(package, state):
    return {
        "job_id": package.get("job_id"),
        "project_id": package.get("project_id"),
        "session_id": package.get("session_id"),
        "state": state,
        "handoff_type": "controlled_worker_queue",
    }
