# Sinsen Tebing — September 2026 source freshness reconciliation

- Verification date: 2026-10-14 (Asia/Jakarta)
- Type: CURRENT_BUSINESS_DATA / OWNER_CORRECTION
- Reconciliation: UPDATE (older AWD retail Jul and market Jun snapshots remain historically accurate, but are stale for Sep reporting)
- Scope: Sinsen Tebing retail; Tanjab Barat kabupaten-level market; September-source currentness conflict
- Privacy: aggregate business metrics only. No consumer names, ID, contacts, addresses, unit identifiers, FLP identifiers, or raw rows retained.

## Inputs and authority

1. `SSU.2026.xlsx` (Drive modified 2026-10-07): master `Monitoring Penjualan Dealer Dai`, 2026 Jan–Sep, 97,908 rows for province all dealers.
2. `SSU.2026.09.xlsx` (Drive modified 2026-10-01): September-only, 11,527 transactions. Province September and Tebing September match the current master exactly (11,527 and 116).
3. `Record Sales 2008-2025.xlsx` / `Monthly`: comparable 2025 monthly history.
4. `SINSEN_EVALPOLREG+MSPERKAB_SEP 2026.xlsx`: 2026 and 2025 raw market databases, months Jan–Sep.
5. `POLREG PER KECAMATAN PER KELURAHAN PER SEGMENT 2026.xlsx` in folder `9. Sept`, Drive modified 2026-10-14: `Data` only contains January–August; its September monthly values remain zero. DO NOT promote this as September-ready kecamatan data.
6. Upstream workbook sources are private; the ASB PUBLIC repository may retain only sanitized aggregates and provenance names, never raw workbooks.

## Verification

- Retail Tebing YTD Jan–Sep 2026: **1,117**, vs 2025 **858**, YoY **+30.19%**.
- Retail monthly Tebing Jul/Aug/Sep 2026: **153 / 132 / 116**; Aug→Sep **−12.12%**; Jul→Sep **−24.18%**.
- Sep 2025 Tebing **86**, therefore Sep 2026 YoY **+34.88%**.
- Tanjab Barat market Honda YTD Jan–Sep: 2026 **9,272**, 2025 **7,175**, +29.23%; all-brand market 2026 **11,512**, 2025 **9,215**, +24.93%.
- Honda Tanjab Barat market share YTD 2026 **80.54%**, vs 2025 **77.86%**, +2.68 pp.
- Tanjab Barat Honda monthly Aug 2026 **1,045** vs Sep **1,078** (+3.16%); dealer Tebing retail fell over the same months; this is only kabupaten-level context, not dealer-specific market share.
- Tanjab Barat MS Cub High **23.89%** (54/226), Cub Mid **55.83%** (785/1406), AT High **61.11%** (1931/3160).
- Polreg per-kecamatan as of the September-folder source remains Jan–Aug only, including 2026 Jan–Aug Tanjab Barat Honda **8,194**. Its regional total-market cached YTD value is **10,200**, versus **10,201** aggregated from the Sep market evaluation Jan–Aug source (1-unit discrepancy); investigate classification/source before a full geography refresh.

## Targeted August–September sales diagnosis

Validated against the separate monthly SSU workbooks (not a lead funnel; categories below are sales activity attribution):
- Dealer Tebing retail Aug **132** and Sep **116**.
- Walk-in/Buku Tamu **50 → 33** (−17 units); Canvassing **21 → 11** (−10); Flyering **39 → 44** (+5); Mobile App MD/Dealer **3 → 14** (+11). These categories count realized retail, NOT leads or conversion rates.
- Unique FLP IDs with at least one sale **11 → 10**; top single FLP contributed **60/132 (45.45%)** in Aug and **50/116 (43.10%)** in Sep. This does not measure full active roster.
- Customer geographic origin (aggregated kecamatan): Tebing Tinggi **87 → 83**; Senyerang **30 → 24**; other origin districts combined **15 → 9**. Source fields are buyer address areas; do NOT treat them as sales-territory allocation or exclusive dealer ring mapping.
- In the current per-kecamatan POLREG file (data through Aug), Tebing Tinggi shows Honda **874** / market **1,133** (77.14% MS), Senyerang Honda **494** / market **630** (78.41% MS); both are below the Jan–Aug kabupaten average of ~80.3% but not Sep-ready.
- Priority questions: what drove the walk-in/canvassing dip, why one fewer FLP achieved a sale, whether Senyerang coverage slipped, and why retail fell when Tanjab Barat Honda market improved Aug→Sep.

## Deep-audit addendum — 2026-10-14

### September source audit and cross-source QA

