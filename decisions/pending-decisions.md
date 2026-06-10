
last_updated: 2026-06-10
updated_by: owner-confirmed-design
status: current
confidence: owner-confirmed
source: chat-derived
Pending Decisions

Unresolved or deferred decisions only.

Do not duplicate this file under state/.

Open
Distillation automation trigger

Status:

Deferred to Phase 2.

Question:

Should distillation be manually triggered by owner or automatically suggested by Hermes/Earesmes?

Default safe answer:

Manual trigger first.
Automation may suggest, not directly rewrite canonical files.
Concurrent consumer lock mechanism

Status:

Deferred to Phase 2.

Question:

How should AIRO handle multiple consumers updating the repo at the same time?

Default safe answer:

Use append-only inbox files per consumer/session first.
Avoid simultaneous edits to canonical files.
Add merge/lock script later.
Hermes session-start hook

Status:

Deferred to Phase 2.

Question:

How should Hermes/Earesmes automatically load BOOT.md at session start?

Default safe answer:

Add a local startup routine that reads BOOT.md, CURRENT.md, CONTEXT.md, AGENTS.md, and SECURITY.md.

## 2026-06-10 23:06 — AIRO Finance remaining mandatory work
- verified: Remaining mandatory count after Task 8 is 4.
- verified: Count includes Task 9.
- verified: Count excludes optional Task 10.
- pending: Credit Card ledger-first implementation path and acceptance guards.
- pending: Asset ledger-first implementation path and acceptance guards.
- pending: Dashboard migration away from Finance Events toward Account Ledger/domain tabs.
- pending: Task 9 final regression, cleanup, documentation, and owner acceptance checklist.
- unknown: whether Task 10 Alert Engine will be activated.

## 2026-06-10 23:51 — AIRO Sync cross-consumer automation pending
- owner-confirmed: owner wants AIRO Sync to keep Second Brain updated from meaningful decisions/progress across ChatGPT, other chat sessions, and other AI tools.
- pending: define exact automation mechanism for cross-consumer closeout ingestion.
- pending: decide whether Hermes/Earesmes, Antigravity, Claude, and future agents should auto-write to inbox/state/changelog after meaningful work.
- constraint: no raw transcript dump, no secrets, no unavailable-session claims.

## 2026-06-10 23:55 — AIRO Finance Task 9 preparation pending items
- pending: Credit Card exact route audit for purchase/payment ledger-first behavior.
- pending: Asset/Aset exact route audit for purchase/valuation ledger-first behavior.
- pending: Dashboard dependency audit to remove/replace Finance Events dependency and confirm Transactions/Cash Ledger absence.
- pending: update stale AIRO Finance current-state docs only after evidence and owner-approved scope.
- constraint: no Task 9 ready-to-use declaration until the three pre-final technical items are verified or explicitly owner-deferred.

## 2026-06-10 23:57 — Credit Card ledger-first pending audit
- pending: inspect markCreditCardPocketBluTransfer_ exact order: match pending purchase, write Account Ledger, readback, update Credit Card status, duplicate guard.
- pending: inspect appendCreditCardPurchase_ exact behavior: domain write only, no Account Ledger wallet outflow, duplicate guard.
- pending: decide whether Credit Card requires source patch or only guarded live regression/readback.

## 2026-06-11 00:03 — AIRO Sync batch mode and Credit Card pending work
- owner-confirmed: AIRO Sync batch mode should be inherited by future chats/AI consumers through Second Brain.
- pending: consider promoting this operating rule into AGENTS.md/CURRENT.md later with explicit owner-approved canonical edit, if needed.
- pending: Credit Card patch plan for ledger-success-before-status-update and duplicate/idempotency guard.
- pending: after CC, continue Asset/Aset narrow audit and Dashboard dependency audit.

## 2026-06-11 00:07 — Task 9 preparation pending after CC/Asset audits
- pending: Credit Card focused patch plan for ledger-success-before-status-update and idempotency guard.
- pending: Asset focused patch plan for Account Ledger-first then Aset projection and idempotency guard.
- pending: Dashboard dependency audit to migrate away from Finance Events and verify Transactions/Cash Ledger absence.
- pending: after Dashboard audit, decide patch order and whether CC+Asset can be patched together or should be split.
