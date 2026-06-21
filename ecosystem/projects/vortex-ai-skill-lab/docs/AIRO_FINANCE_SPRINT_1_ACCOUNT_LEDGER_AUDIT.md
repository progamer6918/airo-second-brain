# AIRO Finance — Sprint 1 Account Ledger Read-Only Audit

Status: AUDIT STARTED
Sprint: Sprint 1 — Account Ledger Hardening
Generated at: 2026-05-24 12:40:56
Runtime scope: Read-only audit / documentation only
Canonical source: docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md

## 1. Sprint 1 Boundary

Sprint 1 must harden Account Ledger as the wallet/account movement source-of-truth.

This audit does not implement runtime behavior yet.

Allowed in this micro-step:

- inspect current repo references
- map Account Ledger behavior against Kitab
- identify likely runtime files
- identify test gaps
- prepare patch plan

Not allowed in this micro-step:

- runtime Apps Script patch
- schema migration
- Cash Ledger removal
- Finance Events v1 implementation
- Dashboard Final work
- Sprint 2+ domain maturation

## 2. Kitab Scope for Sprint 1

Sprint 1 scope:

- internal transfer two-sided
- cash movement into Account Ledger
- CC payment into Account Ledger
- asset purchase wallet outflow into Account Ledger
- debt payment wallet outflow into Account Ledger
- balance consistency
- linked_txn_id consistency
- source_tab consistency
- optional quality_status additive column

Definition of Done:

- Account Ledger becomes wallet movement source-of-truth.
- Cash Umum and Cash Bensin can be read from Account Ledger.
- Internal transfer always has two sides.
- Balance is not broken.
- New movement no longer depends on Cash Ledger.

## 3. Candidate Repo Files

These tracked files are likely relevant to Sprint 1 audit because their paths contain ledger/finance/sheet/telegram/account/cash/apps/script keywords.

