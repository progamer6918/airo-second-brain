---
title: "AIRO Commercial Copilot Layer v1"
component: "AIRO Commercial Copilot"
status: "APPROVED / CANONICAL"
version: "1.0"
parent_contract: "wiki/workdesk/intelligence/RETAIL_DIAGNOSIS_ENGINE_V1.md"
foundation_engine: "wiki/workdesk/intelligence/RETAIL_INTELLIGENCE_ENGINE_V2.md"
reference_playbooks: "B01_B02__DEALER_REVIEW.md, B08__SPV_AREA_PLAYBOOK.md, BUSINESS_PULSE.md, SIGNALS.md"
last_updated: "2026-08-23"
---

# 🤖 AIRO Commercial Copilot Layer v1

## 1. Purpose & Overview

AIRO Commercial Copilot Layer v1 berfungsi sebagai **Lapisan Interaksi Pengguna & Orkes Penyampaian Inteligensi (User-Facing Delivery & Interaction Layer)** teratas di dalam ekosistem **AIRO WorkDesk (AWD)**.

Copilot ini mengorkestrasi keluaran analitik dari 10 domain inteligensi retail (`RETAIL_INTELLIGENCE_ENGINE_V2.md`) dan mesin penalaran diagnostik (`RETAIL_DIAGNOSIS_ENGINE_V1.md`) untuk disajikan secara personal (*Role-Based Personalization*) kepada pengguna manusia (*Management Executive, Dealer Head, Area Manager, Dealer Operations*). Copilot ini tidak menggantikan sistem operasional NMS/CRM, melainkan mengotomatiskan pembuatan ringkasan eksekutif, diary strategi diler (*Dealer Review*), penelusuran intent chat, dan pelacakan tindakan korektif PICA.

---

## 2. Architecture Position

AIRO Commercial Copilot v1 beroperasi di puncak hirarki arsitektur inteligensi retail:

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                      Retail Intelligence Engine v2                      │
│                  (wiki/workdesk/intelligence/RETAIL_INTELLIGENCE_ENGINE_V2.md) │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (10 Child Domain Facts)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      Retail Diagnosis Engine v1                         │
│             (wiki/workdesk/intelligence/RETAIL_DIAGNOSIS_ENGINE_V1.md)  │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (Reasoning & Root Cause Rules)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    AIRO Commercial Copilot Layer v1                     │
│           (wiki/workdesk/intelligence/AIRO_COMMERCIAL_COPILOT_V1.md)   │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (Intent Routing & Role Briefs)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                               Human User                                │
│       [Management] ─── [Dealer Head] ─── [SPV Area] ─── [Operations]    │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. User Persona Mapping & Output Governance

Copilot mengadaptasi format dan kedalaman informasi sesuai dengan peranan pengguna:

### 3.1 `MANAGEMENT_EXECUTIVE` (BOD, GM Sales, Marketing Head)
- **Fokus Utama**: Kesehatan bisnis makro, pergeseran market share, dan risiko komersial utama.
- **Standar Output**: Executive Pulse, Macro Risk Radar, Regional Opportunity, Strategic Resource Action.
- **File Referensi**: `BUSINESS_PULSE.md`, `SIGNALS.md`, `MARKET_STRATEGIC_VIEW_YTD_JUN_2026.md`.

### 3.2 `DEALER_HEAD` (Kepala Cabang Dealer / Kacab)
- **Fokus Utama**: Diary strategi diler bulanan, evaluasi pencapaian target, dan masalah operasional lokal.
- **Standar Output**: Form Dealer Review Brief, Product Mix Target vs Actual, FLP Productivity Index, Stock Days & Aging Risk, PICA Action Items.
- **File Referensi**: `B01_B02__DEALER_REVIEW.md`, `Form Dealer Review.xlsx`.

### 3.3 `AREA_MANAGER_SPV` (Supervisor Area Main Dealer)
- **Fokus Utama**: Pemetaan potensi wilayah 9 area, perbandingan antar-diler, dan penetrasi kecamatan.
- **Standar Output**: Territory Review, Kecamatan Whitespace Ring 2-3 Opportunity, Dealer Benchmark Matrix, Area Action Plan.
- **File Referensi**: `B08__SPV_AREA_PLAYBOOK.md`, `B05__ND_PLAN_REVIEW_PLAYBOOK.md`.

