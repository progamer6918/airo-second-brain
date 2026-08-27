---
type: awd-status-data
aliases:
  - Status Data
  - Status Data WorkDesk
---

# 🩺 Status Data

> **Ringkasan Ketersediaan, Cakupan Periode, dan Kualitas Data Bisnis AIRO**

---

## ⚠️ Aturan Kemutakhiran Antar-Domain
*Setiap data punya periode terbarunya sendiri. Market, Retail, Stock, Program, Ring, dan Network tidak boleh dianggap berasal dari satu tanggal yang sama.*

---

## 📌 Ringkasan Kelengkapan
- 🟢 **Tersedia**: 13 Topik Utama (Lengkap & Siap Digunakan)
- 🟡 **Perlu Pembaruan**: 1 Topik Utama (Proses Ada, Catatan Historis Belum Disediakan)
- 🟠 **Sebagian**: 2 Topik Utama (Dealer & POS, Integrated Network)
- 🔴 **Belum Tersedia**: 0 Topik
- ⚪ **Historis**: 1 Topik Utama (Pemetaan Ring Historis 2022)

---

## 📑 Indeks Status Data

| Topik Data | Periode s.d. | Status | Riwayat | Buka Rincian |
|---|---|---|---|---|
| Penjualan Retail | Jul 2026 | 🟢 Tersedia | FY 2025 (107.108 unit) & 2024 | [[#penjualan-retail\|Rincian Retail]] |
| Market Share | Jun 2026 | 🟢 Tersedia | FY 2025 (127.244 Total Market) | [[#market-share\|Rincian Market Share]] |
| Territory & POLREG | Jun 2026 | 🟢 Tersedia | 118 Kecamatan / 1.223 Baris Kelurahan-Desa Terpetakan | [[#territory--polreg\|Rincian Territory]] |
| Dealer & POS | Belum terkonfirmasi | 🟠 Sebagian | Hierarki Dealer → POS → FLP Tersedia | [[#dealer--pos\|Rincian Dealer]] |
| Ring Penjualan | 2022 | ⚪ Historis | 803 Dealer/POS-Kecamatan Records | [[#ring-penjualan\|Rincian Ring]] |
| Stock Kendaraan | Snapshot 6 Aug 2026 | 🟢 Tersedia | Dealer 5.239 unit / MD 3.496 unit | [[#stock-kendaraan\|Rincian Stock]] |
| Produk & Model | Jul 2026 | 🟢 Tersedia | Lineup Sepeda Motor 2025–2026 | [[#produk--model\|Rincian Produk]] |
| Pembiayaan & Finance | Jul 2026 | 🟢 Tersedia | Transaksi Tunai & Kredit 2025–2026 | [[#pembiayaan--finance\|Rincian Finance]] |
| Customer Segment | Jul 2026 | 🟢 Tersedia | Demografi & Pekerjaan 2025–2026 | [[#customer-segment\|Rincian Segmen]] |
| Customer Lifecycle | Jul 2026 | 🟢 Tersedia | Database Consumer & Repeat Order | [[#customer-lifecycle--repeat-order\|Rincian Lifecycle]] |
| FLP & Manpower | Jul 2026 | 🟢 Tersedia | FLP Active Roster 2026 | [[#flp--manpower\|Rincian FLP]] |
| Sales Activity & Leads | Jul 2026 | 🟢 Tersedia | Activity Log & Prospek 2026 | [[#sales-activity--leads\|Rincian Leads]] |
| Promotion & Program | YTD Aug 2026 | 🟢 Tersedia | Katalog Program Promo Q1–Q3 2026 | [[#promotion--program\|Rincian Promo]] |
| Commercial & MSW | Aug 2026 | 🟢 Tersedia | Fleet Account & MSW Aug 2026 | [[#commercial--msw\|Rincian Commercial]] |
| Market Info & Event | Aug 2026 | 🟡 Perlu Pembaruan | Event Calendar 2026 (Catatan Historis Belum Disediakan) | [[#market-info--event\|Rincian Event]] |
| Standar NOS | Jul 2026 | 🟢 Tersedia | Hasil Audit Kualitas NOS 2026 | [[#standar-nos\|Rincian NOS]] |
| Integrated Network | Snapshot Aug 2026 | 🟠 Sebagian | Network Map (Kesiapan Pengajuan Belum Terbukti) | [[#integrated-ttm--network\|Rincian Network]] |

---

## 🔍 RINCIAN TOPIK DATA

### Penjualan Retail
- **Data s.d.**: Juli 2026 (Juli = 12.241 unit, YTD Jan–Jul 2026 = 73.968 unit)
- **Riwayat tersedia**: FY 2025 (107.108 unit) & FY 2024
- **Status**: 🟢 Tersedia
- **Referensi Utama**: [[wiki/workdesk/business-memory/operational/CURRENT_OPERATING_STATE|Laporan Operasional Retail]]
- **Terakhir diperbarui**: Belum terkonfirmasi dari sumber otoritas
- **Frekuensi Pembaruan**: Belum terkonfirmasi
- **Periode belum tersedia**: Agustus 2026 (masih berjalan)
- **Bisa dipakai untuk**: Evaluasi target retail per cabang, analisis pencapaian bulanan, dan perbandingan tren year-on-year.
- **Catatan / batasan**: Total Retail FY 2025 adalah 107.108 unit. Angka 127.244 unit adalah Total Pasar (Market).

---

### Market Share
- **Data s.d.**: Juni 2026 (YTD Jan–Jun 2026) & FY 2025 (Jan–Des 2025)
- **Riwayat tersedia**: FY 2025 Total Market (127.244 unit) per Kabupaten, Brand, & Kompetitor
- **Status**: 🟢 Tersedia
- **Referensi Utama**: 
  - [[wiki/workdesk/business-memory/operational/CURRENT_OPERATING_STATE|Market Share Current 2026]]
  - [[wiki/workdesk/intelligence/MARKET_SHARE_2025_HISTORICAL_RECOVERY|Market Share Historis 2025]]
- **Terakhir diperbarui**: Belum terkonfirmasi dari sumber otoritas
- **Frekuensi Pembaruan**: Belum terkonfirmasi
- **Periode belum tersedia**: Juli 2026
- **Bisa dipakai untuk**: Analisis posisi kompetisi pasar, pengukuran market share per kabupaten, dan identifikasi pergeseran dominasi brand.
- **Catatan / batasan**: Hierarki mikro terverifikasi 2025: Area ID -> Kecamatan -> Kabupaten. Data tingkat Kelurahan/Desa 2025 belum terbukti (NOT_PROVEN).

---

### Territory & POLREG
- **Data s.d.**: Juni 2026
- **Riwayat tersedia**: 9 Market Areas, 118 Kecamatan, 1.223 Baris Kelurahan-Desa Terpetakan
- **Status**: 🟢 Tersedia
- **Referensi Utama**: [[wiki/workdesk/reference/AWD_CAPABILITY_REGISTRY|Data Registrasi Wilayah]]
- **Terakhir diperbarui**: Belum terkonfirmasi dari sumber otoritas
- **Frekuensi Pembaruan**: Belum terkonfirmasi
- **Periode belum tersedia**: Pemetaan tingkat desa diluar 1.223 baris kelurahan-desa terpetakan
- **Bisa dipakai untuk**: Pemetaan wilayah potensi mendalam dan alokasi area sales force.
- **Catatan / batasan**: Menggunakan cakupan aktual 118 kecamatan dan 1.223 baris kelurahan-desa terpetakan.

---

### Dealer & POS
- **Data s.d.**: Belum terkonfirmasi
- **Riwayat tersedia**: Hierarki Dealer → POS → FLP Tersedia
- **Status**: 🟠 Sebagian
- **Referensi Utama**: [[wiki/workdesk/reference/AWD_CAPABILITY_REGISTRY|Jaringan Dealer & POS]]
- **Terakhir diperbarui**: Belum terkonfirmasi dari sumber otoritas
- **Frekuensi Pembaruan**: Belum terkonfirmasi
- **Periode belum tersedia**: Total jaringan acuan terkini belum terkonfirmasi dari sumber otoritas khusus
- **Bisa dipakai untuk**: Audit jangkauan jaringan dan evaluasi kinerja operasional cabang.
- **Catatan / batasan**: Hierarki Dealer → POS → FLP tersedia; total jaringan acuan terkini belum terkonfirmasi.

---

### Ring Penjualan
- **Data s.d.**: 2022 (Historis)
- **Riwayat tersedia**: 803 catatan pemetaan Dealer/POS ke Kecamatan (Ring 1–3)
- **Status**: ⚪ Historis
- **Referensi Utama**: [[wiki/workdesk/reference/AWD_CAPABILITY_REGISTRY|Matriks Ring Penjualan]]
- **Terakhir diperbarui**: 2022
- **Frekuensi Pembaruan**: Belum terkonfirmasi
- **Periode belum tersedia**: Pemutakhiran Ring versi 2026 belum terkonfirmasi dari sumber otoritas
- **Bisa dipakai untuk**: Acuan historis pembagian Ring 1–3 per kecamatan.
- **Catatan / batasan**: Merupakan data historis 2022 dan tidak boleh diklaim sebagai data mutakhir.

---

### Stock Kendaraan
- **Data s.d.**: Snapshot Dealer 6 Aug 2026 (08:03:42) & MD 6 Aug 2026 (08:04:46)
- **Riwayat tersedia**: Stock Dealer (5.239 unit) & Stock MD (3.496 unit)
- **Status**: 🟢 Tersedia
- **Referensi Utama**: [[wiki/workdesk/business-memory/operational/CURRENT_OPERATING_STATE|Laporan Snapshot Stock]]
- **Terakhir diperbarui**: Dealer: 2026-08-06 08:03:42 | MD: 2026-08-06 08:04:46
- **Frekuensi Pembaruan**: Belum terkonfirmasi
- **Periode belum tersedia**: Data umur stock (MD aging) belum disediakan sumber
- **Bisa dipakai untuk**: Monitoring ketersediaan stok fisik saat snapshot diambil.
- **Catatan / batasan**: Merupakan posisi snapshot tanggal 6 Agustus 2026, bukan data running bulanan.

---

### Produk & Model
- **Data s.d.**: Juli 2026
- **Riwayat tersedia**: Lineup Sepeda Motor 2025–2026
- **Status**: 🟢 Tersedia
- **Referensi Utama**: [[wiki/workdesk/reference/AWD_CAPABILITY_REGISTRY|Katalog Produk & Tipe]]
- **Terakhir diperbarui**: Belum terkonfirmasi dari sumber otoritas
- **Frekuensi Pembaruan**: Belum terkonfirmasi
- **Periode belum tersedia**: Belum terkonfirmasi tipe terbaru pasca Juli 2026
- **Bisa dipakai untuk**: Analisis bauran produk (product mix) dan perencanaan target per tipe.
- **Catatan / batasan**: Berdasarkan katalog resmi tipe sepeda motor.

---

### Pembiayaan & Finance
- **Data s.d.**: Juli 2026
- **Riwayat tersedia**: FY 2025 & YTD 2026 per Leasing Partner
- **Status**: 🟢 Tersedia
- **Referensi Utama**: [[wiki/workdesk/reference/AWD_CAPABILITY_REGISTRY|Data Mitra Pembiayaan]]
- **Terakhir diperbarui**: Belum terkonfirmasi dari sumber otoritas
- **Frekuensi Pembaruan**: Belum terkonfirmasi
- **Periode belum tersedia**: Agustus 2026
- **Bisa dipakai untuk**: Evaluasi kontribusi leasing partner dan monitoring rasio kredit vs tunai.
- **Catatan / batasan**: Data mencakup transaksi pembiayaan terkonfirmasi.

---

### Customer Segment
- **Data s.d.**: Juli 2026
- **Riwayat tersedia**: FY 2025 & YTD 2026
- **Status**: 🟢 Tersedia
- **Referensi Utama**: [[wiki/workdesk/reference/AWD_CAPABILITY_REGISTRY|Database Segmen Konsumen]]
- **Terakhir diperbarui**: Belum terkonfirmasi dari sumber otoritas
- **Frekuensi Pembaruan**: Belum terkonfirmasi
- **Periode belum tersedia**: Agustus 2026
- **Bisa dipakai untuk**: Segmentasi demografi dan profil pekerjaan pembeli.
- **Catatan / batasan**: Data dianonimkan sesuai prinsip privasi.

---

### Customer Lifecycle & Repeat Order
- **Data s.d.**: Juli 2026
- **Riwayat tersedia**: Database Consumer & Repeat Order
- **Status**: 🟢 Tersedia
- **Referensi Utama**: [[wiki/workdesk/reference/AWD_CAPABILITY_REGISTRY|Program Retensi Konsumen]]
- **Terakhir diperbarui**: Belum terkonfirmasi dari sumber otoritas
- **Frekuensi Pembaruan**: Belum terkonfirmasi
- **Periode belum tersedia**: Agustus 2026
- **Bisa dipakai untuk**: Telemarketing retensi dan program tukar tambah (trade-in).
- **Catatan / batasan**: Menggunakan kunci pencocokan identitas konsumen terverifikasi.

---

### FLP & Manpower
- **Data s.d.**: Juli 2026
- **Riwayat tersedia**: Roster Sales Force Active 2026
- **Status**: 🟢 Tersedia
- **Referensi Utama**: [[wiki/workdesk/reference/AWD_CAPABILITY_REGISTRY|Data Tenaga Penjualan]]
- **Terakhir diperbarui**: Belum terkonfirmasi dari sumber otoritas
- **Frekuensi Pembaruan**: Belum terkonfirmasi
- **Periode belum tersedia**: Agustus 2026
- **Bisa dipakai untuk**: Evaluasi produktivitas sales force rata-rata per orang.
- **Catatan / batasan**: Hanya mencakup FLP berstatus aktif di roster.

---

### Sales Activity & Leads
- **Data s.d.**: Juli 2026
- **Riwayat tersedia**: Activity Tracking & Prospect Leads 2026
- **Status**: 🟢 Tersedia
- **Referensi Utama**: [[wiki/workdesk/reference/AWD_CAPABILITY_REGISTRY|Laporan Aktivitas Sales]]
- **Terakhir diperbarui**: Belum terkonfirmasi dari sumber otoritas
- **Frekuensi Pembaruan**: Belum terkonfirmasi
- **Periode belum tersedia**: Agustus 2026
- **Bisa dipakai untuk**: Evaluasi aktivitas lapangan dan konversi prospek.
- **Catatan / batasan**: Berdasarkan log aktivitas terverifikasi.

---

### Promotion & Program
- **Data s.d.**: YTD Agustus 2026
- **Riwayat tersedia**: Program Promo Q1–Q3 2026
- **Status**: 🟢 Tersedia
- **Referensi Utama**: [[wiki/workdesk/reference/AWD_CAPABILITY_REGISTRY|Katalog Program Promo]]
- **Terakhir diperbarui**: Belum terkonfirmasi dari sumber otoritas
- **Frekuensi Pembaruan**: Belum terkonfirmasi
- **Periode belum tersedia**: September 2026 dan setelahnya belum tersedia pada acuan saat ini.
- **Bisa dipakai untuk**: Evaluasi efektivitas subsidi dan diskon promo.
- **Catatan / batasan**: Mencakup promo reguler dan promo khusus YTD Agustus 2026.

---

### Commercial & MSW
- **Data s.d.**: Agustus 2026 (Program Family Aug 2026)
- **Riwayat tersedia**: Fleet Account 2026
- **Status**: 🟢 Tersedia
- **Referensi Utama**: [[wiki/workdesk/business-memory/operational/CURRENT_OPERATING_STATE|Data Penjualan Commercial]]
- **Terakhir diperbarui**: Belum terkonfirmasi dari sumber otoritas
- **Frekuensi Pembaruan**: Belum terkonfirmasi
- **Periode belum tersedia**: September 2026
- **Bisa dipakai untuk**: Pengelolaan akun fleet korporat dan skema MSW.
- **Catatan / batasan**: Menggunakan acuan program family Agustus 2026.

---

### Market Info & Event
- **Data s.d.**: Agustus 2026 (Alur Proses per 11 Aug 2026)
- **Riwayat tersedia**: Event Calendar 2026 (Catatan Historis Belum Disediakan)
- **Status**: 🟡 Perlu Pembaruan
- **Referensi Utama**: [[wiki/workdesk/business-memory/operational/CURRENT_OPERATING_STATE|Kalender Event & Competitor Info]]
- **Terakhir diperbarui**: Belum terkonfirmasi dari sumber otoritas
- **Frekuensi Pembaruan**: Belum terkonfirmasi
- **Periode belum tersedia**: Rekaman historis mingguan belum disediakan sumber (belum disediakan)
- **Bisa dipakai untuk**: Pemantauan jadwal event dan alur kerja pengumpulan intelijen pasar.
- **Catatan / batasan**: Membedakan antara proses kerja yang tersedia vs data historis mingguan yang belum disediakan.

---

### Standar NOS
- **Data s.d.**: Juli 2026
- **Riwayat tersedia**: Hasil Audit NOS Q1–Q2 2026
- **Status**: 🟢 Tersedia
- **Referensi Utama**: [[wiki/workdesk/reference/AWD_CAPABILITY_REGISTRY|Hasil Audit Kualitas NOS]]
- **Terakhir diperbarui**: Belum terkonfirmasi dari sumber otoritas
- **Frekuensi Pembaruan**: Belum terkonfirmasi
- **Periode belum tersedia**: Hasil audit semester II 2026
- **Bisa dipakai untuk**: Evaluasi pemenuhan standar fasilitas fisik dan mutu layanan dealer.
- **Catatan / batasan**: Nilai berdasarkan audit resmi standar NOS.

---

### Integrated TTM & Network
- **Data s.d.**: Snapshot Agustus 2026 (Sinsen POS Snapshot 11 Aug 2026)
- **Riwayat tersedia**: Network Coverage Map 2026
- **Status**: 🟠 Sebagian
- **Referensi Utama**: [[wiki/workdesk/business-memory/operational/CURRENT_OPERATING_STATE|Peta Jaringan & TTM]]
- **Terakhir diperbarui**: Belum terkonfirmasi dari sumber otoritas
- **Frekuensi Pembaruan**: Belum terkonfirmasi
- **Periode belum tersedia**: Kesiapan pengajuan resmi (kesiapan pengajuan) belum terbukti
- **Bisa dipakai untuk**: Visualisasi peta jangkauan jaringan dan lokasi POS Sinsen.
- **Catatan / batasan**: Kesiapan pengajuan ekspansi jaringan fisik masih memerlukan pembuktian dokumen resmi (kesiapan pengajuan belum terbukti).