- airo_personal_workflow/adapters/google/sheets_adapter.py
- airo_personal_workflow/telegram/__init__.py
- airo_personal_workflow/telegram/local_handler.py
- docs/AIRO_FINANCE_CANONICAL_ROADMAP_LOCK.md
- docs/AIRO_FINANCE_CARRYOVER_2026-05-14.md
- docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
- docs/AIRO_FINANCE_HANDOFF_2026-05-13.md
- docs/AIRO_FINANCE_NEW_CHAT_BOOTSTRAP.md
- docs/AIRO_FINANCE_NEXT_PROJECT_2026-05-14.md
- docs/AIRO_FINANCE_SPRINT_0A_COVERAGE_MATRIX.md
- docs/AIRO_FINANCE_SPRINT_0A_FINAL_PASS.md
- docs/AIRO_FINANCE_SPRINT_0B_EMAIL_POLICY_DESIGN.md
- docs/AIRO_FINANCE_SPRINT_0B_FINAL_PASS.md
- docs/AIRO_FINANCE_SPRINT_0B_SCOPE_MATRIX.md
- docs/personal-workflow/AIRO_NEW_CHAT_CARRYOVER_GOOGLE_SHEET_FINANCE_V1_1_8.md
- docs/personal-workflow/handoff/AIRO_FINANCE_ACCOUNT_LEDGER_PARITY_DELTA_CARRYOVER.md
- docs/personal-workflow/handoff/AIRO_FINANCE_ACCOUNT_LEDGER_V101_STABLE_HANDOFF.md
- docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md
- docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_HANDOFF.md
- docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_2_CARRYOVER.md
- docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_2_CLOSEOUT.md
- docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_2_FINAL_HANDOFF.md
- docs/personal-workflow/handoff/AIRO_V13_TELEGRAM_TO_SHEETS_CARRYOVER_PROMPT.md
- docs/personal-workflow/integration/AIRO_ACCOUNT_ALIAS_NORMALIZATION_V0_1.md
- docs/personal-workflow/integration/AIRO_ACCOUNT_ALIAS_PARSER_INTEGRATION_V0_2.md
- docs/personal-workflow/integration/AIRO_CASH_LEDGER_ROUTE_PLANNER_V1_2.md
- docs/personal-workflow/integration/AIRO_FINANCE_CONTRACT_V1_1.md
- docs/personal-workflow/integration/AIRO_FINANCE_DASHBOARD_REFERENCE_SPEC.md
- docs/personal-workflow/integration/AIRO_FINANCE_LANGUAGE_CONTRACT_V1_0.md
- docs/personal-workflow/integration/AIRO_FINANCE_V1_3_INTENT_ROUTER_FORCE_PATCH.md
- docs/personal-workflow/integration/AIRO_FINANCE_V1_3_TELEGRAM_FORCE_ROUTER_PATCH.md
- docs/personal-workflow/integration/AIRO_FULL_AUTO_SHEETS_SYNC_V1_1.md
- docs/personal-workflow/integration/AIRO_FULL_AUTO_SHEETS_SYNC_V1_1_1_SMOKE_HARDENING.md
- docs/personal-workflow/integration/AIRO_FULL_AUTO_SHEETS_SYNC_V1_1_2_OAUTH.md
- docs/personal-workflow/integration/AIRO_FULL_AUTO_SHEETS_SYNC_V1_1_3_LIVE_DRY_RUN_PASS.md
- docs/personal-workflow/integration/AIRO_FULL_AUTO_SHEETS_SYNC_V1_1_4_TIMER_PASS.md
- docs/personal-workflow/integration/AIRO_GATEWAY_PACKAGE_FINANCE_CONTRACT_FIX.md
- docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_FIRST_LEDGER_WRITE_V0_7_PASS.md
- docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_HEADER_VALIDATION_V0_1.md
- docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_LEDGER_WRITE_V0_4.md
- docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_SYNC_DRY_RUN_V0_1.md
- docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_PROBE_V0_2_PASS.md
- docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md
- docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_PREVIEW_V0_3.md
- docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_PREVIEW_V0_3_PASS.md
- docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md
- docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md
- docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_MAPPER_PREVIEW.md
- docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md
- docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_UNIFIED_REGRESSION.md
- docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_3_FULL_AUTO_WRITE_PATH.md
- docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_3_PRODUCTION_TELEGRAM_TO_SHEETS.md
- docs/personal-workflow/integration/AIRO_TELEGRAM_GATEWAY_DISCOVERY_NOTES.md
- docs/personal-workflow/integration/AIRO_TELEGRAM_LOCAL_HANDLER_PERSISTENCE_V0_6.md
- docs/personal-workflow/integration/AIRO_TELEGRAM_NOTION_OPENCLAW_COLLISION_GUARDRAIL.md
- docs/personal-workflow/integration/AIRO_TELEGRAM_OPTION_A_AGENTS_PATCH_LOG.md
- docs/personal-workflow/integration/AIRO_TELEGRAM_OPTION_A_GATEWAY_RESTART_LOG.md
- docs/personal-workflow/integration/AIRO_TELEGRAM_OPTION_A_NOTION_COMMAND_GUARD_LOG.md
- docs/personal-workflow/integration/AIRO_TELEGRAM_OPTION_A_PERSISTENT_DB_ROUTE_LOG.md
- docs/personal-workflow/integration/AIRO_TELEGRAM_OPTION_A_SINGLE_FRONT_DOOR_PLAN.md
- docs/personal-workflow/integration/AIRO_TELEGRAM_OPTION_A_WORKSPACE_PRECEDENCE_PATCH_LOG.md
- docs/personal-workflow/integration/AIRO_TELEGRAM_PERSISTENCE_NAMEERROR_HOTFIX_V1_0.md
- docs/personal-workflow/integration/AIRO_V13_TELEGRAM_TO_SHEETS_CURRENT_STATE.md
- docs/personal-workflow/phase-2/AIRO_PHASE_2E_GOOGLE_SHEETS_APPROVAL_GATE.md
- docs/personal-workflow/phase-3/AIRO_PHASE_3C_FIRST_GOOGLE_SHEETS_WRITE.md
- docs/personal-workflow/phase-4/AIRO_PHASE_4D_GOOGLE_SHEETS_SYNC_RELIABILITY.md
- docs/personal-workflow/phase-5/AIRO_PHASE_5B_APPROVED_GOOGLE_SHEETS_QUEUE_EXECUTION.md
- docs/personal-workflow/postmortems/AIRO_INCIDENT_2026_05_10_TELEGRAM_FALSE_ERROR_STALE_CONTEXT.md
- docs/personal-workflow/runbooks/AIRO_TELEGRAM_PRODUCTION_DEPLOYMENT_GUARDRAIL.md
- ops/personal-workflow/systemd/airo-full-auto-sheets-sync.service
- ops/personal-workflow/systemd/airo-full-auto-sheets-sync.timer
- ops/personal-workflow/systemd/sheets-sync.env.example
- scripts/airo_gateway_smoke.py
- scripts/airo_integration_contract_smoke.py
- scripts/airo_personal_workflow_call.sh
- scripts/personal-workflow/airo_account_aliases.py
- scripts/personal-workflow/airo_action_gate.py
- scripts/personal-workflow/airo_approval_queue.py
- scripts/personal-workflow/airo_approval_review.py
- scripts/personal-workflow/airo_apps_script_deploy.sh
- scripts/personal-workflow/airo_asset_event_planner.py
- scripts/personal-workflow/airo_cash_ledger_planner.py
- scripts/personal-workflow/airo_cicilan_rumah_planner.py
- scripts/personal-workflow/airo_credit_card_billing_cycle.py
- scripts/personal-workflow/airo_credit_card_mirror_planner.py
- scripts/personal-workflow/airo_daily.py
- scripts/personal-workflow/airo_dashboard_daily_alignment.py
- scripts/personal-workflow/airo_executor_recommend.py
- scripts/personal-workflow/airo_final_smoke.py
- scripts/personal-workflow/airo_finance_prod_regression.sh
- scripts/personal-workflow/airo_finance_sheet_v12_mapper_preview.py
- scripts/personal-workflow/airo_finance_sheet_v12_regression.py
- scripts/personal-workflow/airo_finance_sheet_v12_status.py
- scripts/personal-workflow/airo_full_auto_sheets_sync.py
- scripts/personal-workflow/airo_google_credential_preflight.py
- scripts/personal-workflow/airo_google_fallback.py
- scripts/personal-workflow/airo_google_sheets_client.py
- scripts/personal-workflow/airo_google_sheets_writer.py
- scripts/personal-workflow/airo_health_check.sh
- scripts/personal-workflow/airo_hutang_planner.py
- scripts/personal-workflow/airo_intent_router.py
- scripts/personal-workflow/airo_local_dashboard.py
- scripts/personal-workflow/airo_ops_dashboard.py
- scripts/personal-workflow/airo_queue_executor.py
- scripts/personal-workflow/airo_receipt_intake.py
- scripts/personal-workflow/airo_receipt_review.py
- scripts/personal-workflow/airo_regression_smoke.sh
- scripts/personal-workflow/airo_review_queue_planner.py
- scripts/personal-workflow/airo_sheets_ledger_write_v0_4.py
- scripts/personal-workflow/airo_sheets_sync.py
- scripts/personal-workflow/airo_sheets_sync_dry_run.py
- scripts/personal-workflow/airo_sheets_sync_write_preview.py
- scripts/personal-workflow/airo_status.sh
- scripts/personal-workflow/airo_status_workflow.py
- scripts/personal-workflow/airo_transaction_executor.py
- scripts/personal-workflow/airo_transaction_persistence.py
- scripts/personal-workflow/airo_transaction_proposal.py
- scripts/personal-workflow/airo_v13_next_chat_bootstrap.sh
- scripts/personal-workflow/airo_workflow_response_polish.py
- scripts/personal-workflow/airoctl.py
- scripts/personal-workflow/apps-script/airo_credit_card_billing_cycle_v0_8.gs
- scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs
- scripts/personal-workflow/apps-script/airo_finance_sheet_key_exporter_v0_3.gs
- scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs
- scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs
- scripts/personal-workflow/runtime-tests/airo_finance_clarification_regression.sh
- scripts/personal_workflow_db_smoke.py
- scripts/personal_workflow_export_smoke.py
- scripts/personal_workflow_google_dry_run.py
- scripts/personal_workflow_smoke.py
- scripts/personal_workflow_telegram_smoke.py
- tests/personal-workflow/test_airo_account_aliases.py
- tests/personal-workflow/test_airo_cash_ledger_planner.py
- tests/personal-workflow/test_airo_finance_contract_v1_1.py
- tests/personal-workflow/test_airo_finance_language_contract.py
- tests/personal-workflow/test_airo_finance_sheet_v12_mapper_preview.py
- tests/personal-workflow/test_airo_finance_sheet_v12_regression.py
- tests/personal-workflow/test_airo_finance_sheet_v12_status.py
- tests/personal-workflow/test_airo_full_auto_sheets_sync_v13_write_path.py
- tests/personal-workflow/test_airo_gateway_finance_contract.py
- tests/personal-workflow/test_airo_intent_router_v13_finance_force.py
- tests/personal-workflow/test_airo_sheets_sync_skip_deleted.py

