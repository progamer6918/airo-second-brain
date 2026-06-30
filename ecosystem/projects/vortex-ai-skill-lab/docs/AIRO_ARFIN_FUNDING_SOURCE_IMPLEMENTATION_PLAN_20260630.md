---
title: AIRO Arfin Funding Source Implementation Plan
status: PLAN_ONLY_NOT_IMPLEMENTED
date: 2026-06-30
base_head: 7d6c86d378d4d2eddf9bb5ba5e6c348c10eaa34a
generated_at: 2026-06-30T22:47:30+07:00
depends_on:
  - AIRO_ARFIN_NO_TEST_PROOF_20260630.md
  - AIRO_ARFIN_FUNDING_SOURCE_CONFIRMATION_REQUIREMENT_20260630.md
---

# AIRO Arfin Funding Source Implementation Plan

## Status

```text
STATUS=PLAN_ONLY_NOT_IMPLEMENTED
NO_SOURCE_PATCH=YES
NO_DEPLOY=YES
NO_RUNTIME_TEST=YES
FULL_RUNTIME_FUNCTIONING=NOT_CLAIMED
```

## Source-of-truth context

- Arfin no-test proof is complete: source capability and deployment source parity are proven for active deployment version 112.
- Funding-source confirmation requirement is captured as owner-requested and not implemented.
- This plan must not be treated as implementation proof.

## Goal

Add a seamless funding-source confirmation step after category/subcategory resolution and before final approval/write.

Required UX:

```text
Sumber dana transaksi ini dari mana?

A. Saldo akun sekarang / akun terdeteksi
B. Saldo Blu Pocket
C. Saldo Cash umum
D. Akun lain / transfer dari akun lain
E. Manual / lainnya
```

If owner chooses current/detected account, preserve current flow.

If owner chooses another source account, Arfin must create a linked internal transfer for the exact transaction amount before writing the actual transaction.

Every successful final write must include post-write balance/readback in Telegram.

## Implementation gates

### Gate A — Read-only source audit

Mutation scope:

```text
NO_SOURCE_PATCH=YES
NO_DEPLOY=YES
NO_GMAIL_READ=YES
NO_TELEGRAM_SEND=YES
NO_WORKBOOK_EDIT=YES
```

Audit candidate anchors only. Candidate function names from prior static inventory are not final patch anchors until inspected.

Candidate areas:

```text
tryHandlePendingClarificationReply_
reprocessClarifiedTelegramText_
airoSprint7FEmailAnswerMaybeHandleRoute_
airoSprint7FUpdatePendingEmailResolution_
airoSprint7FUpsertPendingEmailCandidate_
airoSprint7HApprovalCommandMaybeHandleRoute_
writeInternalTransferToAccountLedger_
writeRouted_
writeAccountLedgerPrimary_
findAccountLedgerEntryById_
getAccountLedgerRowDetails_
airoBuildFinanceWriteSuccessReply_
```

Audit questions:

1. Where exactly does email pending transaction move from category/subcategory to Review Queue?
2. Where exactly does `/approval` resolve pending Review Queue into write?
3. Is pending state stored in PropertiesService, Review Queue, Email Ingestion Log, or mixed?
4. What idempotency key currently prevents duplicate approval?
5. How to add funding source fields without breaking existing pending candidates?
6. Which existing transfer writer already creates correct linked Account Ledger out/in rows?
7. Which existing readback function can compute post-write account balance?
8. Which success reply builder should be extended?

Gate A PASS condition:
- Exact source anchors identified with line numbers/function names.
- No source mutation.
- No runtime call.
- Clear patch target list.

### Gate B — Patch design

Add/extend pending candidate state with fields:

```text
funding_source_status
funding_source_account
funding_source_answer
spending_account
pre_transfer_required
funding_transfer_linked_txn_id
funding_expense_linked_txn_id
funding_chain_status
funding_idempotency_key
```

Suggested status lifecycle:

```text
category_pending
subcategory_pending
funding_source_pending
approval_pending
approved_write_in_progress
approved_written
approved_failed_review_required
```

Rules:
- Existing candidates without funding fields must default safely to `funding_source_status=not_required_legacy` or `funding_source_account=spending_account`.
- Do not ask funding-source question before category/subcategory is resolved.
- Do not permit approval write while `funding_source_pending`.
- Do not silently infer a different funding source.
- Do not duplicate transfer or expense on repeated `/approval`.

### Gate C — Source patch only

Patch scope should be minimal:

1. Add funding-source question builder.
2. Add funding-source answer normalizer.
3. Add pending candidate field update.
4. Gate `/approval` so it blocks if funding source is unresolved.
5. Add linked transfer-before-expense write path when funding source differs.
6. Extend success reply to include balance/readback.
7. Add idempotency guard around transfer+expense chain.

No deploy in Gate C.

### Gate D — Static validation

Required validation:

```text
BASH_SYNTAX=PASS
JS_PARSE_OR_CLASP_DRY_VALIDATION=PASS
SOURCE_SHA_CHANGED=YES_EXPECTED
FORBIDDEN_SCOPE_CHECK=PASS
NO_DEPLOY=YES
NO_WORKBOOK_EDIT=YES
NO_GMAIL_READ=YES
NO_TELEGRAM_SEND=YES
```

Static assertions:
- Funding-source question exists.
- Approval blocker exists for unresolved funding source.
- Internal transfer path is only called when source account differs.
- Current-account path does not create transfer.
- Success reply includes balance section.
- Duplicate approval idempotency signal exists.

### Gate E — Commit source patch

Allowed only after Gate D PASS.

Commit should include:
- Apps Script source patch.
- Implementation evidence doc.
- No deploy yet unless owner explicitly approves.

### Gate F — Deploy

Deploy only after source commit + owner approval.

Deployment description should be explicit:

```text
AIRO Arfin funding source confirmation + balance readback
```

Post-deploy readback must prove:
- Active version number.
- Deployment source SHA.
- Local source SHA.
- Deployment source parity.

### Gate G — Guarded runtime proof

Runtime proof must be staged:

1. No-write route preview / synthetic pending object if available.
2. Current account path proof.
3. Different funding source path proof.
4. Repeated approval duplicate guard proof.
5. Telegram success reply balance proof.

No Gmail body dumping.
No uncontrolled Telegram spam.
No workbook write except owner-approved bounded test.
No PASS claim without readback rows/balances.

## Acceptance criteria

1. After category/subcategory, Arfin asks funding-source confirmation.
2. Current account choice preserves current normal flow.
3. Different source account creates internal transfer first.
4. Transfer amount equals transaction amount.
5. Actual expense is still written against the detected/spending account.
6. Transfer and expense are linked/auditable.
7. Repeated approval does not duplicate rows.
8. Final Telegram reply shows post-write balances for affected accounts.
9. Failure is fail-closed into Review Queue / manual handling.
10. Runtime PASS is only claimed after guarded readback proof.

## Stop conditions

Stop immediately if:
- Source anchor is ambiguous.
- Existing approval flow cannot be safely traced.
- Account Registry does not expose supported funding accounts.
- Internal transfer writer cannot be proven idempotent.
- Balance readback source is unclear.
- Diff touches dashboard or unrelated domains.
- Remote diverges before push/deploy.
