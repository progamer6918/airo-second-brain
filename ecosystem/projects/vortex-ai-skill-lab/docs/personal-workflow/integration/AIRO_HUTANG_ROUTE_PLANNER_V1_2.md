# AIRO Hutang Route Planner v1.2

Status: IMPLEMENTED / READ-ONLY PLANNER
Date: 2026-05-11
Scope: AIRO Finance Sheet Workflow

## Purpose

This artifact adds a local read-only planner for 🤝 Hutang routing.

It supports the v1.1.8 Google Sheet Finance design for active debts:

- HT-001 Mamak Egit: Rp15.000.000
- HT-002 Bapak Egit: Rp5.000.000
- HT-003 Mamak Nurul: Rp5.000.000

## Behavior

Supported examples:

- hari ini bayar hutang ke mamak egit 1 juta
- bayar hutang ke bapak egit 500rb pakai bca

The planner produces:

- hutang_payment_candidate
- debt_id
- creditor
- amount
- optional account
- balance_before
- balance_after

If amount or creditor is unclear, the planner routes to:

🧾 Review Queue

## Artifact

Script:

scripts/personal-workflow/airo_hutang_planner.py

Test:

tests/personal-workflow/test_airo_hutang_planner.py

## Safety

The planner is dry-run only.

It performs:

- no Google write
- no SQLite mutation
- no credential read
- no OpenClaw restart

## Next Item

Integrate the planner into the dry-run/write-preview mapper so Hutang candidates can be produced safely before any production write.
