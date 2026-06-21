# AIRO Finance Sheet Workflow v1.2 — YOLO Carryover

Date: 2026-05-20
Repo: /home/egitaristorandas/vortex-ai-skill-lab
Branch: main
Parent project: Airo Personal Workflow
Current workstream: AIRO Finance Sheet Workflow v1.2
Formal scope: Telegram Finance to Google Sheet Finance

## Project Name Lock

Current project name: AIRO Finance Sheet Workflow v1.2

Parent project: Airo Personal Workflow

Important distinction:
- Airo Personal Workflow main project is already complete through Phase 8.
- Current work is a finance v1.2 scope extension / workstream.
- This is not Phase 9.
- Do not create Phase 9 unless the user explicitly expands the project scope.

Official roadmap sources:
- docs/personal-workflow/AIRO_PROJECT_INDEX.md
- docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md
- docs/personal-workflow/integration/AIRO_TELEGRAM_OPTION_A_SINGLE_FRONT_DOOR_PLAN.md

## Operating Mode

Mode: YOLO execution mode.

Meaning:
- Fast-track execution.
- Prefer direct WSL commands.
- Do not over-interview once scope is clear.
- Use terminal output, GitHub/repo, and Telegram replies as source of truth.
- Commit and push after PASS.
- Keep commands paste-safe.
- Avoid unnecessary fragmentation.

YOLO does not bypass safety.

Safety boundaries:
- Do not request or expose .env, tokens, secrets, API keys, OAuth tokens, private keys, cookies, sessions, credentials, or browser profiles.
- Do not touch EarnsAI trading runtime.
- Do not enable live trading, real-money trading, private exchange API, or real-money execution.
- Do not commit local DB, receipts, runtime state, OAuth/client files, credentials, private config, or secrets.
- Do not hard-delete finance records.
- Do not patch/restart OpenClaw core or services without explicit approval.
- Do not use clasp deploy -d.
- If Apps Script deploy is needed, use only: bash scripts/personal-workflow/airo_apps_script_deploy.sh

## Required Response Header in New Chat

Every assistant response must start with:

Indeks kepadatan chat:
Status konteks project:
Repo aktif:
Branch aktif:
Progress project:
Current phase:
Milestone sekarang:
Target micro-step:

Context meter rules:
- In a new chat, start around 5/100 to 10/100.
- Do not copy old meter number.
- Increase based on actual chat length, terminal logs, file outputs, and complexity.
- After 70/100, remind user about checkpoint.
- After 80/100, do not start large new tasks unless user explicitly says YOLO/carryover is acceptable.

## Source of Truth Rules

- Terminal output is primary source of truth.
- GitHub/repo is long-term source of truth.
- Telegram bot replies are runtime validation source of truth.
- Chat is only execution, debugging, planning, and discussion.
- If information is not in terminal output, repo files, or Telegram output, do not invent it.
- Ask for a snapshot or inspect relevant files.
- Do not claim commit, push, deploy, or spreadsheet state unless terminal/Telegram proves it.

## Latest Verified Repo State Before This Carryover

Latest verified workflow commit before this docs carryover:

cbe4f89 test(airo-finance): cap cash rows audit output

Verified state before carryover:
- Branch: main
- Working tree: clean
- origin/main: cbe4f89e296d946524ef005446886c1783e45a9e
- ahead/behind: 0/0
- Latest Apps Script deploy: version 125

Latest verified Apps Script deployment:
- Deployment ID: AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA
- Version: 125
- Deployment method: bash scripts/personal-workflow/airo_apps_script_deploy.sh

## Roadmap Lock

Current workstream: AIRO Finance Sheet Workflow v1.2.

Priority 1 — Preserve current PASS state.
Purpose:
- Do not break Transactions, Credit Card, Sync Log, or Aset.
- Keep existing stable behavior working while patching other routes.

