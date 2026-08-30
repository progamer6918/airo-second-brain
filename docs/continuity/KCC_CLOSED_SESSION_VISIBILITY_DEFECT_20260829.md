# KCC Closed Session Visibility Defect (2026-08-29)

**Status:** OPEN / NEEDS_VERIFICATION  
**Date:** 2026-08-29  
**Affected Closed Session ID:** `1e97cbf6-2e62-4f2e-9385-dcd10b12c1c7`  
**Related Replan Document:** [EAB vNext — Earesmes Orchestrator Replan](../../ecosystem/projects/earesmes-arfin-bridge/docs/EAB_VNEXT_EARESMES_ORCHESTRATOR_REPLAN.md)  
**Governing Contract:** [docs/contracts/AIRO_KNOWLEDGE_CONTINUITY_SOP.md](../contracts/AIRO_KNOWLEDGE_CONTINUITY_SOP.md)  

---

## 1. Incident Overview & Mandatory Facts

* **Active Visibility:** While session `1e97cbf6-2e62-4f2e-9385-dcd10b12c1c7` was active, the session was visible to the Owner in Obsidian via standard active session projection views (`state/active-session.md`, `state/active-context.md`).
* **Closeout Receipt Evidence:** The stop-loss closeout script executed canonical session close, reporting:
  ```text
  SESSION_CLOSE_RESULT=PASS
  CLOSEOUT_STATUS=SAFE_CLOSEOUT_COMPLETE
  ```
* **Observed Disappearance:** Immediately following session closeout, the Owner could not locate or view the session in Obsidian as expected.
* **Continuity Imperative:** The Owner explicitly flagged this visibility breakdown for investigation because knowledge continuity and historical session discoverability must remain trustworthy and intuitive across AI sessions.

---

## 2. Preliminary Hypotheses (Unproven)

These hypotheses are recorded strictly as unverified candidates for the upcoming verifier task:

* **Hypothesis 1 (H1 — Path & Projection Mismatch):** The active session projection path/title (e.g. `state/active-session.md` or live title) differs from the permanent historical archive path (e.g. `worklog/sessions/YYYY-MM-DD/...`), causing navigation and discoverability confusion in the Obsidian file tree.
* **Hypothesis 2 (H2 — Linkage & Indexing Failure):** The permanent historical session note or the daily log index (`worklog/daily/2026-08-29.md`) may not have been updated, formatted, or linked correctly despite the session close command returning success.
* **Hypothesis 3 (H3 — Semantic Status Confusion):** The closeout operation outcome (`BERHASIL` for the technical rollback/closeout command) may mask or conflict with the actual business outcome of the objective (`FAILED_BOUNDED_ATTEMPT`), creating misleading metadata in generated notes.

---

## 3. Required Verifier Scope & Metrics

The next dedicated verifier task (`NEXT_1`) must empirically prove:

| Metric Key | Expected Target | Description |
| :--- | :--- | :--- |
| `PERMANENT_SESSION_NOTE_EXISTS` | `YES` | Confirm existence of note under `worklog/sessions/2026-08-29/...` |
| `PERMANENT_SESSION_NOTE_PATH` | `<exact path>` | Report absolute/canonical path of archive note |
| `PERMANENT_SESSION_NOTE_SESSION_ID_MATCH` | `YES` | Verify note frontmatter contains `1e97cbf6-2e62-4f2e-9385-dcd10b12c1c7` |
| `DAILY_2026_08_29_LINKS_SESSION` | `YES` | Confirm daily note links to the permanent session note |
| `OBSIDIAN_EXPECTED_DISCOVERABILITY` | `HIGH / LOW` | Evaluate navigation discoverability from Owner vault perspective |
| `SESSION_NOTE_STATUS` | `CLOSED` | Verify session lifecycle state inside note |
| `SESSION_NOTE_OUTCOME_INCLUDES_FAILED_BOUNDED_ATTEMPT` | `YES` | Confirm factual outcome is clearly stated in note body |
| `ACTIVE_SESSION_AFTER_CLOSE` | `NONE` | Confirm active projection is cleared upon close |
| `CLOSEOUT_SEMANTIC_CONSISTENCY` | `PASS / FAIL` | Verify no contradiction between technical and business verdicts |

---

## 4. Defect Classification Rules

Following the empirical verifier run, the defect must be classified into exactly one category:

* **`KCC_CLOSEOUT_DURABILITY_DEFECT`:** If no permanent historical session note was generated on disk despite `SESSION_CLOSE_RESULT=PASS`.
* **`KCC_CLOSEOUT_VISIBILITY_UX_DEFECT`:** If the permanent note exists on disk but is practically undiscoverable due to folder hierarchy, naming mismatch, or missing daily index links.
* **`KCC_CLOSEOUT_SEMANTIC_STATUS_DEFECT`:** If the permanent note metadata incorrectly labels the session as successful when the underlying objective ended in a stop-loss failure.

---

## 5. Bounded Next Step

* **Action:** Execute task `KCC_CLOSED_SESSION_VISIBILITY_AND_SEMANTIC_INTEGRITY_VERIFIER`.
* **Scope Guard:** Read-only inspection and verifier evidence generation only. No code mutation or KCC rewriting in this phase.


## 7. Deterministic Root Cause & Resolution (2026-08-29)

