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
| “Market share 2025 / histori 2025” | [[intelligence/MARKET_SHARE_2025_HISTORICAL_RECOVERY]] |
| “Sales turun” | [[playbooks/DIAGNOSE_BUSINESS_PROBLEM]] + [[business/SALES_STOCK_DISTRIBUTION]] |
| “Activity banyak tapi hasil kecil” | [[playbooks/HIGH_ACTIVITY_LOW_RESULT]] |
| “Dealer nggak perform” | [[playbooks/DEALER_REVIEW]] + [[network/NOS_2026_CORE]] jika execution standard relevan |
| “Sales people rendah” | [[business/SALES_FORCE_PRODUCTIVITY]] |
| “AT High kalah” | [[playbooks/AT_HIGH_UNDERPERFORMANCE]] |
| “Mau audit/gap NOS” | [[playbooks/NOS_DIAGNOSIS]] |
| “Gue belum tahu masalahnya apa” | [[playbooks/DIAGNOSE_BUSINESS_PROBLEM]] |

## Output routes (Deliverable Mode)

| Output | Route | Deliverable Blueprint |
|---|---|---|
| Dealer Review | [[playbooks/DEALER_REVIEW]] | [[deliverables/DEALER_REVIEW]] |
| PICA / Action Plan | [[frameworks/PROBLEM_SOLVING_SYSTEM]] | [[deliverables/PICA]] |
| Business Case | [[playbooks/DIAGNOSE_BUSINESS_PROBLEM]] | [[deliverables/BUSINESS_CASE]] |
| Market / Area Brief | [[business/MARKET_INTELLIGENCE]] | [[deliverables/MARKET_BRIEF]] |
| PPT / Management Review | [[presentation/AHM_REVIEW_AND_PRESENTATION]] | [[deliverables/MANAGEMENT_REVIEW]] |
| Data Validation Checklist | [[analytics/DATA_ANALYTICS_POWER_BI]] | [[deliverables/DATA_VALIDATION]] |
| Dealer / Management Communication | [[playbooks/DEALER_REVIEW]] | [[deliverables/COMMUNICATION]] |
| Meeting Preparation Brief | [[playbooks/DEALER_REVIEW]] | [[deliverables/MEETING_PREP]] |

## AI Context Loading Rule

Load WorkDesk core boot first, lalu modul relevan berdasarkan rute di atas. Tidak perlu memuat seluruh 103 berkas sumber ke dalam konteks.
