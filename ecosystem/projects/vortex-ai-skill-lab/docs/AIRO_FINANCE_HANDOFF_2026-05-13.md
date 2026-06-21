# AIRO Finance Handoff — 2026-05-13

## Final Decision
Vortex/Airo lama di-freeze. n8n berhasil sebagai prototype, tetapi tidak dipakai sebagai final karena local n8n + Pinggy free tidak sustainable. Final target dipindah ke:

Telegram Bot → Google Apps Script Web App → Google Sheet → Telegram Reply

## Important Constraints
- Jangan commit token, secret, .env, API key, private key, cookie, session.
- Jangan pakai live trading / private exchange API / real-money trading.
- Project ini fokus personal finance / research-only.
- Token Telegram disimpan manual di Apps Script Script Properties sebagai BOT_TOKEN.

## Vortex/Airo Old Repo Status
OpenClaw sempat hidup:
- openclaw-gateway.service active
- port 18789 LISTENING
- Telegram lama bisa reply

Masalah utama:
- Input `cash beli minum 12345 hari ini` tetap masuk Review Queue di live Telegram.
- Local dry-run sempat berhasil ke Cash Ledger, tetapi live path tetap beda.
- Root cause lama terlalu banyak layer: Telegram → OpenClaw → agent → router → mapper → planner → DB → sync timer → Google Sheet.

Patch lokal sempat menyentuh:
- scripts/personal-workflow/airo_cash_ledger_planner.py
- scripts/personal-workflow/airo_review_queue_planner.py
- scripts/personal-workflow/airo_finance_sheet_v12_mapper_preview.py

Jangan anggap patch Airo ini final sebelum direview ulang.

## n8n Prototype Status
Folder prototype:
~/finance-bot-alternatives/n8n-finance

n8n MVP berhasil:
Telegram Trigger → Code parser → HTTP Request Apps Script → Google Sheet → Telegram Send Message

Tab staging:
n8n_Transactions

Header:
timestamp | date | type | category | description | amount | account | source | raw_text | status

5 smoke test berhasil:
- cash beli kopi 15000 hari ini
- bca beli makan 20000 hari ini
- blu bayar parkir 5000 hari ini
- gopay beli es teh 8000 hari ini
- cash beli bensin 30000 hari ini

n8n tidak final karena Pinggy free expire sekitar 60 menit. Folder n8n jangan dihapus sampai Apps Script direct berhasil.

## Apps Script Prototype
Apps Script sebagai writer dari n8n berhasil:
- menerima JSON
- append row ke n8n_Transactions
- response ok:true appended:true

## Final Architecture Target
Telegram langsung ke Apps Script:

Telegram Bot → Apps Script doPost(e) → parser JS → router tab → append row → sendMessage

Tidak perlu n8n, Pinggy, VPS, Docker, atau laptop menyala.

## Current Blocking Issue
Direct Apps Script belum berhasil.

Webhook Telegram sudah bisa diset, tetapi Web App URL Apps Script masih membalas Google Drive 404 / "Halaman Tidak Ditemukan" saat dites curl.

URL yang pernah gagal:
- https://script.google.com/macros/s/AKfycbwJGz7zAVvq5eP66LtSwijXPoMRllEh68Ew72_5yPiohrl4ZOdhDx6pBF1NqpbSkFpV-w/exec
- https://script.google.com/macros/s/AKfycbw24BIbdd2Irj4a4mc1AtE3l6GhQ7eu8M37dobupVoddf7cxWf7trlzU1sE8pQ3R7ubFw/exec

Kesimpulan:
Masalah sekarang bukan token, bukan Telegram, bukan parser. Masalah utama adalah Apps Script deployment URL/access.

## Next Step in New Chat
1. Buka Apps Script dari Google Sheet sandbox.
2. Deploy ulang sebagai Web App:
   - Execute as: Me
   - Who has access: Anyone
3. Copy URL /exec baru.
4. Test URL dengan curl POST dummy.
5. Kalau URL tidak lagi Google Drive 404, baru setWebhook Telegram ke URL itu.
6. Test Telegram → Apps Script → Sheet → reply.
7. Setelah direct webhook berhasil, lanjut multi-tab routing.
8. Setelah direct webhook stabil, folder n8n prototype boleh dihapus:
   rm -rf ~/finance-bot-alternatives/n8n-finance

