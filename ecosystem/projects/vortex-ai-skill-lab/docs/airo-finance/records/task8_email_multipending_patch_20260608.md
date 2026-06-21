# AIRO Finance — Task 8 Email Multi-Pending Clarification Patch

Date: 2026-06-08 WIB  
Status: PASS  
Scope: Task 8 email clarification multi-pending binding fix

## Repo State

Repo HEAD before commit: `3fafcaa`  
Previous Task 8B status: PASS and pushed  
Workbook write performed: no  
Gmail mutated: no  
Telegram production modified: no  
Apps Script deployment performed: no  
Trigger changed: no  
Tab hidden/archived/deleted: no

## Problem

Owner reported a real behavior bug:

- Two email clarification messages could arrive close together in Telegram.
- Owner replied to the clarification.
- Only the latest email candidate was resolved.
- The earlier email candidate remained unresolved.

## Root Cause

The email clarification pending pointer was stored as a single chat-scoped Script Property:

- `AIRO_SPRINT7F_PENDING_EMAIL_<chatId>`

The reply handler loaded only one pending candidate by chat id. Therefore, a newer email clarification for the same chat could overwrite the previous pending candidate.

Review Queue already had enough deterministic identity fields:

- `email_candidate_id`
- `gmail_message_id`
- `gmail_thread_id`
- `duplicate_key`

The issue was pending state and reply routing, not workbook schema.

## Patch Summary

The patch adds deterministic multi-pending handling for email clarification replies.

Implemented behavior:

1. Keep legacy single pending key for backward compatibility.
2. Add per-chat pending list key:
   - `AIRO_SPRINT7F_PENDING_EMAIL_LIST_<chatId>`
3. Upsert pending email candidates by candidate identity.
4. Preserve plain `A/B/C/D/E` behavior when only one pending email exists.
5. When multiple pending emails exist, plain answers are blocked.
6. User is instructed to reply with selector syntax:
   - `1 A`
   - `2 C`
   - `#1 A`
7. Selector routing resolves the intended candidate, not the latest pending candidate.
8. Successful resolution removes only the selected candidate from the pending list.
9. If other pending candidates remain, they stay active.
10. Legacy key is maintained for compatibility and cleaned only when appropriate.

## Source Changes

Tracked source files patched:

- `apps-script-prod-v2/AIRO_Finance_Multitab_Final_v1.js`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs`

The local ignored Apps Script live file was also patched for local parity, but it is intentionally not committed:

- `apps-script-live/AIRO_Finance_Multitab_Final_v1.js`

## Added Helpers

The patch adds helpers including:

- `airoSprint7FEmailPendingListKey_`
- `airoSprint7FEmailPendingCandidateIdentity_`
- `airoSprint7FNormalizePendingEmailCandidate_`
- `airoSprint7FLoadPendingEmailCandidateList_`
- `airoSprint7FSavePendingEmailCandidateList_`
- `airoSprint7FUpsertPendingEmailCandidate_`
- `airoSprint7FRemovePendingEmailCandidate_`
- `airoSprint7FBuildEmailPendingDisambiguationMessage_`
- `airoSprint7FParseEmailPendingSelector_`
- `airoSprint7FSelectPendingEmailCandidate_`

## Self-Test

A self-test function was added:

- `runTask8EmailMultiPendingSelfTestFromEditor()`

Self-test intent:

- create two fake pending candidates
- verify plain `A` is ambiguous when two candidates exist
- verify `1 A` selects candidate 1
- verify `2 C` selects candidate 2
- verify removing candidate 1 leaves candidate 2 active
- cleanup fake Script Properties
- no Telegram send
- no Gmail mutation
- no workbook write

## Verification Evidence

Local evidence files:

- `/tmp/airo_task8_email_multipending_patch_run.txt`
- `/tmp/airo_task8_email_multipending_patch_verify.json`
- `/tmp/airo_task8_email_multipending_patch_evidence_collect.txt`

Verification result:

- `STATIC_VERIFY_STATUS=PASS`
- `patched_files=3`
- `helpers_in_sync=True`
- `deploy_performed=False`
- `gmail_mutation=False`
- `workbook_write=False`
- `commit_performed=False`

## Explicitly Not Done

This commit does not:

- deploy Apps Script
- mutate Gmail
- modify Telegram production
- write workbook values
- install/remove triggers
- run live Telegram smoke
- hide/archive/delete tabs

## Activation Note

This patch is committed to source, but production activation still requires a later deployment step.

Production smoke test should be done only after deployment and should verify:

1. two pending fake/manual email candidates can coexist
2. plain `A` is rejected with a disambiguation prompt
3. `1 A` resolves candidate 1 only
4. candidate 2 remains pending
5. no Gmail mutation occurs
6. no Account Ledger or Finance Events write occurs during clarification staging

## Decision

Task 8 email multi-pending source patch is closed as PASS at repo level.

Deployment and production smoke remain pending as separate later action inside Task 8.
