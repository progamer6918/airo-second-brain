---
type: workdesk-home
project: AIRO_WORKDESK
workdesk_status: V1_CANDIDATE
audience: human
---
# 🏢 AIRO WorkDesk

> **Kerjaan apa yang mau lo beresin?**
>
> Lo tidak perlu tahu folder, framework, atau singkatan. Mulai dari kebutuhan atau gejala. WorkDesk yang memilih knowledge dan urutan analisis di belakang layar.

## ⚡ Mulai cepat

| Gue mau... | Masuk lewat |
|---|---|
| 🔎 Ngerti istilah / framework | [[learn/PICA|PICA]], [[learn/PDCA|PDCA]], [[learn/SALES_STOCK_MONITORING|Sales & Stock]], [[learn/PRICING_FID_BA|Pricing/FID/BA]] |
| 📊 Selesaikan masalah performance | [[playbooks/MARKET_SHARE_OR_RETAIL_DOWN|Retail / Market Share turun]] |
| 🧭 Review performance | [[review/SALES_AND_STOCK|Review Sales & Stock]] |
| 🛠 Bikin output | [[deliverables/PICA|Bikin PICA]] |
| ❓ Gue cuma tahu gejalanya | [[TASK_ROUTER|Bantu arahkan masalah gue]] |
| 📚 Mau deep dive | [[KNOWLEDGE_MAP_V1|Peta knowledge v1]] |

## Cara pakainya

Cukup ngomong pakai bahasa kerja biasa:

> "M/S AT High Kota Jambi turun bulan kemarin. Bantu gue cari kenapa."

> "Dealer ini stock banyak tapi retail nggak jalan."

> "Bikin PICA dari hasil analisis ini."

Untuk pertanyaan kerja seperti itu, AI harus langsung bekerja sebagai professional partner. Ceremony repo/AIRO control-plane tidak ditampilkan kecuali task memang soal ASB, Git, runtime, migration, atau governance.

## Prinsip trust

WorkDesk harus selalu membedakan:

- **fakta/source explicit**;
- **synthesis lintas-source**;
- **working hypothesis / inference**;
- **data current vs historical**;
- **data yang belum tersedia**.

Kalau bukti belum cukup, jawaban yang benar adalah `UNRESOLVED` atau `DATA_NOT_AVAILABLE`, bukan mengisi celah dengan tebakan.