## Multi-tab Routing Plan
Target routing:
- cash/tunai → Cash Ledger
- normal expense/income → Transactions
- tokopedia cc / credit card / cc → Credit Card
- cicilan rumah / kpr / angsuran rumah → Cicilan Rumah
- hutang / utang → Hutang
- nabung / tabung / saving / aset → Aset
- ambiguous / amount missing → Review Queue

Dashboard, Monthly Review, dan Settings bukan target append utama. Itu dipakai sebagai dashboard/config/formula.


---

# Update - Direct Hosting Cleared

## Confirmed Working
Final free architecture is now working:

Telegram Bot -> Cloudflare Worker -> Google Apps Script standalone -> Google Sheet -> Telegram reply

## Working URLs
Cloudflare Worker:
https://airo-finance-telegram-proxy.progamer6918.workers.dev

Apps Script standalone:
https://script.google.com/macros/s/AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA/exec

## Why Cloudflare Worker Is Used
Direct Telegram webhook to Apps Script failed with:
Wrong response from the webhook: 302 Moved Temporarily

Cloudflare Worker fixes this by accepting Telegram webhook requests and forwarding POST requests to Apps Script while returning a 200 response.

## Authorization Fix
Apps Script needed manual authorization for:
- SpreadsheetApp.openById
- UrlFetchApp.fetch

A helper function named authorizeRequiredScopes was run manually once in Apps Script. After permission approval, Telegram bot successfully replied.

## Current Working Bot Reply
The bot successfully replied with:
✅ Tercatat ke Google Sheet.
Rencana tab: Cash Ledger
Ditulis ke: n8n_Transactions

## Current State
- n8n and Pinggy are no longer required for final architecture.
- n8n was only a prototype.
- Current physical write target is still staging tab: n8n_Transactions.
- Apps Script already detects planned_tab such as Cash Ledger.
- Next milestone is real multi-tab write.

## Next Milestone
Implement multi-tab real write in Apps Script:
- Keep raw/staging log in n8n_Transactions.
- Also write parsed row to planned target tab.
- Target tabs: Cash Ledger, Transactions, Credit Card, Cicilan Rumah, Hutang, Aset, Review Queue.
- Do not touch Dashboard, Monthly Review, or Settings yet.


---

# Update - Multi-tab Routing v1 Passed

Confirmed Telegram end-to-end tests:

1. Input: bca beli makan 20000 hari ini
   Result: n8n_Transactions + 💸 Transactions
   Account: BCA
   Category: Makan
   Amount: 20000

2. Input: cash beli kopi 15000 hari ini
   Result: n8n_Transactions + 💵 Cash Ledger
   Account: Cash
   Category: Makan
   Amount: 15000

3. Input: kayaknya kemarin bayar sesuatu
   Result: n8n_Transactions + 🧾 Review Queue
   Account: Unknown
   Category: Lainnya
   Amount: 0

Current validated architecture:
Telegram Bot -> Cloudflare Worker -> Google Apps Script standalone -> Google Sheet staging + routed tab -> Telegram reply

Validated routed tabs:
- 💸 Transactions
- 💵 Cash Ledger
- 🧾 Review Queue

Next tabs to implement carefully:
- 💳 Credit Card
- 🏠 Cicilan Rumah
- 🤝 Hutang
- 🥇 Aset

Important:
Do not directly write to complex tabs before auditing their internal row/section schema.

---

# Update - Multi-tab Final Passed

Confirmed live Worker -> Apps Script -> Google Sheet tests passed.

Validated architecture:

Telegram Bot -> Cloudflare Worker -> Google Apps Script standalone -> Google Sheet staging + routed tab -> Telegram reply

Validated final routed tabs:

- 💸 Transactions: written
- 💵 Cash Ledger: written
- 💳 Credit Card: written
- 🏠 Cicilan Rumah: written
- 🤝 Hutang: written
- 🥇 Aset: written
- 🧾 Review Queue: written

Final fixes applied:

- Apps Script code managed through clasp.
- Old doPost in Kode.js disabled locally before push.
- Active Web App deployment updated to latest version.
- Aset savings route fixed by writing valid savings event type, e.g. savings_deposit.
- Review Queue status fixed by normalizing review rows to pending.
- Cicilan Rumah header/schema detection fixed enough for live write.

