# AIRO Finance Post-Project Debt

This file tracks non-blocking cleanup and hardening items that are intentionally deferred until the main AIRO Finance sprint roadmap is completed.

## Deferred after all active sprints

### 1. Transcript/log text Review Queue hygiene

Status: deferred / post-project debt  
Priority: medium  
Blocking current sprint: no

Context:

During the @192 regression audit, core ambiguity handling was confirmed to still ask clarification for normal ambiguous finance inputs such as:

- `cc <amount>`
- `makan <amount>`
- `cash <amount>`
- `hutang <amount>`

However, pasted chat transcript/log text can still be classified as `Unknown/Lainnya` and may fall into `🧾 Review Queue` instead of being rejected immediately.

Desired future behavior:

- Admin commands must remain admin-only.
- Chat transcript/log text such as `[25/05/2026 ...]`, `Airo Finance:`, or user/bot conversation dumps should be safe-rejected.
- Transcript/log text should not be written to domain tabs or Review Queue unless explicitly imported by a future supported import flow.

Reason for deferral:

This is not blocking current Sprint 2 domain tab work. Main active blocker remains Hutang direct routing/write.

### 2. Credit Card dirty smoke rows cleanup

Status: deferred / post-project debt  
Priority: low-medium  
Blocking current sprint: no

Known dirty rows in `💳 Credit Card` from prior live smoke/debug attempts:

- row 20: wrong amount from numeric smoke/date text
- row 21: admin transcript dirty write
- row 22: duplicate/wrong amount smoke row

Desired future behavior:

- Do not delete brutally without audit trail.
- Mark as void/test_dirty/ignored if cleanup is needed.
- Preserve reason notes for traceability.

Reason for deferral:

User chose to skip cleanup for now to keep project moving quickly through remaining sprints.
