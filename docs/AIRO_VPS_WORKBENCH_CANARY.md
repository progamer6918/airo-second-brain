# AIRO VPS Workbench — Architecture and Operational Workflow

**Document type:** Canary artifact — workflow validation only  
**Status:** Current  
**Produced by:** EARESMES executor canary (`job_20260831T150937Z`)  
**Session:** `0b299a56-3328-4e6b-beff-052809a47af8`

---

## 1. AIRO VPS Purpose

The AIRO VPS Workbench is the primary runtime host for AIRO ecosystem automation.

It provides:

- A persistent Linux environment (Ubuntu on WSL2 / VPS) for continuous background agent operation.
- The canonical execution surface for EARESMES, Arfin, and AIRO Sync workflows.
- Local git operations and push/pull access to the AIRO Second Brain (ASB) repository.
- A controlled, governance-bound surface — no ad-hoc autonomous mutations are permitted without an approved job or session event.

---

## 2. EARESMES Role

EARESMES is the **controlled job coordinator** running on the VPS. It is NOT an autonomous agent.

| Property              | Value                                        |
|-----------------------|----------------------------------------------|
| Role                  | Controlled coordinator only                  |
| Model calls           | FORBIDDEN                                    |
| Autonomous planning   | FORBIDDEN                                    |
| Self-modification     | FORBIDDEN                                    |
| Execution authority   | Owner-approved jobs only                     |
| State transitions     | Deterministic — pending → running → done     |

EARESMES components on the VPS:

| File                          | Purpose                                            |
|-------------------------------|----------------------------------------------------|
| `earesmes/runner.py`          | Polling job runner — state machine only            |
| `earesmes/cli.py`             | Human command entry point — creates validated jobs |
| `earesmes/task_boundary.py`   | Deterministic risk/category classifier             |
| `earesmes/capability_resolution.py` | Deterministic capability routing layer       |
| `earesmes/executor_adapter.py`| Controlled handoff package builder                 |

---

## 3. Operational Workflow

```
Owner types objective
       │
       ▼
earesmes/cli.py submit "<objective>"
       │
       ├─ task_boundary.py         → category / risk / approval_required
       ├─ capability_resolution.py → capability / executor_hint / authority
       └─ executor_adapter.py      → execution package (if packageable capability)
       │
       ▼
Job JSON written to:
  earesmes/jobs/pending/<job_id>.json
       │
       ▼
runner.py polls pending/
       │
       ├─ Validates approval field
       ├─ pending → running  (receipt written)
       ├─ executor dispatched (V1: manual placeholder, no autonomous action)
       └─ running → success | failed  (receipt written)
       │
       ▼
Job moved to:
  earesmes/jobs/done/<job_id>.json

Receipts written to:
  earesmes/state/receipts/<job_id>_<timestamp>_<status>.json
```

---

## 4. Capability Routing Summary

| Capability       | Trigger Keywords                        | Executor Hint | Authority           |
|------------------|-----------------------------------------|---------------|---------------------|
| `maintenance`    | vps, server, disk, memory, status, cek  | local         | earesmes_runner     |
| `development`    | code, script, feature, bug, build, buat | antigravity   | earesmes_runner     |
| `airo_workdesk`  | sales, dealer, market, territory, flp   | awd_workflow  | airo_workdesk_system|
| `knowledge`      | obsidian, kcc, documentation, session   | asb_kcc       | asb_kcc_system      |
| `owner_review`   | architecture, delete, remove, migration | owner         | owner_direct        |
| `unknown`        | (no match)                              | unknown       | unresolved          |

---

## 5. Governance Boundaries

```
EARESMES_GOVERNANCE_V1=ENFORCED
  no_model_calls=true
  no_autonomous_planning=true
  no_recursive_loops=true
  no_self_modification=true
  no_uncontrolled_execution=true
  coordinator_only=true
```

**Hard limits:**

- No job may mutate the runner, CLI, boundary, or capability files.
- No execution package may contain secrets, credentials, or sensitive data.
- `approval: approved` is required on every job — missing or invalid approval routes to `review_required`.
- High-risk (`architecture`, `delete`, `remove`) capabilities require `owner_review` — no package is created automatically.
- Every state transition is receipt-bound and evidence-logged.

---

## 6. Receipt Model

Every job state transition produces an immutable receipt in `earesmes/state/receipts/`.

Receipt schema:

```json
{
  "earesmes_version": "1.0.0",
  "job_id": "<id>",
  "status": "pending | running | success | failed | review_required",
  "detail": "<transition reason>",
  "timestamp_utc": "<ISO-8601>",
  "job_snapshot": { }
}
```

Executor receipt contract (required fields from executor on completion):

| Field                 | Description                                       |
|-----------------------|---------------------------------------------------|
| `RESULT`              | PASS or FAIL                                      |
| `EXIT_CODE`           | Integer (0 = success)                             |
| `CHANGED_FILES`       | Files created, modified, or deleted               |
| `COMMIT_SHA`          | Git SHA if committed (or NONE)                    |
| `VALIDATION_EVIDENCE` | Proof that objective was met                      |

---

## 7. Canary Validation Evidence

This document is itself the canary artifact, produced by the end-to-end EARESMES workflow:

| Step                    | Evidence                                                        |
|-------------------------|-----------------------------------------------------------------|
| Job submitted           | `job_20260831T150937Z` via `earesmes/cli.py`                   |
| Boundary classified     | `category=development risk=medium approval_required=True`       |
| Capability resolved     | `capability=knowledge executor_hint=asb_kcc`                   |
| Execution package       | `earesmes/execution_packages/job_20260831T150937Z/` — 4 files  |
| `handoff.json` status   | `READY_FOR_EXECUTION`                                           |
| Runner processed        | `pending → running → success` (receipt written)                 |
| Artifact created        | `docs/AIRO_VPS_WORKBENCH_CANARY.md` (this file)                |

---

*Generated as EARESMES real workflow canary — session `0b299a56-3328-4e6b-beff-052809a47af8`.*
