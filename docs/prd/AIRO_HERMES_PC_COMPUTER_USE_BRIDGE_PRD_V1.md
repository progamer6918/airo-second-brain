# PRD: AIRO Hermes — Autonomous PC Computer Use & Desktop Control Bridge V1

- **Document ID:** `PRD-AIRO-HERMES-COMPUTER-USE-V1`
- **Status:** `OWNER_APPROVED_SPEC_TARGET`
- **Owner / Champion:** Egit Aristorandas
- **Author:** Antigravity (Executor Layer) & AIRO Hermes
- **Date:** 2026-09-26
- **Architecture Baseline:** Hybrid OS-Command First + Native Win32 GUI Computer Use Actuator

---

## 1. Executive Summary & Vision

AIRO Hermes adalah co-thinker dan autonomous partner bagi Owner (Egit). Visi dari PRD ini adalah memberikan AIRO Hermes **kemampuan Computer Use penuh** pada PC Windows lokal milik Owner secara remote melalui obrolan natural di Telegram.

AIRO tidak lagi sekadar membuka video YouTube atau URL browser statis, melainkan memiliki kemampuan layaknya operator manusia yang duduk di depan komputer:
1. **Membuka dan mengendalikan software kerja desktop**: Microsoft PowerPoint, Excel, Word, VS Code, Spotify, Notepad, Calculator, File Explorer, Terminal.
2. **Melakukan aksi antarmuka (GUI Actuation)**: Menggerakkan kursor mouse, melakukan klik (left/right/double click), mengetikkan teks ke dalam dokumen/aplikasi, dan mengeksekusi tombol kombinasi keyboard (hotkeys seperti `Ctrl+S`, `Enter`, `Alt+F4`, `Win+D`).
3. **Mengendalikan sistem operasi & audio**: Pengaturan volume (mute/unmute/level), kunci layar (`LockWorkStation`), dan remote power management.
4. **Melihat tampilan layar (Screen Vision on Demand)**: Mengambil screenshot layar monitor secara instan dan mengirimkannya ke chat Telegram hanya saat diminta oleh Owner.

---

## 2. Core Architectural Pillars

```
+-------------------------------------------------------------+
|              OWNER TELEGRAM (Mobile / Remote)               |
+-------------------------------------------------------------+
                              |
                              v [Natural Language Chats]
+-------------------------------------------------------------+
|             AIRO HERMES RUNTIME (Tencent Cloud VPS)         |
|  - Native LLM Function Calling Engine (No brittle regex)    |
|  - Reasoning & Multi-step Plan Decomposition                |
|  - Tools: pc_launch_app, pc_click, pc_type, pc_hotkey,     |
|          pc_screenshot, pc_system_control, pc_open_url      |
+-------------------------------------------------------------+
                              |
                              v [Atomic JSON Packets via SSH Queue]
+-------------------------------------------------------------+
|             NATIVE WINDOWS RELAY (Local Windows 11 PC)      |
|  - Zero-dependency .NET / Win32 API Engine (PowerShell host)|
|  - Target WindowStation: WinSta0\Default (Physical Monitor) |
|  - Actuators:                                               |
|    * App Launcher (App Paths / Executable Resolver)         |
|    * Mouse Event Actuator (SetCursorPos, mouse_event)       |
|    * Keyboard Actuator (SendKeys, keybd_event)              |
|    * Screen Capture (System.Drawing.Graphics CopyFromScreen)|
|    * System Controller (Audio Endpoint Volume, User32 Lock) |
+-------------------------------------------------------------+
                              |
                              v [Instant Physical Desktop Execution]
+-------------------------------------------------------------+
|       PHYSICAL DESKTOP & MONITORS (Brave, Office, Apps)     |
+-------------------------------------------------------------+
```

---

## 3. Detailed Functional Requirements

### 3.1. Intelligence & Tool Calling Layer (VPS Hermes)
- **Eliminasi Regex Kaku**: Seluruh parsing perintah dipindahkan ke native LLM function calling / tools.
- Hermes mengenali maksud Owner secara kontekstual:
  - *"buka ppt di pc gw"* ➔ memanggil `pc_launch_app(app="powerpoint")`
  - *"buka ppt terus ketik judul Rencana Bisnis AIRO"* ➔ memanggil rangkaian aksi: `pc_launch_app(app="powerpoint")` ➔ jeda ➔ `pc_keyboard_type(text="Rencana Bisnis AIRO")`
  - *"buka youtube lofi girl"* ➔ memanggil `pc_open_url(url="https://youtube.com/...", browser="brave")`
  - *"coba screenshot layar PC gw"* ➔ memanggil `pc_take_screenshot(send_to_telegram=True)`
