# AIRO Phase 2G Local Dashboard and Approval Queue

Generated: 2026-05-08T20:20:53+07:00
Branch: main
Base commit: 576d8ea

Status:
PASS

Scope:
Phase 2G adds a local approval queue and local dashboard for Airo Personal Workflow.

Script:
scripts/personal-workflow/airo_approval_queue.py

Local queue DB:
/home/egitaristorandas/.local/share/airo-personal-workflow/approval_queue.sqlite

Local dashboard:
/home/egitaristorandas/.local/share/airo-personal-workflow/dashboard/index.html

Capabilities:
- add approval item
- list pending or historical items
- approve item
- reject item
- generate local HTML dashboard
- return pure JSON for CLI operations
- store queue state locally in SQLite

Important boundary:
The approval queue tracks approval state only.
It does not execute Google writes, OpenClaw patches, service restarts, browser actions, finance deletions, or trading actions.

Example commands:
python3 scripts/personal-workflow/airo_approval_queue.py add --action-type google_sheets_write --title "Approve Sheets append preview" --payload payload.json --risk-level medium
python3 scripts/personal-workflow/airo_approval_queue.py list --status pending
python3 scripts/personal-workflow/airo_approval_queue.py approve --id 1 --note "approved after review"
python3 scripts/personal-workflow/airo_approval_queue.py reject --id 1 --note "rejected"
python3 scripts/personal-workflow/airo_approval_queue.py dashboard

Safety:
- no secret read
- no .env read
- no browser profile access
- no Google OAuth
- no Google Workspace write
- no service restart
- no OpenClaw core patch
- no EarnsAI runtime access
- no live trading
- no hard delete
- no queued action execution

Validation:
PASS - inside git repo
PASS - branch main
PASS - python3 available
PASS - approval queue script created
PASS - queue add valid JSON id=1
PASS - queue list valid JSON
PASS - queue approve valid JSON
PASS - dashboard generated
PASS - local dashboard generated: /home/egitaristorandas/.local/share/airo-personal-workflow/dashboard/index.html

Phase 2 completion:
Phase 2A health check: DONE
Phase 2B OpenClaw/Airo routing: DONE
Phase 2C SQLite cleanup/reconcile: DONE
Phase 2D Google OAuth bootstrap guide: DONE
Phase 2E Google Sheets approval gate: DONE
Phase 2F attachment intake: DONE
Phase 2G local dashboard and approval queue: DONE