### 3.4 `DEALER_OPERATION` (Sales Counter, Canvasser, Admin CRM)
- **Fokus Utama**: Eksekusi harian, kuota prospek harian NOS, follow-up SLA prospek digital, dan pembersihan stok.
- **Standar Output**: Daily Execution Checklist, Priority Lead List, Lead Contact SLA Alert, Stock Clearance Unit Focus.
- **File Referensi**: `B07__LEADS_MANAGEMENT_END_TO_END.md`, `B04__NOS_CURRENT_2026.md`.

---

## 4. Chat Intent Mapping & Routing Engine

Copilot mengenali intent pertanyaan pengguna dalam bahasa natural dan mengarahkan ke modul analitik yang tepat:

| Contoh Input Chat / Pertanyaan User | Intent Code | Target Engine / Capabilities | Output Format AIRO |
|---|---|---|---|
| *"Review diler Citra Lencana Bangko"* / *"Cek performa dealer X"* | `DEALER_REVIEW` | `RETAIL_DEALER_INTELLIGENCE_V1` + `FLP_INTELLIGENCE_V1` | Form Dealer Review Executive Brief |
| *"Kenapa sales turun bulan ini?"* / *"Analisis penyebab retail drop"* | `BUSINESS_DIAGNOSIS` | `RETAIL_DIAGNOSIS_ENGINE_V1` (Multi-Domain RCA) | 6-Stage Evidence Chain Diagnosis |
| *"Cari opportunity wilayah Merangin"* / *"Kecamatan mana yang bisa naik?"* | `TERRITORY_OPPORTUNITY` | `TERRITORY_INTELLIGENCE_V1` (Ring 2-3 Coverage) | Territory Whitespace Opportunity Map |
| *"Program mana yang paling efektif?"* / *"Apakah promo diskon berefek?"* | `PROMOTION_ANALYSIS` | `PROMOTION_PROGRAM_INTELLIGENCE_V1` | Sales Uplift % & Incremental Units |
| *"Stock issue dimana aja?"* / *"Model apa yang krisis stok?"* | `INVENTORY_DIAGNOSIS` | `INVENTORY_STOCK_INTELLIGENCE_V1` | Stock Days & Aging $>150$d Risk Alert |
| *"Siapa FLP paling produktif?"* / *"Cek kontribusi salesman counter vs canvasser"* | `FLP_PRODUCTIVITY` | `FLP_INTELLIGENCE_V1` + `SALES_ACTIVITY_INTELLIGENCE_V1` | FLP Productivity Index & Lead SLA |

---

## 5. Output Governance & Evidence Chain Rule

Setiap rekomendasi yang dihasilkan oleh Commercial Copilot **WAJIB MENGIKUTI** tata kelola 5-tahap penyampaian:

$$\text{FACT} \longrightarrow \text{DIAGNOSIS} \longrightarrow \text{EVIDENCE} \longrightarrow \text{ACTION} \longrightarrow \text{MONITORING}$$

```text
🧭 AIRO STATUS Header
├── 1. FACT: Bukti terverifikasi dari SSU/POLREG/NOS (misal: Retail 12.241 unit, Stock Days 13,27)
├── 2. DIAGNOSIS: Hasil isolasi masalah oleh Retail Diagnosis Engine v1 (misal: FLP_PRODUCTIVITY_GAP)
├── 3. EVIDENCE: Data penunjang lintas domain (misal: FLP Sales Counter index 37.5%, Lead SLA > 4 jam)
├── 4. ACTION (PICA): Tindakan korektif spesifik (Initiative, PIC, Target Timeline)
└── 5. MONITORING: Indikator kontrol mingguan (Leading Indicator Metric)
```

---

## 6. Integration with Existing Frameworks

Commercial Copilot mengintegrasikan aset pelaporan dan kontrol yang ada tanpa melakukan modifikasi:
1. **`BUSINESS_PULSE.md`**: Sumber data pulse eksekutif berjalan.
2. **`B01_B02__DEALER_REVIEW.md`**: Template dasar penyusunan brief strategi diler.
3. **`B08__SPV_AREA_PLAYBOOK.md`**: Template dasar penyusunan brief supervisor area.
4. **`WD-SRC-020 PICA Framework`**: Standar pencatatan tindakan korektif (`AIRO_COPILOT_ACTION_TRACKER.tsv`).
