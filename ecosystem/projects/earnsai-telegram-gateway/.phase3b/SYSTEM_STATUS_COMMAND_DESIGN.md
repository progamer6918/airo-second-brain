# Phase 3B System Status Command

Goal: add safe Bubu status command without breaking capture-by-default.

Commands:
- /status
- /system_status
- /system-status

Patch point:
- after rawText validation
- before autoMergeBuffers logic

MVP behavior:
- reply with system status
- do not capture command to Notion
- do not call Notion
- do not read secrets
- do not change routing
- do not change auto-merge

Validation:
- tsc
- wrangler dry-run
- live /status test
- normal capture test
- auto-merge regression test
