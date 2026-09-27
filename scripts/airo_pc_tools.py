#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/airo_pc_tools.py — PC Computer Use & Desktop Control Tools for AIRO Hermes.

Provides atomic queue-based tool execution for Hermes on Tencent Cloud VPS
targeting the Owner's local Windows 11 PC.
"""

import os
import json
import time
import uuid
import logging
from datetime import datetime, timezone
from typing import Optional, Dict, Any

logger = logging.getLogger("airo-pc-tools")

QUEUE_BASE_DIR = os.path.expanduser("~/.local/state/airo-second-brain/pc-action-bridge/queue")
PENDING_DIR = os.path.join(QUEUE_BASE_DIR, "pending")
IN_PROGRESS_DIR = os.path.join(QUEUE_BASE_DIR, "in_progress")
DONE_DIR = os.path.join(QUEUE_BASE_DIR, "done")
DEAD_DIR = os.path.join(QUEUE_BASE_DIR, "dead")

for d in (PENDING_DIR, IN_PROGRESS_DIR, DONE_DIR, DEAD_DIR):
    os.makedirs(d, exist_ok=True)


def enqueue_pc_action(action_type: str, payload: dict, chat_id: str = "") -> str:
    """Writes an atomic action packet to the pending queue."""
    now_ts = int(time.time())
    now_utc = datetime.now(timezone.utc)
    action_id = f"act-{now_ts}-{uuid.uuid4().hex[:6]}"
    packet = {
        "action_id": action_id,
        "type": action_type,
        "payload": payload,
        "chat_id": str(chat_id),
        "created_at": now_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "created_at_epoch": now_ts,
        "status": "pending"
    }

    tmp_file = os.path.join(PENDING_DIR, f"{action_id}.tmp")
    final_file = os.path.join(PENDING_DIR, f"{action_id}.json")

    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(packet, f, indent=2, ensure_ascii=False)
    os.replace(tmp_file, final_file)
    logger.info("Enqueued PC action %s (type=%s)", action_id, action_type)
    return action_id


def pc_launch_app(app: str, args: str = "", display_name: str = "", chat_id: str = "") -> Dict[str, Any]:
    """
    Launch a native Windows desktop application on Owner's PC.
    Supported apps: powerpoint, excel, word, vscode, notepad, calc, spotify, brave, chrome, edge, explorer, terminal.
    """
    payload = {
        "app": app.lower().strip(),
        "display_name": display_name or app,
        "args": args
    }
    action_id = enqueue_pc_action("open_app", payload, chat_id=chat_id)
    return {
        "status": "ENQUEUED",
        "action_id": action_id,
        "action": "open_app",
        "app": app,
        "display_name": display_name or app
    }


def pc_open_url(url: str, browser: str = "brave", title: str = "", chat_id: str = "") -> Dict[str, Any]:
    """Open a URL or media stream in a web browser on Owner's PC."""
    payload = {
        "url": url,
        "browser": browser,
        "title": title or url
    }
    action_id = enqueue_pc_action("open_url", payload, chat_id=chat_id)
    return {
        "status": "ENQUEUED",
        "action_id": action_id,
        "action": "open_url",
        "url": url,
        "browser": browser,
        "title": title or url
    }


def pc_type_text(text: str, chat_id: str = "") -> Dict[str, Any]:
    """Type text into the currently active window on Owner's PC."""
    payload = {"text": text}
    action_id = enqueue_pc_action("type_text", payload, chat_id=chat_id)
    return {
        "status": "ENQUEUED",
        "action_id": action_id,
        "action": "type_text",
        "characters_count": len(text)
    }


def pc_send_hotkey(keys: str, chat_id: str = "") -> Dict[str, Any]:
    """
    Send keyboard shortcuts to the active window on Owner's PC.
    Examples: 'ctrl+s', 'alt+f4', 'enter', 'esc', 'win+d', 'tab'.
    """
    payload = {"keys": keys.lower().strip()}
    action_id = enqueue_pc_action("send_hotkey", payload, chat_id=chat_id)
    return {
        "status": "ENQUEUED",
        "action_id": action_id,
        "action": "send_hotkey",
        "keys": keys
    }


