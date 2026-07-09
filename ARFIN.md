# ARFIN

Canonical runtime contract for Arfin / AIRO Finance transaction intake.

This file is the default standard for Arfin behavior across sessions. If chat memory, old validation logs, or implementation plans conflict with this file, follow this file unless newer ASB evidence explicitly supersedes it.

## Read First

For Arfin work, read this file after `CURRENT.md` and before touching Apps Script, pending state, Telegram flow, Review Queue, Account Ledger, or approval logic.

Do not claim PASS without runtime/readback evidence.

## Telegram UX

Direction prompts may use semantic letters:

- A = Pengeluaran
- B = Pemasukan
- C = Transfer antar akun sendiri
- D = Abaikan

Account prompts must use numeric account options and may also accept account names.

Category prompts must use numeric options.

Subcategory prompts must use numeric options.

`0` means `Other / Review` or safe review fallback.

Legacy letter answers for subcategory may be accepted for backward compatibility, but prompts should not display A/B/C/D/E for category or subcategory.

Admin commands must preempt all pending reply handlers.

These commands must never be swallowed as account, category, subcategory, or direction answers:

- `admin cek pending`
- `admin clear pending clarification`
- `/approval`
- `/admin`

Non-finance chat such as greetings or social text must not create transaction pending state.

## Email Flow

Email provider account is notification / execution provenance, not automatically the funding account.

For outgoing email transactions:

1. infer direction;
2. if direction is confident `pengeluaran`, ask funding account first;
3. after account selection, ask category;
4. after category selection, ask subcategory;
5. save resolved item to Review Queue;
6. write Account Ledger only after approval.

For ambiguous email transactions:

1. ask direction A/B/C/D;
2. if Owner chooses A, continue outgoing account-first flow;
3. if Owner chooses B, continue income flow;
4. if Owner chooses C, continue transfer flow;
5. if Owner chooses D, ignore safely.

Incoming email transactions should ask income source/category and then go to Review Queue before ledger write.

Transfer email transactions must ask source account and destination account, or fall back to Review Queue as `Transfer / Review` without direct ledger write.

## Direction

Classifier must not treat bare boilerplate words as income by themselves:

- `masuk`
- `diterima`
- `received`

Strong income phrases may classify as `pemasukan`, for example:

- `dana masuk`
- `uang masuk`
- `transfer masuk`
- `transfer diterima`
- `penerimaan transfer`
- `incoming transfer`
- `funds received`
- `credited to your account`

Strong outgoing evidence may classify as `pengeluaran`, for example:

- `Transaksimu Pakai blu Berhasil`
- `Pakai blu Berhasil`
- `pembayaran berhasil`
- `transaksi debit berhasil`
- `debit berhasil`
- `QRIS berhasil`
- `purchase`
- `pembelian`
- `bayar`
- `saldo berkurang`

Do not classify every Blu email as outgoing. Use evidence.

Conflicting strong evidence should become `ambigu`.

## Category

Top-level category prompt is canonical numeric:

- `1..N` = category
- `0` = `Other / Review`

Subcategory prompt is canonical numeric:

- `1..N` = subcategory
- `0` = `Other / Review`

Displayed instruction and parser must match. Do not display letter choices while error text asks for numbers.

## Admin

Admin commands always win before pending reply logic.

`admin cek pending` should show active pending items and tell Owner how to reopen one.

When multiple pending email transactions exist, a single transaction number should select that pending item and re-ask the correct missing question.

Owner should not be required to remember compound formats like `2 2`.

Compound shortcuts may remain supported, but must not be mandatory.

`admin clear pending clarification` should either confirm before clearing or perform a bounded clear with readback evidence. It must not write ledger or Review Queue.

## Review Queue

All transaction intake flows write to Review Queue first.

No Account Ledger write is allowed before approval.

Review Queue item must preserve:

- direction;
- amount;
- description;
- source notification/provider;
- funding account selected by Owner;
- execution account when different;
- category;
- subcategory;
- transfer plan when needed;
- email provenance/dedupe metadata when applicable.

## Approval

`/approval` is the only normal path from Review Queue to Account Ledger.

Approval must write ledger rows according to the stored posting plan.

Expense from selected account writes one expense row.

Income to account writes one income row.

Transfer between accounts writes two rows:

1. source account `transfer_out`;
2. destination account `transfer_in`.

Email outgoing where provider/execution account differs from funding account must create bridge transfer rows before expense.

Example contract:

```text
Email provider / execution account: Blu
Owner-selected funding account: Blu Pocket
Type: outgoing expense
```

Approval posting plan:

```text
1. Blu Pocket transfer_out to Blu
2. Blu transfer_in from Blu Pocket
3. Blu expense to selected category/subcategory
```

If funding account equals execution account, approval posts only the expense row.

If funding account differs from execution account, Telegram and Review Queue must clearly explain the planned bridge transfer before approval.

## Ledger

Account Ledger must reflect real balance movement.

For email outgoing through a provider account:

* provider account = execution account;
* Owner-selected account = funding account.

When funding account and execution account differ:

```text
funding_account transfer_out amount -> execution_account
execution_account transfer_in amount <- funding_account
execution_account expense amount -> selected category/subcategory
```

All rows in a multi-row approval should share a common group/source reference and must remain dedupe-safe.

## Tests

Runtime patches that touch Arfin must test these contracts:

* email outgoing account-first;
* ambiguous direction flow;
* Blu outgoing template classification;
* generic received/diterima/masuk not falsely income;
* numeric category prompt;
* numeric subcategory prompt;
* admin command precedence;
* multi-pending single-number selection;
* Review Queue before ledger;
* approval ledger posting plan;
* bridge transfer when funding account differs from execution account;
* no Gmail modification;
* no ledger write before approval.

## Forbidden

Do not:

* use chat memory as final truth over ASB;
* write finance rows before Review Queue approval;
* treat provider as funding account without Owner selection;
* let pending handlers swallow admin commands;
* create transaction pending from social chat;
* display category/subcategory letter menus as the primary UX;
* erase email provenance or dedupe metadata;
* claim PASS without source, deployment, runtime, or readback evidence.