## 4. Reference Scan Findings

### Pattern: Account Ledger

Total matches: 167

- `docs/personal-workflow/integration/AIRO_FINANCE_DASHBOARD_REFERENCE_SPEC.md:161:- Net Worth Total: Aset, Hutang, Cicilan Rumah, Account Ledger/account balances`
- `docs/personal-workflow/integration/AIRO_FINANCE_DASHBOARD_REFERENCE_SPEC.md:162:- Liquid assets: Account Ledger and account balance formulas`
- `docs/personal-workflow/integration/AIRO_FINANCE_DASHBOARD_REFERENCE_SPEC.md:168:- Account balances: Account Ledger and Cash Ledger compatibility where needed`
- `docs/personal-workflow/integration/AIRO_FINANCE_DASHBOARD_REFERENCE_SPEC.md:169:- Cashflow month: Account Ledger and Monthly Review`
- `docs/personal-workflow/integration/AIRO_FINANCE_DASHBOARD_REFERENCE_SPEC.md:179:- Cash/Account Ledger: increasingly stable.`
- `docs/personal-workflow/integration/AIRO_CREDIT_CARD_CYCLE_FOCUS_LOCK_2026_05_20.md:70:- Account Ledger transfer matrix`
- `docs/personal-workflow/integration/AIRO_V12_DASHBOARD_FINAL_IMPLEMENTATION_PLAN.md:26:\| Net Worth / Assets \| Aset + Account Ledger \| Snapshot of liquid assets, savings, gold \| Ready after asset regression PASS \|`
- `docs/personal-workflow/integration/AIRO_V12_DASHBOARD_FINAL_IMPLEMENTATION_PLAN.md:27:\| Cashflow Month \| Monthly Review + Account Ledger \| Monthly income/expense summary \| Ready after reporting formula guard PASS \|`
- `docs/personal-workflow/integration/AIRO_V12_DASHBOARD_FINAL_IMPLEMENTATION_PLAN.md:29:\| Cash Position \| Cash Ledger + Account Ledger \| Cash sessions and cash spend visibility \| Ready after Cash Ledger preview regression PASS \|`
- `docs/personal-workflow/integration/AIRO_CLARIFICATION_BEFORE_REVIEW_QUEUE_BATCH_D_PASS.md:125:- Written to Account Ledger`
- `docs/personal-workflow/integration/AIRO_TRANSFER_INCOMPLETE_CLARIFICATION_PASS.md:35:Transfer was written as internal transfer pair in Account Ledger:`
- `docs/personal-workflow/integration/AIRO_TRANSFER_INCOMPLETE_CLARIFICATION_PASS.md:50:- Lets the existing internal transfer writer create the Account Ledger out/in pair.`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:112:- Keep Account Ledger as mutation center.`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:151:- Account Ledger :out/:in transfer pairs`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:168:- Account Ledger is the mutation center.`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:172:- Credit Card, Hutang, and Aset must not be forcibly merged into Account Ledger.`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:173:- Dashboard and Monthly Review should read Account Ledger where appropriate.`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:187:- admin audit account rows can display internal transfer Account Ledger rows.`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:196:- Result: Cash Ledger inflow, Account Ledger Cash Umum inflow, cash parity PASS.`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:200:- Result: Cash Ledger outflow, Account Ledger Cash Bensin outflow, cash parity PASS.`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:204:- Result: Account Ledger BCA amount_out Rp1.000, Blu amount_in Rp1.000, pair linked via :out/:in, cash parity PASS.`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:208:- Result: Account Ledger Blu amount_out Rp1.000, Cash Umum amount_in Rp1.000, Cash Ledger amount_in Rp1.000 type transfer_in, cash parity PASS.`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:212:- Result: Account Ledger Cash Umum amount_out Rp1.000, Blu amount_in Rp1.000, Cash Ledger amount_out Rp1.000 type transfer_out, cash parity PASS.`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:218:- Account Ledger Cash in: Rp130000`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:219:- Account Ledger Cash out: Rp81000`

### Pattern: Cash Ledger

Total matches: 295

- `docs/personal-workflow/integration/AIRO_FINANCE_DASHBOARD_REFERENCE_SPEC.md:168:- Account balances: Account Ledger and Cash Ledger compatibility where needed`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_MAPPER_PREVIEW.md:14:- 💵 Cash Ledger`
- `docs/personal-workflow/integration/AIRO_CREDIT_CARD_CYCLE_FOCUS_LOCK_2026_05_20.md:69:- Cash Ledger`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_PROBE_V0_2_PASS.md:33:- 💵 Cash Ledger: not written`
- `docs/personal-workflow/integration/AIRO_V12_REPORTING_FORMULA_GUARD_PASS.md:21:- PASS: 💵 Cash Ledger is FULL_AUTO_WRITE_PATH_READY`
- `docs/personal-workflow/integration/AIRO_V12_REPORTING_FORMULA_GUARD_PASS.md:32:- PASS: cash entry targets Cash Ledger`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:26:This verifies the Google Sheets write path while keeping Transactions, Credit Card, Review Queue, Aset, Hutang, Cash Ledger, and Cicilan Rumah untouched.`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:57:- 💵 Cash Ledger`
- `docs/personal-workflow/integration/AIRO_V12_DASHBOARD_FINAL_IMPLEMENTATION_PLAN.md:29:\| Cash Position \| Cash Ledger + Account Ledger \| Cash sessions and cash spend visibility \| Ready after Cash Ledger preview regression PASS \|`
- `docs/personal-workflow/integration/AIRO_V12_DASHBOARD_READINESS_MATRIX.md:21:- PASS: 💵 Cash Ledger is FULL_AUTO_WRITE_PATH_READY`
- `docs/personal-workflow/integration/AIRO_V12_DASHBOARD_READINESS_MATRIX.md:32:- PASS: cash entry targets Cash Ledger`
- `docs/personal-workflow/integration/AIRO_V12_DASHBOARD_READINESS_GATE_PASS.md:29:- PASS: 💵 Cash Ledger is FULL_AUTO_WRITE_PATH_READY`
- `docs/personal-workflow/integration/AIRO_V12_DASHBOARD_READINESS_GATE_PASS.md:40:- PASS: cash entry targets Cash Ledger`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:18:3. 💵 Cash Ledger`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:34:\| 💵 Cash Ledger \| DESIGNED / HEADER_VALID / NOT_GENERALIZED \| Needs route and sync completion \|`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:221:### 💵 Cash Ledger`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:223:Pattern: `Cash Ledger\|cash session\|cash_sessions\|cash entries\|cash_entries\|amount_remaining``
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:226:docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_PROBE_V0_2_PASS.md:33:- 💵 Cash Ledger: not written`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:227:docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:26:This verifies the Google Sheets write path while keeping Transactions, Credit Card, Review Queue, Aset, Hutang, Cash Ledger, and Cicilan Rumah untouched.`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:228:docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:57:- 💵 Cash Ledger`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:229:docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:18:3. 💵 Cash Ledger`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:230:docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:34:\| 💵 Cash Ledger \| DESIGNED / HEADER_VALID / NOT_GENERALIZED \| Needs route and sync completion \|`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:231:docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:221:### 💵 Cash Ledger`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:232:docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:223:Pattern: `Cash Ledger\|cash session\|cash_sessions\|cash entries\|cash_entries\|amount_remaining``
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:233:docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_FIRST_LEDGER_WRITE_V0_7_PASS.md:38:- 💵 Cash Ledger`

### Pattern: internal transfer

Total matches: 27

- `docs/personal-workflow/integration/AIRO_FINANCE_LANGUAGE_CONTRACT_V1_0.md:58:- default: internal transfer BLU BCA -> Cash`
- `docs/personal-workflow/integration/AIRO_FINANCE_LANGUAGE_CONTRACT_V1_0.md:62:- default internal transfer unless explicit consumption purpose exists.`
- `docs/personal-workflow/integration/AIRO_TRANSFER_INCOMPLETE_CLARIFICATION_PASS.md:35:Transfer was written as internal transfer pair in Account Ledger:`
- `docs/personal-workflow/integration/AIRO_TRANSFER_INCOMPLETE_CLARIFICATION_PASS.md:50:- Lets the existing internal transfer writer create the Account Ledger out/in pair.`
- `docs/personal-workflow/AIRO_NEW_CHAT_CARRYOVER_GOOGLE_SHEET_FINANCE_V1_1_8.md:454:- Cash withdrawal defaults to internal transfer to Cash.`
- `docs/personal-workflow/AIRO_NEW_CHAT_CARRYOVER_GOOGLE_SHEET_FINANCE_V1_1_8.md:455:- Topup defaults to internal transfer unless explicit consumption purpose exists.`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:113:- Ensure cash and internal transfers do not create parity deltas or wrong amount direction.`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:142:Finish remaining internal transfer matrix and final audit.`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:187:- admin audit account rows can display internal transfer Account Ledger rows.`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:203:- Test: transfer 1000 dari bca ke blu test phase d internal transfer bca blu`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:207:- Test: transfer 1000 dari blu ke cash test phase d internal transfer blu cash`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:211:- Test: transfer 1000 dari cash ke blu test phase d internal transfer cash blu`
- `docs/personal-workflow/handoff/AIRO_FINANCE_ACCOUNT_LEDGER_PARITY_DELTA_CARRYOVER.md:102:The likely root cause is an ID mismatch between internal transfer rows and Cash Ledger compatibility/backfill rows.`
- `docs/personal-workflow/handoff/AIRO_FINANCE_ACCOUNT_LEDGER_PARITY_DELTA_CARRYOVER.md:113:- Account Ledger internal transfer inflow uses `entry_id = sharedTxnId + ":in"`.`
- `docs/personal-workflow/handoff/AIRO_FINANCE_ACCOUNT_LEDGER_PARITY_DELTA_CARRYOVER.md:153:2. Patch dedupe so Cash Ledger compatibility rows from internal transfers do not create duplicate Account Ledger rows when matching `sharedTxnId + ":in"` or `sharedTxnId + ":out"` already exists.`
- `docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_HANDOFF.md:85:- Savings / Transfer Ledger for automated savings/internal transfer events`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:358:internal transfer`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:778:internal transfer has two sides`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:793:internal transfer one-sided`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:1054:internal transfer`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:1388:internal transfer two-sided`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:348:internal transfer`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:768:internal transfer has two sides`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:783:internal transfer one-sided`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:1044:internal transfer`