Priority 2 — Cash Ledger route/dry-run mapping and Review Queue ambiguity route.
Purpose:
- Stabilize Cash Ledger as compatibility layer.
- Keep Account Ledger as mutation center.
- Ensure cash and internal transfers do not create parity deltas or wrong amount direction.
- Ensure ambiguous parser output goes to Review Queue or asks clarification instead of unsafe auto-write.

Priority 3 — Cicilan Rumah route/dry-run mapping and Hutang route/dry-run mapping.
Purpose:
- Prepare monthly Cicilan Rumah and Hutang flows.
- Avoid overengineering because user uses these about once per month.
- Keep it safe, auditable, and stable.

Priority 4 — Monthly Review reporting refresh and Dashboard/status UX summary.
Purpose:
- Keep reporting formulas healthy.
- Build Dashboard Sheet as a personal finance snapshot/status page, not a PDF export.

Future-only unless explicitly approved:
- Budgeting expansion
- Investment expansion
- New tabs
- Broad parser refactor
- OpenClaw core patch
- Service restart

## Current Position

Current position:
AIRO Finance Sheet Workflow v1.2
Priority 2A — Cash Ledger route and dry-run mapping

Current milestone:
Finish remaining internal transfer matrix and final audit.

Already validated PASS:
- Cash Umum inflow
- Cash Bensin outflow
- BCA to Blu
- Blu to Cash
- Cash to Blu
- Cash Ledger amount_in/amount_out sync
- Account Ledger :out/:in transfer pairs
- Cash parity Delta net Rp0
- Cash rows audit output no longer silent after cap patch

Remaining Priority 2A transfer matrix:
- Blu to BCA
- BCA to Cash
- Cash to BCA
- Final cash parity audit
- Final reporting formula audit
- Final cash header audit

After Priority 2A:
Priority 2B — Review Queue ambiguity route

## Architecture Lock

- Account Ledger is the mutation center.
- Cash Ledger is a compatibility layer.
- Cash Ledger must not be deleted/hidden yet.
- _AIRO_Dedupe_Log must not be deleted.
- Credit Card, Hutang, and Aset must not be forcibly merged into Account Ledger.
- Dashboard and Monthly Review should read Account Ledger where appropriate.
- Do not refactor Dashboard broadly unless audit proves it is needed.

## Relevant Commits

0573f4c test(airo-finance): include phase d cash rows in audit
0bab8e9 test(airo-finance): add account ledger row audit command
e706c1e fix(airo-finance): respect parsed cash transfer direction
ad5f5f8 test(airo-finance): include blu cash transfer rows in audits
e10406c test(airo-finance): include cash blu transfer rows in audits
cbe4f89 test(airo-finance): cap cash rows audit output

Key behavior:
- admin audit cash rows includes Phase D/Cash transfer test keywords.
- admin audit account rows can display internal transfer Account Ledger rows.
- writeCashLedger_ respects parsed transfer direction via isCashInflowData_.
- Transfer to Cash can correctly become Cash Ledger inflow.
- Cash rows audit output is capped to avoid Telegram silent/no response due to long message.

## Runtime Validation Completed

Cash Umum inflow:
- Test: cash diterima 1000 test phase d cash umum
- Result: Cash Ledger inflow, Account Ledger Cash Umum inflow, cash parity PASS.

Cash Bensin outflow:
- Test: cash bensin keluar 1000 test phase d cash bensin
- Result: Cash Ledger outflow, Account Ledger Cash Bensin outflow, cash parity PASS.

BCA to Blu:
- Test: transfer 1000 dari bca ke blu test phase d internal transfer bca blu
- Result: Account Ledger BCA amount_out Rp1.000, Blu amount_in Rp1.000, pair linked via :out/:in, cash parity PASS.

Blu to Cash:
- Test: transfer 1000 dari blu ke cash test phase d internal transfer blu cash
- Result: Account Ledger Blu amount_out Rp1.000, Cash Umum amount_in Rp1.000, Cash Ledger amount_in Rp1.000 type transfer_in, cash parity PASS.

