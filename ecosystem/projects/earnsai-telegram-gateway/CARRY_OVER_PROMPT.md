Lanjutkan project EarnsAI Notion Life OS + OpenClaw Agent.

JANGAN mulai dari nol.
JANGAN ubah prinsip besar.
JANGAN lompat ke AI routing berat, Queue, Gemini, lifecycle, atau dashboard intelligence.
Lanjutkan micro-step pendek, satu target kecil, lalu tunggu output user.

Status konteks terakhir: 90/100.
Progress project terakhir: 51/100.
Milestone terakhir: Rule-Based Initial Routing Bridge hampir selesai.

Arsitektur utama:
Input user dari mana pun
→ Recent Captures sebagai capture ledger / audit trail wajib
→ initial route ringan
→ final database nanti
→ Recent Captures di-update dengan audit trail final
→ dashboard hanya view ringkas.

Stable baseline:
- Telegram webhook owned by Cloudflare Worker.
- OpenClaw Telegram channel disabled, jangan re-enable.
- Worker writes directly to Notion Recent Captures.
- Raw Input preserved.
- Body Raw Note preserved.
- Source=Telegram.
- Status=Captured.
- Bot replies fast after Recent Captures created.

Manual audit trail helper:
- scripts/update_recent_capture.py stable.
- Tested end-to-end with dummy capture and real EarnsAI Dev Lab destination page.
- Helper updates Routed To, Destination DB, Destination URL, Reason, Status.
- Helper does not touch Raw Input or Raw Note body.

Current Worker:
- Cloudflare Worker TypeScript.
- No grammY.
- No Notion SDK.
- No Queue.
- No Gemini.
- Rule-based initial routing only.
- npx tsc --noEmit passes.
- Health endpoint ok.

Validated initial routes:
- Inbox
- Notes
- General Notes → Notes
- Tasks
- Sources / Daftar Pustaka
- Work Hub
- Growth Lab
- Career & Portfolio
- Life Records
- EarnsAI Dev Lab
- Top of Mind

Important bugfixes completed:
- Fixed substring bug: "tapi" no longer matches "api".
- Fixed negated reminder bug:
  - "bukan reminder" stays Inbox
  - "bukan tolong ingatkan" stays Inbox
  - "besok" alone does not create reminder/task.

Latest known deployed Worker versions:
- Negation fix: 1c9c7d2c-873a-41c0-aefb-0f86e129515f
- General Notes fix: 7c395533-a0b2-46ac-b9d6-797069f965b7
- Growth Lab fix: 36e87ada-af44-4f3c-807a-e194729baf74
- Career & Portfolio fix: fbb31d57-272d-4c9c-b309-f0c9a96d6537
- Life Records fix: 9a1f8e6f-3556-40e1-ab81-a240fbc4e956
- Top of Mind fix: 7dd9304f-f59c-442b-b4b9-786599e8498a

Backups:
- ~/earnsai-backups/earnsai-telegram-gateway-baseline-20260428-212923.tar.gz
- ~/earnsai-backups/earnsai-telegram-gateway-rule-routing-stable-20260428-215957.tar.gz
- ~/earnsai-backups/earnsai-telegram-gateway-route-coverage-stable-20260428-222450.tar.gz

Current project folder:
~/earnsai-telegram-gateway

Important files:
- src/index.ts
- NEXT_STEP.md
- TELEGRAM_GATEWAY_BASELINE.md
- scripts/update_recent_capture.py
- CARRY_OVER_PROMPT.md

Next safest micro-step:
1. Test AI System Log route before patch.
2. If it goes Inbox, patch rule for AI System Log.
3. Validate with Telegram.
4. Record result in NEXT_STEP.md.
5. Then continue Projects / Areas / Weekly Digest / Tags later.

## 2026-04-29 — Final routing live validated

Status project:
- Progress project: 100/100 untuk milestone Telegram → Recent Captures → final DB routing.
- Worker live version:
  - 28d70f14-55e5-437e-86f5-038c729d4523
- Health endpoint OK:
  - https://earnsai-telegram-gateway.earnsai.workers.dev/health

