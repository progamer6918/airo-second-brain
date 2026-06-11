---
last_updated: 2026-06-11
updated_by: owner-confirmed-design
status: current
confidence: owner-confirmed
source: chat-derived
---

# Repository Registry

This file is the central registry for repositories and knowledge sources that belong to, support, or inform the AIRO ecosystem.

AIRO Second Brain is the canonical knowledge hub. Other repositories may contain implementation, experiments, tools, skills, automations, or reference material, but durable knowledge should be summarized or linked from this repo so future AIRO operators do not depend on scattered context.

## Core Rule

Do not treat external repositories, past chats, or model memory as canonical unless they are represented in AIRO Second Brain.

When important knowledge exists outside this repo, convert it into one of these forms:

- a project file under `projects/`
- a system file under `systems/`
- an agent/operator rule under `AGENTS.md`
- durable context under `CONTEXT.md`
- active status under `CURRENT.md`

## Core Hub

| Repository | Role | Status | Notes |
|---|---|---|---|
| `progamer6918/airo-second-brain` | Canonical AIRO knowledge hub | Active | Start from `BOOT.md`, then follow the startup sequence. |

## AIRO Ecosystem Repositories

| Repository | Role | Status | Notes |
|---|---|---|---|
| `progamer6918/airo-finance` | AIRO Finance implementation/project repo | Active / registered | AIRO Finance is one project inside the broader AIRO ecosystem, not the whole ecosystem. |
| `progamer6918/vortex-ai-skill-lab` | AI skills, experiments, and reusable capability lab | Registered | Important skills should be summarized into AIRO Second Brain before being treated as durable operator knowledge. |

## EarnsAI / Trading Repositories

| Repository | Role | Status | Notes |
|---|---|---|---|
| `progamer6918/earnai-pulse-trading` | Trading system / pulse trading workstream | Registered | Needs project context capture before future operators rely on it. |
| `progamer6918/earnai-telegram-gateway` | Telegram gateway / integration workstream | Registered | Needs architecture and operational notes captured if active. |
| `progamer6918/earnai-trading-research-lab` | Trading research and experimentation workstream | Registered | Research conclusions should be distilled into AIRO Second Brain. |
| `progamer6918/earnai-notion-agent-os` | Notion agent operating system / workflow automation | Registered | Needs workflow and agent behavior mapping if still active. |

## Reference / Learning Repositories

These repositories are useful as learning or reference sources, but they are not canonical AIRO memory by themselves.

| Repository | Role | Status | Notes |
|---|---|---|---|
| `progamer6918/the-art-of-command-line` | Command line learning/reference | Reference | Use as supporting material only. |
| `progamer6918/developer-roadmap` | Developer learning roadmap/reference | Reference | Use as supporting material only. |
| `progamer6918/build-your-own-x` | Engineering learning/reference | Reference | Use as supporting material only. |

## Knowledge Capture Policy

For every active repository, AIRO Second Brain should eventually contain:

- what the repository is for
- whether it is active, paused, archived, or reference-only
- where its canonical project context lives
- the current next step
- constraints, risks, and important decisions
- how a new AI operator should continue the work without guessing

## Recommended Mapping

Current recommended mapping:

| Workstream | Canonical AIRO file |
|---|---|
| AIRO ecosystem overview | `CURRENT.md`, `CONTEXT.md`, `AGENTS.md`, `systems/repository-registry.md` |
| Report Automation VBA | `projects/report-automation-vba.md` |
| AIRO Finance | `projects/airo-finance.md` or existing finance project file |
| Vortex AI Skill Lab | `projects/vortex-ai-skill-lab.md` or `systems/skills-registry.md` |
| EarnsAI / trading workstreams | dedicated project files under `projects/` after owner confirmation |

## Cleanup Rule

Do not create one project file per chat, one per bug, or one per small experiment.

Create one project file per durable workstream.

When a workstream grows too large for one file, promote it from:

```text
projects/example-workstream.md
to:

projects/example-workstream/
├── README.md
├── decisions.md
├── runbook.md
└── session-closeouts.md
Current Next Step

Capture the active Report Automation VBA project in:

projects/report-automation-vba.md

Then add a short pointer in:

CURRENT.md
