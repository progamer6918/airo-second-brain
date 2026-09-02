"""
Controlled worker execution policy.

Boundary:
- capability_resolution owns authority
- worker owns execution flow
- this layer prevents unsafe handoff
"""

from .risk_classifier import RiskClassifier


class ExecutionPolicy:
    def __init__(self):
        self.classifier = RiskClassifier()

    def decide(self, package):
        result = self.classifier.runtime_check(package)

        if not result.get("allowed", False):
            return {
                "decision": "REVIEW_REQUIRED",
                "model_call_allowed": False,
                "approval_required": True,
                "reason": result,
            }

        return {
            "decision": "EXECUTION_ALLOWED",
            "model_call_allowed": True,
            "approval_required": False,
            "reason": result,
        }
