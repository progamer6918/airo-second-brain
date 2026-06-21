# AIRO Personal Workflow Phase 8B Backup and Restore Guide

Generated: 2026-05-09T18:59:44+07:00
Repository: progamer6918/vortex-ai-skill-lab
Branch: main
Base commit before Phase 8B guide: 46e1d57

Status:
PHASE 8B COMPLETE

Official roadmap item:
Phase 8B: Backup and Restore Guide

## Purpose

Document how to safely backup and restore local Airo Personal Workflow data without reading, exposing, or committing secrets, credentials, receipts, OAuth tokens, local databases, or runtime files.

## Scope

This guide covers backup and restore for the current Airo Personal Workflow scope:
- local approval queue
- receipt manifest
- audit logs
- dashboard HTML
- Google API fallback exports
- local Google OAuth client/token paths
- GitHub source-of-truth docs

This guide does not expand the project roadmap and does not introduce a new phase.

## Safety Rules

Always active:
- do not read secrets, tokens, cookies, sessions, passwords, or .env files
- do not access browser profiles
- do not commit local DBs, receipts, OAuth tokens, or credentials
- do not perform real Google writes without approval gate
- do not patch OpenClaw core without approval
- do not restart OpenClaw service without approval
- do not touch EarnsAI trading runtime unless explicitly requested
- do not enable live trading
- do not hard-delete finance records

## Local Data Root

Default local data root:

    ~/.local/share/airo-personal-workflow/

Recommended backup destination pattern:

    ~/airo-personal-workflow-backups/YYYYMMDD-HHMMSS/

Backups should stay local or in a user-approved encrypted/private storage location.

## Important Local Paths

Approval queue database:

    ~/.local/share/airo-personal-workflow/approval_queue.sqlite

Receipt manifest database:

    ~/.local/share/airo-personal-workflow/receipts/manifest.sqlite

Receipts directory:

    ~/.local/share/airo-personal-workflow/receipts/

Dashboard directory:

    ~/.local/share/airo-personal-workflow/dashboard/

Google fallback exports:

    ~/.local/share/airo-personal-workflow/exports/google_api_fallback/

Audit files:

    ~/.local/share/airo-personal-workflow/audits/

Google local credential directory:

    ~/.local/share/airo-personal-workflow/google/

OAuth client local path:

    ~/.local/share/airo-personal-workflow/google/oauth_client.local.json

OAuth token local path:

    ~/.local/share/airo-personal-workflow/google/token.local.json

GitHub source-of-truth repository:

    ~/vortex-ai-skill-lab

## What To Backup

Backup these local artifacts when present:
- approval_queue.sqlite
- receipts/manifest.sqlite
- receipts directory metadata and files, if the user wants receipt continuity
- audits directory
- dashboard directory
- exports/google_api_fallback directory
- google/oauth_client.local.json
- google/token.local.json

Important:
OAuth files are sensitive. They may be backed up only to a private user-controlled destination. Their contents must not be printed, pasted into chat, committed to Git, or shared.

## What Must Never Be Committed

Never commit:
- local SQLite databases
- receipt files
- OAuth client files
- OAuth token files
- Google credential files
- cookies
- browser profiles
- .env files
- runtime state
- EarnsAI trading runtime files
- live trading config or state

## Safe Backup Command Pattern

Use metadata-preserving copy without printing file contents:

    mkdir -p "$HOME/airo-personal-workflow-backups/$(date +%Y%m%d-%H%M%S)"
    rsync -a --ignore-missing-args "$HOME/.local/share/airo-personal-workflow/" "$HOME/airo-personal-workflow-backups/$(date +%Y%m%d-%H%M%S)/airo-personal-workflow/"

Before moving backup files off the machine, confirm the destination is private, encrypted, and user-approved.

## Safe Restore Pattern

1. Stop any manual Airo operation currently running.
2. Create a pre-restore backup of the current local data root.
3. Restore files into:

       ~/.local/share/airo-personal-workflow/

4. Preserve permissions.
5. Do not open or print OAuth/token contents.
6. Run read-only verification commands.

## Restore Verification Commands

After restore, run:

    ./bin/airo-daily --text
    ./bin/airo-dashboard-align
    python3 scripts/personal-workflow/airo_approval_review.py list --status pending --compact
    python3 scripts/personal-workflow/airo_ops_dashboard.py
    python3 scripts/personal-workflow/airo_google_fallback.py status

Expected behavior:
- daily command works
- dashboard alignment works
- approval queue is visible
- dashboard regenerates
- Google fallback status checks metadata only
- OAuth client/token content_read remains false
- no real Google write occurs

## GitHub Source-of-Truth Backup

The GitHub repo stores project docs, roadmap, handoff, and command contracts.

To verify source-of-truth docs after restore:

    git checkout main
    git pull --ff-only
    sed -n "1,220p" docs/personal-workflow/AIRO_PROJECT_INDEX.md
    sed -n "1,260p" docs/personal-workflow/AIRO_CONTINUITY_PACK.md
    sed -n "1,220p" docs/personal-workflow/AIRO_NEW_CHAT_BOOTSTRAP_TEMPLATE.md
    sed -n "1,260p" docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_PHASE_7_HANDOFF.md
    sed -n "1,260p" docs/personal-workflow/phase-8/AIRO_PHASE_8_ROADMAP.md

## Phase 8B Validation

PASS - backup and restore paths documented
PASS - approval queue backup target documented
PASS - receipt manifest backup target documented
PASS - audit log backup target documented
PASS - dashboard backup target documented
PASS - Google fallback export backup target documented
PASS - OAuth local paths documented without reading contents
PASS - forbidden commit list documented
PASS - restore verification commands documented
PASS - no real write required
PASS - no secret content read required

## Final Decision

Phase 8B Backup and Restore Guide is complete.

Next official item:
Phase 8C Final Smoke Test Suite
