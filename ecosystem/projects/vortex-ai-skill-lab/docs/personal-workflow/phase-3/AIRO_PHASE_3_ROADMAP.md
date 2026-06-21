# AIRO Personal Workflow Phase 3 Roadmap

Created: 2026-05-08T20:33:08+07:00
Repository: progamer6918/vortex-ai-skill-lab
Branch: main
Base commit: a79cac6

Status:
OFFICIAL NEXT ROADMAP AFTER PHASE 2

## Purpose

Phase 3 moves Airo Personal Workflow from completed local foundation into approved real-world operation.

Phase 3 must preserve the project rule:
local-first, approval-gated, no secret leakage, no browser profile access, no unapproved service restart, no EarnsAI trading access, and no hard-delete of finance records.

## Starting Checkpoint

Already complete:
- MVP v0.1
- Phase 2A health check
- Phase 2B OpenClaw/Airo routing
- Phase 2C SQLite reconcile
- Phase 2D Google OAuth bootstrap guide
- Phase 2E Google Sheets approval gate
- Phase 2F receipt attachment intake
- Phase 2G local dashboard and approval queue
- Phase 2 handoff
- project source-of-truth index

Primary source of truth:
docs/personal-workflow/AIRO_PROJECT_INDEX.md

Latest handoff:
docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_PHASE_2_HANDOFF.md

## Phase 3 Goal

Make Airo Personal Workflow practically usable as a daily personal assistant workflow with controlled real integrations.

Expected result:
- Airo can capture personal finance events.
- Airo can prepare Google Sheets write previews.
- Airo can queue sensitive actions for approval.
- User can approve or reject actions locally.
- Real Google Sheets write only happens after explicit approval.
- Receipts can be attached to finance workflow records.
- Dashboard gives local visibility of pending actions and recent workflow state.
- GitHub remains the durable memory for roadmap, decisions, and handoff.

## Phase 3 Milestones

### Phase 3A: Stabilization and Repo Cleanliness

Goal:
Verify Phase 2 checkpoint, repo cleanliness, command availability, and smoke tests before real integration work.

Output:
- Phase 3A stabilization report
- commit and push after PASS

No real Google access.

### Phase 3B: Local Google Credential Preflight

Goal:
Prepare local credential path and environment checks without reading or committing secrets.

Output:
- credential directory check
- safe config template
- preflight command
- no credential content printed
- no real OAuth login unless explicitly approved

No token or secret committed.

### Phase 3C: First Approval-Gated Google Sheets Write

Goal:
Use the Phase 2E writer to perform the first real Google Sheets append only after explicit user approval.

Required before real write:
- spreadsheet ID selected by user
- local credentials already stored outside repo
- rows preview shown
- approval queue item created
- user approval recorded
- command uses approval flag

Output:
- real-write audit report
- no credential committed
- commit only docs/audit, not local data

### Phase 3D: OpenClaw/Airo Approval Queue Integration

Goal:
Make sensitive Airo actions create approval queue items instead of executing immediately.

Sensitive actions include:
- Google Sheets write
- SQLite mutation/reconciliation
- receipt-to-transaction conversion
- any future external write

Output:
- routing design
- local queue integration
- smoke tests
- no OpenClaw core patch without approval

### Phase 3E: Receipt-to-Transaction Review Flow

Goal:
Connect receipt attachment intake to a review workflow.

Initial boundary:
No OCR by default.
Receipt metadata and user-provided description are enough for v1.

Output:
- intake-to-queue bridge
- manual transaction review payload
- approval before writing transaction record

### Phase 3F: Local Dashboard Usability Pass

Goal:
Improve the dashboard so the user can quickly see:
- pending approvals
- recent approvals
- receipt attachments
- Google Sheets write previews
- finance workflow status

Output:
- local dashboard improvement
- no browser profile access
- no background web access

### Phase 3G: Phase 3 Handoff and Release Tag

Goal:
Close Phase 3 with source-of-truth docs, handoff, smoke tests, and Git tag.

Output:
- Phase 3 handoff
- final smoke test
- release tag

## Safety Boundaries

Always active:
- do not read secrets, tokens, cookies, sessions, passwords, or .env files
- do not access browser profiles
- do not use real Google OAuth without approval
- do not write to Gmail, Drive, Sheets, Docs, or Calendar without approval gate
- do not patch OpenClaw core without approval
- do not restart OpenClaw service without approval
- do not touch EarnsAI trading runtime unless explicitly requested
- do not enable live trading
- do not hard-delete finance records
- do not commit local DBs, receipts, tokens, or credentials to GitHub

## Working Style

Use one paste-safe command per milestone.

Each milestone must:
- check repo
- check branch
- run smoke test
- write/update docs
- commit after PASS
- push to main

Do not create extra phases or sub-phases unless the user explicitly asks.

## Next Action

Start with Phase 3A stabilization and repo cleanliness.

Validation:
PASS - inside git repo
PASS - branch main
PASS - project index exists
PASS - Phase 2 handoff exists
PASS - airo-workflow available
