# AIRO FINANCE — FINAL LIVING PRD v2.1.3

Execution Contract after Architecture Freeze Audit

PRD Version      : 2.1.3
Status           : CANONICAL EXECUTION CONTRACT — READY FOR OWNER-APPROVED REPO REPLACEMENT
Last verified    : 2026-06-03 19:40 WIB
Repo baseline    : bd6815e
Feature baseline : a4fd0ac — Phase 6H-G3 category registry fix
Apps Script      : apps-script-live @241
Deployment ID    : AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA
Worker           : airo-finance-telegram-proxy → env.APPS_SCRIPT_URL unchanged
Gmail trigger    : NOT INSTALLED
Email ingestion  : DISABLED
Alert Engine     : SAFE MODE, trigger installed, proactive send OFF
E-path layer 1   : LIVE PASS @241
Audit basis      : Architecture Freeze Audit Pack 1, Pack 1B, Pack 2

---

## 0. Status Claim

This PRD is execution-ready after repo, active source, deployment, workbook schema, and dashboard contract audit.

Allowed claim:

```text
No known architecture-level blocker remains undocumented after Architecture Freeze Audit.
Antigravity may execute in task-contract mode with no roadmap discovery expected.
```

Forbidden claim:

```text
zero bug
zero mistake
zero implementation issue
project already ready-to-use
```

This document removes known architecture ambiguity. It does not remove the need for task-level tests, deployment verification, Telegram live smoke, and workbook readback.

---

## 1. Purpose

This document is the execution contract for completing AIRO Personal Finance Command Center.

Antigravity must not use this document as passive documentation. It must execute tasks in order, respect stop gates, avoid speculative redesign, and report evidence after every task.

A task is done only when all layers align:

```text
repo source
→ Apps Script editor synced
→ Apps Script deployed using existing deployment ID
→ Cloudflare Worker target unchanged or explicitly approved
→ Telegram live behavior matches expected
→ Google Sheet write/readback verified
→ PRD/current-state evidence updated
→ committed and pushed
```

Feature existence in repo is not sufficient.

---

## 2. Non-Negotiable Architecture

Do not redesign the system unless the owner explicitly approves a breaking change.

### 2.1 Platform

Google Spreadsheet remains the operational workspace and source-of-truth for current v1.

No web app, localhost backend, SaaS migration, or external database migration is in current scope.

### 2.2 Interface

Telegram is the primary owner-facing interface for:

```text
manual transaction input
cash transaction input
clarification replies
admin commands
approval actions
Review Queue actions
alert acknowledgement
email clarification replies
```

Email never replaces Telegram manual input.

### 2.3 Runtime

```text
Google Apps Script = main backend runtime
Cloudflare Worker = Telegram proxy / async_ack bridge
Gmail = optional passive input only
GitHub repo = canonical docs and source control
```

### 2.4 Data Layers

```text
Account Ledger = wallet/account movement only
Finance Events = central event index, not balance ledger
Credit Card = credit card domain truth
Hutang = debt/liability/receivable domain truth
Aset = asset/gold/domain truth
Cicilan Rumah = home installment domain truth
Review Queue = unresolved exception fallback + email staging gate
Audit Log = script/admin/reconciliation trail
Dashboard = intelligence cockpit, not source-of-truth
Monthly Review = legacy/partial until rewired
Transactions = visible but forbidden as v1 master
Cash Ledger = hidden legacy/transitional
```

### 2.5 Hard Forbidden Actions

Never do these without explicit owner approval:

```text
store full email body
forward OTP/security email to Telegram or any sheet tab
mutate Gmail: archive/delete/read-unread/label change
write Account Ledger from email
install Gmail scheduled trigger
enable proactive Alert Engine send
change Worker APPS_SCRIPT_URL
change .clasp.json projectId
create new Apps Script deployment ID
delete workbook tabs
activate noreply@tokopedia.com parser
run clasp run
run clasp apis
inspect credential/token files
```

Deployment must update the existing Apps Script deployment ID in-place.

---

## 3. Source Truth Hierarchy

Execution must follow this hierarchy:

```text
1. Live runtime proof
2. Google Sheet actual schema/formulas
3. Apps Script active source
4. Git repo and sprint records
5. Living PRD
6. Chat summaries
```

When conflict exists, live reality wins and the PRD/current-state docs must be updated.

---

## 4. Input Source Contract

Project completion is not email-only.

### 4.1 Telegram Direct Input — Primary

Telegram manual input is the main daily-use path.

Required final regression types:

```text
cash keluar 15000 parkir
bca keluar 25000 kopi
blu masuk 100000 refund
transfer 50000 dari bca ke blu
cc 75000 tokopedia skincare
bayar cc 500000 dari blu
bayar hutang 100000 ke budi dari bca
beli emas 1 gram dari bca
bayar cicilan rumah 3500000 dari bca
```