- SSU master `SSU.2026.xlsx` Jan–Sep 2026 totals **97,908** records, including Sep **11,527** across **61 dealer/POS names**. All 61 Sep dealer-name subtotals match the separate `SSU.2026.09.xlsx` source exactly (**zero mismatches**). Jan–Jul master total **73,968** matches the prior AWD July snapshot.
- Current `SINSEN_EVALPOLREG+MSPERKAB_SEP 2026.xlsx` raw database yields province market Jan–Sep 2026 **101,306 Honda / 122,865 total**, compared to 2025 **75,014 Honda / 92,024 total**. Its historical Jan–Jun 2026 aggregate **65,031 / 79,042** matches the existing older ASB authority.
- Schema drift: the SSU master has an additional field relative to early-month records beginning July; when deriving FLP IDs or financing by fixed ordinal index, **the June and July–September rows must not share one fixed column mapping**. August and September drilldowns here were re-extracted independently from the respective monthly files with validated header positions.
- A dedicated Sep-12 stock file was found later than the old Aug-06 stock authority: Sinsen Tebing **54 units**, including Ready **49**, Soft Booking **4**, Unfill **1**. Aging: **40** (0–30), **7** (31–60), **2** (61–90), **0** (91–120), **2** (121–150), **3** (>150). Comparison with Aug-06 total **70** is cross-snapshot, not a trend in supply quality.
- Retail September 116 units over 30 days implies *retrospective indicative* stock cover **13.97 days** using stock observed Sept 12; never treat as month-end cover.

### Root-cause leads and evidence limits

- Finco recorded and matching populated tenor: Aug **78/132 (59.1%)** to Sep **51/116 (44.0%)**, **−27** financed-retail records; missing both fields Aug **54** to Sep **65**. The blank category is **not proven cash** without dealer operational confirmation.
- Finco among completed retail: **FIFASTRA 41→21 (−20)**, **ADMF 14→6 (−8)**, **SOF 18→21 (+3)**, **MUF 5→3 (−2)**. These are financed retail counts, not credit rejection/approval, SPK, or funnel rates.
- Retail-source channels: Walk-in **50→33**, Canvassing **21→11**, Flyering **39→44**, Mobile App **3→14**, Facebook Message **10→6**. The first two channels account for a combined **−27** gross unit change; others offset a portion. These are **final retail** classifications.
- Consumer kecamatan origin: Tebing Tinggi **87→83**, Senyerang **30→24**. These are buyer-address fields, **not dealer ring**.
- Independently confirmed kecamatan-level POLREG Jan–Aug 2026 from top-level Tanjab Barat rows (not nested village labels): Tebing Tinggi Honda **874 / 1,133 market = 77.14%**; Senyerang **494 / 630 = 78.41%**. Both below kabupaten ~**80.33%** Jan–Aug. POLREG September fields are **zero / not ingested** despite September folder name.
- BeAT family Aug **46** Sep **39** (−7), Scoopy **22→18** (−4), PCX **13→10** (−3), Vario **8→5** (−3), Revo **20→20** (flat), Stylo **6→9** (+3). Product family derived from type description only; do not infer official Honda segment mix without proper mapping.
- Actual selling FLP IDs counted from monthly sales records **11→10**. Largest single anonymized FLP contribution **60→50**; total active workforce cannot be determined from the set of IDs with sales.
- Benchmark peer dealer totals (not dealer territory MS): Bulan Motor Tungkal **288→302**, Bulan Motor Merlung **260→265**, POS Patria Tungkal **120→113**, TDM Merlung **151→151**, Tebing **132→116**. Dealer catchments and POS types are non-equivalent; peer movements are diagnostic only.

### Public-safe structured references

- `wiki/workdesk/business-memory/operational/SINSEN_TEBING_AUG_SEP_2026_DIAGNOSTICS_VERIFIED.tsv`
- `wiki/workdesk/business-memory/operational/DEALER_STOCK_2026-09-12_SINSEN_TEBING_VERIFIED.tsv`

**Priority validation in INR:** credit retail down (especially FIF/ADMF); walk-in and canvassing volume down; identify reason for financial conversion gap; validate stock-fit for BeAT, PCX, Vario EVO, Stylo, and Revo; test Tebing Tinggi/Senyerang field coverage. Ask for applications and approval/rejection funnel separately, plus active FLP roster and lost-sale log. No causality established by retail aggregate alone.

## Canonical synchronization boundary

- This evidence verifies September source availability and **targeted** Tebing/Tanjab Barat aggregates. It does NOT assert a full network-wide Sep AWD runtime refresh.
- Existing generated `AWD_RUNTIME_STATUS.md` (2026-09-18), July retail TSVs, June market-share TSVs, and geography TSVs have NOT been regenerated by this limited reconciliation.
- Full AWD refresh requires regeneration of all dependent dealer/area/type, market hierarchy, nine-segment, provenance, inventory indexes and validation/manifest/checksum gates. Runtime ALL_PASS must be earned by execution, not edited by hand.
- Review status: **TARGETED_SEPTEMBER_VERIFIED; FULL_AWD_RUNTIME_REFRESH_PENDING**.

## New targeted structured memory

- `wiki/workdesk/business-memory/operational/RETAIL_2026_YTD_SEP_SINSEN_TEBING_VERIFIED.tsv`
- `wiki/workdesk/business-memory/operational/MARKET_SHARE_YTD_SEP_2026_TANJAB_BARAT_SEGMENT_VERIFIED.tsv`
