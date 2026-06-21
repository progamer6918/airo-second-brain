# AIRO Phase 5F Google API Fallback Strategy

Generated: 2026-05-08T22:01:24+07:00
Repository: progamer6918/vortex-ai-skill-lab
Branch: main
Base commit: c24db07

Status:
PASS

Scope:
Phase 5F prepares fallback paths for cases where Google Cloud trial expires, Google API access is disabled, OAuth breaks, quota is exceeded, or real API sync is temporarily unavailable.

Script:
scripts/personal-workflow/airo_google_fallback.py

Fallback priority:
1. Use approved queue executor with OAuth Google Sheets API when available.
2. If Google API is unavailable, export approved rows to CSV.
3. Import CSV manually into Google Sheets.
4. Keep local dashboard and SQLite workflow active.
5. Consider Apps Script Web App fallback only after explicit future approval.

Capabilities added:
- fallback status check
- CSV fallback export
- manual Google Sheets import checklist
- Apps Script Web App fallback proposal
- local fallback audit log

Commands:
python3 scripts/personal-workflow/airo_google_fallback.py status
python3 scripts/personal-workflow/airo_google_fallback.py csv-export --payload rows.json
python3 scripts/personal-workflow/airo_google_fallback.py manual-checklist
python3 scripts/personal-workflow/airo_google_fallback.py apps-script-plan

Fallback CSV directory:
/home/egitaristorandas/.local/share/airo-personal-workflow/exports/google_api_fallback

Fallback audit:
/home/egitaristorandas/.local/share/airo-personal-workflow/audits/google_fallback_audit.jsonl

Operations dashboard:
/home/egitaristorandas/.local/share/airo-personal-workflow/dashboard/daily_ops.html

Apps Script boundary:
This phase creates proposal documentation only.
It does not create, deploy, or configure Apps Script.
It does not generate endpoint secrets.
It does not write externally.

Validation:
PASS - inside git repo
PASS - branch main
PASS - Phase 5E exists
PASS - sheets sync helper exists
PASS - ops dashboard exists
PASS - python3 available
PASS - Google API fallback helper created
PASS - fallback status JSON PASS
PASS - fallback CSV export JSON PASS
PASS - manual checklist JSON PASS
PASS - Apps Script proposal JSON PASS
PASS - fallback CSV directory exists
PASS - fallback audit exists
PASS - daily ops dashboard regenerated

Safety:
- no secret read
- no token content read
- no credential content read
- no .env read
- no browser profile access
- no real Google Workspace write
- no Apps Script deployment
- no endpoint secret creation
- no OpenClaw core patch
- no service restart
- no EarnsAI runtime access
- no live trading
- no hard delete
- no finance transaction write

Decision:
Phase 5F is complete. The project can continue to Phase 5G Phase 5 Handoff and Release Tag.
