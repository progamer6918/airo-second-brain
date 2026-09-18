---
type: awd-runtime-status
last_generated: 2026-09-18 13:28:27 UTC
generator: scripts/airo-workdesk-refresh-check
status: ALL_PASS
---

# 🧭 AWD Operational Runtime Status

> [!info] Operational Ground Truth
> **Generated**: `2026-09-18 13:28:27 UTC` · **Validation Status**: `ALL_PASS` · **Consumption Mode**: Direct Operational TSV (No database, no materialization, zero TSV mutation).

## 1. Executive Business Pulse Snapshot
- **Retail Sales (YTD Jan-Jul 2026)**: **73,968 units** total volume (+29.78% YoY) · Jul: **12,241 units** · 60 active dealer outlets · 73 product types · 10 kabupaten/kota.
- **Market Share (YTD Jan-Jun 2026)**: **82.27%** Honda market share (+0.92 pp YoY) · **65,031** Honda / **79,042** Total Market across 9 kabupaten & 9 segments.
- **Territory Authority (2026)**: **9 Kabupaten**, **118 Kecamatan**, **1,223 Kelurahan/Desa** mapped in hierarchy · **14,849** dense geography filter rows.
- **Inventory Stock (2026-08-06)**: **5,239 dealer stock units** (6.17% aging >150d, 13.27 stock days) · **3,496 MD warehouse stock units**.
- **Commercial & Historical Ring**: MSW August 2026 active resolver · 2022 Historical Ring mapping baseline (802 rows).

## 2. Operational Authority Verification Matrix
| Domain | Role | Canonical Runtime TSV | Period | Rows | Schema | Checksum (SHA256) | Registry | Status |
|---|---|---|---|---|---|---|---|---|
| Retail Sales | Dealer Contribution & Monthly Volume | `RETAIL_2026_YTD_JUL_DEALER.tsv` | YTD Jan-Jul 2026 | 61 | PASS | PASS | PASS | **PASS** |
| Retail Sales | Product Type Contribution & Volume | `RETAIL_2026_YTD_JUL_TYPE.tsv` | YTD Jan-Jul 2026 | 74 | PASS | PASS | PASS | **PASS** |
| Retail Sales | Area Geographic Distribution | `RETAIL_2026_YTD_JUL_AREA.tsv` | YTD Jan-Jul 2026 | 12 | PASS | PASS | PASS | **PASS** |
| Retail Sales | Monthly Retail Actuals & YoY Growth | `RETAIL_2026_CURRENT_SUMMARY.tsv` | Jan-Jul 2026 | 8 | PASS | PASS | PASS | **PASS** |
| Market Share | Kabupaten & Segment Breakdown | `MARKET_SHARE_YTD_JUN_2026_KABUPATEN_SEGMENT.tsv` | YTD Jan-Jun 2026 | 89 | PASS | PASS | PASS | **PASS** |
| Market Share | Province Segment Market Share | `MARKET_SHARE_YTD_JUN_2026_SEGMENT.tsv` | YTD Jan-Jun 2026 | 11 | PASS | PASS | PASS | **PASS** |
| Territory | Master Geographic Hierarchy | `POLREG_2026_AREA_HIERARCHY.tsv` | 2026 | 1,223 | PASS | PASS | PASS | **PASS** |
| Territory | Dense Geography Segment Matrix | `POLREG_YTD_JUN_2026_GEOGRAPHY_SEGMENT.tsv` | YTD Jan-Jun 2026 | 14,850 | PASS | PASS | PASS | **PASS** |
| Inventory Stock | Dealer Stock Positions & Aging | `DEALER_STOCK_2026-08-06_AGGREGATE.tsv` | 2026-08-06 | 2,877 | PASS | PASS | PASS | **PASS** |
| Inventory Stock | MD Warehouse Stock Positions | `MD_STOCK_2026-08-06_AGGREGATE.tsv` | 2026-08-06 | 3,489 | PASS | PASS | PASS | **PASS** |
| Territory/Commercial | Historical Ring Mapping 2022 | `RING_MAPPING_2022_HISTORICAL.tsv` | 2022 | 803 | PASS | PASS | PASS | **PASS** |

## 3. Provenance & Data Protection Governance
All active operational TSVs originate from private upstream workbooks (`PRIVATE_RAW_UPSTREAM_PROVENANCE`). Raw workbooks remain strictly uncommitted/excluded from public repository memory. Aggregated and sanitized data structures protect customer PII and engine-level identifiers in compliance with ASB `DATA_USE_RULES.md`. Zero database, zero materialization, and zero TSV mutations are performed.

## 4. Consumption Query Guide for Fresh AI
Fresh AI instances MUST query the operational runtime layer directly using `scripts/airo-workdesk-query` without requesting user file uploads:

```bash
# 1. Query dealer performance (e.g. Anugrah Honda Motor YTD 2026):
python3 scripts/airo-workdesk-query --dealer 'Anugrah Honda Motor'

# 2. Compare dealers head-to-head (e.g. CSM Sarolangun vs CSM Mandiangin):
python3 scripts/airo-workdesk-query --compare-dealers 'CSM Sarolangun' 'CSM Mandiangin'

# 3. Display full AWD data availability and operating pulse:
python3 scripts/airo-workdesk-query --availability

# 4. Direct table query with column filters:
python3 scripts/airo-workdesk-query --table market_kabupaten_segment --filter 'kabupaten=Sarolangun,segment=AT High'
```