def pc_click_mouse(x: Optional[int] = None, y: Optional[int] = None, button: str = "left", double_click: bool = False, chat_id: str = "") -> Dict[str, Any]:
    """Simulate a mouse click at coordinates (x, y) or at the current cursor location."""
    payload = {
        "x": x,
        "y": y,
        "button": button,
        "double_click": double_click
    }
    action_id = enqueue_pc_action("mouse_click", payload, chat_id=chat_id)
    return {
        "status": "ENQUEUED",
        "action_id": action_id,
        "action": "mouse_click",
        "button": button,
        "coords": [x, y] if x is not None and y is not None else "current"
    }


def pc_capture_screenshot(send_to_telegram: bool = True, chat_id: str = "") -> Dict[str, Any]:
    """
    Capture full desktop screenshot on Owner's PC and upload it directly to Telegram chat.
    """
    payload = {
        "send_to_telegram": send_to_telegram,
        "chat_id": str(chat_id)
    }
    action_id = enqueue_pc_action("capture_screenshot", payload, chat_id=chat_id)
    return {
        "status": "ENQUEUED",
        "action_id": action_id,
        "action": "capture_screenshot",
        "send_to_telegram": send_to_telegram
    }


def pc_control_system(command: str, chat_id: str = "") -> Dict[str, Any]:
    """
    Execute system OS operations on Owner's PC: 'lock', 'mute', 'volume_up', 'volume_down'.
    """
    payload = {"command": command.lower().strip()}
    action_id = enqueue_pc_action("system_control", payload, chat_id=chat_id)
    return {
        "status": "ENQUEUED",
        "action_id": action_id,
        "action": "system_control",
        "command": command
    }


def pc_live_ppt_build(slides: list, title: str = "", subtitle: str = "", category: str = "Executive Brief", chat_id: str = "") -> Dict[str, Any]:
    """
    Build a PowerPoint presentation LIVE on the Owner's physical monitor via COM Automation.
    PowerPoint will open and type out the slides in real time.
    Also compiles presentation on VPS and delivers document to Telegram when chat_id is provided.
    """
    payload = {
        "title": title or "Live Presentation",
        "slides": slides
    }
    action_id = enqueue_pc_action("live_ppt_build", payload, chat_id=chat_id)

    filename = ""
    if chat_id:
        try:
            try:
                from airo_presentation_engine import build_dynamic_deck
            except ImportError:
                from scripts.airo_presentation_engine import build_dynamic_deck

            safe_name = "".join(c if c.isalnum() else "_" for c in (title or "Presentation").strip()[:30]).strip("_") or "Presentation"
            filename = f"{safe_name}.pptx"
            vps_deck_path = os.path.expanduser(f"~/.local/state/airo-second-brain/pc-action-bridge/files/{filename}")
            os.makedirs(os.path.dirname(vps_deck_path), exist_ok=True)
            deck_title = title or "AIRO Live Presentation"
            build_dynamic_deck(vps_deck_path, title=deck_title, slides=slides, subtitle=subtitle, category=category)
            tg_caption = f"🎯 <b>{deck_title}</b>\n{len(slides)} Slide Executive Presentation (16:9 Modern Dark Tech Theme)"
            send_telegram_document(chat_id, vps_deck_path, caption=tg_caption)
        except Exception as e:
            logger.error("Failed to generate and deliver live pptx to Telegram: %s", e)

    return {
        "status": "ENQUEUED",
        "action_id": action_id,
        "action": "live_ppt_build",
        "slides_count": len(slides),
        "filename": filename
    }


def send_telegram_document(chat_id: str, file_path: str, caption: str = "") -> bool:
    """Uploads a document directly to Telegram chat."""
    import subprocess
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


