# Phase 9F Autostart and Telegram Control

## Result

This phase adds:

- WSL interactive shell autostart
- safe paper runtime start script
- safe Telegram control bot start script
- Telegram operator commands for paper runtime control

## Telegram Commands

Allowed:

- /help
- /status
- /start
- /stop
- /tail
- /report
- /readiness
- /maintenance

Blocked:

- /buy
- /sell
- /live_on
- /unlock_live
- /show_env
- /set_secret
- /trade
- /market_order

## Local Secret Storage

Telegram token and chat ID are stored outside the repo:

    ~/.config/earnsai-pulse/paper_runtime.env

Permissions:

    chmod 600

This file must not be committed.

## Autostart

Autostart is installed in:

    ~/.bashrc

When WSL is opened interactively, it runs:

    scripts/autostart_wsl_safe.sh

This starts the paper runtime and Telegram control bot if they are not already running.

## Safety

This does not enable:

- live trading
- real-money execution
- private exchange API
- arbitrary Telegram shell execution

The system remains paper-only.
