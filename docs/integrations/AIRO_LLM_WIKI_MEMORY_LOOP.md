# AIRO LLM Wiki Memory Loop Protocol v0.6

- **Status:** `ACTIVE_GOVERNED_CONTRACT`
- **Scope:** `ASB_GLOBAL`
- **Authoritative Boundary:** Derivative Knowledge Only (`canonical: false`)

---

## 1. Apa itu Session?
Sesi kerja (*Session*) adalah rekam jejak kerja sementara yang mencatat aktivitas, perintah, verifikasi, dan hasil akhir dari satu pekerjaan spesifik dengan satu tujuan utama (*one project + one main objective*). Sesi disimpan secara permanen di `worklog/sessions/` setelah melalui validasi bukti.

## 2. Apa itu Wiki?
LLM Wiki adalah basis pengetahuan derivatif berstruktur (*structured derivative knowledge base*) yang menyimpan konsep, sumber, dan sintesis pembelajaran dari pengalaman operasional AIRO. Wiki membantu AI dan manusia memahami aturan, pola kegagalan, dan solusi terbaik tanpa harus membaca ulang seluruh riwayat obrolan atau log mentah.

## 3. Kapan sesuatu layak diingat? (`WORTH_REMEMBERING=YES`)
Suatu informasi dari Sesi **layak diingat** apabila memenuhi setidaknya satu kriteria berikut:
- **Akar Masalah Bug & Solusi**: Berhasil menemukan penyebab utama bug dan cara memperbaikinya.
- **Aturan Operasional Baru**: Menemukan pola kegagalan yang harus dicegah secara deterministik di masa depan.
- **Perilaku Alat/Sistem Non-Obvious**: Menemukan perilaku tersembunyi dari alat atau lingkungan kerja yang berguna bagi sesi mendatang.
- **Pola Eksekusi Teruji**: Menemukan alur kerja yang terbukti efisien dan aman.

## 4. Kapan harus dilewati? (`WORTH_REMEMBERING=NO`)
Suatu informasi **harus dilewati** apabila:
- Hanya berupa laporan kemajuan rutin (*normal progress update*).
- Berisi perintah atau perintah sederhana yang tidak menghasilkan wawasan baru.
- Merupakan diskusi mentah yang belum menghasilkan kesimpulan teruji.
- Merupakan informasi faktual yang sudah tercatat dengan jelas di dokumen kanonis atau Wiki yang ada.

## 5. Dari Session ke Memory Candidate
Alur perubahan dari catatan Sesi menjadi kandidat memori:

```text
SESSION
  │
  ▼
WORTH_REMEMBERING? (Evaluasi Semantik)
  ├── NO  ──► SKIP (Selesai)
  └── YES ──► MEMORY CANDIDATE (distill/proposals/wiki/)
                │
                ▼
              PROVENANCE CHECK (Path, Commit, Section)
                │
                ▼
              INGEST / MERGE (wiki/concepts/)
                │
                ▼
              LINT & QUERY (Automated Verification)
```

## 6. Provenance Wajib
Setiap fakta atau aturan di dalam kandidat memori dan catatan Wiki **wajib mencantumkan provenance lengkap**:
- `source_path`: Path relatif repositori ke catatan Sesi asal.
- `source_commit`: Hash komit Git persis saat catatan Sesi dibuat/divalidasi.
- `source_section`: Judul seksi persis di dalam catatan Sesi asal.

## 7. Candidate ke Wiki
Kandidat memori yang dibuat oleh alat `scripts/airo-wiki-memory-candidate` disimpan di `distill/proposals/wiki/`. Kandidat ini menjadi bahan usulan sebelum diintegrasikan ke dalam halaman konsep Wiki.

## 8. Merge vs Create
- **MERGE**: Jika konsep yang relevan sudah ada di `wiki/concepts/`, kandidat akan memperkaya halaman konsep tersebut tanpa membuat berkas duplikat.
- **CREATE**: Jika belum ada konsep yang setara, konsep baru akan dibuat di bawah `wiki/concepts/`.

## 9. Lint dan Query
- **Lint**: Menguji keterhubungan tautan, ketersediaan sumber provenance, ketiadaan kunci rahasia, serta memastikan tidak ada kebocoran `canonical: true`.
- **Query**: Memastikan pengetahuan Wiki dapat ditemukan dan dijawab secara akurat berdasarkan bukti faktual.

## 10. Wiki bukan Source of Truth
Wiki bersifat derivatif (`canonical: false`). Wiki **tidak pernah boleh** menggantikan atau merubah dokumen kanonis seperti PRD, Roadmap, Log Keputusan, atau status proyek secara sepihak.

## 11. Canonical Promotion Membutuhkan Workflow Terpisah
Promosi dari pengetahuan Wiki ke status kanonis (*Canonical Promotion*) membutuhkan alur kerja formal terpisah dan persetujuan eksplisit Owner.

## 12. Contoh Real Workflow
- **Sesi Asal**: Sesi M2 (`02 - M2 Session & Worklog Implementation.md`).
- **Pelajaran**: Script success (`EXIT_CODE=0`) bukan penanda tugas selesai (`BERHASIL`). Bukti wajib harus terpenuhi secara eksplisit.
- **Kandidat**: `distill/proposals/wiki/2026-08-05 - Execution Assurance — Script Success Is Not Task Success.md`.
- **Konsep Wiki**: `wiki/concepts/execution-assurance.md`.
