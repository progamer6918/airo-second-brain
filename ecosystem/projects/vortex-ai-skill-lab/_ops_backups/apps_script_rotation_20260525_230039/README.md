# AIRO Apps Script Project Rotation Backup

- Timestamp: 2026-05-25T23:00:49+07:00
- Repo: /home/egitaristorandas/vortex-ai-skill-lab
- Old clasp dir: apps-script-live
- New clasp dir prepared: apps-script-prod-v2
- Backup root: /home/egitaristorandas/vortex-ai-skill-lab/_ops_backups/apps_script_rotation_20260525_230039
- Reason: old Apps Script project reached 200 immutable versions
- Sprint: Sprint 4 Finance Events remains active
- Important: this rotates Apps Script project/version container only, not repo architecture and not Google Sheet

## Current git head
c0d57f2 fix(airo-finance): surface Finance Events emission failures
1a1e1ed docs(airo-finance): record Sprint 4 post-deploy live blockers
72afd38 docs(airo-finance): record Sprint 4 cash Finance Events production update
86ca693 fix(airo-finance): emit Finance Events for cash Account Ledger writes
af13a70 docs(airo-finance): correct Sprint 4 schema verify status

## Next manual-sensitive items
- Create new Apps Script project with clasp in apps-script-prod-v2
- Set Script Properties in new project: BOT_TOKEN and SPREADSHEET_ID
- Deploy new Web App
- Update Cloudflare Worker APPS_SCRIPT_URL to new Web App URL
- Keep old project until new smoke passes
