# Birthday reminder — verified production recovery

AIRO_AGENT_IDENTITY_GUARD=PASS
IDENTITY_CONTRACT_READ=YES
EARESMES_BOT_OWNERSHIP=RESOLVED_SEPARATE_UNTOUCHED
ARFIN_BOT_OWNERSHIP=RESOLVED_SEPARATE_UNTOUCHED
EARNSAI_BOT_OWNERSHIP=RESOLVED_DEDICATED_REMINDER
EVIDENCE_SCOPE_DECLARED=YES
LOCAL_ABSENCE_USED_AS_GLOBAL_ABSENCE=NO
PRODUCTION_SECRET_SCOPE_STATUS=VERIFIED_DEDICATED_OWNER_INPUT_ONLY
OWNER_ARCHITECTURE_DECISION_READ=YES
NEW_BOT_RECOMMENDATION_ALLOWED=NO
TOKEN_ROTATION_RECOMMENDATION_ALLOWED=NO
WEBHOOK_MUTATION_ALLOWED=NO

```json
{
  "TASK": "AIRO_BIRTHDAY_REMINDER_VPS_FINAL_RECOVERY",
  "PARALLEL_ISOLATION": "PASS \u2014 existing approved namespace retained; no repeated isolation audit",
  "EARNSART_UNTOUCHED": "PASS \u2014 18 monitored paths unchanged; no EARNSART lifecycle/process/file mutation",
  "BIRTHDAY_REMINDER": "PASS",
  "BOT_IDENTITY": "PASS \u2014 earnsai_reminder_bot",
  "RECIPIENT_VERIFIED": "PASS \u2014 Owner private dedicated input and getChat exact ID match",
  "DATASET_68_READY": "PASS \u2014 same V3 checksum; 6 quarantined rows excluded",
  "SOURCE_REPAIR": "PASS \u2014 exact tested V4 source installed in dedicated runtime; protected checkout unchanged",
  "DUPLICATE_PREVENTION": "PASS \u2014 V4 27/27 synthetic tests plus durable one-record production smoke ledger",
  "TELEGRAM_DELIVERY": "PASS",
  "TELEGRAM_SMOKE_TEST": "PASS \u2014 exactly one harmless smoke message",
  "TELEGRAM_MESSAGE_ID": 48,
  "SCHEDULER_ACTIVE": "YES \u2014 enabled and active timer",
  "SCHEDULER_PERSISTENCE": "PASS \u2014 Persistent=yes and boot enablement verified; no reboot performed",
  "NEXT_RUN_WIB": "Fri 2026-10-16 08:00:00 WIB",
  "SERVICE_EXECUTION": "PASS \u2014 Result=success, ExecMainStatus=0; no match and no birthday send today",
  "CANONICAL_EVIDENCE": "Published with this receipt; remote parity verified in local final receipt",
  "BLOCKER_IF_ANY": "NONE for the authorized 68-record recovery objective",
  "FINAL_VERDICT": "BERHASIL",
  "SESSION_ID": "0f4865d0-a942-47cd-b1c3-e8fa7c554052",
  "AUTHORITATIVE_RUNTIME_DIR": "/home/ubuntu/.local/lib/airo-birthday-reminder",
  "PRIVATE_RUNTIME_AUTHORITY": "/home/ubuntu/.local/share/airo-birthday-reminder/prepared-dataset.json; status ACTIVE_VERIFIED",
  "dedicated_credential_path": "/home/ubuntu/.config/airo-birthday-reminder/credentials.env (0600; contents private)",
  "source_checksum": "56f0448d2a4e99f30ac1f78e148285a85d11f7fb01847d327abc03414cb59b9c",
  "production_runtime": {
    "production_activated": true,
    "telegram_smoke": "PASS",
    "telegram_message_id": 48,
    "timer": {
      "TimersCalendar": "{ OnCalendar=*-*-* 08:00:00 Asia/Jakarta ; next_elapse=Fri 2026-10-16 08:00:00 WIB }",
      "NextElapseUSecRealtime": "Fri 2026-10-16 08:00:00 WIB",
      "LastTriggerUSec": "",
      "Persistent": "yes",
      "ActiveState": "active",
      "UnitFileState": "enabled"
    },
    "service": {
      "Result": "success",
      "ExecMainStartTimestamp": "Thu 2026-10-15 14:55:43 WIB",
      "ExecMainExitTimestamp": "Thu 2026-10-15 14:55:43 WIB",
      "ExecMainStatus": "0",
      "EnvironmentFiles": "/home/ubuntu/.config/airo-birthday-reminder/credentials.env (ignore_errors=no)",
      "UMask": "0077",
      "User": "ubuntu",
      "ActiveState": "inactive"
    },
    "runtime_release_hashes": {
      "birthday_reminder_simple.py": "135c45bdf9f91d0d328851ec17a5ce81ee011b3a85eced5460d484dc1e81a4e8",
      "run_birthday_reminder": "bd81460491fc92c3ff860ee244d15c2f6e86c5f19e2a3d5938556d2a43cf5d2b"
    },
    "installed_units_match_reviewed_release": true,
    "real_service_execution": "PASS",
    "reboot_test": "NOT_PERFORMED",
    "earnsart_service_actions": [],
    "verified_at": "2026-10-15T07:55:43.968582+00:00"
  },
  "persistence_proof": {
    "durable_smoke_record": "SENT",
    "message_id": 48,
    "smoke_records": 1,
    "daily_birthday_send_records": 0,
    "private_state_mode": "0o600",
    "scheduler_authorities": {
      "system": {
        "birthday_entries": 1,
        "returncode": 0
      },
      "user": {
        "birthday_entries": 0,
        "returncode": 0
      },
      "cron": {
        "birthday_entries": 0,
        "returncode": 1
      }
    },
    "protected_earnsart_paths_unchanged": 18,
    "no_reboot_performed": true
  },
  "smoke_text": "\u2705 AIRO Birthday Reminder VPS recovery test berhasil.",
  "delivery_scope": "Telegram API accepted message with verified recipient and returned message ID; human read status not claimed",
  "reused_evidence": "V3 extraction 11/11 and V4 sender 27/27; no repeated download/extraction or source change",
  "quarantine_disposition": "6 records remain excluded as explicitly authorized by Owner V4; not an active recovery blocker",
  "private_data_publication": false
}
```

## Runtime authority and continuation

The V4 READY_NOT_ACTIVE candidate is now installed only at AUTHORITATIVE_RUNTIME_DIR after real identity and destination verification. Systemd uses that dedicated runtime and dedicated private environment file. The source files in the protected EARNSART checkout and in the approved parallel-session checkout were not overwritten. GitHub source history and this receipt identify the actual live deployment; old cloned source paths are not the execution authority.

The V3 immutable extraction manifest records preparation-time ACTIVATED=false. Current activation authority is the atomic private prepared-dataset.json pointer, now ACTIVE_VERIFIED, plus the verified activation.json and installed unit/readback evidence. No dataset re-extraction or source-workbook mutation occurred.

Timer boot enablement, Persistent=true, explicit Jakarta calendar, next run, exact unit hashes, and actual successful service execution were measured. No reboot was performed. The oneshot service being inactive after success is expected; the timer remains active. The send ledger contains one SENT smoke record with message ID 48 and no daily birthday sends. No further smoke was issued.

Session closeout authority is the existing owning production ledger and its UUID-scoped worklog. Completion is recorded only in the birthday session after canonical evidence publication. No global/daily legacy projection, EARNSART state, ledger, worklog, index, service or process is modified.
