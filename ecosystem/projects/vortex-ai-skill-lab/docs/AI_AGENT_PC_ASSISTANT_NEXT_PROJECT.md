# AI Agent PC Assistant — Next Project Direction

Last updated: 2026-05-07

## Context

The user wants to mature the existing AI agent ecosystem into a real personal PC assistant that can operate the user's PC safely.

Existing ecosystem:

- EarnsAI Pulse Trading
- Vortex AI Skill Lab
- OpenClaw / Airo
- Bubu the Receptionist
- Telegram control/reporting workflows

## Completed Relevant Work

### EarnsAI Pulse Trading

Local paper-only dry-run MVP is operational.

Validated capabilities:

- paper runtime runs in tmux
- Telegram periodic report works
- Telegram control bot works
- allowed Telegram commands include /status, /report, /tail, /start, /stop, /readiness, /maintenance
- dangerous commands remain blocked
- runtime remains PAPER_ONLY
- live trading remains locked

### Vortex AI Skill Lab

Created as the central cross-project skill library.

Initial references:

- build-your-own-x
- developer-roadmap
- the-art-of-command-line

Purpose:

- convert useful GitHub repos into skill cards, playbooks, templates, and reusable agent workflows
- do not inject raw external repos directly into production projects

### OpenClaw / Airo

Airo/OpenClaw browser-control issue was diagnosed and fixed locally.

Findings:

- Chrome was installed and functional
- headless Chrome test worked
- OpenClaw gateway had previously lacked full GUI env
- DISPLAY and WAYLAND_DISPLAY were restored into the service environment
- OpenClaw browser config was restored to visible browser mode
- browser.enabled=true
- browser.headless=false
- browser.noSandbox=true
- Gateway health returned ok=true
- browser server was listening
- Airo browser interaction worked again after repair/session recovery

## Next Project Goal

Build a safe PC-operating AI assistant layer.

Working title:

AIRO PC Operator Layer

Goal:

Make the AI agent capable of operating the user's PC like a real personal assistant while preserving strict safety boundaries.

## Core Capabilities Wanted

1. Open apps or browser pages safely
2. Search the web using browser tool
3. Operate Telegram workflows
4. Manage local project repos
5. Run safe terminal commands
6. Start/stop/check local services
7. Summarize files and logs
8. Maintain project carry-over and next actions
9. Use skill library from Vortex AI Skill Lab
10. Ask for confirmation before risky actions

## Safety Rules

Never allow autonomous unsafe execution.

Always block or require explicit confirmation for:

- deleting files
- exposing tokens/secrets
- sending messages to other people
- making purchases
- logging into personal accounts
- changing security settings
- running unknown scripts
- enabling real-money trading
- granting new permissions
- arbitrary shell execution from Telegram

## Recommended Next Phase

Phase A: PC Assistant Safety Architecture

Tasks:

1. Map existing OpenClaw capabilities
2. Define allowed PC operations
3. Define blocked operations
4. Create command approval levels
5. Create browser-operation policy
6. Create terminal-operation policy
7. Create Telegram remote-control policy
8. Create skill routing policy
9. Create recovery and audit logs

## Recommended Repo Strategy

Use `vortex-ai-skill-lab` for:

- skill cards
- PC assistant playbooks
- safety policies
- prompt handover templates
- repo evaluation notes

Do not mix this directly into EarnsAI Pulse Trading.

EarnsAI remains trading-paper-runtime project.

OpenClaw/Airo remains PC assistant runtime.

Vortex AI Skill Lab becomes the planning and skill source repo.

## New Chat Starting Point

In a new chat, ask the assistant to inspect:

- `~/vortex-ai-skill-lab/NEXT_ACTION.md`
- `~/vortex-ai-skill-lab/docs/AI_AGENT_PC_ASSISTANT_NEXT_PROJECT.md`
- `~/earnsai-pulse-trading/PROJECT_CARRY_OVER.md`
- `~/.openclaw/openclaw.json` safe browser fields only
- OpenClaw gateway status