### Pattern: linked_txn_id

Total matches: 36

- `docs/personal-workflow/integration/AIRO_CREDIT_CARD_BILLING_CYCLE_V0_8_VALIDATE_PASS.md:29:- H3: linked_txn_id`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:153:scripts/personal-workflow/airo_credit_card_mirror_planner.py:106:    for key in ("transaction_id", "linked_txn_id", "entity_id"):`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:161:scripts/personal-workflow/airo_credit_card_mirror_planner.py:160:        "linked_txn_id": transaction_id,`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:269:Pattern: `Credit Card\|credit_card\|Tokopedia\|billing_cycle\|linked_txn_id\|status_pocket_blu``
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:280:scripts/personal-workflow/airo_credit_card_mirror_planner.py:106:    for key in ("transaction_id", "linked_txn_id", "entity_id"):`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:287:scripts/personal-workflow/airo_credit_card_mirror_planner.py:160:        "linked_txn_id": transaction_id,`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:296:scripts/personal-workflow/apps-script/airo_finance_sheet_key_exporter_v0_3.gs:28:      '💳 Credit Card': exportByHeaderV03_(ss, '💳 Credit Card', 3, 'linked_txn_id', null),`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:300:scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:11: * - 💳 Credit Card: linked_txn_id = trx_41a84be31c7e`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:305:scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:45:  const ccHeaders = ["cc_entry_id", "date", "merchant_app", "amount", "description", "status_pocket_blu", "transferred_at", "linked_txn_id", "notes", "billing_cycle_id", "billing_start", "billing_end", "statement_month", "due_date", "is_statement_locked"];`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:306:scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:53:  const ccLinkedTxnId = getValueByHeaderV10_(ccHeaders, ccValues, 'linked_txn_id');`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:307:scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:56:  const existingCc = findRowByHeaderValueV10_(ccSheet, 3, 'linked_txn_id', ccLinkedTxnId);`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:313:scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:112:    linked_txn_id: ccLinkedTxnId,`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:316:scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:145:  const expected = ["cc_entry_id", "date", "merchant_app", "amount", "description", "status_pocket_blu", "transferred_at", "linked_txn_id", "notes", "billing_cycle_id", "billing_start", "billing_end", "statement_month", "due_date", "is_statement_locked"];`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:324:scripts/personal-workflow/apps-script/airo_credit_card_billing_cycle_v0_8.gs:28:    'linked_txn_id',`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:331:scripts/personal-workflow/apps-script/airo_credit_card_billing_cycle_v0_8.gs:97:    'linked_txn_id',`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:337:scripts/personal-workflow/airo_full_auto_sheets_sync.py:44:    "status_pocket_blu", "transferred_at", "linked_txn_id", "notes",`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:340:scripts/personal-workflow/airo_full_auto_sheets_sync.py:179:        or row.get("linked_txn_id")`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:350:scripts/personal-workflow/airo_sheets_sync_dry_run.py:389:                "linked_txn_id": txid,`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:351:scripts/personal-workflow/airo_sheets_sync_dry_run.py:513:                        linked_txn_id = str(row_preview.get("linked_transaction_id") or "")`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:589:scripts/personal-workflow/airo_sheets_sync_dry_run.py:520:                            entity_id=linked_txn_id or str(asset_plan.get("duplicate_key") or ""),`
- `docs/personal-workflow/integration/AIRO_TOKOPEDIA_CC_WRITE_V1_0.md:24:- linked_txn_id: trx_41a84be31c7e`
- `docs/personal-workflow/integration/AIRO_TOKOPEDIA_CC_WRITE_V1_0.md:66:- 💳 Credit Card checks linked_txn_id.`
- `docs/personal-workflow/integration/AIRO_FULL_AUTO_SHEETS_SYNC_V1_1.md:89:- linked_txn_id for 💳 Credit Card`
- `docs/personal-workflow/integration/AIRO_CREDIT_CARD_MIRROR_PLANNER_V0_9.md:60:- linked_txn_id`
- `docs/personal-workflow/integration/AIRO_CREDIT_CARD_MIRROR_PLANNER_V0_9.md:75:This matches the sheet key exporter behavior for 💳 Credit Card, which reads `linked_txn_id`.`

### Pattern: source_tab

Total matches: 17

- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:93:- source_table: write_gate_probe`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:163:scripts/personal-workflow/airo_credit_card_mirror_planner.py:174:        "source_table": op.get("source_table") or "transactions",`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:180:scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:80:    source_table: 'transactions',`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:206:scripts/personal-workflow/airo_full_auto_sheets_sync.py:191:        decision.get("source_table", "transactions"),`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:367:scripts/personal-workflow/airo_sheets_sync_dry_run.py:456:        source_table="installment_payments",`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:683:scripts/personal-workflow/airo_sheets_sync_dry_run.py:415:        source_table="approval_queue",`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:845:scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:154:    'sync_id', 'run_id', 'source_db', 'source_table', 'source_rowid',`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:853:scripts/personal-workflow/airo_full_auto_sheets_sync.py:50:    "sync_id", "run_id", "source_db", "source_table", "source_rowid",`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_HEADER_VALIDATION_V0_1.md:70:- source_table`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:541:- source_table`
- `docs/personal-workflow/handoff/AIRO_FINANCE_ACCOUNT_LEDGER_PARITY_DELTA_CARRYOVER.md:120:- `source_tab = 💵 Cash Ledger``
- `docs/personal-workflow/handoff/AIRO_FINANCE_ACCOUNT_LEDGER_V101_STABLE_HANDOFF.md:59:  - `source_tab`: `?? Cash Ledger``
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:375:source_tab`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:1395:source_tab consistency`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:365:source_tab`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:1385:source_tab consistency`
- `tests/personal-workflow/test_airo_credit_card_mirror_planner.py:17:            "source_table": "transactions",`

### Pattern: quality_status

Total matches: 13

- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:168: if unresolved: quality_status = needs_category`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:386:quality_status`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:564:quality_status`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:1191:Pending category  Finance Events quality_status = needs_category`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:1396:optional quality_status additive column`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:1468:quality_status`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:158: if unresolved: quality_status = needs_category`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:376:quality_status`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:554:quality_status`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:1181:Pending category  Finance Events quality_status = needs_category`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:1386:optional quality_status additive column`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:1458:quality_status`
- `docs/AIRO_FINANCE_SPRINT_0B_EMAIL_POLICY_DESIGN.md:256:- set quality_status according to missing fields`

### Pattern: amount_in

Total matches: 14

- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:219:- amount_in`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:150:- Cash Ledger amount_in/amount_out sync`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:204:- Result: Account Ledger BCA amount_out Rp1.000, Blu amount_in Rp1.000, pair linked via :out/:in, cash parity PASS.`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:208:- Result: Account Ledger Blu amount_out Rp1.000, Cash Umum amount_in Rp1.000, Cash Ledger amount_in Rp1.000 type transfer_in, cash parity PASS.`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:212:- Result: Account Ledger Cash Umum amount_out Rp1.000, Blu amount_in Rp1.000, Cash Ledger amount_out Rp1.000 type transfer_out, cash parity PASS.`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:411:- Cash Ledger amount_in/amount_out direction valid`
- `docs/personal-workflow/handoff/AIRO_FINANCE_ACCOUNT_LEDGER_V101_STABLE_HANDOFF.md:55:  - `amount_in`: blank`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:368:amount_in`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:358:amount_in`
- `docs/AIRO_FINANCE_CARRYOVER_2026-05-14.md:127:entry_id, session_id, date, type, category, description, amount_out, amount_in, balance`
- `docs/AIRO_FINANCE_CARRYOVER_2026-05-14.md:131:amount_in = cash masuk`
- `docs/AIRO_FINANCE_CARRYOVER_2026-05-14.md:135:User ingin amount_out, amount_in, balance lebih dekat kiri setelah header Cash Ledger diaudit.`
- `docs/AIRO_FINANCE_CARRYOVER_2026-05-14.md:154:5. Audit Cash Ledger balance dan layout amount_in/out/balance.`
- `docs/AIRO_FINANCE_HANDOFF_2026-05-13.md:323:- amount_in is filled`

### Pattern: amount_out

Total matches: 14

- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:218:- amount_out`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:241:- amount_out 20000`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:150:- Cash Ledger amount_in/amount_out sync`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:204:- Result: Account Ledger BCA amount_out Rp1.000, Blu amount_in Rp1.000, pair linked via :out/:in, cash parity PASS.`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:208:- Result: Account Ledger Blu amount_out Rp1.000, Cash Umum amount_in Rp1.000, Cash Ledger amount_in Rp1.000 type transfer_in, cash parity PASS.`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:212:- Result: Account Ledger Cash Umum amount_out Rp1.000, Blu amount_in Rp1.000, Cash Ledger amount_out Rp1.000 type transfer_out, cash parity PASS.`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:411:- Cash Ledger amount_in/amount_out direction valid`
- `docs/personal-workflow/handoff/AIRO_FINANCE_ACCOUNT_LEDGER_V101_STABLE_HANDOFF.md:56:  - `amount_out`: `Rp 1.000``
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:369:amount_out`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:359:amount_out`
- `docs/AIRO_FINANCE_CARRYOVER_2026-05-14.md:127:entry_id, session_id, date, type, category, description, amount_out, amount_in, balance`
- `docs/AIRO_FINANCE_CARRYOVER_2026-05-14.md:132:amount_out = cash keluar`
- `docs/AIRO_FINANCE_CARRYOVER_2026-05-14.md:135:User ingin amount_out, amount_in, balance lebih dekat kiri setelah header Cash Ledger diaudit.`
- `docs/AIRO_FINANCE_HANDOFF_2026-05-13.md:324:- amount_out is left blank`