Cash to Blu:
- Test: transfer 1000 dari cash ke blu test phase d internal transfer cash blu
- Result: Account Ledger Cash Umum amount_out Rp1.000, Blu amount_in Rp1.000, Cash Ledger amount_out Rp1.000 type transfer_out, cash parity PASS.

Latest known cash parity after Cash to Blu:
- Cash Ledger in: Rp130000
- Cash Ledger out: Rp81000
- Cash Ledger net: Rp49000
- Account Ledger Cash in: Rp130000
- Account Ledger Cash out: Rp81000
- Account Ledger Cash net: Rp49000
- Delta net: Rp0
- Status: PASS

## User Decisions for Priority 3

Cicilan Rumah:
- Used once per month, usually early month.
- Strategy: audit structure first, then implement payment recording plus update installment number.
- Do not overengineer.

Hutang:
- Used once per month.
- Strategy: focus on payment recording.
- Keep master/payment history safe.
- Do not create complex automation unless audit proves it is needed.

## User Decisions for Priority 4

Monthly Review:
- Keep formula healthy.
- Do not do broad refactor unless audit proves it is needed.

Dashboard/status UX:
- Final output should be a Google Sheet Dashboard page, not PDF export.
- It should visually feel like the provided Airo_Finance_Dashboard.pdf.
- It should be a clean, formal, premium one-page personal finance snapshot.
- It should include finance summary plus small AIRO Finance system status.
- System status should be small, not a large technical panel.

Desired Dashboard content:
- Net Worth total
- Likuid plus ekuitas rumah
- Saldo akun
- Cashflow bulan ini
- Cicilan Rumah
- Hutang aktif
- Kartu Kredit
- Aset emas
- Small AIRO Finance status area

Dashboard source data readiness:
- Cash/Account Ledger: increasingly stable.
- Cicilan Rumah: must be audited in Priority 3.
- Hutang: must be audited in Priority 3.
- Credit Card: roadmap says core-ready/Tokopedia CC PASS, but still needs last regression before Dashboard final.
- Aset: asset sync patched, but still needs regression before Dashboard final.
- Monthly Review: cash reporting formulas have passed; final formula health still needed.

## User Preference for Commands

- Use WSL command only.
- Stop giving Antigravity prompts unless user explicitly asks.
- Commands should copy output automatically using tee + clip.exe.
- User prefers fast execution and fewer unnecessary questions.
- Still explain purpose briefly before risky changes.

## Next Safe Step in New Chat

Start with snapshot:

cd /home/egitaristorandas/vortex-ai-skill-lab

Then run:
- git branch --show-current
- git status --short
- git log -1 --oneline
- git ls-remote origin refs/heads/main
- git rev-list --left-right --count origin/main...HEAD

Then continue from:
Priority 2A — Finish remaining transfer matrix:
1. Blu to BCA
2. BCA to Cash
3. Cash to BCA
4. Final cash parity/reporting/header audits

Do not restart from scratch.

## New Chat Prompt

Saya ingin melanjutkan project WSL/GitHub saya.

Nama project sekarang:
AIRO Finance Sheet Workflow v1.2

Parent project:
Airo Personal Workflow

Scope formal:
Telegram Finance to Google Sheet Finance

Saya newbie, jadi pandu saya step-by-step. Jangan mulai dari nol dan jangan mengarang status project.

Sumber kebenaran:
- Terminal output adalah sumber kebenaran utama.
- GitHub/repo adalah lemari online/source of truth.
- Telegram bot replies adalah runtime validation source of truth.
- Chat hanya tempat eksekusi, diskusi, debugging, dan perencanaan.
- Jika informasi tidak ada di terminal output, Telegram output, atau file repo, jangan menebak. Minta snapshot terminal atau file relevan.

Repo:
`/home/egitaristorandas/vortex-ai-skill-lab`

Branch:
`main`

