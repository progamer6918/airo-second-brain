r"""
airo_world_intelligence.presentation.telegram

Mobile-first Telegram presentation layer for AIRO World Intelligence.
Formats Hermes reasoning output into clean, executive-ready Telegram briefings:
- Cleans escaped markdown (\*\* -> **, \### -> ###)
- Normalizes section headers (### Section -> SECTION TITLE with spacing)
- Converts raw markdown tables into mobile-friendly bullet format
- Optimizes spacing and removes excessive separator noise
- Safely handles long messages to stay within Telegram mobile constraints
"""

import re
from typing import Dict, List, Optional

COUNTRY_FLAGS: Dict[str, str] = {
    "indonesia": "🇮🇩",
    "cambodia": "🇰🇭",
    "japan": "🇯🇵",
    "united states": "🇺🇸",
    "usa": "🇺🇸",
    "us": "🇺🇸",
    "china": "🇨🇳",
    "philippines": "🇵🇭",
    "thailand": "🇹🇭",
    "vietnam": "🇻🇳",
    "malaysia": "🇲🇾",
    "singapore": "🇸🇬",
    "myanmar": "🇲🇲",
    "laos": "🇱🇦",
    "papua new guinea": "🇵🇬",
    "australia": "🇦🇺",
    "india": "🇮🇳",
    "costa rica": "🇨🇷",
    "bolivia": "🇧🇴",
    "peru": "🇵🇪",
    "iran": "🇮🇷",
    "russia": "🇷🇺",
    "ukraine": "🇺🇦",
    "united kingdom": "🇬🇧",
    "uk": "🇬🇧",
    "taiwan": "🇹🇼",
    "south korea": "🇰🇷",
    "korea": "🇰🇷",
    "north korea": "🇰🇵",
    "turkey": "🇹🇷",
    "türkiye": "🇹🇷",
    "israel": "🇮🇱",
    "palestine": "🇵🇸",
    "gaza": "🇵🇸",
    "lebanon": "🇱🇧",
    "syria": "🇸🇾",
    "yemen": "🇾🇪",
    "brazil": "🇧🇷",
    "canada": "🇨🇦",
    "germany": "🇩🇪",
    "france": "🇫🇷",
}


def _add_country_flag(text: str) -> str:
    clean_name = text.strip()
    for ch in clean_name[:2]:
        if ord(ch) > 127000 or ord(ch) in range(0x1F1E6, 0x1F1FF + 1):
            return clean_name
    flag = COUNTRY_FLAGS.get(clean_name.lower())
    if flag:
        return f"{flag} {clean_name}"
    return clean_name


def clean_escaped_markdown(text: str) -> str:
    r"""
    1. Markdown normalization:
    Converts escaped markdown sequences like \*\*text\*\* into readable **text**, \### into ###, etc.
    """
    if not text:
        return ""
    # Unescape common escaped markdown symbols: \*, \_, \#, \[, \], \(, \), \|, \-, \+, \`
    return re.sub(r'\\([*_#\[\]()|\-+`])', r'\1', text)


def normalize_sections(text: str) -> str:
    """
    2. Section normalization:
    Converts:
    ### Section
    into:
    SECTION TITLE
    with Telegram-friendly spacing.
    """
    if not text:
        return ""

    def section_repl(match):
        header_content = match.group(1).strip()
        # Strip any bold wrapper inside header e.g. **Title**
        header_content = re.sub(r'^\*\*([^\*]+)\*\*$', r'\1', header_content).strip()
        return f"\n\n{header_content.upper()}\n"

    result = re.sub(r'^(?:#{1,6})\s*(.+?)$', section_repl, text, flags=re.MULTILINE)
    result = re.sub(r'\n{3,}', '\n\n', result)
    return result


def convert_markdown_tables(text: str) -> str:
    """
    3. Table conversion:
    Converts markdown tables into mobile-friendly bullet format.

    Example:
    | Topic | Impact |
    |---|---|
    | Cambodia | Logistics |

    Becomes:
    🇰🇭 Cambodia

    • Impact:
      Logistics
    """
    if not text or "|" not in text:
        return text

    lines = text.split("\n")
    output_lines: List[str] = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # Detect table start: line contains | and next line is separator row (e.g. |---|)
        if stripped.startswith("|") and i + 1 < n and re.match(r'^[ \t]*\|(?:\s*:?-+:?\s*\|)+[ \t]*$', lines[i + 1].strip()):
            header_cells = [c.strip() for c in stripped.split("|")[1:-1]]
            i += 2  # Skip header and separator

            table_blocks = []
            while i < n and lines[i].strip().startswith("|"):
                row_cells = [c.strip() for c in lines[i].strip().split("|")[1:-1]]
                if row_cells and any(row_cells):
                    topic = _add_country_flag(row_cells[0])
                    entry_lines = [topic, ""]
                    for col_idx in range(1, len(row_cells)):
                        val = row_cells[col_idx]
                        hdr = header_cells[col_idx] if col_idx < len(header_cells) else f"Detail {col_idx}"
                        entry_lines.append(f"• {hdr}:")
                        entry_lines.append(f"  {val}")
                    table_blocks.append("\n".join(entry_lines))
                i += 1

            if table_blocks:
                output_lines.append("\n\n".join(table_blocks))
            continue

        output_lines.append(line)
        i += 1

    return "\n".join(output_lines)


def optimize_for_mobile(text: str) -> str:
    """
    4. Mobile optimization:
    - Avoid excessive separators (---, ===, ***)
    - Keep executive readability
    - Avoid huge walls of text
    """
    if not text:
        return ""

    # Remove horizontal rules that clutter mobile view
    text = re.sub(r'^[ \t]*[-=_*]{3,}[ \t]*$', '', text, flags=re.MULTILINE)

    # Normalize excessive consecutive blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


def handle_long_message(text: str, max_chars: int = 3850) -> str:
    """
    5. Long response handling:
    Implement safe compression/truncation strategy only for presentation.
    Preserves critical intelligence sections without abrupt mid-sentence cuts.
    """
    if len(text) <= max_chars:
        return text

    compacted = re.sub(r'\n{2,}', '\n\n', text).strip()
    if len(compacted) <= max_chars:
        return compacted

    truncated_candidate = compacted[:max_chars]
    last_break = truncated_candidate.rfind("\n\n")
    if last_break > max_chars * 0.7:
        truncated_candidate = truncated_candidate[:last_break].strip()
    else:
        last_dot = truncated_candidate.rfind(". ")
        if last_dot > max_chars * 0.7:
            truncated_candidate = truncated_candidate[:last_dot + 1].strip()

    notice = "\n\n_(Laporan lengkap dipadatkan untuk kenyamanan tampilan Telegram)_"
    return truncated_candidate + notice


def format_world_brief_for_telegram(text: str) -> str:
    """
    Main callable pipeline for AIRO World Intelligence Telegram Presentation.
    """
    if not text:
        return ""

    cleaned = clean_escaped_markdown(text)
    table_converted = convert_markdown_tables(cleaned)
    section_normalized = normalize_sections(table_converted)
    mobile_optimized = optimize_for_mobile(section_normalized)
    final_text = handle_long_message(mobile_optimized)

    return final_text
