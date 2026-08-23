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
