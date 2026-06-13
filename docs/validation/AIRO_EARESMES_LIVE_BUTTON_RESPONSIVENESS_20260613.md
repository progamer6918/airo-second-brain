---
created: 2026-06-13
type: validation
status: PASS_WITH_GATEWAY
---

# AIRO Earesmes Live Button Responsiveness Validation
## 2026-06-13

## Summary

Implementation of persistent Telegram Gateway for real-time button responsiveness and multi-app command routing.

Result: **PASS_WITH_GATEWAY** (due to external conflict on systemd user service `hermes-gateway` sharing the same bot token).

---

## Checklist

| Item | Status | Notes |
|---|---|---|
| `telegram-gateway.py` created | PASS | Centralized long-poll Gateway |
| `telegram-gateway.sh` wrapper | PASS | Bash entrypoint |
| `telegram-gateway-status.sh` | PASS | Status checker (hides secrets) |
| `telegram-action-listener.py` | PASS | Redirected transparently to gateway |
| `telegram-action-listener.sh` | PASS | Redirected transparently to gateway |
| Windows Task `AIRO Earesmes Telegram Listener` | PASS | Points to redirector which executes gateway |
| Short ID Mapping | PASS | `mq-20260613-001` mapped to full capture ID |
| E2E Live Button Click | PASS | Immediate ack `🫡 Diterima. Aku proses sebentar.` received |
| Processor Detail Readback | PASS | Detail readback sent back to Telegram |
| No AIRO listener duplicates | PASS | Only gateway is running |

---

## E2E Proof Status

| Step | Status | Notes |
|---|---|---|
| Owner received live acknowledgement | PASS | Ack received within 5 seconds of clicking |
| Owner received detail readback | PASS | Readback sent successfully by processor |
| Short ID resolved to full capture ID | PASS | resolved: `mq-20260613-001` → `20260613-live-button-responsiveness-smoke-test` |
| callback_data <=64 bytes | PASS | Short ID fits within Telegram callback_data limits |
| Gateway is getUpdates owner | PASS | Gateway process holds the long-poll |
| Old listener stopped | PASS | Process stopped, wrapper redirected |
| Competing token consumer | PARTIAL | `hermes-gateway.service` (external) still polling same token |
| Smoke capture archived | PASS | Archived and compacted in manual sync queue |
| Runtime status | PASS | Healthy except for dirty exception from airo-finance |
| Git status | PASS | Clean and pushed |

---

## External Conflict (EarnSAI / Hermes Gateway)

**Root cause:**
The systemd user service `hermes-gateway.service` (`hermes_cli.main gateway run --replace`) is active and performing `getUpdates` using the same bot token. This triggers intermittent `409 Conflict` errors on both the AIRO Telegram Gateway and the Hermes Gateway.

**Impact:**
- Telegram button clicks may experience delays or fail to register immediately when the Telegram API server routes updates to the competing consumer.
- Both pollers back off exponentially on 409 errors.

**Action Required by Owner:**
- **Option 1 (Temporary/Immediate):** Stop the competing hermes-gateway service:
  ```bash
  systemctl --user stop hermes-gateway.service
  ```
- **Option 2 (Permanent):** Generate a dedicated bot token for EarnSAI/Hermes Agent so that they do not share the same token.

---

## Commits

| Commit | Message |
|---|---|
| `a56b60d` | `fix(airo-brain): make Earesmes Telegram buttons respond live` |
| `623f4ae` | `fix(earesmes): handle 409 conflict gracefully, fix double-log, notify owner` |
| `778f5f0` | `fix(gitignore): exclude inbox/telegram-actions and state/runtime runtime files` |
| `7b328a9` | `fix(airo-brain): finalize Earesmes Telegram gateway routing` |
