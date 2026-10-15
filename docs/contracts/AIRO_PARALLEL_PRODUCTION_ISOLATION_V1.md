---
status: OWNER_DECISION_BOUND_INACTIVE_UNTIL_APPROVED
scope: isolated implementation and verification only
production_approval: EXPLICIT_SOURCE_BOUND_OWNER_DECISION_REQUIRED
---

# Parallel production session isolation V1 — exact proposal

This document is a candidate for Owner review. It does not amend current canonical
governance, grant production authority, or activate birthday recovery.

## Decision requested

Approve a second, explicitly identified parallel-session registry in a dedicated
checkout with independent Git metadata, alongside the untouched legacy EARNSART
runtime. Keep one main Owner objective per session. Do not migrate, checkpoint,
close, reset, or write to the existing EARNSART session or its artifacts.

The existing environment-variable state override remains a synthetic-test tool;
it is not how this production isolation is implemented or authorized.

## Runtime and identity

- Opt-in interface: `python3 bin/airo-session parallel --mode <candidate|production>`.
  All existing unqualified lifecycle commands retain their old implementation.
- Explicit session UUID, project ID and objective ID are mandatory. Start also
  binds the objective text and human title. A session cannot be rebound to a
  different identity, and the same objective cannot acquire a second owner.
- Runtime authority: `.airo-parallel/<mode>/sessions.sqlite3` in the approved
  independent checkout. Candidate and production databases are distinct.
- Each objective has an independent session row. Events form an append-only
  SQLite ledger with unique UUIDs and foreign keys to their owning sessions.
  State and its event are committed in one `BEGIN IMMEDIATE` transaction with
  `synchronous=FULL`, WAL journaling, and bounded SQLite busy waiting.
- Stable event IDs distinguish an explicit retry from a new legitimate event.
  A retry with the same ID/payload is acknowledged without another record;
  changing the identity or payload for that ID fails closed. Identical summary
  text with a different event ID remains a separate event.
- Capture uses explicit parallel selectors. A malformed or rejected parallel
  request never falls back to legacy capture, state, logs or event ledger.
- Semantic fields (Owner request, position, progress, blocker, next action,
  phase, consumer and source) are preserved. A persisted active blocker cannot
  be hidden by passing an empty blocker list at closeout.

## Derived artifacts and crash handling

- A lock file per session serializes its mutations and projection writes.
- Per-session projections and UUID-named closeout notes live under the owning
  mode's `projections/` and `worklogs/`; no global idle reset or daily generator
  runs. Legacy active-session, current-work and daily worklog files are untouched.
- Projections use temporary-file fsync, atomic replacement and directory fsync.
  SQLite remains authoritative. A crash after commit can leave a stale derived
  view, but retry with the same event ID or explicit reconciliation repairs it
  without duplicating the committed event. Failure is reported, never hidden.
- Close requires explicit DoD satisfaction and a canonical verdict of BERHASIL /
  CAN_ADVANCE=YES. Missing evidence, failures, blockers or limitations preserve
  the active session. Interrupted close is retried using the original event ID.
- Any aggregate HOME, active-session or daily view requires a separately reviewed
  single-writer integration. It is excluded from this EARNSART-protected rollout.

## Authorization and rollout boundary

The Owner instruction authorizes engineering in candidate mode only. Candidate
fixtures exercise the same transactional lifecycle but are not real production
sessions, real birthday recovery, or authorization to deploy.

Production startup fails before creating runtime resources unless all of these
exist in the independently approved checkout:

1. `.airo-parallel/authorization.json`: exact resolved workspace, mode production,
   schema 1, and the protected legacy repository path. Writable and protected
   repositories must be disjoint; linked-worktree metadata and alternate Git
   object stores are rejected.
2. Approved final contract at
   `docs/contracts/AIRO_PARALLEL_PRODUCTION_ISOLATION_V1.md`.
3. `.airo-parallel/owner-approval.json`: OWNER_APPROVED status, documented Owner
   decision reference, scope PARALLEL_SESSION_ENGINE_ONLY, exact workspace,
   SHA256 of the approved contract, and exact executable-source fingerprint.
   The authorization descriptor must contain the same contract hash.

An operator-created JSON file is NOT itself proof of Owner approval. Its decision
reference must point to an actual approved exact artifact under the KCC two-stage
process. No approval file is created by this task. A new source revision requires
fresh source-bound approval; candidate state is never promoted into production.

This design authorizes only one registered parallel coordinator checkout per
approved deployment. Another arbitrary clone is not an independent production
namespace by default. Existing ASB project and secret-ownership guards still apply
before any business/runtime action; the session engine does not grant those rights.

## Git and deployment scope

- The candidate clone has its own `.git`, objects, refs, index and working tree.
- Source/draft diffs may be prepared and exact-path staged only in that clone.
  No production staging, fetch, merge, ref update, commit or push is included.
- Future production activation uses a new independent checkout, never installation
  over files currently used by EARNSART. Every command executes from that approved
  checkout; private runtime directories are excluded from Git.
- Inherited Git directory/index/worktree/object-routing overrides are rejected
  before opening the candidate or production session store.
- Independent Git metadata does not grant shared-service or file ownership.
  Canonical publication remains an explicitly approved, serialized promotion.
- The birthday workflow has a later deployment gate for its own bot, dataset,
  private credentials, state and dedicated scheduler. No isolation test counts as
  a Telegram smoke test or scheduler-persistence proof.

## Required acceptance before production activation

A. Two independently identified objectives coexist and repeat start is stable.
B. Wrong session/project/objective and malformed capture routes fail closed.
C. Concurrent events and explicit retries have exact event counts and unique IDs.
D. Closing/reconciling one session leaves the other active and its view unchanged.
E. Legacy behavior is compared before/after on canonical and copied live versions.
F. Real EARNSART state, ledger, projections, worklogs and Git metadata remain unchanged.
G. Process termination before commit rolls back; termination after commit and
   interrupted close/replacement recover without duplicate events or partial views.
H. Canonical governance is unchanged; exact proposed amendments and rollout diff
   are reviewable; production startup without approval is rejected.

## Two-stage Owner review

Stage 1: the current task authorizes this isolated proposal/implementation work.
Stage 2: Owner reviews the exact source patch, governance amendment patch, source
fingerprint, limitations and regression receipt. Approval must specify canonical
publication and independent production rollout scope explicitly. Until then,
PRODUCTION_GOVERNANCE_APPROVED=NO and PRODUCTION_ISOLATION_ACTIVE=NO.
