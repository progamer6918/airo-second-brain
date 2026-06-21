Lanjut project Airo Personal Workflow / Telegram Finance → Google Sheet Finance.

Repo:
- GitHub: progamer6918/vortex-ai-skill-lab
- Branch: main
- Repo URL: https://github.com/progamer6918/vortex-ai-skill-lab.git
- Local repo dir default: ~/vortex-ai-skill-lab

Wajib:
GitHub adalah source of truth. Jangan mengandalkan memory chat saja.

Sebelum memberi command repo apa pun, baca source-of-truth dari GitHub dengan repo bootstrap yang benar:
- Jangan berasumsi terminal saya sedang di folder repo.
- Command harus clone repo kalau belum ada.
- Command harus cd ~/vortex-ai-skill-lab sebelum git/status/sed/test/commit/push.
- Jangan jalankan git command dari folder ~.

Source-of-truth read order minimum:
1. docs/personal-workflow/AIRO_PROJECT_INDEX.md
2. docs/personal-workflow/AIRO_CHAT_RULES.md
3. docs/personal-workflow/AIRO_CONTINUITY_PACK.md
4. docs/personal-workflow/AIRO_NEW_CHAT_BOOTSTRAP_TEMPLATE.md
5. docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_PHASE_8_HANDOFF.md
6. docs/personal-workflow/integration/AIRO_TELEGRAM_OPTION_A_SINGLE_FRONT_DOOR_PLAN.md
7. docs/personal-workflow/integration/AIRO_TELEGRAM_OPTION_A_NOTION_COMMAND_GUARD_LOG.md
8. docs/personal-workflow/integration/AIRO_TELEGRAM_OPTION_A_PERSISTENT_DB_ROUTE_LOG.md
9. docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md
10. docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_HANDOFF.md

Latest project status:
- MVP v0.1: DONE
- Phase 2: DONE
- Phase 3: DONE
- Phase 4: DONE
- Phase 5: DONE
- Phase 6: DONE
- Phase 7: DONE
- Phase 8 complete/stable closeout: DONE
- Final stable tag: airo-personal-workflow-phase-8-complete
- Telegram finance no longer goes to Notion by default.
- Finance intents route to Airo Personal Workflow.
- Current persistent local DB:
  /home/egitaristorandas/.local/share/airo-personal-workflow/airo.sqlite3
- Existing local DB known tables include:
  accounts, approval_queue, attachments, audit_log, conflicts, installment_payments, installments, sync_jobs, transactions.
- Restricted untracked paths may still appear:
  EarnsAI, runtime, trading.
  Do not touch or commit them.

Current Google Sheet Finance design status:
- Google Sheet Finance Balanced+ v1.1.8-final design is stable.
- Final Apps Script has been ramped into one setup script:
  Airo Personal Finance Google Sheets Setup Script v1.1.8-final.
- Main Apps Script function:
  setupAiroFinance
- The final sheet has 11 tabs:
  1. 🏠 Dashboard
  2. 💸 Transactions
  3. 💵 Cash Ledger
  4. 💳 Credit Card
  5. 🏠 Cicilan Rumah
  6. 🤝 Hutang
  7. 🥇 Aset
  8. 📅 Monthly Review
  9. 🧾 Review Queue
  10. ⚙️ Settings
  11. 🔄 Sync Log

Important design choices:
- Dashboard is formula-driven and reads from source tabs.
- Cash has separate Cash Ledger with cash sessions and cash entries.
- Tokopedia Credit Card has its own tab and tracks BLU BCA pocket readiness.
- Cicilan rumah is 53/120 as of May 2026, standard Rp1.543.000, paid Rp1.570.000, due date every 7th.
- Hutang active:
  - Mamak Egit Rp15.000.000
  - Bapak Egit Rp5.000.000
  - Mamak Nurul Rp5.000.000
- Aset is hybrid:
  - Tabungan manual opening/reconciliation balance
  - Savings / Transfer Ledger for automatic transfer/nabung/pocket events
  - Gold Summary + Gold Ledger
- Gold is tracked primarily by grams, with rupiah valuation.
- Review Queue is required for parser ambiguity.
- Sync Log is required for observability.

