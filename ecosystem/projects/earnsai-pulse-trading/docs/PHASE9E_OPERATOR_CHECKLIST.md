# Phase 9E Operator Checklist

Last updated: 2026-05-06

## Purpose

This checklist is for safe local paper-only operation of EarnsAI Pulse Trading.

The current goal is smooth dry-run validation, not live trading.

## Daily Safe Commands

### 1. Check paper status

Run:

    make paper-status

Expected:

- mode is PAPER_ONLY
- live_trading_locked is true
- latest signal exists
- Freqtrade bridge signal exists
- signals match

### 2. Read paper reports

Run:

    make paper-report

Expected:

- compact report is readable
- CI safe gate report is readable
- safety reminder remains paper/dry-run only

### 3. Run optimized readiness

Run:

    make paper-readiness-clean

Expected markers:

- PHASE9E_FULL_GATE_PASS
- PAPER_DRY_RUN_FAST_READINESS_PASS
- PAPER_READINESS_CLEAN_DONE

Expected after command:

    git status --short

The result should be clean.

## Heavy Validation

Use only when needed:

    make paper-readiness-full
    make paper-clean-generated

This may take longer and may regenerate tracked report or signal outputs.

## Safety Boundaries

Never:

- print .env
- print token, secret, credential, private key, cookie, session, or API key
- enable live trading
- enable real-money trading
- add private exchange API
- bypass risk gate

## Current Interpretation

Phase 9E has a smooth paper-only validation path.

This is not yet the same as proving a long-running continuous dry-run runtime.

Before claiming 100% smooth dry-run, the next work should clarify:

- start command
- status command
- report command
- readiness command
- cleanup command
- stop expectation
- whether continuous loop/runtime exists or needs a safe operator wrapper

## Continuous Runtime Commands

The paper runtime can be started in tmux for background operation while PC/WSL is alive.

Use:

    make paper-runtime-tmux-start

Check status:

    make paper-runtime-tmux-status

View recent output:

    make paper-runtime-tmux-tail

Attach interactively:

    make paper-runtime-tmux-attach

Stop safely:

    make paper-runtime-tmux-stop

Expected safe runtime markers:

- PAPER_RUNTIME_STARTED mode=PAPER_ONLY live_trading_locked=true
- TICK cycle=...
- PAPER_RUNTIME_TMUX_RUNNING while active
- PAPER_RUNTIME_TMUX_STOPPED after stop

If the tmux session remains after Ctrl+C, the stop command is allowed to kill the tmux session. This does not enable live trading and does not touch secrets.

## Continuous Runtime Commands

The paper runtime can be started in tmux for background operation while PC and WSL are alive.

Use:

    make paper-runtime-tmux-start

Check status:

    make paper-runtime-tmux-status

View recent output:

    make paper-runtime-tmux-tail

Attach interactively:

    make paper-runtime-tmux-attach

Stop safely:

    make paper-runtime-tmux-stop

Expected safe runtime markers:

- PAPER_RUNTIME_STARTED mode=PAPER_ONLY live_trading_locked=true
- TICK cycle appears while active
- PAPER_RUNTIME_TMUX_RUNNING while active
- PAPER_RUNTIME_TMUX_STOPPED after stop
- PAPER_RUNTIME_TMUX_NOT_RUNNING after stopped

If the tmux session remains after Ctrl+C, the stop command may kill the tmux session. This does not enable live trading and does not touch secrets.
