"""
airo_world_intelligence.adapters.rss — Read-only Public RSS News Adapter.
Consumes configured public news feeds for global situational and geopolitical context.
"""

import xml.etree.ElementTree as ET
import urllib.request
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any

from airo_world_intelligence.schema import NormalizedIntelligenceRecord

DEFAULT_RSS_FEEDS = [
    {"name": "BBC World", "url": "http://feeds.bbci.co.uk/news/world/rss.xml"},
    {"name": "NYT World", "url": "https://rss.nytimes.com/services/xml/rss/World.xml"}
]


def fetch_rss_news(
    feeds: Optional[List[Dict[str, str]]] = None,
    max_items_per_feed: int = 5,
    timeout: float = 10.0
) -> List[NormalizedIntelligenceRecord]:
    """Fetch and normalize global news context from public RSS feeds."""
    if feeds is None:
        feeds = DEFAULT_RSS_FEEDS

    records: List[NormalizedIntelligenceRecord] = []

    for feed in feeds:
        feed_name = feed.get("name", "Public RSS")
        feed_url = feed.get("url", "")
        if not feed_url:
            continue

        req = urllib.request.Request(
            feed_url,
            headers={"User-Agent": "AIRO-World-Intelligence/1.0", "Accept": "application/rss+xml, text/xml"}
        )

        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                xml_text = resp.read().decode("utf-8", errors="replace")
            root = ET.fromstring(xml_text)
        except Exception:
            continue

        items = root.findall(".//item")
        count = 0
        for item in items:
            if count >= max_items_per_feed:
                break

            title_el = item.find("title")
            desc_el = item.find("description")
            link_el = item.find("link")
            pub_el = item.find("pubDate")

            title = title_el.text.strip() if title_el is not None and title_el.text else "Global News Item"
            desc = desc_el.text.strip() if desc_el is not None and desc_el.text else "No description available."
            link = link_el.text.strip() if link_el is not None and link_el.text else ""

            # Clean HTML tags if any in description
            clean_desc = desc.replace("<p>", "").replace("</p>", "").replace("<b>", "").replace("</b>", "").strip()

            ts_iso = datetime.now(timezone.utc).isoformat()
            if pub_el is not None and pub_el.text:
                try:
                    from email.utils import parsedate_to_datetime
                    dt = parsedate_to_datetime(pub_el.text.strip())
                    ts_iso = dt.astimezone(timezone.utc).isoformat()
                except Exception:
                    pass

            rec = NormalizedIntelligenceRecord(
                source=f"RSS_{feed_name.upper().replace(' ', '_')}",
                category="NEWS",
                timestamp=ts_iso,
                severity="LOW",
                location={
                    "name": "Global",
                    "country_code": None,
                    "coordinates": None
                },
                title=f"[{feed_name}] {title}",
                summary=clean_desc[:300].strip(),
                confidence="REPORTED",
                metadata={
                    "feed_name": feed_name,
                    "url": link,
                    "external_id": link or title
                }
            )
            if rec.validate():
                records.append(rec)
                count += 1

    return records
