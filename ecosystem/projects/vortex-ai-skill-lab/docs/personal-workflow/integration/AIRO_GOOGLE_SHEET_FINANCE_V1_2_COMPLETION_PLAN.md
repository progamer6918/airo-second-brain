# AIRO Google Sheet Finance v1.2 Completion Plan

Status: PLANNED / DOCS LOCKED
Date: 2026-05-11
Project: Airo Personal Workflow / Telegram Finance to Google Sheet Finance
Sheet design baseline: Google Sheet Finance Balanced+ v1.1.8-final
Spreadsheet name: 💰 Airo Personal Finance

## Purpose

This document locks the v1.2 completion plan for the finance Google Sheet workflow.

The goal is not to redesign the sheet. The v1.1.8 design is already stable. The goal of v1.2 is to finish the remaining routing, sync, review, and status coverage in the most efficient way possible.

Target execution style:

- maximum practical speed
- small safe batches
- no core rewrite unless regression requires it
- no new phase number
- no invented tabs
- GitHub remains the source of truth

## Product Name

Working track name:

AIRO Finance Sheet Workflow

Parent project:

Airo Personal Workflow

Formal scope:

Telegram Finance to Google Sheet Finance

## User Vision Lock

The user wants AIRO Finance Sheet Workflow to support:

- Telegram as the daily input surface
- local command as debug and regression surface
- all important existing Google Sheet tabs covered by clear routing and status
- automatic writing where the route is verified and low-risk
- Review Queue or clarification question when parser confidence is low
- local SQLite as source of truth
- Google Sheet as human-facing reporting and sync layer
- actionable status/dashboard output
- eventual cashflow, budgeting, and investment direction, but only after the existing tab workflow is stabilized

## Non-negotiable interpretation of auto-write

The user prefers auto-write behavior.

Operationally safe rule:

- auto-write is allowed only for verified, low-risk, idempotent routes
- ambiguous parser output must go to 🧾 Review Queue or ask a clarification question
- unsupported tabs must not receive real writes
- no hard delete
- no Google write without the approved existing write path
- no repeated Telegram smoke testing without production guardrail

This keeps the user goal of speed while preserving finance data safety.

## Existing Sheet Tabs

The final v1.1.8 sheet has exactly 11 tabs:

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

## Verified Sheet Structure

Header validation status from v1.1.8:

- validator: validateAiroFinanceHeadersReadOnlyV011
- mode: read_only
- Google write performed: false
- status: PASS
- tabs expected: 11
- tabs found: 11
- missing tabs: none
- extra tabs: none
- header checks: 13
- failed header checks: 0

Validated sync-critical ranges:

- 💸 Transactions: A1:AD1
- 💵 Cash Ledger cash sessions: A1:H1
- 💵 Cash Ledger cash entries: J1:T1
- 💳 Credit Card ledger: A3:I3, later extended through O for billing cycle fields
- 🏠 Cicilan Rumah payment history: A11:F11
- 🤝 Hutang master: A2:H2
- 🤝 Hutang payment history: A9:H9
- 🥇 Aset savings summary: A3:I3
- 🥇 Aset gold ledger: A23:M23
- 🥇 Aset savings transfer ledger: O3:Z3
- 📅 Monthly Review category breakdown: A12:E12
- 🧾 Review Queue: A1:T1
- 🔄 Sync Log: A2:S2

## Current Completion Matrix

| Tab | Role | Current status | v1.2 action |
|---|---|---|---|
| 🏠 Dashboard | Formula-driven command center | DESIGN_DONE / HEADER_VALID | Keep read-only; improve status UX only if needed |
| 💸 Transactions | Main non-cash ledger | FULL_AUTO_CORE_READY | Keep stable; extend matrix coverage |
| 💵 Cash Ledger | Cash session and cash entry ledger | DESIGNED / HEADER_VALID / NOT_GENERALIZED | Add route and sync completion plan |
| 💳 Credit Card | Tokopedia CC ledger and billing cycle | FULL_AUTO_CORE_READY / TOKOPEDIA_CC_PASS | Keep stable; extend tests |
| 🏠 Cicilan Rumah | House installment payment history | DESIGNED / HEADER_VALID / NOT_GENERALIZED | Add route and sync completion plan |
| 🤝 Hutang | Debt master and repayment history | DESIGNED / HEADER_VALID / NOT_GENERALIZED | Add route and sync completion plan |
| 🥇 Aset | Savings transfer ledger, gold ledger, net worth | ASSET_SYNC_PATCHED | Verify latest regression and complete matrix |
| 📅 Monthly Review | Reporting and monthly category review | DESIGNED / HEADER_VALID / REPORTING | Define refresh/report behavior |
| 🧾 Review Queue | Parser ambiguity guardrail | DESIGNED / HEADER_VALID / NOT_GENERALIZED | Add ambiguity route and sync behavior |
| ⚙️ Settings | Config and approval gate surface | CONFIG_ONLY | Do not use as finance ledger target |
| 🔄 Sync Log | Observability and sync audit | FULL_AUTO_CORE_READY | Keep stable; log new route outcomes |

