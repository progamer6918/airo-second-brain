# EAB Stable Pending Identity & Lineage Contract (`pending_id`) — Final V3

- **SPECIFICATION_ID**: `EAB-SPEC-PID-003`
- **STATUS**: `FINAL_CORRECTION_COMPLETE`
- **PREREQUISITE_MAPPING**: `PREREQ-003`
- **MILESTONE**: `M2` (`EAB_G1_1`)

---

## 1. Core Identity & Reactivation Lineage Invariants

1. **Canonical Target Identity**:
   - `pending_id` is the **sole canonical, immutable target identity** for a specific pending clarification cycle in Arfin.
   - Format: `pid_<timestamp_ms>_<8_char_hex_nonce>` (e.g., `pid_1772184000_a3f89e2b`).
   - Generation: Generated exactly once by Arfin backend upon initiating an active pending cycle.

2. **Reactivation Lineage Data Structure**:
   - Every pending record contains explicit reactivation lineage attributes:
     - `root_source_record_id`: Immutable origin transaction GUID/ID in Arfin ledger.
     - `predecessor_pending_id`: Null for initial cycle; points to parent `EXPIRED_UNRESOLVED` `pending_id` on reactivation.
     - `reactivation_cycle`: Monotonic integer starting at `1` (initial cycle) and incrementing on each prompt reactivation (`2`, `3`, etc.).
   - **One Non-Terminal Cycle Rule**: Exactly ONE non-terminal pending cycle (`ACTIVE` or `SUBMITTED_STAGED`) is permitted per `root_source_record_id` at any time (`ONE_NON_TERMINAL_CYCLE_PER_SOURCE_RECORD = YES`).

3. **Lifecycle & Terminal Boundary**:
   - `pending_id` is immutable for its cycle. Once terminal (`RESOLVED`, `EXPIRED_UNRESOLVED`, `IGNORED`), it cannot be modified or directly reopened.
   - Reactivating an expired prompt creates a **NEW `pending_id`** with `predecessor_pending_id` pointing to the expired `pending_id` and `reactivation_cycle = previous + 1`.