### Proven Root Cause: Dual-Vault Split-Brain
The visibility symptom in Obsidian Bases ("0 results in Hari Ini", "Sesi Terbaru only shows older sessions") was conclusively proven to be a **dual-vault split-brain configuration boundary**:
1. Canonical AIRO / Antigravity Second Brain runs exclusively at:
   - WSL Runtime Path: `/home/egitaristorandas/AI_WORKSPACES/airo-second-brain`
   - Canonical Windows Representation: `\\wsl.localhost\Ubuntu\home\egitaristorandas\AI_WORKSPACES\airo-second-brain`
2. Desktop Obsidian was registered and opened to a separate stale Windows clone:
   - Stale Windows Clone: `C:\Users\Admin\AI_WORKSPACES\airo-second-brain` (last committed Aug 27 at `7fd70d4`).
3. Recent closed session notes (such as Session 03 and 04 from 2026-08-29) were written to canonical WSL ASB and therefore physically did not exist in the stale Windows folder.

### Executed Alignment & Invariants
- Windows Obsidian configuration (`%APPDATA%\obsidian\obsidian.json`) has been aligned to point directly to `\\wsl.localhost\Ubuntu\home\egitaristorandas\AI_WORKSPACES\airo-second-brain`.
- The stale directory `C:\Users\Admin\AI_WORKSPACES\airo-second-brain` has been **unregistered from Obsidian** while remaining physically untouched.
- `KCC` semantic closeout repair (decoupled objective vs closeout status, session_id frontmatter, and closed session bridge) remains 100% canonical and active.
- Canonical Truth Invariant:
  - `CANONICAL_ASB_RUNTIME_PATH` = `/home/egitaristorandas/AI_WORKSPACES/airo-second-brain`
  - `WINDOWS_OBSIDIAN_CANONICAL_VAULT` = `\\wsl.localhost\Ubuntu\home\egitaristorandas\AI_WORKSPACES\airo-second-brain`
  - `STALE_WINDOWS_CLONE` = `C:\Users\Admin\AI_WORKSPACES\airo-second-brain`
  - `STALE_WINDOWS_CLONE_AUTHORITY` = `NONE / NON_CANONICAL_PRESERVED_COPY`



## 8. Post-Acceptance Correction: Direct WSL UNC Obsidian Rejected (2026-08-30)

### Real UI Acceptance Outcome: False Positive in Alignment
During real Owner acceptance testing of Obsidian Windows Desktop (v1.13.7), attempting to open the WSL UNC path (`\\wsl.localhost\Ubuntu\home\egitaristorandas\AI_WORKSPACES\airo-second-brain`) resulted in Obsidian falling back to the vault chooser rather than successfully loading the vault workspace.

Therefore:
- `DIRECT_OBSIDIAN_WINDOWS_TO_WSL_VAULT_ACCEPTANCE` = `FAIL`
- `PRIOR_ALIGNMENT_PRODUCT_VERDICT` = `FALSE_POSITIVE`
- `DIRECT_WSL_OBSIDIAN_APPROACH` = `REJECTED_FOR_CURRENT_ENVIRONMENT`

### Architectural State & Invariants
1. **Config Restored Byte-for-Byte**:
   `obsidian.json` was restored exactly to `obsidian.json.airo-backup-20260829_231823` (SHA: `8f13ff3898c2cd541ef4c63f8c87f8d1bfd97be6c0306d2e57a6649073d948de`).
2. **Authority Declarations**:
   - `CANONICAL_ASB_AUTHORITY` = `WSL_ASB (/home/egitaristorandas/AI_WORKSPACES/airo-second-brain)`
   - `WINDOWS_OBSIDIAN_COPY_AUTHORITY` = `NON_CANONICAL (C:\Users\Admin\AI_WORKSPACES\airo-second-brain)`
   - `LONG_TERM_ASB_OBSIDIAN_ARCHITECTURE` = `OPEN_DECISION`
3. **Safety Guarantee**:
   Neither physical filesystem tree was mutated or synchronized during this rollback. Future designs must not repeat direct WSL UNC vault registration without formal Council review.



## 9. Owner Platform Constraint — Windows Obsidian Required (2026-08-30)

### Locked Owner Requirement
- `OWNER_OBSIDIAN_PLATFORM_REQUIREMENT` = `WINDOWS`
- `WINDOWS_OBSIDIAN_UX_MUST_BE_PRESERVED` = `YES`
- `OBSIDIAN_LINUX_WSLG` = `REJECTED_BY_OWNER`
- Future architecture proposals MUST preserve native Windows Obsidian UX. Future AI must not recommend Obsidian Linux / WSLg unless the Owner explicitly reopens that constraint.

### Environmental Invariants & Direct-WSL-UNC Rejection
- Direct Windows Obsidian access to canonical WSL repo over UNC (`\\wsl.localhost\...`) was tested and failed real UI acceptance (fallback to vault chooser).
- `DIRECT_WINDOWS_OBSIDIAN_TO_WSL_UNC` = `REJECTED_FOR_CURRENT_ENVIRONMENT`
- Prior WSL-UNC config alignment was cleanly rolled back.
- `STALE_WINDOWS_ASB_AUTHORITY` = `NON_CANONICAL` (The stale directory `C:\Users\Admin\AI_WORKSPACES\airo-second-brain` remains physically preserved for safety, but is non-canonical).
- `LONG_TERM_ASB_OBSIDIAN_ARCHITECTURE` = `OPEN_WITH_WINDOWS_OBSIDIAN_HARD_CONSTRAINT`