Important current production URL:

Cloudflare Worker:
https://airo-finance-telegram-proxy.progamer6918.workers.dev

Active Apps Script Web App:
https://script.google.com/macros/s/AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA/exec

Current final status:

AIRO Finance Telegram Bot personal finance multi-tab write path is production-working.

Do not commit:
- .clasprc.json
- .clasp.json from live clone
- token/secret/env files
- runtime folders
- trading folders
- Apps Script local clone folder


---

# Update - n8n_Transactions Removed From Final Flow

The n8n_Transactions staging tab has been removed from the final production path.

Confirmed final path:

Telegram Bot -> Cloudflare Worker -> Google Apps Script standalone -> routed Google Sheet tab -> Telegram reply

The Apps Script no longer writes to n8n_Transactions before routed writes.

Validated direct routed tabs:

- 💸 Transactions
- 💵 Cash Ledger
- 💳 Credit Card
- 🏠 Cicilan Rumah
- 🤝 Hutang
- 🥇 Aset
- 🧾 Review Queue

n8n_Transactions can be deleted from the Google Sheet and should not be recreated by the final Apps Script flow.


---

# Update - Legacy Tabs Removed From Final Flow

Confirmed deleted from Google Sheet and tested not recreated:

- n8n_Transactions
- Airo_Schema_Audit

Final production flow no longer writes to staging/audit tabs.

Current final architecture:

Telegram Bot -> Cloudflare Worker -> Google Apps Script standalone -> routed Google Sheet tab -> Telegram reply

Validated routed tabs:

- 💸 Transactions
- 💵 Cash Ledger
- 💳 Credit Card
- 🏠 Cicilan Rumah
- 🤝 Hutang
- 🥇 Aset
- 🧾 Review Queue

Notes:

- n8n_Transactions was only a prototype/staging tab and has been removed.
- Airo_Schema_Audit was only a temporary audit/debug tab and has been removed.
- Apps Script legacy Kode.js has been neutralized.
- Final doPost handler lives in AIRO_Finance_Multitab_Final_v1.js.
- Do not recreate n8n_Transactions or Airo_Schema_Audit in final flow.


---

# Update - Cash Pocket Finalized

Cash Ledger now supports two cash pockets without adding new tabs:

- cash_umum
- cash_bensin

Confirmed behavior:

- cash masuk / cash terima / dapat cash / uang masuk cash -> Cash Ledger inflow
- cash bensin masuk / cash bbm masuk -> cash_bensin inflow
- cash beli bensin / cash bbm keluar -> cash_bensin outflow
- normal cash spending -> cash_umum outflow

Cash inflow behavior:

- amount_in is filled
- amount_out is left blank
- type is normalized to transfer_in where applicable
- status is set to aktif for cash inflow rows

Cash dashboard support:

- Cash Ledger rows now populate session_id for cash_umum and cash_bensin.
- refreshCashLedgerMaintenance can be run to backfill older test rows.
- Monthly Review cash formulas were added through refreshCashMonthlyReviewFormulas.

Final architecture remains:

Telegram Bot -> Cloudflare Worker -> Google Apps Script standalone -> routed Google Sheet tab -> Telegram reply


---

# Update - Assets, Gold, Net Worth, and CLI Deploy

Current AIRO Finance state:

- Gold asset parser works for gold buy/add and gold sell.
- ANTAM gold price sync writes latest 24K reference price to Aset!F12.
- Daily ANTAM trigger should use updateAntamGoldPriceDailyAndSyncSheet.
- Gold Ledger now stores grams_in / grams_out using 24K-equivalent gram for valuation consistency.
- Dashboard now contains final Net Worth & Home Equity panel.
- Aset legacy Net Worth block is hidden/legacy and should not be treated as final source of truth.
- Final Net Worth source of truth is Dashboard:
  - Net Worth Likuid
  - Ekuitas Rumah
  - Net Worth Total
- House valuation baseline:
  - Nilai Rumah Pasar: Rp166.000.000
  - Haircut: 5%
  - Sisa Pokok Rumah: currently user-adjusted; use conservative estimate until exact principal is known.
