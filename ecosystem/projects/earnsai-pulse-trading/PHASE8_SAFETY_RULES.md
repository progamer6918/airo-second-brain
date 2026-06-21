# EarnsAI Pulse Trading — Phase 8 Safety Rules

## Locked Rules
- PAPER_ONLY remains mandatory.
- LIVE_TRADING_LOCKED=true remains mandatory.
- FreqTrade remains dry-run only.
- Private exchange API remains disabled.
- Telegram remains monitoring and governance only.
- Manual trading commands remain blocked.

## Phase 8 Safety Gate
Every Phase 8 milestone must pass these commands:

- make phase7-full-gate
- make bridge-status
- make telegram-dry-run
- make daily-report

## Failure Rule
If any safety gate fails, stop development and fix the gate before adding features.
