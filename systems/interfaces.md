# Interfaces — Cara Egit Berinteraksi dengan AIRO

## Primary Interface: Telegram

**Telegram adalah satu-satunya primary daily interface** untuk semua agent di ekosistem AIRO.

Kenapa Telegram:
- Mobile-first, selalu tersedia
- Bot API yang mature dan reliable
- Bisa handle text, file, command, inline buttons
- Satu tempat untuk semua agent (Earesmes, Arfin, dll. masing-masing punya bot/persona sendiri)

**Pattern penggunaan**:
- Daily interaction dengan Earesmes → via Telegram
- Finance commands ke Arfin → via Telegram
- Semua notifikasi dan output dari sistem → via Telegram

## Secondary Interface: WSL Terminal

Digunakan **hanya** untuk setup, debugging, dan maintenance sistem — bukan untuk daily use.

Akses: Windows Terminal → WSL2 Ubuntu

## Interface per Agent

| Agent | Interface | Keterangan |
|-------|-----------|------------|
| Earesmes | Telegram bot | Primary asisten, daily use |
| Arfin / AIRO Finance | Telegram bot | Finance commands & queries |
| Claude.ai | Web/mobile | Brainstorming, arsitektur, drafting |
| ChatGPT | Web/mobile | Eksekusi, second opinion |

## Owner-Facing vs Technical Layer

Semua output yang Egit lihat sehari-hari (via Telegram) ditulis dalam **Bahasa Indonesia**.
Semua dokumentasi teknis, PRD, dan konfigurasi sistem ditulis dalam **English**.