### Pattern: Cash Umum

Total matches: 14

- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:145:- Cash Umum inflow`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:194:Cash Umum inflow:`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:196:- Result: Cash Ledger inflow, Account Ledger Cash Umum inflow, cash parity PASS.`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:208:- Result: Account Ledger Blu amount_out Rp1.000, Cash Umum amount_in Rp1.000, Cash Ledger amount_in Rp1.000 type transfer_in, cash parity PASS.`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:212:- Result: Account Ledger Cash Umum amount_out Rp1.000, Blu amount_in Rp1.000, Cash Ledger amount_out Rp1.000 type transfer_out, cash parity PASS.`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:404:- Cash Umum inflow`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:355:saldo Cash Umum`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:403:Cash Umum keluar`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:1063:Cash Umum and Cash Bensin must be read from Account Ledger.`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:1403:Cash Umum and Cash Bensin can be read from Account Ledger.`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:345:saldo Cash Umum`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:393:Cash Umum keluar`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:1053:Cash Umum and Cash Bensin must be read from Account Ledger.`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:1393:Cash Umum and Cash Bensin can be read from Account Ledger.`

### Pattern: Cash Bensin

Total matches: 12

- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:146:- Cash Bensin outflow`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:198:Cash Bensin outflow:`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:200:- Result: Cash Ledger outflow, Account Ledger Cash Bensin outflow, cash parity PASS.`
- `docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md:405:- Cash Bensin outflow`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:356:saldo Cash Bensin`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:404:Cash Bensin keluar`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:1063:Cash Umum and Cash Bensin must be read from Account Ledger.`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:1403:Cash Umum and Cash Bensin can be read from Account Ledger.`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:346:saldo Cash Bensin`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:394:Cash Bensin keluar`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:1053:Cash Umum and Cash Bensin must be read from Account Ledger.`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:1393:Cash Umum and Cash Bensin can be read from Account Ledger.`

### Pattern: cc_payment

Total matches: 6

- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:421:- purpose = cc_payment_pocket`
- `docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_HANDOFF.md:185:- purpose = cc_payment_pocket`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:431:cc_payment`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:446:cc_payment from Blu/BCA  Account Ledger outflow + Credit Card match`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:421:cc_payment`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:436:cc_payment from Blu/BCA  Account Ledger outflow + Credit Card match`

