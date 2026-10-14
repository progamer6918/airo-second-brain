# AWD September 2026 — Reconciled Source-Level Aggregate Validation

**Verification date**: 2026-10-14 (Asia/Jakarta)  
**Task class**: CURRENT_BUSINESS_DATA / UPDATE  
**Status**: SOURCE_AGGREGATES_VERIFIED; FULL_AWD_RUNTIME_REFRESH_PENDING  
**Security**: Public-safe business-level aggregates only. Private customer and unit-level records MUST NOT be committed to public ASB.

## Source files (private upstream)

- `SSU.2026.xlsx` / `Monitoring Penjualan Dealer Dai` — retail 2026 Jan–Sep, dealer, customer kabupaten origin and model description.
- `SSU.2026.09.xlsx` — independent September only, validated on each of 61 dealer/POS names.
- `SINSEN_EVALPOLREG+MSPERKAB_SEP 2026.xlsx` / `Database Polreg 2026`, `Database Polreg 2025` — Honda and competitors by kabupaten, 9 segments, month.
- `Stok_per_no_mesin_dealer - 2026-09-12T102129.734.xls` — stock position for 61 dealer/POS; source snapshot timestamp 2026-09-12.
- `POLREG PER KECAMATAN PER KELURAHAN PER SEGMENT 2026.xlsx` in folder `9. Sept` — **contains Jan–Aug, September month blocks are all zero**; not valid September geographic source.
- `Record Sales 2008-2025.xlsx` — comparable 2025 retailer historic volume.

## Retail source QA

| Month | Dealer retail |
|---|---:|
| January | 10,545 |
| February | 10,944 |
| March | 11,761 |
| April | 9,022 |
| May | 9,479 |
| June | 9,976 |
| July | 12,241 |
| August | 12,413 |
| September | 11,527 |
| **YTD January–September** | **97,908** |

Checks: sum of 61 dealer/POS name aggregates = **97,908**. Sum of 12 customer kabupaten-origin labels = **97,908**. Sum of 53 type-*description* labels = **97,908**. September separate SSU monthly vs master matched **61 / 61** dealer/POS totals, no mismatch. Prior July runtime YTD Jan–Jul **73,968** reconciles.

The 53 current type-description labels are NOT structurally equivalent to the earlier 73 type-code labels. Any replacement of type-code analytical tables must include explicit mapping.

## Market source QA

- Province 2026 YTD Jan–Sep: Honda **101,306**, all-brand market **122,865**, MS **82.45%**.
- Province 2025 YTD Jan–Sep: Honda **75,014**, all-brand market **92,024**, MS **81.52%**.
- Market share Delta **+0.94 pp**; Honda volume growth ~**35.05%**, all-market growth ~**33.51%**.
- June reconciliation from the September evaluation's **raw** database: YTD Jan–Jun 2026 Honda **65,031**, market **79,042** — exactly matches existing ASB June authoritative row.
- All 9 kabupaten rows and 9-segment (+unclassified) component totals were checked to reconcile to each kabupaten ALL row; keep unclassified units separate.

## Inventory source QA

- September 12 dealer network stock: **5,835 units**, **61 dealer/POS**.
- Stock status: Ready **4,122**; Soft Booking **874**; Unfill **626**; Intransit **213**. Sum **5,835**.
- Aging: 0–30 **4,251**, 31–60 **718**, 61–90 **231**, 91–120 **151**, 121–150 **112**, >150 **372**. Sum **5,835**.
- All 61 dealer stock totals reconcile independently to status and aging bucket subtotals.
- Old AWD stock snapshot 2026-08-06 **5,239** units is historical, not a September authority. No MD September stock was verified by this task.

## Source compatibility

- `SSU.2026.xlsx` changes its column layout starting July, causing ordinal-position drift for some fields (especially salesperson ID, role and finco), so blindly applying Jan–June column positions to Jul–Sep can silently corrupt field-level diagnostics. Monthly Aug and Sep workbooks were used to verify Tebing channel/finco/FLP.
- A filename/folder `9. Sept` does not establish Sep coverage. Sep *per kecamatan* POLREG fields are blank/zero, while dedicated September EVALPOLREG does contain provincial/kabupaten market data through Sep.
- The two Tanjab Barat Jan–Aug all-brand market denominators are **10,200** in POLREG per kecamatan vs **10,201** in September market evaluation; source-specific one-unit discrepancy remains open.
- Stock source snapshot is Sep 12, not month-end and not a contemporaneous retailer numerator.

## Runtime status and promotion gate

The above are **validated source aggregates**, **NOT** certification that `AWD_RUNTIME_STATUS.md` (generated 2026-09-18 for July retail/June market) has been refreshed. The legacy `RETAIL_2026_YTD_JUL_*.tsv`, `MARKET_SHARE_YTD_JUN_*.tsv` and `POLREG_YTD_JUN_*.tsv` remain older snapshots. To promote September as AWD runtime source of truth, regenerate all dependent retail/area/dealer/type (using type-code mapping), market segment and geography (through only Aug pending September data), stock, manifests/checksums/registries and run full validation gates. Do not hand-edit runtime status to ALL_PASS.

Targeted verified Sinsen Tebing structured files:
- `wiki/workdesk/business-memory/operational/RETAIL_2026_YTD_SEP_SINSEN_TEBING_VERIFIED.tsv`
- `wiki/workdesk/business-memory/operational/MARKET_SHARE_YTD_SEP_2026_TANJAB_BARAT_SEGMENT_VERIFIED.tsv`
- `wiki/workdesk/business-memory/operational/SINSEN_TEBING_AUG_SEP_2026_DIAGNOSTICS_VERIFIED.tsv`
- `wiki/workdesk/business-memory/operational/DEALER_STOCK_2026-09-12_SINSEN_TEBING_VERIFIED.tsv`

**Note:** Full de-identified 61-dealer, 12-origin-area, 53-description-type, 98 kabupaten/segment, and 61-stock-row source extracts have been generated and QA-checked within the current audit workspace, but have not been committed or promoted to the generated AWD runtime.
