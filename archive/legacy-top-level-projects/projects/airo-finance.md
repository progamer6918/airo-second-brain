last_updated: 2026-06-10
updated_by: owner-confirmed-design
status: current
confidence: owner-confirmed
source: chat-derived
Project: AIRO Finance
Summary

AIRO Finance is one project inside the wider AIRO ecosystem.

It is a personal finance command center using Google Spreadsheet, Google Apps Script, Telegram, and guarded optional email ingestion.

This file is a Second Brain project pointer and summary only. It is not the execution source of truth.

Current Status

Canonical status lives in the vortex-ai-skill-lab repo.

Read these before AIRO Finance execution:

docs/AIRO_FINANCE_PRD_LIVING.md
docs/AIRO_FINANCE_CURRENT_STATE.md
docs/airo-finance/records/

Do not trust status in this file for execution.

Source-of-Truth Rule

For AIRO Finance, use this priority:

Live runtime evidence
Google Sheet actual state
Apps Script active source
vortex-ai-skill-lab repo docs and records
This Second Brain project summary
Chat summaries
Model memory

If this file conflicts with the canonical AIRO Finance repo, the canonical AIRO Finance repo wins.

Stable Architecture Summary
Telegram is the primary owner-facing interface.
Google Spreadsheet is the operational workspace.
Google Apps Script is the main backend runtime.
Cloudflare Worker may act as Telegram proxy / async bridge.
Gmail/email ingestion is optional, guarded, and auxiliary.
Account Ledger is wallet/account movement only.
Finance Events is central event index, not balance ledger.
Dashboard is an intelligence cockpit, not source-of-truth.
Review Queue is unresolved exception fallback and guarded email staging gate.
Sensitive email, OTP, and security content must never be stored or forwarded.
Execution Rule

Before any AIRO Finance patch or deployment, read the canonical repo current state and latest records.

Do not execute from this Second Brain summary alone.