Example Telegram routing:
1. "Catat ini: beli makan 50k pakai tokopedia credit card"
   - Transactions: expense, Makan, 50000, Tokopedia CC
   - Credit Card: amount 50000, status Pocket BLU = Belum
2. "saya hari ini pegang cash 100rb"
   - Cash Ledger: new cash session, amount_start 100000
3. "hari ini cash kepake beli makan 20rb"
   - Cash Ledger: entry keluar 20000 under active session
4. "hari ini sudah bayar cicilan rumah"
   - Cicilan Rumah: next cicilan payment row
5. "hari ini bayar hutang ke mamak egit 1 juta"
   - Hutang: payment row for HT-001
6. "tf 5 juta dari BCA ke BLU BCA tabungan"
   - Transactions: transfer
   - Savings / Transfer Ledger: internal_transfer/general_savings
   - not expense/income
7. "tf 500 ribu ke pocket Bayaran Kartu Kredit dari BCA"
   - Savings / Transfer Ledger: cc_pocket_allocation
   - later reduces CC unpaid pocket indicator
8. "hari ini beli emas 1 gram harga 1.350.000 pakai BCA"
   - Gold Ledger: buy, grams_in 1, price_per_gram 1350000
   - Transactions: asset purchase/conversion

Safety boundaries:
- Jangan baca token, .env, credential, OAuth secret/client, browser profile, cookies, sessions, private keys.
- Jangan commit local DB, receipt files, runtime state, credentials, OAuth token/client, or secret files.
- Jangan sentuh EarnsAI, runtime, atau trading.
- Jangan enable live trading.
- Jangan hard-delete finance records.
- Jangan real Google write tanpa explicit approval gate.
- Jangan patch/restart OpenClaw service tanpa explicit approval.
- Kalau ada untracked path EarnsAI/runtime/trading, jangan disentuh dan jangan commit.

Official next item:
Design SQLite → Google Sheets sync dry-run.

Do not jump straight into real sync/write. Start with safe discovery and sync mapping.

Next sync design must include:
1. safe SQLite schema discovery command
2. no credential read
3. no Google real write
4. table-to-tab mapping
5. row routing rules
6. confidence routing to Review Queue
7. dedup via transaction_id/local_db_rowid/sync_hash
8. dry-run report
9. explicit approval gate before real write
10. sync log plan

Response format wajib:
1. Ringkas checkpoint dari GitHub docs atau output terminal terakhir.
2. Official next item.
3. Safety boundaries aktif.
4. Context meter: X/100.
5. Kalau command diperlukan: jelaskan dulu command untuk apa, lalu berikan satu command paste-safe dalam satu fenced bash code block. Kalau tidak perlu command, tulis command tidak diperlukan.

Strict command requirement:
- Hanya satu command block.
- Command block wajib berlabel bash.
- Isi command wajib langsung mulai dengan bash -lc.
- Jangan taruh command di luar code block.
- Jangan pecah command jadi beberapa blok.
- Jangan nested code block.
- Kalau tidak bisa memastikan format command benar, jawab:
  FORMAT_RISK: command withheld.

Sheet header read-only validation status:
- Apps Script compact validator validateAiroFinanceHeadersReadOnlyV011 was run.
- Result: PASS.
- 11/11 tabs found.
- 13/13 header checks passed.
- Sync Log header was fixed to final 19-column layout before PASS.
- Google write performed: false.

Official next item:
Design Google Sheets write-gate behavior. Do not implement real write yet.

Batch-forward mode status:
- ACTIVE for this project.
- Prefer substantial batches over tiny micro-steps.
- Combine design, implementation artifact, smoke test, docs update, carryover update, commit, push, and next-action statement when safe.
- Keep non-negotiable safety boundaries active.
- When command is needed: exactly one bash code block, command starts with bash -lc, no nested markdown, no code fence IDs.
- If formatting risk exists: FORMAT_RISK: command withheld.

Google Sheets write-gate status:
- Write-gate v0.2 artifact exists.
- First allowed real write is Sync Log probe only.
- Finance ledger writes still disabled.
- Exact approval phrase required:
  I APPROVE GOOGLE SHEETS WRITE FOR AIRO FINANCE

Official next item:
Run Apps Script write-gate probe v0.2 against 🔄 Sync Log only, then record result.

