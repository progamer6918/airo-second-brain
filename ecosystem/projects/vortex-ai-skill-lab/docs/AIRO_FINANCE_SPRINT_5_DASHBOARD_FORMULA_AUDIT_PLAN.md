# AIRO Finance - Sprint 5 Dashboard Formula Audit Plan

Date: 2026-05-26
Sprint: Sprint 5 - Dashboard Analytics
Status: ACTIVE - AUDIT PLAN ONLY

## 1. Context

Sprint 5 reconciliation contract is already committed.

This step defines how existing dashboard formulas and dashboard-related Apps Script code must be audited before any dashboard analytics patch.

This step must not edit runtime writer behavior, deploy Apps Script, update Cloudflare Worker, or edit live Google Sheet formulas.

## 2. Current Source-of-Truth Contract

Dashboard Analytics must follow the Sprint 5 reconciliation contract:

- Account Ledger is the primary source for wallet movement analytics.
- Finance Events is the event index and lineage source.
- Domain tabs may support domain-specific metrics.
- Legacy Cash Ledger must not be the primary source for new cash movement analytics.
- Transactions must not replace Finance Events for event lineage.

## 3. Audit Goals

The audit must identify:

1. Existing dashboard or summary functions in Apps Script.
2. Existing formula-generating code such as SUMIFS, QUERY, FILTER, and setFormula.
3. Any formulas still reading legacy Cash Ledger as a primary source.
4. Any formulas still reading Transactions as a primary analytics source.
5. Any formulas that ignore Account Ledger.
6. Any formulas that cannot be reconciled against Finance Events.
7. Any monthly review or net worth panels that depend on legacy assumptions.
8. Any dashboard tab creation or cleanup helper that could overwrite user-visible sheets.

## 4. Required Audit Surfaces

The audit must cover these source areas:

- Dashboard functions
- Monthly Review functions
- Net Worth functions
- Cash summary functions
- Account Ledger formulas
- Finance Events formulas
- Review Queue summary formulas
- Any getRange / setFormula / setFormulas block that writes formulas
- Any QUERY / FILTER / SUMIFS formula string

## 5. Allowed Output of Audit Step

The audit step may produce:

- A source inventory of dashboard-related functions
- A list of dashboard tabs or sheets referenced by code
- A list of formula strings and their source tabs
- A risk classification per formula
- A proposed minimal patch plan
- Tests that lock formula source-of-truth expectations

The audit step must not produce:

- Runtime Apps Script patch
- Apps Script deploy
- Cloudflare Worker change
- Telegram smoke
- Live Google Sheet formula edit

## 6. Formula Risk Classification

Each dashboard formula or dashboard source block must be classified as one of:

- safe_account_ledger_based
- safe_finance_events_lineage
- domain_supporting_metric
- legacy_cash_ledger_primary_risk
- transactions_primary_risk
- unreconciled_formula_risk
- destructive_sheet_write_risk
- unknown_needs_manual_review

## 7. Sprint 5 Minimum Dashboard Analytics Patch Criteria

A future dashboard analytics patch may start only after the audit confirms:

1. Account Ledger headers are stable.
2. Finance Events headers are stable.
3. Existing dashboard formula sources are inventoried.
4. Legacy Cash Ledger primary reads are identified.
5. Transactions primary reads are identified.
6. Reconciliation checks are specified before dashboard visuals.
7. The patch scope is limited and reversible.
8. Production Apps Script V2 remains the target.

## 8. Initial Proposed Dashboard Analytics Structure

Sprint 5 dashboard analytics should be built in layers:

Layer 1 - Reconciliation Status
- Count Account Ledger rows missing Finance Events.
- Count Finance Events rows missing Account Ledger source.
- Count duplicate Account Ledger candidates.
- Count Uncategorized or Lainnya spending rows.

Layer 2 - Wallet Movement
- Current balance by account.
- Monthly net movement by account.
- Cash combined and cash split views.

Layer 3 - Spending Analytics
- Monthly spending by category.
- Monthly spending by account.
- Top categories.
- Unknown category warnings.

Layer 4 - Lineage Analytics
- Transaction count by source.
- Event count by source_tab.
- Failed Finance Event emission count if present.

Layer 5 - Final Dashboard Visuals
- Only after Layers 1 to 4 are validated.

## 9. Non-goals For This Step

This step does not close Sprint 5.

This step does not deploy.

This step does not change Apps Script runtime.

This step does not modify live Google Sheet formulas.

This step does not touch birthday reminder files.

## 10. Next Micro-step

After this audit plan is committed, run a source inventory command that extracts dashboard-related functions and formula strings into an audit report.

That next micro-step should still be read-only unless the output clearly supports a safe patch.
