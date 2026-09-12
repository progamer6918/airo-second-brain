# AIRO Finance Lab — User Experience Acceptance Report (v1.0)

- **Project**: `AIRO_FINANCE_LAB`
- **Document ID**: `AIRO_FINANCE_USER_EXPERIENCE_ACCEPTANCE_REPORT_V1`
- **Status**: `LOCKED_ACCEPTANCE_REPORT`
- **Date**: `2026-09-11`
- **Task**: `AIRO_FINANCE_LAB_USER_EXPERIENCE_ACCEPTANCE_V1`
- **Role**: `AIRO Executor Agent`
- **Mode**: `DESIGN_AND_VALIDATION`
- **Focus**: `USER_EXPERIENCE_ONLY` (No Architecture Expansion)
- **Source of Truth**: M1-M9 Live Evidence, Web Dashboard, Telegram Adapter, Hermes Read Adapter

---

## 1. Executive Summary & Pertanyaan Inti Produk

Laporan ini memvalidasi produk nyata AIRO Finance Lab dari sudut pandang pengalaman pengguna (*User Experience / UX*) Owner (Egit). Evaluasi ini menjawab dua pertanyaan esensial sebelum melangkah ke Phase 2:

### Pertanyaan 1: Jika Owner membuka AIRO Finance besok pagi, apa yang BISA dilakukan?
1. **Mencatat Pengeluaran Harian Seketika (<3.5 detik)**: Mengetik teks bebas 1-baris seperti `"kopi 25k"` atau `"makan siang 35k bca"` di Telegram, mendapatkan kartu konfirmasi interaktif, dan membatalkan dalam 1 klik jika typo.
2. **Melihat Saldo Kas Terkini & Riwayat Transaksi**: Membuka Web Dashboard di browser laptop/ponsel dalam <1 detik untuk melihat total saldo likuid, rincian per rekening (BCA, Blu, Mandiri, Cash), dan tabel mutasi buku besar real-time.
3. **Mencatat Transaksi Manual Desktop**: Menggunakan form modal Web Dashboard jika sedang bekerja di depan PC tanpa membuka ponsel.
4. **Bertanya Fakta Keuangan ke Hermes**: Bertanya di Telegram tentang saldo, total belanja bulan berjalan, dan pos pengeluaran paling boros dengan jawaban instan dan bebas halusinasi.

### Pertanyaan 2: Apa yang BELUM BISA dilakukan?
1. **Transfer Rekening via Chat**: Belum bisa mencatat pemindahan saldo antar-rekening melalui Telegram (misal: `"trf 500k bca ke mandiri"`). Saat ini transfer harus dicatat lewat Web Modal.
2. **Mengetahui Uang Aman Belanja (*Safe-to-Spend*)**: Hermes dan Dashboard belum bisa memberi tahu berapa sisa uang yang aman dijajankan setelah dikurangi kewajiban tagihan rutin bulanan dan batas dana darurat.
3. **Melihat Estimasi Ketahanan Kas (*Payday Runway*)**: Belum ada visualisasi atau hitungan berapa hari kas bertahan hingga tanggal gajian berikutnya.
4. **Menerima Rekap Mingguan Otomatis**: Belum ada notifikasi rekap belanja berkala di Minggu malam.
5. **Mengekspor Data ke CSV**: Belum ada tombol unduh CSV di Web Dashboard untuk backup mandiri.

---

## 2. Status Permukaan Produk Saat Ini (*Current Product View*)

