# AIRO Finance Sprint 6 - Ensure Audit Log Tab

Status: Sprint 6 prerequisite fix.

## Reason

Sprint 6 dry-run plan now detects the existing Dashboard and all main source tabs, but still reports:

    _AIRO_Audit_Log: MISSING

Dashboard Final includes Data Quality Center and audit count.
Therefore _AIRO_Audit_Log must exist before final build, or Dashboard must show audit unavailable.

Decision:
- Ensure _AIRO_Audit_Log exists.
- This is not a dashboard repaint.
- This is a controlled prerequisite for Data Quality Center.

## Admin Commands

    admin ensure audit log
    admin sprint6 ensure audit log

## Expected Write

This command is allowed to write because it creates/verifies the audit log tab.

Expected:
- write_performed: true
- google_write_performed: true
- tab: _AIRO_Audit_Log
- created: true or false

## Headers

    timestamp
    actor
    event_type
    severity
    source
    message
    ref
    metadata_json

## Next

After live pass:

    admin dashboard sprint6 plan

Expected:
- _AIRO_Audit_Log: OK
- Existing Dashboard found: true