def pc_generate_dynamic_pptx(topic: str, slides: list, chat_id: str = "", title: str = "", subtitle: str = "", category: str = "Executive Brief") -> Dict[str, Any]:
    """
    Compile a presentation dynamically on VPS using PresentationEngine,
    sync it to Windows PC, launch it in PowerPoint, and send the document to Telegram.
    """
    try:
        from airo_presentation_engine import build_dynamic_deck
    except ImportError:
        from scripts.airo_presentation_engine import build_dynamic_deck

    safe_name = "".join(c if c.isalnum() else "_" for c in topic.strip()[:30]).strip("_")
    if not safe_name:
        safe_name = "Presentation"
    filename = f"{safe_name}.pptx"

    vps_deck_path = os.path.expanduser(f"~/.local/state/airo-second-brain/pc-action-bridge/files/{filename}")
    win_deck_path = rf"C:\Users\Admin\Documents\AIRO_Presentations\{filename}"
    os.makedirs(os.path.dirname(vps_deck_path), exist_ok=True)

    deck_title = title or topic.title()
    build_dynamic_deck(vps_deck_path, title=deck_title, slides=slides, subtitle=subtitle, category=category)
    logger.info("Compiled dynamic presentation at %s", vps_deck_path)

    # 1. Launch in PowerPoint on Windows
    pc_launch_app("powerpoint", args=f'"{win_deck_path}"', display_name=deck_title, chat_id=chat_id)

    # 2. Send file directly to Telegram chat
    if chat_id:
        tg_caption = f"🎯 <b>{deck_title}</b>\n{len(slides)} Slide Executive Presentation (16:9 Widescreen Modern Tech Theme)"
        send_telegram_document(chat_id, vps_deck_path, caption=tg_caption)

    return {
        "status": "GENERATED_AND_LAUNCHED",
        "topic": topic,
        "title": deck_title,
        "vps_path": vps_deck_path,
        "win_path": win_deck_path,
        "filename": filename,
        "slides_count": len(slides)
    }


def pc_live_excel_build(headers: list, rows: list, title: str = "", sheet_name: str = "Executive Summary", summary: dict = None, chat_id: str = "") -> Dict[str, Any]:
    """
    Build a spreadsheet LIVE on the Owner's physical monitor via Excel COM Automation.
    Excel will open, maximize, and construct the styled table with visual pacing in real time.
    Also compiles spreadsheet on VPS and delivers document to Telegram when chat_id is provided.
    """
    payload = {
        "title": title or "AIRO Live Spreadsheet",
        "sheet_name": sheet_name or "Executive Summary",
        "headers": headers,
        "rows": rows
    }
    action_id = enqueue_pc_action("live_excel_build", payload, chat_id=chat_id)

    filename = ""
    if chat_id:
        try:
            try:
                from airo_office_engine import build_dynamic_xlsx
            except ImportError:
                from scripts.airo_office_engine import build_dynamic_xlsx

            safe_name = "".join(c if c.isalnum() else "_" for c in (title or "Spreadsheet").strip()[:30]).strip("_") or "Spreadsheet"
            filename = f"{safe_name}.xlsx"
            vps_file_path = os.path.expanduser(f"~/.local/state/airo-second-brain/pc-action-bridge/files/{filename}")
            os.makedirs(os.path.dirname(vps_file_path), exist_ok=True)
            build_dynamic_xlsx(vps_file_path, title=title or "AIRO Live Spreadsheet", headers=headers, rows=rows, sheet_name=sheet_name, summary=summary)
            tg_caption = f"📊 <b>{title or 'AIRO Live Spreadsheet'}</b>\nExecutive Excel Workbook ({len(rows)} baris data, executive styling)"
            send_telegram_document(chat_id, vps_file_path, caption=tg_caption)
        except Exception as e:
            logger.error("Failed to generate and deliver live xlsx to Telegram: %s", e)

    return {
        "status": "ENQUEUED",
        "action_id": action_id,
        "action": "live_excel_build",
        "headers_count": len(headers),
        "rows_count": len(rows),
        "filename": filename
    }


def pc_live_word_build(sections: list, title: str = "", subtitle: str = "", chat_id: str = "") -> Dict[str, Any]:
    """
    Build a Word document LIVE on the Owner's physical monitor via Word COM Automation.
    Word will open and type out styled headings, paragraphs, and points in real time.
    Also compiles document on VPS and delivers document to Telegram when chat_id is provided.
    """
    payload = {
        "title": title or "Dokumen Eksekutif AIRO",
        "subtitle": subtitle or "",
        "sections": sections
    }
    action_id = enqueue_pc_action("live_word_build", payload, chat_id=chat_id)

    filename = ""
    if chat_id:
        try:
            try:
                from airo_office_engine import build_dynamic_docx
            except ImportError:
                from scripts.airo_office_engine import build_dynamic_docx

            safe_name = "".join(c if c.isalnum() else "_" for c in (title or "Dokumen").strip()[:30]).strip("_") or "Document"
            filename = f"{safe_name}.docx"
            vps_file_path = os.path.expanduser(f"~/.local/state/airo-second-brain/pc-action-bridge/files/{filename}")
            os.makedirs(os.path.dirname(vps_file_path), exist_ok=True)
            build_dynamic_docx(vps_file_path, title=title or "Dokumen Eksekutif AIRO", sections=sections, subtitle=subtitle)
            tg_caption = f"📄 <b>{title or 'Dokumen Eksekutif AIRO'}</b>\nExecutive Word Document ({len(sections)} bagian analisis, executive styling)"
            send_telegram_document(chat_id, vps_file_path, caption=tg_caption)
        except Exception as e:
            logger.error("Failed to generate and deliver live docx to Telegram: %s", e)

    return {
        "status": "ENQUEUED",
        "action_id": action_id,
        "action": "live_word_build",
        "sections_count": len(sections),
        "filename": filename
    }


