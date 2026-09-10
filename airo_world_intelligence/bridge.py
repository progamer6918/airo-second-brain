"""
airo_world_intelligence.bridge — Context Bridge for AIRO Hermes with Noise Reduction & Relevance Ranking.

Provides a minimal, stateless, read-only bridge connecting public intelligence
fetchers to AIRO Hermes context with noise filtering and Indonesia-priority ranking.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import logging
import re

from airo_world_intelligence.schema import NormalizedIntelligenceRecord
from airo_world_intelligence.adapters.usgs import fetch_usgs_earthquakes
from airo_world_intelligence.adapters.gdacs import fetch_gdacs_disasters
from airo_world_intelligence.adapters.weather import fetch_weather_signals
from airo_world_intelligence.adapters.rss import fetch_rss_news

logger = logging.getLogger("airo_world_intelligence.bridge")

WORLD_INTELLIGENCE_CONTEXT_AVAILABLE = True

ID_KEYWORDS = {
    "indonesia", "jakarta", "java", "jawa", "sumatra", "sumatera", "bali",
    "sulawesi", "maluku", "papua", "banda", "flores", "sunda", "aceh",
    "lombok", "borneo", "kalimantan", "timor"
}


def is_indonesia_relevant(record: NormalizedIntelligenceRecord) -> bool:
    """Check whether record has geographical or direct relevance to Indonesia / ASEAN."""
    loc_name = str(record.location.get("name", "")).lower()
    country_code = str(record.location.get("country_code", "")).lower()
    title = record.title.lower()
    summary = record.summary.lower()
    combined = f"{loc_name} {country_code} {title} {summary}"
    return any(kw in combined for kw in ID_KEYWORDS)


def filter_noise(records: List[NormalizedIntelligenceRecord]) -> List[NormalizedIntelligenceRecord]:
    """
    Noise reduction rules:
    1. Title deduplication across syndicated feeds.
    2. Drop non-Indonesia micro-earthquakes (M < 4.5) without alert level.
    3. Retain all regional (Indonesia/ASEAN) alerts regardless of size.
    """
    filtered: List[NormalizedIntelligenceRecord] = []
    seen_titles = set()

    for r in records:
        # Title dedup
        norm_title = re.sub(r"[^\w\s]", "", r.title.lower()).strip()
        if norm_title in seen_titles:
            continue
        seen_titles.add(norm_title)

        is_id = is_indonesia_relevant(r)

        # Seismic noise filter: drop micro-quakes outside Indonesia
        if r.category == "SEISMIC":
            mag = float(r.metadata.get("raw_score", 0.0) or 0.0)
            if not is_id and mag < 4.5 and r.severity == "LOW" and not r.metadata.get("alert_level"):
                continue

        filtered.append(r)

    return filtered


def rank_relevance(records: List[NormalizedIntelligenceRecord]) -> List[NormalizedIntelligenceRecord]:
    """
    Relevance ranking rules:
    1. Indonesia / regional signals -> Highest priority (+100)
    2. CRITICAL global severity (GDACS Red, M >= 7.0) -> High priority (+80)
    3. HIGH global severity (GDACS Orange, M >= 6.0) -> Medium-high priority (+50)
    4. MEDIUM global severity -> Medium priority (+20)
    5. Curated Geopolitical News -> Context priority (+15)
    6. Routine / Minor signals -> Baseline (+5)
    """
    def score_record(r: NormalizedIntelligenceRecord) -> int:
        score = 0
        if is_indonesia_relevant(r):
            score += 100
        if r.severity == "CRITICAL":
            score += 80
        elif r.severity == "HIGH":
            score += 50
        elif r.severity == "MEDIUM":
            score += 20
        else:
            score += 5

        if r.category == "NEWS":
            score += 15
        elif r.category == "METEOROLOGICAL":
            score += 10
        return score

    return sorted(records, key=score_record, reverse=True)


def get_world_intelligence_context(
    include_seismic: bool = True,
    include_disaster: bool = True,
    include_weather: bool = True,
    include_news: bool = True,
    apply_tuning: bool = True,
    timeout: float = 10.0
) -> Dict[str, Any]:
    """
    Collects, filters, and ranks real-time signals from all configured public adapters.
    Returns structured, noise-reduced context payload for AIRO Hermes.
    """
    raw_records: List[NormalizedIntelligenceRecord] = []
    sources_queried = []
    sources_failed = []

    # 1. Seismic (USGS)
    if include_seismic:
        sources_queried.append("USGS")
        try:
            raw_records.extend(fetch_usgs_earthquakes(timeout=timeout))
        except Exception as e:
            logger.warning("USGS adapter fetch failed: %s", e)
            sources_failed.append("USGS")

    # 2. Multi-hazard Disasters (GDACS)
    if include_disaster:
        sources_queried.append("GDACS")
        try:
            raw_records.extend(fetch_gdacs_disasters(timeout=timeout))
        except Exception as e:
            logger.warning("GDACS adapter fetch failed: %s", e)
            sources_failed.append("GDACS")

    # 3. Weather / Climate (Open-Meteo)
    if include_weather:
        sources_queried.append("WEATHER")
        try:
            raw_records.extend(fetch_weather_signals(timeout=timeout))
        except Exception as e:
            logger.warning("Weather adapter fetch failed: %s", e)
            sources_failed.append("WEATHER")

    # 4. Curated News (RSS)
    if include_news:
        sources_queried.append("RSS")
        try:
            raw_records.extend(fetch_rss_news(timeout=timeout))
        except Exception as e:
            logger.warning("RSS adapter fetch failed: %s", e)
            sources_failed.append("RSS")

    # Apply noise reduction & ranking
    if apply_tuning and raw_records:
        filtered = filter_noise(raw_records)
        records = rank_relevance(filtered)
        noise_dropped = len(raw_records) - len(filtered)
    else:
        records = raw_records
        noise_dropped = 0

    # Separate categories & priorities
    id_signals = [r for r in records if is_indonesia_relevant(r)]
    high_severity = [r for r in records if r.severity in ("HIGH", "CRITICAL")]
    by_category: Dict[str, int] = {}
    for r in records:
        by_category[r.category] = by_category.get(r.category, 0) + 1

    # Format structured text summary with canonical sections
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    text_lines = [
        f"=== LIVE WORLD INTELLIGENCE CONTEXT ({now_str}) ===",
        f"Sources Queried: {', '.join(sources_queried)} | Signals Ingested: {len(records)} (Noise Filtered: {noise_dropped})",
    ]

    # Section A: Indonesia & Regional Priority
    text_lines.append("\n[1. RADAR & RELEVANSI INDONESIA]:")
    if id_signals:
        for s in id_signals[:5]:
            text_lines.append(f"• [{s.category}] {s.title} ({s.location.get('name')}) - Severity: {s.severity}\n  Ringkasan: {s.summary[:150]}")
    else:
        text_lines.append("• Nihil sinyal kritis langsung di teritori Indonesia saat ini.")

    # Section B: Global High & Critical Disasters
    text_lines.append("\n[2. SINYAL BENCANA & GEMPA KRITIS GLOBAL]:")
    if high_severity:
        for h in high_severity[:6]:
            text_lines.append(f"• [{h.category}] {h.title} ({h.location.get('name', 'Global')}) - Severity: {h.severity}\n  Ringkasan: {h.summary[:150]}")
    else:
        # Fallback to top significant events
        top_events = [r for r in records if r.category in ("SEISMIC", "DISASTER") and not is_indonesia_relevant(r)]
        if top_events:
            for ev in top_events[:5]:
                text_lines.append(f"• [{ev.category}] {ev.title} ({ev.location.get('name', 'Global')}) - Severity: {ev.severity}\n  Ringkasan: {ev.summary[:150]}")
        else:
            text_lines.append("• Tidak ada bencana berskala besar atau gempa signifikan (M >= 5.0) yang tercatat.")

    # Section C: Top Geopolitical & Macro News Context
    news_signals = [r for r in records if r.category == "NEWS"]
    if news_signals:
        text_lines.append("\n[3. KONTEKS GEOPOLITIK & BERITA MAKRO DUNIA]:")
        for n in news_signals[:5]:
            text_lines.append(f"• {n.title} - {n.summary[:140]}")

    text_summary = "\n".join(text_lines)

    return {
        "context_available": len(records) > 0,
        "flag_context_available": WORLD_INTELLIGENCE_CONTEXT_AVAILABLE,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sources_queried": sources_queried,
        "sources_failed": sources_failed,
        "total_records": len(records),
        "raw_records_count": len(raw_records),
        "noise_dropped_count": noise_dropped,
        "indonesia_relevant_count": len(id_signals),
        "high_severity_count": len(high_severity),
        "records_by_category": by_category,
        "records": [r.to_dict() for r in records],
        "text_summary": text_summary,
    }


def format_context_for_prompt(context_payload: Dict[str, Any]) -> str:
    """Helper to extract clean text block for injection into prompt context."""
    if not context_payload or not context_payload.get("context_available"):
        return ""
    return context_payload.get("text_summary", "")
