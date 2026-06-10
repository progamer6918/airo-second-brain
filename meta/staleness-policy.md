
last_updated: 2026-06-10
updated_by: owner-confirmed-design
status: current
confidence: owner-confirmed
source: chat-derived
AIRO Second Brain Staleness Policy

Every canonical file should include metadata:

---
last_updated: YYYY-MM-DD
updated_by: owner | agent | owner-confirmed-design
status: current | stale-risk | planned | archived
confidence: verified | owner-confirmed | assumed | unknown
source: repo-derived | live-verified | chat-derived | owner-confirmed | mixed
---
Stale Thresholds
File / Folder	Stale After
CURRENT.md	14 days
state/active-context.md	7 days
projects/*.md	30 days
systems/*.md	60 days
agents/*.md	60 days
identity/*	never auto-stale
decisions/decision-log.md	never auto-stale
SECURITY.md	90 days or whenever tooling changes
AGENTS.md	60 days or whenever workflow changes
Agent Rule

If a file is stale:

Flag it to owner.
Do not silently trust it as current.
Prefer canonical project repo or live evidence when available.
Ask for or perform a current-state refresh if execution depends on it.
Confidence Meaning
verified

Use only when supported by live runtime proof, repo state, commit evidence, readback, or direct source evidence.

owner-confirmed

Use when the owner explicitly confirmed the concept/decision in conversation.

assumed

Use when inferred but not directly verified.

unknown

Use when the agent cannot establish confidence.
