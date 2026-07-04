---
title: AIRO Finance Dashboard Lite Data Contract
status: owner-approved-working-scope
date: 2026-07-04
project: AIRO Finance
scope: dashboard-lite-rescope
mutation_class: docs-only
---

# AIRO Finance Dashboard Lite Data Contract

## Status

Dashboard Lite is the next owner-directed dashboard target for AIRO Finance.

This document canonicalizes the owner working scope for the next dashboard work. It does not claim runtime deployment, spreadsheet mutation, Apps Script deployment, or scheduler activation.

## Evidence Boundary

- Previous dashboard runtime work remains historical evidence.
- Gate 11B production dashboard remains the current rollback/reference baseline until Dashboard Lite has its own runtime/readback/visual sanity evidence.
- Scheduler remains intentionally parked/off unless the Owner explicitly approves scheduler work.

## Final Naming

| Layer | Final Name |
|---|---|
| Workbook active tab | `Dashboard` |
| Product/design name | `AIRO Finance Dashboard Lite` |
| Data contract name | `Dashboard Lite Data Contract` |
| Previous dashboard baseline | `Dashboard v2 / Gate 11B Production Baseline` |

The final active workbook tab remains `Dashboard`. `Dashboard Lite` is a product/design/doc name, not the primary active sheet tab name.

## Dashboard Lite Sections

### 1. Topbar

Required output:

- sync timestamp;
- month filter;
- year filter.

The sync timestamp should update when dashboard refresh occurs or when transaction-driven refresh occurs.

### 2. Spending Intelligence - Category

Source:

- `Account Ledger`.

Include rule:

- selected month/year only;
- `type = expense`;
- `OUT > 0`.

Exclude rule:

- `transfer_in`;
- `transfer_out`;
- `cc_payment`;
- `debt_payment`;
- `asset_purchase`;
- `income`;
- `cash_in`;
- `cash_out`;
- category `Transfer`.

Required output:

- top 5 categories;
- `Lainnya`;
- current selected period amount;
- versus previous month;
- contribution percentage.

### 3. Spending Intelligence - Subcategory

Source:

- `Account Ledger`.

Use the same include/exclude rule as category spending.

Required output:

- top 10 subcategories;
- `Lainnya`;
- current selected period amount;
- versus previous month;
- contribution percentage.

### 4. Wallet Summary

Source:

- final wallet/account balance values from the relevant account/domain source.

Required output:

- all active wallets;
- each active wallet balance;
- total active wallet balance.

Do not include wallet `LEVEL` or `STATUS` in Dashboard Lite.

### 5. Credit Card Summary

Source:

- final Credit Card domain/projection values.

Required output:

- due bill / tagihan jatuh tempo;
- current-period bill / tagihan periode berjalan;
- Blu Pocket CC balance/deposit value.

Dashboard Lite should read final values from the Credit Card domain. It should not rebuild complex Credit Card logic inside the dashboard renderer.

### 6. Gold / Emas Summary

Source:

- final Asset/Gold projection values.

Required output:

- total grams;
- total gold value.

Dashboard Lite should read final values from the asset/gold domain. It should not rebuild complex asset valuation logic inside the dashboard renderer.

### 7. House Installment / Cicilan Rumah Summary

Source:

- final debt/installment projection values.

Required output:

- installment count as `x/120`;
- progress percentage.

Dashboard Lite should read final values from the debt/installment domain. It should not rebuild complex debt amortization logic inside the dashboard renderer.

## Anti-Scope

Dashboard Lite must not include:

- Smart Insight;
- Executive Command Center;
- complex Action Required panel;
- large Data Quality Center;
- wallet `LEVEL`;
- wallet `STATUS`;
- scheduler activation;
- domain recalculation inside the dashboard;
- Apps Script deployment without explicit owner approval;
- workbook mutation without explicit owner approval.

## Migration Rule

Before Dashboard Lite runtime evidence exists:

- active workbook tab `Dashboard` remains the Gate 11B production baseline;
- Dashboard Lite is a design/data-contract target only.

After explicit owner-approved implementation and runtime evidence:

- active workbook tab `Dashboard` becomes AIRO Finance Dashboard Lite;
- previous Dashboard v2/Gate 11B state remains historical baseline and rollback reference.

## Next Safe Gate

The next safe execution gate is read-only mapping audit:

- identify exact source tabs/ranges/functions for each Dashboard Lite section;
- do not deploy;
- do not mutate workbook;
- do not activate scheduler;
- do not claim PASS without evidence.
