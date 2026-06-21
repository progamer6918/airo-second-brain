# AIRO Full Auto Sheets Sync v1.1.3 Live dry-run PASS

Status: PASS
Date: 2026-05-10

## Live OAuth dry-run result

Observed live dry-run:

- OAuth token created successfully
- google_read_performed=true
- google_write_performed=false
- approval_phrase_required=false
- write_candidate_count=0
- scope:
  - 💸 Transactions
  - 💳 Credit Card
  - 🔄 Sync Log

## Preview summary

- total_preview_decisions=4
- skip_validation_marker=1
- skip_duplicate=3
- would_write_google=false

## Sheet tabs read live

- 💸 Transactions
- 💳 Credit Card
- 🧾 Review Queue
- 🏠 Cicilan Rumah
- 🔄 Sync Log

## Meaning

The full-auto sync can now read the real Google Sheet using OAuth.

Since write_candidate_count=0, no manual apply is needed for the current state.

## Timer

The systemd service was patched to use AIRO_SYNC_PYTHON from the local venv.

Next step is enabling the user timer and testing one new Telegram transaction.
