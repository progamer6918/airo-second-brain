# AIRO Full Auto Sheets Sync v1.1.2 OAuth Support

Status: IMPLEMENTED / READY FOR LIVE OAUTH LOGIN
Date: 2026-05-10

## Trigger

Service account key creation was blocked by Google Cloud organization policy:

- iam.disableServiceAccountKeyCreation

So the full-auto sync pipeline now supports OAuth Desktop Client credentials.

## Credential mode

Preferred mode:

- AIRO_GOOGLE_OAUTH_CLIENT_SECRET_PATH
- AIRO_GOOGLE_OAUTH_TOKEN_PATH

Fallback mode:

- AIRO_GOOGLE_SERVICE_ACCOUNT_JSON_PATH
- AIRO_GOOGLE_SERVICE_ACCOUNT_JSON

## Behavior

On first live run:

1. The client starts a local OAuth browser flow.
2. User approves Google Sheets access once.
3. Token is saved locally at AIRO_GOOGLE_OAUTH_TOKEN_PATH.
4. Future runs reuse/refresh token automatically.

## Safety

OAuth client secret and token are local-only and must never be committed.

## Next official item

Run live dry-run once, complete OAuth browser approval, verify live sheet key export, then run apply.