- CLI deploy helper added:
  scripts/personal-workflow/airo_apps_script_deploy.sh

Deployment workflow going forward:
- Edit Apps Script locally.
- Run scripts/personal-workflow/airo_apps_script_deploy.sh.
- Avoid manual Apps Script UI deployment unless deployment ID changes.


---

# Update - Final Daily Finance Bot Stabilization

Current architecture:
Telegram Bot -> Cloudflare Worker -> Google Apps Script standalone -> Google Sheet -> Telegram reply

Final CLI deploy workflow:
- Edit Apps Script locally in:
  apps-script-live/AIRO_Finance_Multitab_Final_v1.js
- Deploy from terminal with:
  scripts/personal-workflow/airo_apps_script_deploy.sh
- This command pushes source, creates a new Apps Script version, and updates the existing Web App deployment.
- Manual Apps Script UI deployment is no longer required unless the Web App deployment ID changes.

Important:
- Some maintenance functions may still need to be run manually from Apps Script UI unless a dedicated terminal runner or Telegram admin command is later added.
- Current deploy from terminal is confirmed working.
- Current function-run from terminal is not the default workflow yet because clasp run-function requires additional Apps Script Execution API setup.

Validated major features:
- Direct Telegram finance input works.
- Multi-tab routing works.
- n8n_Transactions legacy staging removed.
- Airo_Schema_Audit legacy tab removed.
- Cash Ledger supports cash umum and cash bensin.
- Cash inflow phrases such as "cash masuk", "cash terima", "dapat cash", and "uang masuk cash" are treated as cash inflow.
- Review Queue approved rows can be processed.
- Review Queue onEdit automation exists.
- Gold asset parser supports buy/add and sell.
- Gold Ledger uses 24K-equivalent grams for valuation consistency.
- ANTAM/Logam Mulia price is fetched daily and synced to Aset!F12.
- Dashboard contains final Net Worth & Home Equity panel.
- Legacy Aset Net Worth panel is hidden and not the source of truth.
- Source of truth for Net Worth is Dashboard.

Validated safeguards:
- Telegram duplicate retry is guarded by _AIRO_Dedupe_Log.
- Same Telegram update/message should not double append.
- CLI deploy helper is:
  scripts/personal-workflow/airo_apps_script_deploy.sh

Credit Card final behavior:
- "cc beli ..." and "cc bayar pdam ..." are treated as new CC spending.
- New CC spending increases Total Belanja CC and starts as status_pocket_blu = ⏳ Belum.
- "bayar cc ..." is treated as BLU pocket transfer/payment for an existing CC item.
- "bayar cc ..." should not create a new CC purchase row.
- It should update the matching CC row to status_pocket_blu = ✅ Sudah and fill transferred_at.
- CC dropdown labels must match the sheet:
  ✅ Sudah
  ⏳ Belum
  ⚠️ Sebagian
- Maintenance function for old values:
  fixCreditCardStatusDropdownValues

Credit Card period:
- Current intended cycle pattern:
  16 previous month to 15 current month.
- Example:
  TOKPED_CC_2026-05 = 16 April 2026 to 15 May 2026.

Hutang final behavior:
- "bayar hutang ke [nama] [amount]" writes payment history and updates the matching master row.
- total_dibayar increases.
- sisa_hutang decreases.
- status becomes lunas when remaining debt reaches zero.
- Names must match or partially match master names such as "mamak egit" and "bapak egit".

House / Net Worth baseline:
- Nilai Rumah Pasar: Rp166.000.000
- Haircut Konservatif: 5%
- Sisa Pokok Rumah: use latest conservative user value until exact principal is known.
- Dashboard shows:
  Net Worth Likuid
  Ekuitas Rumah
  Net Worth Total

Known final verification checklist:
1. Confirm Credit Card summary:
   Total Belanja CC, Sudah Transfer BLU, and Sisa Belum Transfer.
2. Confirm Hutang master:
   total_dibayar and sisa_hutang update correctly for mamak/bapak.
3. Clean QA_TEST / QA_* rows if needed.
4. Run final compact regression after cleanup.


---

# Update - Carryover Pointer 2026-05-14

Carry-over file added:
docs/AIRO_FINANCE_CARRYOVER_2026-05-14.md

New chat must read this file before continuing AIRO Finance.
