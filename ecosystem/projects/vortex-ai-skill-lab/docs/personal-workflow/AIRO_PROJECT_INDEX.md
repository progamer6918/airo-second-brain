# AIRO Personal Workflow Project Index

Last updated: 2026-05-09T21:24:32+0700
Repository: progamer6918/vortex-ai-skill-lab
Branch: main
Latest commit when indexed: ffaa237
Phase 2 tag: airo-personal-workflow-phase-2-complete

## Read This First

Required chat operating rules:

    docs/personal-workflow/AIRO_CHAT_RULES.md

Every new AI chat must read the chat rules before generating repo commands, especially repo bootstrap, strict command formatting, safety boundaries, anti-hallucination rules, context meter, and carryover behavior.

This file is the source-of-truth index for continuing Airo Personal Workflow in any new AI chat.

Before giving commands, changing files, proposing phases, or touching integrations, the assistant must understand this index and then use the linked handoff and phase documents as the project memory.

Do not invent new phases.
Do not expand the roadmap without explicit user approval.
Do not touch EarnsAI trading runtime unless explicitly requested.
Do not patch OpenClaw core or restart services without explicit approval.

## Project Purpose

Airo Personal Workflow is a personal PC workflow assistant layer for the user.

The goal is to let Airo/OpenClaw safely handle recurring personal workflow tasks, especially personal finance capture and review, using local-first memory, clear command contracts, approval gates, GitHub handoff documentation, and carefully separated project boundaries.

The expected experience is seamless continuation across new chats:
- GitHub stores roadmap, handoff, status, decisions, and safety boundaries.
- The assistant reads the project index first.
- The assistant continues from the current checkpoint instead of asking the user to repeat context.
- Each milestone is paste-safe, scoped, committed, and pushed.
- Sensitive actions remain approval-gated.

## User Expectation

The user expects this project to behave like a durable AI-assisted operating workflow, not a one-off script.

Important expectations:
- smooth continuation in new chats
- GitHub as long-term memory
- no hallucinated roadmap
- no unnecessary sub-phases
- no overly fragmented commands
- one paste-safe command per milestone
- smoke test before commit
- commit and push after PASS
- respect safety boundaries
- keep project separation clean

## Project Separation

### 1. EarnsAI Pulse Trading

Purpose:
Paper-only trading MVP and trading research/runtime area.

Boundary:
Do not touch unless the user explicitly asks.
Live trading remains locked.
Do not enable live trading.

### 2. Vortex AI Skill Lab

Purpose:
Main repository for skill library, documentation, roadmap, handoff, and Airo Personal Workflow source-of-truth.

Repository:
progamer6918/vortex-ai-skill-lab

### 3. OpenClaw / Airo

Purpose:
Personal PC assistant layer.

Current relationship:
OpenClaw/Airo can route personal finance messages to the global command:

    airo-workflow "<original user message>"

Boundary:
Do not patch OpenClaw core or restart OpenClaw service without explicit approval.

### 4. Bubu the Receptionist

Purpose:
Receptionist/capture assistant.

Boundary:
Bubu is not the full PC executor.

## Current Stable Command

Normal mode:

    airo-workflow "catat beli makan 50k pakai tokopedia credit card"

Dry-run mode:

    AIRO_WORKFLOW_MODE=dry-run airo-workflow "bayar cicilan rumah 2500000"

## Completed Baseline

MVP v0.1 is complete.

Baseline capabilities:
- parser transaksi
- parser cicilan
- SQLite source of truth
- local CLI
- CSV/JSON export
- monthly markdown report
- Google Workspace dry-run
- Telegram local handler
- isolated test DB
- gateway entrypoint
- pure JSON wrapper
- global command airo-workflow
- systemd visibility
- OpenClaw instruction patch
- GitHub checkpoint

Primary handoff:
docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_V0_1_HANDOFF.md

## Completed Phase 2

Phase 2 is complete.

Final handoff:
docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_PHASE_2_HANDOFF.md

