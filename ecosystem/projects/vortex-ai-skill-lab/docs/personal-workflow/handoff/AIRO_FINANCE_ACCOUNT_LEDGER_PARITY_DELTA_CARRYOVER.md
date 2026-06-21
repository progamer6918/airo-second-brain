# AIRO Finance — Account Ledger Parity Delta Carryover

Status: CHECKPOINT / CARRYOVER
Date: 2026-05-17
Repo: /home/egitaristorandas/vortex-ai-skill-lab
Branch: main

## Latest verified Git checkpoint

Latest commit before this handoff:

- `e5bc28e feat(airo-finance): add cash parity detail audit command`

Latest Apps Script deploy:

- Version: `108`
- Deployment ID: `AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA`
- Deploy method: official script only
- Script: `bash scripts/personal-workflow/airo_apps_script_deploy.sh`

Do not use `clasp deploy -d`.

## Architecture wording

Correct architecture:

- `📒 Account Ledger` is the maturing account mutation center.
- `💵 Cash Ledger` is a temporary compatibility layer.
- Current live Telegram may still write or report through Cash Ledger for compatibility.
- Do not describe Cash Ledger as the final main ledger.
- Do not delete Cash Ledger yet.
- Do not delete `_AIRO_Dedupe_Log`.
- `💳 Credit Card`, `🤝 Hutang`, and `🥇 Aset` must not be force-merged into Account Ledger.

## Completed in this session

### Formula reporting migration

Dashboard and Monthly Review formulas were migrated from `💵 Cash Ledger` to `📒 Account Ledger` for account `Cash`.

Completed commits:

- `d797797 fix(airo-finance): read cash reporting from account ledger`
- `b632e05 feat(airo-finance): add admin refresh for cash reporting formulas`
- `78b1564 feat(airo-finance): add cash reporting formula audit command`
- `26b108a fix(airo-finance): make cash reporting formula audit robust`

Validation:

- Telegram command `admin refresh cash reporting` responded.
- Telegram command `admin audit cash reporting formulas` returned:
  - Monthly B6 uses Account Ledger: true
  - Monthly E6 uses Account Ledger: true
  - Monthly B8 formula exists: true
  - Dashboard D17 uses Account Ledger: true

Conclusion:

- Phase A reporting migration is PASS.

### Parity audit tooling

Completed commits:

- `2e403c3 feat(airo-finance): add cash ledger parity audit command`
- `f0734cb fix(airo-finance): make cash parity audit header-based`
- `e5bc28e feat(airo-finance): add cash parity detail audit command`

Validation command:

- `admin audit cash parity`

Latest parity result:

- Cash Ledger in: Rp142000
- Cash Ledger out: Rp30000
- Cash Ledger net: Rp112000
- Account Ledger Cash in: Rp342000
- Account Ledger Cash out: Rp30000
- Account Ledger Cash net: Rp312000
- Delta net: Rp200000
- Status: CHECK

Detail audit command:

- `admin audit cash parity detail`

Detail result found likely duplicate Account Ledger inflows:

- Account Ledger row #18: Rp100000, source tab `Cash`, text `cash diterima 100rb dari blu`
- Account Ledger row #16: Rp100000, source tab `💵 Cash Ledger`, text `cash diterima 100rb dari blu`

Cash Ledger inflows shown:

- Rp10000, `cash diterima 10rb`
- Rp24000, `cash diterima 24rb dr ganti makan`
- Rp5000, `cash bensin diterima 5rb dr tf`
- Rp103000, `cash diterima 103rb dari tf hari ini`

## Current root cause analysis

The likely root cause is an ID mismatch between internal transfer rows and Cash Ledger compatibility/backfill rows.

Internal transfer generation:

- `writeInternalTransferToAccountLedger_` generates:
  - base `sharedTxnId`
  - source outflow row with `rowId = sharedTxnId + ":out"`
  - target inflow row with `rowId = sharedTxnId + ":in"`

For `cash diterima 100rb dari blu`:

- Account Ledger internal transfer inflow uses `entry_id = sharedTxnId + ":in"`.
- Cash Ledger compatibility row uses the base `sharedTxnId`.

Backfill/reconciliation from Cash Ledger to Account Ledger may later check only for exact `entry_id === sharedTxnId`.

Because Account Ledger already has `sharedTxnId + ":in"`, but not base `sharedTxnId`, the backfill can assume the Cash Ledger row is missing and append another Account Ledger row with:

