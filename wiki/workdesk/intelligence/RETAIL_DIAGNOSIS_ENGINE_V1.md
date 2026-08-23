---
title: "Retail Diagnosis Engine v1 Contract"
component: "Retail Diagnosis Engine"
status: "APPROVED / CANONICAL"
version: "1.0"
parent_contract: "wiki/workdesk/intelligence/RETAIL_INTELLIGENCE_ENGINE_V2.md"
reference_playbook: "wiki/workdesk/playbooks/DIAGNOSE_BUSINESS_PROBLEM.md"
source_authority: "Retail Sales Authorities (SSU 2024-2026, POLREG 2026, NOS 2026, Stock State 2026)"
last_updated: "2026-08-23"
---

# 🧠 Retail Diagnosis Engine v1 Contract

## 1. Purpose & Business Context

Retail Diagnosis Engine v1 mentransformasikan 10 domain inteligensi retail di bawah arsitektur **Retail Intelligence Engine v2** menjadi **Mesin Penalaran Diagnostik & Rekomendasi Tindakan (Level 3 Prescriptive Reasoning Engine)**.

Engine ini berfungsi sebagai lapisan penalaran berbasis bukti (*Evidence-Based Reasoning Layer*) yang mengisolasi akar masalah bisnis (*Root Cause Analysis / RCA*) dari sekadar gejala permukaan (*Symptom*), serta menghasilkan rekomendasi aksi korektif terukur (*Plan-Initiative-Corrective-Action / PICA*) tanpa melakukan tebakan atau menghasilkan rekomendasi tanpa rantai bukti (*Evidence Chain*).

---

## 2. Parent Contract & Multi-Domain Architecture

Retail Diagnosis Engine v1 beroperasi sebagai lapisan penalaran utama (*Reasoning Synthesizer*) yang menyatukan 10 domain inteligensi retail:

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                      Retail Intelligence Engine v2                      │
│                  (wiki/workdesk/intelligence/RETAIL_INTELLIGENCE_ENGINE_V2.md) │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      Retail Diagnosis Engine v1                         │
│             (wiki/workdesk/intelligence/RETAIL_DIAGNOSIS_ENGINE_V1.md)  │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
 ┌──────────────┬──────────────┬─────┴────────┬──────────────┬──────────────┐
 ▼              ▼              ▼              ▼              ▼              ▼
┌────────────┐┌────────────┐┌────────────┐┌────────────┐┌────────────┐┌────────────┐
│1. Dealer   ││2.Territory ││3. Product  ││4. Financing││5. Customer ││6. Lifecycle│
└────────────┘└────────────┘└────────────┘└────────────┘└────────────┘└────────────┘
 ┌────────────┐┌────────────┐┌────────────┐┌────────────┐
 │7. FLP      ││8. Activity ││9. Stock    ││10. Promo   │
 └────────────┘└────────────┘└────────────┘└────────────┘
