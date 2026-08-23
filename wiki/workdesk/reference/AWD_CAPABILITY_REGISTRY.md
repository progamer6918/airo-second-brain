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
