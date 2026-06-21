# AIRO Carryover Prompt — 2026-05-10

Paste this into the next chat.

## Context

We are working in:

`~/vortex-ai-skill-lab`

Do not touch these untracked restricted dirs:

- `EarnsAI`
- `runtime`
- `trading`

## Current stable state

AIRO Finance Capture v1.1 is operationally stable.

Latest important commits:

- `61a39a3 fix: add unique AIRO sync status trigger`
- `766bd5a feat: add AIRO workflow status command`
- `f60ef90 chore: add simple AIRO status command`
- `5fe4f86 feat: polish AIRO duplicate transaction reply`
- `99468ca chore: add AIRO production health check`
- `884f212 feat: add AIRO finance contract v1.1`
- `0d55c7f chore: add AIRO finance production regression`
- `f23ba60 docs: add AIRO Telegram stale-context postmortem`
- `a9070cb fix: preserve Airo gateway persist action`
- `485d3d4 fix: update Airo asset rows by section range`

## Verified PASS

- `scripts/personal-workflow/airo_status.sh`
- `scripts/personal-workflow/airo_finance_prod_regression.sh`
- OpenClaw gateway active
- Sheets timer active
- real DB canonical row active count = 1 for `nabung 5000 ke blu`
- live Sheets dry-run write candidates = 0
- `airo-workflow "cek airosync"` returns `intent=airo_status`
- duplicate transaction reply is polished
- stale OpenClaw context incident documented

## Important lessons / rules

Do not treat local `airo-workflow` PASS as production Telegram PASS.

Before Telegram smoke:

1. pause write-capable automation if touching DB/sync logic
2. use temp DB wrapper test first
3. confirm real DB count does not change
4. confirm OpenClaw env/path/session freshness
5. send only one Telegram smoke
6. immediately verify DB + Sheets dry-run

If Telegram repeats an old tool error but OpenClaw journal has no fresh traceback/tool execution, suspect stale OpenClaw context first.

## Current commands

Health check:

`cd ~/vortex-ai-skill-lab && scripts/personal-workflow/airo_status.sh`

Workflow status:

`airo-workflow "cek airosync"`

Telegram status trigger:

`cek airosync`

## Next recommended work

Proceed only with small scoped work:

1. compact Telegram status reply if still verbose
2. add Finance Contract v1.2 test matrix
3. add dashboard/status UX
4. avoid core DB/Sheets changes unless regression requires it
