# AIRO Finance Sprint 6 - Dashboard Tab Discovery Fix

Status: Sprint 6 safety fix before Dashboard build.

## Reason

Live dry-run command worked:

    admin dashboard sprint6 plan

But plan reported:

    Existing Dashboard found: false
    Finance Events: MISSING
    Hutang: MISSING
    Aset: MISSING
    _AIRO_Audit_Log: MISSING

This should not immediately trigger Dashboard build.

The likely issue is exact tab matching:
- Dashboard may be named with emoji/prefix.
- Finance Events may use a different emoji/prefix.
- Domain tabs may use existing workbook naming variants.
- Audit log may exist with slight naming differences or may truly be missing.

## Patch

Add loose tab discovery:

    exact match
    normalized exact match
    normalized partial match

Normalization strips emoji, spaces, underscores, punctuation, and casing.

Example:

    Dashboard
    📊 Dashboard
    🏠 Dashboard

all normalize to:

    dashboard

## Safety

This patch does not build dashboard.
This patch does not write dashboard formulas.
This patch does not clear or delete sheets.
This patch only improves dry-run plan detection.

## Next Live Validation

Run:

    admin dashboard sprint6 plan

Expected improvement:
- Existing Dashboard found should detect emoji/prefix Dashboard if present.
- Finance Events should detect emoji/prefix Finance Events if present.
- Hutang and Aset should detect existing tabs if present.
- Reply should show fewer false MISSING results.

If any source remains MISSING after loose discovery, treat it as real missing or schema mismatch before Dashboard build.
