# AIRO Finance Sprint 6B - Cooldown Suppression Readback

Status: Sprint 6B cooldown verification patch.

Admin commands:

    admin alerts sprint6b cooldown check
    admin alerts sprint6b cooldown readback
    admin alerts sprint6b cooldown verify

Behavior:
- read-only
- scans _AIRO_Audit_Log for alert_key records
- evaluates today's alert candidates
- reports suppressed vs eligible alerts
- checks target key data_status_warning:20260527:WARNING

Expected:
- write_performed: false
- proactive_send_performed: false
- trigger_created: false
- target_key_suppressed: true after ACK live pass
