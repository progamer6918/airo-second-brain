# EarnsAI Pulse Trading — Phase 9 Safety Rules

## Locked Rules
- PAPER_ONLY remains mandatory.
- LIVE_TRADING_LOCKED=true remains mandatory.
- FreqTrade remains dry-run only.
- Private exchange API remains disabled.
- Telegram remains monitoring and reporting only.
- Manual trading commands remain blocked.

## Required Gate
Every Phase 9 milestone must pass:

- make phase8-full-gate
- make security-scan
- make doctor

## Failure Rule
If any gate fails, stop development and fix the failed gate before adding features.
