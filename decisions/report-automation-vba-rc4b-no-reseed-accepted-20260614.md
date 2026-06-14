# Decision - RC4B No-Reseed Accepted

Date: 2026-06-14

## Decision
Accept RC4B no-reseed patch as product-ready freeze after automated acceptance and smoke run.

## Why
The RC3S runtime engine already produced RPT001/RPT002/RPT003 OK. The missing product behavior was self-service/admin survivability: registry/source edits must not be overwritten by setup/check/rebuild.

## Rules Frozen
- Default seed may add missing baseline rows only.
- Existing admin-edited report/source rows must be preserved.
- Runtime evidence fields stay runtime-only.
- Legacy R7 canonical reseed must not overwrite registry rows if reactivated.
- Runtime runners remain unchanged.

## Package
AIRO_RC4B_NO_RESEED_PRODUCT_READY_20260614_145911.zip
SHA256: 7FB03CC30B55EE91FAED9928A28027A11844061FE79060264BD8029D46423E12