Cash transactions usually have no email source. Cash is Telegram/manual first-class input.

Allowed cash aliases if parser supports them:

```text
Cash Umum keluar 15000 parkir
Cash Bensin keluar 15000 bensin
```

### 4.2 Email Notification Input — Passive Auxiliary

Current approved sender:

```text
receipts@blubybcadigital.id
```

Candidate/future sender, not active:

```text
noreply@tokopedia.com
```

Do not open Tokopedia scope unless owner explicitly approves and parser validation exists.

Target email flow:

```text
Gmail candidate detected read-only
→ OTP/security hard-block
→ metadata-only parsing
→ Telegram clarification
→ category/subcategory resolution
→ Review Queue staging
→ owner-approved controlled Account Ledger write
→ Finance Events co-emission
→ Audit Log
→ readback verification
```

Email must never bypass Telegram clarification in current v1.

### 4.3 Review Queue Refinement for Email

General doctrine remains:

```text
Review Queue = fallback after clarification fails
```

Narrow v2.1.3 refinement:

```text
For email ingestion only, Review Queue is also an owner-approved staging/audit gate before controlled Account Ledger write.
```

This does not change normal Telegram ambiguity behavior.

---

## 5. Current Verified Baseline

```text
Repo baseline       : bd6815e
Feature commit      : a4fd0ac
Apps Script project : apps-script-live
Apps Script version : @241
Deployment ID       : AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA
Worker              : airo-finance-telegram-proxy
Worker target       : env.APPS_SCRIPT_URL
Gmail trigger       : NOT INSTALLED
Email ingestion     : DISABLED
Alert Engine        : SAFE MODE
E-path layer 1      : LIVE PASS
Rollback target     : @237 on same deployment ID
```

Known repo issue:

```text
Working tree has untracked files from prior local work.
Antigravity must inspect and classify them before committing PRD or feature work.
```

---

## 6. Architecture Freeze Audit Summary

### 6.1 Pack 1 — Repo and Docs

Result:

```text
PASS with stale-doc finding
```

Key finding:

```text
AIRO_FINANCE_CURRENT_STATE.md is stale and still references old Sprint 2 / old deployment context.
```

Consequence:

```text
Task 0B must refresh CURRENT_STATE.md before feature work.
```

### 6.2 Pack 1B — Active Source

Result:

```text
PASS
```

Active source confirms these runner/function areas exist:

```text
runSprint7FSendOneClarificationAndLogPendingFromEditor
runSprint7GManualWritePilotFromEditor
runSprint7GReviewQueueReadbackVerifierFromEditor
runSprint7HInstallPollerTriggerFromEditor
runSprint7HUninstallPollerTriggerFromEditor
runSprint7HPollerTriggerStatusFromEditor
airoSprint7HScheduledGmailPoller_
airoSprint7HResolveToReviewQueueFallback_
airoSprint7CategoryContractGetRegistry_
airoSprint7FEmailAnswerMaybeHandleRoute_
airoSprint6DashboardV2Build_
airoSprint6DashboardV2Readback_
```

Worker still uses:

```text
env.APPS_SCRIPT_URL
async_ack
```

### 6.3 Pack 2 — Workbook and Dashboard

Result:

```text
PASS with findings
```

Important findings:

```text
Transactions is visible but forbidden as v1 master.
Cash Ledger is hidden and legacy/transitional.
Monthly Review still reads Transactions.
Dashboard official formula scan uses Account Ledger, Finance Events, and Review Queue.
Dashboard B2 is script-written sync timestamp.
Dashboard G2 is selected month.
M2/M3/M4 derive selected period from G2.
G2 validation currently only lists April/May/June 2026.
Review Queue lacks email-specific identity columns.
```

---

## 7. Actual Workbook Schema Contract

Antigravity must use actual headers. Do not assume ideal headers.

### 7.1 Account Ledger

Actual headers:

```text
entry_id
date
account
amount_in
amount_out
balance
type
category
description
raw_text
source_tab
linked_txn_id
notes
```

Rules:

```text
Current canonical linkage = linked_txn_id.
Do not require event_ref in current v1.
Allowed additive columns only with explicit task scope.
Do not reorder.
Do not rename.
Use header-based mapping.
```

### 7.2 Finance Events

Actual headers:

```text
event_id
event_ts
event_type
event_source
source_tab
source_row
linked_txn_id
account
category
amount
direction
status
reason
payload_json
notes
```

Rules:

```text
Finance Events is event index, not balance ledger.
linked_txn_id links to Account Ledger/domain context.
Extra fields such as subcategory, quality_status, reconciliation_status may live in payload_json unless additive columns are approved.
Do not force schema rewrite.
```

### 7.3 Review Queue

Actual headers:

```text
queue_id
created_at
source
raw_text
parsed_type
parsed_category
parsed_subcategory
parsed_amount
parsed_currency
parsed_account
parser_confidence
issue_reason
suggested_fix
review_status
reviewed_at
approved_transaction_id
local_db_table
local_db_rowid
sync_hash
notes
```

