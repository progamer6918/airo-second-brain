# AIRO Telegram / Notion / OpenClaw Collision Guardrail

Generated: 2026-05-09 13:18:39 UTC
Repository: progamer6918/vortex-ai-skill-lab
Branch: main

Status:
SOURCE-OF-TRUTH MAINTENANCE NOTE

## Purpose

Document the integration boundary discovered after Airo Personal Workflow Phase 8 completion.

The user confirmed that Telegram messages are already connected to an active Airo/OpenClaw gateway that captures into Notion Life / Recent Captures.

This means Airo Personal Workflow must not add or activate a second live Telegram listener without an explicit new integration design.

## Current Observed Architecture

Current live path, based on user-provided Telegram output:

    Telegram message
      -> existing Airo/OpenClaw Telegram gateway
      -> Notion Life / Recent Captures

Current Airo Personal Workflow path, based on tracked repo and local smoke tests:

    Local Telegram-style text
      -> airo_personal_workflow.telegram.local_handler.handle_telegram_text()
      -> local workflow parser / SQLite test DB / dry-run Google plan

The local Telegram handler is smoke-testable, but it is not a tracked live Telegram polling or webhook runner.

## Collision Risk

Do not run two independent Telegram consumers for the same chat unless explicitly designed.

Risks:

- duplicate capture into Notion and local SQLite
- ambiguous routing between Notion Life capture and personal finance workflow
- split state across Notion and Airo Personal Workflow
- inconsistent approval behavior
- accidental writes outside the intended approval model
- user confusion when Telegram confirms Notion capture while local finance workflow is separate

## Guardrail

Default behavior:

- Treat the existing Airo/OpenClaw/Bubu Telegram gateway as the live Telegram front door.
- Treat Airo Personal Workflow as the local workflow, command, router, approval, dashboard, and finance layer.
- Do not create or enable a second live Telegram bot/runner for Airo Personal Workflow by default.
- Do not start polling or webhook services from this repo without explicit user approval.
- Do not read, print, or commit Telegram or Notion tokens.
- Do not read .env files or browser/session credentials.
- Do not patch or restart OpenClaw without explicit approval.

## Preferred Future Integration Pattern

If the user wants Telegram to trigger Airo Personal Workflow, prefer one of these explicitly approved designs:

1. Existing gateway routes personal finance intents to:

       airo-workflow "<original user message>"

2. Existing gateway routes personal finance intents to dry-run first:

       AIRO_WORKFLOW_MODE=dry-run airo-workflow "<original user message>"

3. Existing gateway sends finance-intent captures to an approval queue before any real external write.

4. Notion Life remains the default destination for general life notes, journal-like captures, and non-finance inbox items.

## Routing Ownership

Suggested ownership:

- General capture, notes, memory, Life OS:
  Existing Bubu / Airo / OpenClaw Telegram gateway -> Notion Life / Recent Captures

- Personal finance capture and review:
  Airo Personal Workflow -> local parser, SQLite, approval queue, dashboard, Google dry-run or approved write path

- Sensitive actions:
  approval queue and explicit confirmation only

- Live trading:
  always blocked for this project scope

## Safe Test Commands

Local Airo Personal Workflow smoke:

    python3 scripts/personal-workflow/airo_final_smoke.py --text

Local Telegram-style handler smoke:

    AIRO_WORKFLOW_MODE=dry-run python3 scripts/personal_workflow_telegram_smoke.py

Read-only integration discovery:

    git ls-files | grep -Ei 'telegram|notion|openclaw|life|gateway|router|workflow|approval|queue'

## Non-Goals

This guardrail does not:

- enable a live Telegram bot
- configure Telegram tokens
- configure Notion tokens
- patch OpenClaw
- restart OpenClaw
- perform real Google or Notion writes
- create Phase 9

## Final Decision

Airo Personal Workflow remains complete for the current scope.

Telegram/Notion/OpenClaw live integration changes are a separate scope extension and require explicit user approval before implementation.
