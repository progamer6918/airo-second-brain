# EarnsAI Pulse v3.1.3 VERIFIED

## Status
VERIFIED — Phase 4 Trading Research Lab

## Verified Features
- /status works
- /balance works
- /price works
- Multi-command support works in one Telegram bubble:
  - /status
  - /balance
  - /price

## Safety Behavior
- Multi-command mode processes read-only commands.
- /buy and /sell are blocked in multi-command mode.

## Current Mode
- Virtual trading only
- Persistent memory via trading_data.json
- Fast degraded mode using cached BTC price when live feeds timeout

## Next Recommended Patch
v3.1.4 Trade Safety Guard:
- Add /whoami
- Add optional TELEGRAM_ADMIN_ID support
- Restrict /buy and /sell to admin when TELEGRAM_ADMIN_ID is configured
