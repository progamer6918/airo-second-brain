# AIRO Finance Sprint 7 - Manual Sample Email Preview

Status: implemented as dry-run Telegram admin command.

Telegram command prefix:
admin email sprint7 sample preview

Example command:
admin email sprint7 sample preview Blu debit notification sample Rp125000 merchant Kopi Kenangan

Safety contract:
- Mode: dry-run
- Write performed: false
- Email ingestion enabled: false
- Email default OFF: true
- Dry-run only: true
- Input mode: manual sample text or mock payload only
- Output mode: preview object only
- Live email scan allowed: false
- Auto write allowed: false
- Gmail read performed: false
- Mailbox read performed: false
- Mail trigger created: false
- Finance write performed: false
- Account Ledger write performed: false
- Finance Events write performed: false
- Review Queue write performed: false
- Full email body storage allowed: false
- Sample text stored: false
- OTP/security hard-block before finance parse: true

Required preview fields:
- source_message_id
- sender
- subject
- received_at
- merchant
- amount
- currency
- transaction_date
- payment_method
- category_guess
- confidence
- duplicate_key
- needs_review_reason

Next valid step after Telegram live readback: record live pass, then add negative OTP/security sample preview test.

## Merchant extraction fix

Date: 2026-05-27

Reason:

The first live Telegram readback showed merchant was extracted as:

ion sample Rp125000 merchant Kopi Kenang

Expected merchant:

Kopi Kenangan

Root cause:

The previous merchant regex allowed the token "di" without a word boundary, so it could match inside the word "notification".

Fix:

- Prefer explicit labels: merchant, toko, store.
- Only use "di" or "at" as standalone words.
- Clean amount and generic words from merchant candidate.
- Keep all Sprint 7 safety gates unchanged.

Verified expected sample:

admin email sprint7 sample preview Blu debit notification sample Rp125000 merchant Kopi Kenangan

Expected merchant:

Kopi Kenangan

## Merchant extraction fix recovery

Date: 2026-05-27

Reason:

The first merchant fix test failed on:

BCA transaksi Rp240000 di Tokopedia

The extractor needed to prioritize standalone place tokens before broader transaction-context parsing.

Expected verified merchant outputs:

- Blu debit notification sample Rp125000 merchant Kopi Kenangan -> Kopi Kenangan
- BCA transaksi Rp240000 di Tokopedia -> Tokopedia
- credit card purchase at Starbucks Rp58000 -> Starbucks

Safety gates remain unchanged:

- no Gmail read
- no mailbox read
- no mail trigger
- no finance write
- no Account Ledger write
- no Finance Events write
- no Review Queue write

## Merchant extraction token fix

Date: 2026-05-27

Reason:

Regex-based merchant extraction was replaced with deterministic token parsing after failed recovery tests.

Verified intent:

- The word notification must not be treated as the Indonesian token di.
- Standalone di Tokopedia must return Tokopedia.
- Standalone at Starbucks must return Starbucks.
- Explicit merchant Kopi Kenangan must return Kopi Kenangan.

Safety gates remain unchanged:

- no Gmail read
- no mailbox read
- no mail trigger
- no finance write
- no Account Ledger write
- no Finance Events write
- no Review Queue write

## Sensitive hard-block before finance parse fix

Date: 2026-05-27

Reason:

Negative OTP/security Telegram readback correctly returned parse_status skipped_sensitive, but still extracted finance fields:

- amount: 123456
- payment_method: BCA

This violated the Sprint 7 rule that OTP/security samples must be hard-blocked before finance parsing.

Fix:

- Detect sensitive keyword before amount, merchant, payment method, and category extraction.
- Return preview object with amount 0 and blank finance fields for sensitive samples.
- Keep parse_status skipped_sensitive and confidence 0.
- Keep all no-write/no-Gmail/no-trigger safety gates unchanged.

Expected negative sample result:

admin email sprint7 sample preview OTP kode verifikasi login 123456 dari BCA jangan bagikan kode ini

Expected:

- amount: 0
- currency: blank
- payment_method: blank
- merchant: blank
- category_guess: blank
- confidence: 0
- parse_status: skipped_sensitive
- sensitive_skip_reason: blocked_keyword_otp

## Manual fixture quality fix

Date: 2026-05-27

Reason:

Additional Telegram manual sample fixture readback found two parser quality issues:

- Starbucks sample returned blank category_guess.
- Refund Tokopedia sample returned merchant as Tokopedia kartu kredit.

Fix:

- Add Starbucks/coffee/cafe keywords to Makan category guess.
- Remove payment-method tokens from merchant cleanup: kartu, kredit, credit, card, cc.
- Keep Refund priority before Makan.
- Keep all Sprint 7 safety gates unchanged.

Expected verified fixtures:

- BCA transaksi Rp240000 di Tokopedia -> merchant Tokopedia, amount 240000, payment_method BCA, needs category clarification.
- credit card purchase at Starbucks Rp58000 -> merchant Starbucks, amount 58000, payment_method Credit Card, category_guess Makan.
- refund reversal Rp75000 merchant Tokopedia kartu kredit -> merchant Tokopedia, amount 75000, payment_method Credit Card, category_guess Refund.

Safety gates remain unchanged:

- no Gmail read
- no mailbox read
- no mail trigger
- no finance write
- no Account Ledger write
- no Finance Events write
- no Review Queue write
