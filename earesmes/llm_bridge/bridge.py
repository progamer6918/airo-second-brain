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

        # 4. Controlled Execution with Persona, Casual Fast-Path & Fallback
        from earesmes.llm_bridge.prompt_sanitizer import (
            extract_user_query_and_context,
            format_clean_reasoning_prompt,
            sanitize_reasoning_output,
        )
        from earesmes.routing.intent_router import classify_intent, IntentType, format_casual_response
        from earesmes.routing.model_policy import (
            DEFAULT_REASONING_MODEL,
            DEFAULT_FALLBACK_MODEL,
        )

        user_query, _ = extract_user_query_and_context(objective or "")

        # A. Casual Conversation Fast-Path (No LLM call)
        if classify_intent(user_query) == IntentType.CASUAL_CONVERSATION:
            casual_ans = format_casual_response(user_query)
            outcome = builder.set_outcome(
                result="BERHASIL",
                model_status="EXECUTED_LOCAL_CASUAL",
                output_reference=casual_ans,
                model_provider="local/casual_fast_path",
            ).build()
            outcome["routing_decision"] = {
                "primary_model": "NONE",
                "fallback_used": False,
                "fallback_reason": None,
                "selected_model": "NONE",
            }
            return outcome

        # B. Reasoning Path with Single Fallback
        primary_model = DEFAULT_REASONING_MODEL
        fallback_model = DEFAULT_FALLBACK_MODEL
        fallback_used = False
        fallback_reason = None

        clean_prompt = format_clean_reasoning_prompt(objective or "")
        success, stdout_output, err_msg = self.provider.invoke_quiet(clean_prompt, model=primary_model)

        # Detect failure condition on primary model
        combined_check = (stdout_output + " " + err_msg).lower()
        needs_fallback = False
        if any(k in combined_check for k in ["429", "rate limit"]):
            needs_fallback = True
            fallback_reason = "HTTP_429"
        elif any(k in combined_check for k in ["api call failed", "http 500", "no endpoints found"]):
            needs_fallback = True
            fallback_reason = "PROVIDER_ERROR"
        elif not success:
            needs_fallback = True
            fallback_reason = "PRIMARY_NON_ZERO_EXIT"

        # Immediate single fallback without retry loop
        if needs_fallback and fallback_model:
            fallback_used = True
            fb_success, fb_stdout, fb_err = self.provider.invoke_quiet(clean_prompt, model=fallback_model)
            fb_check = (fb_stdout + " " + fb_err).lower()
            if fb_success and not any(k in fb_check for k in ["429", "rate limit", "api call failed"]):
                success = True
                stdout_output = fb_stdout
                err_msg = ""
            else:
                success = fb_success
                stdout_output = fb_stdout
                err_msg = fb_err or fb_stdout

        clean_output = sanitize_reasoning_output(stdout_output)
        outcome = builder.set_outcome(
            result="BERHASIL" if success else "GAGAL",
            model_status="EXECUTED" if success else "EXECUTION_FAILED",
            output_reference=clean_output[:4000] if success else None,
            error=err_msg if not success else None,
            model_provider=fallback_model if fallback_used else primary_model,
        ).build()
        outcome["routing_decision"] = {
            "primary_model": primary_model,
            "fallback_used": fallback_used,
            "fallback_reason": fallback_reason,
            "selected_model": fallback_model if fallback_used else primary_model,
        }
        return outcome
