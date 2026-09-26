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
from datetime import datetime
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