## Current Full-Auto Scope

Confirmed core full-auto scope from v1.1:

- 💸 Transactions
- 💳 Credit Card
- 🔄 Sync Log

Confirmed later extension:

- 🥇 Aset through v1.2B asset sync integration

Not yet fully generalized:

- 💵 Cash Ledger
- 🏠 Cicilan Rumah
- 🤝 Hutang
- 🧾 Review Queue
- 📅 Monthly Review

## Existing Routing Examples From v1.1.8

| Telegram input | Expected target |
|---|---|
| Catat ini: beli makan 50k pakai tokopedia credit card | 💸 Transactions and 💳 Credit Card |
| saya hari ini pegang cash 100rb | 💵 Cash Ledger session |
| hari ini cash kepake beli makan 20rb | 💵 Cash Ledger entry |
| hari ini sudah bayar cicilan rumah | 🏠 Cicilan Rumah |
| hari ini bayar hutang ke mamak egit 1 juta | 🤝 Hutang |
| tf 5 juta dari BCA ke BLU BCA tabungan | 💸 Transactions and 🥇 Aset savings transfer ledger |
| tf 500 ribu ke pocket Bayaran Kartu Kredit dari BCA | 🥇 Aset savings transfer ledger |
| hari ini beli emas 1 gram harga 1.350.000 pakai BCA | 🥇 Aset gold ledger and 💸 Transactions |

## v1.2 Definition of Done

v1.2 is done when these are true:

1. The 11-tab completion matrix is committed.
2. Each tab has a declared status: FULL_AUTO_CORE_READY, PATCHED, DESIGNED_ONLY, REPORTING_ONLY, CONFIG_ONLY, or NOT_GENERALIZED.
3. Each finance intent has a route matrix entry.
4. Low-risk verified routes have auto-write behavior documented.
5. Ambiguous routes go to 🧾 Review Queue or ask a clarification question.
6. SQLite remains source of truth.
7. Google Sheet remains reporting/sync layer.
8. No extra tabs are invented.
9. Existing stable routes are not broken.
10. Final carryover explains what is done and what remains.

## Two-Hour Execution Filter

In a maximum two-hour execution window, do not attempt full implementation for every tab.

Recommended two-hour target:

1. Create this completion plan.
2. Create or update carryover.
3. Audit current scripts against the 11 tabs.
4. Identify exact missing implementation files or functions for:
   - 💵 Cash Ledger
   - 🏠 Cicilan Rumah
   - 🤝 Hutang
   - 🧾 Review Queue
   - 📅 Monthly Review
5. Implement only one small missing route if it is clearly safe.
6. Otherwise stop at route matrix and carryover.
7. Run read-only or dry-run regression.
8. Commit and push.

## v1.2 Priority Order

Priority 1:

- preserve current PASS state
- do not break Transactions, Credit Card, Sync Log, Aset

Priority 2:

- Cash Ledger route and dry-run mapping
- Review Queue ambiguity route

Priority 3:

- Cicilan Rumah route and dry-run mapping
- Hutang route and dry-run mapping

Priority 4:

- Monthly Review reporting refresh
- Dashboard/status UX summary

Future-only unless explicitly approved:

- budgeting expansion
- investment expansion
- new tabs
- broad parser refactor
- OpenClaw core patch
- service restart

## Safety Boundaries

Always active:

- do not read secrets, tokens, cookies, sessions, passwords, .env files, browser profiles, OAuth secrets, OAuth clients, or private keys
- do not commit local DB, receipt files, runtime state, credentials, OAuth token/client, or secret files
- do not touch EarnsAI, runtime, or trading
- do not enable live trading
- do not hard-delete finance records
- do not restart OpenClaw without explicit approval
- do not patch OpenClaw core without explicit approval
- do not real-write Google Sheets outside approved existing write path
- do not send repeated Telegram smoke tests

## Telegram Production Guardrail

Local airo-workflow PASS is not production Telegram PASS.

Before any Telegram production smoke that can affect finance state:

1. Pause write-capable automation if DB or sync logic was touched.
2. Run local wrapper with temp DB.
3. Confirm real DB row count does not change.
4. Confirm OpenClaw env and path freshness.
5. Confirm stale context is not suspected.
6. Send only one Telegram smoke.
7. Immediately verify DB.
8. Immediately verify live Sheets dry-run.

## Official Next Item After This Plan

Run a source audit against scripts and tests to produce a tab-by-tab implementation map for the 11 existing tabs.

The audit must answer:

- which scripts know each tab
- which scripts can write each tab
- which scripts only preview each tab
- which tests cover each tab
- which tabs lack production-safe implementation
- what is the smallest safe next patch