### Pattern: asset_purchase

Total matches: 4

- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:572:scripts/personal-workflow/airo_transaction_persistence.py:260:            "cashflow_treatment": "asset_purchase",`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:580:scripts/personal-workflow/airo_sheets_sync_dry_run.py:182:        return "asset_purchase", "asset_purchase"`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:483:asset_purchase`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:473:asset_purchase`

### Pattern: debt_payment

Total matches: 4

- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:495:docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:348:- Optional Transactions row with type transfer/debt_payment depending sync mapping`
- `docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:348:- Optional Transactions row with type transfer/debt_payment depending sync mapping`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:460:debt_payment`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:450:debt_payment`

### Pattern: wallet movement

Total matches: 18

- `docs/AIRO_FINANCE_NEW_CHAT_BOOTSTRAP.md:50:- Account Ledger hanya wallet movement.`
- `docs/AIRO_FINANCE_NEW_CHAT_BOOTSTRAP.md.bak.20260524_064212:50:- Account Ledger hanya wallet movement.`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:59:7. Account Ledger records wallet movement only.`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:418:domain state without wallet movement`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:624:2. Write Account Ledger if wallet movement exists`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:776:Account Ledger refs exist when event needs wallet movement`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:796:debt payment without wallet movement`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:1402:Account Ledger becomes wallet movement source-of-truth.`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:1616:3. Account Ledger is wallet movement only.`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:1703:- Account Ledger hanya wallet movement.`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:49:7. Account Ledger records wallet movement only.`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:408:domain state without wallet movement`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:614:2. Write Account Ledger if wallet movement exists`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:766:Account Ledger refs exist when event needs wallet movement`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:786:debt payment without wallet movement`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:1392:Account Ledger becomes wallet movement source-of-truth.`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:1606:3. Account Ledger is wallet movement only.`
- `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md.bak.20260524_064212:1693:- Account Ledger hanya wallet movement.`

