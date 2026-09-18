# AWD Capability Registry

## Purpose

Canonical discovery entrypoint for AIRO WorkDesk business queries.

AIRO Sync MUST resolve this registry before requesting user-provided data.

---

## Business Query Routing

For queries involving:

- Retail Sales
- Market Share
- Dealer Performance
- Territory
- Ring
- FLP Productivity
- Customer
- RO
- FINCO
- Product Performance

Default project:

AIRO_WORKDESK

---

## AWD Runtime Access & Consumption Interface

- **Status**: `AWD_RUNTIME_ACCESS_STATUS=AVAILABLE`
- **Runtime Location**: `VPS AWD Runtime` (Host: 43.157.241.228, VM-0-9-ubuntu)
- **Capability**: Fresh AI may request runtime query through approved interface (`awd-query`, `awd-remote-query`, or `AWD Runtime Access Bridge`).
- **Access Boundary**: Strictly read-only. Zero direct filesystem access claimed. No TSV mutation.
- **Verification**: Runtime health check available via `awd-health-check` or `GET /api/v1/health`.

---

## Operational Data Authorities

### Retail Sales Authority

Source (Operational Runtime):
- Monthly Operating Summary: wiki/workdesk/business-memory/operational/RETAIL_2026_CURRENT_SUMMARY.tsv
- Dealer Contribution Breakdown: wiki/workdesk/business-memory/operational/RETAIL_2026_YTD_JUL_DEALER.tsv
- Product Type Breakdown: wiki/workdesk/business-memory/operational/RETAIL_2026_YTD_JUL_TYPE.tsv
- Area Geographic Breakdown: wiki/workdesk/business-memory/operational/RETAIL_2026_YTD_JUL_AREA.tsv
- Historical 2025 Dealer Comparable: wiki/workdesk/business-memory/operational/RETAIL_2025_YTD_JUL_DEALER_HISTORICAL.tsv
- FY2025 Full-Year Baseline: wiki/workdesk/business-memory/operational/RETAIL_SALES_2025_FULL_YEAR_SUMMARY.md
- Ingestion Lineage: Operational TSVs originate from Private Raw Upstream Provenance (Retail Sales/SSU.2026.xlsx & SSU 2025.xlsx; raw customer PII excluded from ASB)

Coverage:
- Active 2026 operating period: Latest period resolved from runtime authority metadata
- Full Year 2025 historical baseline: Jan-Dec 2025 (107,108 units total, Dec 12,381 units)

Use:
- retail performance & growth rate evaluation
- dealer retail contribution and sales volume ranking
- product type contribution and area sales volume analysis

---

### Retail Intelligence Engine v2 Authority

Source:
wiki/workdesk/intelligence/RETAIL_INTELLIGENCE_ENGINE_V2.md
wiki/workdesk/reference/RETAIL_RAW_FIELD_INVENTORY.tsv

Coverage:
Unified Retail Sales Intelligence (2024, 2025, 2026) across 7 Domains (Sales, Dealer, Territory, Product, Financing, Customer Segment, FLP)

Use:
- cross-year retail sales comparability
- raw field schema resolution & PII storage boundary
- multi-domain intelligence routing

---

### Financing Intelligence Authority

Source:
wiki/workdesk/intelligence/FINANCING_INTELLIGENCE_V1.md
wiki/workdesk/intelligence/DEALER_FINANCING_CLASSIFICATION_MODEL.tsv
wiki/workdesk/business-memory/operational/FINANCING_2026_CURRENT_SUMMARY.tsv

Coverage:
Retail Financing Intelligence (2024, 2025, 2026) covering Cash vs Credit ratio, Finco market share, DP Real %, and Tenor distribution

Use:
- financing schema sensing
- Finco market share & partnership analysis
- DP % & tenor bucket evaluation
- dealer financing classification (CASH_DOMINANT, BALANCED_FINANCING, CREDIT_EXPANSION_OPPORTUNITY, HIGH_RISK_FINANCING_GAP)

---

