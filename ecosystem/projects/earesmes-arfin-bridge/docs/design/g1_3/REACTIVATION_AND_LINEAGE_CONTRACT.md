# EAB G1.3 Reactivation and Lineage Contract

- **STATUS**: `DESIGN_COMPLETE`

---

## 1. Backlog Reactivation Protocol

1. **Explicit Reactivation Required**: An expired item in `DURABLE_UNRESOLVED_BACKLOG` can only be reactivated via explicit Owner confirmation (e.g. replying `"YA"` to reactivation prompt or `/reactivate pid_101`).
2. **New Reactivation Cycle**: Reactivation creates a new pending cycle:
   - `pending_id`: `pid_102` (New pending ID for Cycle 2)
   - `predecessor_pending_id`: `pid_101` (Refers to Cycle 1)
   - `root_source_record_id`: `root_100` (Maintains immutable root lineage)
   - `reactivation_cycle`: `2` (Incremented cycle count)
   - `pending_version`: `1` (Initialized for new cycle)
   - `pending_state`: `ACTIVE`
3. **Single Active Cycle Guard**: Exactly **ONE** non-terminal cycle is permitted per root source record (`MAX_ACTIVE_CYCLES_PER_ROOT = 1`). Attempting to create multiple active cycles fails with `409 Conflict` (`ERR_MULTIPLE_ACTIVE_CYCLES_BLOCKED`).
4. **Old Prompt Rejection**: Old Telegram messages bound to Cycle 1 (`pid_101`) CANNOT target Cycle 2 (`pid_102`). Replies to Cycle 1 return `410 Gone` (`ERR_STALE_PROMPT_CYCLE_MISMATCH`).
