---
title: "FLP Intelligence Layer v1"
component: "FLP Intelligence"
status: "APPROVED / CANONICAL"
version: "1.0"
parent_contract: "wiki/workdesk/intelligence/RETAIL_INTELLIGENCE_ENGINE_V2.md"
legacy_reference: "wiki/workdesk/intelligence/FLP_INTELLIGENCE.md"
source_authority: "Retail Sales Authority (SSU 2024, WD-SRC-057 FY2025, SSU.2026.xlsx) & NOS H1 Standards"
last_updated: "2026-08-23"
---

# 👷 FLP Intelligence Layer v1

## 1. Purpose & Business Context

FLP (Front Line People) Intelligence Layer v1 mentransformasikan data tenaga penjual / tenaga pemasar retail (*Sales Force*) jaringan dealer Honda periode **2024, 2025, dan 2026** di bawah arsitektur **Retail Intelligence Engine v2** menjadi inteligensi produktivitas tenaga kerja (*manpower productivity*).

Layer ini mengukur pencapaian target penjualan bulanan per peran salesman berbasis standar **NOS (Network Operating System) H1 People**, memetakan siklus hidup tenaga kerja (*manpower lifecycle*), dan mengevaluasi kecukupan kapasitas tim penjualan di setiap outlet/dealer.

---

## 2. Parent Contract & Legacy Contract Relationship

FLP Intelligence Layer v1 beroperasi sebagai *child capability* dari Retail Intelligence Engine v2 dan mempertahankan rujukan resmi ke kontrak legasi grooming & kompetensi:

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                      Retail Intelligence Engine v2                      │
│                  (wiki/workdesk/intelligence/RETAIL_INTELLIGENCE_ENGINE_V2.md) │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        FLP Intelligence Layer v1                        │
│                     (wiki/workdesk/intelligence/FLP_INTELLIGENCE_V1.md) │
└───────────────────┬─────────────────────────────────┬───────────────────┘
                    │                                 │
                    ▼                                 ▼