```

---

## 3. Mandatory Evidence-Based Diagnosis Chain

Setiap diagnosis dan rekomendasi PICA yang dihasilkan oleh AIRO WorkDesk **WAJIB OBEY** alur penalaran 6-tahap tak terputus (*6-Stage Evidence Chain*):

$$\text{FACT} \longrightarrow \text{SYMPTOM} \longrightarrow \text{HYPOTHESIS} \longrightarrow \text{EVIDENCE} \longrightarrow \text{ROOT CAUSE} \longrightarrow \text{ACTION}$$

1. **`FACT`**: Bukti angka/data mentah terverifikasi dari SSU, POLREG, NOS, atau laporan resmi.
2. **`SYMPTOM`**: Sinyal penurunan kinerja teramati (misal: Retail Sales drop -12% MoM, Market Share turun -2.4%).
3. **`HYPOTHESIS`**: Dugaan awal penyebab masalah yang belum dibuktikan secara matematis.
4. **`EVIDENCE`**: Verifikasi fakta lintas domain (misal: Stock Days, FLP SLA, Finco Share, Channel Conversion).
5. **`ROOT CAUSE`**: Akar masalah terbukti secara empiris yang berada di bawah kendali manajemen diler/MD.
6. **`ACTION`**: Rekomendasi aksi korektif PICA spesifik terukur (PIC, Target, Timeline, Leading Metric).

---

## 4. Problem Classification Taxonomy

Masalah bisnis retail diklasifikasikan ke dalam 9 taksonomi standar:

1. **`SALES_DROP`**: Penurunan volume penjualan SSU bulanan dibanding target atau periode sebelumnya.
2. **`MARKET_SHARE_LOSS`**: Penurunan pangsa pasar Honda dibanding kompetitor di tingkat Kabupaten/Kecamatan.
3. **`STOCK_CONSTRAINT`**: Keterbatasan pasokan unit dari MD (*Under-stocked*) atau penumpukan stok mati (*Critical Aging $> 150$d*).
4. **`PRODUCT_MISMATCH`**: Ketidaksesuaian alokasi tipe/seri motor dengan preferensi segmen lokal.
5. **`CHANNEL_WEAKNESS`**: Laju konversi prospek rendah (*Low Conversion Rate*) atau keterlambatan kontak (*Lead SLA Delay*).
6. **`FLP_PRODUCTIVITY_GAP`**: Produktivitas tim salesman di bawah standar NOS harian ($\text{Productivity Index} < 80\%$).
7. **`FINANCING_BARRIER`**: Tingkat penolakan angsuran kredit tinggi (*High Reject Rate*) atau dominasi Finco tunggal berisiko.
8. **`PROMOTION_INEFFECTIVENESS`**: Program promosi menghasilkan *uplift* rendah ($< 10\%$) atau biaya program tidak seimbang.
9. **`TERRITORY_OPPORTUNITY`**: Area putih (*Whitespace Ring 2-3*) dengan penetrasi rendah dibanding potensi pasar.

---

## 5. Cross-Domain Diagnostic Decision Rules

### Rule 1: Demand vs Supply Bottleneck Isolation
$$\begin{cases} 
\text{Retail Drop} + \text{Stock Days } < 10 \text{ hari} \Longrightarrow \mathbf{STOCK\_CONSTRAINT\ (Supply\ Bottleneck)} \\
\text{Retail Drop} + \text{Stock Days } > 20 \text{ hari} + \text{Aging } \ge 5\% \Longrightarrow \mathbf{SALES\_DROP\ (Demand\ Problem)} 
\end{cases}$$

### Rule 2: Channel Conversion vs FLP Productivity Isolation
$$\begin{cases}
\text{Leads High} + \text{Contacted Rate } < 60\% \Longrightarrow \mathbf{CHANNEL\_WEAKNESS\ (Lead\ SLA\ Delay)} \\
\text{Contacted High} + \text{Retail Deal } < 15\% \Longrightarrow \mathbf{FLP\_PRODUCTIVITY\_GAP\ (Salesman\ Probing\ Competency)}
\end{cases}$$

### Rule 3: Commercial Competitiveness Isolation
$$\begin{cases}
\text{Credit Share Drop} + \text{Finco Reject } > 25\% \Longrightarrow \mathbf{FINANCING\_BARRIER\ (Finco\ Credit\ Term)} \\
\text{Promo Active} + \text{Sales Uplift } < 10\% \Longrightarrow \mathbf{PROMOTION\_INEFFECTIVENESS\ (Promo\ Offer\ Fit)}
\end{cases}$$

---

## 6. PICA Action Recommendation Standard

Setiap rekomendasi PICA (*Plan-Initiative-Corrective-Action*) harus menyertakan 4 elemen wajib:
1. **Initiative**: Tindakan spesifik (misal: *Clearance Promo Discount*, *FLP Probing Retraining*, *Finco Portfolio Diversification*).
2. **PIC**: Penanggung jawab eksekusi (Kacab, SPV Area, Sales Manager, MD NetDev).
3. **Timeline**: Target durasi penyelesaian (1 minggu, 2 minggu, 1 bulan).
4. **Monitoring Metric**: Indikator leading untuk mengukur progres mingguan.