### Product Intelligence Authority

Source:
wiki/workdesk/intelligence/PRODUCT_INTELLIGENCE_V1.md
wiki/workdesk/intelligence/PRODUCT_PORTFOLIO_CLASSIFICATION_MODEL.tsv
wiki/workdesk/business-memory/operational/PRODUCT_2026_CURRENT_SUMMARY.tsv

Coverage:
Retail Product Intelligence (2024, 2025, 2026) covering Model Volume Share, Segment Mix, Price Bands, and Facelift Transitions

Use:
- product performance & model mix analysis
- segment share sensing (Matik, Cub, Sport, EV)
- price band evaluation (ENTRY, MID, UPPER_MID, PREMIUM)
- product portfolio classification (BACKBONE_VOLUME_LEADER, GROWTH_LAUNCH_MODEL, NICHE_SPECIALTY_MODEL, PHASING_OUT_LEGACY)

---

### Customer Segment Intelligence Authority

Source:
wiki/workdesk/intelligence/CUSTOMER_SEGMENT_INTELLIGENCE_V1.md
wiki/workdesk/intelligence/CUSTOMER_SEGMENT_CLASSIFICATION_MODEL.tsv
wiki/workdesk/business-memory/operational/CUSTOMER_SEGMENT_2026_CURRENT_SUMMARY.tsv

Coverage:
Retail Customer Segment Intelligence (2024, 2025, 2026) covering Age Groups, Occupation Mix, Expenditure Tiers, and Repeat Order Ratios

Use:
- customer profile & demographic sensing
- occupation share & alias resolution
- expenditure tier evaluation
- repeat order (RO) vs first-time buyer analysis
- customer profile classification (YOUNG_COMMUTER, COMMERCIAL_AGRI_WORKER, FAMILY_STABILITY_BUYER, FLEET_CORPORATE_CLIENT)

---

### FLP Intelligence Authority

Source:
wiki/workdesk/intelligence/FLP_INTELLIGENCE_V1.md
wiki/workdesk/intelligence/DEALER_MANPOWER_PRODUCTIVITY_MODEL.tsv
wiki/workdesk/business-memory/operational/FLP_2026_CURRENT_SUMMARY.tsv
wiki/workdesk/intelligence/FLP_INTELLIGENCE.md (Legacy Reference)

Coverage:
Retail FLP & Manpower Productivity Intelligence (2024, 2025, 2026) covering Sales Force Headcount, NOS Role Benchmarks, Productivity Indexes, and Manpower Lifecycle

Use:
- manpower headcount & role mix evaluation (SALES_COUNTER, FIELD_SALES_CANVASSER, WING_SALES_PEOPLE, SPV_TL)
- NOS H1 People benchmark tracking & productivity index calculation
- FLP manpower lifecycle sensing (ACTIVE, NEW_ONBOARDING, DORMANT_INACTIVE)
- manpower performance classification (ABOVE_EXPECTATION, WITHIN_EXPECTATION, BELOW_EXPECTATION, CRITICAL_GAP)

---

### Customer Lifecycle Intelligence Authority

Source:
wiki/workdesk/intelligence/CUSTOMER_LIFECYCLE_INTELLIGENCE_V1.md
wiki/workdesk/intelligence/CUSTOMER_LIFECYCLE_MODEL.tsv
wiki/workdesk/business-memory/operational/CUSTOMER_LIFECYCLE_2026_CURRENT_SUMMARY.tsv

Coverage:
Retail Customer Lifecycle & Repurchase Intelligence (2024, 2025, 2026) covering Repeat Gap Months, Tenor Repurchase Behavior, Model Migration, and Dealer Retention

Use:
- repeat purchase analysis & repurchase timing distribution (Repeat Gap Months)
- ownership timeline tracking & sequence ordering (First Purchase vs Repeat Order)
- tenor-to-repurchase relationship evaluation (PREMATURE_UPGRADE, MATURITY_REPLACEMENT, DELAYED_RETENTION)
- model migration path sensing (SAME_MODEL_REFRESH, SEGMENT_UPGRADE, CROSS_SEGMENT_EXPANSION)
- dealer retention & POS migration analysis (DEALER_RETAINED, POS_MIGRATED, DEALER_SWITCHED)