┌───────────────────────────────────────┐ ┌───────────────────────────────┐
│ Legacy FLP Reference (Grooming/NOS)   │ │ Source Data Authorities       │
│ (wiki/workdesk/intelligence/          │ │ - SSU 2024, 2025, 2026        │
│  FLP_INTELLIGENCE.md)                 │ │ - NOS 2026 H1 People Canonical│
└───────────────────────────────────────┘ └───────────────────────────────┘
```

### Preservasi Kontrak Legasi:
Dokumen legasi `wiki/workdesk/intelligence/FLP_INTELLIGENCE.md` (v2.4) tetap dipertahankan sebagai **referensi sekunder** untuk standar seragam (*Uniform Guidance*), grooming, dan modul pelatihan kompetensi NOS. Kontrak v1 ini memperluas fungsi inteligensi ke domain **Produktivitas Penjualan dan Manpower**.

---

## 3. Privacy Boundary & Synthetic Identifier Rule

### 3.1 Strict Private Raw Exclusion:
Nama asli salesman (`NAMA_SALES`), nomor telepon, alamat, dan nomor identitas pribadi bersifat **100% PRIVATE_RAW_ONLY** dan **DILARANG HARUS EXCLUDED** dari repositori publik ASB memory.

### 3.2 Synthetic FLP Identifier Rule:
Seluruh publikasi inteligensi tingkat individu mengadopsi format **Synthetic FLP ID** teranonimisasi:
$$\text{Synthetic FLP ID} = \text{FLP-} \langle \text{DEALER\_CODE} \rangle \text{-} \langle \text{SEQUENCE} \rangle$$
*Contoh*: `FLP-01001-01`, `FLP-01001-02`, `FLP-01002-01`.

### 3.3 Public Memory Rule:
Repositori publik ASB hanya menyimpan **fakta agregat tingkat dealer/POS** (jumlah headcount aktif, proporsi peran, rata-rata unit per FLP, dan persentase pencapaian NOS).

---

## 4. Role Taxonomy & NOS Benchmark Standards

Tenaga penjual dikelompokkan ke dalam 4 peran terstandar berbasis standar AHM NOS H1 People:

| Role Code | Standard Role Description | Benchmark NOS Range | Benchmark Mid Target | Primary Allocation / Focus |
|---|---|---|---|---|
| `SALES_COUNTER` | Counter Sales / Showroom Salesman | 6 – 10 unit/bulan | **8 unit/bulan** | Walk-in customer & Showroom leads (Target: 10 leads/hari) |
| `FIELD_SALES_CANVASSER` | Field Salesman / Canvasser / Sales Lapangan | 4 – 8 unit/bulan | **6 unit/bulan** | BTL event, Canvassing, Mobile exhibition (Target: 5 leads/hari) |
| `WING_SALES_PEOPLE` | Wing Sales People (WSP) | 8 – 14 unit/bulan | **11 unit/bulan** | Segment Premium, Big Bike & High-AT (Vario 160/Stylo/PCX/ADV) |
| `SALES_SUPERVISOR_TEAM_LEADER` | Sales Supervisor / Team Leader (SPV/TL) | Supervisory Target | **Team Target** | Supervisi, koordinasi tim sales, dan kontrol SPK |

---

## 5. Productivity Methodology & Classification

Produktivitas salesman dihitung berdasarkan perbandingan antara realisasi penjualan retail dengan target titik tengah (*Benchmark Mid*) peran yang bersangkutan:

### 5.1 Productivity Index Formula
$$\text{Productivity Index (\%)} = \left( \frac{\text{Actual Retail Units Sold}}{\text{NOS Benchmark Mid Target}} \right) \times 100$$

### 5.2 Performance Classification Matrix
Setiap tenaga penjual diklasifikasikan ke dalam 4 tingkatan kinerja produktivitas:

1. **`ABOVE_EXPECTATION`** ($\text{Productivity Index} \ge 100\%$):
   - Salesman melampaui target titik tengah NOS (misal: Sales Counter $\ge 8$ unit, Canvasser $\ge 6$ unit, Wing Sales $\ge 11$ unit).
   - *Tindakan*: Berikan reward/insentif dan pertimbangkan sebagai kandidat Team Leader.

2. **`WITHIN_EXPECTATION`** ($80\% \le \text{Productivity Index} \le 99\%$):
   - Salesman mendekati target titik tengah NOS dan berada dalam rentang wajar (misal: Sales Counter 6–7 unit, Canvasser 5 unit).
   - *Tindakan*: Pertahankan konsistensi pasokan leads dan pembinaan reguler.

3. **`BELOW_EXPECTATION`** ($50\% \le \text{Productivity Index} \le 79\%$):
   - Kinerja salesman di bawah standar minimum NOS (misal: Sales Counter 4–5 unit, Canvasser 3 unit).
   - *Tindakan*: Lakukan coaching keterampilan penjualan (*Virtual Communication / CX Training*) dan evaluasi alokasi prospek.

4. **`CRITICAL_GAP`** ($\text{Productivity Index} < 50\%$):
   - Kinerja salesman sangat rendah (misal: Sales Counter $< 4$ unit, Canvasser $< 3$ unit).
   - *Tindakan*: Lakukan audit penyebab (*Root Cause Audit*), pendampingan harian oleh SPV, atau penataan ulang peran.

---

## 6. FLP Manpower Lifecycle Methodology

Sesuai aturan guardrail legasi (*"Never infer active/inactive FLP status without verified payroll or attendance log evidence"*), status siklus hidup salesman ditentukan dengan kriteria berikut:

1. **`ACTIVE`**:
   - Salesman memiliki bukti transaksi retail SSU atau tercatat dalam daftar absensi aktif dealer dalam 30 hari terakhir.

2. **`NEW_ONBOARDING`**:
   - Salesman dengan masa kerja $< 3$ bulan yang sedang menjalani program pelatihan dasar AHM NOS H1 People (*Virtual Communication & Customer Experience*).

3. **`DORMANT_INACTIVE`**:
   - Salesman tanpa pencatatan penjualan SSU atau log aktivitas aktif selama 60+ hari berturut-turut.