Final tag:
airo-personal-workflow-phase-2-complete

Completed roadmap:
- Phase 2A: health check and MVP review
- Phase 2B: OpenClaw/Airo personal finance routing
- Phase 2C: SQLite cleanup/reconcile without hard-delete
- Phase 2D: Google Workspace OAuth bootstrap guide without Git secrets
- Phase 2E: Google Sheets real-write approval gate
- Phase 2F: PDF/screenshot receipt attachment intake
- Phase 2G: local dashboard and approval queue

## Phase 2 Documents

Health check:
docs/personal-workflow/phase-2/AIRO_PHASE_2A_HEALTH_CHECK.md

Routing contract:
docs/personal-workflow/phase-2/AIRO_PHASE_2B_ROUTING_CONTRACT.md

SQLite reconcile:
docs/personal-workflow/phase-2/AIRO_PHASE_2C_SQLITE_RECONCILE.md

OAuth bootstrap guide:
docs/personal-workflow/phase-2/AIRO_PHASE_2D_GOOGLE_OAUTH_BOOTSTRAP.md

Google Sheets approval gate:
docs/personal-workflow/phase-2/AIRO_PHASE_2E_GOOGLE_SHEETS_APPROVAL_GATE.md

Attachment intake:
docs/personal-workflow/phase-2/AIRO_PHASE_2F_ATTACHMENT_INTAKE.md

Dashboard and approval queue:
docs/personal-workflow/phase-2/AIRO_PHASE_2G_LOCAL_DASHBOARD_APPROVAL_QUEUE.md

## Current Capabilities After Phase 2

Airo Personal Workflow can now support:
- personal transaction capture
- credit card expense capture
- installment payment capture
- installment progress check
- monthly summary
- local SQLite source of truth
- CSV/JSON export from MVP baseline
- monthly markdown report from MVP baseline
- OpenClaw/Airo routing instruction
- Google Sheets dry-run and approval-gated writer
- local PDF/screenshot receipt intake
- local approval queue
- local dashboard

## Important Local Paths

OpenClaw instruction:

    ~/.openclaw/workspace/AGENTS.md

Phase 2C reconcile ledger:

    ~/.local/share/airo-personal-workflow/phase2c/phase2c_reconcile_flags.sqlite

Receipt manifest:

    ~/.local/share/airo-personal-workflow/receipts/manifest.sqlite

Approval queue:

    ~/.local/share/airo-personal-workflow/approval_queue.sqlite

Local dashboard:

    ~/.local/share/airo-personal-workflow/dashboard/index.html

Google local credential directory recommendation:

    ~/.local/share/airo-personal-workflow/google/

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

## Known Issues

Earlier real-mode test transactions may exist in the main SQLite DB.

Phase 2C handled this by creating local backup and local reconcile ledger, without hard-delete and without committing raw finance data.

## Current Project Status

Airo Personal Workflow MVP v0.1: DONE
Airo Personal Workflow Phase 2: DONE
Whole Airo long-term vision: not declared complete unless a future roadmap says so.

This project is currently at a stable checkpoint and ready for one of these next decisions:
- freeze/stabilize
- create official Phase 3 roadmap
- perform approved real Google OAuth/Sheets setup
- improve OpenClaw/Airo runtime integration
- expand receipt understanding after explicit approval


## Official Next Roadmap

Phase 3 roadmap has been created as the next official roadmap after Phase 2.

Roadmap file:
docs/personal-workflow/phase-3/AIRO_PHASE_3_ROADMAP.md

Next execution item:
Phase 3A stabilization and repo cleanliness.


## Official Phase 3 Completion

Airo Personal Workflow Phase 3 is complete.

Phase 3 handoff:
docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_PHASE_3_HANDOFF.md

Phase 3 release tag:
airo-personal-workflow-phase-3-complete

