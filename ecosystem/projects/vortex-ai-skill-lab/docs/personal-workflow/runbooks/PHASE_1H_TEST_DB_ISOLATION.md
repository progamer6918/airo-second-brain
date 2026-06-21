# Phase 1H Test DB Isolation

## Goal

Prevent smoke tests from polluting the main local SQLite database.

## Decision

Smoke tests use the `AIRO_DB_PATH` environment variable to point to a temporary SQLite database.

## Impact

- Main local database remains stable.
- Smoke tests can be repeated safely.
- Telegram local handler test no longer increments the user's real installment count.
- Export and Google dry-run tests are generated from isolated test data.

## Safety

No Google OAuth, token, secret, cookie, Drive upload, Calendar write, or Gmail access is used.
