---
title: AIRO Arfin Gate B Funding Source Patch Design
status: GATE_B_DESIGN_ONLY_NOT_IMPLEMENTED
date: 2026-06-30
base_head: 9e0f9dac6b4792ae0f53a70e0f9fed235c1983f6
generated_at: 2026-06-30T22:54:52+07:00
depends_on:
  - AIRO_ARFIN_FUNDING_SOURCE_CONFIRMATION_REQUIREMENT_20260630.md
  - AIRO_ARFIN_FUNDING_SOURCE_IMPLEMENTATION_PLAN_20260630.md
  - AIRO_ARFIN_GATE_A_SOURCE_AUDIT_20260630.md
---

# AIRO Arfin Gate B Funding Source Patch Design

## Status

```text
STATUS=GATE_B_DESIGN_ONLY_NOT_IMPLEMENTED
NO_SOURCE_PATCH=YES
NO_DEPLOY=YES
NO_RUNTIME_TEST=YES
FULL_RUNTIME_FUNCTIONING=NOT_CLAIMED
```

## Gate A inputs

Gate A read-only source audit returned:

```text
RESULT=PASS_GATE_A_ANCHORS_IDENTIFIED_REQUIREMENT_TERMS_ALREADY_PRESENT_REVIEW_NEEDED
SOURCE_SHA=add9d5a538e48ed8cde6049f0632cbb8318c28e7074428ccc00dae7985353b19
FUNCTION_COUNT_PARSED=693
CANDIDATE_ANCHORS_FOUND=12/12
CRITICAL_MISSING=NONE
```

Gate A warning:
- Existing Blu Pocket / transfer / balance logic already exists.
- Patch must reuse existing registry/normalizer/transfer/readback logic where possible.
- Do not create a duplicate parallel transfer system.

## Business objective

After category/subcategory resolution and before final approval/write, Arfin must ask the owner to confirm funding source.

If funding source equals detected/spending account:
- Continue existing approval/write flow.
- No internal transfer.

If funding source differs from detected/spending account:
- Create linked internal transfer from funding source to spending account for the exact amount.
- Then create the actual expense from spending account.
- Final Telegram success reply must show affected balances.

## Exact patch anchors

### Email category/subcategory answer route

Primary anchor:

```text
airoSprint7FEmailAnswerMaybeHandleRoute_ L22823-L23165
```

Purpose:
- After category/subcategory is resolved, do not immediately move to approval-ready state.
- Instead set pending candidate to `funding_source_pending`.
- Send funding-source question.

### Pending candidate persistence

Primary anchors:

```text
airoSprint7FUpsertPendingEmailCandidate_ L22172-L22191
airoSprint7FUpdatePendingEmailResolution_ L22460-L22522
```

Purpose:
- Persist funding-source state fields.
- Preserve backward compatibility for existing pending candidates.

### Approval route

Primary anchors:

```text
airoSprint7HApprovalCommandMaybeHandleRoute_ L24419-L24570
airoSprint7HApprovalApprove_ caller chain from approval route
```

Purpose:
- Block approval if funding source is unresolved.
- On approval, write funding transfer first when needed, then transaction.
- Preserve existing approval list/detail/reject/fix behavior.

### Internal transfer writer

Primary anchor:

```text
writeInternalTransferToAccountLedger_ L14519-L14604
```

Purpose:
- Reuse existing internal transfer writer.
- Do not create a new transfer writer.

### Main transaction write

Primary anchors:

```text
writeRouted_ L3820-L3849
airoWriteRoutedCore_ via writeRouted_
```

Purpose:
- Preserve existing routed transaction write.
- Funding-source feature should wrap/precede existing write, not rewrite domain routing.

### Balance/readback

Primary anchors:

```text
getAccountLedgerRowDetails_ L1163-L1186
airoBuildFinanceWriteSuccessReply_ L1188-L1318
```

Purpose:
- Reuse existing balance formatting/readback.
- Extend final approval success reply to include post-write saldo for affected accounts.

## New pending candidate fields

Add these fields as optional/backward-compatible fields in pending candidate payload:

```text
funding_source_status
funding_source_account
funding_source_label
funding_source_answer
funding_source_options_json
spending_account
pre_transfer_required
funding_transfer_linked_txn_id
funding_expense_linked_txn_id
funding_chain_status
funding_idempotency_key
funding_transfer_out_entry_id
funding_transfer_in_entry_id
funding_expense_entry_id
funding_balance_readback_json
```

Defaulting rules:
- Existing candidates without these fields must not crash.
- Existing approval-ready candidates may default to `funding_source_status=not_required_legacy`.
- New email candidates after category/subcategory should become `funding_source_pending`.
- `spending_account` should derive from current detected account, e.g. Blu.
- `funding_source_account` is only set after owner answer.

## Lifecycle

Target lifecycle:

```text
email_candidate_detected
category_pending
subcategory_pending
funding_source_pending
approval_pending
approval_write_in_progress
approval_written
approval_failed_review_required
```

Blocking rule:

```text
IF candidate requires funding source confirmation
AND funding_source_status != resolved
THEN /approval must not write
AND Arfin must ask funding-source question again.
```

## Funding-source options design

Question text:

```text
Sumber dana transaksi ini dari mana?

A. Saldo akun sekarang / akun terdeteksi
B. Saldo Blu Pocket
C. Saldo Cash umum
D. Akun lain / transfer dari akun lain
E. Manual / lainnya
```

Design decision:
- Gate C should implement static-safe options first with dynamic registry hook if already easy.
- Do not block implementation on a perfect UI registry system.
- However, account normalization must reuse existing supported account logic and aliases.

Minimum answer mapping:

```text
A -> detected/spending account
B -> Blu Pocket
C -> Cash
D -> manual/ask account
E -> manual/other
```

Fail-closed rules:
- Unsupported account -> do not write.
- Ambiguous account -> ask clarification.
- Source account equals spending account -> no transfer.
- Source account differs -> transfer required.

## Write design

### Current account path

```text
funding_source_account == spending_account
pre_transfer_required=false
```

Action:
1. Call existing approval/write path.
2. Do not call `writeInternalTransferToAccountLedger_`.
3. Extend success reply with spending account balance.

### Different funding source path

```text
funding_source_account != spending_account
pre_transfer_required=true
```

Action:
1. Create internal transfer from funding source to spending account.
2. Then call existing approval/write path for the expense.
3. Store/link transfer out/in entry IDs and expense entry ID.
4. Build success reply with both balances.

Expected example:

```text
Funding source: Blu Pocket
Spending account: Blu
Amount: Rp12.000

Write chain:
1. Blu Pocket -> Blu Rp12.000
2. Blu expense Rp12.000 Food & Drink / Makan Siang
```

## Idempotency design

Idempotency key:

```text
funding_idempotency_key = candidate_id + "|" + amount + "|" + funding_source_account + "|" + spending_account
```

Required behavior:
- Repeated `/approval` must not duplicate transfer.
- Repeated `/approval` must not duplicate expense.
- If transfer succeeded but expense failed, next run must detect partial state and recover/fail closed, not duplicate transfer.
- Store transfer entry IDs and expense entry ID in pending candidate or Review Queue row where existing approval state already lives.

State transitions:

```text
approval_pending
-> approval_write_in_progress
-> transfer_written
-> expense_written
-> approval_written
```

Failure states:

```text
transfer_failed_review_required
expense_failed_after_transfer_review_required
balance_readback_failed_write_succeeded
```

## Reply design

Final success reply must include:

```text
✅ Transaksi berhasil disetujui!

Nominal: Rp12.000
Akun transaksi: Blu
Kategori: Food & Drink / Makan Siang

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

If no transfer:

```text
✅ Transaksi berhasil disetujui!

Nominal: Rp12.000
Akun transaksi: Blu
Kategori: Food & Drink / Makan Siang

Ledger Entry ID:
- Expense: Account Ledger:<row>

Saldo setelah transaksi:
- Blu: Rp...

Readback: PASS.
```

## New helper functions for Gate C

Proposed helper functions:

```text
airoArfinFundingSourceQuestion_
airoArfinFundingSourceOptions_
airoArfinNormalizeFundingSourceAnswer_
airoArfinApplyFundingSourceResolution_
airoArfinCandidateNeedsFundingSource_
airoArfinCandidateFundingSourceResolved_
airoArfinBuildFundingSourcePendingReply_
airoArfinBuildFundingSourceSuccessReadback_
airoArfinBuildFundingSourceApprovalBlockedReply_
airoArfinBuildFundingIdempotencyKey_
airoArfinWriteFundingTransferIfNeeded_
airoArfinReadAffectedAccountBalances_
```

Placement:
- Near Sprint 7F/7H email pending + approval helpers, not inside Dashboard code.
- Keep helpers small and explicit.
- Avoid modifying old dashboard/task functions.

## Minimal Gate C patch scope

Gate C should touch only:

```text
apps-script-prod-v2/AIRO_Finance_Multitab_Final_v1.js
docs/evidence or docs implementation note, if needed
state/active-context.md, if committing evidence
```

Gate C should not touch:
- Dashboard renderer.
- Scheduled refresh.
- Gmail poller scheduling.
- Workbook structure.
- Worker URL.
- Deployment config until Gate F.

## Static validation required after Gate C

Required checks:

```text
JS_PARSE=PASS
SOURCE_SHA_CHANGED=YES_EXPECTED
PATCH_MARKERS_FOUND=YES
FUNDING_SOURCE_QUESTION_FOUND=YES
APPROVAL_BLOCKER_FOUND=YES
INTERNAL_TRANSFER_REUSE_FOUND=YES
BALANCE_REPLY_FOUND=YES
IDEMPOTENCY_GUARD_FOUND=YES
NO_DEPLOY=YES
NO_GMAIL_READ=YES
NO_TELEGRAM_SEND=YES
NO_WORKBOOK_EDIT=YES
```

## Runtime validation later, not Gate B

Gate B does not approve runtime tests.

Runtime proof later must be guarded:
1. No-write/synthetic route preview.
2. Current account flow.
3. Different funding source flow.
4. Repeated approval duplicate guard.
5. Balance reply readback.

## Gate B decision

```text
GATE_B_PATCH_DESIGN=READY_FOR_OWNER_REVIEW
SOURCE_PATCH_ALLOWED_NEXT=ONLY_AFTER_OWNER_APPROVAL
DEPLOY_ALLOWED=NO
RUNTIME_TEST_ALLOWED=NO
```
