# AIRO Phase 2D Google Workspace OAuth Bootstrap Guide

Generated: 2026-05-08T20:17:08+07:00
Branch: main
Base commit: 974fb75

Status:
PASS

Scope:
Phase 2D prepares the Google Workspace OAuth bootstrap plan for Airo Personal Workflow.

This phase does not perform real OAuth login, does not store credentials in Git, does not write to Google Workspace, and does not access Gmail, Drive, Sheets, Docs, or Calendar.

Goal:
Prepare a safe path for later Google Sheets real-write integration behind approval gate.

Local-only files:
OAuth credentials and tokens must stay outside Git.

Recommended local directory:

    ~/.local/share/airo-personal-workflow/google/

Recommended local file names:

    credentials.local.json
    token.local.json

Never commit these files.

Git guardrail:
.gitignore now excludes common local OAuth and token filenames.

Google Cloud setup checklist:
1. Open Google Cloud Console manually in browser.
2. Create or select a project for Airo Personal Workflow.
3. Enable only the APIs needed for the next phase.
4. For Phase 2E, start with Google Sheets API only.
5. Configure OAuth consent screen.
6. Create OAuth Client ID for Desktop App.
7. Download OAuth client JSON locally.
8. Save it outside this repo.
9. Do not paste client secret, token, refresh token, cookie, or session into chat or GitHub.
10. Run future OAuth bootstrap only after explicit approval.

Minimum scope for Phase 2E:
Use the narrowest practical Google Sheets scope.

Preferred initial scope:

    https://www.googleapis.com/auth/spreadsheets

Do not request Gmail, Drive-wide, Docs, or Calendar scopes during Phase 2E unless explicitly needed later.

Approval gate:
Before any real Google write, Airo must show:
- target spreadsheet ID or name
- target sheet/tab
- rows to be written
- exact operation
- dry-run preview
- confirmation prompt

Forbidden:
- no Gmail access
- no Drive-wide scan
- no browser profile access
- no cookie/session read
- no token committed to Git
- no OAuth secret committed to Git
- no automatic real write without approval

Phase 2D validation:
PASS - inside git repo
PASS - branch main
PASS - git available
PASS - .gitignore local secret guardrail added
PASS - no tracked secret-like OAuth filenames detected

Tracked risky filenames check:
none

Next:
Phase 2E Google Sheets real write with approval gate.