---

### Sales Activity Intelligence Authority

Source:
wiki/workdesk/intelligence/SALES_ACTIVITY_INTELLIGENCE_V1.md
wiki/workdesk/intelligence/SALES_ACTIVITY_MODEL.tsv
wiki/workdesk/business-memory/operational/SALES_ACTIVITY_2026_CURRENT_SUMMARY.tsv
wiki/workdesk/brain/modules/B07__LEADS_MANAGEMENT_END_TO_END.md

Coverage:
Retail Sales Activity & Source of Sale Intelligence (2024, 2025, 2026) covering Lead Channels, Conversion Rates, Funnel Health, and FLP Activity Effectiveness

Use:
- lead source analysis & channel mix evaluation (WALK_IN, BTL_CANVASSING, BTL_EVENT, VIRTUAL_EXHIBITION, SOCIAL_MEDIA, APPS_REFERRAL, FINCOY, REPEAT_ORDER_CRM, CALL_WA)
- channel conversion rate tracking (Retail Deal / Total Leads)
- funnel health monitoring (Touchpoint -> Prospect -> Follow Up -> SPK -> Retail SSU)
- FLP activity effectiveness evaluation (NOS daily lead allocation SLA and contact rates)
- dealer acquisition performance and funnel bottleneck diagnosis

---

### Inventory Stock Intelligence Authority

Source:
- Intelligence Contract: wiki/workdesk/intelligence/INVENTORY_STOCK_INTELLIGENCE_V1.md
- Dealer Stock Granular Aging: wiki/workdesk/business-memory/operational/DEALER_STOCK_2026-08-06_AGGREGATE.tsv
- Main Dealer Warehouse Stock: wiki/workdesk/business-memory/operational/MD_STOCK_2026-08-06_AGGREGATE.tsv
- Dealer Stock Days Derived: wiki/workdesk/business-memory/operational/DEALER_STOCK_DAYS_2026-08-06_DERIVED.tsv
- Monthly Summary: wiki/workdesk/business-memory/operational/INVENTORY_STOCK_2026_CURRENT_SUMMARY.tsv
- Decision Model: wiki/workdesk/intelligence/INVENTORY_STOCK_MODEL.tsv
- Current State Note: wiki/workdesk/business-memory/operational/STOCK_CURRENT_STATE.md
- Ingestion Lineage: Operational TSVs originate from Private Raw Upstream Provenance (Stok_per_no_mesin_dealer & StokMD; raw engine identifiers excluded)

Coverage:
Retail Inventory Stock & Supply Intelligence (2024, 2025, 2026) covering granular dealer stock positions, MD stock, stock days, aging hazards (>150 Days), and demand vs supply bottleneck diagnosis

Use:
- stock availability monitoring & status breakdown (Ready, Soft Booking, Unfill, Intransit, MD Stock)
- stock days calculation and stock health evaluation (OPTIMAL, UNDER_STOCKED, OVER_STOCKED, CRITICAL_AGING)
- aging stock sensing (>150 days aging hazard)
- demand vs supply bottleneck diagnosis (Demand Problem vs Supply Bottleneck)

---

### Promotion Program Intelligence Authority

Source:
wiki/workdesk/intelligence/PROMOTION_PROGRAM_INTELLIGENCE_V1.md
wiki/workdesk/intelligence/PROMOTION_PROGRAM_MODEL.tsv
wiki/workdesk/business-memory/operational/PROMOTION_PROGRAM_2026_CURRENT_SUMMARY.tsv
wiki/workdesk/domains/pricing-financing/COMMERCIAL_PROGRAM_INTELLIGENCE.md

Coverage:
Retail Promotion & Commercial Sales Program Intelligence (2024, 2025, 2026) covering Program Adoption, Sales Uplift, Incremental Units, and Program Conversion Rates

