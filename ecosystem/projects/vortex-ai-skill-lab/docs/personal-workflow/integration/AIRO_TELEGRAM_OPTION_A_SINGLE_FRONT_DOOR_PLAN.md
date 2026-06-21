# AIRO Telegram Option A — Single Front Door Routing Plan

Generated: 2026-05-09 13:29:27 UTC
Repository: progamer6918/vortex-ai-skill-lab
Branch: main

Status:
SOURCE-OF-TRUTH SCOPE EXTENSION PLAN

## User Decision

The user approved Option A:

Use the existing Telegram gateway as the single live Telegram front door.

Do not create a second Telegram bot by default.

## Current Situation

The live Telegram path already exists outside the local Airo Personal Workflow Telegram smoke handler.

Observed live behavior from the user:

    Telegram message
      -> Airo/OpenClaw/Bubu gateway
      -> Notion Life / Recent Captures

Tracked Airo Personal Workflow behavior:

    local text
      -> airo_personal_workflow.telegram.local_handler.handle_telegram_text()
      -> local workflow parser / SQLite / dry-run Google plan

The tracked repo does not currently expose a live Telegram polling or webhook runner for Airo Personal Workflow.

## Problem

If Airo Personal Workflow creates a second live Telegram listener, the same user message can be captured twice:

- once by the existing gateway into Notion Life
- once by Airo Personal Workflow into local finance workflow

This causes duplicate capture, ambiguous ownership, split state, and inconsistent approval behavior.

## Target Architecture

There must be one Telegram front door:

    Telegram
      -> existing Telegram gateway / Bubu / OpenClaw
          -> routing decision
              -> OpenClaw command/status handler
              -> Notion Life / Recent Captures for general capture
              -> Airo Personal Workflow for finance workflow
              -> approval/block for sensitive actions

## Routing Ownership

General capture:

    Existing gateway -> Notion Life / Recent Captures

Examples:
- notes
- memories
- life inbox
- ideas
- general reminders that belong in Life OS

Personal finance:

    Existing gateway -> Airo Personal Workflow

Examples:
- catat beli makan 50k pakai tokopedia credit card
- bayar cicilan rumah 2500000
- cek cicilan rumah sudah bayar ke berapa
- ringkasan bulan ini

Command/status:

    Existing gateway -> existing OpenClaw/Airo command handler

Examples:
- /status
- /report
- /readiness

Sensitive actions:

    Existing gateway -> block or approval queue

Examples:
- real Google writes
- deletion
- trading
- OpenClaw runtime changes
- any credential/token action

## Initial Rollout Mode

Start with dry-run routing for Telegram finance intents:

    AIRO_WORKFLOW_MODE=dry-run airo-workflow "<original user message>"

This avoids accidental duplicate real writes while testing the live gateway route.

After dry-run routing is proven stable, low-risk finance capture may be promoted to real local execution only with explicit user approval:

    airo-workflow "<original user message>"

External writes still require approval gates.

## Router Rule

The existing gateway should decide before sending to Notion.

Pseudo-flow:

1. Receive Telegram message.
2. If message is an existing command such as /status, use existing command handler.
3. Else classify whether it is a personal finance workflow intent.
4. If finance intent, call Airo Personal Workflow dry-run and reply with the result.
5. If not finance, continue existing Notion Life capture flow.
6. If blocked/sensitive, do not execute and reply with the safety reason.

## Important Guardrails

- Do not create or enable a second live Telegram bot/runner by default.
- Do not patch or restart OpenClaw without explicit approval.
- Do not read, print, or commit Telegram/Notion tokens.
- Do not read .env files, browser profiles, cookies, sessions, or credentials.
- Do not perform real Notion or Google writes from discovery commands.
- Do not enable live trading.
- Do not touch EarnsAI trading runtime.
- Do not hard-delete finance records.
- Do not commit local DBs, receipts, OAuth tokens, credentials, or runtime state.

## Implementation Sequence

Step A1:
Document this plan and perform read-only gateway discovery.

Step A2:
Identify the exact live Telegram gateway file or service that currently routes to Notion.

Step A3:
Create a patch proposal against that exact target.

Step A4:
Add dry-run finance routing before Notion capture.

Step A5:
Test Telegram messages end-to-end.

Step A6:
Only after explicit approval, decide whether low-risk finance capture can run real local {"ok":false,"error":"empty_input","message":"No text provided"}.

## Non-Goals

This plan does not:

- create Phase 9
- start a live Telegram bot
- create a second Telegram bot
- configure tokens
- patch OpenClaw runtime
- restart any service
- perform real Notion or Google writes

## Current Decision

Proceed with Option A in stages.

The next runtime step after this source-of-truth plan is read-only gateway target discovery, followed by an explicit patch proposal.
