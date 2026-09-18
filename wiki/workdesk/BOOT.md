---
type: workdesk-boot
project: AIRO_WORKDESK
workdesk_status: ACTIVE
audience: ai
---
# AIRO WorkDesk — AI Boot Contract

Global ASB BOOT/governance is higher authority.

## Required read order after ASB global boot

1. `control/airo-workdesk.md`
2. `wiki/workdesk/CURRENT.md`
3. `wiki/workdesk/SOURCE_AUTHORITY.md`
4. `wiki/workdesk/KNOWLEDGE_MAP.md`
5. `wiki/workdesk/role/AREA_SALES_SUPERVISOR.md`
6. `wiki/workdesk/glossary/WORK_TERMINOLOGY.md`
7. `wiki/workdesk/TASK_ROUTER.md`
8. task-relevant module(s)
9. source/claim evidence only when verification is needed

## Boot receipt

```text
WORKDESK_BOOT_GUARD=PASS|FAIL
WORKDESK_PROJECT_READ=YES|NO
WORKDESK_CURRENT_READ=YES|NO
WORKDESK_SOURCE_AUTHORITY_READ=YES|NO
WORKDESK_KNOWLEDGE_MAP_READ=YES|NO
WORKDESK_ROLE_MODEL_READ=YES|NO
WORKDESK_GLOSSARY_READ=YES|NO
WORKDESK_TASK_ROUTER_READ=YES|NO
WORKDESK_TASK_MODULES=<list>
AWD_RUNTIME_STATUS=ACTIVE
AWD_RUNTIME_ACCESS_STATUS=AVAILABLE
RUNTIME_LOCATION=VPS AWD Runtime
RUNTIME_CAPABILITY=Fresh AI may request runtime query through approved interface (no direct filesystem access claimed)
```

Missing required file => `WORKDESK_BOOT_GUARD=FAIL`; do not fill gaps from model memory.

## Mandatory AIRO WorkDesk (AWD) Operational Runtime Guard

For every AIRO WorkDesk, business intelligence, or retail sales task:

### 1. AWD Runtime State
- `AWD_RUNTIME_STATUS=ACTIVE`
- `AWD_RUNTIME_ACCESS_STATUS=AVAILABLE`
- `RUNTIME_LOCATION=VPS AWD Runtime` (Host: 43.157.241.228, VM-0-9-ubuntu)

### 2. Operational Architecture
```text
USER
 │
 ▼
AIRO Intelligence Layer (Strategic Reasoning)
 │
 ▼
AWD Runtime Access Interface (awd-query / awd-remote-query / HTTP Bridge)
 │
 ▼
VPS Runtime Executor (Independent from AGY PC)
 │
 ▼
Entity Resolution (AwdEntityResolver dynamic catalog)
 │
 ▼
Query Engine (Direct memory streaming)
 │
 ▼
Operational TSV Authority (Retail, Market, Territory, Stock)
```

### 3. Fresh AI Behavior Contract
- **Step 1**: Check AWD runtime availability first (`awd-query availability` or `awd-remote-query availability`).
- **Step 2**: IF runtime is available, use the approved runtime access interface:
  ```text
  USER BUSINESS TERM → CANONICAL ENTITY → AUTHORITY QUERY → EVIDENCE RECEIPT
  ```
- **Step 3**: IF runtime is unavailable:
  - State limitation clearly.
  - Do NOT pretend direct filesystem access exists.
  - Do NOT ask user to upload raw data prematurely unless runtime is confirmed permanently unavailable or requested data is outside authority scope.

### 4. Authority Source of Truth Rule
- Canonical truth lives strictly in sanitized **Operational TSV runtime datasets** (`wiki/workdesk/business-memory/operational/*.tsv`).
- Raw Excel workbooks (`SSU.2026.xlsx`, `SINSEN_EVALPOLREG`, etc.) are `PRIVATE_RAW_UPSTREAM_PROVENANCE` only. Never resolve current business queries from raw workbook references.

### 5. Entity Resolution Rule
- Mandatory translation before query.
- Canonical examples:
  - `"Sinsen Bulian"` → `PT. SINAR SENTOSA MOTORA - BULIAN`
  - `"CSM Sarolangun"` → `CV. CITRA SENTOSA MOTOR - SRLG`
  - `"Kecamatan Pauh"` → `PAUH` / Sarolangun territory hierarchy

### 6. Diagnostic Workflow
```text
FACT → SYMPTOM → HYPOTHESIS → EVIDENCE → ROOT CAUSE → ACTION PLAN
```

### 7. Security & Limitation Contract
- No direct filesystem access claim.
- No raw data hallucination.
- No invented metrics.
- No authority bypass.
- No TSV mutation.


## Reasoning guard

For business-performance questions, default to evidence-based diagnosis before solution:

`result gap → scope/market → segment/area → dealer/channel → commercial → people/productivity → activity/funnel → execution/system/NOS → root cause → quantified action → control`

Use only relevant branches.

## Source guard

- current official/current-year source wins current-rule conflict;
- current verified work evidence wins stale documentation for live state;
- formal training defines the taught framework;
- Owner projects show applied working patterns, not current market data;
- Notion transcript is supplementary and may be corrupt;
- model memory is last resort.

## Evidence guard

For consequential claims, prefer `evidence/workdesk/CLAIM_LEDGER.tsv` and exact source pointers.

## Completion guard

`SOURCE_ACCOUNTING=100%` != `FULLY_DIGESTED_AND_TRANSFERABLE=YES`.
