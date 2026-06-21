# AIRO Finance — Alert Engine ADMIN_CHAT_ID Worker Secret Rebind

Date: 2026-05-31 WIB
Document type: Rebind record
Phase: Phase 5B-3c — ADMIN_CHAT_ID self-register/readback
Status: REBOUND / AWAITING TELEGRAM LIVE SMOKE

## Scope

This rebind updates the Cloudflare Worker secret `APPS_SCRIPT_URL` to point to the new Apps Script deployment for Phase 5B-3c:
- Worker Name: `airo-finance-telegram-proxy`
- Target URL: `https://script.google.com/macros/s/AKfycbyw5J5RWMoe9Vz2FDRwRInxt3J7VBGF5uWHOTKoKPNDYzgK83wqdrXU7zVP_Db0oOvCFQ/exec`
- Target Deployment: `@201`

## Steps Executed

1. Verified local git status is clean and matches origin/main.
2. Cleared corrupted local npm cache to resolve wrangler execution failures.
3. Updated Cloudflare Worker secret `APPS_SCRIPT_URL` on worker `airo-finance-telegram-proxy` to Apps Script deployment `@201`.
4. Deployed the Worker proxy source file `workers/airo-finance-telegram-proxy/src/index.js` using wrangler to the `earnsai` subdomain account.
5. Performed a health check on `https://airo-finance-telegram-proxy.earnsai.workers.dev` to confirm it returns `ok` and is correctly configured.

## Live smoke commands to run in Telegram

1. `admin alerts admin chat status`
2. `admin alerts set admin chat`
3. `admin alerts admin chat status`
4. `admin alerts live status`
5. `admin alerts live run once`

## Expected Safe State

- `ADMIN_CHAT_ID` route is recognized.
- `ADMIN_CHAT_ID` configured and masked in status after set.
- Live switch remains `FALSE`.
- Run once in OFF mode sends `0` alerts.
- Trigger count remains unchanged.
- Gmail/email untouched.
