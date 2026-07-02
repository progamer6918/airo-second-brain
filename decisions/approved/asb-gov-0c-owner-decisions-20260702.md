# ASB-GOV-0C Owner Decisions Record

- **Timestamp:** 2026-07-02 22:10:53 +07:00
- **Base Head Commit:** `b739b0d817783bf3a40c146b6f445ba029b7eaf4`
- **Source Reports (Local Evidence Only - Not Committed):**
  - `/tmp/asb_gov0b_distilled_20260702_220100.md`
  - `/tmp/asb_gov0c_canonical_verification_20260702_220242.md`
  
> [!NOTE]
> The `/tmp` source reports listed above are local evidence files and are not committed as source artifacts in this patch.

---

## Mapped Owner Decisions

### ASB-D004 — Project Folder Classification

1. `ecosystem/projects/vortex-ai-skill-lab`  
   **STATUS:** `ACTIVE`

2. `ecosystem/projects/finance-bot-alternatives`  
   **STATUS:** `EXPERIMENT_REFERENCE`

3. `ecosystem/projects/earnsai-pulse-trading-local-backups`  
   **STATUS:** `ARCHIVE_LOCAL_BACKUP`

4. `ecosystem/projects/earnsai-telegram-gateway`  
   **STATUS:** `PARKED_UNTIL_VERIFIED`

5. `ecosystem/projects/earnsai-pulse-trading`  
   **STATUS:** `PARKED_HANDOVER`

6. `ecosystem/projects/github-handover`  
   **STATUS:** `ARCHIVE_HANDOVER`

---

### ASB-D001 — ASB PRD Canonical Decision

- `docs/prd/AIRO_SECOND_BRAIN_PRD_v0.5.1.md`  
  **STATUS:** `ACTIVE_CANONICAL`

- `docs/AIRO_SECOND_BRAIN_PRD_v0.4.1_NO_BRAINER.md`  
  **STATUS:** `SUPERSEDED_ARCHIVE_REFERENCE`

---

### ASB-D002 — CURRENT.md Policy

- **Target Path:** `CURRENT.md`  
  **STATUS:** `ACTIVE_BUT_MIXED_SNAPSHOT`  
  **Policy:**
  - Do not rewrite or migrate `CURRENT.md` in this task.
  - Going forward, `CURRENT.md` should become a compact snapshot.
  - Existing historical/mixed content remains pre-normalization content until a separate owner-approved normalization task.

---

### ASB-D003 — active-context Policy

- **Target Path:** `state/active-context.md`  
  **STATUS:** `LEGACY_MIXED_HISTORY_LOG`  
  **Policy:**
  - Keep as historical/context log.
  - Do not treat it as the only current execution source.
  - Do not split per project in this task.
  - Any future split must be forward-only and owner-approved.

---

## Out-of-Scope Section

The following actions are explicitly out of scope for this decision record:
- No roadmap normalization or directory refactoring.
- No PRD normalization.
- No moving or deleting of files.
- No archive cleanup.

---

## Next Safe Step
- `ASB-GOV-2` may create minimal indexes / context brief only after owner approval.

> [!IMPORTANT]
> AIRO Finance Task 10.4 remains separate and must not be executed by this decision patch.
