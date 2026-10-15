# Birthday H-1 preparation reminders — active

```json
{
  "TASK": "BIRTHDAY_H1_REMINDER",
  "FINAL_VERDICT": "BERHASIL",
  "H1_ENABLED": true,
  "H_DAY_RETAINED": true,
  "TIMEZONE": "Asia/Jakarta",
  "SCHEDULE": "08:00 WIB daily; one existing timer evaluates day and eve independently",
  "NEXT_RUN_WIB": "Fri 2026-10-16 08:00:00 WIB",
  "DEDUPE": "Independent birthday:target-date and birthday-eve:target-date keys; prior day-of and smoke keys preserved",
  "TESTS": "32/32 offline regressions PASS",
  "DATASET": "68 eligible; existing 6 quarantined records stay excluded",
  "BOT_IDENTITY": "PASS \u2014 earnsai_reminder_bot",
  "RECIPIENT": "PASS \u2014 existing verified private authority",
  "REAL_MESSAGES_SENT_BY_THIS_CHANGE": 0,
  "EARNSART_UNTOUCHED": "PASS \u2014 18 monitored files unchanged",
  "LIVE_SENDER_SHA256": "f2509031646455f4ece49388b8d827bb9fa6d2f2453357add76d7c42c4bf98a2",
  "CHECK_MODE_RESULT": {
    "status": "COMPLETE",
    "reminders": {
      "day": {
        "status": "CHECK_ONLY",
        "eligible_rows": 68,
        "matches": 0,
        "sends": 0
      },
      "eve": {
        "status": "CHECK_ONLY",
        "eligible_rows": 68,
        "matches": 0,
        "sends": 0
      }
    }
  },
  "EXAMPLE": "18 October birthday: 17 October 08:00 WIB preparation reminder, 18 October 08:00 WIB birthday reminder",
  "SESSION_ID": "37fe1fdb-699d-4215-9285-de3c4426e70d",
  "ROLLBACK": "Atomic restore of sender-before.py only if needed; preserve existing private SQLite delivery state and timer; never touch EARNSART"
}
```

The existing private runtime and single persistent timer now process both current-day birthdays and tomorrow preparation reminders. No additional scheduler, credential, recipient, dataset extraction, historical replay, or test notification was introduced. H-1 wording asks the Owner to prepare the greeting design. Birth year remains unknown where source authority marks it unknown. Date arithmetic handles month/year/leap boundaries, and uncertain delivery remains held for reconciliation.
