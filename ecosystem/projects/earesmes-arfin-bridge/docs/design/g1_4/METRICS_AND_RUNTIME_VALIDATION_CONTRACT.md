# EAB G1.4 Metrics and Runtime Validation Contract

- **STATUS**: `REMEDIATED_R5_DESIGN_COMPLETE`

---

## 1. Canonical Implementation Constraints

The following values are canonically locked architectural constraints and MUST NOT be presented as proposed defaults:

1. `EAB_CLOCK_SKEW_TOLERANCE_SEC` = 60 seconds (`CANONICAL_SOURCE = G1_2_SCOPE_LOCK`) [TR-026]
2. `KEY_ROTATION_GRACE_WINDOW_HOURS` = 24 hours (`CANONICAL_SOURCE = G1_2_SCOPE_LOCK`) [TR-027]
3. `EAB_PROMPT_TTL_HOURS` = 24 hours (`CANONICAL_SOURCE = G1_3_SCOPE_LOCK`) [TR-028]
4. `MAX_ACTIVE_CYCLES_PER_ROOT` = 1 active cycle (`CANONICAL_SOURCE = G1_3_SCOPE_LOCK`) [TR-011]

---

## 2. Proposed Defaults Requiring M11/M12 Validation

The following operational values are proposed defaults that MUST be validated during Milestone `M11` (Integration Dry Run) and `M12` (Live Canary):

1. `EAB_ADAPTER_TIMEOUT_MS` = 8000 ms [TR-023]
2. `EAB_MAX_RETRY_COUNT` = 2 retries [TR-024]
3. `EAB_REQUEST_REPLAY_WINDOW_SEC` = 300 seconds [TR-025]
4. `EAB_NONCE_RETENTION_SEC` = 600 seconds [TR-029]
5. `EAB_RECEIPT_RETENTION_DAYS` = 30 days [TR-030]
6. `EAB_SERVICE_SECRET_ROTATION_DAYS` = 90 days [TR-021]
7. `EAB_AUDIT_KEY_ROTATION_DAYS` = 180 days [TR-022]
8. Operational error rates, rejection spikes, crash loop thresholds [TR-002, TR-003, TR-005 to TR-010, TR-012 to TR-020]