Email staging needs additional deterministic fields.

Task 3A must verify actual headers first, then add only missing columns at the end:

```text
email_candidate_id
gmail_message_id
gmail_thread_id
email_provider
email_log_ref
duplicate_key
write_policy
write_status
linked_event_id
linked_account_ledger_entry_id
```

Rules:

```text
Additive-only.
Header-based mapping only.
No rename.
No reorder.
Backfill existing rows blank.
No Account Ledger write during schema extension.
No Finance Events write during schema extension.
No Gmail mutation.
```

### 7.4 Email Ingestion Log

Actual headers:

```text
created_at
candidate_id
message_id
thread_id
sender
provider
received_at
subject_hash
display_amount
inferred_direction
display_time
clarification_question_type
parse_status
candidate_type
clarification_needed
clarification_status
resolved_answer
resolved_label
resolved_at
telegram_chat_id
telegram_sent
write_allowed
write_performed
finance_event_ref
notes
```

Rules:

```text
This is the source for email candidate identity.
Review Queue staging must link back to this log.
Do not store full email body.
Do not mutate Gmail.
```

---

## 8. Dashboard and Monthly Review Data Contract

### 8.1 Official Dashboard

Actual official dashboard:

```text
🏠 Dashboard
visible
36 rows
13 columns
```

Dashboard row 1 headers are blank. This is expected because Dashboard is visual, not a table.

### 8.2 Topbar Contract

```text
B2 = global last dashboard build/sync timestamp, script-written, no formula
G2 = selected month dropdown, script-written/validated, no formula
M2 = selected month helper derived from G2
M3 = start date of selected month
M4 = end date of selected month
```

Current G2 validation:

```text
📅 April 2026
📅 Mei 2026
📅 Juni 2026
```

Task 7 must validate or expand month selector logic so it does not become permanently hardcoded to Apr/May/Jun 2026.

### 8.3 Dashboard Source Contract

Pack 2 formula scan found official Dashboard references to:

```text
Account Ledger
Finance Events
Review Queue
```

No official Dashboard formula dependency on `Transactions` or `Cash Ledger` was found in Pack 2 sample.

Rules:

```text
Dashboard must not use Transactions as current v1 source.
Dashboard must not use Cash Ledger as source-of-truth.
Dashboard wallet/cashflow uses Account Ledger.
Dashboard spending/category analytics uses Finance Events.
Dashboard pending/action items may use Review Queue.
Dashboard operational trust may use Audit Log, Finance Events, Review Queue, and reconciliation output.
```

### 8.4 Action Required Contract

Current Action Required cells are script-written values, not guaranteed pure formulas.

Required behavior:

```text
Global urgent issues remain visible regardless of G2.
Selected-month issues follow G2 via M2/M3/M4.
Review Queue pending, partial write, dirty data, runtime mismatch, and Gmail polling error are global urgent issues.
Missing category/spending anomaly/cashflow issue may be selected-month scoped.
```

Task 7 must verify this with dashboard readback after email staging/write tasks.

### 8.5 Smart Insight Contract

Required behavior:

```text
Smart Insight is mostly selected-month scoped through G2/M2/M3/M4.
Critical global data-quality warnings may still appear even when viewing another month.
Smart Insight must not present clean confidence if Data Status is Warning/Dirty.
```

### 8.6 Monthly Review Contract

Actual finding:

```text
📅 Monthly Review is visible and still reads 💸 Transactions in multiple formulas.
```

Status:

```text
legacy/partial
not trusted as current v1 source-of-truth
```

Task 7 or Task 8 must decide one of:

```text
A. Rewire Monthly Review to Account Ledger + Finance Events.
B. Hide/archive Monthly Review until future Transactions scope.
```

Do not treat Monthly Review as official trust source until one option is completed.

---

## 9. Transactions and Cash Ledger Policy

### 9.1 Transactions

Actual state:

```text
💸 Transactions = visible
```

Policy:

```text
reserved/future
for future bank mutation/PDF/statement scope only
forbidden as v1 master
no current task may write to Transactions
```

Do not hide in Task 0. Task 0 is state lock and refresh only.

Hide/archive only in Task 8 after dependency audit and owner approval.

### 9.2 Cash Ledger

Actual state:

```text
💵 Cash Ledger = hidden
```

Policy:

```text
legacy/transitional
cutover-forward
do not require historical migration
archive/delete only after dependency audit
```

Task 8 must verify:

```text
Dashboard no longer reads Cash Ledger.
Monthly Review no longer reads Cash Ledger or is hidden/rewired.
Apps Script active compatibility references are safe or retired.
```

---

## 10. Execution Order

Execute strictly in this order:

```text
Task 0A — Runtime State Lock
Task 0B — CURRENT_STATE.md Refresh
Task 0C — Workbook Schema Contract Verification
Task 0D — Dashboard + Monthly Review Contract Verification
Task 1  — E-path subcategory flow completion
Task 2  — Amount pointer fix
Task 3A — Review Queue email schema extension
Task 3B — Email → Telegram → Review Queue staging
Task 4A — Polling readiness + run-once verification, no trigger install
Task 4B — Scheduled trigger install, owner approval required
Task 5  — Controlled Account Ledger write pilot from email, owner approval required
Task 6  — Final Telegram manual regression matrix
Task 7  — Dashboard + Finance Events + Reconciliation integration smoke
Task 8  — Workbook and repo cleanup audit
Task 9  — Final PRD closeout and ready-to-use declaration
Task 10 — Optional proactive Alert Engine activation
```

No skipped task. No skipped stop gate.

---

## 11. Task 0A — Runtime State Lock

Objective:

```text
Prevent repo/editor/deployment/Worker/Telegram mismatch.
```

Required checks:

```text
git fetch origin main
git status --short --branch
git log -8 --oneline
apps-script-live clasp deployments
verify @241 or newer on known deployment ID
verify Worker uses env.APPS_SCRIPT_URL
verify Telegram E-path still PASS
```

Live smoke:

```text
Apps Script editor:
runSprint7FSendOneClarificationAndLogPendingFromEditor

Telegram:
E

Expected:
numbered category registry appears, including Personal Care and 0. Other/Review.
```

Stop gate:

```text
If runtime mismatch exists, fix runtime alignment before product patching.
```

---

## 12. Task 0B — CURRENT_STATE.md Refresh

Objective:

```text
Replace stale current-state baseline before feature work.
```

`docs/AIRO_FINANCE_CURRENT_STATE.md` must record:

```text
Repo baseline: bd6815e or newer
Feature baseline: a4fd0ac
Apps Script live: @241 or newer
Deployment ID
Worker target status
Gmail trigger status
Email ingestion status
Alert Engine status
Workbook schema summary
Dashboard contract summary
Current task order
Known risks
Next task: Task 1 after Task 0 complete
```

Acceptance criteria:

```text
CURRENT_STATE.md no longer references old Sprint 2 operating mode as current.
Old deployment references are historical only or removed from current state.
Antigravity can read CURRENT_STATE.md without being routed to obsolete work.
```

---

## 13. Task 0C — Workbook Schema Contract Verification

Objective:

```text
Confirm actual workbook schema still matches PRD v2.1.3 before feature work.
```

Required checks:

```text
Account Ledger headers
Finance Events headers
Review Queue headers
Email Ingestion Log headers
Transactions visibility
Cash Ledger visibility
Monthly Review visibility
Dashboard sheet existence
```

Acceptance criteria:

```text
Actual schema matches Section 7 or differences are recorded before patching.
Review Queue missing email extension fields is expected until Task 3A.
No product data mutation.
No Gmail mutation.
No finance write.
```

---

## 14. Task 0D — Dashboard + Monthly Review Contract Verification

Objective:

```text
Confirm dashboard/monthly review data dependencies before feature work.
```

Required checks:

```text
Dashboard B2/G2/M2/M3/M4
G2 validation list
Action Required cells
Smart Insight cells
Dashboard formulas referencing Account Ledger / Finance Events / Review Queue
Dashboard formulas referencing Transactions / Cash Ledger
Monthly Review formulas referencing Transactions
```

Acceptance criteria:

```text
Dashboard official source contract documented.
Monthly Review legacy/partial status documented.
No dashboard patch unless Task 7 scope is active.
```

---

## 15. Task 1 — E-path Subcategory Flow Completion

Status:

```text
Layer 1 PASS, layer 2 unproven live.
```

Steps:

```text
Telegram:
admin clear clarification

Apps Script editor:
runSprint7FSendOneClarificationAndLogPendingFromEditor

Telegram:
E

Expected:
full numbered category registry with 0. Other/Review

Telegram:
select displayed number for Food & Drink

Expected:
Food & Drink subcategory prompt

Telegram:
select Kopi

Expected:
Food & Drink / Kopi resolved, no Account Ledger write
```

Repeat:

```text
Personal Care by displayed number
Personal Care by exact text
personal care lowercase
invalid number 999
0. Other/Review
```

Acceptance criteria:

```text
E opens full registry.
Valid number resolves canonical category.
Valid text resolves case-insensitively.
Subcategory prompt appears when category has subcategories.
Invalid number keeps pending active.
0 routes safely to Review Queue/manual review path.
No Account Ledger write.
No clean financial Finance Events write.
Gmail not mutated.
```

---

## 16. Task 2 — Amount Pointer Fix

Problem:

```text
Email clarification path may show Nominal belum terbaca even when poller extracted valid amount.
```

Likely areas:

```text
pending candidate builder
save/load pending email candidate
email route answer handler
confirmation builder
Review Queue builder
amount display helper
```

