# PRD: AIRO Hermes — Autonomous Presentation Deck Generation Skill & Bridge V1

- **Document ID:** `PRD-AIRO-PRESENTATION-GENERATOR-SKILL-V1`
- **Status:** `PROPOSED_FOR_OWNER_REVIEW`
- **Owner / Champion:** Egit Aristorandas
- **Author:** Antigravity (Executor Layer) & AIRO Hermes
- **Date:** 2026-09-27
- **Architecture Baseline:** LLM Structured Presentation Spec + Open-Source Inspired PPTX Engine + Dual Delivery (PC Launch & Telegram Upload)

---

## 1. Executive Summary & Problem Analysis

### 1.1 Root Cause Analisis Kegagalan (27/09/2026 06:46 WIB)
Saat Owner mengirimkan prompt:
> *"coba buka ppt di pc gw, dan buat ppt yang menarik ttg diri lo untuk dapat di presentasi kan ke kons public yg bisa menarik org dan ingin beli lo"*

Airo hanya merespons:
> *"Siap bro! Aplikasi Microsoft PowerPoint lagi gue bukain di monitor PC lo sekarang. 🚀"*

**Fakta Diagnostik Runtime:**
1. **Relay PC Berhasil**: Aplikasi Microsoft PowerPoint (`POWERPNT.EXE`, PID 2872) benar-benar berhasil dibuka di monitor fisik PC Owner pada jam 06:46:05 WIB.
2. **Router Short-Circuit Bug**: `PCActionRouter` di VPS memiliki regex greedy yang mencocokkan kata `"buka"` + `"ppt"` + `"di pc"`, lalu langsung men-dispatch `open_app("powerpoint")` statis.
3. **Generative Intent Terpotong**: Akibat router memotong alur sebelum LLM Hermes sempat membaca pesan secara utuh, instruksi krusial: *"dan buat ppt yang menarik ttg diri lo..."* terbuang sia-sia.
4. **Ketiadaan Engine Generator PPT**: Sistem belum memiliki kapabilitas (*skill*) untuk menyusun slide deck terstruktur, meng-compile menjadi file `.pptx` berdesain menarik, dan membukanya di PowerPoint.

---

## 2. Core Architectural Pillars

```
+---------------------------------------------------------------------------------+
|                        OWNER TELEGRAM (Mobile / Remote)                         |
|   "buat ppt menarik ttg diri lo untuk presentasi publik agar org tertarik beli"  |
+---------------------------------------------------------------------------------+
                                       |
                                       v
+---------------------------------------------------------------------------------+
|                        INTENT ROUTER (Non-Greedy Bypass)                        |
|  - Deteksi Generative Intent (buat/bikin/generate/susun + ppt/slide/presentasi) |
|  - BYPASS open_app sederhana -> teruskan prompt ke Hermes Intelligence          |
+---------------------------------------------------------------------------------+
                                       |
                                       v
+---------------------------------------------------------------------------------+
|                   AIRO HERMES PRESENTATION DECK SKILL                           |
|  - Structured Pitch Copywriting (Problem, Solution, Superpowers, Value, CTA)    |
|  - Dynamic Theming Engine (16:9 Widescreen, Dark Tech AI Theme, Card Shapes)    |
|  - Inspired by Open-Source: pptx-generator / Slideforge / python-pptx           |
|  - Output: AIRO_Pitch_Deck.pptx                                                 |
+---------------------------------------------------------------------------------+
                                       |
                                       +------------------------------------------+
                                       |                                          |
                                       v                                          v
+-----------------------------------------------+ +-------------------------------+
|      PC ACTION BRIDGE (Local Windows PC)      | |   TELEGRAM DIRECT DELIVERY    |
| - Salin/Buat .pptx di C:\Users\Admin\Documents| | - Upload file dokumen .pptx   |
| - Eksekusi: POWERPNT.EXE "AIRO_Pitch_Deck.pptx"| | - Kirim ringkasan slide &     |
| - Layar monitor menampilkan slide deck siap   | |   executive overview ke chat  |
+-----------------------------------------------+ +-------------------------------+
```

---

## 3. Product Specifications & Features

### 3.1 Non-Greedy Semantic Router
Router tidak lagi memotong pesan secara naif jika mendeteksi kata-kata pembuatan konten:
- **Dilarang Short-Circuit jika mengandung**: `buat`, `bikin`, `generate`, `susun`, `tulis`, `rangkai`, `bikin slide`, `buat presentasi`.
- Prompt diteruskan ke Hermes LLM untuk perencanaan dan penulisan materi mendalam.