Completed Phase 3 roadmap:
- Phase 3A stabilization and repo cleanliness
- Phase 3B local Google credential preflight
- Phase 3C first approval-gated Google Sheets write
- Phase 3D OpenClaw/Airo approval queue integration
- Phase 3E receipt-to-transaction review flow
- Phase 3F local dashboard usability pass
- Phase 3G handoff and release tag

Next status:
Stable checkpoint. Do not start Phase 4 without creating an official Phase 4 roadmap first.


## Official Next Roadmap After Phase 3

Phase 4 roadmap has been created as the next official roadmap after Phase 3.

Roadmap file:
docs/personal-workflow/phase-4/AIRO_PHASE_4_ROADMAP.md

Next execution item:
Phase 4A Stabilization and Command Inventory.


## Official Phase 4 Completion

Airo Personal Workflow Phase 4 is complete.

Phase 4 handoff:
docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_PHASE_4_HANDOFF.md

Phase 4 release tag:
airo-personal-workflow-phase-4-complete

Completed Phase 4 roadmap:
- Phase 4A stabilization and command inventory
- Phase 4B unified local command wrapper
- Phase 4C approval queue executor
- Phase 4D Google Sheets sync reliability pass
- Phase 4E dashboard operations view
- Phase 4F OpenClaw/Airo queue-first instruction update
- Phase 4G handoff and release tag

Next status:
Stable checkpoint. Do not start Phase 5 without creating an official Phase 5 roadmap first.


## Official Next Roadmap After Phase 4

Phase 5 roadmap has been created as the next official roadmap after Phase 4.

Roadmap file:
docs/personal-workflow/phase-5/AIRO_PHASE_5_ROADMAP.md

Next execution item:
Phase 5A Live-State Review.


## Official Phase 5 Completion

Airo Personal Workflow Phase 5 is complete.

Phase 5 handoff:
docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_PHASE_5_HANDOFF.md

Phase 5 release tag:
airo-personal-workflow-phase-5-complete

Completed Phase 5 roadmap:
- Phase 5A live-state review
- Phase 5B approved Google Sheets queue execution
- Phase 5C receipt review to approved transaction proposal
- Phase 5D approved transaction write executor
- Phase 5E dashboard daily ops polish
- Phase 5F Google API fallback strategy
- Phase 5G handoff and release tag

Next status:
Stable checkpoint. Do not start Phase 6 without creating an official Phase 6 roadmap first.


## Official Next Roadmap After Phase 5

Phase 6 roadmap has been created as the next official roadmap after Phase 5.

Roadmap file:
docs/personal-workflow/phase-6/AIRO_PHASE_6_ROADMAP.md

Next execution item:
Phase 6A Seamless Readiness Review.

## Rule For Future AI Chats

When continuing this project, the assistant should:

1. Read this index first.
2. Read the latest handoff doc.
3. Check the current branch and git status.
4. Confirm the official next roadmap item.
5. Give one paste-safe command per milestone.
6. Smoke test before commit.
7. Commit and push only after PASS.
8. Never invent phases or touch restricted systems without approval.

## Validation Log

PASS - inside git repo
PASS - branch main
PASS - airo-workflow available
PASS - found docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_V0_1_HANDOFF.md
PASS - found docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_PHASE_2_HANDOFF.md
PASS - found docs/personal-workflow/phase-2/AIRO_PHASE_2A_HEALTH_CHECK.md
PASS - found docs/personal-workflow/phase-2/AIRO_PHASE_2B_ROUTING_CONTRACT.md
PASS - found docs/personal-workflow/phase-2/AIRO_PHASE_2C_SQLITE_RECONCILE.md
PASS - found docs/personal-workflow/phase-2/AIRO_PHASE_2D_GOOGLE_OAUTH_BOOTSTRAP.md
PASS - found docs/personal-workflow/phase-2/AIRO_PHASE_2E_GOOGLE_SHEETS_APPROVAL_GATE.md
PASS - found docs/personal-workflow/phase-2/AIRO_PHASE_2F_ATTACHMENT_INTAKE.md
PASS - found docs/personal-workflow/phase-2/AIRO_PHASE_2G_LOCAL_DASHBOARD_APPROVAL_QUEUE.md

