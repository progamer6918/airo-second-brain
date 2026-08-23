---
title: "Customer Lifecycle Intelligence Layer v1"
component: "Customer Lifecycle Intelligence"
status: "APPROVED / CANONICAL"
version: "1.0"
parent_contract: "wiki/workdesk/intelligence/RETAIL_INTELLIGENCE_ENGINE_V2.md"
sibling_contract: "wiki/workdesk/intelligence/CUSTOMER_SEGMENT_INTELLIGENCE_V1.md"
source_authority: "Retail Sales Authority (SSU 2024, WD-SRC-057 FY2025, SSU.2026.xlsx)"
last_updated: "2026-08-23"
---

# 🔄 Customer Lifecycle Intelligence Layer v1

## 1. Purpose & Business Context

Customer Lifecycle Intelligence Layer v1 mentransformasikan data histori transaksi penjualan retail per unit (Sales & Stock Unit / SSU) periode **2024, 2025, dan 2026** di bawah arsitektur **Retail Intelligence Engine v2** menjadi inteligensi siklus hidup kepemilikan konsumen (*Customer Ownership & Repurchase Journey*).

Berbeda dari `CUSTOMER_SEGMENT_INTELLIGENCE_V1.md` yang berfokus pada demografi statis (Kelompok Usia, Pekerjaan, Pengeluaran), layer ini menganalisis dinamika hubungan antar-transaksi temporal: rentang waktu pembelian ulang (*Repeat Gap Months*), perilaku pelunasan tenor vs pembaruan unit (*Tenor Repurchase Behavior*), migrasi antar-tipe motor (*Model Upgrade Migration*), dan tingkat retensi jaringan dealer (*Dealer & POS Retention*).

---

## 2. Parent Contract & Source Authority Relationship

Customer Lifecycle Intelligence Layer v1 beroperasi secara hirarkis sebagai *child capability* dari Retail Intelligence Engine v2 dan berdampingan dengan Customer Segment Intelligence Layer v1:

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                      Retail Intelligence Engine v2                      │
│                  (wiki/workdesk/intelligence/RETAIL_INTELLIGENCE_ENGINE_V2.md) │
└───────────────────┬─────────────────────────────────┬───────────────────┘
                    │                                 │
                    ▼                                 ▼
