#!/usr/bin/env bash
set -e
cd ~/earnsai-telegram-gateway/trading-research-lab
source .venv/bin/activate
pkill -f simple_pulse_bot.py 2>/dev/null || true
python3 simple_pulse_bot.py
