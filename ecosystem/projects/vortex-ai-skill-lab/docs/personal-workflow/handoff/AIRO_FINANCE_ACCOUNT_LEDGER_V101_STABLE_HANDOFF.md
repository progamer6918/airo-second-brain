# AIRO Finance ? Account Ledger v101 Stable Handoff

Status: STABLE CHECKPOINT
Date: 2026-05-17
Repo: /home/egitaristorandas/vortex-ai-skill-lab
Branch: main

## Latest verified Git checkpoint

Latest pushed commit:

- `04be6e9 fix(airo-finance): use explicit in-out mapping for account ledger mirror`

GitHub push status:

- DONE
- `origin/main` verified at commit `04be6e9b6ee8e2ce825efc0d12be0710d1dac324`

## Apps Script deployment

Apps Script deploy status:

- DONE
- Deployment method: official project script only
- Script used: `bash scripts/personal-workflow/airo_apps_script_deploy.sh`
- Apps Script version: `101`
- Deployment ID: `AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA`

Do not use `clasp deploy -d` for the main webhook deployment.

## Telegram live test

Telegram test status:

- PASS

Test message:

- `tes akun cash keluar 1000 beli kopi`

Bot response:

- `? Tercatat ke Google Sheet.`
- Rencana tab: `?? Cash Ledger`
- Ditulis ke: `?? Cash Ledger`
- Akun: `Cash`
- Kategori: `Makan`
- Nominal: `Rp1000`

Observed ledger result:

- Cash Ledger received the transaction through the existing live routing.
- Account Ledger mirror received the transaction.
- Account Ledger outflow was correct:
  - `amount_in`: blank
  - `amount_out`: `Rp 1.000`
  - `type`: `expense`
  - `category`: `Makan`
  - `source_tab`: `?? Cash Ledger`
  - balance formula populated.

## Correct architecture wording

Use this wording going forward:

- `?? Account Ledger` is the main account mutation ledger being matured and is the intended center for daily account movements.
- `?? Cash Ledger` is a temporary compatibility layer because parts of the existing Telegram/live workflow still write there first.
- Current live behavior may still show Telegram output as written to `?? Cash Ledger`, but this is implementation compatibility, not the final architecture direction.
- Cash Ledger should not be described as the final main ledger.
- Cash Ledger may be hidden later after dependencies are audited.
- Cash Ledger must not be deleted before auditing dependencies, dashboard formulas, dedupe behavior, backfill, reporting, and compatibility paths.
- `?? Credit Card`, `?? Hutang`, and `?? Aset` must not be force-merged into Account Ledger.
- `_AIRO_Dedupe_Log` must not be deleted. At most, hide it after explicit audit and approval.

## What changed in commit 04be6e9

The Account Ledger mirror logic was improved:

1. `entry_id` now prioritizes `common.rowId`.
2. Inflow/outflow mapping is explicit:
   - inflow: `income`, `transfer_in`, `cash_in`
   - outflow: `expense`, `transfer_out`, `cash_out`
   - fallback to `isCashInflowText_(rawText)` only when type is not explicit.
3. `linked_txn_id` is no longer forced to duplicate `rowId`.

Purpose:

- Prevent clear outflow transactions from being misclassified as inflow due to ambiguous raw text.
- Keep `entry_id` and `linked_txn_id` semantically cleaner.
- Support the Account Ledger as the maturing source for account mutation history.

## Important source files

Primary source file:

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs`

Live Apps Script source folder:

- `apps-script-live/`

Live file synced before deploy:

- `apps-script-live/AIRO_Finance_Multitab_Final_v1.js`

Deploy script:

- `scripts/personal-workflow/airo_apps_script_deploy.sh`

Chat rules:

- `docs/personal-workflow/AIRO_CHAT_RULES.md`

## Latest validation completed

Completed checks:

- `git status --short`
- `git diff --stat`
- `git diff --check`
- `python3 scripts/personal-workflow/airo_approval_review.py list --status pending --compact`
- `python3 scripts/personal-workflow/airo_google_fallback.py status`
- source vs live sync check with `diff -q`
- official Apps Script deploy
- Telegram live test

Validation result:

- PASS

## Safety boundaries

Continue following these boundaries:

- Terminal output is the source of truth.
- Do not invent roadmap, phase, commit hash, file status, or deploy status.
- Do not read or paste `.env`, token, secret, private key, cookie, session, API key, credential, OAuth token, or browser profile contents.
- Do not commit local DBs, receipts, OAuth tokens, OAuth clients, credentials, runtime state, or private files.
- Do not touch EarnsAI, runtime, trading, or live trading files unless explicitly requested.
- Do not perform Google writes unless approval-gated.
- Do not commit, push, deploy, delete, rename, or patch large areas without explicit approval.
- Use one small step at a time.

## Recommended next item

Next recommended task:

- Decide the next small Account Ledger maturation step.

Safe candidates:

1. Audit remaining dashboard/formula dependencies on `?? Cash Ledger`.
2. Audit whether new cash transactions can route directly to `?? Account Ledger` while preserving Cash Ledger compatibility.
3. Add a clear UI/report note that `?? Account Ledger` is the account mutation center and `?? Cash Ledger` is compatibility.
4. Review whether Cash Ledger can be hidden later, after dependency audit passes.

Do not start a large milestone without a fresh source-of-truth audit.
