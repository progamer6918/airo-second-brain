# AFPD Contradiction Resolution Plan

The following plans resolve the five detected contradictions in documentation and runtime behavior for AIRO Finance:

## 1. AUTHORITY_FINAL_KITAB_VS_ARFIN (CONFIRMED_SPLIT_AUTHORITY)
- **Problem**: Both `AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md` and `ARFIN.md` claim primary project guidance/authority.
- **Resolution Plan**:
  - `FINAL_KITAB` is designated as the primary authority for durable architecture and developer governance rules.
  - `ARFIN.md` is designated as the primary authority for reconciled active Arfin runtime behavior rules.
  - `AFPD.md` is established as the future sole documentation entrypoint and authority resolver.
  - This structure will be formally codified in `docs/afpd/02_ARCHITECTURE_AND_GOVERNANCE.md` (governance rules) and `docs/afpd/03_ARFIN_RUNTIME_CONTRACT.md` (runtime rules).

## 2. EMAIL_DEFAULT_OFF_VS_ACTIVE_RUNTIME (SUPERSESSION_REQUIRED)
- **Problem**: Final Kitab describes email ingestion as default OFF/optional, while v375 runtime has an active poller.
- **Resolution Plan**:
  - Preserve the "default OFF" status in documentation as historical context and default-policy design.
  - Formally record the current active Gmail poller in `docs/afpd/04_RUNTIME_TOPOLOGY.md` as active production runtime state, not architecture default.
  - Create a clear distinction between `policy_default` (default OFF) and `production_current_state` (poller active) within `docs/afpd/03_ARFIN_RUNTIME_CONTRACT.md`.

## 3. REVIEW_QUEUE_FALLBACK_VS_APPROVAL_STAGING (SEMANTIC_CONTRACT_MERGE_REQUIRED)
- **Problem**: Final Kitab describes Review Queue as a fallback for failed clarifications, while ARFIN stages all email transactions for explicit approval.
- **Resolution Plan**:
  - Formally define two explicit concepts in `docs/afpd/03_ARFIN_RUNTIME_CONTRACT.md`:
    1. **Manual-Review Fallback**: Rows written to Review Queue because parser confidence is low, category is missing, or clarification timed out.
    2. **Approval Staging**: Rows written to Review Queue by design (e.g., email-sourced transactions) to wait for explicit manual Owner approval before writing to the Account Ledger.
  - Both concepts use the Review Queue sheet but write distinct status and reason codes (`review_status` / `fallback_reason`) to distinguish staging from fallbacks.

## 4. SCRIPT_TIMEZONE_VS_POLLER_TIMEZONE (NORMALIZATION_REQUIRED)
- **Problem**: `appsscript.json` specifies `Asia/Bangkok` while `AIRO_Finance_Multitab_Final_v1.js` explicitly parses date in `Asia/Jakarta`.
- **Resolution Plan**:
  - Define `Asia/Jakarta` as the intended business timezone in the data and runtime contract (`docs/afpd/03_ARFIN_RUNTIME_CONTRACT.md`).
  - Keep the manifest timezone as a normalization anomaly under legacy config in `docs/afpd/07_OPERATIONS_DEPLOYMENT_TRIGGERS.md` to prevent deployment mismatch risks.
  - Do not modify `appsscript.json` timezone during Phase 2.

## 5. LEGACY_ALPHA_UX_VS_NUMERIC_UX (DEPRECATION_MAP_REQUIRED)
- **Problem**: Source code contains legacy A/B/C/D/E UX handler paths while ARFIN mandates numeric `1..N` options.
- **Resolution Plan**:
  - Classify the numeric `1..N` (plus `0` Other / Review) prompt format as the canonical Arfin UX contract.
  - Map legacy letter UX patterns in `docs/afpd/03_ARFIN_RUNTIME_CONTRACT.md` as deprecated or test-only fallbacks.
  - Retain legacy code handlers in the source file for backward compatibility during Phase 2; no source deletion is performed.