def pc_generate_dynamic_xlsx(topic: str, headers: list, rows: list, title: str = "", sheet_name: str = "Executive Summary", summary: dict = None, chat_id: str = "") -> Dict[str, Any]:
    """
    Compile a styled spreadsheet dynamically on VPS using openpyxl,
    sync it to Windows PC, launch it in Excel, and send the document to Telegram.
    """
    try:
        from airo_office_engine import build_dynamic_xlsx
    except ImportError:
        from scripts.airo_office_engine import build_dynamic_xlsx

    safe_name = "".join(c if c.isalnum() else "_" for c in topic.strip()[:30]).strip("_")
    if not safe_name:
        safe_name = "Spreadsheet"
    filename = f"{safe_name}.xlsx"

    vps_file_path = os.path.expanduser(f"~/.local/state/airo-second-brain/pc-action-bridge/files/{filename}")
    win_file_path = rf"C:\Users\Admin\Documents\AIRO_Spreadsheets\{filename}"
    os.makedirs(os.path.dirname(vps_file_path), exist_ok=True)

    wb_title = title or topic.title()
    build_dynamic_xlsx(vps_file_path, title=wb_title, headers=headers, rows=rows, sheet_name=sheet_name, summary=summary)
    logger.info("Compiled dynamic spreadsheet at %s", vps_file_path)

    # 1. Launch in Excel on Windows
    pc_launch_app("excel", args=f'"{win_file_path}"', display_name=wb_title, chat_id=chat_id)

    # 2. Send file directly to Telegram chat
    if chat_id:
        tg_caption = f"📊 <b>{wb_title}</b>\nExecutive Excel Workbook ({len(rows)} baris data, auto-fit styling)"
        send_telegram_document(chat_id, vps_file_path, caption=tg_caption)

    return {
        "status": "GENERATED_AND_LAUNCHED",
        "topic": topic,
        "title": wb_title,
        "vps_path": vps_file_path,
        "win_path": win_file_path,
        "filename": filename,
        "rows_count": len(rows)
    }


def pc_generate_dynamic_docx(topic: str, sections: list, title: str = "", subtitle: str = "", chat_id: str = "") -> Dict[str, Any]:
    """
    Compile an executive Word document dynamically on VPS using python-docx,
    sync it to Windows PC, launch it in Word, and send the document to Telegram.
    """
    try:
        from airo_office_engine import build_dynamic_docx
    except ImportError:
        from scripts.airo_office_engine import build_dynamic_docx

    safe_name = "".join(c if c.isalnum() else "_" for c in topic.strip()[:30]).strip("_")
    if not safe_name:
        safe_name = "Document"
    filename = f"{safe_name}.docx"

    vps_file_path = os.path.expanduser(f"~/.local/state/airo-second-brain/pc-action-bridge/files/{filename}")
    win_file_path = rf"C:\Users\Admin\Documents\AIRO_Documents\{filename}"
    os.makedirs(os.path.dirname(vps_file_path), exist_ok=True)

    doc_title = title or topic.title()
    build_dynamic_docx(vps_file_path, title=doc_title, sections=sections, subtitle=subtitle)
    logger.info("Compiled dynamic Word document at %s", vps_file_path)

    # 1. Launch in Word on Windows
    pc_launch_app("winword", args=f'"{win_file_path}"', display_name=doc_title, chat_id=chat_id)

    # 2. Send file directly to Telegram chat
    if chat_id:
        tg_caption = f"📄 <b>{doc_title}</b>\nExecutive Word Document ({len(sections)} bagian analisis, styled layout)"
        send_telegram_document(chat_id, vps_file_path, caption=tg_caption)

    return {
        "status": "GENERATED_AND_LAUNCHED",
        "topic": topic,
        "title": doc_title,
        "vps_path": vps_file_path,
        "win_path": win_file_path,
        "filename": filename,
        "sections_count": len(sections)
    }



