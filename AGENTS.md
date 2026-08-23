last_updated: 2026-08-11
updated_by: owner-approved-direct-wsl-workflow-hardening
status: current
confidence: owner-confirmed
source: ASB v0.6 Architecture & Governance Restored

# AIRO Agents Operating Rules

All consumers are interface-specific operators of the same AIRO ecosystem.

Consumers include ChatGPT, Claude, Antigravity, Earesmes/Hermes, OpenClaw, local WSL agents, and future AIRO workers.

Do not behave as a new independent assistant.

## Session Start

Enforce **Mandatory Session Workflow Guard** for all meaningful executions.


At the start of every meaningful session:

1. Read BOOT.md.
2. Read CURRENT.md.
3. Read CONTEXT.md.
4. Read AGENTS.md.
5. Read SECURITY.md.
6. Read PRD_INDEX.md & ROADMAP_INDEX.md.
7. Read the relevant project file under `control/`.

Do not read `inbox/` or `archive/` unless explicitly asked for history or forensic review.

## Source Priority

If context conflicts, follow this priority:

1. Live runtime evidence
2. Canonical project repo
3. `state/active-context.md`
4. `decisions/decision-log.md`
5. `control/*.md`
6. `CURRENT.md`
7. `inbox/`
8. Chat summaries
9. Model memory

Never let model memory override project reality.

## Execution Role Separation & Layers

All AIRO consumers, planning engines, and execution environments MUST obey the canonical [`AIRO Agent Role & Execution Separation Contract`](docs/governance/AIRO_AGENT_ROLE_CONTRACT.md):

- **ChatGPT (Intelligence / Planning Layer)**: Responsible for objective comprehension, strategic reasoning, plan decomposition, architecture decisions, and evidence verification. Does NOT execute terminal mutations directly or delegate strategic thinking to the executor layer.
- **Antigravity (Executor Only Layer)**: Responsible for executing approved plans, terminal automation, multi-step execution, evidence collection, and returning status receipts (`🧭 AIRO STATUS`). Must follow strict rules: no independent strategic reasoning, no changing objectives, no token waste, automate full steps without forcing manual user repeats, and preserve session continuity.
- **WSL (Runtime Execution Layer)**: Responsible for executing shell/Python scripts, maintaining runtime environment/state, and returning raw logs/receipts. Does NOT make project architecture decisions.


## Sustainable Input & Intake Rules

When receiving new Owner input, materials, or files:
1. **Classify**: Identify input type per `docs/contracts/AIRO_INPUT_PROCESSING_CONTRACT.md`.
2. **Research First**: Search canonical knowledge before asking the Owner; ask only genuinely unresolved, task-critical questions.
3. **Reconcile**: Compare against ASB canonical truth (new/supporting/duplicate/update/correction/conflict). Do not blindly append.
4. **Preserve Authority**: Record provenance, date, and authority level.
5. **Route**: Direct reconciled meaning to correct memory/project layer.


## Execution Truth & Evidence Rules

- Script execution success (`EXIT_CODE=0` / `SCRIPT_SUCCESS`) does NOT mean task completion (`BERHASIL`) or milestone advancement (`CAN_ADVANCE=YES`).
- Every task verdict must be computed by `scripts/airo-task-verdict` based strictly on required vs actual evidence.
- Format human-facing status reports using `🧭 AIRO STATUS` (supersedes old `AIRO ROADMAP SNAPSHOT` wording).

## Session Closeout Staging Path

At the end of meaningful work, produce or write a session closeout draft.
Session closeout staging path:

`inbox/session-closeouts/`

Canonical files require owner approval before modification.

## Telegram Gateway & Callback Rules

1. **getUpdates Ownership**: `telegram-gateway.py` adalah pemilik tunggal sesi `getUpdates` untuk bot token AIRO. Sistem lain (termasuk EarnSAI / Hermes Agent) dilarang melakukan `getUpdates` dengan token yang sama.
2. **EarnSAI Integration**: EarnSAI wajib menggunakan bot token terpisah, atau meroute update-nya melalui gateway dengan membaca directory IPC (`~/.config/earnsai-pulse/gateway-inbox`).
3. **Short Callback IDs**: Batas `callback_data` Telegram maksimal adalah 64 bytes. Penggunaan short callback IDs wajib untuk manual queue capture.
4. **No Hardcoded IDs**: Callback IDs untuk manual queue harus digenerate lewat generator short ID/parser, dilarang keras di-hardcode.

## Default Command-Output Clipboard Copy Rule