- **Safety Boundary**: Aksi destruktif (seperti menghapus file atau mematikan paksa aplikasi tanpa save) memerlukan konfirmasi eksplisit dari Owner.

### 3.2. Actuator Capabilities (Local Windows Engine)
1. **`open_app` (Software Launcher)**:
   - Resolusi path otomatis untuk:
     - Office: PowerPoint (`powerpnt.exe`), Excel (`excel.exe`), Word (`winword.exe`).
     - Productivity: VS Code (`Code.exe`), Notepad (`notepad.exe`), Calculator (`calc.exe`), Spotify (`Spotify.exe`), File Explorer (`explorer.exe`), Windows Terminal (`wt.exe`).
   - Eksekusi langsung ke desktop aktif (`WinSta0\Default`).
2. **`mouse_click` & `mouse_move` (Mouse Actuation)**:
   - Klik kiri, klik kanan, double click pada koordinat $(x, y)$ atau posisi kursor saat ini.
   - Menggunakan Win32 API: `SetCursorPos`, `mouse_event` (MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP).
3. **`keyboard_type` & `hotkey` (Keyboard Actuation)**:
   - Mengetik string teks natural ke dalam field input aktif menggunakan `[System.Windows.Forms.SendKeys]::SendWait`.
   - Mengirim kombinasi tombol pintas (e.g. `Ctrl+S` untuk save, `Enter`, `Tab`, `Esc`, `Win+D` untuk show desktop).
4. **`take_screenshot` (Visual Perception)**:
   - Mengambil tangkapan layar penuh menggunakan .NET `System.Drawing.Graphics.CopyFromScreen`.
   - Menyimpan gambar terkompresi di direktori staging lokal.
   - Mengirimkan gambar tersebut kembali ke Telegram bot via Telegram Bot API `sendPhoto`.
5. **`system_control` (OS Operations)**:
   - Mute / Unmute / Set Volume PC.
   - Mengunci komputer (`LockWorkStation`).

---

## 4. Non-Functional Requirements & Constraints

1. **Zero External Dependencies on Windows Host**:
   - Berjalan murni menggunakan PowerShell 5.1/7+ dan .NET Framework / Win32 API bawaan Windows 11.
   - Tidak memerlukan instalasi compiler, Python Windows terpisah, atau library pip pihak ketiga.
2. **Desktop Session Isolation Immunity**:
   - Seluruh proses peluncuran wajib secara eksplisit mengikat `lpDesktop = @"WinSta0\Default"` untuk menjamin jendela aplikasi selalu muncul di monitor fisik yang sedang dilihat Owner.
3. **Responsiveness & Latency**:
   - Waktu reaksi dari tombol 'Kirim' di Telegram hingga aksi fisik terjadi di monitor adalah **< 2.5 detik**.
   - Polling antrean VPS dilakukan setiap 1.0 - 1.5 detik dengan multiplexed SSH tunnel hemat resource.
4. **Resilience & Background Persistence**:
   - Relay Windows berjalan di latar belakang (hidden/minimized) tanpa memunculkan jendela console yang mengganggu pekerjaan Owner.
   - Otomatis melakukan reconnect bila koneksi internet terputus sementara.

---

## 5. Verification & Acceptance Criteria (Definition of Done)

- [x] **AC-1 (Browser & Media)**: Perintah memutar video/lagu YouTube di Telegram berhasil membuka tab Brave di monitor fisik dan otomatis berputar (*Validated*).
- [ ] **AC-2 (Desktop App Launch)**: Perintah *"buka ppt di pc"* membuka Microsoft PowerPoint asli di layar PC dalam < 3 detik.
- [ ] **AC-3 (Typing & Hotkeys)**: Perintah mengetik teks dan menekan tombol (e.g. ngetik di Notepad / PPT) tereksekusi akurat di jendela aktif.
- [ ] **AC-4 (Screenshot on Demand)**: Perintah *"coba kirim screenshot PC"* menghasilkan foto layar monitor terkini yang dikirim langsung ke chat Telegram Owner.
- [ ] **AC-5 (LLM Tool Calling Resilience)**: Hermes di VPS membedakan antara YouTube video vs Aplikasi desktop tanpa ada insiden salah tafsir regex.
