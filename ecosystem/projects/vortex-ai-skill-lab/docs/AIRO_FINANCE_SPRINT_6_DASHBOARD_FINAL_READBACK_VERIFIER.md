# AIRO Finance Sprint 6 - Dashboard Final Readback Verifier

Status: Sprint 6 verification patch.

## Reason

Controlled build returned success, but generic smoke find returned 0 match for Dashboard markers.

This patch adds a dedicated read-only Dashboard verifier.

## Admin Commands

    admin dashboard sprint6 readback
    admin dashboard sprint6 verify
    admin dashboard sprint6 check

## Safety

This route is read-only.

Expected:
- write_performed: false
- google_write_performed: false

## Verification

The readback checks:
- Dashboard actual tab name
- Dashboard rows and columns
- required Dashboard markers
- backup tab count
- latest backup tab
- _AIRO_Audit_Log existence
- recent audit rows for build event
- Dashboard preview from A1:G14

## Live Pass Rule

Sprint 6 Dashboard Final controlled build can be recorded as live pass if:

    required marker pass = 6/6
    Dashboard found = true
    Backup tab count >= 1
    Cash Ledger dependency marker = OK
    Data Quality Center marker = OK
