# Telegram Gateway Stable Baseline

Date: 2026-04-28

Status:
- Telegram webhook points to Cloudflare Worker.
- Cloudflare Worker writes directly to Notion Recent Captures.
- Raw Input is preserved.
- Page body contains Raw Note.
- Source = Telegram.
- Status = Captured.
- Routed To = Inbox.
- Reason is filled with lightweight default routing explanation.
- Destination DB = Inbox (pending final routing).

OpenClaw:
- OpenClaw gateway is active.
- OpenClaw Telegram channel is disabled to avoid getUpdates/webhook conflict.
- Config path: ~/.openclaw/openclaw.json
- Stable setting: channels.telegram.enabled = false

Reason:
Telegram must be handled by Cloudflare Worker first so capture is fast and raw-safe.
OpenClaw remains the larger brain for later routing, debugging, workflow, and source-of-truth work.

Notion Source of Truth:
- Database: EarnsAI Dev Lab
- URL: https://www.notion.so/Project-Source-of-Truth-Telegram-Gateway-Stable-Baseline-350768acbac98150919ff5fc56d3d18a

## Stable Snapshot — 2026-04-28 23:02

Status:
- Telegram webhook is owned by Cloudflare Worker.
- OpenClaw Telegram channel remains disabled.
- Worker writes directly to Notion Recent Captures.
- Recent Captures remains capture ledger / audit trail, not final database.
- Raw Input and Raw Note body are preserved.
- Source=Telegram and Status=Captured are preserved.
- Bot replies quickly after Recent Captures page is created.

Rule-based initial routing:
- Inbox ✅
- Notes ✅
- General Notes → Notes ✅
- Tasks ✅
- Sources / Daftar Pustaka ✅
- Work Hub ✅
- Growth Lab ✅
- Career & Portfolio ✅
- Life Records ✅
- EarnsAI Dev Lab ✅
- Top of Mind ✅
- AI System Log ✅
- Projects ✅
- Areas ✅
- Weekly Digest ✅
- Tags ✅

Latest deployed Worker version:
- 3c4f5dfa-df47-4c73-bbef-b884d8a86b12

Stable backup:
- ~/earnsai-backups/earnsai-telegram-gateway-all-light-routes-stable-20260428-2301.tar.gz

Still not implemented:
- Automatic final page creation in destination databases.
- Automatic Destination URL update back to Recent Captures.
- AI classifier.
- Confidence check.
- Lifecycle automation.
- Dashboard intelligence.
