# EAB Human-Readable Short Reference & Prompt Context Contract (`short_ref`) — Final V3

- **SPECIFICATION_ID**: `EAB-SPEC-REF-003`
- **STATUS**: `FINAL_CORRECTION_COMPLETE`
- **PREREQUISITE_MAPPING**: `PREREQ-003`
- **MILESTONE**: `M2` (`EAB_G1_1`)

---

## 1. Format & Scope Rules

1. **Format Specification**:
   - `short_ref` format is **EXACTLY `AF-` followed by 4 decimal digits** (`^AF-[0-9]{4}$`, e.g., `AF-1042`).

2. **Non-Terminal Uniqueness Scope**:
   - `short_ref` must be **unique across all non-terminal records** (`ACTIVE`, `SUBMITTED_STAGED`) per Owner (`SHORT_REF_NON_TERMINAL_UNIQUENESS = UNIQUE_PER_OWNER_NON_TERMINAL`).

## 2. Canonical 6-Field Prompt Context Binding

`short_ref` is durably bound to a **canonical 6-field prompt context tuple**:
```text
(prompt_id, short_ref, pending_id, expected_pending_version, owner_chat_id, telegram_message_id)
```

1. `prompt_id`: Canonical UUID generated per prompt message session.
2. `short_ref`: Human shortcut (`AF-1042`).
3. `pending_id`: Canonical item target identity (`pid_...`).
4. `expected_pending_version`: Monotonic expected version (`v1`).
5. `owner_chat_id`: Telegram owner chat ID allowlist.
6. `telegram_message_id`: Telegram prompt message ID.

## 3. Stale Prompt Message Guard

- Old Telegram prompt messages or unbound free-form references must **NEVER silently resolve to a different pending cycle** (`SHORT_REF_STALE_REUSE_GUARD = PASS`).
- When a user replies to a Telegram message, the bridge extracts the bound 6-field tuple.
- If `pending_id` is terminal, or if `short_ref` in Arfin storage currently points to a different `pending_id` (from a newer cycle), the request fails closed with `STALE_PROMPT_REFERENCE_MISMATCH` (HTTP 410/404). Silent resolution against a new cycle is strictly forbidden.
