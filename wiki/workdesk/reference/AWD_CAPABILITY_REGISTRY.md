---
type: workdesk-registry
project: AIRO_WORKDESK
workdesk_status: ACTIVE
audience: human-ai
---

# 🧭 AWD Capability Registry & Discovery Router

## 1. Market Share Authority Routing

| Authority Scope | Primary Source / Contract | Coverage Period | Retrieval Target |
|---|---|---|---|
| **Current 2026 YTD Market Authority** | `SINSEN_EVALPOLREG+MSPERKAB_JUN 2026.xlsx` | Jan-Jun 2026 YTD | `wiki/workdesk/business-memory/operational/MARKET_SHARE_YTD_JUN_2026_KABUPATEN_SEGMENT.tsv` |
| **Historical 2025 Market Authority** | `MARKET_SHARE_2025_HISTORICAL_RECOVERY.md` | Jan-Dec 2025 FY | `wiki/workdesk/intelligence/MARKET_SHARE_2025_HISTORICAL_RECOVERY.md` |

## 2. Query Routing Rules
- **Monthly / Annual 2025**: Route to `MARKET_SHARE_2025_HISTORICAL_RECOVERY.md` (FY 127,244 units)
- **Brand / Competitor 2025**: Route to `MARKET_SHARE_2025_HISTORICAL_RECOVERY.md` (Honda 103,182 / 81.09%, Yamaha 23,261 / 18.28%)
- **Micro-Geography 2025 (Area ID)**: Route to Private Sidecar `~/.config/airo-workdesk/market/2025/foundation_2_micro_geo_fact.ndjson`
- **Model Type Market 2025**: Route to Private Sidecar `~/.config/airo-workdesk/market/2025/foundation_1_type_kabupaten_fact.ndjson`