Google Sheets write-gate probe status:
- PASS.
- Function: airoFinanceWriteGateProbeV02.
- google_write_performed=true.
- write_scope=sync_log_only.
- finance_ledger_write_performed=false.
- run_id=write_probe_20260510_074005_f7513e.
- The controlled write path works for 🔄 Sync Log only.
- Finance ledger writes remain disabled.

Official next item:
Implement Python write_preview mode: read SQLite + read existing Google Sheet keys/headers, compute insert/update/skip/conflict plan, perform no Google write.

Python write_preview mode status:
- v0.3 implemented as repo artifact.
- Script: scripts/personal-workflow/airo_sheets_sync_write_preview.py.
- Apps Script key exporter: scripts/personal-workflow/apps-script/airo_finance_sheet_key_exporter_v0_3.gs.
- write_preview performs no Google write.
- default mode reads SQLite and treats existing sheet keys as empty if no snapshot is provided.
- with sheet snapshot JSON, it compares duplicate_key/sync_hash and returns insert/update/skip plan.

Official next item:
Run Apps Script sheet key exporter, then run Python write_preview with snapshot.

write_preview v0.3 PASS status:
- Ran with Apps Script sheet key snapshot.
- google_write_performed=false.
- credentials_read=false.
- sheet_snapshot_provided=true.
- total_preview_decisions=1.
- preview_action skip_validation_marker=1.
- target_tab NO_WRITE=1.
- Current SQLite has no production finance ledger rows ready for write.

Ledger write skeleton v0.4 status:
- Implemented as scripts/personal-workflow/airo_sheets_ledger_write_v0_4.py.
- Skeleton only; performs no Google write.
- Approval gate structure exists.
- Real Google API write is deferred until real finance rows exist and credential strategy is approved.

Official next item:
Wait for or create real finance rows through the normal Telegram/local parser path, then rerun dry-run/write_preview. Do not implement real ledger write while DB only contains validation marker.

Account alias normalization status:
- User normally uses "blubca" or "blu" for BLU BCA.
- Airo response showed account unresolved for: catat beli makan siang 12000 pakai blubca.
- Canonical account must be BLU BCA.
- Aliases to support: blu, blubca, blu bca, blu-bca, blu_bca, bank blu, bank blu bca.
- Parser support artifact exists at scripts/personal-workflow/airo_account_aliases.py.
- Tests exist at tests/personal-workflow/test_airo_account_aliases.py.

Official next item:
Integrate account alias normalization into the active Telegram finance parser path, then retry the same Telegram capture and rerun sync preview.

Account alias parser integration status:
- v0.2 patch applied.
- Patched files: scripts/personal-workflow/airo_transaction_executor.py
- Alias module remains scripts/personal-workflow/airo_account_aliases.py.
- BLU BCA aliases: blu, blubca, blu bca, blu-bca, blu_bca, bank blu, bank blu bca.
- No Google write, no DB manual mutation, no credential read.

Official next item:
Retry Telegram capture after normal parser/service reload: catat beli makan siang 12000 pakai blubca. Then rerun SQLite dry-run/write_preview.

Sync alias rescue v0.5 status:
- Implemented in scripts/personal-workflow/airo_sheets_sync_dry_run.py.
- Purpose: recover canonical account from payment_method/account/note raw text.
- blubca/blu aliases normalize to BLU BCA at sync mapper layer too.
- No Google write, no DB mutation, no service restart.

Official next item:
Review alias-rescue preview output. If REAL_WRITE_CANDIDATE_COUNT > 0, design first ledger-write implementation. If still 0, inspect Telegram persistence path because captures may not be entering SQLite.

Telegram local handler persistence v0.6 status:
- Runtime bot path is /home/egitaristorandas/earnsai-pulse-trading/scripts/telegram_paper_control_bot.py.
- Repo does not contain that bot file.
- Source-of-truth repo handler patched: airo_personal_workflow/telegram/local_handler.py.
- Added persistence helper: scripts/personal-workflow/airo_transaction_persistence.py.
- Helper persists record_transaction payloads to canonical SQLite and normalizes blubca/blu to BLU BCA.
- Handler updates saved.account_name/payment_method after persistence so response can show BLU BCA.
- Smoke test used temporary SQLite and passed.
- No Google write, no credential read, no production DB mutation during smoke, no service restart.

