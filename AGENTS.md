last_updated: 2026-08-04
updated_by: owner-approved-v06-architecture-correction
status: current
confidence: owner-confirmed
source: ASB v0.6 Architecture & Governance Restored

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
7. Read the relevant project file under `projects/`.

Do not read `inbox/` or `archive/` unless explicitly asked for history or forensic review.

## Source Priority

If context conflicts, follow this priority:

1. Live runtime evidence
2. Canonical project repo
3. `state/active-context.md`
4. `decisions/decision-log.md`
5. `projects/*.md`
6. `CURRENT.md`
7. `inbox/`
8. Chat summaries
9. Model memory

Never let model memory override project reality.

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

Setiap perintah yang dieksekusi atas permintaan Owner wajib menangkap output-nya ke berkas `/tmp/airo_<task>_<timestamp>.txt`, diarahkan lewat `tee`, dan disalin ke clipboard Windows menggunakan `clip.exe` di WSL.

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
- Follow the canonical WSL command template with logging to `/tmp`, `tee` output capture, Windows clipboard copy via `/mnt/c/Windows/System32/clip.exe` (fallback `clip.exe`), and validation summary output.
- Never execute logout, session termination, or WSL shutdown commands.
- Apply exact-path staging only; never use `git add .` or `git add -A`. Block on unexpected staged files or secrets.
- Verify remote parity and fetch/compare branches before push. Do not force push.

### 5. Antigravity Prompt Contract
Antigravity prompts must be detail-guarded, contain explicit allowed/forbidden directories, define step-by-step procedures, preflight checks, secret checks, commit rules, and output a compact validation summary with logs copied to the Windows clipboard.

### 6. Mandatory Identity & Project Guards
- **AIRO Finance AFPD Boot Guard**: Read full AFPD boot bundle before proposing mutations.
- **Telegram Identity Guard**: Obey `systems/telegram-agent-identity-contract.md`. Distinct bot tokens required for Earesmes and Arfin.
