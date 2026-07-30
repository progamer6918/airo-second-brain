# EAB G1.4 Implementation Change Plan

- **SYSTEM**: Earesmes-Arfin Clarification Bridge (`EAB`)
- **MILESTONE**: `M5` / Gate `EAB_G1_4`
- **STATUS**: `REMEDIATED_DESIGN_COMPLETE`

---

## 1. Implementation Principles and Boundaries

1. **Strict Milestone Isolation**: Implementation MUST NOT begin until explicit Owner authorization in Gate `EAB_G1_6`.
2. **Authorization Candidacy**: With all G1.4 readiness checks PASS, the package is `M6_AUTHORIZATION_CANDIDATE = YES_PENDING_EXACT_OWNER_APPROVAL`. Source implementation remains `IMPLEMENTATION_ALLOWED = NO`.
3. **Modular Change Units**: Implementation is partitioned into 12 small, independently verifiable units (CU-01 through CU-12).
4. **No Mixed Mutations**: No single change unit may combine source code, runtime, deployment, or workbook mutations under one approval.
5. **Primary UI & Authority Safeguards**:
   - `PRIMARY_INTERFACE = EARESMES`
   - `FINANCE_AUTHORITY = ARFIN`
   - `DIRECT_ARFIN_FALLBACK = RETAIN`
   - `REVIEW_QUEUE_REQUIRED = YES`
   - `OWNER_APPROVAL_REQUIRED = YES`
   - `EARESMES_LEDGER_WRITE = FORBIDDEN`
