# AIRO Finance Gate P2 Email Expense Direction False Inflow v383 Email Ingestion Lag Remediation Plan Summary

- **Marker**: `AIRO_ARFIN_GATE_P2_EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_V383_EMAIL_INGESTION_LAG_OR_MISSED_CANDIDATE_REMEDIATION_PLAN_NO_DEPLOY`
- **Timestamp**: `20260720_173927`
- **Base Commit SHA**: `5cf50ef86026fe1e81ff341ed6f9531e8a68718a`
- **Source SHA256 Deployed**: `a02aeafa8f689d6a6f2c1bf62f3259d950fdb70aea612806fd0cf828287dc620`
- **Apps Script Deployed Version**: `383`
- **Target Deployment Suffix**: `ZYjuOA`
- **Deployment Readback**: PASS
- **Local Self-Test**: PASS (35/35)
- **Runtime Proof Status**: `PASS 35/35 (accepted with log truncation limitation)`
- **RCA Classification**: `EMAIL_INGESTION_PICKUP_PATH_HAS_SOURCE_LEVEL_LAG_OR_SKIP_RISK_AWAITING_SAFE_REMEDIATION_PLAN`
- **Remediation Plan Status**: `READY`
- **Repair Scope**: `EMAIL_INGESTION_SAFE_DIAGNOSTICS_PROCESSED_MARKER_GUARD_AND_PROMPT_DISPATCH_CONFIRMATION`
- **Direction Repair Scope**: `UNCHANGED_UNLESS_LIVE_PROMPT_PROVES_DIRECTION_REGRESSION`
- **Current Test Count**: 35
- **Planned Ingestion Tests**: 11
- **Expected Test Count After Repair**: 46

## Remediation Plan Key Components

### 1. Safe Non-Mutating Ingestion Audit Helper
- Add a diagnostic helper function (`runTask105EmailIngestionDiagnosticFromEditor`) for manual Owner editor run.
- Returns non-secret pickup metrics (candidate count, provider, subject hash/class, skip reason, processed marker status, prompt dispatch status).
- Agent will **NOT** execute this runtime function and will **NOT** access Gmail API.

### 2. Processed-Marker Safety Guard
- Refactor processed marker logic: do **NOT** mark an email/thread as processed until Telegram prompt dispatch returns explicit success.
- If prompt dispatch fails or encounters network error, candidate remains retryable in subsequent poller cycles.

### 3. Prompt-Dispatch Confirmation Guard
- Introduce explicit pipeline state progression:
  `CANDIDATE_FOUND` -> `PROMPT_DISPATCH_ATTEMPTED` -> `PROMPT_DISPATCH_CONFIRMED` -> `PROCESSED_MARKER_WRITTEN`.

### 4. Search Window & Query Recency Review
- Audit and normalize Gmail search query parameters and recency filters (`newer_than:1d`, label criteria, and timezone handling) to eliminate boundary drop risks during polling gaps.

### 5. Self-Test Expansion (+11 Ingestion Tests)
- Expand local unit harness from **35** to **46** tests covering:
  - Blu expense candidate eligibility;
  - Recency window normalization;
  - Processed marker ordering (never written before prompt success);
  - Dispatch error fallback & retryability;
  - Non-secret diagnostic output validation.

## Governance & Privacy
- **Agent Gmail Access**: DILARANG (NO).
- **Agent Poller / Trigger Execution**: DILARANG (NO).
- **Workbook / Ledger Mutation**: DILARANG (NO).
- **Direction Repair Logic**: Unchanged (Direction repair logic remains verified at 35/35 PASS).
- **Incident Status**: `AFPD-INC-009=EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_V383_EMAIL_INGESTION_LAG_OR_MISSED_CANDIDATE_REMEDIATION_PLAN_READY_AWAITING_REPAIR_PREFLIGHT`
- **Recommended Next Gate**: `GATE_P2_EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_V383_EMAIL_INGESTION_LAG_OR_MISSED_CANDIDATE_REPAIR_PREFLIGHT_NO_DEPLOY`
