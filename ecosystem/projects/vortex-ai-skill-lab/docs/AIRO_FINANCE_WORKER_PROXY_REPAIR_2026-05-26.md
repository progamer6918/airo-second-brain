# AIRO Finance - Worker Proxy Repair

Date: 2026-05-26
Sprint: Sprint 5 - Dashboard Analytics
Status: Worker proxy repair

## Trigger

Direct Apps Script V2 returned the correct read-only reconciliation response.

Telegram through Worker still routed `admin audit sprint5 reconciliation` into Review Queue as Rp5.

Wrangler secret update reported that it could not find an existing Worker named `airo-finance-telegram-proxy` and created a new Worker in non-interactive mode.

## Repair

A minimal Cloudflare Worker proxy source is now stored in the repo:

workers/airo-finance-telegram-proxy/src/index.js

Contract:

- GET returns health JSON.
- POST reads Telegram update body.
- POST forwards body to APPS_SCRIPT_URL.
- Worker responds immediately with async_ack.
- Apps Script V2 sends the Telegram reply.
- Worker does not parse finance text.
- Worker does not write to Google Sheets.

## Required secret

APPS_SCRIPT_URL must point to Apps Script V2:

https://script.google.com/macros/s/AKfycbx4HWJNY9YOPIssAF9tn3Gx36hFkumyH0TfsuWInPr0e8aZTyrbIs4-kn_Fd-Kox_ie/exec

## Bad live artifacts

Two Review Queue rows were created from:

admin audit sprint5 reconciliation

Do not approve them.
