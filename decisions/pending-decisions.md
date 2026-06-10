
last_updated: 2026-06-10
updated_by: owner-confirmed-design
status: current
confidence: owner-confirmed
source: chat-derived
Pending Decisions

Unresolved or deferred decisions only.

Do not duplicate this file under state/.

Open
Distillation automation trigger

Status:

Deferred to Phase 2.

Question:

Should distillation be manually triggered by owner or automatically suggested by Hermes/Earesmes?

Default safe answer:

Manual trigger first.
Automation may suggest, not directly rewrite canonical files.
Concurrent consumer lock mechanism

Status:

Deferred to Phase 2.

Question:

How should AIRO handle multiple consumers updating the repo at the same time?

Default safe answer:

Use append-only inbox files per consumer/session first.
Avoid simultaneous edits to canonical files.
Add merge/lock script later.
Hermes session-start hook

Status:

Deferred to Phase 2.

Question:

How should Hermes/Earesmes automatically load BOOT.md at session start?

Default safe answer:

Add a local startup routine that reads BOOT.md, CURRENT.md, CONTEXT.md, AGENTS.md, and SECURITY.md.
