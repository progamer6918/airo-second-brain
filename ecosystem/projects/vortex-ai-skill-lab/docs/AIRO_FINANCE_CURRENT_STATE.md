# AIRO Finance Current State

This file is the compact handoff state for new chats, agents, and future work.
Update this file after major live milestones, deployment promotions, and blocker changes.

## Last updated

2026-06-03 22:15 WIB

---

## 1. Verified Active Baseline

* **Repo baseline**: `4a902bb` (current HEAD)
* **Previous PRD baseline**: `bd6815e`
* **Feature baseline**: `a4fd0ac` (Phase 6H-G3 category registry fix)
* **Apps Script Project**: `apps-script-live`
* **Apps Script version**: `@244`
* **Deployment ID**: `AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA`
* **Worker**: `airo-finance-telegram-proxy` (running, target `env.APPS_SCRIPT_URL` unchanged, async_ack bridge active)
* **Gmail trigger**: NOT INSTALLED
* **Email Ingestion**: DISABLED
* **Alert Engine**: SAFE MODE (trigger installed, safe mode handler, proactive send OFF)
* **E-path Layer 1**: LIVE PASS @243

---

## 2. Workbook Schema Contract Summary (Task 0C Verified)

All headers are header-mapped in the Apps Script and correspond to the following structures:

### 2.1 Account Ledger
* **Headers**: `entry_id, date, account, amount_in, amount_out, balance, type, category, description, raw_text, source_tab, linked_txn_id, notes`
* **Rules**: 
  - linked_txn_id is the canonical linkage.
  - Do not require event_ref in v1.
  - Do not reorder or rename columns.

### 2.2 Finance Events
* **Headers**: `event_id, event_ts, event_type, event_source, source_tab, source_row, linked_txn_id, account, category, amount, direction, status, reason, payload_json, notes`
* **Rules**:
  - Event index only, not a balance ledger.
  - Subcategory/status live in payload_json.

### 2.3 Review Queue
* **Headers**: `queue_id, created_at, source, raw_text, parsed_type, parsed_category, parsed_subcategory, parsed_amount, parsed_currency, parsed_account, parser_confidence, issue_reason, suggested_fix, review_status, reviewed_at, approved_transaction_id, local_db_table, local_db_rowid, sync_hash, notes`
* **Status**: Missing email extension fields (email_candidate_id, etc.) is expected until Task 3A.

### 2.4 Email Ingestion Log (`_AIRO_Email_Ingestion_Log`)
* **Headers**: `created_at, candidate_id, message_id, thread_id, sender, provider, received_at, subject_hash, display_amount, inferred_direction, display_time, clarification_question_type, parse_status, candidate_type, clarification_needed, clarification_status, resolved_answer, resolved_label, resolved_at, telegram_chat_id, telegram_sent, write_allowed, write_performed, finance_event_ref, notes`
* **Rules**:
  - Main source for email candidate identities. No full body is stored.

### 2.5 Visibility Policies
* **Transactions**: `💸 Transactions` is visible but forbidden as v1 master (for future statement parsing only).
* **Cash Ledger**: `💵 Cash Ledger` is hidden, legacy, and transitional.
* **Monthly Review**: `📅 Monthly Review` is visible, legacy, and partial until rewired or hidden.
* **Dashboard**: `🏠 Dashboard` is visible and official.

---

## 3. Dashboard and Monthly Review Data Contract (Task 0D Verified)

* **Visual Template Source**: Rebuilt using copy-from-template `_AIRO_Dashboard_Template_Claude` (Excel reference clone).
* **Topbar helpers**:
  - `B2`: Sync timestamp (script-written)
  - `G2`: Selected month dropdown. Current validation values: `📅 April 2026`, `📅 Mei 2026`, `📅 Juni 2026`
  - `M2`: Selected month helper derived from G2
  - `M3`: Start date of selected month
  - `M4`: End date of selected month
* **Action Required cards**: Script-written values. Global urgent issues (Review Queue pending, poller errors) remain visible regardless of G2. Month-specific issues follow G2 filter.
* **Smart Insight**: Month-scoped via G2/M2/M3/M4. Displays data-quality warnings if Data Status is Dirty/Warning.
* **Source Mappings**:
  - Dashboard analytics reads: `Account Ledger`, `Finance Events`, `Review Queue`
  - Dashboard must never use `Transactions` or `Cash Ledger` as source of truth.
  - Monthly Review currently reads `Transactions` in multiple formulas (unrewired, legacy).

---

## 4. Current Handoff Hiearchy & Task Order

Antigravity must execute tasks strictly in this order:

1. **Task 0A** — Runtime State Lock (PASS)
2. **Task 0B** — CURRENT_STATE.md Refresh (PASS, this file)
3. **Task 0C** — Workbook Schema Contract Verification (PASS)
4. **Task 0D** — Dashboard + Monthly Review Contract Verification (PASS)
5. **Task 1** — E-path subcategory flow completion (PASS)
6. **Task 2** — Amount pointer fix (PASS)
7. **Task 3A** — Review Queue email schema extension (PASS)
8. **Task 3B** — Email → Telegram → Review Queue staging (BLOCKED_OWNER_ACTION_REQUIRED)
9. **Task 4A** — Polling readiness, no trigger install
10. **Task 4B** — Scheduled trigger install (owner approval required)
11. **Task 5** — Controlled email-to-ledger write pilot (owner approval required)
12. **Task 6** — Final Telegram manual regression matrix
13. **Task 7** — Dashboard + Finance Events + Reconciliation smoke
14. **Task 8** — Workbook and repo cleanup audit
15. **Task 9** — Final closeout and ready-to-use declaration

---

## 5. Active Risks & Mitigation Strategies

| Risk | Severity | Required Handling |
| :--- | :--- | :--- |
| Runtime/deployment mismatch | Critical | Task 0A check at start of every session |
| CURRENT_STATE.md stale | Critical | Task 0B refresh before starting feature work |
| Review Queue missing email identity | Critical | Staged schema extension in Task 3A |
| Amount pointer loss | Critical | Task 2 mapping validation |
| Email-to-ledger duplicate write | Critical | Task 5 idempotency check and dedupe key |
| Monthly Review reads Transactions | High | Rewire to Account Ledger or hide in Task 7/8 |
| Transactions visible | High | Forbidden write target; cleanup in Task 8 |
| Dashboard G2 hardcoded months | Medium | Task 7 dynamic validation range update |
| Dashboard backups accumulate | Low | Archive policy enforcement in Task 8 |

---

## 6. Historical Handoff Log (Pushed to Handoff History)

For historical logs and sprint records prior to Phase 6H activation, consult the commit history or `docs/airo-finance/records/`.
Previous operating modes, such as Sprint 2 Domain Tabs and Sprint 3 Cash Ledger Removal, are fully verified and closed.
All source code, proxy routing, and script deployments are now frozen at version `@243`.
No feature development, Apps Script deploy, or trigger mutations should occur until Task 3B.
