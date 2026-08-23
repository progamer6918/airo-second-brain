---
title: "Sales Activity Intelligence Layer v1"
component: "Sales Activity Intelligence"
status: "APPROVED / CANONICAL"
version: "1.0"
parent_contract: "wiki/workdesk/intelligence/RETAIL_INTELLIGENCE_ENGINE_V2.md"
source_authority: "CRM/Leads Dossiers (B06, B07) & Retail Sales Authority (SSU 2024-2026)"
last_updated: "2026-08-23"
---

# 🎯 Sales Activity & Source of Sale Intelligence Layer v1

## 1. Purpose & Business Context

Sales Activity Intelligence Layer v1 mentransformasikan data aktivitas akuisisi prospek konsumen (*Leads Management*) dan saluran penjualan (*Source of Sale*) jaringan dealer Honda periode **2024, 2025, dan 2026** di bawah arsitektur **Retail Intelligence Engine v2** menjadi inteligensi efektivitas saluran akuisisi dan produktivitas aktivitas sales force.

Layer ini menjembatani modul operasional CRM NMS (`B07__LEADS_MANAGEMENT_END_TO_END.md`, `B06__VIRTUAL_EXHIBITION_LEADS_OPERATING_SYSTEM.md`) dengan fakta transaksi retail SSU untuk mengukur tingkat konversi saluran (*Channel Conversion Rate*), efektivitas tindak lanjut salesman (*FLP Activity Effectiveness*), dan kesehatan corong penjualan dealer (*Dealer Funnel Health*).

---

## 2. Parent Contract & Source Authority Relationship

Sales Activity Intelligence Layer v1 beroperasi secara hirarkis sebagai *child capability* dari Retail Intelligence Engine v2 dan mengalirkan fakta dari Modul Operasional CRM serta Otoritas Sales SSU:

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                      Retail Intelligence Engine v2                      │
│                  (wiki/workdesk/intelligence/RETAIL_INTELLIGENCE_ENGINE_V2.md) │
└───────────────────┬─────────────────────────────────┬───────────────────┘
                    │                                 │
                    ▼                                 ▼
┌───────────────────────────────────────┐ ┌───────────────────────────────┐
│ Sales Activity Intelligence Layer v1  │ │ Source Authorities            │
│ (Channel Conversion, Funnel Health &  │ │ - CRM NMS Dossiers B06 / B07  │
│  FLP Activity Effectiveness)          │ │ - SSU 2024, 2025, 2026        │
│ (wiki/workdesk/intelligence/          │ │ - NOS 2026 Daily Lead Target  │
│  SALES_ACTIVITY_INTELLIGENCE_V1.md)   │ └───────────────────────────────┘
└───────────────────────────────────────┘
```

---

## 3. Privacy Boundary & Public Derivative Rules

### 3.1 Strict Private Raw Exclusion:
Informasi identitas pribadi konsumen dan rincian prospek mentah berikut **100% EXCLUDED** dari repositori publik ASB memory:
- `NIK` (Nomor Induk Kependudukan)
- `NAMA_KONSUMEN` (Nama Lengkap Pembeli / Prospek)
- `LEAD_IDENTITY_ID` (ID Unik Prospek CRM Individual)

### 3.2 Public Derived Intelligence:
Repositori publik ASB hanya menyimpan **fakta agregat terderivasi**:
- Kinerja Saluran Akusis Penjualan (*Channel Performance Aggregate*)
- Metrik Konversi Corong Penjualan (*Funnel Conversion Metrics*)
- Agregat Efektivitas Aktivitas FLP (*FLP Activity Productivity*)

---

## 4. Canonical Channel Classification Taxonomy

Sesuai dengan hasil audit discovery resmi, saluran akuisisi konsumen diklasifikasikan ke dalam 9 taksonomi saluran terstandar:

1. **`WALK_IN_SHOWROOM`**: Konsumen yang datang langsung (*walk-in*) ke showroom dealer utama atau POS.
2. **`BTL_CANVASSING`**: Prospek hasil aktivitas lapangan / pameran mobile (*canvassing*) oleh salesman.
3. **`BTL_EVENT`**: Prospek hasil pameran BTL (*Below The Line*) / roadshow lokal jaringan dealer.
4. **`VIRTUAL_EXHIBITION`**: Prospek digital hasil pameran virtual (*Virtual Exhibition / VE*).
5. **`SOCIAL_MEDIA`**: Prospek dari saluran media sosial resmi diler/Sinsen (Instagram, Facebook, TikTok).
6. **`CUSTOMER_APPS_REFERRAL`**: Prospek dari aplikasi konsumen Honda (*SinsenGo*) dan kode referral FLP.
7. **`FINCOY_OUTBOUND`**: Prospek penawaran ulang dari kerjasama perusahaan pembiayaan (*Finco database*).
8. **`REPEAT_ORDER_CRM`**: Prospek konsumen lama Honda hasil program retensi CRM diler.
9. **`CALL_WA_OUTBOUND`**: Prospek hasil kontak langsung via telepon atau WhatsApp Outbound oleh FLP/Telemarketing.

---

## 5. Intelligence Capabilities & Core Metrics

Sales Activity Intelligence mengukur 4 dimensi utama:

### 5.1 Lead Source Performance & Conversion
Mengukur volume prospek dan tingkat keberhasilan konversi saluran menjadi transaksi retail:
- $\text{Conversion Rate (\%)} = \left( \frac{\text{Retail Deal SSU}}{\text{Total Lead Volume}} \right) \times 100$
- $\text{Contacted Rate (\%)} = \left( \frac{\text{Contacted Prospects}}{\text{Total Lead Volume}} \right) \times 100$
- $\text{Success Rate (\%)} = \left( \frac{\text{Retail Deal SSU}}{\text{Contacted Prospects}} \right) \times 100$

### 5.2 Funnel Intelligence Chain
Melacak pergerakan prospek melalui 5 tahapan corong penjualan:
$$\text{Touchpoint / Lead} \longrightarrow \text{Validated Prospect} \longrightarrow \text{Follow Up / Contacted} \longrightarrow \text{SPK / Booking} \longrightarrow \text{Retail SSU}$$

### 5.3 FLP Activity Effectiveness & NOS Benchmark
Mengukur kinerja eksekusi tindak lanjut oleh salesman berbasis standar alokasi prospek harian NOS 2026:
- **Standar Alokasi Prospek Harian NOS**:
  - `SALES_COUNTER`: **10 leads / hari**
  - `FIELD_SALES_CANVASSER`: **5 leads / hari**
- **Indikator Efektivitas**:
  - `LEAD_SLA`: Durasi waktu (jam) dari alokasi prospek hingga kontak pertama.
  - `SPK_CONVERSION_EFFICIENCY`: Persentase prospek teralokasi yang berhasil menjadi SPK.

### 5.4 Dealer Funnel Health
Mengevaluasi kesehatan corong penjualan di tingkat diler:
$$\text{Dealer} \longrightarrow \text{Channel Mix} \longrightarrow \text{Lead Volume} \longrightarrow \text{Conversion Rate} \longrightarrow \text{Retail Output (SSU)}$$
- `HIGH_CONVERSION_HEALTH`: Diler dengan konversi prospek $\ge 25\%$.
- `BALANCED_FUNNEL`: Diler dengan konversi prospek $15\% - 24\%$.
- `LEAD_BOTTLENECK_WARNING`: Diler dengan volume prospek tinggi tetapi tingkat kontak $< 60\%$ atau konversi $< 15\%$.
