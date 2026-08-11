# POLREG 2026 Geographic × Segment Retrieval Memory

## Purpose
Preserve the decision-grade filtered views that exist in `POLREG PER KECAMATAN PER KELURAHAN PER SEGMENT 2026.xlsx` without copying the workbook binary.

## Current supplied period
- Source data months present: **January–June 2026**.
- Comparable memory uses **January–June 2025** from the supplied 2025 POLREG workbook, mapped through the supplied 2026 geography hierarchy.
- Province-level Market Share authority remains the dedicated `SINSEN_EVALPOLREG+MSPERKAB_JUN 2026.xlsx` memory. POLREG is the deep geographic-filter authority.

## Retrieval coverage
- **9** supplied market-area sheets.
- **118 kecamatan**.
- **1,223 mapped area-code / kelurahan-desa rows**.
- Filter states preserved densely for every geography: `ALL SEG`, all **9 named segments**, plus source state `OTHERS`.
- Dense structured matrix: **14,850 rows** = `(9 kabupaten + 118 kecamatan + 1,223 kelurahan/desa) × 11 filter states`.

| Kabupaten/source sheet | Kecamatan | mapped kelurahan/desa rows |
|---|---:|---:|
| Batanghari | 8 | 123 |
| Bungo | 17 | 153 |
| Kota Jambi | 11 | 68 |
| Ma. Jambi | 11 | 154 |
| Merangin | 24 | 214 |
| Sarolangun | 11 | 158 |
| Tanjab Barat | 13 | 132 |
| Tanjab Timur | 11 | 93 |
| Tebo | 12 | 128 |

## Filter semantics recovered from source
The workbook formula switches on the segment selector. `ALL SEG` sums Month + Brand + AREA; a selected segment adds the Segment condition. Therefore a filtered value is not a cosmetic view; it is a materially different query result.

Structured retrieval file: `POLREG_YTD_JUN_2026_GEOGRAPHY_SEGMENT.tsv`.
Hierarchy/provenance file: `POLREG_2026_AREA_HIERARCHY.tsv`.

## Source-specific classification boundary — do not silently harmonize
All-Segment totals reconcile exactly across the dedicated M/S workbook and POLREG geography source: Honda **65,031**, Total Market **79,042**. However, a few segment classifications differ at source level:

| Segment | SINSEN Honda | SINSEN TM | POLREG Honda | POLREG TM | TM difference |
|---|---:|---:|---:|---:|---:|
| AT High | 14251 | 23125 | 14251 | 23125 | +0 |
| AT Low | 23019 | 23392 | 23019 | 23393 | +1 |
| AT Mid | 13539 | 14396 | 13539 | 14395 | -1 |
| Cub High | 234 | 1368 | 234 | 1368 | +0 |
| Cub Low | 6713 | 6731 | 6713 | 6731 | +0 |
| Cub Mid | 2968 | 5284 | 2968 | 5284 | +0 |
| Sport High | 6 | 42 | 6 | 41 | -1 |
| Sport Low | 717 | 719 | 717 | 719 | +0 |
| Sport Mid | 3584 | 3981 | 3584 | 3981 | +0 |

Additional boundary:
- Dedicated M/S workbook has **4** Total-Market units blank/uncategorized in the 9-segment field.
- POLREG source has **5** Total-Market units explicitly classified as `OTHERS`.

Therefore:
1. Answer province/all-9-segment M/S from the dedicated `SINSEN_EVALPOLREG+MSPERKAB_JUN 2026.xlsx` memory.
2. Answer kecamatan/kelurahan filtered questions from the POLREG source-specific structured matrix.
3. If combining the two views, disclose the small source classification discrepancy rather than forcing one taxonomy onto the other.

## Source-structure correction discovered during remediation
An earlier chat-derived count of `117 kecamatan / 1,206 kelurahan-desa` was not source-accurate. Re-read of the original workbook resolves **118 kecamatan / 1,223 mapped area rows**. Example: `AREA 60` has a blank FY2025 label cell but the Jan-2026 label is `Jelmu`; current hierarchy memory preserves the available current-source label instead of dropping the row.

## Zero-denominator rule
The dense matrix includes explicit zero rows for filter/geography combinations with no market observations. When denominator = 0, M/S is blank/undefined. Do not return 0% as if it were measured share and do not divide by zero.
