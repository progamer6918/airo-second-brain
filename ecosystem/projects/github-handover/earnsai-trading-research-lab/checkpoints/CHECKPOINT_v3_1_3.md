# EarnsAI Pulse v3.1.3 Checkpoint

## Status
READY — Phase 4 Trading Research Lab

## New Feature
Multi-command support for safe read-only commands.

## Supported Multi-Commands
- /status
- /system
- /balance
- /price
- /help
- /start

## Safety Rule
/buy and /sell are blocked in multi-command mode to prevent accidental execution.
They must be sent one by one.

## Previous Stable Features
- Telegram bot running
- Persistent trading_data.json
- Virtual trading engine
- Robust price fallback
- Fast degraded cache mode
