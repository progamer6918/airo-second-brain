# EarnsAI Pulse Trading — Next Action

Last updated: 2026-05-07

## Current Completed State

EarnsAI Pulse Trading has reached local paper-only dry-run MVP operation.

Validated capabilities:

- Local continuous paper runtime runs in tmux.
- Runtime status can be checked safely.
- Runtime tail can be viewed safely.
- Runtime can be stopped safely.
- Telegram periodic runtime reporting is active.
- Telegram paper control bot is active.
- Telegram commands validated:
  - /help
  - /status
  - /report
  - /tail
- Dangerous commands remain blocked:
  - /buy
  - /sell
  - /live_on
  - /unlock_live
  - /show_env
  - /set_secret
  - /trade
  - /market_order
- Runtime remains PAPER_ONLY.
- live_trading_locked remains true.
- No real-money execution is enabled.
- No private exchange API is enabled.

## Active Operator Commands

Local terminal:

    make paper-runtime-tmux-status
    make paper-runtime-tmux-tail
    make paper-runtime-tmux-stop
    make paper-runtime-tmux-start
    make paper-status
    make paper-report
    make paper-readiness-clean

Telegram:

    /help
    /status
    /report
    /tail
    /start
    /stop
    /readiness
    /maintenance

## Autostart Status

WSL autostart has been installed through ~/.bashrc.

Expected behavior:

- when WSL opens, paper runtime should start if not already running
- Telegram paper control bot should start if not already running

Important:

- final autostart validation from a clean stopped state should still be checked if not already recorded in docs/PHASE9F_WSL_AUTOSTART_VALIDATION.md

## Next Recommended Phase

Phase 10A: Paper Strategy Quality Evaluation

Goal:

Evaluate whether the current strategy is useful, too conservative, too noisy, or stuck in HOLD.

Main questions:

1. How often does the strategy produce HOLD, BUY, and SELL?
2. After enough runtime history, does the strategy ever generate simulated trades?
3. Are BUY/SELL signals reasonable based on MA/RSI logic?
4. Does the runtime report explain clearly why it holds?
5. Should strategy thresholds be tuned?
6. Should Telegram reports include daily summary and warning alerts?
7. Should runtime health alerts be added if bot stops unexpectedly?

## Recommended Next Commands in New Chat

Start with:

    cd ~/earnsai-pulse-trading
    git status --short
    git log --oneline -8
    cat PROJECT_CARRY_OVER.md
    cat NEXT_ACTION.md
    make paper-runtime-tmux-status
    make paper-control-tmux-status

## Safety Reminder

Do not enable:

- live trading
- real-money execution
- private exchange API
- arbitrary shell execution through Telegram

This project remains:

- PAPER_ONLY
- dry-run only
- research-only
- local operator controlled
