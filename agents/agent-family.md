# Agent Family — Ekosistem AIRO

## Overview

Ekosistem AIRO terdiri dari beberapa agent dengan peran berbeda. Semua berinteraksi dengan Egit via Telegram. Earesmes adalah orchestrator (saat ini masih Opsi 3 — aware tapi belum active orchestration).

## Agent Registry

### Earesmes
- **Peran**: Orchestrator / asisten utama
- **Interface**: Telegram
- **Status**: Aktif
- **Runtime**: Hermes (WSL2 lokal)
- **Detail**: Lihat [`earesmes.md`](earesmes.md)

### Arfin / AIRO Finance
- **Peran**: Finance automation interface
- **Interface**: Telegram
- **Status**: Aktif, sedang in development
- **Backend**: Google Apps Script + Google Sheets + Cloudflare Worker
- **Catatan**: "Arfin" adalah nama persona Telegram-nya; "AIRO Finance" adalah nama sistem/project-nya

### Remin
- **Peran**: Reminder system
- **Interface**: Telegram (planned)
- **Status**: Planned — belum dibangun
- **Dependency**: Menunggu Earesmes cukup mature untuk di-orchestrate

### Bubu
- **Peran**: Note-keeping
- **Interface**: Telegram (planned)
- **Status**: Planned — belum dibangun
- **Dependency**: Menunggu Earesmes cukup mature untuk di-orchestrate

## Model Relasi Antar Agent

### Saat Ini: Opsi 3

```
Egit
 ├── Earesmes (tahu workers ada, belum route ke mereka)
 ├── Arfin (direct, independent)
 ├── Remin (planned)
 └── Bubu (planned)
```

Earesmes aware bahwa Arfin, Remin, Bubu ada — tapi setiap agent masih diakses langsung oleh Egit. Tidak ada routing aktif dari Earesmes ke workers.

### Target: Opsi 4+ (Active Orchestration)

```
Egit
 └── Earesmes (active orchestrator)
      ├── Arfin
      ├── Remin
      └── Bubu
```

Egit hanya perlu ngobrol dengan Earesmes. Earesmes yang mendelegasikan ke worker yang tepat. **Transisi ini di-defer sampai semua workers cukup mature dan reliable.**

## Prinsip "Slot Not Stub"

Untuk workers yang belum dibangun (Remin, Bubu): **reserve slot, jangan build stub**. Artinya dokumentasikan bahwa slot itu ada dan akan diisi, tapi jangan build dummy implementation yang bisa menyebabkan false positives atau confusion.
