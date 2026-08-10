# Sales & Stock Monitoring — Mulai Cek dari MD sampai Series

## Cepat ngerti

Kalau sales berubah, source ini mengajarkan **jangan langsung lompat ke satu Dealer atau satu alasan**.

Mulai dari gambaran besar, lalu turun:

`Total MD → Kabupaten → Dealer → Series`

Dan pada level total MD, **sales dibaca bersama stock dan flow unit**, bukan sendirian.

## Apa yang dilihat di Total MD?

**Dari source:**

- Sales.
- Stock Main Dealer.
- Stock Dealer.
- AHM–MD in-transit.
- AHM Distribution.
- All Type dan detail per series.
- Perbandingan `M` vs `M-1`.

Tujuannya antara lain memastikan komposisi stock MD–Dealer seimbang dan stock tidak menumpuk di in-transit.

## Kenapa sales harus dibaca bareng stock?

Karena angka sales turun bisa muncul bersamaan dengan kondisi inventory yang berbeda-beda.

Source tidak memberi root-cause tree lengkap, tetapi jelas mengajarkan bahwa **availability/flow stock adalah konteks yang perlu dibaca bersama movement sales**.

## Lalu turun ke Kabupaten

**Dari source:** compare Daily Sales & Stock `M` vs `M-1` per Kabupaten.

Gunanya:

- lihat Kabupaten mana yang growth-nya naik/turun;
- kombinasikan dengan economic-driver information;
- lihat All Type dan per-series.

## Turun lagi ke Dealer dan Series

Setelah Kabupaten dipilih:

1. cari Dealer yang menyebabkan positive/negative growth;
2. di Dealer tersebut, cari series yang menyebabkan movement;
3. ulangi untuk Kabupaten lain yang perlu dianalisis.

## “How to Analyze” dari source

Slide 10 memberi urutan eksplisit:

1. Lihat total all-Kabupaten Daily Sales Growth `M` vs `M-1`.
2. Lihat detail Kabupaten dan identifikasi Kabupaten yang growth-nya “lebih” dari total; gunakan economic-driver information untuk pendalaman.
3. Break down Kabupaten ke Dealer.
4. Break down Dealer ke series.
5. Ulangi proses pada Kabupaten yang memenuhi kriteria source.

## Caveat penting

Kalimat source mengenai Kabupaten dengan `growth > growth total` dipertahankan apa adanya. Deck tidak menjelaskan apakah itu satu-satunya selection rule untuk kasus underperformance/negative contribution.

Jadi jangan membuat rule baru seperti:

> “hanya Kabupaten di atas total yang boleh direview.”

Sampai source lain menjelaskan konteksnya.

## Metric yang muncul

- Daily Sales `M` vs `M-1`.
- Daily Sales Growth % dan gap.
- Dealer Stock `M` vs `M-1`.
- Stock Growth % dan gap.
- Stock MD.
- In-transit AHM–MD.
- AHM Distribution.
- All Type / series.

**Formula growth/gap tidak ditulis eksplisit pada deck ini**, jadi WorkDesk tidak mengarang formula source-specific.

## Source

`10. Sales _ Stock Monitoring per Dealer.pptx`

- Hierarchy: slide 2.
- Total MD sales/stock/in-transit/distribution: slide 4.
- Series breakdown: slide 5.
- Kabupaten: slide 7.
- Dealer: slide 9.
- How to Analyze: slide 10.
