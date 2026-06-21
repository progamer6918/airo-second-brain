# AIRO Personal Workflow Phase 7 Roadmap

Created: 2026-05-08T22:21:07+07:00
Repository: progamer6918/vortex-ai-skill-lab
Branch: main
Base commit: a6c28ea

Status:
OFFICIAL NEXT ROADMAP AFTER PHASE 6

## Finish Estimate

Recommended remaining phases until practical completion:

- Phase 7: seamless daily execution loop
- Phase 8: final hardening, backup/restore, closeout, stable release

This means the project should be considered practically complete after Phase 8, unless the user expands the scope into a broader autonomous PC assistant.

## Purpose

Phase 7 turns the Phase 6 router-first workflow into a smoother daily loop.

The focus is:

- one-command daily status
- one-command router preview
- one-command approval review
- safer executor dry-run guidance
- better local dashboard handoff
- fewer separate scripts for the user
- no real execution without approval

## Starting Checkpoint

Already complete:

- MVP v0.1
- Phase 2 complete
- Phase 3 complete
- Phase 4 complete
- Phase 5 complete
- Phase 6 complete
- continuity pack complete
- new chat bootstrap template complete
- router-first OpenClaw/Airo instruction active
- local intent router active
- approval review CLI active
- executor recommendation helper active
- daily ops dashboard active
- Google fallback strategy active

Latest handoff:

docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_PHASE_6_HANDOFF.md

Phase 6 release tag:

airo-personal-workflow-phase-6-complete

## Phase 7 Goal

Make Airo Personal Workflow feel like one coherent local assistant workflow.

Expected result:

- user can ask a message and get the safe route
- user can review daily pending actions quickly
- user can see next commands clearly
- user can approve/reject from one review tool
- user can dry-run executors without guessing commands
- dashboard reflects the same recommended next actions
- OpenClaw/Airo stays router-first and queue-first

## Phase 7 Milestones

### Phase 7A: Daily Loop Readiness Review

Goal:
Verify Phase 6 checkpoint, router, approval review, recommendation helper, dashboard, and continuity files.

Output:
- Phase 7A readiness report
- smoke tests
- no real writes
- commit and push after PASS

### Phase 7B: Unified Daily Command

Goal:
Add one command that summarizes the daily state.

It should show:
- pending approvals
- approved items needing dry-run
- failed/blocked audits
- Google sync readiness
- dashboard path
- recommended next command

Output:
- daily command script
- JSON output
- smoke tests

### Phase 7C: Router Preview Integration

Goal:
Make router output more useful for daily use.

Add:
- confidence label
- recommended next step
- exact safe command
- reason for route
- blocked reason where relevant

Output:
- router update
- smoke tests

### Phase 7D: Approval Review UX Polish

Goal:
Improve approval review CLI for practical daily use.

Add:
- compact pending view
- item summary
- safer approve/reject prompts
- recommendation included in inspect result

Output:
- approval review CLI update
- smoke tests

### Phase 7E: Dashboard Daily Command Alignment

Goal:
Make dashboard and CLI recommendations consistent.

Add:
- daily loop summary section
- same recommended commands as daily CLI
- clearer action hierarchy

Output:
- dashboard update
- no execution from dashboard

### Phase 7F: Phase 7 Handoff and Release Tag

Goal:
Close Phase 7 with docs, source-of-truth update, smoke tests, and release tag.

Output:
- Phase 7 handoff
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
- write or update docs
- commit after PASS
- push to main

Do not create extra phases or sub-phases unless explicitly approved.

## Next Action

Start with Phase 7A Daily Loop Readiness Review.

Validation:
PASS - inside git repo
PASS - branch main
PASS - project index exists
PASS - Phase 6 handoff exists
PASS - Phase 6 release tag exists
PASS - found executable scripts/personal-workflow/airo_intent_router.py
PASS - found executable scripts/personal-workflow/airo_approval_review.py
PASS - found executable scripts/personal-workflow/airo_executor_recommend.py
PASS - found executable scripts/personal-workflow/airo_ops_dashboard.py
PASS - found executable scripts/personal-workflow/airo_queue_executor.py
PASS - found executable scripts/personal-workflow/airo_transaction_executor.py
PASS - found executable bin/airoctl
