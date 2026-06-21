# Phase 1B Local MVP Runbook

## Goal

Upgrade Airo Personal Workflow from basic parser into local database-backed assistant core.

## Capabilities

- classify transaction intent
- classify installment payment intent
- classify installment check intent
- classify monthly report intent
- save transactions into SQLite
- save installment payments into SQLite
- auto-create installment records when needed
- generate monthly summary
- maintain audit log

## Still Not Included

- Google OAuth
- Drive upload
- Sheets sync
- Docs report generation
- Calendar reminder
- Telegram live bot integration
- OCR

## Test Commands

```bash
python3 -m airo_personal_workflow.cli parse "bayar cicilan rumah 2500000"
python3 -m airo_personal_workflow.cli record "bayar cicilan rumah 2500000"
python3 -m airo_personal_workflow.cli check-installment "Cicilan Rumah"
python3 -m airo_personal_workflow.cli summary --period 2026-05
python3 scripts/personal_workflow_smoke.py
