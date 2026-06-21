# AIRO Personal Workflow Continuity Pack

Generated: 2026-05-09T19:53:35+0700
Repository: progamer6918/vortex-ai-skill-lab
Branch: main
Commit when generated: ffaa237

## Current Stable Checkpoint

Completed:
- MVP v0.1
- Phase 2
- Phase 3
- Phase 4
- Phase 5
- Phase 6
- Phase 7
- Phase 8 roadmap
- Phase 8A Final System Audit
- Phase 8B Backup and Restore Guide
- Phase 8C Final Smoke Test Suite
- Phase 8D Final Source-of-Truth Refresh
- Phase 8E Final Handoff and Stable Release Tag

Latest handoff:
docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_PHASE_8_HANDOFF.md

Latest release tag:
airo-personal-workflow-phase-8-complete

Final project status:
- Airo Personal Workflow is complete for the current personal workflow scope.
- Final release tag: airo-personal-workflow-phase-8-complete
- Final handoff: docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_PHASE_8_HANDOFF.md
- Stable verification command: python3 scripts/personal-workflow/airo_final_smoke.py --text
- Do not create Phase 9 unless the user explicitly expands the project scope.

## Source Of Truth

Read in this order:
1. docs/personal-workflow/AIRO_PROJECT_INDEX.md
2. docs/personal-workflow/AIRO_CHAT_RULES.md
3. docs/personal-workflow/AIRO_CONTINUITY_PACK.md
4. docs/personal-workflow/AIRO_NEW_CHAT_BOOTSTRAP_TEMPLATE.md
5. docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_PHASE_7_HANDOFF.md
6. docs/personal-workflow/phase-8/AIRO_PHASE_8_ROADMAP.md
7. docs/personal-workflow/phase-8/AIRO_PHASE_8A_FINAL_SYSTEM_AUDIT.md
8. docs/personal-workflow/phase-8/AIRO_PHASE_8B_BACKUP_RESTORE_GUIDE.md
9. docs/personal-workflow/phase-8/AIRO_PHASE_8C_FINAL_SMOKE_TEST_SUITE.md

## Most Important Commands

- python3 scripts/personal-workflow/airo_final_smoke.py --text
- python3 scripts/personal-workflow/airo_final_smoke.py --json

- ./bin/airo-daily --text
- ./bin/airo-daily
- ./bin/airo-dashboard-align
- python3 scripts/personal-workflow/airo_intent_router.py "<message>"
- python3 scripts/personal-workflow/airo_approval_review.py list --status pending --compact
- python3 scripts/personal-workflow/airo_approval_review.py inspect --id "<queue_id>"
- python3 scripts/personal-workflow/airo_executor_recommend.py recommend --id "<queue_id>"
- python3 scripts/personal-workflow/airo_ops_dashboard.py

## Safety Boundaries

Always active:
- do not read secrets, tokens, cookies, sessions, passwords, or .env files
- do not access browser profiles
- do not commit local DBs, receipts, OAuth tokens, or credentials
- do not perform real Google write without approval gate
- do not patch OpenClaw core without approval
- do not restart OpenClaw service without approval
- do not touch EarnsAI trading runtime unless explicitly requested
- do not enable live trading
- do not hard-delete finance records

## Next Rule

Do not start Phase 8 without creating an official Phase 8 roadmap first.

## Integration Collision Guardrail

Read this before changing Telegram, Notion, or OpenClaw integration:

- docs/personal-workflow/integration/AIRO_TELEGRAM_NOTION_OPENCLAW_COLLISION_GUARDRAIL.md

Default rule:
Do not create or enable a second live Telegram runner for Airo Personal Workflow. The existing Airo/OpenClaw/Bubu Telegram gateway is the live Telegram front door unless the user explicitly approves a new integration design.

## Telegram Option A Routing Plan

The user approved Option A: use the existing Telegram gateway / Bubu / OpenClaw as the single live Telegram front door.

Read before Telegram/Notion/OpenClaw integration work:
- docs/personal-workflow/integration/AIRO_TELEGRAM_OPTION_A_SINGLE_FRONT_DOOR_PLAN.md
- docs/personal-workflow/integration/AIRO_TELEGRAM_GATEWAY_DISCOVERY_NOTES.md

Default rule:
Do not create a second live Telegram bot. Route finance intents through the existing gateway to Airo Personal Workflow, starting with dry-run behavior, and keep general captures going to Notion Life.

## Telegram Option A AGENTS Patch Applied

OpenClaw workspace instruction now contains a finance-first exception before Notion Recent Captures rules.

Patch log:
- docs/personal-workflow/integration/AIRO_TELEGRAM_OPTION_A_AGENTS_PATCH_LOG.md

Default test:
Send a clear finance message through Telegram and verify it routes to Airo Workflow dry-run instead of Notion Recent Captures.

Do not restart OpenClaw unless explicitly approved.

## Telegram Option A Workspace Precedence Patch Applied

OpenClaw workspace instruction and Notion skill files now contain finance-first exceptions with top precedence before Notion Recent Captures rules.

Patch log:
- docs/personal-workflow/integration/AIRO_TELEGRAM_OPTION_A_WORKSPACE_PRECEDENCE_PATCH_LOG.md

Default live test:
Send a clear finance message through Telegram and verify it routes to Airo Workflow dry-run instead of Notion Recent Captures.

If Telegram still routes to Notion, do not keep patching blindly. The likely next step is OpenClaw gateway/session refresh or service restart, which requires explicit user approval.

## Telegram Option A Gateway Restart Applied

OpenClaw gateway was restarted after Option A finance-first instruction patches.

Restart log:
- docs/personal-workflow/integration/AIRO_TELEGRAM_OPTION_A_GATEWAY_RESTART_LOG.md

Next live test:
Send clear finance and non-finance Telegram messages and compare routing.

## Telegram Option A Notion Command Guard Installed

Command-level guard installed for Notion writer commands.

Guard log:
- docs/personal-workflow/integration/AIRO_TELEGRAM_OPTION_A_NOTION_COMMAND_GUARD_LOG.md

Default live test:
Send clear finance Telegram message and verify it no longer creates a real Notion Recent Captures write.

If gateway wording still says Recent Captures, verify whether the URL is real and whether the guard JSON is surfaced; the guard blocks the Notion writer command for detected finance intents.

## Telegram Option A Persistent DB Route Applied

Telegram finance routing now uses real local Airo Workflow execution with explicit persistent DB path.

Log:
- docs/personal-workflow/integration/AIRO_TELEGRAM_OPTION_A_PERSISTENT_DB_ROUTE_LOG.md

Persistent DB:
- /home/egitaristorandas/.local/share/airo-personal-workflow/airo.sqlite3

Default live test:
Send clear finance Telegram message and verify no Notion URL appears. Then inspect marker/recent rows in the persistent local Airo DB.

Do not commit local DB data.
