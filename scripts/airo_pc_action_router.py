#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/airo_pc_action_router.py — Remote PC Action Router for AIRO Hermes.

Dispatches local desktop actions (browser, YouTube, links) from the cloud VPS
to the Owner's local PC via an atomic file queue.
"""

import os
import re
import json
import time
import uuid
import html
import urllib.request
import urllib.parse
import logging
from datetime import datetime
from typing import Optional, Tuple

logger = logging.getLogger("airo-pc-action-router")

QUEUE_BASE_DIR = os.path.expanduser("~/.local/state/airo-second-brain/pc-action-bridge/queue")
PENDING_DIR = os.path.join(QUEUE_BASE_DIR, "pending")
IN_PROGRESS_DIR = os.path.join(QUEUE_BASE_DIR, "in_progress")
DONE_DIR = os.path.join(QUEUE_BASE_DIR, "done")
DEAD_DIR = os.path.join(QUEUE_BASE_DIR, "dead")

os.makedirs(PENDING_DIR, exist_ok=True)
os.makedirs(IN_PROGRESS_DIR, exist_ok=True)
os.makedirs(DONE_DIR, exist_ok=True)
os.makedirs(DEAD_DIR, exist_ok=True)


def search_youtube_video(query: str) -> Tuple[str, str]:
    """
    Searches YouTube and returns (video_url, video_title).
    Zero external dependencies, parses public YouTube results directly.
    """
    clean_q = query.strip()
    encoded = urllib.parse.quote(clean_q)
    url = f"https://www.youtube.com/results?search_query={encoded}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"}
    )
    try:
        html_content = urllib.request.urlopen(req, timeout=8).read().decode("utf-8", errors="ignore")
        vids = re.findall(r"watch\?v=([a-zA-Z0-9_-]{11})", html_content)
        titles = re.findall(r'"title":\{"runs":\[\{"text":"([^"]+)"', html_content)

        if vids:
            seen = set()
            unique_vids = []
            for v in vids:
                if v not in seen:
                    seen.add(v)
                    unique_vids.append(v)
            vid = unique_vids[0]
            title = titles[0] if titles else clean_q
            ts = int(time.time())
            return f"https://www.youtube.com/watch?v={vid}&autoplay=1&airo_ts={ts}", title
    except Exception as e:
        logger.warning("YouTube search failed for '%s': %s", clean_q, e)

    return f"https://www.youtube.com/results?search_query={encoded}", clean_q


def enqueue_pc_action(action_type: str, payload: dict, chat_id: str = "") -> str:
    """Writes an atomic action packet to the pending queue."""
    action_id = f"act-{int(time.time())}-{uuid.uuid4().hex[:6]}"
    packet = {
        "action_id": action_id,
        "type": action_type,
        "payload": payload,
        "chat_id": str(chat_id),
        "created_at": datetime.now().isoformat(),
        "status": "pending"
    }

    tmp_file = os.path.join(PENDING_DIR, f"{action_id}.tmp")
    final_file = os.path.join(PENDING_DIR, f"{action_id}.json")

    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(packet, f, indent=2, ensure_ascii=False)
    os.replace(tmp_file, final_file)
    logger.info("Enqueued PC action %s (type=%s)", action_id, action_type)
    return action_id


class PCActionRouter:
    """Pre-router for desktop actions executed on Owner PC."""

    KNOWN_APPS = {
        "ppt": ("powerpoint", "Microsoft PowerPoint"),
        "powerpoint": ("powerpoint", "Microsoft PowerPoint"),
        "power point": ("powerpoint", "Microsoft PowerPoint"),
        "microsoft powerpoint": ("powerpoint", "Microsoft PowerPoint"),
        "microsoft power point": ("powerpoint", "Microsoft PowerPoint"),
        "excel": ("excel", "Microsoft Excel"),
        "microsoft excel": ("excel", "Microsoft Excel"),
        "word": ("word", "Microsoft Word"),
        "microsoft word": ("word", "Microsoft Word"),
        "spotify": ("spotify", "Spotify"),
        "vscode": ("vscode", "Visual Studio Code"),
        "vs code": ("vscode", "Visual Studio Code"),
        "code": ("vscode", "Visual Studio Code"),
        "notepad": ("notepad", "Notepad"),
        "catatan": ("notepad", "Notepad"),
        "calc": ("calc", "Kalkulator"),
        "kalkulator": ("calc", "Kalkulator"),
        "calculator": ("calc", "Kalkulator"),
        "chrome": ("chrome", "Google Chrome"),
        "brave": ("brave", "Brave Browser"),
        "edge": ("edge", "Microsoft Edge"),
        "explorer": ("explorer", "File Explorer"),
    }

    PATTERNS_APP = [
        re.compile(
            r"(?:coba\s+|tolong\s+|bro\s+|bukan\s+buka\s+youtube\s+ttg\s+[\w\s]+,\s*tapi\s+)*"
            r"(?:buka(?:in|kan)?|jalankan|start|launch)\s+"
            r"(?:aplikasi\s+|software\s+|program\s+)?"
            r"([a-zA-Z\s0-9]+?)"
            r"(?:\s+(?:di|pada)\s+(?:pc|laptop|komputer)(?:\s+(?:gw|gua|gue|ku|coba|dong|nih|ya))*|\s+(?:coba|dong|nih|ya))*$",
            re.IGNORECASE
        ),
    ]

    # Regex patterns
    PATTERNS_YOUTUBE = [
        # "Bro putar lagu Bohemian Rhapsody di YouTube PC", "Tolong putarin podcast Raditya Dika di pc gw"
        re.compile(
            r"(?:bro\s+|bang\s+|tolong\s+|coba\s+)*"
            r"(?:putar(?:in|kan)?|setel(?:in|kan)?|tonton(?:in|kan)?|buka(?:in|kan)?|play(?:-?in)?|main(?:in|kan)?|dengar(?:in|kan)?)\s+"
            r"(?:video|lagu|musik)?\s*"
            r"(.+?)\s*"
            r"(?:di|via)\s+(?:pc|laptop|komputer|browser|chrome|brave|yt|youtube)"
            r"(?:\s+(?:pc|laptop|komputer|browser|chrome|brave|yt|youtube|gw|gua|gue|dong|nih|ya|ku|bro|bang))*$",
            re.IGNORECASE
        ),
        # "di pc/laptop coba buka/putar X"
        re.compile(
            r"(?:di\s+(?:pc|laptop|komputer)(?:\s+(?:gw|gua|gue|ku))?)\s*"
            r"(?:coba\s+|tolong\s+|bro\s+)*"
            r"(?:buka(?:in|kan)?|putar(?:in|kan)?|play(?:-?in)?|tonton(?:in|kan)?|setel(?:in|kan)?|dengar(?:in|kan)?)\s*"
            r"(?:video|lagu|musik)?\s*(.+)",
            re.IGNORECASE
        ),
        # "buka youtube X", "play youtube X", "putar youtube X"
        re.compile(
            r"(?:bro\s+|bang\s+|tolong\s+|coba\s+)*"
            r"(?:buka(?:in|kan)?|play(?:-?in)?|putar(?:in|kan)?|setel(?:in|kan)?|tonton(?:in|kan)?)\s+"
            r"(?:youtube|yt)\s*(?:dan\s+(?:play|putar))?\s*(.+)",
            re.IGNORECASE
        ),
        # Catch-all PC media intent (only when NOT explicitly an app or anti-youtube)
        re.compile(
            r"(?:putar(?:in|kan)?|setel(?:in|kan)?|play(?:-?in)?|tonton(?:in|kan)?)\s+"
            r"(.+?)\s+"
            r"(?:di\s+(?:pc|laptop|komputer))",
            re.IGNORECASE
        ),
    ]

    PATTERNS_GENERIC_URL = [
        # "buka link/web/url https://... di pc"
        re.compile(r"(?:buka|open)\s+(?:link|url|web|situs|halaman)?\s*(https?://\S+)(?:\s+di\s+(?:pc|laptop|komputer))?", re.IGNORECASE),
        re.compile(r"(?:di\s+(?:pc|laptop|komputer)\s+)?(?:buka|open)\s+(https?://\S+)", re.IGNORECASE),
    ]

    PATTERNS_STATUS = [
        re.compile(r"^(?:cek\s+)?status\s+pc(?:\s+relay)?$", re.IGNORECASE),
        re.compile(r"^status\s+(?:pc|relay|bridge)$", re.IGNORECASE),
    ]

    @classmethod
    def route(cls, text: str, chat_id: str = "") -> Optional[str]:
        t = text.strip()

        # 1. Status Check
        for p in cls.PATTERNS_STATUS:
            if p.search(t):
                pending_count = len([f for f in os.listdir(PENDING_DIR) if f.endswith(".json")])
                done_count = len([f for f in os.listdir(DONE_DIR) if f.endswith(".json")])
                return (
                    f"🖥️ <b>Status PC Action Bridge</b>:\n"
                    f"• Antrean pending: <b>{pending_count}</b> tugas\n"
                    f"• Riwayat selesai: <b>{done_count}</b> tugas\n"
                    f"• Status antrean: <b>SIAP</b> 🚀\n\n"
                    f"<i>Pastikan daemon di PC lo aktif via <code>START_AIRO_PC_RELAY.bat</code> biar tugas langsung diproses seketika!</i>"
                )

        # 2. Native Desktop Application Launch (PowerPoint, Excel, Word, Spotify, etc.)
        for p in cls.PATTERNS_APP:
            m = p.search(t)
            if m:
                raw_app = m.group(1).strip().lower()
                raw_app = re.sub(r"^(?:aplikasi|software|program)\s+", "", raw_app).strip()
                raw_app = re.sub(r"\s+(?:di\s+(?:pc|laptop|komputer)|pc|laptop|komputer|gw|gua|gue|ku|coba|dong|nih|ya)$", "", raw_app).strip()
                if raw_app in cls.KNOWN_APPS:
                    app_key, display_name = cls.KNOWN_APPS[raw_app]
                    logger.info("PC_ACTION: Detected native desktop app intent for '%s' -> %s", raw_app, app_key)
                    payload = {
                        "app": app_key,
                        "display_name": display_name,
                        "raw_query": t
                    }
                    action_id = enqueue_pc_action("open_app", payload, chat_id=chat_id)
                    return f"Siap bro! Aplikasi <b>{html.escape(display_name)}</b> lagi gue bukain di PC lo sekarang. 🖥️"

        # If user explicitly specified NOT youtube or requested an app, do NOT fallback to YouTube
        if re.search(r"\b(?:bukan\s+youtube|bukan\s+yt|bukan\s+video|aplikasi\s+microsoft)\b", t, re.IGNORECASE):
            return None

        # 3. YouTube Search & Play
        for p in cls.PATTERNS_YOUTUBE:
            m = p.search(t)
            if m:
                raw_query = m.group(1).strip()
                # Clean filler words
                clean_query = re.sub(r"^(?:video|lagu|musik|tentang|channel)\s+", "", raw_query, flags=re.IGNORECASE).strip()
                clean_query = re.sub(r"\s+(?:di\s+(?:pc|laptop|komputer|browser|chrome|brave|yt|youtube)|pc|laptop|komputer|browser|chrome|brave|yt|youtube|gw|gua|gue|dong|nih|ya|ku|bro|bang)$", "", clean_query, flags=re.IGNORECASE).strip()
                if not clean_query:
                    clean_query = "trending youtube indonesia"

                logger.info("PC_ACTION: Detected YouTube intent for query '%s'", clean_query)
                video_url, video_title = search_youtube_video(clean_query)

                payload = {
                    "url": video_url,
                    "title": video_title,
                    "query": clean_query,
                    "browser": "brave"
                }
                action_id = enqueue_pc_action("open_url", payload, chat_id=chat_id)

                return (
                    f"Siap bro! Video <b>{html.escape(video_title)}</b> lagi gue bukain di browser PC lo sekarang. 🚀\n\n"
                    f"🔗 <a href=\"{html.escape(video_url)}\">{html.escape(video_url)}</a>"
                )

        # 4. Generic URL Open
        for p in cls.PATTERNS_GENERIC_URL:
            m = p.search(t)
            if m:
                target_url = m.group(1).strip()
                # Ensure valid schema
                if not target_url.startswith("http://") and not target_url.startswith("https://"):
                    target_url = "https://" + target_url

                logger.info("PC_ACTION: Detected generic URL open intent for '%s'", target_url)
                payload = {
                    "url": target_url,
                    "title": target_url,
                    "browser": "chrome"
                }
                action_id = enqueue_pc_action("open_url", payload, chat_id=chat_id)

                return (
                    f"Siap bro! Link <b>{html.escape(target_url)}</b> lagi gue luncurkan di browser PC lo sekarang. 🌐"
                )

        return None
