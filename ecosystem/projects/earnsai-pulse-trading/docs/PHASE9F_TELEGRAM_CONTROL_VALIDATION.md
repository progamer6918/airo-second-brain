# Phase 9F Telegram Control Validation

Last updated: 2026-05-07

## Result

Telegram paper control bot has been validated.

Observed working Telegram commands:

- /help
- /status
- /report
- /tail

## Current Operator Capability

The user can now operate the local paper runtime from Telegram using safe commands.

Allowed commands:

- /help
- /status
- /start
- /stop
- /tail
- /report
- /readiness
- /maintenance

Blocked commands:

- /buy
- /sell
- /live_on
- /unlock_live
- /show_env
- /set_secret
- /trade
- /market_order

## Autostart

WSL interactive-shell autostart is installed through ~/.bashrc.

Autostart script:

- scripts/autostart_wsl_safe.sh

When WSL opens, it attempts to start:

- paper runtime tmux session
- Telegram paper control bot tmux session

## Safety

This phase does not enable:

- live trading
- real-money execution
- private exchange API
- arbitrary shell execution through Telegram

The system remains PAPER_ONLY, dry-run only, and local-operator controlled.
