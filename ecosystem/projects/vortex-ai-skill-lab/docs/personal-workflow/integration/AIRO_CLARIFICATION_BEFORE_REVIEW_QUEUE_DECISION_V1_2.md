# AIRO Clarification Before Review Queue Decision v1.2

Date: 2026-05-21
Project: AIRO Finance Sheet Workflow v1.2
Scope: Telegram ambiguity handling before Review Queue fallback

## Status

DESIGN LOCKED / NOT IMPLEMENTED YET

This decision is an explicit user-approved scope change after Credit Card cycle checkpoint validation.

## User Choices

- 1E: AIRO should ask specifically based on what is missing.
- 2D: User may answer with number, letter, or natural language.
- 3D: After 2 failed clarification attempts, route to Review Queue.
- 4A: Store pending clarification in Review Queue with status `pending_clarification`.
- 5C: AIRO may infer safe category, but must ask account when account is missing.

## Target Behavior

Before writing ambiguous messages directly into Review Queue, AIRO should ask a clarification question in Telegram.

Example:

User:
`beli makan 8rb`

AIRO should infer:
- type: expense
- category: Makan
- amount: Rp8.000
- missing field: account

AIRO should ask:

`Saya tangkap ini pengeluaran kategori Makan Rp8.000. Akun pembayarannya yang mana?`
`A. BCA`
`B. Blu`
`C. Cash`
`D. Credit Card`
`E. Lainnya / tulis manual`

Accepted user replies:
- `A`
- `1`
- `BCA`
- `pakai bca`
- other natural variants if safely parseable

If reply resolves the missing field, AIRO should write to the correct destination tab.

If clarification fails twice, AIRO should route to Review Queue with:
- review_status: `pending_review`
- issue_reason: `clarification_failed`

## Review Queue Statuses

Use Review Queue as storage, but distinguish state:

- `pending_clarification`: waiting for user answer
- `pending_review`: needs manual review after failed clarification or unsafe ambiguity
- `approved` / `edited`: existing manual processing states

## Safety Rules

- Do not guess account.
- Do not guess cash direction if unclear.
- Do not write to ledger until required fields are resolved.
- Do not use live trading, external payment, or credential access.
- Do not touch unrelated tabs while implementing this flow.

## Implementation Direction

Add a small Telegram clarification layer before final Review Queue fallback:

1. Detect missing required fields from parsed finance text.
2. If missing field is resolvable by asking one question, store pending clarification.
3. Send Telegram options.
4. Accept next reply as clarification answer.
5. Resolve final parsed payload and write to destination.
6. If failed twice, convert to Review Queue pending review.

## First Implementation Target

Start with the common case:

`beli makan 8rb`

Required clarification:
- missing account only

Do not implement all ambiguity classes at once.

## Expanded User Decisions — 2026-05-21

After the first runtime test passed, the user approved expanded ambiguity handling with:

- 1E: Map all ambiguity taxonomy, but implementation may be staged safely.
- 2D: For missing amount cases such as `beli makan`, ask nominal and account together.
- 3E: For `cash 8rb`, show all cash interpretation options.
- 4D: Natural replies may be accepted only when account/cash context is already clear.
- 5E: After 2 failed clarification attempts, do not record the transaction; send examples of correct formats.

## Updated Fallback Decision

Previous fallback idea:
- Failed clarification after 2 attempts -> Review Queue.

Updated user decision:
- Failed clarification after 2 attempts -> do not write to ledger and do not write to Review Queue.
- Send a clear example format instead.

## Next Runtime Implementation Batch

Implement next batch in this order:

1. Missing amount + missing account
   - Example: `beli makan`
   - Ask amount and payment account together.
   - Example options:
     - `8000 BCA`
     - `8rb cash`
     - `12000 blu`

2. Cash ambiguous
   - Example: `cash 8rb`
   - Ask:
     - A. Cash masuk
     - B. Cash keluar
     - C. Saldo cash awal / saya pegang cash
     - D. Sisa cash
     - E. Lainnya / tulis manual

3. Direction ambiguous
   - Example: `bca 50rb`
   - Ask:
     - A. Uang keluar
     - B. Uang masuk
     - C. Transfer
     - D. Saldo awal/saldo tercatat
     - E. Lainnya / tulis manual

## Do Not Implement Yet

Do not implement all taxonomy at once. Defer these until the first three classes are stable:

- Transfer incomplete
- Credit Card ambiguous
- Debt ambiguous
- Asset/gold ambiguous