Requirement:

```text
detected/display amount persists from email candidate
→ pending object
→ category/subcategory reply
→ Review Queue staging
→ controlled write pilot
```

Acceptance criteria:

```text
Clarification message shows correct amount.
Route preview shows correct amount.
Review Queue staging row shows correct amount.
No fallback to Nominal belum terbaca when parser extracted amount.
No Gmail mutation.
No finance write outside approved scope.
```

---

## 17. Task 3A — Review Queue Email Schema Extension

Objective:

```text
Prepare Review Queue for deterministic email staging and idempotency.
```

Procedure:

```text
Audit actual Review Queue headers.
Add only missing email extension columns at end.
Update helper mapping to header-based reads/writes.
Backfill existing rows blank.
```

Target extension fields:

```text
email_candidate_id
gmail_message_id
gmail_thread_id
email_provider
email_log_ref
duplicate_key
write_policy
write_status
linked_event_id
linked_account_ledger_entry_id
```

Acceptance criteria:

```text
Columns added only if missing.
No existing columns renamed.
No existing columns reordered.
Existing rows preserved.
No Account Ledger write.
No Finance Events write.
No Gmail mutation.
Readback verifies headers.
```

---

## 18. Task 3B — Email → Telegram → Review Queue Staging

Objective:

```text
Prove full controlled staging flow without ledger write.
```

Flow:

```text
Gmail candidate
→ read-only detection
→ Telegram clarification
→ category/subcategory answer
→ Review Queue staging
→ admin readback
```

Candidate availability rule:

```text
If inbox has no candidate, that is not product failure.
Use safe transient/manual candidate function or ask owner for fresh approved Blu email.
```

Allowed functions:

```text
runSprint7FManualDryRunPollerFromEditor
runSprint7FBManualDryRunPollerWithTransientBodyFromEditor
runSprint7FSendOneClarificationAndLogPendingFromEditor
runSprint7GReviewQueueReadbackVerifierFromEditor
```

Acceptance criteria:

```text
Telegram clarification arrives.
Amount correct.
Category/subcategory accepted.
Review Queue row created/updated with email identity.
Duplicate candidate does not duplicate row.
No Account Ledger write.
No clean financial Finance Events write unless explicitly staging-only.
Gmail not mutated.
Admin readback finds row.
```

---

## 19. Task 4A — Polling Readiness, No Trigger Install

Objective:

```text
Verify polling engine guardrails without scheduled trigger.
```

Acceptance criteria:

```text
kill switch exists
active window 07:00–22:00 WIB enforced
max candidates cap exists
max Telegram clarification cap exists
sender allowlist enforced
only receipts@blubybcadigital.id active
OTP/security hard-block before parsing
dedupe confirmed
run-once PASS
trigger count = 0
no Gmail mutation
no finance write
Telegram status command works
```

Stop gate:

```text
Task 4B requires explicit owner approval.
```

---

## 20. Task 4B — Scheduled Trigger Install

Owner approval phrase:

```text
APPROVE AIRO Task 4B Gmail scheduled trigger install.
Read-only. No finance write. Kill switch confirmed active.
```

Allowed functions:

```text
runSprint7HInstallPollerTriggerFromEditor
runSprint7HPollerTriggerStatusFromEditor
runSprint7HUninstallPollerTriggerFromEditor
```

Acceptance criteria:

```text
Owner approval recorded.
Trigger installed via approved function.
Trigger status confirms active trigger.
Kill switch disables activity.
First scheduled run has no Gmail mutation.
First scheduled run has no finance write.
```

---

## 21. Task 5 — Controlled Email-to-Account-Ledger Write Pilot

Status:

```text
Not started.
Mandatory for owner-defined 100% completion.
```

Owner approval phrase:

```text
APPROVE AIRO Task 5 controlled email-to-Account-Ledger write pilot.
Scope: one approved Review Queue candidate only.
Manual trigger only.
No Gmail mutation.
No scheduled auto-write.
Require Account Ledger, Finance Events, Review Queue, Audit Log, and Dashboard readback.
Stop on first unexpected write.
```

Preconditions:

```text
Task 1 PASS
Task 2 PASS
Task 3A PASS
Task 3B PASS
Task 4A PASS
owner approval received
```

Allowed function:

```text
runSprint7GManualWritePilotFromEditor
```

Acceptance criteria:

```text
Exactly one Account Ledger row per approved candidate.
Amount correct.
Account mapping correct.
Category/subcategory correct.
Finance Events row exists.
Finance Events linked via linked_txn_id or equivalent.
Review Queue status changes to committed/linked.
Audit Log records lifecycle.
Second run creates no duplicate.
Dashboard does not duplicate count.
Gmail not mutated.
Admin readback finds rows.
```

---

## 22. Task 6 — Telegram Manual Regression Matrix

Objective:

```text
Prove email work did not break primary Telegram manual input.
```

