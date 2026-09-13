#!/usr/bin/env python3
"""
AIRO Second Brain — Earesmes Telegram Action Listener (Redirected to Gateway)
"""
import sys
import os

# Note: Telegram ingress is canonically managed by airo-telegram-gateway.service.
# This entrypoint exits cleanly to prevent duplicate polling from legacy Windows Task Scheduler triggers.
if __name__ == "__main__":
    sys.exit(0)
