# Earesmes Telegram Message Templates

This document outlines the templates, buttons, and formats used for sending messages through `ops/notifications/telegram-notify.sh`.

## 1. Manual Queue Action Card
Sent when pending captures exist in `inbox/manual-sync-queue.md`.

**Message:**
```text
🟡 Ada capture baru di Manual Sync Queue.

Judul:
Correct Product Direction: Automated Template Onboarding

Intinya:
Arah Report Automation bukan RPT003 doang.
Target aktif harus Automated Template Onboarding and Mapping Engine.
R8.11 tetap frozen baseline.
Platform belum boleh disebut complete.

Mau diapain?
```

**Inline Buttons:**
- `[Proses ke canonical]` -> `manualqueue:canonicalize:<capture-id>`
- `[Lihat detail]` -> `manualqueue:detail:<capture-id>`
- `[Tunda]` -> `manualqueue:defer:<capture-id>`
- `[Arsipkan]` -> `manualqueue:archive:<capture-id>`

---

## 2. Owner Review Card
Sent when pending review items exist in `reviews/owner-review-queue-20260612.md`.

**Message:**
```text
🟡 Ada review pending.

1. CC Ledger-first Production Deploy — verify first
2. CC Ledger-first Source Patch — verify first
3. Dashboard Audit + Patch Split Decision — defer
4. Task 9 CC Parser Deploy — verify first
5. AIRO Sync Operating Rule — verify first
6. Semantic Proposal airo-finance — defer

Pilih mode aman:
```

**Inline Buttons:**
- `[Lihat detail]` -> `ownerreview:summary`
- `[Defer verify-first]` -> `ownerreview:defer_verify_first`
- `[Proses aman]` -> `ownerreview:process_safe`
- `[Tunda 12 jam]` -> `ownerreview:snooze12h`