Use:
- sales program monitoring & classification (VOUCHER_DISCOUNT, POTONGAN_ANGSURAN, POTONGAN_DP, DIRECT_GIFT_APPAREL, FINCOY_SUPPORT, LOYALTY_RETENTION_PROGRAM)
- dealer program adoption rate tracking (Participating Dealer / Total Dealer)
- promotion effectiveness & sales uplift analysis (Sales Uplift % & Incremental Units)
- program conversion rate evaluation (Claimed Retail Deals / Program Leads)
- multi-domain integration (Promotion + Sales Activity + Financing + Product + Retail Sales)

---

### Retail Diagnosis Engine Authority

Source:
wiki/workdesk/intelligence/RETAIL_DIAGNOSIS_ENGINE_V1.md
wiki/workdesk/intelligence/RETAIL_DIAGNOSIS_MODEL.tsv
wiki/workdesk/business-memory/operational/RETAIL_DIAGNOSIS_2026_CURRENT_SUMMARY.tsv
wiki/workdesk/playbooks/DIAGNOSE_BUSINESS_PROBLEM.md

Coverage:
Multi-Domain Retail Diagnosis & Prescriptive Action Engine (2024, 2025, 2026) combining 10 Retail Intelligence layers into evidence-based root cause diagnosis and PICA action recommendations

Use:
- multi-domain root cause diagnosis & evidence chain enforcement (FACT -> SYMPTOM -> HYPOTHESIS -> EVIDENCE -> ROOT CAUSE -> ACTION)
- business problem taxonomy classification (SALES_DROP, MARKET_SHARE_LOSS, STOCK_CONSTRAINT, PRODUCT_MISMATCH, CHANNEL_WEAKNESS, FLP_PRODUCTIVITY_GAP, FINANCING_BARRIER, PROMOTION_INEFFECTIVENESS, TERRITORY_OPPORTUNITY)
- demand vs supply bottleneck isolation (Stock Days < 10d vs > 20d & Aging > 150d)
- prescriptive PICA action recommendation (Initiative, PIC, Timeline, Leading Metric)

---

### AIRO Commercial Copilot Authority

Source:
wiki/workdesk/intelligence/AIRO_COMMERCIAL_COPILOT_V1.md
wiki/workdesk/intelligence/AIRO_COPILOT_ACTION_TRACKER.tsv
wiki/workdesk/business-memory/operational/AIRO_COPILOT_2026_CURRENT_SUMMARY.tsv
BUSINESS_PULSE.md
SIGNALS.md

Coverage:
AIRO Commercial Copilot Delivery & Interaction Layer (2024, 2025, 2026) orchestrating 11 underlying intelligence engines into role-tailored briefs, chat intent routing, and PICA action tracking

Use:
- role-based briefing (MANAGEMENT_EXECUTIVE, DEALER_HEAD, AREA_MANAGER_SPV, DEALER_OPERATION)
- chat intent routing & Natural Language Query parsing (DEALER_REVIEW, BUSINESS_DIAGNOSIS, TERRITORY_OPPORTUNITY, PROMOTION_ANALYSIS, INVENTORY_DIAGNOSIS, FLP_PRODUCTIVITY)
- evidence chain governance & output delivery (FACT -> DIAGNOSIS -> EVIDENCE -> ACTION -> MONITORING)
- PICA action tracking & resolution monitoring (AIRO_COPILOT_ACTION_TRACKER.tsv)
- executive pulse summary generation (BUSINESS_PULSE.md & SIGNALS.md)

---

### Market Share Authority

Source:
- Kabupaten & Segment Matrix: wiki/workdesk/business-memory/operational/MARKET_SHARE_YTD_JUN_2026_KABUPATEN_SEGMENT.tsv
- Province Segment Matrix: wiki/workdesk/business-memory/operational/MARKET_SHARE_YTD_JUN_2026_SEGMENT.tsv
- Strategic Analysis Memo: wiki/workdesk/business-memory/operational/MARKET_STRATEGIC_VIEW_YTD_JUN_2026.md
- Ingestion Lineage / Invariant: Private Raw Upstream Provenance (Market/SINSEN_EVALPOLREG+MSPERKAB_JUN 2026.xlsx)

