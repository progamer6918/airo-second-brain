"""
airo_world_intelligence.adapters.weather — Read-only Public Weather Adapter.
Consumes public Open-Meteo endpoint for meteorological conditions and alerts.
"""

import json
import urllib.request
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any

from airo_world_intelligence.schema import NormalizedIntelligenceRecord

DEFAULT_LAT = -6.2088
DEFAULT_LON = 106.8456
DEFAULT_LOC_NAME = "Jakarta, Indonesia"


def fetch_weather_signals(
    latitude: float = DEFAULT_LAT,
    longitude: float = DEFAULT_LON,
    location_name: str = DEFAULT_LOC_NAME,
    timeout: float = 10.0
) -> List[NormalizedIntelligenceRecord]:
    """Fetch current weather observations and evaluate meteorological alert signals."""
    records: List[NormalizedIntelligenceRecord] = []
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}&"
        f"current=temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m&"
        f"timezone=auto"
    )
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "AIRO-World-Intelligence/1.0", "Accept": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception:
        return []

    curr = data.get("current") or {}
    if not curr:
        return []

    temp = curr.get("temperature_2m")
    precip = curr.get("precipitation", 0.0)
    wind_spd = curr.get("wind_speed_10m", 0.0)
    wcode = curr.get("weather_code", 0)

    # Meteorological severity classification
    # WMO code >= 95: Thunderstorm, wind_spd > 60: severe gale, precip > 20: heavy rain
    if wcode >= 95 or wind_spd > 70 or precip > 30:
        severity = "HIGH"
        status_label = "Severe Weather Alert"
    elif wcode >= 80 or wind_spd > 45 or precip > 10:
        severity = "MEDIUM"
        status_label = "Weather Advisory"
    else:
        severity = "LOW"
        status_label = "Normal Weather Conditions"

    title = f"{status_label} - {location_name}"
    summary = (
        f"Current meteorological signal for {location_name}: "
        f"Temperature {temp}C, Precipitation {precip}mm, Wind Speed {wind_spd} km/h (WMO Code {wcode})."
    )

    rec = NormalizedIntelligenceRecord(
        source="OPEN_METEO",
        category="METEOROLOGICAL",
        timestamp=datetime.now(timezone.utc).isoformat(),
        severity=severity,
        location={
            "name": location_name,
            "country_code": None,
            "coordinates": [longitude, latitude]
        },
        title=title,
        summary=summary,
        confidence="OBSERVED",
        metadata={
            "temperature_c": temp,
            "precipitation_mm": precip,
            "wind_speed_kmh": wind_spd,
            "weather_code": wcode
        }
    )
    if rec.validate():
        records.append(rec)

    return records
