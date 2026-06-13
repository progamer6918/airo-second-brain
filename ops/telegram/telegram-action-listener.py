#!/usr/bin/env python3
"""
AIRO Second Brain — Earesmes Telegram Action Listener (Redirected to Gateway)
"""
import sys
import os

if __name__ == "__main__":
    gateway_path = os.path.join(os.path.dirname(__file__), "telegram-gateway.py")
    if os.path.exists(gateway_path):
        os.execv(sys.executable, [sys.executable, gateway_path] + sys.argv[1:])
    else:
        print(f"Error: {gateway_path} not found.", file=sys.stderr)
        sys.exit(1)
