"""
Pre-LLM worker orchestration gate.

No Hermes call.
No model call.
Only readiness decision.
"""

from .package_consumer import PackageConsumer
from .llm_handoff import LLMHandoff
from .execution_policy import ExecutionPolicy


class PolicyOrchestrator:
    def __init__(self):
        self.consumer = PackageConsumer()
        self.handoff = LLMHandoff()
        self.policy = ExecutionPolicy()

    def evaluate(self, package):
        validation = self.consumer.validate(package)

        if not validation.get("valid"):
            return {
                "status": "BLOCKED",
                "reason": "INVALID_PACKAGE"
            }

        handoff = self.handoff.validate(package)

        if not handoff.get("ready"):
            return {
                "status": "BLOCKED",
                "reason": "HANDOFF_NOT_READY"
            }

        decision = self.policy.decide(package)

        return {
            "status": (
                "READY_FOR_LLM"
                if decision["model_call_allowed"]
                else "REVIEW_REQUIRED"
            ),
            "decision": decision,
        }
