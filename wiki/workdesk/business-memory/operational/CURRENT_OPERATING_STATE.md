# AIRO WorkDesk — Current Operating State from Latest Supplied Sources

This page is a retrieval index, not a synchronized single-date dashboard. Each topic keeps its own latest supplied period and provenance.

## Market share — latest supplied market period
**Period:** YTD Jan–Jun 2026. Comparable: YTD Jan–Jun 2025 derived directly from raw database rows, not from the workbook's conflicting `YTD 2025` summary label.

**All Segment:** Honda **65.031** / Total Market **79.042** = **82.27%**, versus **81.36%** comparable; **+0.92 pp**.

| 9 Segment | Honda YTD 2026 | Total Market YTD 2026 | M/S 2026 | M/S 2025 comparable | Δ pp | Market contribution |
|---|---:|---:|---:|---:|---:|---:|
| AT High | 14.251 | 23.125 | 61.63% | 55.23% | +6.40 pp | 29.26% |
| AT Low | 23.019 | 23.392 | 98.41% | 98.21% | +0.20 pp | 29.59% |
| AT Mid | 13.539 | 14.396 | 94.05% | 92.50% | +1.55 pp | 18.21% |
| Cub High | 234 | 1.368 | 17.11% | 24.27% | -7.17 pp | 1.73% |
| Cub Low | 6.713 | 6.731 | 99.73% | 99.92% | -0.18 pp | 8.52% |
| Cub Mid | 2.968 | 5.284 | 56.17% | 53.44% | +2.73 pp | 6.69% |
| Sport High | 6 | 42 | 14.29% | 18.18% | -3.90 pp | 0.05% |
| Sport Low | 717 | 719 | 99.72% | 99.80% | -0.08 pp | 0.91% |
| Sport Mid | 3.584 | 3.981 | 90.03% | 87.48% | +2.55 pp | 5.04% |

There are **4 market units** in 2026 whose 9-segment category is blank/uncategorized. Do not force those units into one of the nine segments. Therefore nine classified segment denominators total 79,038 while All Segment denominator is 79,042.

**Material concern:** `Cub High`. Honda volume rose **226 → 234 (+3.54%)**, but total market rose **931 → 1,368 (+46.94%)**, so M/S fell **24.27% → 17.11% (-7.17 pp)**. This is an actual denominator example of volume-up / share-down. `Sport High` has lower absolute M/S (14.29%) but only 42 total-market units, so Cub High is materially more consequential.

Structured data: `MARKET_SHARE_YTD_JUN_2026_SEGMENT.tsv` and `MARKET_SHARE_YTD_JUN_2026_KABUPATEN_SEGMENT.tsv`.

### Deep geographic market retrieval — POLREG source-specific view
A separate supplied workbook, `POLREG PER KECAMATAN PER KELURAHAN PER SEGMENT 2026.xlsx`, preserves the current Jan–Jun 2026 drill-down to **9 market areas / 118 kecamatan / 1,223 mapped kelurahan-desa rows**, queryable for `ALL SEG`, all nine named segments, and `OTHERS`.

Use `POLREG_YTD_JUN_2026_GEOGRAPHY_SEGMENT.tsv` for filtered geography retrieval and `POLREG_2026_AREA_HIERARCHY.tsv` for hierarchy/provenance.

**Do not silently merge segment classifications across workbooks.** All-Segment totals reconcile at 65,031 Honda / 79,042 market, but POLREG differs from the dedicated M/S workbook by one Total-Market unit in AT Low, AT Mid and Sport High, and uses 5 explicit `OTHERS` units while the dedicated M/S workbook retains 4 blank/uncategorized units. Province-level 9-segment M/S remains sourced from the dedicated M/S workbook; deep geographic filtering remains sourced from POLREG.

Provenance: `SINSEN_EVALPOLREG+MSPERKAB_JUN 2026.xlsx`, raw sheets `Database Polreg 2026` and `Database Polreg 2025`; Month column filtered Jan–Jun; Unit/Brand/9-segment/Kabupaten retained in aggregate memory.

## Retail — latest supplied retail period
Latest monthly actual: **Jul 2026 = 12,241 units**. YTD Jan–Jul 2026 = **73.968 units**, versus Jan–Jul 2025 **56.996**, growth **29.78%**.

Monthly actual: Jan 10,545; Feb 10,944; Mar 11,761; Apr 9,022; May 9,479; Jun 9,976; Jul 12,241.

Current authority: `SSU.2026.xlsx` for 2026 actual. Comparable Jan–Jul 2025 uses `Record Sales 2008-2025.xlsx / Monthly`, because the supplied `SSU 2025.xlsx` raw detail only covers Jan–Apr and the historical record is the supplied source covering Jan–Jul. The historical record's cached 2026 values are stale after May and must **not** be used as current 2026 authority.

