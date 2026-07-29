# EAB Scope-Locked Project Boot Specification

- **STATUS**: `SCOPE_LOCKED`
- **OWNER_SCOPE_LOCK**: `APPROVED`
- **CANONICAL_STATUS**: `CANONICAL`
- **IMPLEMENTATION_STATE**: `NOT_STARTED`
- **IMPLEMENTATION_AUTHORIZED**: `NO`
- **AFPD_INC_011_IMPLEMENTATION_BLOCKER**: `YES`
- **OWNER_SCOPE_LOCK**: `APPROVED`
- **PROJECT**: `EARESMES_ARFIN_CLARIFICATION_BRIDGE` (`EAB`)
- **REMOTE_MAIN_BASELINE**: `7056f66ed739deaf6717ced40ba5f2606a544524`

---

## A. Authority Hierarchy & Scope-Locked Entry

1. **ASB Root BOOT.md**: Top-level system governance and read order.
2. **ARFIN.md**: Authoritative runtime contract for AIRO Finance, account/category menus, admin precedence, Review Queue mandatory staging, and `/approval` posting plan.
3. **systems/telegram-agent-identity-contract.md**: Authoritative identity contract for Telegram bot ownership, getUpdates long-poll gateway isolation, webhook boundaries, and fail-closed security rules.
4. **AFPD Modules (`docs/afpd/`)**: Active derived module manifest (`docs/afpd/AFPD_BOOT_MANIFEST.tsv` - 16/16 active modules). Status remains `PROPOSED_NOT_CANONICAL` until explicit Owner activation.
5. **EAB Scope-Locked Specification Suite (`00` to `04`)**: Project-specific workflow, architecture, contract, and acceptance specifications.

---

## B. Scope-Locked Boot Receipt

```ini
EAB_BOOT_GUARD=PASS
AFPD_BOOT_GUARD=PASS
TELEGRAM_IDENTITY_GUARD=PASS
OWNER_SCOPE_LOCK_RECEIPT=APPROVED
EAB_PROJECT_BOOT_READ=YES
EAB_MANIFEST_VERIFIED=YES
EAB_CORE_DOCS_READ=5/5
EAB_TRACEABILITY_READ=YES
EAB_REGRESSION_GUARDS_READ=YES
LATEST_PROJECT_PROGRESS_READ_LAST=YES
CURRENT_PROJECT_HANDOFF_READ_LAST=YES
LATEST_GIT_RUNTIME_EVIDENCE_RESOLVED=YES
```

- **ROADMAP_POINTER**: `ecosystem/projects/earesmes-arfin-bridge/docs/05_EXECUTION_ROADMAP.md`
- **TRACKER_POINTER**: `ecosystem/projects/earesmes-arfin-bridge/docs/MILESTONE_TRACKER.tsv`
