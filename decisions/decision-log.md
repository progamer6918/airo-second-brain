
last_updated: 2026-06-10
updated_by: owner-confirmed-design
status: current
confidence: owner-confirmed
source: chat-derived
AIRO Decision Log

Final decisions only. Do not write uncertain items here.

Pending or unresolved decisions belong in decisions/pending-decisions.md.

2026-06-10 — AIRO Brand Scope

Decision:

AIRO is the umbrella ecosystem brand.
AIRO Finance is one project inside the wider AIRO ecosystem.

Evidence:

Owner confirmed explicitly.

Superseded by:

—
2026-06-10 — Second Brain Architecture

Decision:

AIRO Second Brain will be the shared canonical knowledge base / AIRO Kernel.
It should support multiple consumers: ChatGPT, Claude, Hermes, Antigravity, OpenClaw, and local agents.
It should use a router-based structure, not a single giant file.

Evidence:

Owner approved the shared-brain direction.

Superseded by:

—
2026-06-10 — Raw Chat Policy

Decision:

Raw chat history is relevant as source material.
Raw chat should not be stored as default canonical context.
Important chats should be distilled into decisions, worklogs, lessons, and project summaries.

Evidence:

Owner asked to preserve cross-consumer context without bloating the default brain.

Superseded by:

—
2026-06-10 — Cross-Consumer Operator Model

Decision:

All AIRO consumers are interface-specific operators of the same AIRO ecosystem.
They should not behave as separate independent assistants.
Each consumer should load AIRO Second Brain at session start and produce closeout at session end.

Evidence:

Owner wants interaction to feel like one consistent assistant across tools.

Superseded by:

—
2026-06-10 — Auto-Write / Auto-Commit Policy

Decision:

Inbox/state/changelog append-only updates may be automated when configured.
Canonical files require owner approval.
Auto-commit is allowed only for configured local consumers with git access and only for non-canonical append-only updates.

Evidence:

Owner wants less manual logging but still needs safe canonical control.

Superseded by:

—
