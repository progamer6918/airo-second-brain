# EarnsAI Project Boundaries

## Purpose
This document defines boundaries between EarnsAI subprojects so AI-assisted work stays inside the correct scope.

## Main Project Map

| Area | Location | Purpose | Current Handling | Risk |
|---|---|---|---|---|
| EarnsAI Pulse Trading | ~/earnsai-pulse-trading | Multi-agent trading research, risk gate, dry-run bridge, paper runtime | Active repo | Must stay PAPER_ONLY |
| Paper Runtime Live-Feel | ~/earnsai-pulse-trading/earnsai/paper_runtime | Paper-only simulation with virtual P/L | Active workflow | Generated runtime files must not pollute commits |
| Telegram Trading Layer | ~/earnsai-pulse-trading/earnsai/telegram | Trading status/report command router | Trading-only Telegram layer | Must not be mixed with Notion gateway |
| FreqTrade Dry-run Bridge | ~/earnsai-pulse-trading/freqtrade_user_data | Dry-run signal bridge/simulator boundary | Paper/dry-run only | Must not become live exchange execution |
| Telegram Gateway | ~/earnsai-telegram-gateway | Telegram gateway and routing project | Separate repo | Must not be mixed with Pulse Trading runtime |
| Trading Research Lab | ~/earnsai-telegram-gateway/trading-research-lab | Older research lab, Agent OS, Notion, paper trading experiments | Separate lab | Mixed scope, high caution |
| Notion Agent OS | ~/earnsai-telegram-gateway/trading-research-lab/agent_os/notion | Notion read/check/dry-run/guarded append | Notion-only scope | No token print, no delete, no bulk update |
| OpenClaw / Airo | ~/.openclaw and ~/.openclaw/workspace | Agent memory, identity, skills, backups | Sensitive workspace | Inventory first, no patch without dedicated issue |
| AI Agent Workspace | ~/AI_AGENT_WORKSPACE | Docs, inbox, archive, temporary outputs | Support workspace | Do not treat as active code repo |
| Backups | ~/earnsai-backups and ~/earnsai-pulse-trading-local-backups | Recovery backups | Reference only | Do not treat as source of truth |

## Hard Boundaries

### Trading Boundary
Trading-related work must keep:
- PAPER_ONLY
- LIVE_TRADING_LOCKED=true
- no private exchange API
- no real-money execution
- no live order execution

### Notion Boundary
Notion-related work must keep:
- dry-run first
- no token printing
- no delete operation
- no bulk update
- no external share or invite
- guarded append only after explicit approval

### Telegram Boundary

| Telegram Area | Location | Rule |
|---|---|---|
| Trading Telegram | ~/earnsai-pulse-trading/earnsai/telegram | Reports trading status only |
| Telegram Gateway Notion | ~/earnsai-telegram-gateway/src | Must not touch trading runtime |
| OpenClaw Telegram | ~/.openclaw/telegram | Must not be patched without OpenClaw issue |

## Issue Rule
One issue must target one area only.

Do not combine:
- Notion + trading
- OpenClaw + Pulse Trading
- Telegram Gateway + FreqTrade
- backup restore + feature development
- live trading + dry-run validation

## Recommended Labels Later
- safety
- trading
- dry-run
- telegram
- notion
- openclaw
- docs
- bug
- feature
- refactor
- no-live-trading

## Current Recommendation
Use local tasks/ first. Do not push to GitHub until repo is clean, remote is verified, no secret is staged, and user explicitly approves push/setup.
