# AIRO Incident 2026-05-10 — Telegram false error stale context

Status: resolved.

## Summary

Telegram kept replying with an old `NameError` about `airo_transaction_persistence.py` even after local `airo-workflow`, DB, and Sheets sync were healthy.

Final resolution happened only after stale OpenClaw/agent context was purged and OpenClaw was restarted fresh.

## Main mistake

Local `airo-workflow` PASS was treated as production Telegram PASS. That was wrong.

## Root cause

OpenClaw/agent context was stale and repeated an old tool-error narrative. The OpenClaw journal did not show a fresh traceback or tool execution for the final false-error replies.

## Guardrail

Never run repeated Telegram smoke tests after a false-error reply unless:

1. Sheets timer/service are paused.
2. DB duplicate state is reconciled.
3. Local wrapper passes with temp DB.
4. Real DB count does not change during temp smoke.
5. OpenClaw env/path/session freshness is verified.
6. Only one Telegram smoke is sent.
7. DB and Sheets dry-run are checked immediately after.