Dealer, area, and type drill-down are in the associated TSVs. Raw `SSU.2026.xlsx` contains customer PII; public memory intentionally retains only aggregated analytical facts.

## Dealer stock — as of 2026-08-06 08:03:42
Total dealer stock **5.239 units**. Status: Ready 3,495; Soft Booking 803; Unfill 593; Intransit 348.
Aging: 0–30 **3.862**; 31–60 **526**; 61–90 **252**; 91–120 **162**; 121–150 **114**; >150 **323**. >150 = **6.17%** of total.

Cross-source derived overall stock days using Jul-2026 retail: **13.27 days**, formula `End Stock / (Jul retail / 31)`. This is derived, not source-reported.

Highest derived stock-days concerns:
- POS PATRIA - SIJENJANG: **29.11 days**, stock 77, Jul retail 82, aging >90 10, >150 5.
- POS PATRIA - PAUH: **28.56 days**, stock 82, Jul retail 89, aging >90 2, >150 0.
- POS TUNAS JAMBI - BULURAN: **28.53 days**, stock 81, Jul retail 88, aging >90 21, >150 7.
- POS PATRIA - BUNGO: **27.90 days**, stock 81, Jul retail 90, aging >90 8, >150 2.
- PT. DAYA ANUGRAH MANDIRI - BAHAR: **25.61 days**, stock 114, Jul retail 138, aging >90 27, >150 20.
- POS PATRIA - SEI. GELAM: **25.59 days**, stock 71, Jul retail 86, aging >90 16, >150 6.
- POS TUNAS SABAK - RANTAU RASAU: **24.70 days**, stock 51, Jul retail 64, aging >90 3, >150 0.
- PT. CITRA KARYA INTISENTOSA I: **23.59 days**, stock 35, Jul retail 46, aging >90 12, >150 6.
- PT. TUNAS DWIPA MATRA - JAMBI: **22.81 days**, stock 117, Jul retail 159, aging >90 26, >150 16.
- CV. CITRA SENTOSA MOTOR - M.ANGIN: **21.45 days**, stock 101, Jul retail 146, aging >90 10, >150 2.

## MD stock — as of 2026-08-06 08:04:46
Total **3.496 units**: RFS 3.362, BOOKING 105, NRFS 29. Model year: 2026 3.446; 2025 50.

**MD aging is not present in the supplied MD-stock source. Do not derive aging from model year.**

## Ring authority
Latest supplied ring mapping is explicitly **2022**. It is preserved as historical mapping with 803 normalized dealer/POS-to-kecamatan ring records. **Current Ring authority remains unconfirmed**; do not promote Ring 2022 to current.

## Commercial/MSW
Latest supplied commercial program family covers **Aug 2026**. Use `business-memory/commercial/MSW_2026_CURRENT_VERSION_RESOLVER.tsv` before retrieving offers. Current August structured offers are in `MSW_AUGUST_2026_COMMERCIAL_OFFERS.tsv`.



## Integrated TTM / POS — current supplied 2026 state
Meeting authority: **2026-08-06**. Sinsen POS working snapshot: **2026-08-11**.

Current Integrated TTM extends H1 TTM into H1-H2 coverage analysis down to kecamatan and POS. Mapping Ring uses all network/POS locations; initial POS performance/target input focuses on Mega + Selected POS. For SSP, meeting target input is **3 Mega POS / 0 Selected**.

KPI 2026 remains H1-focused: Achievement Lokasi ≥85%, Achievement Ring 1 ≥85%, Locality based on grading. Slide table gives **SSP Target Locality 2026 = 89%**.

Current Sinsen POS standardization snapshot: **14 rows / 10 parent dealer codes / 3 revised or new codes**. It is **not proven submission-ready** because the supplied table lacks POS class, kelurahan and coordinates; five H1 rows are annotated `merupakan H23`; one H23 row lacks kabupaten/kecamatan.

Deadlines from the meeting: POS coding **13 Aug 2026**, Mapping Ring **24 Aug 2026**, Q2 review **21 Sep**, Q3 **30 Oct**, Q4 **29 Jan 2027**. Q1 deadline was 7 Aug; submission completion is not proven.

Use `INTEGRATED_TTM_POS_CURRENT_STATE_2026-08-11.md` plus the POS/timeline TSVs. Formal AHM guidance issued after the meeting may supersede meeting details.

## Cross-domain currentness boundary
These are asynchronous snapshots: market through Jun, retail through Jul, stock on Aug 6, MSW applicable Aug, Ring only 2022 historical. Never describe them as one same-date dataset.


## Market Info Tools — 11 Aug 2026 rollout
- Weekly dealer/kecamatan market-sensing workflow is current supplied process.
- Current Sinsen transition: MD Google Form quality validation -> approved dealer entry into AHM portal.
- Submission due no later than Friday of running week; still submit on scheduled no-event weeks.
- Actual historical weekly Market Info records are not supplied.
- Portal URLs/credentials are intentionally excluded from public ASB.
