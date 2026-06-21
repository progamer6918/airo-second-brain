# AIRO Finance - Sprint 5 Reconciliation Contract

Date: 2026-05-26
Sprint: Sprint 5 - Dashboard Analytics
Status: ACTIVE - CONTRACT ONLY

## 1. Context

Sprint 4 Finance Events v1 is closed and live-proven.

Live proof:
- Smoke ID: SMKFEDELTA
- Finance Events row: 8
- Account Ledger row: 62
- Duplicate Account Ledger row: not observed

Sprint 5 must not start by drawing dashboard panels directly.

The first Sprint 5 task is to define the reconciliation contract that analytics must respect.

## 2. Source of Truth Rules

Primary dashboard metrics must use Account Ledger for wallet movement values.

Finance Events must be used as the event index and lineage surface.

Domain tabs may be used for domain-specific supporting metrics, but they must not replace Account Ledger for wallet balances.

Dashboard analytics must not read legacy Cash Ledger as the primary source for new cash movements after Sprint 3.

Dashboard analytics must not use Transactions as a replacement for Finance Events.

## 3. Analytics Source Map

### 3.1 Wallet balances

Source:
- Account Ledger

Required fields:
- entry_id
- date
- account
- amount_in
- amount_out
- balance
- type
- category
- description
- raw_text
- source_tab
- linked_txn_id

Rules:
- Balance is grouped by account.
- Net movement equals amount_in minus amount_out.
- Cash accounts include Cash, Cash Umum, and Cash Bensin.
- Dashboard may display Cash combined and Cash split views.

### 3.2 Spending by category

Source:
- Account Ledger

Required fields:
- date
- account
- amount_out
- category
- type
- raw_text
- linked_txn_id

Rules:
- Spending uses amount_out.
- Income and transfer_in must not be counted as spending.
- Internal transfer handling must not double count in spending.
- Uncategorized or Lainnya rows must be surfaced as data quality warnings.

### 3.3 Event lineage

Source:
- Finance Events

Required fields:
- event_id
- event_ts
- event_type
- event_source
- source_tab
- source_row
- linked_txn_id
- account
- category
- amount
- status
- reason
- payload_json
- notes

Rules:
- Every committed post-cutover transaction should have a Finance Events row.
- Finance Events is append-only.
- Finance Events is not a balance ledger.
- Finance Events must expose failures through status or returned write metadata.

### 3.4 Data quality and reconciliation

Sources:
- Account Ledger
- Finance Events

Required checks:
- Account Ledger rows without linked_txn_id.
- Account Ledger rows without source_tab.
- Duplicate Account Ledger candidates by linked_txn_id.
- Duplicate Account Ledger candidates by raw_text plus amount plus account plus date.
- Finance Events rows without source_tab.
- Finance Events rows without linked_txn_id.
- Account Ledger rows after Sprint 4 cutover with no matching Finance Events event.
- Finance Events transaction_created rows with no matching Account Ledger row.
- Finance Events failed emission metadata if present.

## 4. Reconciliation Status Values

The dashboard analytics layer may classify rows using these statuses:

- reconciled
- missing_finance_event
- missing_account_ledger_ref
- duplicate_account_ledger_candidate
- finance_event_without_source
- needs_category
- ignored_legacy
- manual_review_required

These statuses are for analytics and review. They must not hard-delete source rows.

## 5. Sprint 5 Dashboard Gate

Before any dashboard patch, Sprint 5 must pass these gates:

1. Existing formulas and dashboard surfaces are audited.
2. Account Ledger and Finance Events headers are locked by tests.
3. Reconciliation rules are documented.
4. No runtime write path is changed during the contract step.
5. Birthday/OpenClaw files remain untouched.
6. V2 production remains the Apps Script target.
7. Sprint 4 proof remains preserved in docs.

## 6. Non-goals For This Step

This step must not:
- change Apps Script runtime writer behavior
- deploy Apps Script
- change Cloudflare Worker
- edit Google Sheet formulas live
- create dashboard visuals
- touch birthday reminder files
- close Sprint 5

## 7. Next Micro-step

After this contract is committed, the next micro-step is:

Sprint 5 dashboard formula and reconciliation audit plan.

That next step may inspect current dashboard formulas and propose the minimum safe analytics patch, but it still must not deploy until tests and patch scope are clear.