```text
+-----------------------------------------------------------------------------------+
| 1. TELEGRAM QUICK CAPTURE SURFACE                                                 |
| Status: OPERATIONAL & STABLE (M3/M4/M9)                                           |
| Akses: Chat Telegram Bot AIRO Finance                                             |
| UX: Input 1-baris -> Inline Keyboard Confirmation [Konfirmasi] [Batal]           |
| Kecepatan: <3.5 detik total interaksi | Zero prompt loop                           |
+-----------------------------------------------------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
| 2. WEB DASHBOARD COCKPIT SURFACE                                                  |
| Status: OPERATIONAL & RESPONSIVE (M2)                                             |
| Akses: Localhost HTTP Server (Python standard library, tanpa dependensi berat)    |
| Layout: Dark Mode (Slate-900), 4 Balance Cards, Manual Entry Form, Ledger Table    |
| Kecepatan: Latensi render <1 detik | Auto-fetch data overview                     |
+-----------------------------------------------------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
| 3. HERMES REASONING SURFACE                                                       |
| Status: OPERATIONAL FACTUAL ADAPTER (M6/M7/M8)                                    |
| Akses: Chat AIRO Hermes Telegram                                                  |
| Respon: 4 Intent terpetakan (Saldo, Pengeluaran Bulanan, Kategori Boros, Anomali) |
| Kecepatan: <1 detik | Zero hallucination | Read-only enforcement                  |
+-----------------------------------------------------------------------------------+
```

---

## 3. Simulasi Alur Harian Owner (*Daily Workflow Simulation*)

Berikut adalah hasil simulasi skenario harian riil Owner:

### 3.1 Pagi Hari: *"Catat kopi 25k"* (Mobile Quick Capture)
- **Aksi Pengguna**: Owner membeli kopi di jalan, membuka Telegram, mengetik: `kopi 25k`.
- **Pengalaman Nyata**:
  - Bot mem-parse teks secara deterministik dalam hitungan milidetik.
  - Bot mengembalikan kartu konfirmasi:
    ```text
    📋 Konfirmasi Transaksi:
    Nominal : Rp25.000
    Arah    : PENGELUARAN
    Rekening: BCA Utama (Sane Default)
    Kategori: Makanan & Minuman
    Catatan : kopi

    [✅ Konfirmasi]  [❌ Batal]
    ```
  - Owner menekan `[✅ Konfirmasi]`. Saldo BCA terpotong Rp25.000, 1 baris audit log tercatat di SQLite.
- **Evaluasi UX**:
  - *Friksi*: Sangat rendah (<3.5 detik). Tidak ada kuis interogasi berulang.
  - *Safety Net*: Terbukti aman. Jika ada salah nominal (misal terketik `250k`), Owner cukup menekan `[❌ Batal]`.

### 3.2 Siang Hari: *"Berapa pengeluaran saya?"* (Hermes Quick Inquiry)
- **Aksi Pengguna**: Saat jam istirahat, Owner ingin tahu posisi belanja bulan ini via Hermes: *"Berapa pengeluaran bulan ini?"*.
- **Pengalaman Nyata**:
  - Hermes mengenali intent `MONTHLY_SPENDING_SUMMARY` dan memanggil tool agregat Finance Core.
  - Hermes menjawab:
    > *"Fakta Finansial Periode 2026-09: Total pengeluaran tercatat Rp2.150.000 dari 6 transaksi, total pemasukan Rp7.500.000, sehingga net cashflow saat ini Rp5.350.000."*
- **Evaluasi UX**:
  - *Friksi*: Nol friksi. Jawaban to-the-point dan akurat secara matematis.
  - *Missing Context*: Hermes belum memberi tahu apakah laju belanja ini termasuk cepat atau lambat dibandingkan tanggal dalam bulan berjalan, kecuali jika Owner menanyakan anomali secara eksplisit.

### 3.3 Malam Hari: *"Review kondisi keuangan saya"* (Evening Review)
- **Aksi Pengguna**: Owner membuka laptop di rumah untuk mengevaluasi keuangan harian.
- **Pengalaman Nyata**:
  - *Jalur Web Dashboard*: Membuka browser, seluruh kartu saldo (BCA, Blu, Mandiri, Cash) dan tabel mutasi langsung tampil.
  - *Jalur Hermes Chat*: Jika Owner bertanya *"Bagaimana kondisi keuangan saya malam ini?"*, Hermes memberikan ringkasan saldo likuid dan pengeluaran bulan ini, namun menyatakan batasan bahwa analisis komparatif mendalam belum tersedia.
