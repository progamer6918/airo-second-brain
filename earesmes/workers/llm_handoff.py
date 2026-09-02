"""
Controlled LLM handoff boundary.

Phase 4:
- validates approved worker package
- prepares LLMBridge handoff metadata
- does not execute model call
"""


class LLMHandoff:

    def validate(self, package):

        required = [
            "job_id",
            "project_id",
            "session_id",
            "approval_status",
            "objective",
        ]

        missing = [
            x for x in required
            if x not in package
        ]

        if missing:
            return {
                "ready": False,
                "missing": missing,
            }

        if package["approval_status"] != "approved":
            return {
                "ready": False,
                "reason": "approval_required",
            }

        return {
            "ready": True,
            "job_id": package["job_id"],
        }


    def build_bridge_metadata(self, package):

        return {
            "job_id": package["job_id"],
            "project_id": package["project_id"],
            "session_id": package["session_id"],
            "objective": package["objective"],
            "source": "controlled_worker_queue",
        }
