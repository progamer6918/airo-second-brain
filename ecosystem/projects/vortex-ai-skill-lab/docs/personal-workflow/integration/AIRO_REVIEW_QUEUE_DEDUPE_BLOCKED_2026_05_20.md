# AIRO Review Queue Dedupe Blocked

Date: 2026-05-20  
Project: AIRO Finance Sheet Workflow  
Scope: Review Queue dedupe closeout

## Status

BLOCKED.

Review Queue routing itself had been previously verified end-to-end, but dedupe guard is not safe to patch yet.

## What happened

Multiple patch attempts tried to prevent duplicate Review Queue rows by adding dedupe logic around Apps Script append paths.

Runtime tests showed the dedupe attempts did not work:

- Rows continued to increase by 2 after sending the same Review Queue phrase twice.
- Review Queue audit still showed empty `queue_id`, `raw_text`, `amount`, and `account` for rows.
- Hidden dedupe log attempts did not increment at runtime.
- The actual runtime write path and actual Review Queue header mapping are not sufficiently understood.

## Recovery

The failed uncommitted patch attempts were backed up to `/tmp` and rolled back.

Clean source from `HEAD` was restored to:

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs`
- `apps-script-live/AIRO_Finance_Multitab_Final_v1.js`

Apps Script was redeployed from clean source:

- Version: 146

## Current Decision

Do not patch Review Queue dedupe again until the following are available:

1. Actual Review Queue header row audit from Google Sheet.
2. Exact write path used by Telegram runtime for Review Queue rows.
3. A read-only proof showing which columns receive `raw_text`, `queue_id`, status, reason, amount, and account.
4. A minimal failing reproduction that does not write repeated smoke rows blindly.

## Roadmap impact

Review Queue dedupe is not closed.

Roadmap should continue with domains that have clearer runtime commands or safer isolated planners, such as:

1. Cicilan Rumah
2. Hutang
3. Aset
4. Monthly Review
5. Dashboard final after source domains stabilize

## Safety Rule

No more Review Queue dedupe patching in production until header/path audit is completed first.
