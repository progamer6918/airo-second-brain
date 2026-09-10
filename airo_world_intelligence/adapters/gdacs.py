"""
airo_world_intelligence.adapters.gdacs — Read-only GDACS Feed Adapter.
Consumes public Global Disaster Alert and Coordination System RSS/GeoRSS feeds.
"""

import xml.etree.ElementTree as ET
import urllib.request
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any

from airo_world_intelligence.schema import NormalizedIntelligenceRecord

# Use 24h rolling feed (fast, low payload, contains real-time active alerts)
DEFAULT_GDACS_URL = "https://www.gdacs.org/xml/rss_24h.xml"

GDACS_NS = "http://www.gdacs.org"
GEORSS_NS = "http://www.georss.org/georss"


def fetch_gdacs_disasters(
    feed_url: str = DEFAULT_GDACS_URL,
    timeout: float = 25.0
) -> List[NormalizedIntelligenceRecord]:
    """Fetch and normalize multi-hazard disaster alerts from GDACS feed."""
    records: List[NormalizedIntelligenceRecord] = []
    req = urllib.request.Request(
        feed_url,
        headers={"User-Agent": "AIRO-World-Intelligence/1.0"}
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            xml_text = resp.read().decode("utf-8", errors="replace")
        root = ET.fromstring(xml_text)
    except Exception:
        return []

    for item in root.findall(".//item"):
        title_el = item.find("title")
        desc_el = item.find("description")
        link_el = item.find("link")
        pub_el = item.find("pubDate")

        title = title_el.text.strip() if title_el is not None and title_el.text else "GDACS Disaster Alert"
        desc = desc_el.text.strip() if desc_el is not None and desc_el.text else "No description available."
        link = link_el.text.strip() if link_el is not None and link_el.text else ""

        # Coordinates from georss:point (format: "lat lon")
        coords = None
        point_el = item.find(f"{{{GEORSS_NS}}}point")
        if point_el is not None and point_el.text:
            parts = point_el.text.strip().split()
            if len(parts) >= 2:
                try:
                    lat = float(parts[0])
                    lon = float(parts[1])
                    coords = [lon, lat]
                except ValueError:
                    coords = None

        # GDACS specific fields using Clark notation
        alert_el = item.find(f"{{{GDACS_NS}}}alertlevel")
        event_el = item.find(f"{{{GDACS_NS}}}eventtype")
        country_el = item.find(f"{{{GDACS_NS}}}country")
        iso3_el = item.find(f"{{{GDACS_NS}}}iso3")
        severity_el = item.find(f"{{{GDACS_NS}}}severity")

        alert_level = (alert_el.text.strip() if alert_el is not None and alert_el.text else "Green").upper()
        event_type = event_el.text.strip() if event_el is not None and event_el.text else "DISASTER"
        country = country_el.text.strip() if country_el is not None and country_el.text else "Global"
        iso3 = iso3_el.text.strip() if iso3_el is not None and iso3_el.text else None
        gdacs_sev = severity_el.text.strip() if severity_el is not None and severity_el.text else ""

        # Severity mapping
        if alert_level == "RED":
            severity = "CRITICAL"
        elif alert_level == "ORANGE":
            severity = "HIGH"
        elif "GREEN" in alert_level:
            severity = "LOW"
        else:
            severity = "MEDIUM"

        # Timestamp normalization
        ts_iso = datetime.now(timezone.utc).isoformat()
        if pub_el is not None and pub_el.text:
            try:
                from email.utils import parsedate_to_datetime
                dt = parsedate_to_datetime(pub_el.text.strip())
                ts_iso = dt.astimezone(timezone.utc).isoformat()
            except Exception:
                pass

        summary_text = desc.replace("<p>", "").replace("</p>", "").replace("<b>", "").replace("</b>", "")
        summary_text = summary_text[:300].replace("\n", " ").strip()
        if not summary_text:
            summary_text = f"GDACS {event_type} alert ({alert_level}) in {country}."

        rec = NormalizedIntelligenceRecord(
            source="GDACS",
            category="DISASTER",
            timestamp=ts_iso,
            severity=severity,
            location={
                "name": country,
                "country_code": iso3,
                "coordinates": coords
            },
            title=title,
            summary=summary_text,
            confidence="CONFIRMED",
            metadata={
                "external_id": link or title,
                "url": link,
                "event_type": event_type,
                "alert_level": alert_level,
                "gdacs_severity": gdacs_sev
            }
        )
        if rec.validate():
            records.append(rec)

    return records