## New Chat Continuity

Use these files to continue smoothly in a new chat:

- docs/personal-workflow/AIRO_CONTINUITY_PACK.md
- docs/personal-workflow/AIRO_NEW_CHAT_BOOTSTRAP_TEMPLATE.md
- docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_PHASE_5_HANDOFF.md

Rule:
A new assistant must read the index, continuity pack, and latest handoff before giving commands.
Do not invent phases.
Do not touch restricted systems.
Use one paste-safe command per milestone.

## Official Phase 6 Completion

Airo Personal Workflow Phase 6 is complete.

Phase 6 handoff:
docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_PHASE_6_HANDOFF.md

Phase 6 release tag:
airo-personal-workflow-phase-6-complete

Completed Phase 6 roadmap:
- Phase 6A seamless readiness review
- Phase 6B local intent router
- Phase 6C approval review CLI
- Phase 6D executor command recommendation
- Phase 6E dashboard next-action upgrade
- Phase 6F OpenClaw/Airo unified router instruction update
- Phase 6G handoff and release tag

Next status:
Stable checkpoint. Do not start Phase 7 without creating an official Phase 7 roadmap first.

## Official Next Roadmap After Phase 6

Phase 7 roadmap has been created as the next official roadmap after Phase 6.

Roadmap file:
docs/personal-workflow/phase-7/AIRO_PHASE_7_ROADMAP.md

Next execution item:
Phase 7A Daily Loop Readiness Review.

Recommended remaining phases:
- Phase 7: seamless daily execution loop
- Phase 8: final hardening, backup/restore, closeout, stable release

## Official Phase 7 Completion

Airo Personal Workflow Phase 7 is complete.

Phase 7 handoff:
docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_PHASE_7_HANDOFF.md

Phase 7 release tag:
airo-personal-workflow-phase-7-complete

Completed Phase 7 roadmap:
- Phase 7A daily loop readiness review
- Phase 7B unified daily command
- Phase 7C router preview integration
- Phase 7D approval review UX polish
- Phase 7E dashboard daily command alignment
- Phase 7F handoff and release tag

Next status:
Stable checkpoint. Recommended next and final practical phase is Phase 8: final hardening, backup/restore, closeout, stable release.
Do not start Phase 8 without creating an official Phase 8 roadmap first.

## Official Next Roadmap After Phase 7

Phase 8 roadmap has been created as the final practical roadmap after Phase 7.

Roadmap file:
docs/personal-workflow/phase-8/AIRO_PHASE_8_ROADMAP.md

Next execution item:
Phase 8A Final System Audit.

Finish target:
Phase 8 is the final practical completion phase for the current Airo Personal Workflow scope.
Do not create Phase 9 unless the user explicitly expands the project scope.

## Official Phase 8 Completion

Airo Personal Workflow Phase 8 is complete.

Phase 8 final handoff:
docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_PHASE_8_HANDOFF.md

Phase 8 final release tag:
airo-personal-workflow-phase-8-complete

Completed Phase 8 roadmap:
- Phase 8A Final System Audit
- Phase 8B Backup and Restore Guide
- Phase 8C Final Smoke Test Suite
- Phase 8D Final Source-of-Truth Refresh
- Phase 8E Final Handoff and Stable Release Tag

Final practical project status:
Airo Personal Workflow is complete for the current personal workflow scope.

Stable verification command:
python3 scripts/personal-workflow/airo_final_smoke.py --text

Next status:
Stable closeout checkpoint. Do not create Phase 9 unless the user explicitly expands the project scope beyond the current Airo Personal Workflow scope.

## Telegram / Notion / OpenClaw Integration Guardrail

A source-of-truth guardrail has been added for Telegram, Notion Life, and OpenClaw collision risk.

Guardrail file:
docs/personal-workflow/integration/AIRO_TELEGRAM_NOTION_OPENCLAW_COLLISION_GUARDRAIL.md

