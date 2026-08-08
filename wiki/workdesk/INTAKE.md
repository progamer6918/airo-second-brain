---
type: workdesk-intake
project: AIRO_WORKDESK
workdesk_status: ACTIVE
audience: human-ai
---

# 📥 AIRO WorkDesk Sustainable Intake Specification

Specialized intake rules for receiving, digesting, and routing professional work materials into AIRO WorkDesk.

> [!NOTE]
> Inherits from global [`docs/contracts/AIRO_INPUT_PROCESSING_CONTRACT.md`](../../docs/contracts/AIRO_INPUT_PROCESSING_CONTRACT.md).
> Governed by `WORKDESK_PUBLIC_KNOWLEDGE_POLICY=PUBLIC_FIRST`.

---

## 🛠 WorkDesk Intake Routing Table

| Input Type | Trigger Example | Primary Target | Action / Ledger |
|---|---|---|---|
| `OWNER_CORRECTION` | "NMS = Network Management System" | `wiki/workdesk/glossary/WORK_TERMINOLOGY.md` | Update claim ledger; mark `OWNER_CONFIRMED` |
| `NEW_SOURCE_DOCUMENT` | "Dealer Review 2026.pdf" | `evidence/workdesk/SOURCE_MANIFEST.tsv` | Digest atomic claims; update affected modules |
| `CURRENT_BUSINESS_DATA` | "Sales Excel September" | Active task evidence / Daily report | Do NOT pollute permanent Wiki; task-level evidence |
| `PROJECT_ARTIFACT` | "D-READY update formula" | `projects/d-ready.md` | Route to child project `D_READY` |
| `PROJECT_ARTIFACT` | "VBA macro update script" | `projects/report-automation-vba.md` | Target `REPORT_AUTOMATION_VBA`; BLOCK IF FROZEN |
| `EPISODIC_INPUT` | "Besok meeting jam 9" | Active session note / Scratch | Do NOT create Wiki note; session context only |
| `CONFLICT` | New presentation vs old policy | `evidence/workdesk/CONFLICT_REGISTER.tsv` | Apply `SOURCE_AUTHORITY.md`; resolve or log conflict |
| `SECRET_OR_SENSITIVE` | Password, credential, raw transcript | EXCLUDED | Do NOT commit; report secret detection |

---

## 🔒 Public-First Knowledge Policy

- `WORKDESK_PUBLIC_KNOWLEDGE_POLICY=PUBLIC_FIRST`
- `DISTILLED_PROFESSIONAL_KNOWLEDGE=PUBLIC_SAFE`
- `OWNER_APPLIED_KNOWLEDGE=PUBLIC_SAFE_AFTER_SANITIZATION`
- `PROVENANCE_METADATA=PUBLIC_SAFE`
- `SOURCE_ACCOUNTING=PUBLIC_SAFE`
- `SECRETS=EXCLUDED`
- `AUTH_ARTIFACTS=EXCLUDED`
- `RAW_PRIVATE_CHAT_EMAIL=EXCLUDED`
- `SENSITIVE_PERSONAL_DATA=EXCLUDED`
- `RAW_THIRD_PARTY_TRAINING_SOURCE=CASE_BY_CASE_RIGHTS_CONFIDENTIALITY_SIZE_DECISION`
- `FRESH_AI_DEPENDENCY_ON_PRIVATE_SOURCE=NO`

---

## 🌿 WorkDesk Child Project Routing Rules

- If input target is **D-READY**:
  - `TARGET_PROJECT=AIRO_WORKDESK`
  - `TARGET_CHILD_PROJECT=D_READY`
  - Status: `ACTIVE` (`PILOT_LOGIC_VALIDATION`).

- If input target is **Report Automation VBA**:
  - `TARGET_PROJECT=AIRO_WORKDESK`
  - `TARGET_CHILD_PROJECT=REPORT_AUTOMATION_VBA`
  - Status: `FROZEN_BY_OWNER` (`EXECUTION_ALLOWED=NO`). Execution or mutation blocked unless Owner explicitly reopens project.
