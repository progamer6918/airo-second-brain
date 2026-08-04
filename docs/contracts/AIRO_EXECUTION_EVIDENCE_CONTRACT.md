# AIRO Execution Evidence Contract

- **Status:** `ACTIVE_CONTRACT`
- **Version:** `1.0.0`
- **Scope:** `ASB_GLOBAL`

---

## 1. Purpose

This contract defines evidence classification, required evidence matching, and execution assurance rules for AIRO Second Brain v0.6.

---

## 2. Evidence Classes

1. `LIVE_RUNTIME`: Verified execution on real live infrastructure (e.g. HTTP 200 JSON from live Apps Script, verified process state).
2. `SIMULATION`: Execution in dry-run, mock, or local test harness.
3. `VERIFIED_COMMIT`: Git commit object verified in local repository.
4. `VERIFIED_REMOTE_PARITY`: Verification that local commit SHA matches remote HEAD.
5. `MACHINE_TELEMETRY`: Raw event recorded in `events/raw/events.ndjson`.

---

## 3. Invariant Matching Rules

- A `SIMULATION` evidence item MUST NEVER satisfy a requirement specifying `LIVE_RUNTIME` evidence.
- If required evidence is `LIVE_RUNTIME` and actual evidence is `SIMULATION`, the validator MUST compute `BELUM_TERBUKTI` and `can_advance: NO`.
