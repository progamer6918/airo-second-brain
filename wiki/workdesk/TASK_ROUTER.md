---
type: workdesk-router
project: AIRO_WORKDESK
workdesk_status: ACTIVE
audience: human-ai
---
# 🧭 WorkDesk Task Router

User cukup menyebut gejala atau output. Tidak perlu tahu nama framework.

## Problem routes

| Bahasa user | Route |
|---|---|
| “Market share turun” | [[playbooks/MARKET_SHARE_DOWN]] |
| “Sales turun” | [[playbooks/DIAGNOSE_BUSINESS_PROBLEM]] + [[business/SALES_STOCK_DISTRIBUTION]] |
| “Activity banyak tapi hasil kecil” | [[playbooks/HIGH_ACTIVITY_LOW_RESULT]] |
| “Dealer nggak perform” | [[playbooks/DEALER_REVIEW]] + [[network/NOS_2026_CORE]] jika execution standard relevan |
| “Sales people rendah” | [[business/SALES_FORCE_PRODUCTIVITY]] |
| “AT High kalah” | [[playbooks/AT_HIGH_UNDERPERFORMANCE]] |
| “Mau audit/gap NOS” | [[playbooks/NOS_DIAGNOSIS]] |
| “Gue belum tahu masalahnya apa” | [[playbooks/DIAGNOSE_BUSINESS_PROBLEM]] |

## Output routes

| Output | Route |
|---|---|
| Dealer Review | [[playbooks/DEALER_REVIEW]] |
| PICA/RCA/PDCA/DMAIC | [[frameworks/PROBLEM_SOLVING_SYSTEM]] |
| PPT / management review | [[presentation/AHM_REVIEW_AND_PRESENTATION]] |
| Excel / Power BI | [[analytics/DATA_ANALYTICS_POWER_BI]] |
| Market research | [[business/MARKET_INTELLIGENCE]] |
| Target/forecast | [[business/TARGETING_FORECASTING]] + [[business/DEMAND_MANAGEMENT]] |

## AI rule

Load WorkDesk core boot first, then task modules. `100% knowledge available` never means all raw sources must be loaded into context every turn.
