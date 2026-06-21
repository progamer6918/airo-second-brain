# AIRO Batch-forward Execution Mode

Status: ACTIVE
Date: 2026-05-10
Scope: Airo Personal Workflow, especially Google Sheet Finance and future sync work.

## Purpose

Batch-forward mode is the default execution mode for this project.

The goal is to move faster with fewer micro-steps while preserving non-negotiable safety boundaries.

## Default working style

Prefer one substantial batch per turn or milestone:

1. read source-of-truth docs
2. implement the planned artifact
3. run smoke tests
4. update handoff/carryover when relevant
5. stage only intended files
6. check restricted paths
7. commit and push
8. state the next official item

Do not split into tiny steps unless there is a real blocker.

## Command style

When a command is needed:

- provide exactly one command block
- code fence language must be bash only
- command contents must start with bash -lc
- no command outside the fenced block
- no nested markdown code blocks
- no markdown attributes or IDs in the code fence
- command must bootstrap the repo and cd into the repo
- command must read source-of-truth docs before changing project files
- command must stage only intended files
- command must avoid restricted paths

If command formatting cannot be guaranteed, respond with:

FORMAT_RISK: command withheld.

## Batch-forward expectations

For project tasks, aim to complete multiple useful outcomes in one step:

- design plus implementation artifact
- implementation plus smoke test
- smoke test plus documentation
- documentation plus carryover update
- commit plus push

Avoid unnecessary "confirm before every small patch" behavior.

## Non-negotiable boundaries

Batch-forward does not override these boundaries:

- do not read token, .env, credentials, OAuth secret/client, private key, cookies, session, or browser profile
- do not commit local DB, receipt files, runtime state, credentials, tokens, or secrets
- do not touch EarnsAI, runtime, or trading
- do not enable live trading
- do not hard-delete finance records
- do not perform real Google Sheets finance ledger write without explicit approval gate
- do not patch or restart OpenClaw service without explicit approval

## Google Sheets sync-specific policy

Default modes:

- dry_run
- sheet_read_only
- write_preview

Write mode requires exact approval phrase:

I APPROVE GOOGLE SHEETS WRITE FOR AIRO FINANCE

Even in batch-forward mode, real write must remain controlled and idempotent.

## Quality bar

Batch-forward must optimize for:

- no avoidable mistakes
- no known bugs
- smoke tests before commit
- clear rollback/skip behavior
- idempotent operations
- concise but complete handoff updates
