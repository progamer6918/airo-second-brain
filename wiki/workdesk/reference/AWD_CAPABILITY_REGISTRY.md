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

## Operational Data Authorities

### Retail Sales Authority

Source:
Retail Sales/SSU.2026.xlsx

Coverage:
Jan-Jul 2026 aggregate (Current Operating Authority)
Full Year 2025 Baseline (107,108 units - Historical Authority)

Use:
- retail performance
- dealer contribution
- area analysis

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
wiki/workdesk/intelligence/INVENTORY_STOCK_INTELLIGENCE_V1.md
wiki/workdesk/intelligence/INVENTORY_STOCK_MODEL.tsv
wiki/workdesk/business-memory/operational/INVENTORY_STOCK_2026_CURRENT_SUMMARY.tsv
wiki/workdesk/business-memory/operational/STOCK_CURRENT_STATE.md

Coverage:
Retail Inventory Stock & Supply Intelligence (2024, 2025, 2026) covering Stock Position, Stock Days, Dealer Stock Aging (>150 Days), and Demand vs Supply Bottleneck Diagnosis

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

### Market Share Authority

Source:
Market/SINSEN_EVALPOLREG+MSPERKAB_JUN 2026.xlsx

Coverage:
YTD Jan-Jun 2026

Use:
- market share
- segment analysis
- kabupaten comparison

---

### Territory Authority

Source:
Market/POLREG PER KECAMATAN PER KELURAHAN PER SEGMENT 2026.xlsx

Coverage:
118 kecamatan / 1,223 mapped kelurahan-desa rows

Use:
- ring mapping
- coverage
- whitespace opportunity

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
