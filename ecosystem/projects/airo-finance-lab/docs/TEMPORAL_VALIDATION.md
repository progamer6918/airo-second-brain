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

## Gmail conversation follow-up

125 related checks passed after five additional regressions covering terminal rejection, repeated callbacks, context restoration on explicit selection, restart during note entry, and purpose plus account parsing in one answer. Gmail action buttons now occupy one row each. Rejecting another email does not replace the active note context; rejected rows are kept for audit and removed from actionable recaps. For Gmail-confirmed payment accounts, a different owner-specified account is a funding source; existing transfer evidence is checked before a funding question or posting. No financial records or balances changed during this repair. Existing Telegram messages are not proactively resent by the operator.

## Natural-purpose and status follow-up

130 related checks pass after four additional purpose/status regressions. Explicit purchase purposes survive partial parsing even when classification is unresolved. Existing subcategory names are recognized; conflicting labels can use existing recorded context as a suggestion. Bounded semantic interpretation runs when meaning remains unresolved after partial fact extraction. Status/help questions and `rekapan` do not change draft data or trigger semantic reinterpretation. Visible category suggestions are approved together with a single Save action; other missing facts still block. An acceptance run against a private copy of live data verified a ready draft, non-mutating status question, one save action, repeat-save idempotency, account debit and receipt account/balance. No real financial posting or Telegram send was performed by that acceptance run.
