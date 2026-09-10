"""
airo_world_intelligence.adapters.usgs — Read-only USGS Earthquake API Adapter.
Consumes public USGS GeoJSON feeds without authentication or local persistence.
"""

import json
import urllib.request
import urllib.error
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any

from airo_world_intelligence.schema import NormalizedIntelligenceRecord

DEFAULT_USGS_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"


def fetch_usgs_earthquakes(
    feed_url: str = DEFAULT_USGS_URL,
    min_magnitude: float = 0.0,
    timeout: float = 10.0
) -> List[NormalizedIntelligenceRecord]:
    """Fetch and normalize earthquake signals from USGS GeoJSON feed."""
    records: List[NormalizedIntelligenceRecord] = []
    req = urllib.request.Request(
        feed_url,
        headers={"User-Agent": "AIRO-World-Intelligence/1.0", "Accept": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        # Return empty list on network/transient failure without crashing
        return []

    features = data.get("features", [])
    for feat in features:
        props = feat.get("properties") or {}
        geom = feat.get("geometry") or {}
        coords = geom.get("coordinates") or []  # [longitude, latitude, depth]

        mag = props.get("mag")
        if mag is None:
            continue
        try:
            mag_float = float(mag)
        except (ValueError, TypeError):
            continue

        if mag_float < min_magnitude:
            continue

        # Severity mapping
        alert = str(props.get("alert") or "").lower()
        if mag_float >= 7.0 or alert == "red":
            severity = "CRITICAL"
        elif mag_float >= 6.0 or alert == "orange":
            severity = "HIGH"
        elif mag_float >= 4.5 or alert == "yellow":
            severity = "MEDIUM"
        else:
            severity = "LOW"

        # Timestamp normalization
        time_ms = props.get("time")
        if time_ms:
            ts_iso = datetime.fromtimestamp(time_ms / 1000.0, tz=timezone.utc).isoformat()
        else:
            ts_iso = datetime.now(timezone.utc).isoformat()

        place = props.get("place") or "Unknown Location"
        title = props.get("title") or f"M {mag_float:.1f} Earthquake - {place}"
        summary = (
            f"Seismic event of magnitude {mag_float:.1f} recorded at {place}. "
            f"Depth: {coords[2] if len(coords) > 2 else 'unknown'} km. "
            f"Tsunami flag: {bool(props.get('tsunami'))}."
        )

        lon_lat = [coords[0], coords[1]] if len(coords) >= 2 else None

        rec = NormalizedIntelligenceRecord(
            source="USGS",
            category="SEISMIC",
            timestamp=ts_iso,
            severity=severity,
            location={
                "name": place,
                "country_code": None,
                "coordinates": lon_lat
            },
            title=title,
            summary=summary,
            confidence="OBSERVED",
            metadata={
                "external_id": str(feat.get("id") or props.get("code") or ""),
                "url": props.get("url") or "",
                "raw_score": mag_float,
                "alert_level": alert.upper() if alert else None,
                "tsunami_alert": bool(props.get("tsunami")),
                "felt_reports": props.get("felt")
            }
        )
        if rec.validate():
            records.append(rec)

    return records
