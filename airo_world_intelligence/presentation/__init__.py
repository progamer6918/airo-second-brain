"""
airo_world_intelligence.presentation — Presentation formatting layer for AIRO World Intelligence.
"""

from airo_world_intelligence.presentation.telegram import (
    format_world_brief_for_telegram,
    clean_escaped_markdown,
    normalize_sections,
    convert_markdown_tables,
    optimize_for_mobile,
    handle_long_message,
)

__all__ = [
    "format_world_brief_for_telegram",
    "clean_escaped_markdown",
    "normalize_sections",
    "convert_markdown_tables",
    "optimize_for_mobile",
    "handle_long_message",
]
