"""
airo_world_intelligence.adapters — Collection of read-only intelligence source adapters.
"""

from airo_world_intelligence.adapters.usgs import fetch_usgs_earthquakes
from airo_world_intelligence.adapters.gdacs import fetch_gdacs_disasters
from airo_world_intelligence.adapters.weather import fetch_weather_signals
from airo_world_intelligence.adapters.rss import fetch_rss_news

__all__ = [
    "fetch_usgs_earthquakes",
    "fetch_gdacs_disasters",
    "fetch_weather_signals",
    "fetch_rss_news"
]
