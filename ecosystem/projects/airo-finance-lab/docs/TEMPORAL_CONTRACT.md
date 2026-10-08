# Finance event and source times

Event timestamps are offset-aware and normalized to UTC for new writes. The business calendar and all user-facing clock displays use Asia/Jakarta (WIB), independent of the host or device timezone. Existing offset-bearing timestamps are not rewritten by migration.

## Clock contract

- `occurred_at`: nullable event instant; `time_precision`: DATE, MINUTE, SECOND; `time_accuracy`: CONFIRMED, ESTIMATED, UNKNOWN.
- `time_source`: attribution, separate from certainty. Owner-supplied shared clocks can be estimates.
- `source_sent_at`, `source_received_at`, `source_id`: input evidence, preserved before routing. Telegram callback card dates are not owner message dates.
- `message_at` remains a compatibility field; Gmail received timestamps are not presented as message send timestamps.
- `created_at` / `updated_at` retain their recording/configuration meaning.
- Billing periods, due dates, installment schedules, valuation dates and budget months remain calendar values. Metadata-only time edits preserve ledger dates and ordering.

## Coverage

| Domain | Posting owner | Time handling |
| --- | --- | --- |
| Expenses, income, refund | create_transaction | Event clock plus input provenance |
| Transfer and pocket transfer | transfer_funds | Both ledger sides share one clock |
| Payment split | IntakeService | Payment posting lines share a clock; funding transfers remain independent |
| Card / PayLater purchase | record_credit_card_purchase | Purchase clock; billing period is separate |
| Card payment | record_credit_card_payment | Payment and linked ledger carry the same clock; web statement payment uses Core |
| Loan disbursement | create_liability + create_transaction | Disbursement date/time independent from maturity and due dates |
| Loan repayment | record_liability_payment | Payment and linked ledger share a clock |
| Asset purchase | record_asset_purchase | Purchase event timestamp |
| Valuation / gold lot | record_asset_valuation | Valuation date required; optional clock, otherwise unknown |
| Account, category, budget, statement and schedule setup | Existing configuration methods | Creation/update times and calendar periods; no invented payment clock |

Posting methods validate before writes and preserve atomicity across nested Core methods. The shared SQLite connection is protected by a reentrant lock. Gmail and batch approval pass their original event context, rather than the approval message time.

## Web and Telegram use

Transaction history displays event time and approximation marks. Detail views separate event, source and recording clocks. New financial forms support current time (estimate at submission), explicit time with certainty, or unknown time. A past date disables automatic current time. Financial corrections and time corrections have distinct controls.

- `Ubah waktu`: single transaction, payment or valuation; preview first.
- Batch selection: `Ubah jam yang dipilih`; original dates stay fixed.
- `Waktu seluruh domain`: payment/valuation history and source detail, including entries without a linked cash transaction.
- `Pemulihan waktu`: persisted historical preview, grouped by confidence. One approval applies selected groups; remaining groups can be reviewed after restart.
- Telegram example: `ubah jam transaksi tx_EXAMPLE jadi 12.05`.
- Telegram example: `ubah jam batch ABC123 jadi 17.30 perkiraan`.

The temporal preview is persistent, expands linked payment records and transfer sides, rejects conflicting changes, and compares the current record against the preview snapshot before applying. Repeated approval does not replay financial operations. Metadata changes and temporal audit records commit atomically. Existing time-dependent learned rules are quarantined when relevant time evidence changes; trusted category labels remain intact. Only CONFIRMED event times provide lunch/dinner learning features, converted to WIB.

## Recovery

`scripts/finance_time_recovery.py` builds a preview only. Gmail full MIME content is decoded transiently; only structured time evidence is cached. Source IDs and direct review-to-ledger links are required for Gmail matching. Historical receipts with conflicting dates/clocks remain unresolved. A single Telegram JSON export can recover source send timestamps through an unambiguous full-input match; it does not manufacture actual transaction time from a delayed chat. Raw exports and email bodies stay out of Git and logs.

The preview/apply endpoints are `/api/time/preview` and `/api/time/apply`; durable previews can be read through `/api/time/proposals`. `/api/time/domains` exposes current event records and their provenance. CSV and existing JSON responses include temporal metadata. No historical approval is implicit in code deployment.

## Rollback

Stop ingestion before a code rollback. Preserve the latest database, transactions, additive temporal columns and audit records. Never replace a live database with a pre-deployment backup after new owner transactions exist.
