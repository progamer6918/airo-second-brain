"""
EARESMES Controlled LLM Bridge — V1
===================================
Main bridge interface for processing validated execution packages.

Responsibilities:
  - receive validated execution package reference
  - validate required fields exist and approval status
  - call provider adapter
  - return structured result
"""

from pathlib import Path
from typing import Dict, Any, Optional

from earesmes.llm_bridge.providers.hermes import HermesProviderAdapter
from earesmes.llm_bridge.receipts import BridgeReceiptBuilder


class LLMBridge:
    """Main controlled LLM bridge interface."""

    def __init__(self, provider_adapter: Optional[HermesProviderAdapter] = None) -> None:
        self.provider = provider_adapter or HermesProviderAdapter()

    def process_package(
        self,
        job_id: str,
        session_id: Optional[str] = None,
        project_id: Optional[str] = None,
        objective: Optional[str] = None,
        approval_status: Optional[str] = None,
        package_path: Optional[str] = None,
        dry_run: bool = True,
    ) -> Dict[str, Any]:
        """
        Process a validated execution package through the LLM bridge.
        If dry_run=True (default), validates contract without model execution.
        """
        builder = BridgeReceiptBuilder(
            job_id=job_id,
            session_id=session_id,
            project_id=project_id,
            objective=objective,
            approval_status=approval_status,
            package_path=package_path,
        )

        # 1. Validate required fields
        if not job_id:
            return builder.set_outcome(
                result="GAGAL",
                model_status="REJECTED",
                error="Missing required field: job_id",
            ).build()

        if approval_status != "approved":
            return builder.set_outcome(
                result="GAGAL",
                model_status="REJECTED_UNAPPROVED",
                error=f"Job approval status '{approval_status}' is not approved",
            ).build()

        # 2. Check package directory existence if path provided
        if package_path:
            pkg_p = Path(package_path)
            if not pkg_p.exists():
                return builder.set_outcome(
                    result="GAGAL",
                    model_status="PACKAGE_NOT_FOUND",
                    error=f"Execution package path '{package_path}' does not exist",
                ).build()

        # 3. Handle dry-run / readiness validation
        if dry_run:
            avail, reason = self.provider.check_availability()
            if not avail:
                return builder.set_outcome(
                    result="TERHAMBAT",
                    model_status="PROVIDER_UNAVAILABLE",
                    error=reason,
                ).build()
            return builder.set_outcome(
                result="BERHASIL",
                model_status="READY_DRY_RUN",
                output_reference="PACKAGE_VALIDATED_DRY_RUN",
            ).build()

        # 4. Controlled Execution
        prompt = f"Execution Objective: {objective}"
        success, stdout_output, err_msg = self.provider.invoke_quiet(prompt)

        if success:
            return builder.set_outcome(
                result="BERHASIL",
                model_status="EXECUTED",
                output_reference=stdout_output[:500],
            ).build()
        else:
            return builder.set_outcome(
                result="GAGAL",
                model_status="EXECUTION_FAILED",
                error=err_msg,
            ).build()
