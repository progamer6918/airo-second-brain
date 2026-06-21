# AIRO Telegram Local Handler Persistence v0.6

Status: IMPLEMENTED / NO SERVICE RESTART
Date: 2026-05-10

## Trigger

Runtime inspection showed the active Telegram process is launched from:

/home/egitaristorandas/earnsai-pulse-trading/scripts/telegram_paper_control_bot.py

The source-of-truth repo does not contain that bot file. The relevant repo handler candidate is:

airo_personal_workflow/telegram/local_handler.py

It contains record_transaction behavior and the unresolved account phrase.

## Decision

Patch the source-of-truth local handler, not the runtime/trading path.

Added persistence helper:

scripts/personal-workflow/airo_transaction_persistence.py

Patched handler:

airo_personal_workflow/telegram/local_handler.py

## Behavior

The persistence helper:

- writes to canonical SQLite DB
- inserts transaction rows
- ensures account row exists
- normalizes blubca/blu to BLU BCA
- writes audit row when possible

The local handler now calls the persistence helper after `record_from_text(text)` for `record_transaction`, then updates `saved.account_name` / `payment_method` for the user-facing response.

## Smoke test

A temporary SQLite DB smoke test passed:

- input: catat beli makan siang 12000 pakai blubca
- amount: 12000
- category: makan
- payment_method: BLU BCA
- transaction row inserted

## Safety

- no Google write
- no credential read
- no production DB mutation during smoke test
- no service restart
- no direct patch to earnsai-pulse-trading runtime path

## Next official item

Deploy/reload the normal Telegram/Airo runtime path so it uses this source-of-truth handler, then retry Telegram capture and rerun sync preview.
