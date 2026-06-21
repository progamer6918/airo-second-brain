# Phase 9F WSL Autostart Validation

Last updated: 2026-05-07

## Result

WSL interactive-shell autostart has been validated.

## Validated Behavior

From a clean stopped state, opening a new WSL interactive shell starts:

- EarnsAI paper runtime tmux session
- EarnsAI Telegram paper control bot tmux session

## Validated Sessions

- earnsai-paper-runtime
- earnsai-paper-control

## Safety

This autostart does not enable:

- live trading
- real-money execution
- private exchange API
- arbitrary Telegram shell execution

The system remains:

- PAPER_ONLY
- dry-run only
- local operator controlled

## Local Secret Storage

Telegram credentials remain outside the repo:

    ~/.config/earnsai-pulse/paper_runtime.env

This file must not be committed.
