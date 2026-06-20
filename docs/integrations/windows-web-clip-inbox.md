# Windows Web Clip Inbox Bridge

Dokumen ini menjelaskan arsitektur dan panduan penggunaan jembatan kliping web dari sistem operasi Windows host ke repositori AIRO Second Brain di WSL Ubuntu.

## Arsitektur

1. **Brave Windows (Kliping)**: Pengguna menggunakan browser Brave di Windows untuk menangkap halaman web sebagai berkas Markdown.
2. **Inbox Transisi (Staging)**: Catatan Markdown disimpan ke folder lokal Windows `C:\\Users\\Admin\\AIRO_CLIP_INBOX`. Ekstensi Obsidian Web Clipper secara default menyimpan catatan hasil kliping ke dalam subfolder `Clippings/`.
3. **Penyelarasan WSL**: Repositori WSL Ubuntu mengakses direktori tersebut di jalur `/mnt/c/Users/Admin/AIRO_CLIP_INBOX`.
4. **Skrip Importir**: Skrip `scripts/airo-import-web-clip-inbox` melakukan pemindaian rekursif, menyaring berkas non-Markdown, memvalidasi kepatuhan keamanan (tanpa rahasia/token, tanpa path absolut), melakukan deduplikasi, dan menyimpan catatan hasil sanitasi ke dalam direktori `wiki/sources/web-clips/` dengan frontmatter terstandarisasi.

## Penanganan Kliping Khusus

- **Subfolder Clippings**: Importer mendukung pemindaian rekursif di bawah staging vault, termasuk subfolder `Clippings/` tempat penyimpanan default Obsidian Web Clipper. Direktori pengawasan konseptual `.obsidian/` diabaikan secara otomatis dari pemindaian.
- **Kliping Percakapan (Conversation Clips)**: Berkas kliping yang diidentifikasi sebagai transkrip obrolan/percakapan nyata (seperti ChatGPT atau Claude) tidak diimpor secara mentah (*raw*) ke dalam repositori kanonik ASB. Hal ini dikarenakan transkrip percakapan obrolan memerlukan alur kerja penyulingan (*distillation workflow*) terlebih dahulu sebelum informasi bernilai di dalamnya dipromosikan ke wiki.

## Panduan Penggunaan Skrip

Jalankan skrip importir di terminal WSL:

```bash
# Untuk melihat bantuan opsi
./scripts/airo-import-web-clip-inbox --help

# Untuk menjalankan simulasi (dry-run) tanpa menulis data ke disk
./scripts/airo-import-web-clip-inbox --dry-run

# Untuk menjalankan importir riel
./scripts/airo-import-web-clip-inbox
```
