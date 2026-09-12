"""Earesmes Routing Package."""
from earesmes.routing.intent_router import (
    IntentType,
    PresentationMode,
    classify_intent,
    resolve_presentation_mode,
    format_casual_response,
)
from earesmes.routing.model_policy import (
    resolve_model_policy,
    execute_with_fallback,
    DEFAULT_REASONING_MODEL,
    DEFAULT_RESEARCH_MODEL,
    DEFAULT_FALLBACK_MODEL,
)

__all__ = [
    "IntentType",
    "PresentationMode",
    "classify_intent",
    "resolve_presentation_mode",
    "format_casual_response",
    "resolve_model_policy",
    "execute_with_fallback",
    "DEFAULT_REASONING_MODEL",
    "DEFAULT_RESEARCH_MODEL",
    "DEFAULT_FALLBACK_MODEL",
]
