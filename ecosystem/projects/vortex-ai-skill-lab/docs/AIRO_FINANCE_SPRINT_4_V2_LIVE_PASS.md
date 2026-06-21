# AIRO Finance - Sprint 4 V2 Live Pass

Date: 2026-05-25
Sprint: Sprint 4 - Finance Events v1
Status: LIVE PASS / CLOSED CANDIDATE

## Summary

Sprint 4 Finance Events live proof passed after rotating production Apps Script to a new V2 project because the old Apps Script project reached the 200 immutable version limit.

This rotates the Apps Script production container only. It does not reset AIRO Finance architecture, GitHub source, Google Sheet data, Telegram bot, or roadmap state.

## Source Patch

Latest source patch:

c0d57f2 fix(airo-finance): surface Finance Events emission failures

Patch impact:

- Finance Events write failure is no longer silently swallowed.
- recordFinanceEventForWriteResult_ returns financeEventStatus, financeEventRow, financeEventTab, and financeEventError when applicable.
- Finance Events write failure is logged as AIRO_FINANCE_EVENT_WRITE_FAILED.
- Admin smoke readback priority tab now uses AIRO_CONFIG.tabs.financeEvents.

Regression result before cutover:

32 passed

## Apps Script Rotation

Old Apps Script project reached:

200 versions

Old production deployment before rotation:

AKfycbwLGNdWSHF6_V-WFteyvPq9tm2hgB_jK-ecv56AImZn3D8VMHBYvtv6IOWFz4MP7qAYqQ @200

Backup path created locally:

_ops_backups/apps_script_rotation_20260525_230039

New Apps Script V2 project:

Script ID:
17JglcgQLf9qa4TbmOyfntbX0LEPy2SKdyIIycordDamFYMs9Og5ScWZi

Deployment ID:
AKfycbx4HWJNY9YOPIssAF9tn3Gx36hFkumyH0TfsuWInPr0e8aZTyrbIs4-kn_Fd-Kox_ie

Web App URL:
https://script.google.com/macros/s/AKfycbx4HWJNY9YOPIssAF9tn3Gx36hFkumyH0TfsuWInPr0e8aZTyrbIs4-kn_Fd-Kox_ie/exec

Cloudflare Worker production variable was manually updated:

APPS_SCRIPT_URL=https://script.google.com/macros/s/AKfycbx4HWJNY9YOPIssAF9tn3Gx36hFkumyH0TfsuWInPr0e8aZTyrbIs4-kn_Fd-Kox_ie/exec

## Live Smoke Proof

Telegram input:

SMKFEDELTA cash keluar 124049 buat kopi

Bot write reply:

Rencana tab: Cash Ledger
Ditulis ke: Account Ledger
Akun: Cash
Kategori: Makan
Nominal: Rp124049

Admin readback:

admin find smoke all SMKFEDELTA

Readback result:

Hasil: 2 match

Match #1:

Tab: Finance Events
Row: 8
Preview includes:
fe:a9409a96-9668-408e-83a9-84e9c6b5e68c
Account Ledger
tg:8482041086:895:1779726070:i7ouH_WZBzckWbGU
Cash
Makan
124049

Match #2:

Tab: Account Ledger
Row: 62
Preview includes:
tg:8482041086:895:1779726070:i7ouH_WZBzckWbGU
Cash Umum
Rp 124.049
expense
Makan
SMKFEDELTA cash keluar 124049 buat kopi
Cash Ledger

## Verification Result

Expected:

1 Account Ledger match
1 Finance Events match
No duplicate Account Ledger row

Observed:

PASS

## Sprint 4 Decision

Sprint 4 Finance Events v1 is now live-proven for the cash Account Ledger route after V2 production cutover.

Do not proceed to Sprint 5 until this proof is committed to GitHub and the current state document is updated.
