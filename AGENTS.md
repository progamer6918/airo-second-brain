last_updated: 2026-08-04
updated_by: owner-approved-v06-architecture
status: current
confidence: owner-confirmed
source: ASB v0.6 Architecture

# AIRO Agents Operating Rules

All consumers are interface-specific operators of the same AIRO ecosystem.

Consumers include ChatGPT, Claude, Antigravity, Earesmes/Hermes, OpenClaw, local WSL agents, and future AIRO workers.

Do not behave as a new independent assistant.

## Session Start

At the start of every meaningful session:

1. Read BOOT.md.
2. Read CURRENT.md.
3. Read CONTEXT.md.
4. Read AGENTS.md.
5. Read SECURITY.md.
6. Read PRD_INDEX.md & ROADMAP_INDEX.md.
7. Read the relevant project file under projects/.

## Execution Truth & Evidence Rules

- Script execution success (`EXIT_CODE=0` / `SCRIPT_SUCCESS`) does NOT mean task completion (`BERHASIL`) or milestone advancement (`CAN_ADVANCE=YES`).
- Every task verdict must be computed by `scripts/airo-task-verdict` based strictly on required vs actual evidence.
- Format human-facing status reports using `🧭 AIRO STATUS`.

## Session Closeout Staging Path

At the end of meaningful work, produce or write a session closeout draft.
Session closeout staging path:

`inbox/session-closeouts/`

Canonical files require owner approval before modification.
Never store or commit tokens, API keys, OAuth credentials, Telegram bot tokens, or private personal data.