- **Evaluasi UX**:
  - *Kekurangan Pengalaman (Missing Experience)*:
    1. Owner masih harus menghitung manual di kepala: *"Sisa uang Rp5 juta ini, yang kepakai untuk bayar kos dan tagihan berapa ya? Sisanya aman dijajanin berapa?"*.
    2. Belum ada indikator *Safe-to-Spend* atau sisa hari runway hingga gajian berikutnya.

---

## 4. Evaluasi Pengalaman Hermes: Database Query Interface vs Personal Assistant

Pertanyaan Kunci:
> **Apakah Hermes terasa sebagai (A) Database Query Interface atau (B) Personal Finance Assistant?**

### Hasil Evaluasi Empiris:
Hermes saat ini berada pada tahap **"Smart Query Interface with Conversational Phrasing" (Transisi antara A dan B)**:

1. **Mengapa Bukan Sekadar Query Interface (Bukan A Murni)?**
   - Hermes tidak memuntahkan raw JSON atau tabel mentah SQL.
   - Hermes merangkum fakta angka ke dalam kalimat bahasa Indonesia yang rapi, santun, dan komunikatif.
   - Hermes memiliki pemahaman anomali deterministik (bisa menjelaskan alasan suatu transaksi dianggap mencurigakan atau boros).

2. **Mengapa Belum Menjadi True Personal Finance Assistant (Belum B Penuh)?**
   - **Ketiadaan Konteks Komitmen Hidup**: Hermes belum tahu pengeluaran mana yang bersifat wajib (sewa rumah, listrik, utang) vs fleksibel (jajan, hobi).
   - **Ketiadaan Konteks Waktu Siklus Gaji**: Hermes belum tahu kapan uang masuk berikutnya akan tiba, sehingga tidak bisa memberi rasa tenang (*peace of mind*) mengenai ketahanan kas.
   - **Reaktif Murni**: Hermes hanya berbicara saat dipicu kata kunci spesifik. Ia belum memiliki memori kesinambungan obrolan finansial harian.

### Kesenjangan Pengalaman (*Experience Gaps*) yang Teridentifikasi:
- **Gap UX 1 (The Anxiety Gap)**: Saldo Rp5.000.000 tampak besar, tetapi tanpa data komitmen tetap, Owner tetap merasa cemas apakah uang tersebut cukup hingga akhir bulan.
- **Gap UX 2 (The Multi-Account Transfer Gap)**: Kebutuhan memindahkan uang antar rekening fisik masih terhambat karena belum bisa diketik santai di Telegram.
- **Gap UX 3 (The Passive Closure Gap)**: Belum adanya rekap mingguan hari Minggu malam membuat Owner tidak memiliki penutup evaluasi mingguan yang pasif dan tenang.

---

## 5. Rekomendasi Prioritas Fase Berikutnya (*Recommended Next Phase*)

Berdasarkan temuan pengalaman nyata pengguna, roadmap Phase 2 difokuskan secara presisi untuk menutup kesenjangan di atas:

1. **Langkah 1: Tambahkan Dukungan Transfer Rekening di Chat (`trf 500k bca ke mandiri`)**
   - Memberikan kelengkapan 100% pada pencatatan transaksi harian tanpa perlu buka modal web.
2. **Langkah 2: Model Komitmen Tetap & Parameter Siklus Gajian**
   - Menambahkan penanda `is_recurring` dan konfigurasi `payday_day` + `safety_floor` di Finance Core.
3. **Langkah 3: Buka Kemampuan Hermes Level 3 (Safe-to-Spend & Payday Runway)**
   - Mengubah Hermes dari *Smart Query Interface* menjadi *True Financial Awareness Partner* yang dapat menjawab: *"Berapa uang aman saya?"* dan *"Apakah saldo cukup s.d. gajian?"*.
4. **Langkah 4: Rekap Pasif Mingguan (Sunday Evening)**
   - Menghadirkan penutupan mingguan otomatis tanpa interogasi.
