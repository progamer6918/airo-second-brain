# AIRO Personal Workflow Phase 4 Roadmap

Created: 2026-05-08T21:38:41+07:00
Repository: progamer6918/vortex-ai-skill-lab
Branch: main
Base commit: 6654519

Status:
OFFICIAL NEXT ROADMAP AFTER PHASE 3

## Purpose

Phase 4 turns Airo Personal Workflow from a stable capability set into a smoother daily-use operating workflow.

Phase 4 focuses on:
- making commands easier to use
- making approvals executable through a controlled local flow
- improving Google Sheets sync reliability
- improving dashboard visibility
- improving OpenClaw/Airo handoff behavior
- preserving all safety boundaries

## Starting Checkpoint

Already complete:
- MVP v0.1
- Phase 2 complete
- Phase 3 complete
- OAuth Google Sheets write works
- approval queue works
- action gate works
- receipt intake works
- receipt-to-transaction review works
- enhanced local dashboard works

Source of truth:
docs/personal-workflow/AIRO_PROJECT_INDEX.md

Latest handoff:
docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_PHASE_3_HANDOFF.md

Phase 3 release tag:
airo-personal-workflow-phase-3-complete

## Phase 4 Goal

Make Airo usable as a practical daily personal workflow assistant.

Expected result:
- User can run fewer, simpler commands.
- Sensitive actions enter queue automatically.
- Approved queue items can be executed through a controlled executor.
- Google Sheets sync can run from approved queue items.
- Dashboard shows current workflow state clearly.
- OpenClaw/Airo has clear routing instructions for queue-first behavior.
- GitHub remains the durable project memory.

## Phase 4 Milestones

### Phase 4A: Stabilization and Command Inventory

Goal:
Verify Phase 3 checkpoint and document all current commands, scripts, local paths, and run modes.

Output:
- Phase 4A stabilization report
- command inventory
- smoke tests
- commit and push after PASS

### Phase 4B: Unified Local Command Wrapper

Goal:
Create one local entry command for Phase 3/4 helper scripts.

Target:
- one wrapper for dashboard, queue, receipt review, Sheets dry-run, and action gate
- no real execution by default
- pure JSON where needed

Output:
- wrapper script
- smoke tests
- docs

### Phase 4C: Approval Queue Executor

Goal:
Add a local executor that can execute approved queue items safely.

Initial supported executor:
- approved Google Sheets append only

Blocked:
- deletion
- trading
- browser profile access
- service restart
- OpenClaw core patch

Output:
- executor script
- approved-only checks
- dry-run mode
- audit log
- no execution without approval

### Phase 4D: Google Sheets Sync Reliability Pass

Goal:
Make Google Sheets sync more reliable and auditable.

Focus:
- token preflight
- spreadsheet/tab validation
- duplicate prevention strategy
- append result audit
- fallback to CSV export when API is unavailable

Output:
- sync preflight
- better error handling
- docs

### Phase 4E: Dashboard Operations View

Goal:
Improve dashboard for daily operations.

Add visibility for:
- pending approvals
- approved but not executed items
- executed items
- recent receipt reviews
- recent Sheets write audits
- local fallback/export state

Output:
- dashboard operations view
- read-only local HTML
- no external access

### Phase 4F: OpenClaw/Airo Queue-First Instruction Update

Goal:
Update OpenClaw/Airo instruction so sensitive actions route to the action gate and approval queue first.

Boundary:
- instruction patch only after approval
- no OpenClaw core patch
- no service restart unless explicitly approved

Output:
- patch proposal
- apply log if approved
- smoke test

### Phase 4G: Phase 4 Handoff and Release Tag

Goal:
Close Phase 4 with docs, smoke tests, source-of-truth update, and release tag.

Output:
- Phase 4 handoff
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

Start with Phase 4A Stabilization and Command Inventory.

Validation:
PASS - inside git repo
PASS - branch main
PASS - project index exists
PASS - Phase 3 handoff exists
PASS - Phase 3 release tag exists
PASS - airo-workflow available
