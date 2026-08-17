# EAB M16 — Proactive Front Desk Contract

status: IMPLEMENTATION_CANDIDATE
gate: EAB_PFD_G1
phase1_status: COMPLETE_UNCHANGED
m15_status: DEFERRED_UNCHANGED

## Product intent

Owner must not need to poll Arfin for clarification work.

When an unresolved Arfin clarification exists while the local Earesmes worker
is online, Earesmes proactively contacts Owner. Owner answers in Earesmes.
Arfin remains the authoritative finance backend.

## Runtime topology

- Reuse `airo-hermes-worker.service`.
- Reuse existing Earesmes Telegram bot.
- Earesmes Gateway remains sole `getUpdates` consumer.
- Worker uses signed EAB `LIST_PENDING`, `GET_PENDING`,
  `SUBMIT_CLARIFICATION` and outbound Telegram `sendMessage`.
- No new bot, webhook, token, daemon or second Telegram poller.

## Proactive delivery contract

Default interval: 60 seconds.

State:
`~/.local/state/airo-second-brain/hermes-bridge/eab-proactive-frontdesk.json`

Delivery identity:
`pending_id + pending_version`.

A successful Telegram send records delivery.
A failed send does not record delivery.
The same unchanged pending/version is not sent twice.
A changed version is eligible for a new prompt.
State is persisted atomically.

## Reply contract

For a single active proactive prompt, Owner may answer naturally without
typing an `AF-XXXX` reference.

Before submit:
1. `EAB_GET_PENDING`
2. exact `pending_id` match
3. exact current `pending_version` match

Stale reply fails closed.

`EAB_SUBMIT_CLARIFICATION` calls the existing pending-clarification
resolver directly through a bounded EAB wrapper. It MUST NOT delegate to full
`doPost()`, special/admin dispatch, `reprocessClarifiedTelegramText_()`, or
`writeRouted_()`.

Resolver Telegram replies are captured and returned to Earesmes. A completed
clarification that returns `resolved_text` is staged directly to Review Queue
with `appendByHeader_()` plus queue-id readback. A failed staging attempt
restores the exact pending snapshot. Unsupported reprocessing pending types
fail closed and remain pending.

## Pending metadata

New saved pending clarification records receive:
- stable `pending_id`
- stable deterministic `short_ref`
- monotonic `pending_version`

Legacy pending remains readable with projection defaults.

## Safety

- Arfin remains finance authority.
- Earesmes performs no direct Account Ledger write.
- No approval capability is added to Earesmes.
- Existing Phase 1 Review Queue and `/approval` invariants remain unchanged.
- M15 Cloud Inbox remains deferred.
- Local proactive operation is available only while the local worker is online.

## Acceptance

REQ-015:
automatic Earesmes prompt without Owner polling.

REQ-016:
natural Owner reply uses canonical pending identity/version.

REQ-017:
durable idempotent fail-closed notification state.

Real Owner acceptance is required before M16 can become DONE.


## M16 bounded semantic-security repair

Pre-deploy review of candidate `4b20be23c9963361e431c08991153c279178eba2`
proved that delegating EAB clarification to full `doPost()` was unsafe:
special-command routing and transitive finance writes were reachable while
the EAB response unconditionally claimed `direct_ledger_write=false`.

The repaired candidate therefore enforces:

- no full `doPost()` delegation;
- no EAB `writeRouted_()` path;
- direct pending resolver only;
- unsupported reprocessing pending type fails closed;
- EAB retry execution cannot reach legacy automatic write fallback;
- completed `resolved_text` stages directly to Review Queue;
- Review Queue row must retain `write_policy=staging`, pending status,
  empty ledger/event/approval links, and verified queue-id readback;
- production remains unchanged until a separate activation gate passes.