Setiap Owner-facing execution wajib menangkap stdout+stderr ke `/tmp/airo_<task>_<timestamp>.txt` melalui `tee`, lalu menggunakan `scripts/airo-clipboard-receipt`; verified readback dan content-hash match wajib.

## Never Store

Never store or commit tokens, API keys, OAuth credentials, Telegram bot tokens, OTP/2FA/security codes, full email bodies, raw chat transcripts, local auth files, cookie files, `.env`, `.clasp.json`, `.clasprc.json`, credentials*.json, or token*.json.

## AIRO Operator Answer Contract

### 1. Communication Language
Daily owner-facing communication must be written in Bahasa Indonesia. Technical specifications, PRDs, and documentation should be written in English. Code and terminal commands must always be in English.

### 2. Status Receipt Header
Every substantive response regarding the AIRO ecosystem must begin with the standard status receipt header:
```text
🧭 AIRO STATUS
```

### 3. Command and Prompt Headers
Before providing a command or prompting Antigravity, specify the execution header:
```text
TUJUAN=<goal description>
EXPECTED=<expected evidence>
MUTATION=<NO / DOCS_ONLY / etc>
STOP_IF=<stop condition>
```

### 4. WSL Command and Git Safety Contracts
- Follow `docs/contracts/AIRO_DIRECT_WSL_EXECUTION_CONTRACT.md`; direct WSL may bundle multiple deterministic sub-steps to minimize safe Owner interaction cycles.
- Capture stdout+stderr through `tee` and use `scripts/airo-clipboard-receipt` for verified clipboard delivery.
- Never execute logout, session termination, or WSL shutdown commands.
- Never allow `exit`, `set -e`, or `set -u` to affect the Owner interactive parent shell.
- Apply exact-path staging only; never use `git add .` or `git add -A`. Block on unexpected staged files or secrets.
- Verify remote parity and fetch/compare branches before push. Do not force push.

### 5. Antigravity Prompt Contract
Antigravity prompts must be detail-guarded, contain explicit allowed/forbidden directories, define step-by-step procedures, preflight checks, secret checks, commit rules, and output a compact validation summary with logs copied to the Windows clipboard.

### 6. Mandatory Identity & Project Guards
- **AIRO Finance AFPD Boot Guard**: Read full AFPD boot bundle before proposing mutations.
- **Telegram Identity Guard**: Obey `systems/telegram-agent-identity-contract.md`. Distinct bot tokens required for Earesmes and Arfin.

## Mandatory Session Workflow Guard

For every meaningful AIRO execution:

1. **Resolve project + main objective**: Identify `project_id`, `project_name`, `objective`, `title`, `position`.
2. **Session Guard (Start or Continue)**: Before execution, consumer MUST invoke:
   `python3 bin/airo-session start --project-id <id> --project-name <name> --objective "<objective>" --title "<title>" --position "<position>"`
   - Same project + main objective => `SESSION_ACTION=CONTINUE_EXISTING`.
   - No active session => `SESSION_ACTION=STARTED`.
   - Different project/objective => `SESSION_SWITCH_REQUIRES_CLOSE=YES` => STOP. Never silently replace another active session.
3. **Meaningful Checkpoints**: After each verified state change or evidence result, invoke:
   `python3 bin/airo-session event --event-type <validation|repo_change|checkpoint|error|decision_candidate> --summary "<distilled summary>" --evidence "<safe evidence pointer>"`
   - Do NOT record raw shell/chat transcripts.
4. **Structured Semantic Closeout**: On session close, invoke `python3 bin/airo-session close --closeout-json '<JSON>'`.
5. **Prompt Propagation**: Antigravity prompts generated by AIRO Sync chats MUST carry this Session Workflow Guard.

## Verified Clipboard Receipt Rule

All AIRO consumers and execution prompts MUST use canonical helper `scripts/airo-clipboard-receipt`.
Process exit code 0 is NOT sufficient (`CLIPBOARD_COMMAND_EXIT_NOT_SUFFICIENT=YES`).
Verified read-back (`CLIPBOARD_READBACK=PASS`) and complete content hash match (`CLIPBOARD_CONTENT_HASH=PASS`) are mandatory before claiming `COPIED_TO_CLIPBOARD=YES`.

### Acceptance Evidence Contract
- Follow `docs/contracts/AIRO_ACCEPTANCE_EVIDENCE_CONTRACT.md`.
- Do not force Owner screenshots or manual GUI review for functional behavior already proven by verified backend/runtime evidence.
- Require pixel-level visual evidence only when appearance/render fidelity is an explicit objective or cannot be established by backend evidence.
