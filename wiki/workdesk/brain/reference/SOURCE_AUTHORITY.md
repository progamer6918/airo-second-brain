# Source Authority Resolver

Use this before applying a dated/current rule. The underlying TSV is the machine-friendly canonical matrix.

| topic | authority_class | preferred_authority | lower_or_historical_authority | resolver_rule |
|---|---|---|---|---|
| NOS current network standard | CURRENT | NOS 2026 workbook set / change-control workbook | NOS 2023 deck + workbook | 2026 supersedes 2023 for current checklist/scoring; 2023 retained as lineage |
| Network development / Reshape | CURRENT_2026 | ND Plan & Reshape Review 2026 + NetDev Strategy 2026 + latest applicable BEST 2026 | earlier BEST 2025/early-2026 | Use latest applicable operating meeting for period-specific status |
| BTL current network/activity standard | CURRENT_2026 | NOS BTL 2026 + latest applicable BEST 2026 | 2022/2023 BTL letters | Old quotas/financial terms/COVID clauses historical only |
| Virtual Exhibition operating guidance | LATEST_AVAILABLE_NOT_CONFIRMED_CURRENT | 2025 NMS/survey guidance; 2024 plan for KPI model | 2022 VE/SAFARI | No supplied 2026 VE authority |
| CRM methods | DURABLE_METHOD_WITH_VERSIONED_WORKFLOW | 2024 CRM training for CDB/lead logic; newer 2026 system facts if available | older workflow-specific tool/cadence | Tool names, allocation and follow-up cadence are version-sensitive |
| Target / Forecast / Dealer Review | DURABLE_METHOD | ASSDP target/dealer review/demand sources + workbook logic | historical examples | Current target values must come from current business data |
| Niguri | HISTORICAL_METHOD_PENDING_CURRENT_SCHEDULE_AUTHORITY | Niguri 2023 deck for planning concept | conflicting schedule in same slide | Planning method usable; exact current submission calendar unresolved |
| Sales / Stock monitoring | DURABLE_METHOD_PLUS_CURRENT_DATA | ASSDP monitoring deck + current business-memory snapshots | historical sample values | Method stable; actual state must resolve by requested date |
| Pricing / FID / BA | DURABLE_FORMULAS_WITH_HISTORICAL_THRESHOLDS | ASSDP pricing/FID-BA deck for DP Real/FID/BA definitions | 2023 thresholds | Current lender/program thresholds require current authority |
| Commercial program / MSW | TIME_BOUND_CURRENTNESS_RESOLVER | formal applicable Juklak / revisions by requested date | superseded/not-valid program files | August 2026 latest supplied baseline; resolve exact requested date |
| Market share actual | CURRENT_DATA_REQUIRED | same-period brand volume + total-market denominator | older denominator | Never mix Honda current volume with unavailable/different-period denominator |
| Ring mapping | HISTORICAL_UNTIL_CONFIRMED | 2022 ring map | none newer supplied | Do not assume current territory ring without confirmation |
| FLP uniform | LATEST_SUPPLIED_NOT_CONFIRMED_CURRENT | 5 Jun 2025 instruction | older appearance guidance | Verify unsuperseded before current enforcement |
| Leadership/coaching/negotiation/problem solving | DURABLE_METHOD | ASSDP Basic/Intermediate/Advance training sources | training timings/examples | Methods reusable; timing/example claims not universal |

## Remediation v0.2 — decision-grade operational authority
| topic | latest supplied authority | period/as-of | rule |
|---|---|---|---|
| Market share actual | SINSEN_EVALPOLREG+MSPERKAB_JUN 2026.xlsx raw databases | YTD Jan-Jun 2026 | Use same-period Honda numerator + total-market denominator; 2025 comparable derived Jan-Jun from raw DB because summary label conflicts. |
| Retail actual | SSU.2026.xlsx aggregate memory | through Jul 2026 | Current 2026 authority. Raw customer PII excluded. |
| Retail comparable (FY2025) | SSU 2025 Full Year Summary / WD-SRC-057 | Jan-Dec 2025 | Preferred full-year historical comparable baseline (107,108 units). |
| Retail comparable | Record Sales 2008-2025.xlsx / Monthly | Jan-Jul 2025 | Use only as historical comparable; do not use stale cached 2026 cells. |
| Dealer stock | Stok_per_no_mesin_dealer - 2026-08-06T080342.480.xls | 2026-08-06 08:03:42 | Aggregate status/aging; raw engine identifiers excluded. |
| MD stock | StokMD - 2026-08-06T080446.204.xls | 2026-08-06 08:04:46 | Status/type/location available; aging absent. |
| Ring mapping | MAPPING RING 2022/Summary Pembagian Ring.xlsx | 2022 | Historical only; current authority unconfirmed. |
| NOS 2026 mandatory | Original 2026 checklist workbooks | 2026 supplied baseline | Use exact physical-row Mandatory cells; do not infer from indicator text. |
| MSW | 2026-MSW source tree + resolver | requested date Jan-Aug 2026 | Explicit invalidation/revision and effective date control; current Aug workbook numeric rows structured separately. |

