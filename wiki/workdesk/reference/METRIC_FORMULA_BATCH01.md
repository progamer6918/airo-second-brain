# Metric & Formula — Batch 01

Hanya metric/formula yang memang didukung source. Kalau formula tidak ditulis jelas, statusnya tetap unresolved.

## DP Real

**Arti:** DP yang dibayar consumer setelah average credit discount.

`DP Real = DP Pricelist - Discount`

**Status:** explicit source formula.

**Source:** `11. Analisa Pricing _ FID-BA.pptx` slide 3.

## FID

**Nama:** First Installment Default.

`FID = Bad Customer / Total Booking`

FID6 pada deck memonitor booking cohort dan kondisi pembayaran selama 6 bulan berikutnya.

**Historical thresholds 2023 dari source:** ADIRA 3%, OTO 5%, MCF 2%.

**Status current:** belum diverifikasi.

**Source:** slide 7.

## BA / BA4

**Nama:** Bad Account.

`BA = Bad Customer / Total Booking`

BA4 pada deck memonitor cohort selama 4 bulan berikutnya.

**Historical source:** 2.5%, dengan `<2.5%` dilabeli sehat; Fincoy yang disebut adalah FIF.

**Status current:** belum diverifikasi.

**Source:** slide 8.

## Daily Sales Growth M vs M-1

Metric field dan basis perbandingan `M vs M-1` memang eksplisit dipakai pada Sales & Stock Monitoring.

**Formula:** `NOT EXPLICITLY DEFINED IN SOURCE`.

Jangan mengarang formula “resmi source” sampai ada source lain yang mendefinisikannya.

## Stock Growth M vs M-1

Field eksplisit pada deck.

**Formula:** `NOT EXPLICITLY DEFINED IN SOURCE`.

## Market Share

Dipakai pada PDCA dan PICA Market Share analysis.

**Formula:** `NOT DEFINED IN THESE FOUR SOURCES`.

## Rate After / Before Discount

Source menampilkan formula tetapi hasil render memiliki term `-1` yang ambigu.

**Status:** `FORMULA_UNRESOLVED`.

WorkDesk dilarang “membetulkan” berdasarkan pengetahuan umum sebelum ada source corroboration.
