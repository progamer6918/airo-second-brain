---
type: workdesk-boot
project: AIRO_WORKDESK
workdesk_status: ACTIVE
audience: ai
---
# AIRO WorkDesk — AI Boot Contract

Global ASB BOOT/governance is higher authority.

## Required read order after ASB global boot

1. `projects/airo-workdesk.md`
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
```

Missing required file => `WORKDESK_BOOT_GUARD=FAIL`; do not fill gaps from model memory.

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