### 3.2 Dynamic Theming Engine
Sistem mendukung tema visual adaptif sesuai topik presentasi:
1. **Modern Tech Dark (Default untuk AI/Tech/AIRO)**:
   - Background: Dark Navy / Deep Space Slate (`#0B0F19`, `#111827`)
   - Accent Primary: Neon Cyan (`#00E5FF`)
   - Accent Secondary: Vibrant Violet / Purple (`#7C3AED`)
   - Text Hierarchy: Clean Off-White (`#F9FAFB`) & Muted Slate (`#9CA3AF`)
   - Container: Semi-transparent Card Shapes dengan rounded corners dan highlight borders.
2. **Corporate Clean Light (Untuk Finansial/Bisnis Tradisional)**:
   - Background: Crisp White (`#FFFFFF`) & Pearl Gray (`#F3F4F6`)
   - Accent: Corporate Royal Blue (`#1D4ED8`) & Forest Green (`#059669`)

### 3.3 Target First Deck: AIRO Executive Pitch Deck (7 Slides)
- **Slide 1 — Title / Vision**:
  - *Title*: **AIRO — Autonomous Executive Operating System**
  - *Subtitle*: The Next-Generation Autonomous AI Partner for High-Performance Operators & Founders
- **Slide 2 — The Industry Problem**:
  - *Title*: The Fragmentation & Context Crisis in Modern AI
  - *Points*: Traditional chatbots are trapped in browser tabs; lack physical OS interaction; reset memory every session; require endless manual prompts and babysitting.
- **Slide 3 — The Solution (Meet AIRO)**:
  - *Title*: Unifying Strategic Intelligence with Physical Desktop Execution
  - *Points*: Tri-layer Architecture (ChatGPT Strategic Reasoning + Antigravity Engineering + Hermes Runtime + Native Windows 11 Bridge).
- **Slide 4 — Core Superpowers**:
  - *Title*: Real-World Capabilities from Cloud to Desktop
  - *Points*: Autonomous WorkDesk query engine, direct financial capture, native Windows application control, keyboard/mouse actuation, vision on demand.
- **Slide 5 — Live Case Demonstrations**:
  - *Title*: Proven Tangible Execution, Not Hypothetical Chat
  - *Points*: Automated multi-device workflows, Excel data extraction, instant PowerPoint generation & display, physical desktop lockdown.
- **Slide 6 — The Unfair Value Proposition**:
  - *Title*: Why High-Performance Leaders Choose AIRO
  - *Points*: 10x Operational Speed, 100% Local Data Sovereignty, Permanent State Continuity, Zero Cognitive Fatigue.
- **Slide 7 — Call to Action**:
  - *Title*: Transform Your Executive Workflow Today
  - *Points*: Deploy AIRO into your ecosystem. Scale your mind, automate your operations.

### 3.4 Dual Delivery Protocol
1. **PC Display Actuation**:
   - File `.pptx` disimpan di `C:\Users\Admin\Documents\AIRO_Presentations\AIRO_Pitch_Deck.pptx`.
   - Relay PC meluncurkan: `POWERPNT.EXE "C:\Users\Admin\Documents\AIRO_Presentations\AIRO_Pitch_Deck.pptx"`.
   - Slide langsung tampil di monitor fisik Owner.
2. **Telegram Direct Delivery**:
   - Mengirim file `.pptx` via API Telegram `sendDocument` ke chat Owner.
   - Mengirimkan ringkasan 7 slide agar Owner dapat langsung membaca materi melalui smartphone.

---

## 4. Open-Source Adaptation Strategy

Mengacu pada riset repositori open-source (`pptx-generator`, `Slideforge`, `python-pptx`):
- Menggunakan arsitektur pemisahan: **LLM Copywriter (JSON Spec)** -> **Deterministic PPTX Compiler**.
- Menghindari ketergantungan berat atau server eksternal, cukup memanfaatkan library `python-pptx` di VPS / PC lokal atau script compiler mandiri yang portabel.

---

## 5. Acceptance Criteria

1. **Router Test**: Pesan *"coba buka ppt di pc gw, dan buat ppt yang menarik ttg diri lo..."* tidak lagi terpotong ke respons statis `open_app`.
2. **File Generation**: File `.pptx` valid berhasil dibuat dengan 7 slide, layout 16:9 widescreen, kontras teks tinggi, dan copy yang persuasif.
3. **PC Screen Display**: PowerPoint terbuka di layar monitor PC fisik Owner dan menampilkan slide deck yang baru saja dibuat.
4. **Telegram Delivery**: File dokumen `.pptx` dan ringkasan eksekutif terkirim ke Telegram Owner.
