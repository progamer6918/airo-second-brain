# AIRO Telegram Actions Policy

Earesmes Telegram interface allows the owner to take quick governance decisions directly from chat messages using inline keyboard callback actions.

## Security Rules

1. **Owner-Only Authentication**: The callback poller/gateway and processor must verify the incoming message sender `chat_id` against `/home/egitaristorandas/.airo/telegram.env`. Callbacks from unverified chats must be ignored and logged as errors.
2. **Secrets Protection**: Never print, log, or commit tokens, bot credentials, or chat IDs.
3. **No Auto-Promotion**: High-risk deploy/source claims and semantic proposals must not be auto-promoted. Any promotion or canonicalization must happen via explicit owner callback approval.
4. **Action Queue Staging**: Callback actions are staged in `inbox/telegram-actions/` as pending action files before processing.
5. **Idempotency**: Each callback_id is processed only once. Duplicates are rejected silently.
6. **Callback Data Limit**: `callback_data` must stay ≤ 64 bytes. Short callback IDs are mandatory because Telegram's limit is strict.
7. **No Hardcoded IDs**: Manual queue callback IDs must be dynamically generated from parser/short ID map. Never hardcode them.

## Live Button Responsiveness (v0.4.2+)

**Requirement**: Owner must receive visible acknowledgement within seconds of clicking any inline button.

### Architecture

```
[Owner clicks button]
       ↓
[Telegram server → long-poll]
       ↓
[telegram-gateway.py] (Centralized Gateway, owns getUpdates)
       ↓
   1. answerCallbackQuery  → stops button spinner immediately
   2. sendMessage          → "🫡 Diterima. Aku proses sebentar."
   3. Stage action JSON    → inbox/telegram-actions/<callback_id>.json (with resolved ID)
   4. Run processor inline → readback result
```

### Components

| Component | Path | Role |
|---|---|---|
| Telegram Gateway | `ops/telegram/telegram-gateway.py` | Single `getUpdates` consumer & router |
| Gateway Wrapper | `ops/telegram/telegram-gateway.sh` | Bash entrypoint |
| Status Checker | `ops/telegram/telegram-gateway-status.sh` | Status & health check |
| Redirector | `ops/telegram/telegram-action-listener.py` | Overwritten with transparent exec redirector to gateway |
| Windows Task | `AIRO Earesmes Telegram Listener` | Triggers redirector/gateway at logon |

### Gateway Ownership & getUpdates Policy

- **Single getUpdates Owner**: `telegram-gateway.py` is the **only** authorized consumer of `getUpdates` for the primary AIRO bot token.
- **No Competing Consumers**: Other bots, systems, or platforms (including EarnSAI/Hermes Agent) **must not** call `getUpdates` using the same bot token. Doing so results in `409 Conflict` errors and breaks live responsiveness.
- **EarnSAI / Hermes Agent routing**: EarnSAI/Hermes Agent must either:
  1. Use a separate, dedicated Telegram bot token.
  2. Or consume updates routed by the Gateway via file-based IPC folder (`~/.config/earnsai-pulse/gateway-inbox`).

### Short ID Mapping (64-byte Limit)

Because Telegram limits `callback_data` to 64 bytes, long manual queue capture IDs (e.g., `20260613-live-button-responsiveness-smoke-test`) cannot be directly sent in callbacks.
- **Rule**: If `callback_data` exceeds 64 bytes, the sender must generate a short ID mapping of format `mq-YYYYMMDD-NNN` (using `scripts/airo-manual-queue-shortid`).
- **Storage**: The mapping is saved to `state/runtime/manual-queue-short-id-map.json`.
- **Resolution**: The Gateway resolves the short ID back to the full capture ID before staging and running the processor.

### Post-Detail Decision Card UX

After Earesmes retrieves the capture details for `manualqueue:detail`, it must send the detail markdown message followed by a decision follow-up card:
- **Pesan**: `Mau diapain dengan capture ini?`
- **Inline Keyboard (Real Capture)**:
  - `Proses ke canonical` (`manualqueue:canonicalize:<short-id>`) - only if target canonical files exist and status is real pending.
  - `Tunda` (`manualqueue:defer:<short-id>`)
  - `Arsipkan` (`manualqueue:archive:<short-id>`)
  - `Kembali` (`manualqueue:back:<short-id>`)
- **Inline Keyboard (Smoke/Test Capture)**:
  - `Arsipkan smoke test` (`manualqueue:archive:<short-id>`)
  - `Kembali` (`manualqueue:back:<short-id>`)
- **Back Navigation**: Clicking `Kembali` (`manualqueue:back`) re-sends the compact summary card for the same capture.

### Fallback

If the gateway is not running, the periodic runtime scheduler calls `telegram-action-poller.sh` as fallback. The poller also handles short ID resolution, sends visible acknowledgement messages, and supports navigation.