- `source_tab = 💵 Cash Ledger`
- same amount
- same raw text

This creates double-counting in Account Ledger Cash inflow.

## Important source locations

Main Apps Script source:

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs`

Live Apps Script source:

- `apps-script-live/AIRO_Finance_Multitab_Final_v1.js`

Relevant functions:

- `writeRouted_`
- `detectInternalTransfer_`
- `writeInternalTransferToAccountLedger_`
- `writeCashLedger_`
- `writeAccountLedgerMirror_`
- Cash Ledger to Account Ledger backfill/sync block around Account Ledger backfill functions
- Account Ledger audit/cleanup functions

## Next official item

Patch prevention before cleanup.

Recommended next step:

1. Audit the Cash Ledger to Account Ledger backfill dedupe logic.
2. Patch dedupe so Cash Ledger compatibility rows from internal transfers do not create duplicate Account Ledger rows when matching `sharedTxnId + ":in"` or `sharedTxnId + ":out"` already exists.
3. Commit, push, sync live, deploy.
4. Run `admin audit cash parity detail` again.
5. Only after prevention is deployed, add/run a targeted cleanup for the duplicate row(s).

Do not cleanup first.

## Safety boundaries

Continue following these boundaries:

- Terminal output is source of truth.
- Do not invent status, commit hash, deploy version, or spreadsheet state.
- Do not open or paste `.env`, token, secret, private key, cookie, session, API key, credential, OAuth token, or browser profile contents.
- Do not commit local DBs, receipts, OAuth tokens, OAuth clients, credentials, runtime state, or private files.
- Do not touch EarnsAI, runtime, trading, or live trading files.
- Do not perform Google writes unless approval-gated.
- Do not use `clasp deploy -d`.
- Use official deploy script only:
  `bash scripts/personal-workflow/airo_apps_script_deploy.sh`

## Carryover prompt for next chat

Paste this into a new chat:

```text
Lanjut project WSL/GitHub AIRO Finance.

Repo:
/home/egitaristorandas/vortex-ai-skill-lab

Branch:
main

Latest stable/carryover handoff:
docs/personal-workflow/handoff/AIRO_FINANCE_ACCOUNT_LEDGER_PARITY_DELTA_CARRYOVER.md

Read order:
1. docs/personal-workflow/AIRO_CHAT_RULES.md
2. docs/personal-workflow/handoff/AIRO_FINANCE_ACCOUNT_LEDGER_V101_STABLE_HANDOFF.md
3. docs/personal-workflow/handoff/AIRO_FINANCE_ACCOUNT_LEDGER_PARITY_DELTA_CARRYOVER.md

Current status:
- Account Ledger is the maturing account mutation center.
- Cash Ledger is only a temporary compatibility layer.
- Formula reporting migration is PASS.
- Monthly Review and Dashboard now read Account Ledger for Cash.
- Apps Script has been deployed through version 108.
- Latest functional commit before carryover: e5bc28e feat(airo-finance): add cash parity detail audit command.
- Parity audit result is CHECK because Account Ledger Cash net exceeds Cash Ledger net by Rp200.000.
- Detail audit found likely duplicate rows for `cash diterima 100rb dari blu`:
  - #18 Rp100000 [Cash]
  - #16 Rp100000 [💵 Cash Ledger]

Root cause hypothesis:
- Internal transfer writes Account Ledger row with `sharedTxnId + ":in"`.
- Cash Ledger compatibility writes base `sharedTxnId`.
- Backfill/sync may not recognize `sharedTxnId + ":in"` as matching base `sharedTxnId`, so it appends a duplicate Account Ledger row from Cash Ledger.

Official next item:
Patch prevention in the Cash Ledger to Account Ledger backfill/dedupe logic before doing any cleanup.

Rules:
- Fast-track mode is active, but do not bypass safety.
- Give one target step at a time.
- Use terminal output as source of truth.
- Do not read the whole repo.
- Scope 1 file unless explicitly approved.
- Validate git status, diff stat, diff check.
- Do not commit/push/deploy without explicit approval or user-approved fast-track step.
- Do not use `clasp deploy -d`.
- Use official deploy script only.
- Do not open secrets/credentials/runtime/EarnsAI/trading files.

Start by giving:
Indeks kepadatan chat:
Status konteks project:
Repo aktif:
Branch aktif:
Progress project:
Current phase:
Milestone sekarang:
Target micro-step:

Then provide a small read-only audit command for the Cash Ledger to Account Ledger backfill dedupe logic.
```