Architecture now live:
- Telegram input masuk ke Recent Captures dulu sebagai capture ledger / audit trail.
- Worker melakukan initial route ringan.
- Worker menjadwalkan final routing via ctx.waitUntil setelah Recent Captures berhasil dibuat.
- Bot tetap membalas cepat dengan URL Recent Captures.
- Final page dibuat di database final untuk 12 route aktif.
- Recent Captures di-update:
  - Destination DB
  - Destination URL
  - Reason final routing
  - Status = Routed jika final routing berhasil.

Validated smoke tests:
- Notes route: PASSED.
- Inbox fallback route: PASSED.
- Status audit Routed: PASSED.

Active final route env keys:
- INBOX_DB_ID
- NOTES_DB_ID
- TASKS_DB_ID
- SOURCES_DB_ID
- TOP_OF_MIND_DB_ID
- WORK_HUB_DB_ID
- CAREER_PORTFOLIO_DB_ID
- GROWTH_LAB_DB_ID
- LIFE_RECORDS_DB_ID
- EARNSAI_DEV_LAB_DB_ID
- AI_SYSTEM_LOG_DB_ID
- WEEKLY_DIGEST_DB_ID

Deferred routes:
- PROJECTS_DB_ID
- AREAS_DB_ID
- TAGS_DB_ID

Important constraints:
- Do not paste Notion DB IDs, tokens, or secret values into chat.
- Do not read or cat FINAL_ROUTING_DB_IDS.local.md into chat.
- Do not re-enable OpenClaw Telegram channel.
- Do not switch Telegram back to OpenClaw polling.
- Dashboard / Notion structure cleanup is deferred.
- Projects, Areas, Tags database IDs are deferred until final Notion structure is clarified.

## Carry-over Update — Telegram Bot Separation Completed

Telegram bot separation is completed.

Final bot ownership:
- Bubu the Receptionist (@bubu_receptionist_bot)
  - Dedicated Telegram Capture Gateway bot.
  - Used by Cloudflare Worker earnsai-telegram-gateway.
  - Webhook points to Worker /telegram/<TELEGRAM_SECRET_PATH>.
  - Token stored only as Cloudflare secret TELEGRAM_BOT_TOKEN.
  - Do not expose token or secret path.

- EarnsAI (@earns_openclaw_bot)
  - Dedicated OpenClaw / Agent AI bot.
  - No longer used by Capture Gateway Worker.
  - Old webhook was deleted.
  - Ready to be used later by OpenClaw / Agent AI polling/webhook.

Validated:
- Worker health OK.
- Bubu webhook active.
- OpenClaw bot webhook removed.
- Telegram smoke test passed.
- Recent Captures created.
- Final routing to Inbox worked.
- Status = Routed.

Backup:
~/earnsai-backups/earnsai-telegram-gateway-before-bubu-token-switch-20260429-224532.tar.gz

Next safe step:
- Do not change bot token again.
- Do not re-enable OpenClaw Telegram channel until OpenClaw is configured to use @earns_openclaw_bot intentionally.
- If continuing this project, only document final state or test OpenClaw separately.

## Carry-over Update — Bubu Micro-Personality Reply Patch Completed

Bubu the Receptionist now has lightweight micro-personality replies.

Implementation:
- Added buildBubuReply(pageUrl) in src/index.ts.
- Reply is randomly selected from 18 local templates.
- This is template-based only, not LLM-based.
- Bubu remains fast and deterministic enough for Capture Gateway.
- No routing, token, webhook, or OpenClaw changes were made.

Validated:
- Worker deploy succeeded.
- Current Version ID: cc2aed35-bfc3-4451-bee0-ae77b530cdd0.
- Worker health OK.
- Telegram smoke test passed.
- Recent Captures still updates correctly.

Architecture boundary:
- Bubu the Receptionist (@bubu_receptionist_bot)
  - Capture Gateway / receptionist / intake bot.
  - Has micro-personality only.
- EarnsAI (@earns_openclaw_bot)
  - OpenClaw Agent AI.
  - Main reasoning and workflow agent.