Run with unique smoke IDs.

Required tests:

```text
cash keluar 15000 parkir SMK_T6_CASH_EXP
bca keluar 25000 kopi SMK_T6_BCA_EXP
blu masuk 100000 refund SMK_T6_BLU_IN
transfer 50000 dari bca ke blu SMK_T6_TRANSFER
cc 75000 tokopedia skincare SMK_T6_CC_PURCHASE
bayar cc 500000 dari blu SMK_T6_CC_PAYMENT
bayar hutang 100000 ke budi dari bca SMK_T6_HUTANG
beli emas 1 gram dari bca SMK_T6_ASET
bayar cicilan rumah 3500000 dari bca SMK_T6_CICILAN
admin find smoke all SMK_T6
```

Acceptance criteria:

```text
Cash expense uses cash, not BCA.
Wallet expense writes Account Ledger.
Wallet income writes Account Ledger.
Transfer creates exactly two linked Account Ledger rows.
CC purchase writes Credit Card + Finance Events, no Account Ledger outflow.
CC payment writes Account Ledger outflow + CC domain update.
Hutang payment writes wallet movement + Hutang update.
Asset purchase writes wallet movement + Aset update.
Cicilan payment writes wallet movement + Cicilan update.
Finance Events exists for resolved post-cutover events.
No duplicate writes.
Admin readback finds smoke rows.
```

---

## 23. Task 7 — Dashboard, Finance Events, Reconciliation Integration Smoke

Objective:

```text
Prove dashboard and data-quality system reflect real live state after manual and email flows.
```

Required checks:

```text
Dashboard B2 sync timestamp
G2 month selector
M2/M3/M4 period helpers
Action Required global + selected-month issues
Smart Insight selected-month + critical global warnings
Data Status traceability
Review Queue pending visibility
Finance Events linkage
Account Ledger linkage
Monthly Review legacy/rewire decision
```

Acceptance criteria:

```text
Dashboard does not look clean while unresolved issues exist.
Dashboard source remains Account Ledger + Finance Events + Review Queue.
Dashboard does not depend on Transactions as v1 source.
Dashboard does not depend on Cash Ledger as source-of-truth.
G2 period selector is validated or expanded beyond stale hardcoding.
Monthly Review is rewired or explicitly hidden/deferred.
No formula error cells introduced.
```

---

## 24. Task 8 — Workbook and Repo Cleanup Audit

Rule:

```text
No blind delete.
```

Cleanup flow:

```text
inventory all tabs
classify active / hidden backend / legacy / future / candidate delete
grep Apps Script references
grep Dashboard formulas
backup spreadsheet
hide/archive first
owner reviews deletion list
delete only after owner approval
dashboard smoke + admin readback
```

Classification:

```text
Active visible:
Dashboard
Finance Events
Account Ledger
Credit Card
Cicilan Rumah
Hutang
Aset
Review Queue
Settings

Conditional:
Monthly Review — keep only if rewired; otherwise hide/archive candidate

Hidden backend:
_AIRO_Ops_Center
_AIRO_Email_Ingestion_Log
_AIRO_Audit_Log
_AIRO_Dedupe_Log
Sync Log

Legacy:
Cash Ledger
old dashboard backups
dashboard copy tabs
audit temp sheet

Future:
Transactions
```

Acceptance criteria:

```text
No active Apps Script reference to deleted tab.
No dashboard formula reference to deleted tab.
No admin readback broken.
Backup exists.
Owner approved deletion list.
Dashboard smoke PASS after cleanup.
```

---

## 25. Task 9 — Final Closeout

Required updates:

```text
docs/AIRO_FINANCE_PRD_LIVING.md
docs/AIRO_FINANCE_CURRENT_STATE.md
docs/airo-finance/records/<final closeout record>
```

Required final output:

```text
Repo HEAD
Apps Script version
Deployment ID
Worker target status
Gmail trigger status
Email ingestion status
Alert Engine status
Manual Telegram smoke result
Email flow smoke result
Account Ledger readback
Finance Events readback
Review Queue readback
Dashboard Data Status result
Monthly Review decision
Known deferred debt
Rollback path
Commit hash
```

---

## 25B. Credit Card Pending Pocket Numbered Settlement Workflow

1. `cek tagihan pending cc` adalah command read-only untuk menampilkan item Credit Card yang `status_pocket_blu` masih pending/belum.
2. Output harus berupa daftar bernomor 1..N.
3. Setiap item menampilkan minimal:
   * nomor item,
   * `description`,
   * amount,
   * optional: date / merchant_app / billing_cycle_id kalau ringkas.
4. Total amount pending ditampilkan di bawah list.
5. Nomor pada command `cc sudah <nomor>` bukan nomor row spreadsheet.
6. Nomor tersebut adalah nomor item dari daftar pending CC terakhir yang dikirim AIRO ke chat owner.
7. AIRO harus menyimpan mapping sementara:
   * nomor item -> `cc_entry_id`
   * amount
   * description
   * billing_cycle_id
   * timestamp list dibuat
