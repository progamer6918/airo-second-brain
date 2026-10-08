# Temporal release validation

The release adds event-time provenance across ledger transactions, transfers, card and debt payments, purchases and valuations. Source clocks and recording clocks remain distinct. Metadata corrections and recovery require a persistent preview and never replay financial postings.

## Verified

- 120 related unittest checks passed across temporal, intake, Gmail recovery/canary, pending review, draft editor and card payment suites. Fixtures use temporary databases and mocked Telegram/Gmail.
- Nine browser checks passed on mobile/desktop with Asia/Shanghai and America/New_York device timezones. WIB display, manual event-time entry, metadata-only preview, recovery preview and linked statement payment were exercised. No browser page errors.
- Live dashboard, gateway and ingestion/outbox/watchdog timers are active. Deployed code hashes match the release manifest; domain read APIs return valid data.
- Consistent SQLite backup preceded additive migration. Financial rows and balances were preserved. The historical proposal remains PREVIEW: no historical time changes, financial postings or operator Telegram sends were performed by this rollout.
- Historical recovery keeps weak evidence unresolved. A verified-owner Telegram JSON export can provide source time; only an unambiguous immediate same-day input can suggest an estimated event clock.

## Limits

A broader 250-test run retained 12 pre-existing fixture/assertion failures, with no new regressions in that comparison; it is not a fully passing suite. The related suites were rerun after final fixes. Historical time application still requires the owner to review the concrete preview. Learning remains in suggestion/shadow mode; seven-day observation does not automatically authorize email patterns.

## Reproduce

Run unittest discovery for the seven patterns listed above. Browser verification uses `tests/browser_temporal.py --chrome <chromium-path> --output <private-evidence-directory>` with Playwright in an isolated environment. Production does not require Playwright. Keep recovery exports, live screenshots, database snapshots and raw message/email content private.
