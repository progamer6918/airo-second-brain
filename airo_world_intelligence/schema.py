"""
airo_world_intelligence.schema — Normalized Intelligence Schema Contract.

Provides a unified, source-agnostic data contract for all ingested world
intelligence signals (seismic, disaster, weather/climate, news, geopolitical).
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone


VALID_SEVERITIES = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
VALID_CONFIDENCES = {"OBSERVED", "CONFIRMED", "PREDICTED", "REPORTED"}
REQUIRED_FIELDS = {
    "source", "category", "timestamp", "severity",
    "location", "title", "summary", "confidence", "metadata"
}


@dataclass
class NormalizedIntelligenceRecord:
    """Canonical schema for any intelligence signal ingested by AIRO."""
    source: str
    category: str
    timestamp: str  # ISO 8601 UTC
    severity: str   # LOW | MEDIUM | HIGH | CRITICAL
    location: Dict[str, Any]  # {"name": str, "country_code": Optional[str], "coordinates": Optional[List[float]]}
    title: str
    summary: str
    confidence: str  # OBSERVED | CONFIRMED | PREDICTED | REPORTED
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert record to plain Python dict matching the schema contract."""
        return asdict(self)

    def validate(self) -> bool:
        """Validate that all mandatory fields are present, correctly typed, and non-empty."""
        d = self.to_dict()
        for f in REQUIRED_FIELDS:
            if f not in d:
                return False
            if d[f] is None:
                return False

        if not isinstance(self.source, str) or not self.source.strip():
            return False
        if not isinstance(self.category, str) or not self.category.strip():
            return False
        if not isinstance(self.timestamp, str) or not self.timestamp.strip():
            return False
        if self.severity not in VALID_SEVERITIES:
            return False
        if not isinstance(self.location, dict) or "name" not in self.location:
            return False
        if not isinstance(self.title, str) or not self.title.strip():
            return False
        if not isinstance(self.summary, str) or not self.summary.strip():
            return False
        if self.confidence not in VALID_CONFIDENCES:
            return False
        if not isinstance(self.metadata, dict):
            return False
        return True
