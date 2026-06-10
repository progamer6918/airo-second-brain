# AIRO Sync Operating Rule — 2026-06-10 23:51

## Source
- Consumer: ChatGPT Project AIRO
- Scope: current session instruction + latest AIRO Sync bootstrap audit output
- Access limitation: Tidak punya akses langsung ke semua sesi lain; hanya bisa distill dari konteks yang tersedia di chat/project ini atau output yang dibawa owner dari AI lain.
- Raw transcript stored: no
- Secrets/tokens/API keys/OAuth/OTP/full email body stored: no

## Owner-Confirmed Rule
- owner-confirmed: AIRO Sync means the active consumer should behave as an AIRO ecosystem operator, not as a separate assistant.
- owner-confirmed: meaningful decisions, progress, blockers, discussion outcomes, project state, and next actions should be distilled and pushed to AIRO Second Brain.
- owner-confirmed: this applies to the current chat and to other AI/agent sessions only when their context is available, pasted, or written by that consumer.
- verified: AIRO Sync does not authorize raw transcript dumping.
- verified: AIRO Sync does not authorize secret capture.
- verified: AIRO Sync does not mean the consumer can magically access unavailable sessions.

## Practical Cadence
- verified: after a meaningful task segment, produce a Second Brain closeout.
- verified: for small but important decisions, append a compact state/decision note.
- verified: for cross-AI work, each AI consumer should either:
  1. write its own closeout to AIRO Second Brain, or
  2. provide safe distilled output that another operator can push.
- verified: do not push every casual message; push meaningful deltas only.
- verified: preserve labels such as verified, owner-confirmed, assumed, and unknown.

## Current AIRO Finance State Bound to This Rule
- verified: Task 7 done.
- verified: Task 8 done and must not be repeated.
- verified: Task 9 not started.
- verified: Task 10 optional.
- verified: mandatory remaining count is 4.
- verified: remaining 4 includes Task 9 and excludes optional Task 10.
- verified: AIRO Finance Task 8 evidence:
  - FINAL_RESULT=PASS_TASK8_COMPLETE_SISA_WAJIB_4
  - Commit: d9a3e46 fix(airo-finance): route debt approval to hutang projection
  - Production final clean: @287

## Constraint
- verified: AIRO Finance execution must use canonical repo evidence from `/home/egitaristorandas/vortex-ai-skill-lab`, not Second Brain alone.
- verified: do not mutate Gmail.
- verified: do not recreate Transactions.
- verified: do not revive Finance Events as source-of-truth.
- verified: do not re-approve Review Queue row 10.
- verified: do not commit unrelated local files.
