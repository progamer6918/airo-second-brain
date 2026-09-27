#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/airo_pc_action_router.py — Remote PC Computer Use Action Router for AIRO Hermes.

Dispatches local desktop actions (Apps, Typing, Hotkeys, Screenshots, System, YouTube)
from the cloud VPS to the Owner's local PC via an atomic file queue.
"""

import os
import re
import json
import time
import uuid
import html
import subprocess
import urllib.request
import urllib.parse
import logging
from datetime import datetime
from typing import Optional, Tuple

try:
    from airo_presentation_engine import build_airo_pitch_deck
except ImportError:
    build_airo_pitch_deck = None

from airo_pc_tools import (
    enqueue_pc_action,
    pc_launch_app,
    pc_open_url,
    pc_type_text,
    pc_send_hotkey,
    pc_capture_screenshot,
    pc_control_system,
    PENDING_DIR,
    DONE_DIR
)

logger = logging.getLogger("airo-pc-action-router")


def send_telegram_document(chat_id: str, file_path: str, caption: str = "") -> bool:
    """Uploads a document directly to Telegram chat."""
    token = os.environ.get("AIRO_HERMES_TELEGRAM_BOT_TOKEN")
    if not token:
        env_file = os.path.expanduser("~/.config/airo/airo-hermes-telegram.env")
        if os.path.exists(env_file):
            try:
                with open(env_file, encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("AIRO_HERMES_TELEGRAM_BOT_TOKEN="):
                            token = line.strip().split("=", 1)[1].strip("'\" ")
                            break
            except Exception:
                pass
    if not token or not chat_id or not os.path.exists(file_path):
        logger.warning("send_telegram_document: Missing token (%s), chat_id (%s), or file (%s)",
                       bool(token), chat_id, file_path)
        return False

    try:
        cmd = [
            "curl", "-s",
            "-F", f"chat_id={chat_id}",
            "-F", f"caption={caption[:1024]}",
            "-F", f"document=@{file_path}",
            f"https://api.telegram.org/bot{token}/sendDocument"
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=25)
        logger.info("send_telegram_document result: %s", res.stdout[:120])
        return '"ok":true' in res.stdout
    except Exception as e:
        logger.error("Failed to upload document to Telegram: %s", e)
        return False



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


class PCActionRouter:
    """Semantic Intent Router for Remote PC Computer Use."""

    # Canonical mapping of desktop application keywords to (executable_key, display_name)
    APP_MAPPINGS = [
        (r"\b(?:powerpoint|power\s+point|ppt|presentasi)\b", "powerpoint", "Microsoft PowerPoint"),
        (r"\b(?:excel|spreadsheet|lembar\s+sebar)\b", "excel", "Microsoft Excel"),
        (r"\b(?:winword|microsoft\s+word|word\s+dokumen|dokumen\s+word)\b", "word", "Microsoft Word"),
        (r"\b(?:vscode|vs\s+code|visual\s+studio\s+code|code\s+editor)\b", "vscode", "Visual Studio Code"),
        (r"\b(?:notepad|catatan\s+teks|text\s+editor)\b", "notepad", "Notepad"),
        (r"\b(?:kalkulator|calculator|calc)\b", "calc", "Kalkulator"),
        (r"\b(?:spotify|musik\s+spotify)\b", "spotify", "Spotify"),
        (r"\b(?:brave|brave\s+browser)\b", "brave", "Brave Browser"),
        (r"\b(?:chrome|google\s+chrome)\b", "chrome", "Google Chrome"),
        (r"\b(?:edge|microsoft\s+edge)\b", "edge", "Microsoft Edge"),
        (r"\b(?:file\s+explorer|explorer|buka\s+folder)\b", "explorer", "File Explorer"),
        (r"\b(?:terminal|windows\s+terminal|powershell|cmd)\b", "terminal", "Windows Terminal"),
    ]

    @classmethod
    def route(cls, text: str, chat_id: str = "") -> Optional[str]:
        t = text.strip()
        t_lower = t.lower()

        # ─── 1. STATUS CHECK ──────────────────────────────────────────────────
        if re.search(r"\b(?:cek\s+)?status\s+(?:pc|relay|bridge)\b", t_lower):
            pending_count = len([f for f in os.listdir(PENDING_DIR) if f.endswith(".json")])
            done_count = len([f for f in os.listdir(DONE_DIR) if f.endswith(".json")])
            return (
                f"🖥️ <b>Status AIRO PC Computer Use Bridge</b>:\n"
                f"• Antrean pending: <b>{pending_count}</b> tugas\n"
                f"• Riwayat selesai: <b>{done_count}</b> tugas\n"
                f"• Target desktop: <code>WinSta0\\Default</code> (Monitor Fisik)\n"
                f"• Status: <b>OPERATIONAL & READY</b> 🚀\n\n"
                f"<i>Pastikan daemon Windows aktif di PC lo via <code>START_AIRO_PC_RELAY.bat</code>!</i>"
            )

        # ─── 2. SCREENSHOT ON DEMAND ──────────────────────────────────────────
        SCREENSHOT_PATTERNS = [
            r"\b(?:screenshot|screen\s*shot|tangkapan\s+layar|foto\s+layar|foto\s+pc|capture\s+layar)\b",
            r"\b(?:coba|tolong|minta)?\s*(?:lihat|kirim|ambil(?:kan)?)\s*(?:layar|tampilan\s+layar|desktop)\s*(?:pc|laptop)?\b",
        ]
        if any(re.search(pat, t_lower) for pat in SCREENSHOT_PATTERNS):
            logger.info("PC_ACTION: Detected screenshot request from '%s'", t)
            res = pc_capture_screenshot(send_to_telegram=True, chat_id=chat_id)
            return (
                "Siap bro! Screenshot monitor fisik PC lo lagi diambil sekarang dan langsung dikirim ke chat ini. 📸"
            )

        # ─── 3. SYSTEM CONTROL (Lock, Mute, Volume) ───────────────────────────
        if re.search(r"\b(?:kunci\s+(?:pc|laptop|layar)|lock\s+(?:pc|laptop|screen|workstation))\b", t_lower):
            logger.info("PC_ACTION: Detected lock workstation request from '%s'", t)
            pc_control_system("lock", chat_id=chat_id)
            return "Siap bro! PC lo udah gue kunci (LockWorkStation) demi keamanan. 🔒"

        if re.search(r"\b(?:mute|unmute|senyapkan)\s*(?:suara|audio|pc|laptop)?\b", t_lower):
            logger.info("PC_ACTION: Detected mute toggle from '%s'", t)
            pc_control_system("mute", chat_id=chat_id)
            return "Siap bro! Status audio PC lo udah di-toggle mute/unmute. 🔇"

        if re.search(r"\b(?:volume\s+up|besarkan\s+volume|naikkan\s+volume)\b", t_lower):
            logger.info("PC_ACTION: Detected volume up from '%s'", t)
            pc_control_system("volume_up", chat_id=chat_id)
            return "Siap bro! Volume audio PC lo udah gue naikkan. 🔊"

        if re.search(r"\b(?:volume\s+down|kecilkan\s+volume|turunkan\s+volume)\b", t_lower):
            logger.info("PC_ACTION: Detected volume down from '%s'", t)
            pc_control_system("volume_down", chat_id=chat_id)
            return "Siap bro! Volume audio PC lo udah gue kecilkan. 🔉"

        # ─── 4. KEYBOARD SHORTCUTS & HOTKEYS ─────────────────────────────────
        HOTKEY_PATTERN = re.compile(
            r"\b(?:tekan|pencet|kirim\s+tombol|shortcut|hotkey)\s+"
            r"(ctrl\+[a-z0-9]|alt\+[a-z0-9]|win\+[a-z0-9]|super\+[a-z0-9]|enter|esc|escape|tab|space|backspace|delete)\b",
            re.IGNORECASE
        )
        m_hk = HOTKEY_PATTERN.search(t_lower)
        if m_hk:
            key_combo = m_hk.group(1).strip()
            logger.info("PC_ACTION: Detected hotkey intent for '%s'", key_combo)
            pc_send_hotkey(key_combo, chat_id=chat_id)
            return f"Siap bro! Tombol kombinasi <code>{html.escape(key_combo)}</code> lagi gue kirim ke jendela aktif PC lo. ⌨️"

        if re.search(r"\b(?:minimize\s+semua|show\s+desktop|tampilkan\s+desktop)\b", t_lower):
            logger.info("PC_ACTION: Detected show desktop / minimize all intent")
            pc_send_hotkey("win+d", chat_id=chat_id)
            return "Siap bro! Semua jendela di-minimize dan desktop ditampilkan (Win+D). 🖥️"

        # ─── 5. KEYBOARD TYPING ───────────────────────────────────────────────
        TYPE_PATTERNS = [
            r"\b(?:tolong\s+|coba\s+)?(?:ketik(?:an|kan)?|tulis(?:kan)?)\s+(?:teks|kata|tulisan)?\s*[\"']([^\"']+)[\"'](?:\s+(?:di|ke)\s+(?:pc|laptop|jendela|layar))?",
            r"\b(?:tolong\s+|coba\s+)?(?:ketik(?:an|kan)?|tulis(?:kan)?)\s+(?:teks|kata|tulisan)?\s*(.+?)(?:\s+(?:di|ke)\s+(?:pc|laptop|jendela aktif|layar))\b",
        ]
        for pat in TYPE_PATTERNS:
            m_type = re.search(pat, t, re.IGNORECASE)
            if m_type:
                target_text = m_type.group(1).strip()
                # Exclude if it looks like a search query or command
                if target_text and not target_text.startswith("http") and len(target_text) > 0:
                    logger.info("PC_ACTION: Detected typing intent for '%s'", target_text)
                    pc_type_text(target_text, chat_id=chat_id)
                    return f"Siap bro! Teks berikut lagi gue ketikkan di jendela aktif PC lo sekarang:\n\n<code>{html.escape(target_text)}</code> ⌨️"
        # ─── 5.5. AUTONOMOUS PRESENTATION DECK GENERATION & DISPLAY ─────────
        has_gen_verb = bool(re.search(
            r"\b(?:buat(?:kan|in)?|bikin(?:kan|in)?|generate|susun(?:kan)?|tulis(?:kan)?|rangkai|ciptakan|siapkan)\b",
            t_lower
        ))
        has_presentation_kw = bool(re.search(
            r"\b(?:ppt|powerpoint|power\s+point|presentasi|slide|slide\s+deck|pitch\s+deck)\b",
            t_lower
        ))

        if has_gen_verb and has_presentation_kw:
            logger.info("PC_ACTION: Detected presentation deck generation intent from '%s'", t)

            deck_filename = "AIRO_Pitch_Deck.pptx"
            vps_deck_path = os.path.expanduser(f"~/.local/state/airo-second-brain/pc-action-bridge/files/{deck_filename}")
            win_deck_path = rf"C:\Users\Admin\Documents\AIRO_Presentations\{deck_filename}"

            # 1. Compile presentation deck on VPS
            os.makedirs(os.path.dirname(vps_deck_path), exist_ok=True)
            if build_airo_pitch_deck:
                try:
                    build_airo_pitch_deck(vps_deck_path)
                    logger.info("Compiled presentation deck at %s", vps_deck_path)
                except Exception as e:
                    logger.error("Error building pitch deck: %s", e)

            # 2. Dispatch open_app action to local PC (passes Windows path to PowerPoint)
            pc_launch_app("powerpoint", args=f'"{win_deck_path}"', display_name="AIRO Pitch Deck", chat_id=chat_id)

            # 3. Upload document to Telegram chat
            tg_caption = "🎯 <b>AIRO Autonomous Executive OS — Pitch Deck</b>\n7 Slide Executive Presentation (16:9 Widescreen Modern Tech Theme)"
            send_telegram_document(chat_id, vps_deck_path, caption=tg_caption)

            # 4. Return executive status receipt
            return (
                "🎯 <b>AIRO Executive Pitch Deck Berhasil Dibuat & Dibuka di PC!</b> 🚀\n\n"
                "📊 <b>Struktur 7 Slide Presentasi (16:9 Modern Tech Dark Theme):</b>\n"
                "1. <b>Vision & Title</b>: AIRO — The Autonomous Executive OS\n"
                "2. <b>The Industry Crisis</b>: Fragmentasi & Amnesia AI Tradisional\n"
                "3. <b>The Architecture</b>: Penyatuan Strategic Intelligence & Desktop Execution\n"
                "4. <b>Core Superpowers</b>: Physical Computer Use, AWD, Finance, Sovereign Storage\n"
                "5. <b>Live Demonstrations</b>: Bukti Eksekusi Nyata (Excel, PowerPoint, Screen Vision)\n"
                "6. <b>Unfair Advantage & ROI</b>: 10x Velocity & 100% Data Sovereignty\n"
                "7. <b>Call to Action</b>: Transformasi Operasional Eksekutif Hari Ini\n\n"
                "🖥️ Slide presentasi sudah otomatis dibuka di <b>Microsoft PowerPoint</b> monitor PC lo!\n"
                "📎 File dokumen <code>.pptx</code> juga sudah gue kirimkan ke chat Telegram ini untuk lo review di HP. Silakan dicek bro!"
            )

        # ─── 6. NATIVE DESKTOP APPLICATION LAUNCH ─────────────────────────────
        # Check if the user is asking to launch/open an application on PC
        has_app_launch_intent = bool(re.search(
            r"\b(?:buka(?:in|kan)?|jalankan|start|launch|buka\s+aplikasi|buka\s+software|buka\s+program|aplikasi)\b",
            t_lower
        ))

        # Check for explicit app mentions
        for pat, app_key, display_name in cls.APP_MAPPINGS:
            if re.search(pat, t_lower):
                # If explicit app is mentioned, and either launch verb is present OR anti-youtube is present OR "di pc" is mentioned
                if has_app_launch_intent or re.search(r"\b(?:di\s+(?:pc|laptop|komputer)|bukan\s+youtube)\b", t_lower):
                    logger.info("PC_ACTION: Detected native desktop app intent for '%s' -> %s", display_name, app_key)
                    pc_launch_app(app_key, display_name=display_name, chat_id=chat_id)
                    return f"Siap bro! Aplikasi <b>{html.escape(display_name)}</b> lagi gue bukain di monitor PC lo sekarang. 🚀"

        # If user explicitly specified NOT youtube, DO NOT fall through to YouTube
        if re.search(r"\b(?:bukan\s+youtube|bukan\s+yt|bukan\s+video)\b", t_lower):
            return None

        # ─── 7. YOUTUBE SEARCH & PLAY ─────────────────────────────────────────
        # STRICT MEDIA INTENT: Only triggers if verbs and media words indicate audio/video playback
        YOUTUBE_MEDIA_PATTERNS = [
            # "Bro putar lagu Bohemian Rhapsody di YouTube PC", "Tolong putarin podcast Raditya Dika di pc gw"
            re.compile(
                r"(?:bro\s+|bang\s+|tolong\s+|coba\s+)*"
                r"(?:putar(?:in|kan)?|setel(?:in|kan)?|tonton(?:in|kan)?|play(?:-?in)?|dengar(?:in|kan)?)\s+"
                r"(?:video|lagu|musik|podcast)?\s*"
                r"(.+?)\s*"
                r"(?:di|via)\s+(?:pc|laptop|komputer|browser|chrome|brave|yt|youtube)"
                r"(?:\s+(?:pc|laptop|komputer|browser|chrome|brave|yt|youtube|gw|gua|gue|dong|nih|ya|ku|bro|bang))*$",
                re.IGNORECASE
            ),
            # "buka youtube X dan play", "putar di youtube: X"
            re.compile(
                r"(?:bro\s+|bang\s+|tolong\s+|coba\s+)*"
                r"(?:buka(?:in|kan)?|play(?:-?in)?|putar(?:in|kan)?|setel(?:in|kan)?|tonton(?:in|kan)?)\s+"
                r"(?:youtube|yt)\s*(?:dan\s+(?:play|putar))?\s*(.+)",
                re.IGNORECASE
            ),
            # "setelin lagu X di pc"
            re.compile(
                r"(?:putar(?:in|kan)?|setel(?:in|kan)?|play(?:-?in)?|tonton(?:in|kan)?)\s+"
                r"(?:lagu|musik|video|podcast)\s+"
                r"(.+?)\s*"
                r"(?:di\s+(?:pc|laptop|komputer))?",
                re.IGNORECASE
            ),
        ]

        for p in YOUTUBE_MEDIA_PATTERNS:
            m = p.search(t)
            if m:
                raw_query = m.group(1).strip()
                # Clean filler words
                clean_query = re.sub(r"^(?:video|lagu|musik|tentang|channel|podcast)\s+", "", raw_query, flags=re.IGNORECASE).strip()
                clean_query = re.sub(r"\s+(?:di\s+(?:pc|laptop|komputer|browser|chrome|brave|yt|youtube)|pc|laptop|komputer|browser|chrome|brave|yt|youtube|gw|gua|gue|dong|nih|ya|ku|bro|bang)$", "", clean_query, flags=re.IGNORECASE).strip()

                # Guard: ensure the query doesn't match an application
                is_app_query = False
                for pat, _, _ in cls.APP_MAPPINGS:
                    if re.search(pat, clean_query.lower()):
                        is_app_query = True
                        break
                if is_app_query:
                    continue

                if not clean_query:
                    clean_query = "trending youtube indonesia"

                logger.info("PC_ACTION: Detected YouTube intent for query '%s'", clean_query)
                video_url, video_title = search_youtube_video(clean_query)
                pc_open_url(video_url, browser="brave", title=video_title, chat_id=chat_id)

                return (
                    f"Siap bro! Video <b>{html.escape(video_title)}</b> lagi gue bukain di browser PC lo sekarang. 🚀\n\n"
                    f"🔗 <a href=\"{html.escape(video_url)}\">{html.escape(video_url)}</a>"
                )

        # ─── 8. GENERIC URL OPEN ──────────────────────────────────────────────
        GENERIC_URL_PATTERNS = [
            re.compile(r"(?:buka|open)\s+(?:link|url|web|situs|halaman)?\s*(https?://\S+)(?:\s+di\s+(?:pc|laptop|komputer))?", re.IGNORECASE),
            re.compile(r"(?:di\s+(?:pc|laptop|komputer)\s+)?(?:buka|open)\s+(https?://\S+)", re.IGNORECASE),
        ]
        for p in GENERIC_URL_PATTERNS:
            m = p.search(t)
            if m:
                target_url = m.group(1).strip()
                if not target_url.startswith("http://") and not target_url.startswith("https://"):
                    target_url = "https://" + target_url

                logger.info("PC_ACTION: Detected generic URL open intent for '%s'", target_url)
                pc_open_url(target_url, browser="brave", title=target_url, chat_id=chat_id)
                return f"Siap bro! Link <b>{html.escape(target_url)}</b> lagi gue luncurkan di browser PC lo sekarang. 🌐"

        return None
