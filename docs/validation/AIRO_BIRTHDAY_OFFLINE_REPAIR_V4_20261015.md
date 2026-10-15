# Birthday recovery V4 — READY_NOT_ACTIVE

AIRO_AGENT_IDENTITY_GUARD=FAIL (dedicated identity unverified)
PRODUCTION_ACTIVATION_ALLOWED=NO_UNTIL_IDENTITY_AND_RECIPIENT_VERIFIED

```json
{
  "TASK": "AIRO_BIRTHDAY_RECOVERY_V4_OFFLINE_REPAIR",
  "EARNSART_UNTOUCHED": "PASS \u2014 18 monitored paths unchanged; no lifecycle/process writes",
  "DATASET_68_READY": "PASS \u2014 existing V3 checksum and count reused; 6 records remain quarantined",
  "OFFLINE_SENDER_REPAIR": "PASS \u2014 READY_NOT_ACTIVE in independent development checkout",
  "DEDUP_REGRESSION": "PASS \u2014 27/27 offline sender regressions including 8 overlapping processes and interrupted send/commit",
  "SCHEDULER_PREPARED": "PASS \u2014 service/timer syntax verified; 08:00 Asia/Jakarta; Persistent=true; not installed/enabled",
  "BOT_IDENTITY": "UNVERIFIED \u2014 dedicated reference missing",
  "RECIPIENT_VERIFIED": "NO",
  "PRODUCTION_ACTIVATED": "NO",
  "TELEGRAM_SMOKE_TEST": "NOT_SENT",
  "BLOCKER_IF_ANY": "Dedicated earnsai_reminder_bot credential-store reference and authoritative recipient unavailable; supply the dedicated private VPS credentials.env file or an approved store reference, never values in AI chat",
  "FINAL_VERDICT": "TERHAMBAT \u2014 production activation only; authorized offline repair complete",
  "RELEASE_STATUS": "READY_NOT_ACTIVE",
  "REGRESSION_LOG_SHA256": "912b267676038f6fab6edf5dacca898168c34ddf875df6cabd989065aac6ea71",
  "RELEASE_ARCHIVE_SHA256": "7a7525c56f35502ee8c93069c7b63a572f168fabe85692035f21e0710a656f42",
  "release_manifest": {
    "status": "READY_NOT_ACTIVE",
    "created_at": "2026-10-15T07:00:01.619511+00:00",
    "files": {
      "run_birthday_reminder": "bd81460491fc92c3ff860ee244d15c2f6e86c5f19e2a3d5938556d2a43cf5d2b",
      "airo-birthday-reminder.service": "fbcd688c05242869bfaf913ea80ee9a81b5d2894de6eafc24c167cfc764a4faa",
      "airo-birthday-reminder.timer": "d8565d078ebddc05224552432140474e51226acdec0b5d33e78a8c8fb2a17f99",
      "RECOVERY.md": "7b8f09c332543754ca73c92d41f38e2064764abcf27f11414e2654966208032f",
      "birthday_reminder_simple.py": "135c45bdf9f91d0d328851ec17a5ce81ee011b3a85eced5460d484dc1e81a4e8"
    },
    "tested_sender_tests": 27,
    "tests_sha256": "7442a17b194bd32a88d8135ba74f8ce480b7328a7a2d948ba52d89c11013e310",
    "production_installed": false,
    "timer_enabled": false,
    "next_if_activated_wib": "2026-10-16 08:00:00 Asia/Jakarta",
    "actual_scheduled_next_run": "NONE; timer not installed"
  },
  "development_checkout": "/home/ubuntu/Documents/Codex/2026-10-07/halo/birthday-recovery-v4/checkout",
  "production_checkout": "/home/ubuntu/AI_WORKSPACES/airo-parallel-production",
  "production_sender_hashes_unchanged": {
    "birthday_reminder_simple.py": "507f1751061b30edea6f3b644b49fdb7d30a12f0e477e666cc1be6483c9acd50",
    "run_birthday_reminder": "f37cca899288918c523191cb2e676c6a39deece1452be3f84a7b61b8711167ca"
  },
  "production_git_mutations": false,
  "production_sender_deployed": false,
  "systemd_units_installed": false,
  "activation_record_created": false,
  "sender_state_created_in_production": false,
  "real_network_send_calls": 0,
  "source_download_repeated": false,
  "extraction_repeated": false,
  "isolation_audit_repeated": false,
  "conditional_calendar_next_wib": "2026-10-16 08:00 Asia/Jakarta; prediction only, no active timer",
  "actual_next_run_wib": "NONE",
  "private_input_procedure": "Owner terminal: install -d -m700 ~/.config/airo-birthday-reminder; edit credentials.env privately with TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID for the dedicated reminder; chmod 600; report only that file is ready. No tokens/chat IDs in AI chat.",
  "known_limitations": [
    "No real Telegram identity/delivery evidence yet",
    "No actual reboot or power-cut test",
    "SENDING/UNKNOWN entries require external delivery reconciliation; no automatic retry/reset",
    "Private date-conflict row remains excluded with the other five quarantined records; Owner authorized the 68 eligible subset in V4"
  ],
  "OFFLINE_CANONICAL_VERDICT": "BERHASIL",
  "CANONICAL_VERDICT": "TERHAMBAT",
  "clipboard_verified": false
}
```

## Bounded engineering review

The private V3 CSV is read only after checksum, authority, row count, permissions and eligibility checks. No legacy CSV fallback or quarantined-record source is used. Unknown birth year yields no computed age. Message headings, numbered persons, birth-date line, age line and footer preserve the original format; date selection uses Asia/Jakarta. The sender uses only Python standard-library facilities and adds no dependency.

SQLite FULL synchronous intent is committed before any external send. A private flock covers intent, network call and final commit. SENT is idempotent, SENDING/UNKNOWN require reconciliation, and destination changes are rejected. The ledger stores hashes and message IDs, never message content or private raw recipients. Crash-before-call conservatively blocks that attempt; it cannot guarantee delivery under an unobservable crash. This is deliberate duplicate avoidance, not an unsupported exactly-once delivery claim.

Regression evidence covers data eligibility, unknown years, format, Jakarta day boundary, no-match/no-send, same-day edits, restart, simultaneous processes, timeout, invalid acknowledgements, failure after actual synthetic side effect, failure before final state commit, recipient changes and missing/wrong identity. All network sends were mocked. The 11/11 V3 extraction evidence was reused without rerunning extraction. Unit verification emitted only a pre-existing unrelated tat_agent PIDFile warning; no unrelated unit was changed.

The frozen package and this source publication do not install a sender or enable a timer. The existing production checkout stays at its prior commit with unchanged sender files. The new code is held in the separate development clone and public source history only. Existing session ledger/projection receives its own outcome; no new production session or EARNSART lifecycle mutation occurs.

See ops/birthday-reminder/RECOVERY.md for the shortest private input procedure, exact conditional activation checks, ambiguous-outcome reconciliation and scoped rollback.
