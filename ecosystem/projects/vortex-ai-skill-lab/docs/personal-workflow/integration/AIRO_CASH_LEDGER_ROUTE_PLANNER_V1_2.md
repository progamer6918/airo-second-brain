# AIRO Cash Ledger Route Planner v1.2

Status: IMPLEMENTED / READ-ONLY PLANNER
Date: 2026-05-11
Scope: AIRO Finance Sheet Workflow

## Purpose

This artifact adds a local read-only planner for 💵 Cash Ledger routing.

It supports two cash workflows from the v1.1.8 Google Sheet Finance design:

1. Cash session:
   - example: saya hari ini pegang cash 100rb
   - operation: cash_session_candidate

2. Cash entry:
   - example: hari ini cash kepake beli makan 20rb
   - operation: cash_entry_candidate

Ambiguous cash messages are routed to:

🧾 Review Queue

## Artifact

Script:

scripts/personal-workflow/airo_cash_ledger_planner.py

Test:

tests/personal-workflow/test_airo_cash_ledger_planner.py

## Safety

The planner is dry-run only.

It performs:

- no Google write
- no SQLite mutation
- no credential read
- no OpenClaw restart

## Next Item

Integrate the planner into the dry-run/write-preview mapper so Cash Ledger candidates can be produced safely before any production write.
