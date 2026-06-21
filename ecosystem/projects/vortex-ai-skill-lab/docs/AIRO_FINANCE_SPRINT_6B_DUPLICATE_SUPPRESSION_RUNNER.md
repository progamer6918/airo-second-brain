# AIRO Finance Sprint 6B - Duplicate Suppression Runner

Status: Sprint 6B duplicate suppression runner patch.

Admin commands:

    admin alerts sprint6b duplicate check
    admin alerts sprint6b duplicate runner
    admin alerts sprint6b duplicate verify

Behavior:
- read-only
- uses cooldown suppression readback
- evaluates alert candidates
- marks suppressed alerts as BLOCK_DUPLICATE
- marks remaining alerts as WOULD_SEND_IF_TRIGGER_ENABLED
- sends no proactive alert
- creates no trigger
- writes no sheet data

Expected for target key:

    data_status_warning:20260527:WARNING
    target_decision: BLOCK_DUPLICATE
