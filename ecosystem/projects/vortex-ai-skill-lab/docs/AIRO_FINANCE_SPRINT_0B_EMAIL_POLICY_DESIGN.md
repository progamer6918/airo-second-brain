# AIRO Finance — Sprint 0B Email Policy Design

Status: DESIGN FINALIZATION
Sprint: Sprint 0B — Email Ambiguity Research & Bridge Design
Runtime scope: No Gmail/email ingestion implementation
Canonical source: docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md

## 1. Sprint 0B Boundary

Sprint 0B defines policy and bridge design only.

Allowed:
- Email ambiguity taxonomy.
- OTP/security hard-block policy.
- Email source allowlist and negative keyword policy.
- Email-to-Telegram clarification bridge design.
- Missing category policy for email candidates.
- Duplicate email vs Telegram policy.

Not allowed:
- Gmail OAuth.
- Gmail trigger.
- Email fetching runtime.
- Full email body storage.
- Automatic ledger write from email.
- Apps Script email parser implementation.
- Dashboard Email Ingestion Status activation.
- Sprint 1+ implementation work.

## 2. Email Candidate Classification Order

Future email ingestion must classify in this order:

1. Sensitive hard-block check.
2. Sender/source policy check.
3. Negative keyword check.
4. Finance signal extraction.
5. Ambiguity detection.
6. Duplicate detection against Telegram/manual input.
7. Telegram clarification if ambiguous.
8. Review Queue fallback only after clarification failure or unresolved ambiguity.
9. Controlled routing only after parser is proven in a later sprint.

This order is mandatory because OTP/security content must be stopped before finance parsing.

## 3. OTP/Security Hard-Block Policy

If an email matches sensitive security/OTP patterns, it must be stopped before finance parsing.

Hard-blocked email must not:
- enter finance parser
- be sent to Telegram
- enter Review Queue
- enter Finance Events
- be stored as full body text
- generate ledger/domain writes

Allowed metadata only:
- skipped sensitive count
- timestamp
- source category if safe
- hashed message identifier
- sensitive skip reason

Case-insensitive hard-block terms:
- otp
- one time password
- kode otp
- kode
- kode keamanan
- verifikasi
- verification
- verify your identity
- login
- sign in
- security
- keamanan
- password
- reset password
- atur ulang password
- perangkat
- device
- new device
- 2fa
- two factor
- authentication
- auth code
- recovery
- account recovery
- fraud alert
- suspicious login

## 4. Source Allowlist Policy

Email ingestion remains default OFF.

When later enabled, source policy must use explicit allowlist categories:

| Source Type | Example Category | Default Handling |
|---|---|---|
| Bank notification | BCA/Blu/etc. transaction notification | Candidate only |
| Credit card issuer | Card transaction or billing notification | Candidate only |
| E-wallet | Payment/transfer notification | Candidate only |
| Marketplace payment | Payment success/refund only | Candidate only |
| Unknown sender | Any non-allowlisted sender | Review/suspicious, no clean write |

Real personal sender addresses must live in secure config/project settings, not public docs.

## 5. Negative Keyword Policy

Security-sensitive hard-block negative keywords:
- otp
- verification
- verifikasi
- login
- password
- security
- keamanan
- auth
- 2fa
- device
- recovery

Non-finance negative keywords:
- promo
- promotion
- diskon
- voucher
- newsletter
- survey
- statement available
- tagihan tersedia
- penawaran
- reward
- points
- cashback promo
- marketing

Failed/unclear transaction keywords:
- failed
- gagal
- declined
- ditolak
- reversed
- dibatalkan
- cancelled
- pending
- on hold
- refund
- chargeback

## 6. Email Ambiguity Taxonomy

Email-derived finance candidates are ambiguous when any of these are true:

| Ambiguity Type | Required Handling |
|---|---|
| Missing amount | Telegram clarification |
| Multiple amounts | Telegram clarification |
| Missing account/source | Telegram clarification |
| Missing destination | Telegram clarification |
| Missing category | Telegram clarification |
| Direction unclear | Telegram clarification |
| Status unclear | Telegram clarification |
| CC type unclear | Telegram clarification |
| Duplicate candidate | Telegram clarification or skip exact duplicate |
| Parser confidence low | Review Queue after clarification failure |

