"""
Deterministic runtime safety classifier.

Boundary:
- capability_resolution remains authority.
- worker runtime guard only.
- no LLM calls.
"""

HIGH_RISK_SIGNALS = {
    "delete",
    "remove",
    "modify",
    "write",
    "install",
    "deploy",
    "push",
    "commit",
    "service",
    "restart",
    "stop",
    "credential",
    "secret",
    "permission",
    "network",
    "production",
}


class RiskClassifier:

    def classify(self, objective):
        text = str(objective).lower()

        matched = [
            x for x in HIGH_RISK_SIGNALS
            if x in text
        ]

        if matched:
            return {
                "risk_level": "HIGH",
                "approval_required": True,
                "reason": "high_risk_signal",
                "signals": matched,
            }

        return {
            "risk_level": "LOW",
            "approval_required": False,
            "reason": "default_low_risk",
        }


    def runtime_check(self, package):
        objective = package.get("objective", "")
        declared = str(package.get("risk_level", "")).upper()

        result = self.classify(objective)

        if result["risk_level"] == "HIGH":
            return {
                "allowed": False,
                **result,
            }

        if declared != "LOW":
            return {
                "allowed": False,
                "risk_level": "REVIEW_REQUIRED",
                "approval_required": True,
                "reason": "missing_or_unknown_risk",
            }

        return {
            "allowed": True,
            **result,
        }
