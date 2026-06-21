# AIRO Telegram Option A AGENTS Patch Log

Generated: 2026-05-09 13:41:20 UTC
Repository: progamer6918/vortex-ai-skill-lab
Branch: main

Status:
APPLIED WITHOUT SERVICE RESTART

## Purpose

Apply the Option A single-front-door routing design to the OpenClaw workspace instruction file.

This patch adds a finance-first exception before Notion Recent Captures / Telegram quick capture rules.

## Patched File

OpenClaw workspace instruction:

    /home/egitaristorandas/.openclaw/workspace/AGENTS.md

Backup created:

    /home/egitaristorandas/.openclaw/workspace/AGENTS.md.bak-airo-option-a-20260509-204120

## Inserted Rule

Inserted or verified section:

    AIRO OPTION A FINANCE-FIRST TELEGRAM ROUTING v2026-05-09

## Behavior Change

For clear personal finance Telegram/OpenClaw messages:

1. Do not call notion-life-recent first.
2. Do not call notion-life-add first.
3. Route to Airo Personal Workflow dry-run:

       AIRO_WORKFLOW_MODE=dry-run airo-workflow "<original Telegram message>"

4. Reply with short Airo Workflow result summary.
5. If blocked/sensitive/approval-required, follow the Airo safety result and do not route to Notion as fallback.

For non-finance captures:

- continue existing Notion Life / Recent Captures routing behavior.

## Safety Boundaries

This patch did not:

- read Telegram or Notion tokens
- read .env files
- read browser profiles, cookies, sessions, or credentials
- start a live bot
- create a second Telegram bot
- restart OpenClaw
- patch OpenClaw core package
- perform real Notion or Google writes
- touch EarnsAI, runtime, or trading paths
- enable live trading

## Validation

Validation performed:

- source-of-truth docs read
- Option A plan confirmed with flexible wording validation
- AGENTS.md backup created if block was newly inserted
- finance-first block inserted or verified before Notion capture-first rules
- Airo final smoke test passed
- Telegram local handler smoke passed
- airo-workflow dry-run JSON passed

## Rollback

To rollback manually if needed:

    cp "/home/egitaristorandas/.openclaw/workspace/AGENTS.md.bak-airo-option-a-20260509-204120" "/home/egitaristorandas/.openclaw/workspace/AGENTS.md"

Do not restart OpenClaw unless explicitly approved.
