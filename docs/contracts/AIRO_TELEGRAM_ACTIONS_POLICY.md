# AIRO Telegram Actions Policy

Earesmes Telegram interface allows the owner to take quick governance decisions directly from chat messages using inline keyboard callback actions.

## Security Rules

1. **Owner-Only Authentication**: The callback poller and processor must verify the incoming message sender `chat_id` against `/home/egitaristorandas/.airo/telegram.env`. Callbacks from unverified chats must be ignored and logged as errors.
2. **Secrets Protection**: Never print, log, or commit tokens, bot credentials, or chat IDs.
3. **No Auto-Promotion**: High-risk deploy/source claims and semantic proposals must not be auto-promoted. Any promotion or canonicalization must happen via explicit owner callback approval.
4. **Action Queue Staging**: Callback actions are staged in `inbox/telegram-actions/` as pending action files before processing.
5. **Idempotency**: Each callback_id is processed only once. Duplicates are rejected silently.
6. **Callback Data Limit**: `callback_data` must stay ≤ 64 bytes. Use short capture IDs.

## Live Button Responsiveness (v0.4.2+)

**Requirement**: Owner must receive visible acknowledgement within seconds of clicking any inline button.

### Architecture

```
[Owner clicks button]
       ↓
[Telegram server → long-poll]
       ↓
[telegram-action-listener.py] (persistent, always running)
       ↓ immediate (< 5 seconds)
  1. answerCallbackQuery  → stops button spinner
  2. sendMessage          → "🫡 Diterima. Aku proses sebentar."
  3. Stage action JSON    → inbox/telegram-actions/<callback_id>.json
  4. Run processor inline → send readback result
```

### Components

| Component | Path | Role |
|---|---|---|
| Live listener | `ops/telegram/telegram-action-listener.py` | Persistent long-poll loop |
| Listener wrapper | `ops/telegram/telegram-action-listener.sh` | Bash entrypoint |
| Status checker | `ops/telegram/telegram-listener-status.sh` | Health check |
| Stop helper | `ops/telegram/telegram-listener-stop.sh` | Safe shutdown |
| Windows Task | `AIRO Earesmes Telegram Listener` | Auto-start at logon |
| VBS launcher | `ops/windows/AIRO-Earesmes-Telegram-Listener.vbs` | Popup-free WSL launch |

### Persistence

- Listener lock: `state/runtime/telegram-listener.lock`
- Update offset: `state/runtime/telegram-update-offset`
- Log: `logs/telegram-listener.log`
- Windows Task Scheduler triggers listener at logon, restarts on failure.

### Fallback

If the live listener is not running (e.g., system restart before logon), the periodic runtime scheduler calls `telegram-action-poller.sh` as fallback. The poller also sends visible acknowledgement messages.

### Owner Expectation

After clicking any button:
1. Button spinner stops (answerCallbackQuery).
2. A visible message `🫡 Diterima. Aku proses sebentar.` appears in chat.
3. A result readback message appears within 30–60 seconds.

If only the poller is active (no live listener), acknowledgement is delayed until next runtime cycle.

## Supported Telegram Actions

- `manualqueue:canonicalize:<capture-id>`: Process queue item into canonical docs.
- `manualqueue:detail:<capture-id>`: Send detailed text of the capture.
- `manualqueue:defer:<capture-id>`: Move capture to deferred backlog.
- `manualqueue:archive:<capture-id>`: Move capture directly to archive.
- `ownerreview:summary`: List pending review items.
- `ownerreview:defer_verify_first`: Move high-risk items to deferred backlog.
- `ownerreview:process_safe`: Archive processed queue items safely.
- `ownerreview:snooze12h`: Snooze review notifications for 12 hours.

