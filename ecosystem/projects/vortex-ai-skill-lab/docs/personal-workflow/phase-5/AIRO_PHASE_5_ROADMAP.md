# AIRO Personal Workflow Phase 5 Roadmap

Created: 2026-05-08T21:53:38+07:00
Repository: progamer6918/vortex-ai-skill-lab
Branch: main
Base commit: 36ea401

Status:
OFFICIAL NEXT ROADMAP AFTER PHASE 4

## Purpose

Phase 5 turns the Phase 4 local workflow system into a smoother daily automation loop.

The focus is not adding random features. The focus is making the existing system usable end-to-end:

- capture
- queue
- review
- approve
- execute
- sync
- audit
- dashboard visibility
- fallback when Google API is unavailable

## Starting Checkpoint

Already complete:
- MVP v0.1
- Phase 2 complete
- Phase 3 complete
- Phase 4 complete
- OpenClaw/Airo queue-first instruction exists
- OAuth Google Sheets write works
- approval queue exists
- action gate exists
- queue executor exists
- sync reliability helper exists
- receipt review flow exists
- operations dashboard exists
- unified wrapper exists at ./bin/airoctl

Source of truth:
docs/personal-workflow/AIRO_PROJECT_INDEX.md

Latest handoff:
docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_PHASE_4_HANDOFF.md

Phase 4 release tag:
airo-personal-workflow-phase-4-complete

## Phase 5 Goal

Make Airo Personal Workflow usable as a practical daily personal workflow loop.

Expected result:
- User can capture normal finance activity quickly.
- Sensitive actions are queued automatically.
- Approved Google Sheets writes can be executed safely.
- Receipt review can become an approved transaction proposal.
- Dashboard shows what needs attention.
- Fallback CSV/App Script strategy is documented for Google Cloud trial expiry.
- GitHub remains the durable project memory.

## Phase 5 Milestones

### Phase 5A: Stabilization and Live-State Review

Goal:
Verify Phase 4 checkpoint, local queue state, dashboard state, OAuth token state, and command health.

Output:
- Phase 5A live-state review
- no real writes
- commit and push after PASS

### Phase 5B: Approved Google Sheets Queue Execution

Goal:
Execute approved google_sheets_write queue items through the controlled executor.

Rules:
- dry-run first
- only approved queue items
- explicit execute flag required
- spreadsheet id required
- audit required
- no secret print
- no browser profile access

Output:
- execution report
- improved executor docs
- no credential/token commit

### Phase 5C: Receipt Review to Approved Transaction Proposal

Goal:
Convert receipt review payload into a queue-approved transaction proposal.

Boundary:
This phase prepares transaction proposal execution, but does not hard-delete or mutate records without approval.

Output:
- transaction proposal format
- approval queue bridge
- dry-run transaction preview
- audit report

### Phase 5D: Approved Transaction Write Executor

Goal:
Allow approved transaction proposals to write into the local Airo finance workflow safely.

Rules:
- approved queue item only
- dry-run first
- no hard delete
- reversible audit
- local SQLite mutation only after explicit approval

Output:
- executor extension
- transaction write audit
- smoke tests

### Phase 5E: Dashboard Daily Ops Polish

Goal:
Make the operations dashboard more useful for daily decisions.

Add:
- next-action section
- approved-but-not-executed section
- failed/error audit section
- fallback CSV section
- receipt review section
- Google sync readiness section

Output:
- dashboard polish
- local read-only HTML
- no external write

### Phase 5F: Google API Fallback Strategy

Goal:
Prepare fallback paths for when Google Cloud trial expires or API access is unavailable.

Fallback options:
- CSV export/import
- local dashboard only
- optional Apps Script Web App plan
- manual sync checklist

Output:
- fallback strategy doc
- CSV flow command
- Apps Script proposal only
- no new external deployment without approval

### Phase 5G: Phase 5 Handoff and Release Tag

Goal:
Close Phase 5 with docs, source-of-truth update, smoke tests, and release tag.

Output:
- Phase 5 handoff
- updated project index
- release tag

## Safety Boundaries

Always active:
- do not read secrets, tokens, cookies, sessions, passwords, or .env files
- do not access browser profiles
- do not perform real Google write without approval gate
- do not patch OpenClaw core without approval
- do not restart OpenClaw service without approval
- do not touch EarnsAI trading runtime unless explicitly requested
- do not enable live trading
- do not hard-delete finance records
- do not commit local DBs, receipts, OAuth tokens, or credentials to GitHub

## Working Style

Use one paste-safe command per milestone.

Each milestone must:
- check repo
- check branch
- smoke test
- write/update docs
- commit after PASS
- push to main

Do not create extra phases or sub-phases unless explicitly approved.

## Next Action

Start with Phase 5A Live-State Review.

Validation:
PASS - inside git repo
PASS - branch main
PASS - project index exists
PASS - Phase 4 handoff exists
PASS - Phase 4 release tag exists
PASS - airo-workflow available
PASS - found executable bin/airoctl
PASS - found executable scripts/personal-workflow/airo_queue_executor.py
PASS - found executable scripts/personal-workflow/airo_sheets_sync.py
PASS - found executable scripts/personal-workflow/airo_ops_dashboard.py
PASS - found executable scripts/personal-workflow/airo_receipt_review.py
PASS - found executable scripts/personal-workflow/airo_action_gate.py
