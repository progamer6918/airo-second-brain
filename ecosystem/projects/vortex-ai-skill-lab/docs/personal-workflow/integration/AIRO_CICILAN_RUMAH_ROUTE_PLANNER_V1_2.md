# AIRO Cicilan Rumah Route Planner v1.2

Status: IMPLEMENTED / READ-ONLY PLANNER
Date: 2026-05-11
Scope: AIRO Finance Sheet Workflow

## Purpose

This artifact adds a local read-only planner for 🏠 Cicilan Rumah routing.

It supports the v1.1.8 Google Sheet Finance design:

- total tenor: 120
- known paid count as of May 2026: 53 / 120
- standard installment: Rp1.543.000
- usual paid amount: Rp1.570.000
- due day: every 7th

## Behavior

Supported examples:

- hari ini sudah bayar cicilan rumah
- bayar cicilan rumah 1543000

If amount is missing, the planner can use the usual paid amount Rp1.570.000 by default.

If defaulting is disabled or the message is not clearly Cicilan Rumah, the planner routes to:

🧾 Review Queue

## Artifact

Script:

scripts/personal-workflow/airo_cicilan_rumah_planner.py

Test:

tests/personal-workflow/test_airo_cicilan_rumah_planner.py

## Safety

The planner is dry-run only.

It performs:

- no Google write
- no SQLite mutation
- no credential read
- no OpenClaw restart

## Next Item

Integrate the planner into the dry-run/write-preview mapper so Cicilan Rumah candidates can be produced safely before any production write.
