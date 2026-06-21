from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class AgentResult:
    agent: str
    status: str
    confidence: float
    summary: str
    data: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_iso)

    def to_dict(self) -> dict[str, Any]:
        return {
            "agent": self.agent,
            "status": self.status,
            "confidence": float(self.confidence),
            "summary": self.summary,
            "data": self.data,
            "created_at": self.created_at,
        }


def clamp_confidence(value: float) -> float:
    return max(0.0, min(1.0, float(value)))
