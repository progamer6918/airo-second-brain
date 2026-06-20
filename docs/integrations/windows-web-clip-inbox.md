# Windows Web Clip Inbox Bridge

Dokumen ini menjelaskan arsitektur dan panduan penggunaan jembatan kliping web dari sistem operasi Windows host ke repositori AIRO Second Brain di WSL Ubuntu.

## Arsitektur

1. **Brave Windows (Kliping)**: Pengguna menggunakan browser Brave di Windows untuk menangkap halaman web sebagai berkas Markdown.
2. **Inbox Transisi (Staging)**: Catatan Markdown disimpan ke folder lokal Windows `C:\Users\Admin\AIRO_CLIP_INBOX`.
3. **Penyelarasan WSL**: Repositori WSL Ubuntu mengakses direktori tersebut di jalur `/mnt/c/Users/Admin/AIRO_CLIP_INBOX`.
4. **Skrip Importir**: Skrip `scripts/airo-import-web-clip-inbox` menyaring, memvalidasi kepatuhan keamanan (tanpa rahasia/token, tanpa path absolut), melakukan deduplikasi, dan menyimpan catatan hasil sanitasi ke dalam direktori `wiki/sources/web-clips/` dengan frontmatter terstandarisasi.

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
