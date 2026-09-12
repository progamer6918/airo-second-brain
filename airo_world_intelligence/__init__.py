"""
airo_world_intelligence — Minimal read-only public intelligence fetcher library.
Provides normalized ingestion contracts and Hermes context bridge.
"""

from airo_world_intelligence.schema import NormalizedIntelligenceRecord
from airo_world_intelligence.adapters.usgs import fetch_usgs_earthquakes
from airo_world_intelligence.adapters.gdacs import fetch_gdacs_disasters
from airo_world_intelligence.adapters.weather import fetch_weather_signals
from airo_world_intelligence.adapters.rss import fetch_rss_news
from airo_world_intelligence.bridge import (
    WORLD_INTELLIGENCE_CONTEXT_AVAILABLE,
    get_world_intelligence_context,
    format_context_for_prompt
)

__all__ = [
    "NormalizedIntelligenceRecord",
    "fetch_usgs_earthquakes",
    "fetch_gdacs_disasters",
    "fetch_weather_signals",
    "fetch_rss_news",
    "WORLD_INTELLIGENCE_CONTEXT_AVAILABLE",
    "get_world_intelligence_context",
    "format_context_for_prompt"
]
from airo_world_intelligence.presentation import format_world_brief_for_telegram
__all__.append("format_world_brief_for_telegram")
