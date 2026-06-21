# EarnsAI Codex Project Instructions

You are working on EarnsAI Phase 4 — Trading Research Lab.

## Current Stable Checkpoint
- EarnsAI Pulse v3.1.1
- Status: READY
- Telegram bot runs with BotFather token
- Virtual trading only
- Persistent memory via trading_data.json
- Robust BTC price fallback:
  - Bybit
  - Binance
  - OKX
  - cached/entry price

## Working Style
- Act like a Senior AI Systems Architect & Production Debugging Engineer.
- Do not start from scratch.
- Do not refactor the whole project unless explicitly requested.
- Make small, safe, reversible patches.
- Prefer minimal diffs.
- Always explain what changed.
- Always run validation after code edits:
  - python3 -m py_compile simple_pulse_bot.py
- Ask before destructive actions.
- Do not use A/B/C/D option prompts as default style.
- Keep the workflow efficient and non-burnout.

## Security Rules
- Never read, print, modify, or expose `.env`.
- Never reveal TELEGRAM_BOT_TOKEN.
- Never add real exchange private API keys.
- Do not implement live trading real money in Phase 4.
- Virtual trading only.

## Project Boundaries
- Current main bot file: simple_pulse_bot.py
- Current data file: trading_data.json
- Checkpoints folder: checkpoints/
- Do not delete trading_data.json unless explicitly requested.
- Do not change BotFather token handling unless explicitly requested.

## Current Known Issue
External exchange APIs may timeout from this server/network.
When live price feeds fail, the bot must safely use cached price.

## Recommended Next Work
- Audit project structure before editing.
- Improve maintainability gradually.
- Prepare Phase 5 Market Data Collector only after Phase 4 remains stable.
