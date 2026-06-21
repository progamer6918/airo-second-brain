# EarnsAI Pulse Trading — Project Carry Over

Last updated: 2026-05-06

## Active Repo

Primary active repo:

- `~/earnsai-pulse-trading`

This repo is the main EarnsAI Pulse Trading core.

## Current Valid Status

Current technical phase:

- Phase 9E Operator Readiness / Validating

Current interpretation:

- Phase 7 is not the current phase anymore.
- Phase 8 is completed as evaluation hardening.
- Phase 9 is the current validated architecture layer.
- Phase 9E has PASS gates, but the project should still be treated as VALIDATING before claiming 100% smooth dry-run readiness.
- The current active goal is smooth paper-only dry-run operation, not GitHub handover workflow.

## GitHub Handover Status

GitHub handover workflow ISSUE 001 through ISSUE 017 is considered completed as historical handover work.

Important decision:

- Do not continue ISSUE 018 automatically as the main roadmap.
- ISSUE 018 only matters if the user explicitly wants to audit the older Trading Research Lab under `~/earnsai-telegram-gateway/trading-research-lab`.
- For the main `earnsai-pulse-trading` repo, the active focus is Phase 9E validation and smooth paper-only dry-run readiness.

## Architecture Already Evidenced

The repo has evidence of:

- Multi-agent sequential orchestrator
- Research, technical, sentiment, strategy, risk, decision, and monitoring agents
- Signal schema
- Risk gate
- JSONL decision journal
- Freqtrade JSON bridge / dry-run adapter
- Telegram dry-run evaluation and reporting
- Evaluation metrics
- Journal analytics
- Deterministic fixtures
- Backtest adapter planning
- Stability hardening
- Data provider abstraction
- CI safe gate
- Operator guide / documentation hardening

## Operator Commands Added

The following newbie-friendly paper-only operator commands are now available:

- `make paper-status`
- `make paper-report`
- `make paper-readiness`

Confirmed behavior:

- `make paper-status` successfully reads bridge status.
- `make paper-report` successfully reads compact report and CI safe gate report.
- `make paper-report` keeps git status clean.
- Current bridge status remains `PAPER_ONLY`.
- Live trading remains locked.
- Latest observed action is `HOLD`.
- Latest observed risk status is `REJECTED`.
- EarnsAI signal and Freqtrade bridge signal match.

## Current Main Goal

Main goal now:

Make the Phase 9E paper-only dry-run flow smooth, understandable, repeatable, and safe before calling the system complete as a safe MVP.

A smooth dry-run means:

- the system can be checked with simple commands
- paper-only mode is obvious
- live trading remains locked
- risk gate remains active
- reports are readable
- bridge status is readable
- generated report noise is controlled
- a newbie can start, inspect, and stop safely

## Safety Rules

Never:

- print `.env`
- print token, secret, credential, private key, cookie, session, or API key
- enable live trading
- enable real-money trading
- add private exchange API
- bypass risk gate

The system must remain:

- paper-only
- dry-run only
- research-only
- safe MVP oriented

## Related Repo Caution

Related repo:

- `~/earnsai-telegram-gateway`

Known caution:

- This repo had many local status lines in the latest audit.
- It contains older Telegram Gateway and Trading Research Lab work.
- It should not be treated as the clean active trading core.
- Do not push or clean it without a separate read-only audit.

## Next Safe Step

Recommended next step:

Improve the Phase 9E operator workflow so the user has a clean newbie path:

1. `make paper-status`
2. `make paper-report`
3. controlled readiness check
4. cleanup generated report noise if needed
5. document start/status/report/stop expectations

Do not start live trading.
Do not request exchange keys.
Do not touch secrets.

## Latest Validated Operator Flow

Validated on: 2026-05-06

The optimized paper readiness flow has been validated.

Command validated:

    make paper-readiness-clean

Observed result:

- PHASE9E_FULL_GATE_PASS
- PAPER_DRY_RUN_FAST_READINESS_PASS
- PAPER_READINESS_CLEAN_DONE
- command exit code: 0
- git status after command: clean
- mode: PAPER_ONLY
- live trading locked: true
- signals match: true
- latest action: HOLD
- latest risk status: REJECTED

Interpretation:

- Phase 9E now has a smooth daily paper-only validation command.
- This validates readiness and cleans known generated output noise afterward.
- This does not mean live trading is enabled.
- This does not mean production 24/7 is approved.
- This does not mean real-money execution is allowed.

Recommended daily operator flow:

    make paper-status
    make paper-report
    make paper-readiness-clean

Use full validation only when needed:

    make paper-readiness-full
    make paper-clean-generated

## Latest Continuous Paper Runtime Validation

Validated on: 2026-05-07

The local continuous paper-only runtime lifecycle has been validated.

Observed flow:

    make paper-runtime-tmux-start
    make paper-runtime-tmux-status
    make paper-runtime-tmux-tail
    make paper-runtime-tmux-stop
    make paper-runtime-tmux-status

Observed result:

- PAPER_RUNTIME_TMUX_STARTED
- PAPER_RUNTIME_TMUX_RUNNING
- PAPER_RUNTIME_STARTED mode=PAPER_ONLY live_trading_locked=true
- TICK cycle appeared while running
- PAPER_RUNTIME_TMUX_STOPPED
- PAPER_RUNTIME_TMUX_NOT_RUNNING
- RAW_SESSION_AFTER_STOP=1
- git status remained clean

Current interpretation:

- Phase 9E has a smooth local continuous paper-only dry-run lifecycle.
- Runtime can run while PC and WSL are alive.
- This is still not live trading, not real-money execution, and not production 24/7 deployment.

## Latest Telegram Reporting Validation

Validated on: 2026-05-07

Telegram reporting for the local paper runtime has been validated.

Observed markers:

- telegram_enabled=True
- TELEGRAM_PERIODIC_REPORT_SENT

Current interpretation:

- The local continuous paper-only dry-run is running.
- Telegram periodic reporting is active.
- Latest report showed PAPER_ONLY mode and live lock true.
- No simulated trade has executed yet because strategy history was not enough for MA/RSI calculation.
- This remains paper-only and does not enable live trading or real-money execution.

## Latest Phase 9F Telegram Control Validation

Validated on: 2026-05-07

Telegram control bot is active.

Observed working commands:

- /help
- /status
- /report
- /tail

Current interpretation:

- The user can monitor the running paper runtime from Telegram.
- The user can request runtime report from Telegram.
- The Telegram control bot uses an allowlist of safe commands.
- Trading commands remain blocked.
- WSL autostart is installed through ~/.bashrc and starts runtime/control bot when WSL opens.

## Latest WSL Autostart Validation

Validated on: 2026-05-07

WSL interactive-shell autostart has been validated.

Observed result:

- paper runtime tmux session starts automatically
- Telegram paper control bot tmux session starts automatically
- local env file remains outside repo
- runtime remains PAPER_ONLY
- no live trading enabled
- no private exchange API enabled

Current operator expectation:

When WSL is opened, EarnsAI attempts to start the local paper runtime and Telegram control bot automatically if they are not already running.

## Latest GitHub Handover Note

The active next step is now stored in:

    NEXT_ACTION.md

Current project interpretation:

- Local paper-only dry-run MVP is operational.
- Telegram reporting is active.
- Telegram paper control is active.
- WSL autostart is installed.
- Next phase should be Phase 10A Paper Strategy Quality Evaluation.
- Do not continue old GitHub handover issue workflow as the active roadmap.
