# Phase 9E Smooth Dry-Run Operator Readiness

Last updated: 2026-05-06

## Current Status

EarnsAI Pulse Trading is currently in Phase 9E VALIDATING.

The Phase 9E readiness audit confirmed:

- SECURITY_SCAN PASS
- DOCTOR PASS
- PHASE9A_SMOKE PASS
- PHASE9B_SMOKE PASS
- PHASE9C_SMOKE PASS
- PHASE9D_SMOKE PASS
- PHASE9E_SMOKE PASS
- PHASE9E_FULL_GATE_PASS
- PHASE9_FULL_GATE_PASS

Bridge status confirmed:

- mode: PAPER_ONLY
- live_trading_locked: true
- signals_match: true
- latest_action: HOLD
- latest_risk_status: REJECTED

## Interpretation

The project is technically healthy for paper-only validation.

However, it should still be treated as VALIDATING before being called 100% smooth dry-run, because operator commands still need to be easy, repeatable, and safe for a newbie user.

## Smooth Dry-Run Expectation

A smooth dry-run means:

- the system can run in paper-only mode
- live trading remains locked
- no private exchange API is required
- multi-agent decisions are filtered through risk gate
- Freqtrade bridge only receives paper/dry-run signals
- journal and reports can be checked safely
- the user can inspect status without reading secrets

A smooth dry-run does not mean:

- guaranteed profit
- real-money execution
- production 24/7 deployment
- live exchange trading
- private API key usage

## Operator Command Goal

The repo should provide simple commands:

- `make paper-status`
- `make paper-report`
- `make paper-readiness`

These commands are intended for safe local operation and validation only.

## Safety Rules

Never:

- print `.env`
- print token, secret, credential, private key, cookie, session, or API key
- enable live trading
- enable real-money trading
- add private exchange API
- bypass risk gate

The system remains:

- PAPER_ONLY
- dry-run only
- research-only
- safe MVP oriented

## Generated Output Cleanup

Some readiness and gate commands regenerate tracked paper reports or latest signal snapshots.

This is expected during validation.

Use:

```bash
make paper-clean-generated
make paper-readiness-clean
to run readiness and clean known generated output afterward.

These commands must not print secrets, read .env, enable live trading, or use private exchange API.

## Readiness Command Optimization

The first `paper-readiness-clean` test showed that full readiness can feel too slow for daily operator use because multiple gate layers may run repeatedly.

The operator workflow is now split into:

```bash
make paper-readiness
Fast readiness for normal operator validation.

make paper-readiness-clean

Fast readiness followed by known generated-output cleanup.

make paper-readiness-full

Full heavy validation for deeper checkpoint review.

Use the fast readiness path for normal paper-only dry-run checks. Use the full path only when a major validation checkpoint is needed.
