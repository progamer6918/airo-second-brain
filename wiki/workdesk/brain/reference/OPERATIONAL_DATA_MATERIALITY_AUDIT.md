# Operational Data Materiality Audit — Remediation v0.2

## New materiality rule
`Dense table` is not a blanket reason to omit structured memory. Classify rows/fields by decision value.

### A. Low-value/decorative/repetitive detail
May remain in original-source evidence when it does not materially change a WorkDesk decision and can be regenerated or re-read when exceptionally needed. Examples: duplicate visual renderings, layout-only repetitions, raw presentation images, redundant row formatting.

### B. Decision-grade business facts
Must be retained in structured, queryable memory with period and provenance. This includes current market denominators/share, 9-segment state, retail actual, dealer/area/type drill-down, stock status/aging, current program applicability, territory mappings with currentness labels, and NOS mandatory gates.

## Privacy rule
Customer names, KTP/ID, addresses, phone numbers, engine-number detail, and comparable raw identifiers stay out of public ASB. Their analytical contribution is preserved only through sanitized/aggregated memory.

## Topic decisions
| Topic | Material structured memory | Currentness treatment |
|---|---|---|
| Market share | Honda numerator, total-market denominator, M/S, PY comparable, Δ share points, 9 segments, full decision-grade Kabupaten → Kecamatan → Kelurahan/Desa filtered drill-down, plus source-specific classification boundary | Latest supplied: YTD Jan-Jun 2026 |
| Retail | Monthly/YTD actual, dealer/area/type aggregates, historical comparable | Latest supplied: Jul 2026 |
| Dealer stock | status, dealer, aging, derived stock-days with exact formula | As of 2026-08-06 08:03:42 |
| MD stock | type/status/location aggregate | As of 2026-08-06 08:04:46; aging unavailable |
| Ring | dealer/POS ↔ geography ↔ Ring mapping | Historical 2022 only; current authority unconfirmed |
| NOS | exact physical row hierarchy, indicator, mandatory tier, scoring gates | NOS 2026 current supplied baseline |
| MSW | requested-date applicability, revisions/invalidations, current structured offers | Jan-Aug 2026 supplied; Aug current supplied period |

## Geographic drill-down rule
When the operational workbook itself exposes meaningful segment-filtered geography below kabupaten, `dense table` is not a reason to omit it. Preserve the sanitized aggregate query surface and provenance; do not copy raw binaries.