Project state:
- Airo Personal Workflow main project sudah Phase 8 complete.
- Kerja sekarang adalah AIRO Finance Sheet Workflow v1.2.
- Ini scope extension / finance workstream, bukan Phase 9.
- Jangan create Phase 9.
- Jangan nambah roadmap sendiri.
- Roadmap resmi ada di:
  - docs/personal-workflow/AIRO_PROJECT_INDEX.md
  - docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md

Mode eksekusi:
YOLO execution mode.

Makna YOLO:
- Fast-track.
- Command WSL langsung.
- Jangan kebanyakan tanya kalau scope jelas.
- Commit dan push setelah PASS.
- Tetap gunakan terminal/GitHub/Telegram sebagai source of truth.
- Tetap jangan bypass safety.

Aturan keamanan:
- Jangan minta saya paste .env, token, secret, private key, cookie, session, API key, OAuth token, credential, atau data sensitif.
- Jangan aktifkan live trading, private exchange API, atau real-money trading.
- Jangan sentuh EarnsAI, runtime trading, local DB, receipts, OAuth files, credential files, atau private config kecuali saya minta eksplisit.
- Jangan commit local DB, token, credential, OAuth, runtime state, receipt, private config, atau file sensitif.
- Jangan hard-delete finance records.
- Jangan patch/restart OpenClaw core/service tanpa approval eksplisit.
- Jangan pakai clasp deploy -d.
- Kalau perlu deploy Apps Script, gunakan bash scripts/personal-workflow/airo_apps_script_deploy.sh

Aturan cara kerja:
- Berikan satu micro-step yang jelas.
- Untuk command, berikan command paste-safe.
- Kalau command panjang, jelaskan fungsinya dengan bahasa pemula.
- Command WSL harus copy output otomatis pakai tee + clip.exe.
- Jangan mengubah file, commit, push, deploy, cleanup rows, atau delete rows tanpa menjelaskan tujuan command.
- Jangan patch buta. Audit dulu kalau akar masalah belum jelas.
- Boleh fast-track commit/push/deploy jika scope jelas, diff aman, dan user sudah dalam mode YOLO.

Aturan konteks:
- Indeks kepadatan chat adalah estimasi seberapa penuh chat saat ini, bukan progress project.
- Di chat baru, mulai dari 5/100 sampai 10/100.
- Jangan menyalin angka indeks dari chat lama.
- Naikkan angka hanya berdasarkan panjang chat ini, jumlah file/log/output terminal yang saya kirim, dan kompleksitas konteks.
- Setelah indeks chat 70/100 ke atas, ingatkan saya untuk checkpoint.
- Setelah indeks chat 80/100 ke atas, jangan mulai task besar kecuali saya eksplisit minta YOLO/carryover.

Setiap respons wajib mulai dengan format ini:
Indeks kepadatan chat:
Status konteks project:
Repo aktif:
Branch aktif:
Progress project:
Current phase:
Milestone sekarang:
Target micro-step:

Current project position:
AIRO Finance Sheet Workflow v1.2
Priority 2A — Cash Ledger route and dry-run mapping

Architecture lock:
- Account Ledger adalah mutation center.
- Cash Ledger adalah compatibility layer.
- Cash Ledger belum boleh dihapus.
- _AIRO_Dedupe_Log belum boleh dihapus.
- Credit Card, Hutang, dan Aset tidak boleh dipaksa merge ke Account Ledger.
- Dashboard dan Monthly Review harus tetap membaca sumber yang benar.

Latest known code/workflow commit before carryover doc:
cbe4f89 test(airo-finance): cap cash rows audit output

Latest verified Apps Script deploy:
Version 125

Validated PASS:
- Cash Umum inflow
- Cash Bensin outflow
- BCA to Blu
- Blu to Cash
- Cash to Blu
- Cash parity Delta net Rp0
- Account Ledger :out/:in pairs valid
- Cash Ledger amount_in/amount_out direction valid
- Cash rows audit output capped so Telegram no longer silent

