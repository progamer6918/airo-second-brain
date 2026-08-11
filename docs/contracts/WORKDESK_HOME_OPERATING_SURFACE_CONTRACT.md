# WorkDesk Home Operating Surface Contract

**Project:** AIRO_WORKDESK
**Status:** ACCEPTED — CANONICAL
**Date:** 2026-08-11

## Purpose

WorkDesk Home adalah **expert-first operational cockpit dengan beginner-proof navigation**.

Home bukan generic KPI dashboard, training portal, raw repository index, atau static report.

## Information Classes

1. **Business Pulse** = latest supplied operating facts.
2. **Signals** = evidence-backed concern, opportunity, atau decision boundary.
3. **My Commitments** = explicit Owner commitment / confirmed assignment.
4. **Quick Work** = job-to-be-done routing.
5. **Knowledge Updates** = perubahan meaningful pada kemampuan brain.
6. **Explore Brain** = deep professional knowledge.
7. **Work History** = canonical closed WorkDesk sessions.

## Truth Rules

- State ≠ Signal.
- Signal ≠ Commitment.
- Program/meeting date ≠ personal Owner deadline tanpa assignment evidence.
- Semua angka/signal mempertahankan `as-of` / currentness.
- Asynchronous datasets tidak boleh dipresentasikan sebagai same-date snapshot.
- Missing evidence harus tetap visible.
- Market event tidak boleh otomatis menjadi causal proof.
- Derived priority harus dire-evaluate ketika authority/data lebih baru masuk.
- Fake/stale continuation dilarang.

## Live Session Boundary

`airo-session` active state hidup pada external runtime state.

Sampai ada deterministic sanitized session-to-Obsidian bridge, Home tidak menampilkan live-session continuation card yang dibuat manual.

## Case-Driven Delta Refresh

Setiap accepted WorkDesk delta wajib mengevaluasi apakah perlu mengubah:

- `wiki/workdesk/views/BUSINESS_PULSE.md`
- `wiki/workdesk/views/SIGNALS.md`
- `wiki/workdesk/MY_COMMITMENTS.md`
- `wiki/workdesk/updates/`

RAW_INPUT tetap harus melewati canonical input/source-authority rules sebelum dipromosikan ke Home.

## Acceptance

Backend and render acceptance have established:

- content/currentness integrity: PASS;
- semantic and downstream routing: PASS;
- commitment truth guard: PASS;
- no fabricated live continuation: PASS;
- Home information hierarchy and density: PASS;
- knowledge-update runtime surface: PASS;
- existing-vault presentation: PASS.

`HOME_V2_ACCEPTED=YES`

Canonical Git integration is complete. No additional Owner content or visual QA gate remains for Home v2.
