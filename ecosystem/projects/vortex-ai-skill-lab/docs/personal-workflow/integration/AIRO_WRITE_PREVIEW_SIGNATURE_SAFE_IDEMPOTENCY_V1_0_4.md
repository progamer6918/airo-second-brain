# AIRO Write Preview Signature-safe Idempotency v1.0.4

Status: IMPLEMENTED / VERIFIED
Date: 2026-05-10

## Trigger

Post-write idempotency verification failed because earlier patches assumed the wrong internal shape:

1. existing_by_tab value was sometimes a string, not dict.
2. decide_operation must return PreviewDecision, not dict.
3. PreviewDecision required fields not included by the patch.

## Fix

`decide_operation()` now:

- preserves PreviewDecision object return type
- builds PreviewDecision using its dataclass fields
- handles existing values as dict, string, or empty string
- treats existing key with empty sync_hash as skip_duplicate

## Verification

write_preview confirmed:

- transactions:trx_29f527902571 -> skip_duplicate
- transactions:trx_41a84be31c7e -> skip_duplicate
- trx_41a84be31c7e -> skip_duplicate
- REAL_WRITE_CANDIDATE_COUNT=0
- google_write_performed=false
- credentials_read=false
