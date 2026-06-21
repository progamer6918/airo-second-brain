last_updated: 2026-06-10
updated_by: owner-confirmed-design
status: current
confidence: owner-confirmed
source: chat-derived
Project: Earesmes / Hermes
Summary

Earesmes is the primary AI assistant persona intended to run on Hermes, a local Python/WSL agent accessed through Telegram.

Earesmes is the main local operator node of the AIRO ecosystem.

Role in AIRO Ecosystem

Earesmes/Hermes should eventually:

read AIRO Second Brain at session start
act as owner-facing local assistant
interact through Telegram
access approved local AI workspaces
help coordinate project handoffs
write session closeouts to AIRO Second Brain when configured
Canonical Technical Location

Technical implementation details should live in the Hermes/local WSL workspace.

Do not duplicate sensitive infrastructure details here.

This file is a project pointer and summary, not a secret store.

Current Status

Owner-confirmed status:

Hermes/Earesmes is part of the AIRO ecosystem direction.
WSL/local agent setup is relevant.
Google Workspace integration may exist locally.
Session start/end protocol is pending implementation.

Do not assume live runtime status from this file.

Before execution, inspect the actual Hermes/local repo or workspace specified by owner.

Read Also
systems/infrastructure.md
systems/interfaces.md
agents/earesmes.md
agents/design-principles.md
AGENTS.md

SECURITY.md

## 2026-06-18 — Earesmes Gateway Durability Accepted

- verified: Earesmes is the owner-facing personal AI, chief of staff, primary
  AIRO orchestrator, and resident AIRO Sync persona.
- verified: Hermes is the local runtime, not a competing persona.
- verified: Telegram natural-language bridge is live at commit `cb7bbea`.
- verified: canonical ASB context hydration is live at commit `8959193`.
- verified: `telegram-gateway.py` remains the single `getUpdates` owner.
- verified: Windows Scheduled Task
  `AIRO Earesmes Telegram Listener` retains the logon trigger and now has one
  PT5M recurring trigger with `MultipleInstances=IgnoreNew`.
- verified: controlled gateway termination automatically recovered from PID
  `18992` to PID `20505`.
- verified: worker PID `18482` remained active and unchanged.
- verified: no legacy poller or second Hermes Telegram poller was active.
- accepted: gateway durability PASS.
- open: end-to-end response latency has not yet been traced or optimized.
- evidence:
  `docs/validation/AIRO_EARESMES_GATEWAY_DURABILITY_20260618.md`.
- next: PRD v0.5.1 Phase 0A READ_ONLY_AUDIT.
