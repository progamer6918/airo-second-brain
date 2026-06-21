# AIRO v1.3 Telegram-to-Sheets Carryover Prompt

Paste this into the next chat.

## Role for next assistant

You are continuing AIRO Google Sheet Finance v1.3.

Use Bahasa Indonesia. Be direct, command-oriented, and do not give fragmented or broken shell commands. Always put commands inside one complete fenced bash block.

## Repository

Work in:

~/vortex-ai-skill-lab

Do not touch or stage these restricted untracked directories:

- EarnsAI
- runtime
- trading

## Bootstrap Command

First ask the user to run:

```bash
cd ~/vortex-ai-skill-lab && scripts/personal-workflow/airo_v13_next_chat_bootstrap.sh
Then read the output before proposing patches.

Current User Goal

The user wants:

Telegram chat -> AIRO finance route -> local persistence/queue -> Google Sheet 💰 Airo Personal Finance -> correct tab.

They do not only want preview. They want Telegram finance chat to be recorded to Google Sheet.

Latest Commits

Important latest commits:

346bd53 fix: force AIRO finance routing in intent router
a2eabdf docs: add AIRO finance v1.3 Telegram force router patch
24546a2 feat: add AIRO finance sheet v1.3 write path
3b12cc3 docs: start AIRO finance sheet v1.3 production write track
cdd554c docs: close out AIRO finance sheet v1.2 preview layer
3749fe5 feat: complete AIRO finance sheet v1.2 preview layer
7865b88 feat: add AIRO finance sheet v1.2 unified regression
Verified PASS

Latest verified PASS:

local intent router: "kayaknya bayar sesuatu kemarin" -> finance_capture -> 🧾 Review Queue
local mapper: "kayaknya bayar sesuatu kemarin" -> 🧾 Review Queue
local cash route: "hari ini cash kepake beli makan 20rb" -> 💵 Cash Ledger
OpenClaw gateway active
AIRO health check PASS
finance regression PASS
live Sheets dry-run idempotent PASS
Telegram no longer answers generic chat for ambiguous finance
Important Telegram Smoke Result

Telegram smoke:

User:
kayaknya bayar sesuatu kemarin

Airo replied:
Oke Egit, "kayaknya bayar sesuatu kemarin" udah masuk jalur AIRO Finance Review Queue. Nanti bakal gue bantu cek lebih lanjut di sana.

Meaning:

Routing is fixed.

But after smoke, health check still showed:

REPORT_WRITE_CANDIDATE_COUNT=0
TOTAL_WRITE_CANDIDATES=0

Therefore persistence / durable Review Queue candidate / actual Sheet row is not yet proven.

Important OpenClaw Context Finding

OpenClaw logs showed:

AGENTS.md is 21191 chars, limit 12000, truncated in injected context.

So do not rely only on prompt/AGENTS rules. Prefer executable repo code.

Current Status by Tab
💸 Transactions: FULL_AUTO_CORE_READY
💳 Credit Card: FULL_AUTO_CORE_READY
🔄 Sync Log: FULL_AUTO_CORE_READY
🥇 Aset: PATCHED_ASSET_SYNC
🧾 Review Queue: FULL_AUTO_WRITE_PATH_READY
💵 Cash Ledger: FULL_AUTO_WRITE_PATH_READY
🏠 Cicilan Rumah: FULL_AUTO_WRITE_PATH_READY
🤝 Hutang: FULL_AUTO_WRITE_PATH_READY
📅 Monthly Review: REPORTING_ONLY
🏠 Dashboard: DESIGN_DONE
⚙️ Settings: CONFIG_ONLY
Next Technical Task

Patch persistence/write-candidate generation.

Target first route:

kayaknya bayar sesuatu kemarin

Expected final behavior:

Telegram message routes to finance_capture.
It creates durable Review Queue candidate.
Dry-run/write-preview sees the candidate.
Full-auto sync writes Review Queue row to Google Sheet.
Health check after smoke no longer hides this as zero candidates unless already inserted/idempotent.
Airo reply must not claim success unless persistence/write result is verified.
Where to Look

Important files:

scripts/personal-workflow/airo_intent_router.py
scripts/personal-workflow/airo_finance_sheet_v12_mapper_preview.py
scripts/personal-workflow/airo_full_auto_sheets_sync.py
scripts/personal-workflow/airo_sheets_sync_dry_run.py
scripts/personal-workflow/airo_sheets_sync_write_preview.py
scripts/personal-workflow/airo_approval_queue.py
scripts/personal-workflow/airo_queue_executor.py
scripts/personal-workflow/airo_transaction_persistence.py
scripts/personal-workflow/airo_status.sh

Search for:

plan_approval_queue
approval_queue
Review Queue
write_preview
full_auto
persist_transaction
airo_intent_router
Rules
Do not send repeated Telegram smoke.
Do not touch EarnsAI, runtime, trading.
Do not stage secrets, DBs, env, credentials, token files, receipt files.
Patch one route first: Review Queue.
Use temp DB or fake client tests before live.
Run local regression and health check before Telegram smoke.
One Telegram smoke only, then verify.
Expected Next Command Style

Give one paste-safe bash command. No broken heredocs. No command outside markdown. No fragmented manual steps unless absolutely necessary.

## 2026-05-12 v1.3 Review Queue clean mapping checkpoint

Verified before this checkpoint:
- 569f459 persists ambiguous finance text to a local Review Queue candidate.
- 45ef5ae supports the legacy approval_queue schema used by the persistent DB.
- Persistent DB verification passed for: kayaknya bayar sesuatu kemarin.
- Dry-run and write-preview detected one Review Queue candidate.

This checkpoint:
- Maps v1.3 approval_queue payload into a clean Review Queue row.
- Keeps queue_id, raw_text, duplicate_key, and notes clean for Sheet write-preview.
- Lets full-auto mode dry-run run without requiring AIRO_SPREADSHEET_ID.

Still not claimed:
- No real Google Sheet row has been written yet.
- Real write remains approval-gated and must be Review Queue only.
