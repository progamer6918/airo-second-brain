# AIRO Finance — Task 8 Debt and Cicilan Account Ledger Primary

Date: 2026-06-09 WIB
Status: Source patch PASS; production deployment pending

## Scope

Debt payment and Cicilan Rumah payment now write Account Ledger first.
Domain projection runs only after Account Ledger readback succeeds.

## Debt Payment

- Account Ledger is the primary monetary record.
- Hutang payment log uses the ledger entry ID as `pay_id`.
- Retry reuses the existing ledger entry.
- Projection failure returns partial status.

## Cicilan Rumah

- Account Ledger is written before the Cicilan Rumah projection.
- Projection maps `payment_id`, `cicilan_ke`, `date_paid`, `amount_paid`, `status`, and `notes`.
- The Account Ledger entry ID becomes `payment_id`.
- Retry does not duplicate the ledger row.

## Preserved

- Credit Card flow unchanged.
- Asset flow unchanged.
- Internal transfer flow unchanged.
- Debt increase flow unchanged.
- Finance Events remains deprecated and no-op.
- Transactions remains deleted and guarded.

## Safety

- Workbook write: no
- Deployment: no
- Gmail mutation: no
- Telegram production modification: no

## Pending

- Production deployment and live smoke
- Category Registry entry for Bayar Hutang Mamak
- Pending Rp1.000.000 correction
- Credit Card ledger-first conversion
- Asset ledger-first conversion
- Dashboard migration
