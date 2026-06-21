# AIRO Full Auto Asset Sync v1.2C Live Pass

Status: PASS after v1.2D dedupe-key fix.

## Verified target

- duplicate_key / savings_event_id: `sav_d78b1a231bb6`
- source command: `nabung 5000 ke blu`
- verified amount: `5000`
- target tab: `🥇 Aset`
- section: `savings_transfer_ledger`
- sheet row: `7`
- sheet key column: `O`
- post-fix verification action: `skip_duplicate`

## Notes

Initial v1.2C live apply wrote the row successfully, but verification failed because the planner used prefixed duplicate key `savings:sav_d78b1a231bb6` while the sheet exporter used the actual key `sav_d78b1a231bb6`.

v1.2D fixed the planner duplicate-key contract to match the actual sheet key columns.

## Safety

- Amount parser bare-number fix was applied before live write.
- `nabung 5000 ke blu` was verified as `5000`, not `5000000`.
- Timer was paused during live validation.
- Approval phrase remains disabled.
- No Apps Script was used.
- Restricted local paths were not staged.