8. Mapping harus punya TTL pendek, misalnya 15 menit atau sampai list pending CC berikutnya dibuat.
9. Jika owner mengetik `cc sudah <nomor>` tanpa mapping aktif, AIRO harus menolak dan meminta owner menjalankan `cek tagihan pending cc` lagi.
10. Jika nomor tidak valid / out of range, AIRO harus menolak tanpa write.
11. Jika item sudah berubah status menjadi `Sudah`, AIRO harus idempotent: jangan double write ledger.
12. Settlement command `cc sudah <nomor>` harus Account-Ledger-first:
    * resolve nomor ke `cc_entry_id`,
    * baca ulang row Credit Card live,
    * pastikan status masih pending,
    * tulis Account Ledger settlement/payment entry lebih dulu,
    * verify ledger write,
    * hanya jika verified, update row Credit Card:
      * `status_pocket_blu = ✅ Sudah`,
      * `transferred_at = timestamp`,
      * `linked_txn_id = Account Ledger reference`,
      * append notes jika perlu.
13. Jika Account Ledger write gagal, status Credit Card tidak boleh berubah.
14. Setelah settlement sukses, AIRO harus refresh Credit Card cycle/header agar `PERIODE BERJALAN / UNBILLED` dan total pending tidak stale.
15. Manual edit langsung di sheet dari `Belum` ke `Sudah` tetap dianggap owner override, tapi tidak ledger-safe kalau tidak punya `linked_txn_id`. PRD harus mewajibkan audit/flag:
    `CC_STATUS_SUDAH_WITHOUT_LEDGER_LINK`.

### Command Examples
```text
cek tagihan pending cc
cc sudah 1
cc sudah 2
```

### Expected Output Example
```text
💳 Pending Pocket Blu CC

1. Nasgor ShopeeFood — Rp35.000
2. UPS Wifi Shopee — Rp81.000

Total belum disiapkan ke Blu: Rp116.000

Balas:
cc sudah <nomor>
```

### Explicit Non-Goals
* Jangan mengubah `cc_purchase` agar menulis Account Ledger. (CC purchase tetap domain-only di tab Credit Card).
* Jangan menganggap nomor sebagai spreadsheet row number.
* Jangan mengizinankan status berubah ke Sudah tanpa ledger verified.
* Jangan live test Telegram selama WebApp masih 403.

---
## 26. Task 10 — Optional Proactive Alert Activation

Status:

```text
Optional, post-completion.
Not required for owner-defined email-to-ledger completion.
```

Requires separate approval.

Allowed first activation:

```text
Dirty Data Status critical alert
or
pending clarification older than threshold
```

Guardrails:

```text
cooldown
ACK
duplicate suppression
quiet hours 22:00–07:00 WIB
no spam
```

---

## 27. Definition of Done

### 27.1 Level 1 — Core Manual Ready

AIRO is Core Manual Ready when:

```text
Telegram direct input works for all core transaction types including cash.
Account Ledger reliable for wallet movement.
Finance Events emitted for resolved post-cutover events.
Dashboard Data Status and Action Required functional.
Admin readback works.
Deployment registry current.
```

### 27.2 Level 2A — Guarded Email Intake Run-Once Ready

AIRO is Guarded Email Intake Run-Once Ready when:

```text
Level 1 met.
Email detection read-only and safe.
OTP/security hard-block confirmed.
Gmail not mutated.
Telegram clarification works for email candidates.
Category/subcategory flow works.
Amount pointer correct.
Review Queue staging works.
Polling run-once readiness works.
No scheduled trigger installed unless separately approved.
No Account Ledger write from email.
```

### 27.3 Level 2B — Guarded Scheduled Email Intake Ready

AIRO is Guarded Scheduled Email Intake Ready when:

```text
Level 2A met.
Task 4B owner approval received.
Scheduled trigger installed via approved function.
Trigger status verified.
Kill switch confirmed.
First scheduled run has no Gmail mutation.
First scheduled run has no finance write.
```

### 27.4 Level 3 — Owner-Defined 100% Complete

AIRO is owner-defined 100% complete when:

```text
Level 1 met.
Level 2A met.
Level 2B met if owner wants scheduled polling active.
Controlled email-to-Account-Ledger write pilot PASS.
Finance Events co-emission from email write PASS.
Audit Log records email write lifecycle.
Review Queue staging transitions to committed/linked.
Duplicate email candidate creates no duplicate ledger row.
Dashboard/Data Quality reflects email write correctly.
Final Telegram manual regression matrix PASS.
Monthly Review either rewired or explicitly deferred/hidden.
Workbook cleanup complete or explicitly deferred by owner.
PRD and Current State updated and pushed.
```

Task 5 is mandatory for Level 3.

---

