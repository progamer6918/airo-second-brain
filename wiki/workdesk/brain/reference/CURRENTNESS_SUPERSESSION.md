# Currentness & Supersession Resolver

Resolve requested date → applicable authority → supersession/conflict state. Historical examples remain queryable but are not current defaults.

| topic | period | source_family | status | rule |
|---|---|---|---|---|
| NOS | 2023 | NOS deck + Regular H123 workbook | HISTORICAL | Superseded for current operational questions by 2026 workbook set |
| NOS | 2026 | 00 comparison + tier checklists + POS + BTL | CURRENT_SUPPLIED | Current baseline authority |
| BEST | 2025 Oct-Dec | monthly closing decks | HISTORICAL | Cadence/trend only |
| BEST | 2026 Jan-Jun | monthly decks | HISTORICAL_PERIOD_SPECIFIC | Use only for its month; later source supersedes for current status |
| BEST | 2026 Jul | BEST July 2026 | LATEST_SUPPLIED_IN_CLUSTER | Use for Jul/Aug context where applicable |
| VE | 2022 | VE/SAFARI | HISTORICAL | Lead-flow lineage |
| VE | 2024 | Guidance/plan | HISTORICAL_LATEST_KPI_MODEL_BEFORE_2025 | Do not promote targets to 2026 |
| VE | 2025 | NMS survey guidance + survey | LATEST_AVAILABLE_NOT_CONFIRMED_CURRENT | No 2026 source supplied |
| MSW | 2026 Jan-Aug | formal Juklak / revisions | VERSIONED_TIME_BOUND | Resolve by exact date; invalid/superseded files rejected |
| Ring mapping | 2022 | territory ring map | HISTORICAL | Current applicability unconfirmed |
| Pricing FID/BA thresholds | 2023 | training deck thresholds | HISTORICAL | Definitions retained; threshold currentness not assumed |
| Niguri schedule | 2023 | Niguri deck | UNRESOLVED_CONFLICT | Exact schedule must use current authority |
| FLP uniform | 2025-06-05 | uniform instruction | LATEST_SUPPLIED_NOT_CONFIRMED_CURRENT | Verify if current |

| Integrated TTM / POS | 2026-08-06 meeting + 2026-08-11 Sinsen working file | NetDev meeting + clean MoM + POS standardization workbook | CURRENT_SUPPLIED_WITH_POST_MEETING_GUIDANCE_BOUNDARY | Use for current supplied TTM/POS logic; formal later AHM guidance supersedes if supplied; submission completion not inferred |
## Operational-state additions — remediation v0.2
- `MARKET_SHARE_CURRENT = YTD_JAN_JUN_2026`; do not imply Jul/Aug market data were supplied.
- `RETAIL_CURRENT = THROUGH_JUL_2026`.
- `DEALER_STOCK_CURRENT = 2026-08-06T08:03:42`; `MD_STOCK_CURRENT = 2026-08-06T08:04:46`.
- `RING_CURRENT = UNCONFIRMED`; latest supplied Ring mapping is 2022 historical.
- `MSW_CURRENT_SUPPLIED = AUG_2026`; still resolve exact requested date/family using the version resolver.
- Cross-topic latest periods are asynchronous; never merge them into a same-date observation without explicitly saying so.

- `POLREG_GEOGRAPHIC_CURRENT = YTD_JAN_JUN_2026`; deep geography/segment filtered view comes from the supplied POLREG 2026 workbook.
- Do not treat small segment-classification differences between POLREG and the dedicated M/S workbook as an error to silently repair; resolve by question/source authority.

- `MARKET_INFO_TOOLS_WORKFLOW_CURRENT = 2026-08-11 supplied Sinsen rollout`; current flow includes temporary MD Google Form validation before dealer portal submission.
- `MARKET_INFO_TOOLS_TARGET_FLOW = DIRECT_PORTAL_AFTER_CAPABILITY_MATURITY`; this is intended future state, not current proven workflow.
- `MARKET_INFO_EVENT_HISTORY = NOT_SUPPLIED`; process knowledge must not be mistaken for actual weekly field-event data.
