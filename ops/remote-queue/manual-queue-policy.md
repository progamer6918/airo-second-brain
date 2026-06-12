# Manual Remote Queue Policy

This policy governs the processing of the manual remote queue (`inbox/remote/`) to ensure no automated semantic promotion occurs without explicit owner approval.

## Pipeline Flow

1. **Queue Source**:
   Files originating from `inbox/remote/manual-sync-queue.md` or any `inbox/remote/*.md`.
2. **Ingestion**:
   The runtime processor (`process-remote-queue.sh`) reads these files.
3. **Routing**:
   - Items are routed to `events/raw/` for raw logs/events.
   - Items are routed to `distill/proposals/` for tasks or changes.
4. **State**:
   These files enter an `awaiting_owner_review` state implicitly by existing in the `proposals/` or `raw/` directories.
5. **Strict Guardrail**:
   - **No direct canonical promotion.** 
   - Low-risk progress logs may become raw events.
   - Any semantic decision, task finalization, architecture change, or action on a dirty repository requires explicit owner approval. The queue processor will NEVER automatically patch `CURRENT.md` or commit to semantic branches directly.