## 28. Risk Register

| Risk                                       |   Severity | Required Handling                   |
| ------------------------------------------ | ---------: | ----------------------------------- |
| Runtime/deployment mismatch                |   Critical | Task 0A before every session        |
| CURRENT_STATE.md stale                     |   Critical | Task 0B before feature work         |
| Review Queue missing email identity fields |   Critical | Task 3A                             |
| Amount pointer loss                        |   Critical | Task 2                              |
| Email-to-ledger duplicate write            |   Critical | Task 5 idempotency gate             |
| Monthly Review reads Transactions          |       High | Task 7/8 rewire or hide/defer       |
| Transactions visible                       |       High | Forbidden as master; cleanup Task 8 |
| Dashboard G2 hardcoded months              |     Medium | Task 7 validate/expand              |
| Dashboard Action Required script-written   |     Medium | Task 7 readback required            |
| Cash Ledger still exists                   |     Medium | Task 8 dependency audit             |
| Dashboard backups/copies accumulate        | Low/Medium | Task 8 cleanup                      |
| Audit temp sheet exists                    |        Low | Task 8 cleanup candidate            |
| Proactive alert spam                       |     Medium | Task 10 only with approval          |

---

## 29. Deployment Rules

Always deploy in-place:

```bash
cd /home/egitaristorandas/vortex-ai-skill-lab/apps-script-live
clasp push --force
clasp deploy -i AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA -d "<description>"
clasp deployments
```

Never create new deployment ID unless the existing deployment cannot be updated.

Every deployment must be followed by:

```text
Telegram live smoke
admin readback
deployment registry update
commit and push
```

---

## 30. Required Output Format After Every Task

```text
Task ID              :
Result               : PASS / FAIL / BLOCKED
Repo HEAD            :
Files changed        :
Apps Script version  :
Deployment ID        :
Worker changed       : yes / no
Gmail trigger        : installed / not installed
Gmail mutated        : yes / no
Account Ledger write : yes / no
Finance Events write : yes / no
Review Queue write   : yes / no
Tests run            :
Telegram smoke       : PASS / FAIL — observed behavior
Admin readback       : PASS / FAIL
PRD updated          : yes / no
CURRENT_STATE updated: yes / no
Commit hash          :
Next task            :
```

---

## 31. Antigravity Carry-Over Prompt

Use this in a new Antigravity session:

```text
You are continuing AIRO Personal Finance Command Center.

Repository:
/home/egitaristorandas/vortex-ai-skill-lab

Before doing anything, read:
1. docs/AIRO_FINANCE_PRD_LIVING.md
2. docs/AIRO_FINANCE_CURRENT_STATE.md
3. latest docs/airo-finance/records/
4. docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md

This is AIRO Finance Final Living PRD v2.1.3.

Current baseline:
- Repo baseline: bd6815e
- Feature baseline: a4fd0ac
- Apps Script: apps-script-live @241
- Deployment ID: AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA
- Worker: airo-finance-telegram-proxy → env.APPS_SCRIPT_URL unchanged
- Gmail trigger: NOT INSTALLED
- Email ingestion: DISABLED
- Alert Engine: SAFE MODE
- E-path layer 1: LIVE PASS

Mandatory first step:
Task 0A Runtime State Lock.
Then Task 0B CURRENT_STATE.md Refresh.
Then Task 0C Workbook Schema Contract Verification.
Then Task 0D Dashboard + Monthly Review Contract Verification.

Do not start feature work until Task 0A–0D PASS.

Critical rules:
1. Telegram direct input is PRIMARY.
2. Cash transactions are Telegram/manual first-class.
3. Email is auxiliary passive input only.
4. Only receipts@blubybcadigital.id is current approved email sender.
5. noreply@tokopedia.com is NOT active.
6. Transactions is visible but forbidden as v1 master.
7. Monthly Review is legacy/partial until rewired or hidden.
8. Current linkage field is linked_txn_id, not event_ref.
9. Review Queue email schema extension is conditional and additive-only.
10. Task 5 is mandatory for owner-defined 100% completion.
11. Deploy always uses existing deployment ID in-place.
12. No task is done without Telegram live smoke and readback.
13. Do not skip stop gates.

Execute:
Task 0A → 0B → 0C → 0D → 1 → 2 → 3A → 3B → 4A → 4B if approved → 5 if approved → 6 → 7 → 8 → 9.

Task 10 is optional.
```

---

## 32. Replacement Approval Command

Only replace the repo PRD after owner says:

```text
APPROVE replace AIRO living PRD with v2.1.3
```

After replacement, commit with:

```bash
cd /home/egitaristorandas/vortex-ai-skill-lab && {
  git add docs/AIRO_FINANCE_PRD_LIVING.md
  git commit -m "docs(airo-finance): replace living PRD with v2.1.3 execution contract"
  git push origin main
  git log -1 --oneline
  git status --short --branch
}
```
