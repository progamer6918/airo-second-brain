---
title: AIRO Arfin Funding Source Confirmation Requirement
status: NEXT_REQUIREMENT_NOT_IMPLEMENTED
date: 2026-06-30
base_head: b1fefc79dcfdf0e1ecc85169c75d2a4104501b71
generated_at: 2026-06-30T22:44:49+07:00
---

# AIRO Arfin Funding Source Confirmation Requirement

## Status

```text
STATUS=NEXT_REQUIREMENT_NOT_IMPLEMENTED
OWNER_REQUESTED=YES
NO_APPS_SCRIPT_PATCH=YES
NO_DEPLOY=YES
NO_RUNTIME_TEST=YES
```

## Owner intent

After Arfin detects a transaction from email or Telegram and asks for category and subcategory, Arfin should not immediately assume that the spending account balance is the original source of funds.

Before final approval/write, Arfin should ask a simple funding-source confirmation question.

## Current observed UX gap

Current observed flow:

1. Arfin detects a Blu expense.
2. Arfin asks category.
3. Owner answers category.
4. Arfin asks subcategory.
5. Owner answers subcategory.
6. Arfin saves to Review Queue pending approval.
7. Owner sends `/approval`.
8. Arfin approves and writes the transaction.
9. Telegram success reply shows ledger row/readback, but does not show current account balance.

Gap:
- Owner cannot say that the detected spending account was funded by another balance first.
- Success reply does not show post-write balance/readback.

## Required UX

Before final approval, Arfin should ask:

```text
Sumber dana transaksi ini dari mana?

A. Saldo akun sekarang / akun terdeteksi
B. Saldo Blu Pocket
C. Saldo Cash umum
D. Akun lain / transfer dari akun lain
E. Manual / lainnya
```

The options should eventually be dynamic from Account Registry / supported account registry, not hardcoded forever.

## Required behavior

### Case A — current account balance

If owner chooses current detected account balance:

```text
funding_source = detected_account
pre_transfer_required = false
```

Behavior:
- Continue normal approval/write flow.
- No internal transfer should be created.

### Case B/C/D — different funding source

If owner chooses a different funding source account:

```text
funding_source != spending_account
pre_transfer_required = true
```

Behavior:
1. Create internal transfer from funding source account to spending/detected account for the exact transaction amount.
2. Then create the actual expense from the spending/detected account.
3. Link the internal transfer and actual transaction so readback/audit can explain the chain.

Example:

```text
Original transaction:
- Rp12.000
- Spending account: Blu
- Category: Food & Drink / Makan Siang

Owner chooses:
- Funding source: Blu Pocket

Expected write model:
1. Internal transfer: Blu Pocket -> Blu, Rp12.000
2. Expense: Blu, Rp12.000, Food & Drink / Makan Siang
```

## Telegram success reply requirement

Every successful final transaction write should show balance/readback in Telegram.

Minimum reply target:

```text
✅ Transaksi berhasil disetujui!

Nominal: Rp12.000
Akun transaksi: Blu
Kategori: Food & Drink / Makan Siang

Jika ada funding transfer:
Transfer internal: Blu Pocket -> Blu Rp12.000

Ledger Entry ID:
- Transfer out: Account Ledger:<row>
- Transfer in: Account Ledger:<row>
- Expense: Account Ledger:<row>

Saldo setelah transaksi:
- Blu Pocket: Rp...
- Blu: Rp...

Readback: PASS.
```

If no transfer exists:

```text
Saldo setelah transaksi:
- Blu: Rp...
```

## Guardrails

- Do not bypass category/subcategory confirmation.
- Do not bypass approval.
- Do not infer funding source silently if ambiguous.
- Fail closed if funding source account is unclear or unsupported.
- Do not create internal transfer if owner chose current detected account.
- Do not create duplicate transfer on repeated `/approval`.
- Use idempotency key / linked transaction reference for transfer + expense chain.
- Do not claim runtime PASS until guarded runtime proof exists.

## Implementation boundary

This document records requirement only.

```text
NO_SOURCE_PATCH=YES
NO_DEPLOY=YES
NO_GMAIL_READ=YES
NO_TELEGRAM_SEND=YES
NO_WORKBOOK_EDIT=YES
```

## Acceptance criteria draft

1. Arfin asks funding-source confirmation after category/subcategory and before final approval.
2. Choosing current account preserves existing normal flow.
3. Choosing another funding account creates internal transfer first, then transaction.
4. Internal transfer amount equals transaction amount.
5. Telegram final success reply includes post-write balance/readback.
6. Repeated approval does not duplicate transfer or expense.
7. All writes are linked and auditable.
8. Runtime proof must be owner-approved and guarded.
