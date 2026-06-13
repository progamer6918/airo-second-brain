# AIRO Telegram Actions Policy

Earesmes Telegram interface allows the owner to take quick governance decisions directly from chat messages using inline keyboard callback actions.

## Security Rules

1. **Owner-Only Authentication**: The callback poller and processor must verify the incoming message sender `chat_id` against `/home/egitaristorandas/.airo/telegram.env`. Callbacks from unverified chats must be ignored and logged as errors.
2. **Secrets Protection**: Never print, log, or commit tokens, bot credentials, or chat IDs.
3. **No Auto-Promotion**: High-risk deploy/source claims and semantic proposals must not be auto-promoted. Any promotion or canonicalization must happen via explicit owner callback approval.
4. **Action Queue Staging**: Callback actions are staged in `inbox/telegram-actions/` as pending action files. The poller only captures inputs; the processor executes actions during the scheduled runner cycle.

## Supported Telegram Actions

- `manualqueue:canonicalize:<capture-id>`: Process queue item into canonical docs.
- `manualqueue:detail:<capture-id>`: Send detailed text of the capture.
- `manualqueue:defer:<capture-id>`: Move capture to deferred backlog.
- `manualqueue:archive:<capture-id>`: Move capture directly to archive.
- `ownerreview:summary`: List pending review items.
- `ownerreview:defer_verify_first`: Move high-risk items to deferred backlog.
- `ownerreview:process_safe`: Archive processed queue items safely.
- `ownerreview:snooze12h`: Snooze review notifications for 12 hours.
