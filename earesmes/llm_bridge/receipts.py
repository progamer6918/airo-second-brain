"""
EARESMES Controlled LLM Bridge Receipt Generator — V1
=====================================================
Structured receipt data & builder for bridge executions.
"""

from datetime import datetime, timezone
from typing import Optional, Dict, Any


class BridgeReceiptBuilder:
    """Builder for structured LLM bridge receipts."""

    def __init__(
        self,
        job_id: str,
        session_id: Optional[str] = None,
        project_id: Optional[str] = None,
        objective: Optional[str] = None,
        approval_status: Optional[str] = None,
        package_path: Optional[str] = None,
    ) -> None:
        self.job_id = job_id
        self.session_id = session_id or "NONE"
        self.project_id = project_id or "earesmes-runtime-assistant-v1"
        self.objective = objective or ""
        self.approval_status = approval_status or "unapproved"
        self.package_path = package_path or ""
        self.result = "UNTESTED"
        self.model_provider = "openrouter/hermes"
        self.model_status = "INITIALIZED"
        self.output_reference = "NONE"
        self.error = "NONE"

    def set_outcome(
        self,
        result: str,
        model_status: str,
        output_reference: Optional[str] = None,
        error: Optional[str] = None,
        model_provider: Optional[str] = None,
    ) -> "BridgeReceiptBuilder":
        self.result = result
        self.model_status = model_status
        if output_reference:
            self.output_reference = output_reference
        if error:
            self.error = error
        if model_provider:
            self.model_provider = model_provider
        return self

    def build(self) -> Dict[str, Any]:
        return {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "job_id": self.job_id,
            "session_id": self.session_id,
            "project_id": self.project_id,
            "objective": self.objective,
            "approval_status": self.approval_status,
            "package_path": self.package_path,
            "result": self.result,
            "model_provider": self.model_provider,
            "model_status": self.model_status,
            "output_reference": self.output_reference,
            "error": self.error,
        }
