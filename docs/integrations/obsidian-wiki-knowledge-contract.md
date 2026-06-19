# Obsidian Wiki Knowledge Governance Contract

Kontrak tata kelola ini menetapkan aturan integrasi dan pemeliharaan Obsidian Wiki di dalam ekosistem AIRO.

---

## 1. Tujuan
Menyediakan mekanisme sintesis pengetahuan otomatis menggunakan LLM/Ar9av tanpa merusak integritas data canonical repositori ASB.

## 2. Hierarki Sumber Canonical (Canonical Hierarchy)
Pernyataan fakta di ekosistem AIRO ditentukan oleh prioritas berikut (tingkat atas meng-override tingkat bawah):
1. Keputusan eksplisit dari Owner (Egit)
2. Bukti runtime tervalidasi terbaru
3. Berkas di `decisions/`
4. Berkas `CURRENT.md` dan status proyek saat ini
5. Berkas di `projects/`
6. Berkas di `docs/validation/`
7. Berkas canonical ASB lainnya
8. Catatan derivatif di `wiki/`

*Aturan*: Tingkat yang lebih rendah dilarang menimpa atau meng-override tingkat di atasnya secara diam-diam.

## 3. Batasan Otoritas Mutasi & Peran Agen
- **Antigravity**: Bertindak sebagai pelaksana file/semantik berbatas untuk mutasi wiki.
- **Hermes/Earesmes**: Hanya diperbolehkan membaca/kueri (read-only) sampai dengan Milestone M6 selesai diimplementasikan.
- **Claude/ChatGPT**: Hanya digunakan untuk penalaran dan peninjauan (bukan penulis otonom lokal).
- **Scripts**: Hanya untuk plumbing Git, linting, validasi deterministik, dan penjadwalan.

## 4. Protokol Promosi (Promotion Protocol)
Wawasan wiki dapat memengaruhi data canonical hanya melalui prosedur terstruktur:
1. Pengumpulan bukti (evidence collected)
2. Identifikasi kontradiksi (contradiction identified)
3. Pembuatan proposal (proposal created)
4. Persetujuan Owner atau workflow terotorisasi
5. Eksekusi tugas canonical berbatas
6. Validasi kelulusan checks
7. Penyegaran catatan wiki (wiki note refreshed)

Dilarang keras melakukan promosi data secara otonom tanpa persetujuan Owner.

## 5. Provenance, Sensitivitas, & Lifecycle
- **Provenance**: Wajib menyertakan minimal: path sumber, git commit (jika ada), dan bagian spesifik sumber untuk setiap klaim fakta.
- **Sensitivitas**: Mengikuti pembagian kelas `public`, `private-reference-only`, dan `restricted`. Konten mentah pribadi atau rahasia dilarang ditulis di ASB.
- **Lifecycle**: Mengikuti status `draft`, `reviewed`, `stale`, `contradicted`, dan `deprecated`.

## 6. Kebijakan Rollback & Penghapusan
- Jika terjadi kegagalan integrasi, rollback dilakukan dengan menghapus hanya berkas derivatif wiki dan link Hermes/Antigravity yang dibuat oleh tugas tersebut tanpa mengganggu data canonical repositori ASB.
