# 05_STATE_MACHINES.md

## Intake Flow States
- **email_outgoing_account_pending**: Awaiting funding account selection.
- **category_pending / category_expense**: Awaiting category mapping index.
- **category_search_pending**: Resolving category queries.
- **subcategory_pending**: Awaiting subcategory selection index.
- **direction_pending**: Awaiting selection between Pemasukan, Pengeluaran, or Transfer.
- **Review Queue Approval Staging**: Transaction parsed but awaiting manual approval.
- **Manual-Review Fallback**: Clarification failed or timed out; awaits manual corrections.
- **Approval Commit**: Staged transaction posted to ledger.
- **Reject Flow**: Item marked discarded.
- **Pending Removal**: Property state cleared.
- **Last-Prompt Pointer Arbitration**: Disambiguation tracking.

## Core Distinctions
- **Clarification Pending**: Temporary state in Properties Service before write.
- **Manual-Review Fallback**: Review Queue row marked with `issue_reason` fallback status.
- **Approval Staging**: Review Queue row with `pending` status awaiting `/approval`.
- **Committed Transaction**: Transaction finalized in Account Ledger.