┌───────────────────────────────────────┐ ┌───────────────────────────────┐
│ Customer Segment Intelligence Layer v1 │ │Customer Lifecycle Intelligence│
│ (Demographics & Profile Taxonomy)     │ │Layer v1 (Temporal Repurchase, │
│ (wiki/workdesk/intelligence/          │ │Tenor & Model Migration)       │
│  CUSTOMER_SEGMENT_INTELLIGENCE_V1.md) │ │(wiki/workdesk/intelligence/   │
│                                       │ │ CUSTOMER_LIFECYCLE_           │
│                                       │ │ INTELLIGENCE_V1.md)           │
└───────────────────────────────────────┘ └───────────────────────────────┘
```

### Otoritas Data Sumber:
1. **SSU 2024**: `Retail Sales/SSU 2024.xlsx` (SHA256: `31af415f9137dc59c6a22c9dfea0a6869610d53f1de45b33d14162b3912ea380`)
2. **SSU 2025**: `WD-SRC-057__SSU_2025_FULL_YEAR.md` & `Retail Sales/SSU 2025.xlsx` (SHA256: `38e05002d23a6b275b6380bd78e991b8152b70e790c46e7ee543d5bae3891450`)
3. **SSU 2026**: `RETAIL_CURRENT_STATE.md` & `Retail Sales/SSU.2026.xlsx` (SHA256: `a9ff25cd2286e285865cf5d79d9d0e77f6f3dd81d874dfd3a61554a04c99f0c3`)

---

## 3. Strict PII Exclusion & Identity Hash Rule

### 3.1 Private Raw Processing Boundary (Strict Internal Sidecar Only):
Bidang identitas pribadi mentah berikut **DILARANG HARUS EXCLUDED** dari repositori publik ASB memory:
- `NIK` (Nomor Induk Kependudukan / KTP)
- `NAMA_KONSUMEN` (Nama Lengkap Pembeli)
- `NPWP` (Nomor Pokok Wajib Pajak Perusahaan)

Pemrosesan tautan antar-transaksi (*Identity Matching & Sequence Linkage*) dilakukan secara tertutup di dalam lingkungan pemrosesan privat menggunakan kunci unik fallback:
$$\text{Private Customer Key} = \begin{cases} \text{NIK}, & \text{jika } \text{JENIS\_CUSTOMER} = \text{PERORANGAN} \\ \text{NPWP}, & \text{jika } \text{JENIS\_CUSTOMER} = \text{PERUSAHAAN} \end{cases}$$

### 3.2 Public Customer Hash ID Rule:
Dalam dokumen publik dan file inteligensi TSV, seluruh konsumen direferensikan hanya menggunakan kunci terenkripsi anonim (*Customer Hash ID*):
$$\text{customer\_hash\_id} = \text{SHA256}(\text{Private Customer Key} \parallel \text{SALT})[0:16]$$
*Contoh*: `CUST-8F3A29B10C4D`, `CUST-9E112A4B8F77`.

---

## 4. Canonical Customer Types

Sesuai dengan audit data mentah SSU, tipe konsumen diklasifikasikan ke dalam 2 kategori kanonis:
1. **`PERORANGAN`**: Konsumen perorangan / individu.
2. **`PERUSAHAAN`**: Konsumen lembaga / corporate / BUMN / fleet.

---

## 5. Lifecycle Metrics & Methodologies

Customer Lifecycle Intelligence mengukur 3 indikator utama:

### 5.1 Repeat Gap Month (Rentang Waktu Pembelian Ulang)
Selisih waktu dalam bulan antara tanggal transaksi terkini dengan tanggal transaksi sebelumnya untuk konsumen yang sama:
$$\text{Repeat Gap Month} = \frac{\text{TGL\_SALES}_{\text{current}} - \text{TGL\_SALES}_{\text{previous}}}{30.4}$$

### 5.2 Estimated Maturity Date (Perkiraan Tanggal Jatuh Tempo Kredit)
Perkiraan tanggal selesai angsuran kredit berdasarkan tanggal transaksi booking dan durasi tenor:
$$\text{Estimated Maturity Date} = \text{TGL\_SALES}_{\text{previous}} + (\text{TENOR}_{\text{previous}} \times 30.4 \text{ hari})$$

### 5.3 Repurchase Classification Taxonomy
Berdasarkan perbandingan antara rentang waktu pembelian ulang (*Elapsed Month*) dengan durasi tenor transaksi kredit sebelumnya (*Previous Tenor*), perilaku konsumen diklasifikasikan menjadi 3 kategori:

1. **`PREMATURE_UPGRADE`**:
   - **Kriteria**: Pembelian ulang dilakukan **sebelum** tenor angsuran selesai ($\text{Elapsed Month} < \text{Previous Tenor}$).
   - **Makna**: Konsumen melunasi dipercepat (*early payoff*) atau melakukan pelunasan tukar-tambah (*trade-in*) untuk upgrade unit lebih awal.
   - **Fokus Strategi**: Berikan insentif *Trade-in Loyalty Program* dan promosi eksklusif tipe segmen High-AT/Sport.

2. **`MATURITY_REPLACEMENT`**:
   - **Kriteria**: Pembelian ulang dilakukan **tepat saat / sesaat setelah** tenor angsuran selesai ($\text{Previous Tenor} \le \text{Elapsed Month} \le \text{Previous Tenor} + 6 \text{ bulan}$).
   - **Makna**: Konsumen mengganti unit motor tepat ketika angsuran selesai (*ideal replacement cycle*).
   - **Fokus Strategi**: Kirimkan notifikasi penawaran unit baru (*Retention Reminder*) pada bulan ke-($\text{Tenor} - 2$) sebelum angsuran berakhir.

3. **`DELAYED_RETENTION`**:
   - **Kriteria**: Pembelian ulang dilakukan **lama setelah** tenor selesai ($\text{Elapsed Month} > \text{Previous Tenor} + 6 \text{ bulan}$) atau pembelian cash dengan jeda $> 36 \text{ bulan}$.
   - **Makna**: Konsumen mempertahankan unit lama dalam durasi panjang sebelum kembali membeli unit Honda.
   - **Fokus Strategi**: Tawarkan penawaran spesial *Win-back / Re-engagement Promo* dan kemudahan servis di AHASS.

---

## 6. Model & Dealer Migration Tracking

### 6.1 Model Migration Path (Pergerakan Tipe Motor)
- `SAME_MODEL_REFRESH`: Pembelian tipe motor yang sama (misal: Beat Street `MM1` ➔ Beat Street `MM2`).
- `SEGMENT_UPGRADE`: Perpindahan ke kelas segmen lebih tinggi (misal: Beat `MJ1` ➔ Vario 125 `NE0` atau Stylo 160 `MF1`).
- `CROSS_SEGMENT_EXPANSION`: Penambahan tipe motor di segmen berbeda (misal: Vario 125 ➔ CRF150L `ESL`).

### 6.2 Dealer & POS Retention
- `DEALER_RETAINED`: Pembelian ulang dilakukan di diler utama yang sama (`previous_dealer == current_dealer`).
- `POS_MIGRATED`: Pembelian ulang dilakukan di POS/cabang berbeda dalam diler/grup yang sama.
- `DEALER_SWITCHED`: Pembelian ulang dilakukan di diler Honda pesaing dalam wilayah yang sama.
