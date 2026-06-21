# AIRO Chat Rules

Repository: progamer6918/vortex-ai-skill-lab
Branch: main
Scope: Airo Personal Workflow continuation and vibe coding

## Purpose

This file is the source-of-truth operating contract for AI chats that continue Airo Personal Workflow.

The goal is to make project continuation efficient, safe, structured, low-hallucination, and seamless across new chats.

## Core Principle

GitHub is the source of truth.

The assistant must follow repository docs and terminal output instead of relying on chat memory alone.

The assistant must not invent roadmap items, phases, milestones, status, files, commit hashes, or command results.

## Language

Use Bahasa Indonesia for conversation.

Use English only when it is more appropriate for:
- filenames
- commands
- code
- commit messages
- technical terms

## Required Repo Bootstrap Rule

The assistant must never assume the terminal is already inside the repository.

Before running any Git command or repo-relative command, every paste-safe command must:

1. Set REPO_URL.
2. Set REPO_DIR.
3. Clone the repo if REPO_DIR does not contain a Git repo.
4. cd into REPO_DIR.
5. Only then run git, sed, tests, smoke checks, commits, or pushes.

Required variables for this project:

    REPO_URL="https://github.com/progamer6918/vortex-ai-skill-lab.git"
    REPO_DIR="${AIRO_REPO_DIR:-$HOME/vortex-ai-skill-lab}"

Do not run these from the user's home directory unless the command has already cd'd into the repo:
- git status
- git rev-parse
- git branch
- find .
- sed docs/...
- python3 scripts/...
- ./bin/...

Do not perform generic repo discovery from home because the repo path is known.

## Source-of-Truth Read Order

A new chat must read and follow these files in order:

1. docs/personal-workflow/AIRO_PROJECT_INDEX.md
2. docs/personal-workflow/AIRO_CHAT_RULES.md
3. docs/personal-workflow/AIRO_CONTINUITY_PACK.md
4. docs/personal-workflow/AIRO_NEW_CHAT_BOOTSTRAP_TEMPLATE.md
5. latest handoff under docs/personal-workflow/handoff/
6. current phase roadmap
7. latest completed phase documents

If a file is not present yet, the assistant must say so and proceed only with verified available source-of-truth.

## Default Response Format

For important project-continuation responses, start with:

1. Ringkas checkpoint from source-of-truth or latest terminal output.
2. Official next item.
3. Safety boundaries status.
4. Context meter.
5. One paste-safe command for the next step.

The assistant must not provide a new command before analyzing whether the previous terminal output was PASS or FAIL.

## Strict Command Format Rule

When giving a command, the assistant must provide exactly one command block.

The command block must:
- be a single fenced code block labelled bash
- contain the full command
- start directly with bash -lc
- be copy-paste safe
- contain no nested fenced code blocks
- contain no literal fenced code block markers inside the command body
- contain no command fragments outside the command block
- contain no continuation text that must be copied separately

If the assistant cannot guarantee the command format, it must not provide the command and must instead say:

    FORMAT_RISK: command withheld


## Command Rules

Use one paste-safe command per milestone.

For complex commands, use:

    bash -lc

The command must:
- run from the correct repo directory
- smoke test before commit
- commit only after PASS
- push only after commit succeeds
- display git status --short before staging
- stage only relevant files
- include a safety check against forbidden staged files
- avoid reading secret contents
- avoid external writes unless explicitly approval-gated

Do not split one milestone into multiple copy-paste blocks unless the user explicitly asks.

## Smoke Test Rule

Before committing project changes, run relevant smoke tests.

For Airo Personal Workflow, common read-only checks include:

    ./bin/airo-daily --text
    ./bin/airo-dashboard-align
    python3 scripts/personal-workflow/airo_approval_review.py list --status pending --compact
    python3 scripts/personal-workflow/airo_ops_dashboard.py
    python3 scripts/personal-workflow/airo_google_fallback.py status
    python3 scripts/personal-workflow/airo_intent_router.py "enable live trading and execute market orders now"

The smoke test must not perform real Google writes, queue execution, approval mutation, credential reads, trading actions, or service restarts.

## Safety Boundaries

Always active:
- do not read secrets, tokens, cookies, sessions, passwords, .env files, or browser profiles
- do not commit local DBs, receipts, OAuth tokens, OAuth clients, credentials, runtime state, or private files
- do not perform real Google writes without approval gate
- do not patch OpenClaw core without explicit approval
- do not restart OpenClaw service without explicit approval
- do not touch EarnsAI trading runtime unless explicitly requested
- do not enable live trading
- do not hard-delete finance records

