# Pricing, FID & BA4 — Harga Kredit dan Risiko Financing

## Cepat ngerti

Deck ini menghubungkan dua hal:

1. **Price Intelligence** — apakah paket Honda kompetitif terhadap competitor dan antar-Fincoy.
2. **FID / BA4** — apakah kualitas customer credit cukup sehat atau justru membuat Fincoy lebih selektif dan menghambat credit sales.

Jadi “harga kompetitif” bukan cuma OTR.

## Bagian 1 — Price Intelligence

### Komponen yang dibandingkan

**Dari source:**

- OTR Price.
- DP Pricelist.
- Discount.
- DP Real / DP bayar.
- Installment.
- Credit Rate.
- Head-to-head type.
- Paket antar-Fincoy.

### DP Real

`DP Real = DP Pricelist - Discount`

Ini formula yang memang tertulis di source.

### Pelajaran penting

Pada worked example, OTR Honda bisa kompetitif tetapi paket tetap dinilai kurang kompetitif karena **DP Real, installment, atau rate** lebih buruk.

Jadi:

> OTR bagus ≠ otomatis total credit package bagus.

### Cadence source

Pricing analysis vs competitor disebut dilakukan **minimal 1×/month** pada training deck ini.

Follow-up source juga meminta validasi Market Data 2 dan review bersama Dealer/Fincoy.

## Bagian 2 — FID

**FID = First Installment Default.**

`FID = Bad Customer / Total Booking`

FID6 pada deck memonitor booking cohort dan kondisi pembayaran untuk 6 bulan berikutnya.

**Contoh historis threshold 2023:**

- ADIRA FID6: 3%.
- OTO FID6: 5%.
- MCF FID6: 2%.

Jangan anggap angka tersebut current 2026 policy tanpa source terbaru.

## Bagian 3 — BA4

**BA = Bad Account.**

`BA = Bad Customer / Total Booking`

BA4 pada deck memonitor cohort selama 4 bulan berikutnya.

**Contoh historis source:** standard BA4 2.5%, dengan `<2.5%` dilabeli sehat; Fincoy yang disebut untuk BA4 adalah FIF.

Sekali lagi: **historical 2023**, bukan current policy.

## Kenapa FID / BA4 penting ke sales?

Source menjelaskan bahwa FID/BA tinggi dapat membuat finance company lebih selektif, khususnya pada low DP atau customer/area yang dianggap berisiko.

Maka ada hubungan yang perlu dicek:

`credit quality memburuk → Fincoy lebih selektif → akses kredit bisa mengetat → credit sales bisa terdampak`

Ini hubungan yang dinyatakan source, tetapi kondisi current harus dicek dengan data/current policy.

## Cara review FID/BA menurut source

1. Ambil data per Finance Company, series, branch/Dealer.
2. Lihat trend 3 bulan.
3. Bandingkan periode yang sama tahun lalu.
4. Cari konsentrasi risk.
5. Breakdown berdasarkan series, DP layer, consumer occupation segment, dan faktor lain yang dinyatakan source.
6. Diskusi bersama Dealer/Fincoy.
7. Sepakati improvement dan support sales.

## Formula yang sengaja belum dipakai

Deck menampilkan formula `Rate After Discount` dan `Rate Before Discount`, tetapi teks hasil render mengandung term `-1` yang ambigu.

Status WorkDesk:

`FORMULA_UNRESOLVED`

Jangan dipakai menghitung sampai ada source authoritative lain yang menjelaskan formula tersebut.

## Source

`11. Analisa Pricing _ FID-BA.pptx`

- Pricing objectives/components: slide 3.
- Head-to-head pricing analysis: slide 4.
- Pricing follow-up: slide 5.
- FID: slide 7.
- BA4: slide 8.
- Why FID/BA matters: slide 9.
- Trend examples: slides 10–13.
- MD follow-up: slide 14.
