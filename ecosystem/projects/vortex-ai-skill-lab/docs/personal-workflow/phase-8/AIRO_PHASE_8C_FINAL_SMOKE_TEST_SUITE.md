# AIRO Personal Workflow Phase 8C Final Smoke Test Suite

Generated: 2026-05-09 12:50:19 UTC
Repository: progamer6918/vortex-ai-skill-lab
Branch: main
Base commit before Phase 8C suite: 67a0be1

Status:
PHASE 8C COMPLETE after this file and the smoke script are committed and pushed.

Official roadmap item:
Phase 8C: Final Smoke Test Suite

## Purpose

Create one local smoke test command for post-install and post-chat verification of Airo Personal Workflow.

The suite verifies the daily command, intent router, approval review, executor recommendation, dashboard alignment, Google fallback status, operations dashboard generation, and blocked live-trading route.

## Smoke Test Command

Run from the repository root:

    python3 scripts/personal-workflow/airo_final_smoke.py --text

Machine-readable output:

    python3 scripts/personal-workflow/airo_final_smoke.py --json

## Covered Checks

The smoke suite runs:

1. ./bin/airo-daily --text
2. ./bin/airo-daily
3. python3 scripts/personal-workflow/airo_intent_router.py "review my pending personal workflow queue"
4. python3 scripts/personal-workflow/airo_intent_router.py "catat beli makan 50000 pakai tokopedia credit card"
5. python3 scripts/personal-workflow/airo_approval_review.py list --status pending --compact
6. python3 scripts/personal-workflow/airo_executor_recommend.py list-actionable --limit 10
7. ./bin/airo-dashboard-align
8. python3 scripts/personal-workflow/airo_ops_dashboard.py
9. python3 scripts/personal-workflow/airo_google_fallback.py status
10. python3 scripts/personal-workflow/airo_intent_router.py "enable live trading and execute market orders now"

## Pass Criteria

A Phase 8C smoke run passes only when:

- all commands exit successfully
- each command produces output
- the live-trading route returns a safety/blocked-style response
- no real Google write is performed
- no live trading is enabled
- no OpenClaw service restart is performed
- no finance records are hard-deleted
- no secret, token, cookie, session, password, .env, browser profile, OAuth client, or OAuth token contents are read

## Safety Boundaries

Always active:

- do not read secrets, tokens, cookies, sessions, passwords, or .env files
- do not access browser profiles
- do not commit local DBs, receipts, OAuth tokens, OAuth clients, credentials, runtime state, or private files
- do not perform real Google writes without approval gate
- do not patch OpenClaw core without explicit approval
- do not restart OpenClaw service without explicit approval
- do not touch EarnsAI trading runtime unless explicitly requested
- do not enable live trading
- do not hard-delete finance records
- do not stage or commit untracked EarnsAI, runtime, trading, database, receipt, token, credential, or secret paths

## Output Modes

Text output is intended for quick terminal review.

JSON output is intended for future automation or support handoff. It includes command names, PASS/FAIL status, return codes, short output samples, and explicit safety flags.

## Failure Behavior

If any smoke case fails, the script exits non-zero and reports the failing case.

A failed smoke run must not be treated as Phase 8C completion. Fix the failing precondition and rerun the suite.

## Validation Run

Phase 8C validation must run:

    python3 scripts/personal-workflow/airo_final_smoke.py --text
    python3 scripts/personal-workflow/airo_final_smoke.py --json

## Final Decision

Phase 8C Final Smoke Test Suite is complete when:

- scripts/personal-workflow/airo_final_smoke.py exists
- this documentation file exists
- both text and JSON smoke modes pass
- only these Phase 8C files are staged
- the commit is pushed to origin/main

Next official item after Phase 8C:
Phase 8D Final Source-of-Truth Refresh