Current default:
- existing Airo/OpenClaw/Bubu Telegram gateway remains the live Telegram front door
- Notion Life / Recent Captures remains the general capture destination
- Airo Personal Workflow remains the local workflow, finance, approval, dashboard, and command layer
- do not create or enable a second live Telegram bot/runner without explicit user approval
- do not patch or restart OpenClaw without explicit user approval

This is a maintenance note, not a new phase.

## Telegram Option A Single Front Door Routing

The user approved Option A for Telegram integration.

Plan:
- use the existing Telegram gateway / Bubu / OpenClaw as the single live Telegram front door
- do not create a second Telegram bot by default
- route personal finance intents to Airo Personal Workflow before Notion capture
- keep general Life OS captures going to Notion Life / Recent Captures
- start with dry-run Airo Workflow routing before any real local execution
- do not patch or restart OpenClaw without explicit approval

Source-of-truth plan:
docs/personal-workflow/integration/AIRO_TELEGRAM_OPTION_A_SINGLE_FRONT_DOOR_PLAN.md

Read-only discovery notes:
docs/personal-workflow/integration/AIRO_TELEGRAM_GATEWAY_DISCOVERY_NOTES.md

This is a scope extension plan, not Phase 9.

## Telegram Option A AGENTS Patch

Option A finance-first routing has been applied to the OpenClaw workspace instruction file.

Patch log:
docs/personal-workflow/integration/AIRO_TELEGRAM_OPTION_A_AGENTS_PATCH_LOG.md

Runtime behavior intended:
- clear personal finance Telegram/OpenClaw messages route to Airo Personal Workflow dry-run before Notion capture
- non-finance captures continue to Notion Life / Recent Captures
- no second Telegram bot is created
- OpenClaw service was not restarted

## Telegram Option A Workspace Precedence Patch

Option A finance-first routing has been applied with top precedence to OpenClaw workspace instruction and Notion skill files.

Patch log:
docs/personal-workflow/integration/AIRO_TELEGRAM_OPTION_A_WORKSPACE_PRECEDENCE_PATCH_LOG.md

Runtime behavior intended:
- clear personal finance Telegram/OpenClaw messages route to Airo Personal Workflow dry-run before Notion capture
- non-finance captures continue to Notion Life / Recent Captures
- no second Telegram bot is created
- OpenClaw service was not restarted

## Telegram Option A Gateway Restart

OpenClaw gateway was restarted to refresh live Telegram routing after Option A finance-first instruction patches.

Restart log:
docs/personal-workflow/integration/AIRO_TELEGRAM_OPTION_A_GATEWAY_RESTART_LOG.md

Next live test:
- finance Telegram message should route to Airo Personal Workflow dry-run / summary
- non-finance capture should continue to Notion Life / Recent Captures

## Telegram Option A Notion Command Guard

A command-level guard has been installed around Notion writer commands so clear finance intents route to Airo Personal Workflow dry-run before any Notion write.

Guard log:
docs/personal-workflow/integration/AIRO_TELEGRAM_OPTION_A_NOTION_COMMAND_GUARD_LOG.md

Runtime behavior intended:
- finance Telegram captures are blocked from Notion writer commands and routed to Airo dry-run
- non-finance captures pass through to Notion normally
- openclaw-gateway.service was restarted after guard install

## Telegram Option A Persistent DB Route

Telegram finance routing now uses real local Airo Workflow execution with an explicit persistent SQLite DB path.

Log:
docs/personal-workflow/integration/AIRO_TELEGRAM_OPTION_A_PERSISTENT_DB_ROUTE_LOG.md

Persistent DB:
/home/egitaristorandas/.local/share/airo-personal-workflow/airo.sqlite3

Runtime behavior intended:
- finance Telegram captures are blocked from Notion writer commands
- finance Telegram captures are recorded by local Airo Personal Workflow into the persistent DB
- non-finance captures pass through to Notion normally
- local DB is runtime data and must not be committed