| POLREG geographic market drill-down | POLREG PER KECAMATAN PER KELURAHAN PER SEGMENT 2026.xlsx / Data + 9 geography sheets | YTD Jan-Jun 2026 | Current deep-geography authority for segment-filtered Kabupaten/Kecamatan/Kelurahan-Desa retrieval. Preserve source-specific classification differences vs dedicated M/S workbook. |
| Integrated TTM / POS current | 6-Aug-2026 NetDev meeting + clean MoM; Sinsen 11-Aug-2026 POS working snapshot | 2026-08-06 / 2026-08-11 | Meeting governs current supplied TTM logic; local workbook governs supplied Sinsen POS working state; formal later AHM guidance supersedes if supplied; do not infer submission completion. |

| Market Info Tools | 2026-08-11 Sinsen meeting transcript (first 30 min) + 2 screenshots | weekly field-market sensing / transitional submission workflow | CURRENT_SUPPLIED_PARTIAL_MEETING | Use for current weekly workflow and feature boundaries; transcript is incomplete after 30 min; access URLs/credentials excluded; later formal AHM guidance supersedes if supplied |

| Dealer performance classification | RETAIL_DEALER_INTELLIGENCE_V1.md / DEALER_RETAIL_CLASSIFICATION_MODEL.tsv | FY2025 / 2026 | Decision-support intelligence layer classifying BACKBONE, GROWTH_OPPORTUNITY, ATTENTION dealers. |

| Territory coverage classification | TERRITORY_INTELLIGENCE_V1.md / TERRITORY_COVERAGE_CLASSIFICATION_MODEL.tsv | POLREG 2026 / FY2025 | Decision-support intelligence layer classifying territory penetration & ring coverage. |
| Retail Intelligence Engine v2 | RETAIL_INTELLIGENCE_ENGINE_V2.md / RETAIL_RAW_FIELD_INVENTORY.tsv | 2024-2026 | Multi-domain retail intelligence architecture defining raw vs sanitized separation and 7-domain hierarchy. |
| Financing performance classification | FINANCING_INTELLIGENCE_V1.md / DEALER_FINANCING_CLASSIFICATION_MODEL.tsv | 2024-2026 | Decision-support intelligence layer classifying CASH_DOMINANT, BALANCED_FINANCING, CREDIT_EXPANSION_OPPORTUNITY, HIGH_RISK_FINANCING_GAP dealers and Finco shares. |
| Product performance classification | PRODUCT_INTELLIGENCE_V1.md / PRODUCT_PORTFOLIO_CLASSIFICATION_MODEL.tsv | 2024-2026 | Decision-support intelligence layer classifying BACKBONE_VOLUME_LEADER, GROWTH_LAUNCH_MODEL, NICHE_SPECIALTY_MODEL, PHASING_OUT_LEGACY model types and segment shares. |
| Customer segment classification | CUSTOMER_SEGMENT_INTELLIGENCE_V1.md / CUSTOMER_SEGMENT_CLASSIFICATION_MODEL.tsv | 2024-2026 | Decision-support intelligence layer classifying YOUNG_COMMUTER, COMMERCIAL_AGRI_WORKER, FAMILY_STABILITY_BUYER, FLEET_CORPORATE_CLIENT buyer profiles and demographics. |
| FLP manpower productivity classification | FLP_INTELLIGENCE_V1.md / DEALER_MANPOWER_PRODUCTIVITY_MODEL.tsv | 2024-2026 | Decision-support intelligence layer classifying ABOVE_EXPECTATION, WITHIN_EXPECTATION, BELOW_EXPECTATION, CRITICAL_GAP sales force productivity and NOS benchmarks. |
| Customer lifecycle & repurchase classification | CUSTOMER_LIFECYCLE_INTELLIGENCE_V1.md / CUSTOMER_LIFECYCLE_MODEL.tsv | 2024-2026 | Decision-support intelligence layer classifying PREMATURE_UPGRADE, MATURITY_REPLACEMENT, DELAYED_RETENTION customer repurchase behavior and ownership timelines. |
| Sales activity & channel conversion classification | SALES_ACTIVITY_INTELLIGENCE_V1.md / SALES_ACTIVITY_MODEL.tsv | 2024-2026 | Decision-support intelligence layer classifying lead channel performance, conversion rates, funnel health, and FLP lead SLA effectiveness. |
| Inventory stock & supply health classification | INVENTORY_STOCK_INTELLIGENCE_V1.md / INVENTORY_STOCK_MODEL.tsv | 2024-2026 | Decision-support intelligence layer classifying OPTIMAL_STOCK_HEALTH, UNDER_STOCKED_BOTTLENECK, OVER_STOCKED_SURPLUS, CRITICAL_AGING_HAZARD dealer stock positions and stock days. |
| Promotion & sales program effectiveness classification | PROMOTION_PROGRAM_INTELLIGENCE_V1.md / PROMOTION_PROGRAM_MODEL.tsv | 2024-2026 | Decision-support intelligence layer classifying VOUCHER_DISCOUNT, POTONGAN_ANGSURAN, POTONGAN_DP, DIRECT_GIFT_APPAREL, FINCOY_SUPPORT, LOYALTY_RETENTION_PROGRAM sales program effectiveness and sales uplift. |
| Retail multi-domain diagnosis & PICA classification | RETAIL_DIAGNOSIS_ENGINE_V1.md / RETAIL_DIAGNOSIS_MODEL.tsv | 2024-2026 | Level 3 Prescriptive Reasoning Synthesizer engine combining 10 retail intelligence domains into evidence-based root cause diagnosis and PICA action recommendations. |
