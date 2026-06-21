# [architecture][safety] Document EarnsAI project boundaries

## Context
Full WSL scan found multiple EarnsAI areas:
- ~/earnsai-pulse-trading
- ~/earnsai-telegram-gateway
- ~/earnsai-telegram-gateway/trading-research-lab
- ~/.openclaw
- ~/.openclaw/workspace
- ~/AI_AGENT_WORKSPACE
- ~/earnsai-backups
- ~/earnsai-pulse-trading-local-backups

## Goal
Create a clear boundary document so AI work does not mix unrelated subprojects.

## Scope
Documentation only.

## Allowed Changes
- docs/workflow/PROJECT_BOUNDARIES.md
- tasks/open/ISSUE-003-document-project-boundaries.md
- moving completed issues from tasks/open/ to tasks/done/

## Forbidden Changes
- no runtime code changes
- no .env reads
- no secret printing
- no GitHub push
- no live trading
- no Notion real write
- no OpenClaw patching

## Commands to Validate
- make ci-safe
- git status --short

## Acceptance Criteria
- project boundary table exists
- risk per area is documented
- Notion and trading are clearly separated
- OpenClaw/Airo is marked as sensitive
- make ci-safe PASS
