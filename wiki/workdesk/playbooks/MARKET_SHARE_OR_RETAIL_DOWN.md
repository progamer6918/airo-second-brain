# Retail / Daily Sales / Market Share Turun — Cek dari Mana?

## Versi singkat

Jangan mulai dari “penyebab”. Mulai dari **definisi gejala dan contributor**.

`Definisikan gejala → baca sales & stock → lokal-kan contributor → kumpulkan evidence → uji penyebab → PI → CA → monitor lagi`

**Synthesis WorkDesk:** flow ini menggabungkan empat source Batch 01.

## Step 0 — Jelaskan gejala

Isi dulu:

- Metric: Retail / Daily Sales / Market Share.
- Periode: ______ vs ______.
- Scope: Main Dealer / Kabupaten / Dealer / Segment / Series.
- Perubahan: volume / growth / share.

Kalau ini belum jelas, diagnosis belum boleh jalan.

## Step 1 — Lihat performance bersama inventory context

Kalau datanya ada, cek:

- Sales.
- Stock Main Dealer.
- Stock Dealer.
- AHM–MD in-transit.
- AHM Distribution.
- Series breakdown.

**Dari source Sales & Stock:** sales di total-MD memang ditempatkan bersama stock/in-transit/distribution.

Tujuan step ini bukan langsung menyimpulkan “stock penyebab”. Tujuannya memastikan gejala dibaca bersama availability/flow context.

## Step 2 — Cari contributor terbesar

Pilih jalur berdasarkan pertanyaan awal.

### Area-led
`Main Dealer → Kabupaten → Dealer → Type/Series`

### Product-led
`Main Dealer → Segment/Type → Kabupaten → Dealer`

Jangan berhenti di total kalau movement sebenarnya terkonsentrasi di satu Kabupaten, Dealer, atau series.

## Step 3 — Tandai anomaly

PICA mengingatkan bahwa bukan cuma angka negatif yang perlu dilihat. Segment yang bergerak **berlawanan/anomalous** terhadap All Type juga bisa memberi clue.

## Step 4 — Kumpulkan evidence, bukan “daftar penyebab”

Evidence family yang memang muncul di Batch 01:

### Market / external
- market information;
- commodity prices;
- weather/natural disaster;
- political/social/environmental condition.

### Competitor
- sales program;
- price/discount/DP/installment;
- promotion / BTL / GC;
- competitor stock.

### Honda execution / internal
- Honda sales program/activity changes;
- Honda stock / short stock / fulfillment;
- execution AHM/MD strategy di Dealer.

### Pricing / financing
- OTR;
- DP Pricelist;
- Discount;
- DP Real;
- Installment/rate;
- FID/BA trend;
- Fincoy selectivity.

**Penting:** munculnya salah satu evidence di atas **belum membuatnya root cause**.

## Step 5 — Uji root cause

Untuk setiap dugaan, tanya:

### Apa yang berubah?
Kalau faktor itu sudah ada bulan lalu dan bulan ini, bagaimana ia menjelaskan penurunan yang baru terjadi?

### Kenapa objek lain tidak sama?
Kalau faktor luas seperti komoditas adalah penyebab, kenapa comparable series/area tidak menunjukkan pola yang sama?

### Besarnya cukup?
Kalau GC/event/short stock disebut penyebab, kuantifikasi apakah magnitude-nya cukup untuk menjelaskan gap.

### Apakah terjadi di contributor yang sama?
**Synthesis WorkDesk:** root cause idealnya muncul di area/product yang memang terbukti membawa contribution gap.

## Step 6 — Tulis Problem Identification

Format praktis:

> `[objek spesifik] mengalami [perubahan terukur] karena [mechanism yang sudah diuji], didukung oleh [evidence], sementara [alternative explanation] belum terbukti / sudah ditolak.`

Jangan tulis:

> “Sales turun karena market.”

kalau belum ada linkage yang terbukti.

## Step 7 — Buat Corrective Action

CA harus menyerang mechanism PI.

Kalau root cause-nya price/credit package, generic “tambah pameran” belum tentu relevan.

Kalau root cause-nya execution strategy di Dealer, action harus menyasar execution gap tersebut.

## Step 8 — Control dengan PDCA

Setelah action:

- monitor achievement vs target;
- re-check sales/stock/M/S;
- cek execution;
- diskusi next action;
- update evidence lapangan untuk cycle berikutnya.

## Kapan harus STOP?

Tandai `INSUFFICIENT_EVIDENCE` kalau:

- gejalanya belum bisa dilokal-kan;
- periode pembanding tidak konsisten;
- sales/stock tidak comparable;
- external cause tidak punya measurable linkage;
- satu-satunya evidence adalah contoh historis yang dipaksa jadi kondisi current.

## Source utama

- `10. Sales _ Stock Monitoring per Dealer.pptx` — slides 4–5, 7, 9–10.
- `12. PICA.pptx` — slides 4–6, 16–25, 27–30.
- `11. Analisa Pricing _ FID-BA.pptx` — slides 3–5, 7–14.
- `2. ASSDP Basic - PDCA.pptx` — slides 5–8.


---

## WorkDesk v1 - Actual data interface

When private business memory is available, replace dummy placeholders with the actual period data in this order:

1. market denominator / Honda / competitors for the requested geography + segment;
2. Honda retail by dealer × type/series;
3. dealer/product master mapping;
4. stock MD + dealer + inbound/distribution around the same period;
5. applicable commercial program/MSW for that exact period if pricing/financing is relevant;
6. case-specific funnel/activity/competitor/financing evidence only when needed to distinguish hypotheses.

### Important

If the requested Market Share period does not yet have market denominator data, do **not** manufacture M/S from Honda retail alone. State `MARKET_DENOMINATOR_NOT_AVAILABLE` and continue only with the parts that can be proven (for example Honda retail movement or stock context).
