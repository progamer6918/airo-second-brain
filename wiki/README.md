# AIRO Wiki Layer README

Wiki ini adalah lapisan pengetahuan derivatif yang dirancang untuk mensintesis informasi di dalam ekosistem AIRO.

## Perbedaan Canonical vs Derivative
- **Canonical**: BOOT.md, CURRENT.md, CONTEXT.md, projects/, decisions/, state/, systems/, docs/. Berkas-berkas ini adalah source of truth utama.
- **Derivative**: Isi namespace `wiki/`. Berkas-berkas di sini disintesis dari canonical sources dan tidak boleh menimpa canonical state secara diam-diam.

## Peta Direktori
- `concepts/`: Entitas dan ide yang dapat digunakan kembali.
- `sources/`: Catatan sumber derivatif yang bersih dari data sensitif.
- `syntheses/`: Hasil analisis dari berbagai konsep/sumber.
- `indexes/`: Navigasi wiki (misal: home.md).
- `dashboards/`: Status pemeliharaan wiki (misal: status.md).
- `templates/`: Template catatan untuk source, concept, dan synthesis.

## Kebijakan Sensitivitas (Sensitivity Policy)
- **public**: Konten bersih yang aman disimpan di ASB.
- **private-reference-only**: Menyimpan referensi/metadata aman saja, bukan konten mentah pribadi.
- **restricted**: Konten mentah pribadi, percakapan rahasia, token, API keys, dll DILARANG keras ditulis di ASB.

## Siklus Hidup Catatan (Note Lifecycle)
- **draft**: Dihasilkan tapi belum divalidasi.
- **reviewed**: Provenance dan klaim telah diperiksa.
- **stale**: Sumber canonical berubah setelah peninjauan.
- **contradicted**: Sumber canonical saling bertentangan.
- **deprecated**: Dipertahankan untuk sejarah, bukan panduan aktif.

## Hak Akses Penulisan Agen (Agent Write Permissions)
- **Antigravity**: Bounded semantic/file executor untuk wiki mutation.
- **Hermes/Earesmes**: Read/query/front-door saja (sampai M6).
- **ChatGPT/Claude**: Optional reasoning & review (bukan autonomous local writers).
- **Terminal/scripts**: Deterministic validation, Git plumbing, lint, and scheduling.

## Prosedur Resolusi Konflik (Conflict Resolution)
1. Canonical content menang secara mutlak.
2. Wiki content yang bertentangan ditandai sebagai `contradicted` atau `stale`.
3. Proposal perubahan canonical diajukan jika koreksi canonical diperlukan.

## Batasan Sinkronisasi Git
Tidak ada sinkronisasi Git independen atau auto-sync otomatis untuk wiki namespace. Semua perubahan diatur oleh kebijakan repositori ASB.