If untracked paths such as EarnsAI, runtime, or trading appear in git status, do not read, modify, stage, or commit them.

## Anti-Hallucination Rules

The assistant must not:
- claim it read a file without file content or terminal output
- claim a command succeeded before the user provides output
- claim commit or push succeeded without terminal proof
- claim DONE without source-of-truth or terminal proof
- invent roadmap, phases, sub-phases, milestones, file contents, or commit hashes
- infer sensitive file contents from filenames

If the assistant is relying only on a user-provided raw note, say so.

If the assistant is relying on GitHub docs or terminal output, say so.

## Official Roadmap Discipline

Do not invent phases.

Do not add sub-phases.

Run only the official next roadmap item unless the user explicitly approves a source-of-truth maintenance patch.

A source-of-truth maintenance patch must not be mislabelled as a new phase.

## Context Meter Rule

Every important project response must include:

    Context meter: X/100

Use a conservative estimate:
- 0-20: new chat or light context
- 21-50: medium context
- 51-75: long context beginning
- 76-85: prepare carryover soon
- 86-100: do not start large milestone; prepare handoff

The assistant cannot know the exact platform context limit. The number is an operational estimate based on chat length, terminal outputs, decisions, and completed milestones.

## Carryover Rule

If Context meter is 76 or higher:
- start preparing a concise continuation summary
- warn that carryover may be needed soon
- avoid large risky refactors or long milestones

If Context meter is 85 or higher:
- do not start a large milestone
- provide one paste-safe command to write the latest handoff/update to GitHub
- after that command passes, provide a complete carryover prompt for a new chat

## GitHub Handoff Command Rule

Near context limit, the assistant must provide a paste-safe command that records to GitHub:
- latest project status
- last DONE milestone
- latest commit hash if known
- official next item
- key decisions from the chat
- active safety boundaries
- chat rules reference
- required source-of-truth read order
- important commands
- forbidden paths and risks
- instruction that GitHub remains source of truth

The command must not stage or commit secrets, local DBs, receipts, credentials, runtime state, EarnsAI runtime, or trading files.

## Carryover Prompt Rule

The carryover prompt for a new chat must include:
- project name
- repo and branch
- repo bootstrap rule
- source-of-truth read order
- latest DONE status
- latest known commit
- official next item
- safety boundaries
- strict command format rule
- working style
- important commands
- instruction to begin with checkpoint, official next item, safety boundaries, context meter, and one paste-safe command

The carryover prompt must be in one text block that can be copied into a new chat.

Do not use nested fenced code blocks inside the carryover prompt.

## Handling Terminal Output

When the user pastes terminal output:
- analyze PASS or FAIL first
- mention the commit hash if commit succeeded
- mention push status if push succeeded
- identify untracked forbidden paths and state they must not be touched
- give one fix command if FAIL
- give the next official item if PASS

## Important Commands

Common Airo commands:
- ./bin/airo-daily --text
- ./bin/airo-daily
- ./bin/airo-dashboard-align
- python3 scripts/personal-workflow/airo_intent_router.py "<message>"
- python3 scripts/personal-workflow/airo_approval_review.py list --status pending --compact
- python3 scripts/personal-workflow/airo_approval_review.py inspect --id "<queue_id>"
- python3 scripts/personal-workflow/airo_executor_recommend.py recommend --id "<queue_id>"
- python3 scripts/personal-workflow/airo_executor_recommend.py list-actionable --limit 10
- python3 scripts/personal-workflow/airo_ops_dashboard.py
- python3 scripts/personal-workflow/airo_google_fallback.py status

## Final Operating Goal

Finish project work quickly and safely by prioritizing:
- one command per milestone
- repo bootstrap correctness
- smoke test before commit
- source-of-truth GitHub docs
- no hallucinated status
- no leaked or committed secrets
- clean carryover between chats

## Batch-forward Execution Mode

Status: ACTIVE

For Airo Personal Workflow tasks, default to batch-forward execution:

- Prefer substantial batches over tiny micro-steps.
- Combine design, implementation artifact, smoke test, documentation, commit, and next-action updates when safe.
- Keep exactly one bash command block when a command is needed.
- The command must start with bash -lc and must bootstrap/cd into the repo.
- Read source-of-truth docs before repo changes.
- Stage only intended files.
- Do not touch or commit restricted paths: EarnsAI, runtime, trading.
- Do not read or commit secrets, credentials, local DB, token files, or runtime state.
- Do not perform Google Sheets ledger writes without explicit approval gate.
- If command formatting is uncertain, respond with FORMAT_RISK: command withheld.

Batch-forward optimizes for efficient progress, no avoidable mistakes, no known bugs, and smoke tests before commit.
