# WorkDesk Task Router v2

Start from what the user is trying to do.

| User intent | Primary brain route | Supporting routes |
|---|---|---|
| Kenapa market share / retail turun? | [[domains/01_BUSINESS_SENSING_MARKET_INTELLIGENCE]] | [[domains/03_DEALER_TERRITORY_PERFORMANCE]], [[domains/06_PROBLEM_SOLVING_STRATEGY_BUSINESS_CASE]] |
| Target / forecast terasa tidak masuk akal | [[domains/02_TARGET_FORECAST_DEMAND_SUPPLY]] | [[domains/01_BUSINESS_SENSING_MARKET_INTELLIGENCE]], [[domains/03_DEALER_TERRITORY_PERFORMANCE]] |
| Sales turun / stock menumpuk / distribusi tidak pas | [[domains/02_TARGET_FORECAST_DEMAND_SUPPLY]] | [[domains/03_DEALER_TERRITORY_PERFORMANCE]] |
| Dealer / area underperform | [[domains/03_DEALER_TERRITORY_PERFORMANCE]] | [[domains/01_BUSINESS_SENSING_MARKET_INTELLIGENCE]], [[domains/06_PROBLEM_SOLVING_STRATEGY_BUSINESS_CASE]] |
| NOS / network / POS / AHASS / Reshape | [[domains/04_NETWORK_DEVELOPMENT_OPERATING_STANDARD]] | [[domains/03_DEALER_TERRITORY_PERFORMANCE]] |
| Leads / CRM / BTL / VE / customer | [[domains/05_CUSTOMER_CRM_ACTIVATION]] | [[domains/01_BUSINESS_SENSING_MARKET_INTELLIGENCE]] |
| PICA / root cause / improvement / business case | [[domains/06_PROBLEM_SOLVING_STRATEGY_BUSINESS_CASE]] | relevant business domain |
| Coaching / influence / meeting / change / presentation | [[domains/07_LEADERSHIP_PEOPLE_STAKEHOLDER]] | [[domains/06_PROBLEM_SOLVING_STRATEGY_BUSINESS_CASE]] |
| Cari contoh/case yang mirip | [[domains/08_CASE_MEMORY]] | relevant business domain |
| Tanya angka/formula | [[reference/CANONICAL_FORMULA_LIBRARY]] | relevant domain + current data |
| Tanya rule sekarang vs dulu | [[reference/CURRENTNESS_SUPERSESSION]] | [[reference/SOURCE_AUTHORITY]] |
| Source bertentangan / tidak jelas | [[reference/CONTRADICTION_UNRESOLVED]] | source-memory fallback |

## Actual/current business-state routes
| User intent | Primary current-state route | Rule |
|---|---|---|
| Latest M/S / 9 segment / kabupaten | `../business-memory/operational/CURRENT_OPERATING_STATE.md` + `MARKET_SHARE_YTD_JUN_2026_SEGMENT.tsv` | Require numerator + denominator + period; latest supplied market is Jun YTD. |
| Latest retail / dealer / area / type | `../business-memory/operational/RETAIL_CURRENT_STATE.md` + retail TSVs | Latest supplied retail is Jul 2026; raw PII is not public memory. |
| Latest dealer/MD stock / aging / stock-days | `../business-memory/operational/STOCK_CURRENT_STATE.md` + stock TSVs | Dealer aging available; MD aging unavailable. |
| Current Ring | `../business-memory/operational/RING_MAPPING_2022_HISTORICAL.tsv` | Must answer current authority unconfirmed; 2022 historical only. |
| Exact NOS mandatory item | `source-memory/NOS_2026_FIDELITY_CORRECTION.md` + row TSV | Mandatory comes from exact source Mandatory cell, never indicator-language inference. |
| MSW for date/product | `../business-memory/commercial/MSW_CURRENTNESS_RETRIEVAL.md` + resolver + applicable offer TSV | Reject invalid/superseded source; respect date interval. |
| Integrated TTM / POS coding / current POS readiness | `../business-memory/operational/INTEGRATED_TTM_POS_CURRENT_STATE_2026-08-11.md` + POS TSVs | Distinguish all-POS coverage mapping from Mega/Selected target input; preserve required-field/data-quality gaps; formal later AHM guidance may supersede. |


### Weekly market information / local event / Market Info Tools
Route to:
1. `domains/01_BUSINESS_SENSING_MARKET_INTELLIGENCE.md`
2. `modules/B01__MARKET_INFO_TOOLS_WEEKLY_SENSING_OPERATING_SYSTEM.md`
3. `../business-memory/operational/MARKET_INFO_TOOLS_CURRENT_STATE_2026-08-11.md`
4. `playbooks/B01__WEEKLY_MARKET_INFO_TO_PERFORMANCE_DIAGNOSIS.md` when linking event to performance

Guard: current source proves the weekly submission process, not actual historical event records. Do not expose access URLs/credentials.
