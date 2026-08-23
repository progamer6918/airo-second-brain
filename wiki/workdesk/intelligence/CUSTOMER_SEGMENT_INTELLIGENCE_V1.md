---
title: "Customer Segment Intelligence Layer v1"
component: "Customer Segment Intelligence"
status: "APPROVED / CANONICAL"
version: "1.0"
parent_contract: "wiki/workdesk/intelligence/RETAIL_INTELLIGENCE_ENGINE_V2.md"
source_authority: "Retail Sales Authority (SSU 2024, WD-SRC-057 FY2025, SSU.2026.xlsx)"
last_updated: "2026-08-23"
---

# 👥 Customer Segment Intelligence Layer v1

## 1. Purpose & Business Context

Customer Segment Intelligence Layer v1 mentransformasikan data transaksi penjualan retail per unit (Sales & Stock Unit / SSU) periode **2024, 2025, dan 2026** di bawah arsitektur **Retail Intelligence Engine v2** menjadi inteligensi segmen konsumen terstruktur.

Layer ini mengukur demografi pembeli (Kelompok Usia & Gender), profesi/pekerjaan, tingkat pengeluaran bulanan (Expenditure Tiers), serta rasio status pembeli (**First Time Buyer vs Repeat Order / RO**) untuk mengarahkan strategi pemasaran, promosi segmen, dan kesesuaian produk.

---

## 2. Parent Contract & Source Authority Relationship

