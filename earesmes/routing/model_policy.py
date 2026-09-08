"""
EARESMES Capability-Aware Model Routing Policy — P2.3
=====================================================
Deterministic capability-to-model mapping with single-tier fallback.
Adheres strictly to EAB Prevention:
  - NO dynamic benchmarking or scoring
  - NO autonomous model switching
  - NO multi-tier loop

Centralized Configuration:
  Primary Reasoning: nvidia/nemotron-3.5-lightning:free
  Primary Research:  nvidia/nemotron-3.5-lightning:free
  Single Fallback:   google/gemini-2.0-flash-exp:free
"""

import time
from typing import Dict, Any, Optional, Tuple, Callable

# Centralized policy models
DEFAULT_REASONING_MODEL = "nvidia/nemotron-3.5-lightning:free"
DEFAULT_RESEARCH_MODEL = "nvidia/nemotron-3.5-lightning:free"
DEFAULT_FALLBACK_MODEL = "minimax/minimax-m2.7:free"


def resolve_model_policy(intent: str) -> Dict[str, Any]:
    """
    Resolve static model policy based on capability/intent.
    """
    intent_upper = intent.upper() if intent else "UNKNOWN"

    # Deterministic Local / Retrieval Paths (NO LLM REQUIRED)
    if intent_upper in ["GREETING", "CONVERSATIONAL_COURTESY", "CASUAL_CONVERSATION", "DAILY_BRIEFING", "PROJECT_CONTINUITY", "KNOWLEDGE_QUERY"]:
        return {
            "intent": intent_upper,
            "capability": intent_upper.lower(),
            "selected_model": "NONE",
            "fallback_model": None,
            "requires_llm": False,
            "policy_reason": "deterministic_local_or_asb_retrieval",
            "fallback_used": False,
            "fallback_reason": None,
            "timestamp": time.time()
        }

    # Research Capability
    if intent_upper == "RESEARCH_QUERY":
        return {
            "intent": intent_upper,
            "capability": "research",
            "selected_model": DEFAULT_RESEARCH_MODEL,
            "fallback_model": DEFAULT_FALLBACK_MODEL,
            "requires_llm": True,
            "policy_reason": "external_synthesis_required",
            "fallback_used": False,
            "fallback_reason": None,
            "timestamp": time.time()
        }

    # Decision Support & Action Request
    if intent_upper in ["DECISION_SUPPORT", "ACTION_REQUEST", "ACTION"]:
        return {
            "intent": intent_upper,
            "capability": "reasoning_and_action",
            "selected_model": DEFAULT_REASONING_MODEL,
            "fallback_model": DEFAULT_FALLBACK_MODEL,
            "requires_llm": True,
            "policy_reason": "context_reasoning_and_governance_required",
            "fallback_used": False,
            "fallback_reason": None,
            "timestamp": time.time()
        }

    # Default General Reasoning Path
    return {
        "intent": intent_upper,
        "capability": "general_reasoning",
        "selected_model": DEFAULT_REASONING_MODEL,
        "fallback_model": DEFAULT_FALLBACK_MODEL,
        "requires_llm": True,
        "policy_reason": "default_llm_reasoning",
        "fallback_used": False,
        "fallback_reason": None,
        "timestamp": time.time()
    }


def execute_with_fallback(
    invoke_func: Callable[[str, str], Tuple[bool, str, str]],
    prompt: str,
    policy: Dict[str, Any]
) -> Tuple[bool, str, str, Dict[str, Any]]:
    """
    Execute invocation using primary model; fallback EXACTLY ONCE if primary fails.
    Returns: (success, result_text, error_msg, routing_receipt)
    """
    primary_model = policy.get("selected_model", DEFAULT_REASONING_MODEL)
    fallback_model = policy.get("fallback_model", DEFAULT_FALLBACK_MODEL)

    routing_receipt = {
        "intent": policy.get("intent", "UNKNOWN"),
        "capability": policy.get("capability", "unknown"),
        "selected_model": primary_model,
        "fallback_used": False,
        "fallback_reason": None,
        "timestamp": time.time()
    }

    # If deterministic path, return without model invocation
    if not policy.get("requires_llm", True) or primary_model == "NONE":
        return True, "Deterministic response", "", routing_receipt

    # 1. Attempt Primary Model
    success, out, err = invoke_func(prompt, primary_model)
    if success:
        return True, out, err, routing_receipt

    # 2. Primary Failed -> Trigger One-Level Fallback
    fallback_reason = "PROVIDER_ERROR"
    err_lower = (err or "").lower()
    if "429" in err_lower or "rate" in err_lower:
        fallback_reason = "HTTP_429"
    elif "404" in err_lower or "not found" in err_lower:
        fallback_reason = "HTTP_404"
    elif "500" in err_lower or "internal" in err_lower:
        fallback_reason = "HTTP_500"
    elif "timeout" in err_lower:
        fallback_reason = "TIMEOUT"

    routing_receipt["fallback_used"] = True
    routing_receipt["fallback_reason"] = fallback_reason
    routing_receipt["selected_model"] = fallback_model

    # 3. Attempt Fallback Model (EXACTLY ONCE)
    fb_success, fb_out, fb_err = invoke_func(prompt, fallback_model)
    if fb_success:
        return True, fb_out, fb_err, routing_receipt

    # 4. Controlled Failure (No looping)
    return False, fb_out, f"Primary failed ({err}); Fallback failed ({fb_err})", routing_receipt