Coverage:
YTD Jan-Jun 2026 vs Jan-Jun 2025 comparable across 9 Kabupaten & 9 Segmen (ALL, MATIK, SPORT, CUB, etc.)

Use:
- market share calculation and YoY growth comparison
- product segment share and mix analysis
- kabupaten-level market contribution and share gap identification

---

### Territory Authority

Source:
- Master Area Hierarchy (1,222 rows): wiki/workdesk/business-memory/operational/POLREG_2026_AREA_HIERARCHY.tsv
- Dense Geography Matrix (14,849 rows): wiki/workdesk/business-memory/operational/POLREG_YTD_JUN_2026_GEOGRAPHY_SEGMENT.tsv
- Retrieval Specification: wiki/workdesk/business-memory/operational/POLREG_GEOGRAPHIC_FILTER_RETRIEVAL.md
- Ingestion Lineage / Invariant: Private Raw Upstream Provenance (Market/POLREG PER KECAMATAN PER KELURAHAN PER SEGMENT 2026.xlsx)

Coverage:
9 Kabupaten, 118 Kecamatan, 1,222 terpetakan Kelurahan-Desa across 11 Filter States (ALL SEG, 9 named segments, OTHERS)

Retrieval Rule:
Resolve hierarchy (POLREG_2026_AREA_HIERARCHY.tsv) before dense geography matrix query.

Use:
- geographic boundary and territory hierarchy resolution
- micro-territory segment market penetration and whitespace analysis
- coverage mapping down to kelurahan/desa grain

---

### Dealer Network Authority

Hierarchy:

Dealer Group
↓
Dealer
↓
POS
↓
FLP

Use:
- ownership attribution
- dealer responsibility
- performance diagnosis

---

### Historical Ring Mapping Authority

Source:
wiki/workdesk/business-memory/operational/RING_MAPPING_2022_HISTORICAL.tsv

Coverage:
802 rows covering Kabupaten, Kecamatan, Dealer/POS, and Ring Status (Ring 1, Ring 2, Ring 3)

Use:
- historical ring status reference
- dealer/POS core vs expansion territory baseline
- cross-validation against current territory coverage model

---

## Resolution Rule

Before saying:

"I don't have data"

AIRO Sync MUST check:

1. AWD Capability Registry
2. Operational Data Inventory
3. Source Authority

If available:

AWD_CAPABILITY_RESOLUTION=PASS

Proceed analysis.

Only if unavailable:

DATA_AUTHORITY_STATUS=NOT_FOUND

---

## Expected Resolution

Example:

AWD_CAPABILITY_RESOLUTION=PASS

AVAILABLE_AUTHORITIES:
- Retail Sales
- Market Share
- POLREG
- Dealer Network

NEXT:
Proceed analysis

---

### Dealer Classification Authority

Source:
wiki/workdesk/intelligence/RETAIL_DEALER_INTELLIGENCE_V1.md
wiki/workdesk/intelligence/DEALER_RETAIL_CLASSIFICATION_MODEL.tsv

Coverage:
Dealer & POS Retail Classification (BACKBONE, GROWTH_OPPORTUNITY, ATTENTION)

Use:
- Backbone dealer identification
- Growth opportunity detection
- Attention & corrective action routing

---

### Territory Coverage Authority

Source:
wiki/workdesk/intelligence/TERRITORY_INTELLIGENCE_V1.md
wiki/workdesk/intelligence/TERRITORY_COVERAGE_CLASSIFICATION_MODEL.tsv

Coverage:
Kabupaten & Kecamatan Territory Classification (BACKBONE, GROWTH_OPPORTUNITY, ATTENTION)

Use:
- Backbone kecamatan identification
- Growth opportunity territory routing
- White-space / attention territory action mapping
