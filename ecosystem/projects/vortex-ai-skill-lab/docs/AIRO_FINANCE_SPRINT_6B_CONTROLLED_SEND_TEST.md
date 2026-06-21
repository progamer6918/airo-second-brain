# AIRO Finance Sprint 6B - Controlled Send Test

Status: Sprint 6B controlled test patch.

Admin command:

    admin alerts sprint6b send test

Behavior:
- sends exactly one alert test to the requesting Telegram chat
- writes one audit/cooldown record to _AIRO_Audit_Log when available
- does not create trigger
- does not enable scheduled alerts
- does not spam

Expected:
- proactive_send_performed: true
- trigger_created: false
- sent_count: 1
- audit_written: true
