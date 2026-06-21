# AIRO Telegram Production Deployment Guardrail

## Rule

Local `airo-workflow` PASS is not production Telegram PASS.

## Required checklist before Telegram smoke

1. Pause write-capable automation.
2. Run local wrapper with temp DB.
3. Confirm real DB row count does not change.
4. Confirm OpenClaw service env has `AIRO_REPO_DIR` and `PYTHONPATH`.
5. Confirm OpenClaw is not using stale session/context.
6. Send only one Telegram smoke.
7. Check DB active rows.
8. Check live Sheets dry-run has zero write candidates.

## If Telegram repeats an old error

Do not patch random Python/DB/Sheet layers again.

First suspect stale OpenClaw agent context if journal has no fresh traceback or tool execution.