Official next item:
Deploy/reload normal Telegram/Airo runtime path so it uses source-of-truth local handler, retry capture, then rerun sync preview.

Credit Card billing cycle v0.8 status:
- Artifact ready, sheet patch not yet run.
- Tokopedia Card cycle rule: 16th to 15th.
- Transaction date day >= 16 maps to next statement month.
- Transaction date day <= 15 maps to current statement month.
- New 💳 Credit Card columns planned: billing_cycle_id, billing_start, billing_end, statement_month, due_date, is_statement_locked.
- Apps Script artifact: scripts/personal-workflow/apps-script/airo_credit_card_billing_cycle_v0_8.gs.
- Python utility: scripts/personal-workflow/airo_credit_card_billing_cycle.py.
- v0.7 first ledger write PASS was recorded.

Official next item:
Paste Apps Script v0.8, run smokeTestTokpedCardBillingCycleV08, patchCreditCardBillingCycleHeaderV08, then validateCreditCardBillingCycleHeaderV08.

Credit Card billing cycle v0.8 validation status:
- PASS.
- Checked range: 💳 Credit Card!A3:O3.
- mismatches=[].
- google_write_performed=false for validation.
- Header now supports billing_cycle_id, billing_start, billing_end, statement_month, due_date, is_statement_locked.
- Tokopedia Card rule remains 16th to 15th.

Official next item:
Implement Credit Card mirror planner v0.9 so Tokopedia Card transactions mirror into 💳 Credit Card with correct billing cycle.

Credit Card mirror planner v0.9 status:
- Implemented, no Google write.
- Mirror planner: scripts/personal-workflow/airo_credit_card_mirror_planner.py.
- Integrated into write_preview: scripts/personal-workflow/airo_sheets_sync_write_preview.py.
- Tokopedia Card transactions now generate 💳 Credit Card mirror operations.
- Mirror duplicate_key uses linked transaction ID, matching Credit Card key exporter behavior.
- Billing cycle fields are generated using 16th-to-15th rule.
- Validation marker and NO_WRITE operations are skipped.

Official next item:
Create/ingest a Tokopedia Card transaction through Telegram/Airo, rerun write_preview, and confirm it produces both 💸 Transactions and 💳 Credit Card candidates.

Credit Card mirror planner v0.9.1 status:
- Implemented de-dup fix, no Google write.
- Mirror planner now only mirrors canonical 💸 Transactions ops.
- write_preview now normalizes Credit Card duplicate_key to linked_txn_id.
- Legacy credit_card:<txn_id> duplicates are dropped when billing mirror exists.
- Expected Tokopedia CC candidate: trx_41a84be31c7e.
- Expected billing_cycle_id: TOKPED_CC_2026-05.
- Expected candidate counts: REAL_WRITE_CANDIDATE_COUNT=2, TRANSACTIONS_CANDIDATE_COUNT=1, CREDIT_CARD_CANDIDATE_COUNT=1.

Official next item:
Prepare approval-gated Tokopedia CC write artifact after v0.9.1 preview PASS.

Tokopedia CC write v1.0 status:
- Artifact ready, not yet run.
- Apps Script: scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs.
- Main function: airoFinanceTokopediaCcWriteV10.
- Scope: 💸 Transactions + 💳 Credit Card + 🔄 Sync Log.
- Candidate transaction_id: trx_41a84be31c7e.
- Transactions duplicate_key: transactions:trx_41a84be31c7e.
- Credit Card linked_txn_id: trx_41a84be31c7e.
- Billing cycle: TOKPED_CC_2026-05 / 2026-04-16 to 2026-05-15.
- Requires approval phrase: I APPROVE GOOGLE SHEETS WRITE FOR AIRO FINANCE.

Official next item:
Paste Apps Script v1.0, set approval phrase, run airoFinanceTokopediaCcWriteV10, then run key exporter + write_preview to verify skip_duplicate.

