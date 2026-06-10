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
