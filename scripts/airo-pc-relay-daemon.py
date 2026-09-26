#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/airo-pc-relay-daemon.py — Local PC Relay Daemon for AIRO Hermes.

Polls the VPS action queue via multiplexed SSH and executes desktop actions
(e.g., launching Chrome with YouTube videos) directly on the local Windows PC.
"""

import os
import sys
import time
import json
import signal
import logging
import subprocess
from datetime import datetime
from typing import Tuple, Optional, Dict, Any

VPS_HOST = os.environ.get("AIRO_VPS_HOST", "43.157.241.228")
VPS_USER = os.environ.get("AIRO_VPS_USER", "ubuntu")
SSH_KEY = os.path.expanduser(os.environ.get("AIRO_SSH_KEY", "~/.ssh/airo_tencent_vps.pem"))

STATE_DIR = os.path.expanduser("~/.local/state/airo-second-brain/pc-action-bridge")
LOG_FILE = os.path.join(STATE_DIR, "daemon.log")
PID_FILE = os.path.join(STATE_DIR, "daemon.pid")
MUX_SOCKET = f"/tmp/airo_ssh_mux_pc_relay_{os.getuid()}"

POLL_INTERVAL = 2.0  # seconds
BRAVE_PATH = "/mnt/c/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
CHROME_PATH = "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"
EDGE_PATH = "/mnt/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"

os.makedirs(STATE_DIR, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("airo-pc-relay")


def log(msg: str):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}", flush=True)
    logger.info(msg)


def ensure_ssh_mux() -> bool:
    """Ensures persistent SSH multiplexed master connection is active."""
    check_cmd = [
        "ssh", "-O", "check",
        "-o", f"ControlPath={MUX_SOCKET}",
        f"{VPS_USER}@{VPS_HOST}"
    ]
    res = subprocess.run(check_cmd, capture_output=True, text=True)
    if res.returncode == 0:
        return True

    # Start master connection in background
    start_cmd = [
        "ssh", "-i", SSH_KEY,
        "-o", "ControlMaster=yes",
        "-o", f"ControlPath={MUX_SOCKET}",
        "-o", "ControlPersist=600s",
        "-o", "StrictHostKeyChecking=no",
        "-o", "ConnectTimeout=8",
        "-N", "-f",
        f"{VPS_USER}@{VPS_HOST}"
    ]
    start_res = subprocess.run(start_cmd, capture_output=True, text=True)
    if start_res.returncode == 0:
        log("Multiplexed SSH master socket established.")
        return True
    else:
        logger.error("Failed to start SSH multiplexer: %s", start_res.stderr)
        return False


def stop_ssh_mux():
    """Closes SSH multiplexed master socket."""
    cmd = [
        "ssh", "-O", "exit",
        "-o", f"ControlPath={MUX_SOCKET}",
        f"{VPS_USER}@{VPS_HOST}"
    ]
    subprocess.run(cmd, capture_output=True, text=True)


def run_ssh_command(remote_cmd: str) -> Tuple[int, str]:
    """Executes a command on the VPS via the multiplexed SSH connection."""
    cmd = [
        "ssh",
        "-o", f"ControlPath={MUX_SOCKET}",
        f"{VPS_USER}@{VPS_HOST}",
        remote_cmd
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    return res.returncode, res.stdout.strip()


def launch_windows_browser(url: str) -> str:
    """Launches the target URL in the active visible Windows browser via direct single-instance IPC."""
    # 1. Native Chromium direct binary invocation (Fastest & triggers existing desktop window IPC)
    if os.path.exists(BRAVE_PATH):
        subprocess.Popen([BRAVE_PATH, url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return "Brave Browser (Windows native IPC)"
    elif os.path.exists(CHROME_PATH):
        subprocess.Popen([CHROME_PATH, url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return "Chrome (Windows native IPC)"
    elif os.path.exists(EDGE_PATH):
        subprocess.Popen([EDGE_PATH, url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return "Edge (Windows native IPC)"

    # Fallback via cmd.exe start
    try:
        subprocess.Popen(["cmd.exe", "/c", "start", "", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return "Default Windows Browser (via cmd start)"
    except Exception as e:
        logger.error("cmd.exe start failed: %s", e)

    return "Launch failed"


def claim_and_execute_task():
    """Atomically claims a pending task from the VPS queue and executes it locally."""
    # Script on VPS claims the oldest pending item atomically into in_progress
    claim_script = """
PENDING="$HOME/.local/state/airo-second-brain/pc-action-bridge/queue/pending"
IN_PROG="$HOME/.local/state/airo-second-brain/pc-action-bridge/queue/in_progress"
mkdir -p "$PENDING" "$IN_PROG"
for f in $(ls -tr "$PENDING"/*.json 2>/dev/null); do
  fname=$(basename "$f")
  mv "$f" "$IN_PROG/$fname"
  cat "$IN_PROG/$fname"
  break
done
"""
    rc, output = run_ssh_command(claim_script)
    if rc != 0 or not output:
        return

    try:
        packet = json.loads(output)
    except Exception as e:
        logger.error("Failed to parse claimed packet JSON: %s (raw: %s)", e, output)
        return

    action_id = packet.get("action_id", "unknown")
    action_type = packet.get("type", "unknown")
    payload = packet.get("payload", {})

    log(f"⚡ CLAIMED TASK: {action_id} (type={action_type})")

    if action_type == "open_url":
        url = payload.get("url")
        title = payload.get("title", "No Title")
        if url:
            browser_used = launch_windows_browser(url)
            log(f"🚀 EXECUTED open_url: '{title}' -> {url} via {browser_used}")

            # Mark as done on VPS
            mark_done_script = f"""
IN_PROG="$HOME/.local/state/airo-second-brain/pc-action-bridge/queue/in_progress/{action_id}.json"
DONE="$HOME/.local/state/airo-second-brain/pc-action-bridge/queue/done/{action_id}.json"
mkdir -p "$HOME/.local/state/airo-second-brain/pc-action-bridge/queue/done"
if [ -f "$IN_PROG" ]; then
  mv "$IN_PROG" "$DONE"
fi
"""
            run_ssh_command(mark_done_script)
            log(f"✅ TASK COMPLETED: {action_id}")
    else:
        logger.warning("Unknown action type: %s", action_type)


def daemon_loop():
    log("AIRO PC Relay Daemon started.")
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    def handle_signal(sig, frame):
        log(f"Received signal {sig}. Stopping daemon cleanly...")
        stop_ssh_mux()
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
        sys.exit(0)

    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    while True:
        try:
            if ensure_ssh_mux():
                claim_and_execute_task()
            else:
                log("SSH connection retry in 5s...")
                time.sleep(5)
        except Exception as e:
            logger.error("Error in daemon loop: %s", e)

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    daemon_loop()
