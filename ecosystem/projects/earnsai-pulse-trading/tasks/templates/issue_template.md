# [AREA] Task title

## Context
...

## Goal
...

## Scope
...

## Allowed Changes
- ...

## Forbidden Changes
- Do not read or print .env
- Do not print token, secret, credential, private key, cookie, session, or API key
- Do not push to GitHub without explicit approval
- Do not enable live trading
- Do not add private exchange API
- Do not mix Notion and trading scope
- Do not run destructive commands

## Safety Guardrails
- PAPER_ONLY for trading tasks
- LIVE_TRADING_LOCKED=true for trading tasks
- dry-run first for Notion tasks
- no secret exposure

## Files/Folders Likely Affected
- ...

## Commands to Validate
```bash
git status --short
make ci-safe
Acceptance Criteria
validation commands PASS
no secret printed
only allowed files changed
generated files cleaned
git status clean or expected
Rollback Plan
inspect git status
inspect git diff
restore specific files only
do not reset hard without approval
Notes for AI Agent
one safe bundled command when possible
do not leave scope
show expected result
stop at checkpoint
