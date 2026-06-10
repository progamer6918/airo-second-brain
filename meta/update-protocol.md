
last_updated: 2026-06-10
updated_by: owner-confirmed-design
status: current
confidence: owner-confirmed
source: chat-derived
AIRO Second Brain Update Protocol

This protocol controls how AIRO Second Brain is updated.

Update Layers
Layer 1 — Auto-capturable

May be written automatically by configured local consumers:

inbox/[consumer]-[YYYY-MM-DD]-[HHMM].md

May be appended automatically:

state/active-context.md
meta/changelog.md
decisions/pending-decisions.md

Rules:

Append-only preferred.
No secrets.
No raw transcripts.
No full email bodies.
No credential/token contents.
No canonical rewrite.
Layer 2 — Approval-gated canonical files

Require owner approval before modification:

CURRENT.md
CONTEXT.md
AGENTS.md
SECURITY.md
identity/*
systems/*
agents/*
projects/*
decisions/decision-log.md
meta/update-protocol.md
meta/staleness-policy.md

Rules:

Agent may propose updates.
Owner approves before write/commit.
Do not silently rewrite.
Layer 3 — Project canonical repos

Project-specific execution truth remains in the relevant project repo.

Example:

AIRO Finance canonical status lives in:

vortex-ai-skill-lab/docs/AIRO_FINANCE_PRD_LIVING.md
vortex-ai-skill-lab/docs/AIRO_FINANCE_CURRENT_STATE.md
vortex-ai-skill-lab/docs/airo-finance/records/

AIRO Second Brain may point to project truth, but must not replace it.

Distillation Trigger

Run distillation when:

14+ days since last CURRENT.md update; or
a major milestone is completed; or
inbox grows too large; or
owner explicitly asks for "distill Second Brain"; or
a consumer notices stale context.

Distillation means:

Read relevant inbox/session closeouts.
Summarize important changes.
Propose updates to canonical files.
Owner approves.
Apply canonical updates.
Append meta/changelog.md.
Session Closeout Requirement

Every meaningful session should end with a closeout containing project/topic, summary, decisions, pending decisions, files/repos touched, evidence/tests/readbacks, blockers/risks, and next action.

Auto-Commit Policy

Auto-commit is not universal.

Allowed only when:

Consumer runs in a configured local environment.
Git identity is configured.
No secret files are staged.
Only allowed append-only files are staged.
Owner has approved that consumer for auto-commit.

Default for ChatGPT/Claude web:

produce closeout text only
do not claim repo write

Default for Hermes/Earesmes local:

may write closeout locally if configured
may commit only after owner allows auto-commit

Default for Antigravity:

may patch requested files during explicit execution task
must report changed files and validation

must not push unless owner asks
