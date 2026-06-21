# AIRO Personal Workflow Phase 6 Roadmap

Created: 2026-05-08T22:09:40+07:00
Repository: progamer6918/vortex-ai-skill-lab
Branch: main
Base commit: 669d83f

Status:
OFFICIAL NEXT ROADMAP AFTER PHASE 5

## Purpose

Phase 6 makes Airo Personal Workflow more seamless for daily use from chat, OpenClaw, and terminal.

The focus is reducing friction between user message, intent routing, queue creation, approval visibility, executor dry-run, approved execution, audit, and dashboard follow-up.

## Starting Checkpoint

Already complete:
- MVP v0.1
- Phase 2 complete
- Phase 3 complete
- Phase 4 complete
- Phase 5 complete
- continuity pack for new chats
- new chat bootstrap template
- airo-workflow global command
- ./bin/airoctl wrapper
- queue-first OpenClaw/Airo instruction
- OAuth Google Sheets write
- approved queue executor
- transaction proposal flow
- transaction executor
- daily ops dashboard
- Google API fallback strategy

Source of truth:
docs/personal-workflow/AIRO_PROJECT_INDEX.md

Continuity pack:
docs/personal-workflow/AIRO_CONTINUITY_PACK.md

New chat bootstrap:
docs/personal-workflow/AIRO_NEW_CHAT_BOOTSTRAP_TEMPLATE.md

Latest handoff:
docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_PHASE_5_HANDOFF.md

Phase 5 release tag:
airo-personal-workflow-phase-5-complete

## Phase 6 Goal

Make the workflow feel like one practical assistant loop instead of many separate scripts.

Expected result:
- Airo can classify common personal workflow messages locally.
- Safe finance capture routes to airo-workflow.
- Sensitive actions route to approval queue.
- Approved queue items have clear dry-run and execute commands.
- Dashboard shows exactly what to do next.
- OpenClaw/Airo instructions point to the unified router.
- No sensitive execution happens without approval.

## Phase 6 Milestones

### Phase 6A: Seamless Readiness Review

Goal:
Verify Phase 5 checkpoint, queue state, dashboard state, wrapper state, continuity pack, and OpenClaw instruction state before adding routing polish.

Output:
- readiness report
- smoke tests
- no real writes
- commit and push after PASS

### Phase 6B: Local Intent Router

Goal:
Create a local router that accepts a natural message and returns the correct safe route.

Examples:
- catat beli makan 50k -> airo-workflow dry-run/real route
- upload ke Google Sheets -> action gate route
- lihat approval -> airoctl queue route
- buka dashboard -> dashboard route
- live trading -> blocked JSON

Output:
- router script
- JSON output
- smoke tests
- no real execution by default

### Phase 6C: Approval Review CLI

Goal:
Make approval queue easier to inspect from terminal.

Capabilities:
- list pending
- inspect item
- show recommended dry-run command
- approve item with note
- reject item with note
- never execute directly

Output:
- approval review CLI
- docs
- smoke tests

### Phase 6D: Executor Command Recommendation

Goal:
For approved queue items, generate the safest next command.

Examples:
- approved google_sheets_write gives queue executor dry-run command
- approved sqlite_mutation gives transaction executor dry-run command
- unsupported action gives blocked or unsupported reason

Output:
- recommendation helper
- JSON output
- dashboard-compatible result

### Phase 6E: Dashboard Next-Action Upgrade

Goal:
Add actionable daily next steps to the dashboard.

Add:
- recommended command for each approved item
- pending approval summary
- rejected/error audit visibility
- fallback recommendation when Google token or API unavailable
- queue health summary

Output:
- dashboard update
- no execution from dashboard

### Phase 6F: OpenClaw/Airo Unified Router Instruction Update

Goal:
Patch OpenClaw/Airo instruction to use the local intent router first.

Boundary:
- instruction patch only
- no OpenClaw core patch
- no service restart unless explicitly approved

Output:
- patch log
- backup
- smoke test

### Phase 6G: Phase 6 Handoff and Release Tag

Goal:
Close Phase 6 with docs, source-of-truth update, smoke tests, and release tag.

Output:
- Phase 6 handoff
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

Start with Phase 6A Seamless Readiness Review.

Validation:
PASS - inside git repo
PASS - branch main
PASS - project index exists
PASS - continuity pack exists
PASS - new chat template exists
PASS - Phase 5 handoff exists
PASS - Phase 5 release tag exists
PASS - found executable bin/airoctl
PASS - found executable scripts/personal-workflow/airo_queue_executor.py
PASS - found executable scripts/personal-workflow/airo_transaction_executor.py
PASS - found executable scripts/personal-workflow/airo_transaction_proposal.py
PASS - found executable scripts/personal-workflow/airo_google_fallback.py
PASS - found executable scripts/personal-workflow/airo_ops_dashboard.py
PASS - found executable scripts/personal-workflow/airo_action_gate.py
