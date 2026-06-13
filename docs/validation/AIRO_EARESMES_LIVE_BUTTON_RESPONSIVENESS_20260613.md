---
created: 2026-06-13
type: validation
status: partial — 409 conflict blocking live UX (see below)
---

# AIRO Earesmes Live Button Responsiveness Validation
## 2026-06-13

## Summary

Implementation of persistent long-poll Telegram listener for real-time button responsiveness.

---

## Checklist

| Item | Status | Notes |
|---|---|---|
| `telegram-action-listener.py` created | PASS | Persistent long-poll Python listener |
| `telegram-action-listener.sh` created | PASS | Bash wrapper |
| `telegram-listener-status.sh` created | PASS | Health check, no token printed |
| `telegram-listener-stop.sh` created | PASS | Safe shutdown |
| `AIRO-Earesmes-Telegram-Listener.vbs` created | PASS | Popup-free WSL launcher |
| Windows Task `AIRO Earesmes Telegram Listener` | PASS | At logon, wsl.exe, restart on failure |
| `telegram-action-poller.sh` patched | PASS | Sends visible ack message in fallback mode |
| `AIRO_TELEGRAM_ACTIONS_POLICY.md` updated | PASS | Live listener architecture documented |
| `BOOT.md` updated | PASS | Live listener section added |
| `.gitignore` updated | PASS | Runtime state files excluded |
| `readiness` after all changes | PASS — healthy | |
| git push | PASS — 778f5f0 | |
| token not printed | PASS | |
| token not committed | PASS | |
| AIRO Finance untouched | PASS | |

---

## E2E Proof Status

| Step | Status | Notes |
|---|---|---|
| live_listener_installed | PASS | `telegram-action-listener.py` deployed |
| listener_running | PASS | PID=25818, lock file active |
| Windows_task_registered | PASS | State: Ready, wsl.exe trigger |
| smoke_card_sent | PASS | `20260613-live-button-test` sent to Telegram |
| owner_clicked_button | PENDING | Owner must click to complete E2E |
| visible_ack_within_seconds | BLOCKED | See 409 conflict below |
| callback_received | PARTIAL | Poller received prior callback; listener blocked by 409 |
| action_json_stored | PASS | From previous session |
| processor_readback_sent | PASS | From previous session |

---

## Known Issue: 409 Conflict (Critical)

**Root cause:** `python3 scripts/telegram_paper_control_bot.py` (PID 657) dari `earnsai-pulse-trading` sedang melakukan `getUpdates` long-poll menggunakan **bot token yang sama** dengan AIRO Earesmes. Telegram API hanya mengizinkan satu `getUpdates` session per bot token.

**Evidence:**
```
=== [5] CHECK IF 409 PERSISTS WITHOUT OUR LISTENER ===
getUpdates_error: HTTP Error 409: Conflict
```
Ini terjadi bahkan tanpa listener AIRO aktif sama sekali.

**Impact:**
- Live listener tidak bisa melakukan `getUpdates` selama earnsai bot aktif.
- Tombol Telegram tidak akan responsif secara live.
- Fallback: `telegram-action-poller.sh` dipanggil saat runtime scheduler berjalan.

**Fix options (owner decision required):**
1. Hentikan earnsai paper control bot dan gunakan bot token terpisah untuk earnsai.
2. Atau buat Earesmes menggunakan bot token terpisah dari earnsai.
3. Owner bisa hentikan earnsai bot sementara: `pkill -f telegram_paper_control_bot.py`

**Mitigasi yang sudah diimplementasi:**
- Listener mendeteksi 409 dan memberi tahu owner via Telegram.
- Backoff eksponensial: 30s → 300s max, lalu retry.
- Jika earnsai bot berhenti, listener AIRO akan otomatis aktif kembali.

---

## Fields (per request format)

```
owner_clicked_button: PENDING (smoke card sent, waiting owner click)
visible_ack_within_seconds: BLOCKED (409 conflict from earnsai bot)
callback_received: PARTIAL (poller worked; listener blocked)
action_json_stored: PASS (from previous session)
processor_readback_sent: PASS (from previous session)
listener_running: PASS (PID active, 409 backoff mode)
fallback_poller_only: true (currently, due to 409 conflict)
```

---

## Resolution Path

Owner harus:
1. Stop earnsai paper control bot: `pkill -f telegram_paper_control_bot.py`
2. OR: Pisahkan bot token antara AIRO Earesmes dan EarnSAI.
3. Setelah conflict resolved, listener AIRO akan otomatis retry dan aktif.

---

## Commits

| Commit | Message |
|---|---|
| `a56b60d` | `fix(airo-brain): make Earesmes Telegram buttons respond live` |
| `623f4ae` | `fix(earesmes): handle 409 conflict gracefully, fix double-log, notify owner` |
| `778f5f0` | `fix(gitignore): exclude inbox/telegram-actions and state/runtime runtime files` |