Tokopedia CC write v1.0 PASS status:
- PASS.
- Google Sheet write performed by Apps Script with approval gate.
- Function: airoFinanceTokopediaCcWriteV10.
- transaction_id: trx_41a84be31c7e.
- transactions_inserted=1.
- credit_card_inserted=1.
- billing_cycle_id=TOKPED_CC_2026-05.
- run_id=tokopedia_cc_write_v1_0_20260510_095013_bbb8c3.
- Sheet key exporter confirmed:
  - 💸 Transactions has transactions:trx_41a84be31c7e.
  - 💳 Credit Card has trx_41a84be31c7e.
  - 🔄 Sync Log has sync_2268ec87e00a.
- Approval phrase was cleared after write.
- write_preview v1.0.4 confirmed REAL_WRITE_CANDIDATE_COUNT=0.

Official next item:
Move from one-off writers to generalized approval-gated batch sync/write pipeline.

Full Auto Sheets Sync v1.1 status:
- Core auto-sync artifact implemented.
- No per-write approval phrase.
- Main script: scripts/personal-workflow/airo_full_auto_sheets_sync.py.
- Google client: scripts/personal-workflow/airo_google_sheets_client.py.
- Scope: 💸 Transactions, 💳 Credit Card, 🔄 Sync Log.
- Supports live sheet key export, preview, insert/update, idempotency, and Sync Log audit.
- Systemd timer templates added.
- One-time Google credential setup still required.
- Non-core tabs are not yet full-auto write targets.

Official next item:
Connect Google credentials once, run full-auto dry-run live, then run apply once manually, then install timer.

Full Auto Sheets Sync v1.1.1 status:
- Smoke/report hardening implemented.
- Added --report-out to full-auto sync.
- Hardened dry-run validates final report directly.
- Verified: mode=dry-run, google_write_performed=false, approval_phrase_required=false, write_candidate_count=0.
- Next: connect Google credentials once, run live dry-run, then run apply.

Official next item:
Set up Google service account credential/env, run live dry-run, then run live apply.

Full Auto Sheets Sync v1.1.2 OAuth status:
- OAuth Desktop Client support implemented.
- Service account key creation was blocked by iam.disableServiceAccountKeyCreation.
- Preferred credential mode now uses:
  - AIRO_GOOGLE_OAUTH_CLIENT_SECRET_PATH
  - AIRO_GOOGLE_OAUTH_TOKEN_PATH
- OAuth client secret already stored locally by user.
- Next live dry-run will start one-time browser approval and create oauth-token.json.
- No approval phrase is used.

Official next item:
Run live dry-run once, complete OAuth approval, verify live sheet key export, then run apply.

Full Auto Sheets Sync v1.1.3 status:
- Live OAuth dry-run PASS.
- OAuth token created locally.
- Real Google Sheet read succeeded.
- google_read_performed=true.
- google_write_performed=false.
- approval_phrase_required=false.
- write_candidate_count=0.
- Systemd service patched to use AIRO_SYNC_PYTHON from venv.
- Next: timer install/enable.

Official next item:
Enable full-auto timer, then test with one new Telegram transaction and confirm auto-sync writes it.

Full Auto Sheets Sync v1.1.4 status:
- PASS.
- systemd user timer is active.
- New Telegram transaction tested: catat beli kopi 15000 pakai blubca.
- SQLite transaction_id: trx_f2884e451cd1.
- Post-timer live verification showed transactions:trx_f2884e451cd1 as skip_duplicate.
- WRITE_CANDIDATE_COUNT=0.
- approval_phrase_required=false.
- Full-auto core scope is operational: 💸 Transactions, 💳 Credit Card, 🔄 Sync Log.
- Remaining tabs are not yet full-auto write targets.

Official next item:
Extend full-auto pipeline beyond core transaction flow, starting with asset/savings rules or cash ledger.

## AIRO Full Auto Asset Sync v1.2A Planner

- Added pure planner for `🥇 Aset`.
- Savings/tabungan outputs `savings_transfer_ledger` events.
- Gold/emas outputs `gold_ledger` events.
- Gram is canonical for gold quantity.
- No Google write, SQLite read, credential read, or Apps Script dependency in planner.
- Next: integrate planner into `airo_full_auto_sheets_sync.py` using actual write-candidate shape.

## AIRO Full Auto Asset Sync v1.2B Integration

