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

## 8. Output Transport Evidence Invariant

- Clipboard delivery is output transport evidence, NOT task-completion evidence.
- Command exit code 0 does not prove receipt delivery.
- Verified read-back (`CLIPBOARD_READBACK=PASS`) and complete content match (`CLIPBOARD_CONTENT_HASH=PASS`) are mandatory **unless the OSC52 terminal delivery exception applies** (see § 8.1 below).
- Do not confuse clipboard delivery success with task verdict BERHASIL or CAN_ADVANCE.

### 8.1 OSC52 Terminal Delivery Exception

> `OSC52_SEND_SUCCESS_DOES_NOT_REQUIRE_READBACK=true`

**Applies to**: VPS Terminal OSC52 adapter; AGY VPS parent TTY OSC52 adapter.

For **OSC52-based delivery paths**, clipboard readback is structurally unavailable — the terminal emulator absorbs the escape sequence and no in-process read path exists. The following substitutions are accepted:

| Field | Standard Requirement | OSC52 Accepted Value |
|---|---|---|
| `CLIPBOARD_READBACK` | `PASS` | `NOT_AVAILABLE` |
| `CLIPBOARD_CONTENT_HASH` | `PASS` | `NOT_AVAILABLE` |
| `COPIED_TO_CLIPBOARD` | `YES` (via readback) | `YES` (via confirmed OSC52 WRITE exit 0) |
| `DELIVERY_STATUS` | verified match | `OSC52_WRITE_SUCCESS_READBACK_NOT_AVAILABLE` |

This exception does **NOT** relax evidence requirements for the LOCAL PC/WSL clipboard adapter.

**Cross-reference**: [`AIRO_TERMINAL_RECEIPT_DELIVERY_CONTRACT`](./AIRO_TERMINAL_RECEIPT_DELIVERY_CONTRACT.md) — canonical authority for OSC52 delivery rules and the `OSC52_SEND_SUCCESS_DOES_NOT_REQUIRE_READBACK` flag.  
**KCC SOP cross-reference**: [`AIRO_KNOWLEDGE_CONTINUITY_SOP`](./AIRO_KNOWLEDGE_CONTINUITY_SOP.md) § 3.1 — mirrors this exception for session closeout transport.