## 7. Missing Category From Email

Missing category remains ambiguity.

Policy:
1. Do not infer category aggressively from merchant only.
2. Ask Telegram clarification first.
3. If user answers, attach clean category to normalized candidate.
4. If unresolved, mark quality as needs_category.
5. Missing-category candidate must not enter clean spending category metrics.
6. If future write is allowed, unresolved candidate must go to Review Queue.

## 8. Email-to-Telegram Clarification Bridge

Email ambiguity must use Telegram as the active resolution channel.

Future pending email candidate should include:
- candidate_id
- source_channel
- message_id_hash
- thread_id_hash
- received_at
- from_source_id
- subject_hash
- detected_amount
- detected_date
- detected_merchant
- detected_last4
- detected_account
- detected_direction
- detected_status
- ambiguity_type
- clarification_prompt_id
- clarification_status
- created_at
- expires_at

Generic transaction prompt:

AIRO menemukan email transaksi:

Nominal: Rp{amount}
Tanggal: {date}
Merchant/Tujuan: {merchant_or_unknown}
Akun/Kartu: {account_or_unknown}

Ini mau dicatat sebagai apa?
A. Pengeluaran
B. Transfer internal
C. Pembayaran Credit Card
D. Uang masuk / refund
E. Review manual

Credit card prompt:

AIRO menemukan email Credit Card:

Nominal: Rp{amount}
Merchant: {merchant_or_unknown}
Kartu: {last4_or_unknown}
Status: {status_or_unknown}

Ini transaksi apa?
A. Belanja pakai Credit Card
B. Bayar tagihan Credit Card
C. Refund / reversal
D. Fee / bunga
E. Review manual

Missing category prompt:

AIRO menemukan email transaksi yang kategorinya belum jelas:

Nominal: Rp{amount}
Merchant/Tujuan: {merchant_or_unknown}
Akun/Kartu: {account_or_unknown}

Pilih kategori:
A. Makan
B. Transport
C. Belanja
D. Tagihan
E. Lainnya / Review manual

If Telegram answer is missing, timeout, invalid, or still ambiguous:
- write future candidate to Review Queue
- set clarification_status = unresolved
- set quality_status according to missing fields
- never create clean ledger/domain write

## 9. Duplicate Email vs Telegram Policy

Use multiple dedupe fields:
- amount
- date/time window
- merchant/counterparty
- account/card/e-wallet
- direction
- category candidate
- source channel
- message_id_hash
- telegram_message_ref

Collision handling:
- Exact duplicate: skip duplicate write.
- Probable duplicate: ask Telegram.
- Uncertain duplicate: Review Queue fallback.
- Different direction/account/category: not duplicate until clarified.

Same amount alone is not enough to mark duplicate.

## 10. Review Queue Fallback Policy

Review Queue remains fallback, not first destination.

Use Review Queue only when:
- Telegram clarification fails.
- User answer remains ambiguous.
- Candidate has low parser confidence.
- Critical field remains missing.
- Duplicate detection is uncertain.
- Sender is suspicious but not hard-blocked.
- Manual approval is required.

Security hard-blocked email must not enter Review Queue.

## 11. Sprint 0B Validation Assertions

Sprint 0B is valid only if:
- Email ingestion is still default OFF.
- No Gmail OAuth implementation is added.
- No Gmail trigger is added.
- No full email body is stored.
- OTP/security email is blocked before finance parsing.
- OTP/security content is not sent to Telegram.
- Ambiguous email asks Telegram first.
- Review Queue remains fallback.
- No automatic ledger/domain write from email is implemented in Sprint 0B.
- Sprint 1 is not started until Sprint 0B closeout PASS.

## 12. Next Closeout Inputs

Before Sprint 0B closeout, verify:
- Scope matrix exists.
- Policy design exists.
- OTP/security hard-block policy is clear.
- Telegram bridge prompt flow is documented.
- Missing category from email is documented.
- Duplicate email vs Telegram policy is documented.
- No runtime Gmail/email ingestion implementation exists in this sprint.