- Integrated v1.2A asset planner into dry-run planned operations.
- Preview now preserves `section` and supports section snapshot keys.
- Full-auto now supports `🥇 Aset` insert candidates:
  - savings ledger: `O3:Z`
  - gold ledger: `A24:M`
- Asset ledgers are append-only in v1.2B.
- Approval phrase remains disabled.

## AIRO Transaction Amount Parser Bare Number Fix

- Timer was paused before correction.
- Wrong row `trx_a8ad5c2eec99` from `nabung 5000 ke blu` was corrected from `5000000` to `5000` in SQLite.
- Amount parser/persistence now treats bare numbers as exact.
- Explicit suffixes still work: `rb/ribu/k`, `juta/jt`.
- Continue live v1.2C only after parser smoke PASS.

## AIRO Full Auto Asset Sync v1.2D Dedupe Key Fix

- Fixed asset duplicate key mismatch.
- Planner now emits `sav_...` / `gold_...` directly, matching `savings_event_id` / `gold_event_id`.
- Live row `sav_d78b1a231bb6` for `nabung 5000 ke blu` is present in `🥇 Aset` row 7 with amount `5000`.
- Fresh preview should now return `skip_duplicate` for the live savings row.

## AIRO Finance Language Contract v1.0

- Bare `1..999` means thousands; `1000+` is exact rupiah.
- `5000` = `5000`; `5` = `5000`; `5rb` = `5000`; `5 juta` = `5000000`.
- Savings command routes to Transactions + `🥇 Aset`, category `tabungan`.
- Internal transfers are not expenses.
- Cash withdrawal defaults to internal transfer to Cash.
- Topup defaults to internal transfer unless explicit consumption purpose exists.
- Ambiguous parser cases go to Review Queue.
- Hotfix defines missing persistence helpers `extract_payload_value` and `resolve_account`.

## AIRO Gateway Package Finance Contract Fix

- Root cause moved to `airo_personal_workflow/intents/parser.py`.
- OpenClaw/Telegram uses `python3 -m airo_personal_workflow.gateway`, not just `scripts/personal-workflow/airo_transaction_persistence.py`.
- Gateway parser now follows Finance Contract v1.0:
  - `5000` = `5000`
  - `5` = `5000`
  - `5rb` = `5000`
  - savings category = `tabungan`
- Sheets timer remains paused until wrapper + Telegram smoke pass.

## AIRO Sync Skip Soft-Deleted Transactions

- Duplicate smoke rows for `nabung 5000 ke blu` were soft-deleted.
- Sync dry-run initially still planned those deleted rows.
- `plan_transaction()` now skips rows with `deleted_at`.
- Continue only after current DB dry-run has exactly one `nabung 5000 ke blu` asset op.

## AIRO Asset Planner Skip Soft-Deleted Transactions

- Duplicate Telegram smoke rows were soft-deleted.
- Asset planner initially still generated `🥇 Aset` candidates for deleted rows.
- Patched `airo_asset_event_planner.py` to skip rows with `deleted_at`.
- Keep original linked transaction `trx_a8ad5c2eec99`.

## Live Sheet sync hash update pending

- Soft-delete skip patch works locally.
- Current DB has exactly one active `nabung 5000 ke blu` asset candidate.
- Live Sheet row `sav_d78b1a231bb6` shows `update_candidate` because sync hash changed after category/raw_text normalization.
- Inspect all live candidates before apply/re-enabling timer.

## AIRO Asset Section Update Mapping Fix

- Asset snapshot keys are section-specific: `🥇 Aset::savings_transfer_ledger`.
- `find_existing_row()` now resolves section-specific keys.
- Savings ledger updates use range `O{row}:Z{row}`.
- Asset update candidates no longer fallback-append when row lookup fails.

## AIRO Gateway Idempotency and Reply Safety

- `record_transaction()` now skips active semantic duplicates for identical Telegram/OpenClaw commands.
- `local_handler.py` persistence hook is best-effort and cannot turn a successful DB write into an error reply.
- This targets the false-error pattern where Telegram says NameError after DB insert.

## AIRO Gateway Idempotency and Reply Safety Preserve Action

- Legacy hook action is stored separately and does not overwrite primary `persist_action`.
- Repeated command returns `persist_action=skip_duplicate`.
- Temp DB smoke confirms no real DB side effect.