## 5. Initial Sprint 1 Gap Matrix

| Sprint 1 Area | Current Evidence Needed | Audit Status | Runtime Patch Now? |
|---|---|---:|---:|
| Internal transfer two-sided | Find transfer writer and linked_txn_id usage | Pending deeper audit | No |
| Cash movement into Account Ledger | Find current cash routing and Cash Ledger dependency | Pending deeper audit | No |
| CC payment into Account Ledger | Find CC payment route/writer | Pending deeper audit | No |
| Asset purchase wallet outflow | Find asset purchase route/writer | Pending deeper audit | No |
| Debt payment wallet outflow | Find debt payment route/writer | Pending deeper audit | No |
| Balance consistency | Find balance calculation/writer logic | Pending deeper audit | No |
| linked_txn_id consistency | Find linked transaction ID generation | Pending deeper audit | No |
| source_tab consistency | Find source_tab writes | Pending deeper audit | No |
| quality_status additive column | Check schema compatibility | Pending deeper audit | No |

## 6. Proposed Next Micro-Step

Run a focused source audit to locate exact runtime writer functions and tests for:

- Account Ledger row append/update
- transfer route
- cash route
- CC payment route
- asset purchase route
- debt payment route
- balance calculation
- linked_txn_id/source_tab handling

After that audit, patch only the smallest Sprint 1 gap with tests.