Remaining Priority 2A:
1. Blu to BCA
2. BCA to Cash
3. Cash to BCA
4. Final cash parity audit
5. Final reporting formula audit
6. Final cash header audit

After Priority 2A:
Priority 2B — Review Queue ambiguity route

Priority 3 user decisions:
- Cicilan Rumah dipakai awal bulan sekali.
- Cicilan Rumah strategy: audit struktur dulu, lalu catat pembayaran + update cicilan keberapa.
- Hutang dipakai sebulan sekali.
- Hutang strategy: fokus catat pembayaran hutang.
- Jangan overengineer Priority 3.

Priority 4 user decisions:
- Monthly Review: cukup pastikan formula tidak rusak.
- Dashboard/status UX: buat Google Sheet Dashboard seperti referensi PDF, bukan export PDF.
- Style dashboard: clean, formal, premium.
- Dashboard isi: Net Worth, saldo akun, cashflow, Cicilan Rumah, Hutang aktif, Kartu Kredit, Aset Emas, small AIRO Finance status.

Mulai dari snapshot terminal kecil dulu, lalu lanjutkan Priority 2A. Jangan mulai dari nol.

## Addendum — Credit Card Cycle Decision PASS

Credit Card billing cycle has been validated as PASS.

Decision file:

- `docs/personal-workflow/integration/AIRO_CREDIT_CARD_CYCLE_DECISION_V1_2.md`

Final CC cycle rule:

- Statement cycle starts on day 16.
- Statement cycle ends on day 15.
- 16 Apr – 15 May = TOKPED_CC_2026-05.
- 16 May – 15 Jun = TOKPED_CC_2026-06.
- Due date for 16 Apr – 15 May is 30 May.
- Transactions after 15 May must enter the next cycle, not the previous payable bill.

Runtime proof:

- `admin fix cc tanggal` returned Rows updated: 9.
- `admin audit cc cycles` returned:
  - Row #11, 15/05/2026 → TOKPED_CC_2026-05, 2026-04-16 – 2026-05-15.
  - Row #12, 20/05/2026 → TOKPED_CC_2026-06, 2026-05-16 – 2026-06-15.

User decision:

- Dashboard should separate:
  1. Tagihan Jatuh Tempo
  2. Periode Berjalan / Unbilled
- Dashboard shows summary only.
- Credit Card tab shows detail transactions.
- “Belum ke Blu” means the money for paying the CC bill has not yet been prepared in the dedicated Pocket Blu for CC payment.

## Addendum — Active Focus Lock: Credit Card Cycle Only

Current active focus is strictly Credit Card cycle validation/checkpoint.

Focus doc:

- `docs/personal-workflow/integration/AIRO_CREDIT_CARD_CYCLE_FOCUS_LOCK_2026_05_20.md`

Allowed within current focus:

- `💳 Credit Card`
- `billing_cycle_id`
- `billing_start`
- `billing_end`
- `statement_month`
- due date 30
- Tagihan Jatuh Tempo
- Periode Berjalan / Unbilled
- `status_pocket_blu`
- Belum ke Blu / Pocket Blu CC allocation
- `admin fix cc tanggal`
- `admin audit cc cycles`
- Dashboard section only if directly related to Credit Card cycle

Skip unless explicitly approved:

- Review Queue
- Cash Ledger
- Account Ledger transfer matrix
- Cicilan Rumah
- Hutang
- Aset
- Monthly Review general formulas
- Dashboard general redesign
- Any non-CC-cycle roadmap item

Important paste-output rule:

If the user pastes output that does not appear relevant to the current Credit Card cycle focus, do not continue automatically. Ask first whether it is the correct output for the current step or whether the user intended to change scope.

Out-of-focus patch note:

- `df7d20d fix(airo-finance): route ambiguous parser output to review queue` was deployed but is OUT-OF-FOCUS / NOT VALIDATED.
- Keep the commit.
- Do not claim Review Queue PASS.
- Do not continue Review Queue unless explicitly approved.
