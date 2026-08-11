# MSW 2026 Currentness + Retrieval

## Resolver rule
Always resolve `requested date → program family → applicable interval → explicit invalidation/revision → structured offer source`.

- Reject any artifact under a path explicitly marked `TIDAK BERLAKU`.
- For overlapping family versions, the later explicit revision/update applies only from its stated effective start; the earlier source may remain applicable before that start.
- Never extend a campaign outside its source period.
- Numerical OTR/DP/voucher/installment retrieval prefers the applicable structured XLSX; Juklak remains authority for program terms/claim rules where applicable.

## Known high-value version boundaries
- Jan 1–2: original Jan price-list families; Jan 3–31: revised files for the families present in `Revisi/`.
- Apr 1–3: nested folder `PL SMH Periode 1-3 April 2026` constrains those initial artifacts even where inner filenames misleadingly say 1–30. From Apr 4 use explicit updates where supplied.
- Jul 1: the supplied SMH/Accessories/Vario/MSW candidate is inside `TIDAK BERLAKU`. No valid replacement covering Jul 1 is supplied for those families; state `CURRENT_AUTHORITY_UNRESOLVED` rather than using it.
- Jul 2–31: active SMH/Accessories; Jul 3–31: updated BeAT MMC & New Vario Evo 160; Premium/EV have 1–31 sources.
- Aug 1–31: current supplied August family; structured price-list rows are normalized in `MSW_AUGUST_2026_COMMERCIAL_OFFERS.tsv`.

## August source campaign headers
- `1. PL SMH periode Agustus 2026.xlsx` — PL Periode 1 - 31 Agustus 2026 Desain Vario Street; Voucher diskon 600rb*; Potongan Angsuran 1 bulan*; dan Design Genio; Potongan Angsuran 1 bulan* | PL Periode 1 - 31 Agustus 2026 Desain CBR 150R; Potongan Angsuran 1 bulan*; dan Design Supra GTR; Voucher Diskon 600 rb*; Potongan Angsuran 1 Bulan*
- `2. PL SMH Accessories periode Agustus 2026.xlsx` — PL Periode 1 - 31 Agustus 2026 Desain PCX MMC; Voucher diskon 600rb*; Potongan Angsuran 1 bulan* dan Design CB Verza; Potongan angsuran 1 bulan*
- `3. PL BeAT MMC Agustus 2026.xlsx` — Desain BeAT Sporty MMC (tipe baru); Voucher Diskon 150rb*; Special Gift Jaket* dan BeAT Street (tipe baru); Potongan Angsuran 1 bulan* Periode 1-31 Agustus 2026
- `5. PL Premium periode Agustus 2026.xlsx` — Periode 1 - 31 Agustus 2026 - Wing Dealer & Satelit Mandiri | Periode 1-31 Agustus 2026 - Wing Dealer & Satelit Mandiri
- `6. PL EV periode Agustus 2026.xlsx` — Berlaku Mulai 1-31 Agustus 2026 Design Motor EM1 e Series; Potongan Angsuran 1 bulan; Voucher Subsidi 8 Jt* dan Design motor Icon; Potongan Angsuran 1 bulan*; Voucher Subsidi 4 Jt*

## Example retrieval on 2026-08-11
Date is inside the supplied Aug 1–31 interval. Query `MSW_AUGUST_2026_COMMERCIAL_OFFERS.tsv` by product/program family. Do not quote a price/program from memory if the product row is absent; return missing/not supplied.