Customer Segment Intelligence Layer v1 beroperasi secara hirarkis sebagai *child capability* dari Retail Intelligence Engine v2 dan mengalirkan fakta agregat dari Otoritas Sumber Resmi yang telah disahkan:

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                      Retail Intelligence Engine v2                      │
│                  (wiki/workdesk/intelligence/RETAIL_INTELLIGENCE_ENGINE_V2.md) │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Customer Segment Intelligence Layer v1               │
│               (wiki/workdesk/intelligence/CUSTOMER_SEGMENT_INTELLIGENCE_V1.md)│
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
         ┌───────────────────────────┼───────────────────────────┐
         ▼                           ▼                           ▼
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│Demographic Age  │         │Occupation Mix   │         │Repeat Order &   │
│& Gender Ratio   │         │& Spending Tiers │         │Buyer Behavior   │
└─────────────────┘         └─────────────────┘         └─────────────────┘
```

### Otoritas Data Sumber:
1. **SSU 2024**: `Retail Sales/SSU 2024.xlsx` (SHA256: `31af415f9137dc59c6a22c9dfea0a6869610d53f1de45b33d14162b3912ea380`)
2. **SSU 2025**: `WD-SRC-057__SSU_2025_FULL_YEAR.md` & `Retail Sales/SSU 2025.xlsx` (SHA256: `38e05002d23a6b275b6380bd78e991b8152b70e790c46e7ee543d5bae3891450`)
3. **SSU 2026**: `RETAIL_CURRENT_STATE.md` & `Retail Sales/SSU.2026.xlsx` (SHA256: `a9ff25cd2286e285865cf5d79d9d0e77f6f3dd81d874dfd3a61554a04c99f0c3`)

---

## 3. Strict PII Exclusion & Public-Safe Transformation Boundary

Untuk mematuhi Aturan Privasi Data (`DATA_USE_RULES.md`) dan Kebijakan Repositori Publik ASB (`BOOT.md`):

### 3.1 Data PII Dilarang (100% Excluded from Public ASB):
- Nama Konsumen (`NAMA_KONSUMEN`)
- Nomor NIK / KTP (`NIK`)
- Nomor Telepon / HP (`NO_TELP`)
- Alamat Rumah / RT / RW / No Rumah (`ALAMAT_LENGKAP`)

### 3.2 Transformasi Publik Aman (PII-Safe Derived Aggregates):
- `TGL_LAHIR` ➔ Konversi menjadi Kelompok Usia (`AGE_GROUP`): `<20`, `20-29`, `30-39`, `40-49`, `50+` tahun.
- `JENIS_KELAMIN` ➔ Konversi menjadi Rasio Gender (`GENDER_RATIO_PCT`): Pria % vs Wanita %.
- `PEKERJAAN` ➔ Pemetaan ke 7 Kategori Pekerjaan Terstandar.
- `PENGELUARAN` ➔ Pemetaan ke 4 Tingkat Pengeluaran Bulanan.
- `RO_STATUS` ➔ Rasio Pembeli Pertama (`FIRST_TIME_BUYER_PCT`) vs Pembeli Setia/Tambahan (`REPEAT_ORDER_PCT`).

---

## 4. Methodology & Core Rules

Customer Segment Intelligence mengukur 4 dimensi utama:

### 4.1 Age Bucket Standard Rules
Usia pembeli dihitung dari selisih tanggal transaksi dengan tanggal lahir (`TGL_SALES - TGL_LAHIR`) dan dikelompokkan ke dalam 5 rentang:
- `GEN_Z_YOUNG` ($< 20 \text{ tahun}$): Generasi pemula / pelajar.
- `YOUNG_ADULT` ($20 - 29 \text{ tahun}$): Karyawan muda / mahasiswa senior.
- `PRIME_ADULT` ($30 - 39 \text{ tahun}$): Kepala keluarga muda / profesional.
- `MATURE_ADULT` ($40 - 49 \text{ tahun}$): Pembeli mapan / segmen keluarga mature.
- `SENIOR_BUYER` ($\ge 50 \text{ tahun}$): Pembeli senior / tokoh masyarakat.

### 4.2 Spending Tier Rules
- `LOW_SPENDING` ($< \text{Rp 2.000.000 / bulan}$): Pembeli sensitif harga.
- `MID_SPENDING` ($\text{Rp 2.000.000} - \text{Rp 5.000.000 / bulan}$): Segmen komuter utama (mainstream).
- `UPPER_MID_SPENDING` ($\text{Rp 5.000.000} - \text{Rp 8.000.000 / bulan}$): Segmen menengah atas.
- `HIGH_SPENDING` ($> \text{Rp 8.000.000 / bulan}$): Segmen premium / pengusaha.

### 4.3 Repeat Order (RO) Status Rules
- `FIRST_TIME_BUYER`: Pembeli pertama produk Honda di jaringan diler Sinsen.
- `REPEAT_ORDER_REPLACEMENT`: Konsumen yang mengganti motor lama dengan tipe baru.
- `REPEAT_ORDER_ADDITIONAL`: Konsumen yang menambah unit motor untuk keluarga/operasional bisnis.

---

## 5. Customer Profile Taxonomy

Setiap profil pembeli dikelompokkan ke dalam 4 taksonomi inteligensi segmen konsumen:

1. **`YOUNG_COMMUTER`**:
   - **Profil**: Usia $< 25$ tahun, profesi Pelajar/Mahasiswa/Swasta Muda, pengeluaran Low/Mid.
   - **Preferensi Produk**: Beat Series (Beat Street `MM1`/`MM2`, Beat Sporty `MJ1`/`MJ2`), Genio Series, Scoopy Fashion (`MRB`).
   - **Fokus Keputusan**: *Digital Promo & Affordable DP* — Jalankan promosi media sosial, kemudahan Uang Muka ringan, dan event kampus/komunitas muda.

2. **`COMMERCIAL_AGRI_WORKER`**:
   - **Profil**: Profesi Petani/Perkebunan/Wiraswasta Lokal di wilayah kabupaten (Merangin, Tebo, Sarolangun, Bungo), pengeluaran Mid.
   - **Preferensi Produk**: Revo Series (Revo X `GD4`, Revo Fit `GB4`), Supra X 125 (`GF5`), CRF150L (`ESL`).
   - **Fokus Keputusan**: *Durability & Harvest Season Activation* — Tawarkan motor tangguh untuk medan perkebunan dan selaraskan promo angsuran dengan musim panen kelapa sawit/karet.

3. **`FAMILY_STABILITY_BUYER`**:
   - **Profil**: Usia $30 - 49$ tahun, profesi PNS/BUMN/IRT/Karyawan Senior, pengeluaran Mid/Upper-Mid.
   - **Preferensi Produk**: Vario 125 Series (`NE0`/`ND0`), Vario 160 Series (`LV1`/`LVE`), PCX 160 Series (`MT1`/`MV1`), Scoopy Prestige (`MS1`).
   - **Fokus Keputusan**: *Comfort, Safety & Trade-in Program* — Tonjolkan kenyamanan bagasi, fitur keselamatan (ABS/Smartkey), dan program tukar-tambah (trade-in).

4. **`FLEET_CORPORATE_CLIENT`**:
   - **Profil**: Pelanggan perusahaan, instansi pemerintah, atau BUMN (`JENIS_CUSTOMER = CORPORATE`).
   - **Preferensi Produk**: Revo Series, CB150 Verza (`KG0`), Beat Sporty CBS, Supra X 125.
   - **Fokus Keputusan**: *Fleet Service & Corporate Discount* — Berikan paket potongan harga pembelian jumlah besar (bulk discount) dan kontrak perawatan AHASS terpadu.

---

## 6. Occupation Text Normalization & Alias Mapping Rules

Data mentah SSU mencatat nama pekerjaan konsumen secara bervariasi. Customer Segment Engine mentransformasikannya ke dalam Kode Standar Pekerjaan:

| Raw Occupation Input in SSU | Normalized Occupation Code | Standard Canonical Description |
|---|---|---|
| `PNS`, `PEGAWAI NEGERI`, `BUMN`, `ASN`, `TNI`, `POLRI` | `PNS_BUMN` | Pegawai Negeri Sipil / BUMN / Aparat |
| `SWASTA`, `KARYAWAN SWASTA`, `BURUH`, `KARYAWAN`, `PEGAWAI` | `SWASTA` | Karyawan / Pegawai Swasta |
| `WIRASWASTA`, `PEDAGANG`, `TOKO`, `PENGUSAHA`, `DAGANG` | `WIRASWASTA` | Wiraswasta / Pemilik Usaha |
| `PETANI`, `PERKEBUNAN`, `PEKEBUN`, `NELAYAN`, `TANI`, `SAWIT` | `PETANI_PERKEBUNAN` | Petani / Perkebunan / Nelayan |
| `PELAJAR`, `MAHASISWA`, `STUDENT`, `SISWA` | `PELAJAR_MAHASISWA` | Pelajar & Mahasiswa |
| `IBU RUMAH TANGGA`, `IRT`, `RUMAH TANGGA` | `IBU_RUMAH_TANGGA` | Ibu Rumah Tangga |
| `LAINNYA`, `DOKTER`, `GURU`, `DOSEN`, `LAIN-LAIN` | `OTHER_PROFESSION` | Profesi Lainnya / Jasa Profesional |
