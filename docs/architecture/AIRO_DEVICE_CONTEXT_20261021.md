# AIRO — Konteks Perangkat Eksekusi (21 Oktober 2026)

**Jenis:** catatan fakta operasional lintas sesi, **bukan** device registry baru, kebijakan keamanan baru, atau instruksi otomatis untuk menyalakan/memigrasikan perangkat.  
**Sumber otoritas arsitektur:** [AIRO Multi-Device Access ADR V1](./AIRO_MULTI_DEVICE_ACCESS_ARCHITECTURE_DECISION_RECORD_V1.md).  
**Tanggal snapshot:** 2026-10-21 WIB. Status koneksi bersifat *point-in-time*, bukan jaminan sedang online.

> **PENTING UNTUK CHATGPT, CODEX, HERMES, DAN AGY:** **laptop lama pribadi Owner dan laptop Nurul adalah DUA perangkat berbeda**, meskipun sama-sama memakai Linux Mint / Xfce. Jangan menggabungkan identitas, RAM, alamat host, remote route, browser session, atau status koneksinya. Jangan menyuruh Owner menginstal Linux Mint atau mengulang onboarding sebelum membaca catatan ini dan bukti private terkait.

## Perbandingan yang telah dibuktikan

| Atribut | Laptop lama pribadi Owner | Laptop Nurul |
|---|---|---|
| Identitas konseptual | **OWNER_OLD_MINT / Toshiba Satellite C40-A** | **NURUL_MINT / laptop-nurul** |
| Kepemilikan / peran | Laptop pribadi Owner; **calon** pengganti eksekutor browser EARNSART | Perangkat terpisah; eksekutor browser sekunder historis, pertahankan sebagai cadangan |
| OS | Linux Mint **22.3**, kernel 6.14.0-37-generic (pembacaan AGY 21 Okt) | Linux Mint **22.3**, Xfce/X11 (audit historis Codex 21 Okt) |
| Desktop | Xfce 4, Xorg display :0, 1366×768 (pembacaan 21 Okt) | Xfce / X11, desktop relay historis |
| RAM total | **5.7 GiB**; tersedia **3.4 GiB** pada snapshot (21 Okt) | **~1.82 GiB**; MemAvailable **~829 MiB** saat audit 12 Okt |
| Browser | **Brave Flatpak** aktif; Firefox terinstal (21 Okt) | Brave pernah aktif; sesi sosial *tidak* diasumsikan masih login |
| Koneksi yang TERBUKTI | **AGY pada Windows PC utama → laptop lama via direct SSH: PASS**; target hostname dibaca ulang dan cocok (21 Okt) | **VPS ↔ Nurul outbound bridge: PASS** pada audit 12 Okt; satu operasi GUI membuat *draft Facebook* sukses pada 12 Okt |
| Koneksi/aksi yang BELUM TERBUKTI | GUI control via AGY; operasi sosial; **VPS/Hermes → laptop lama**; binding alias historis `laptop-lama` ke device ini; operasi 24/7 | Status online *sekarang*; login sosial terbaru; Hermes otonom penuh; jam layanan 24/7 |
| Daemon/tool yang dilaporkan | Ada listener AIRO historis dan agen vision lokal serta utilitas GUI; **keberadaan proses bukan bukti koneksi VPS atau kemampuan GUI** | Per-device desktop/admin relay dan antrean pernah dibuktikan; *heartbeat* dilaporkan kedaluwarsa pada preflight 21 Okt |
| Batasan yang diketahui | Tidak ada remote GUI network listener yang terdeteksi saat pembacaan; jangan mengasumsikan akses desktop via RDP/VNC | Owner sebelumnya menyatakan pemakaian **malam hari**; jangan perlakukan sebagai perangkat online 24/7 |

**Interpretasi:** laptop lama punya **~3,1× RAM fisik Nurul** menurut dua audit tersebut. Ini hanya perbandingan kapasitas, **bukan** bukti performa keseluruhan atau suksesnya migrasi.

## Identitas dan keamanan — ruang publik vs private

ASB ini **PUBLIC**. Untuk menjaga pemisahan sumber data:
- **JANGAN** menyalin IP lokal/global, hostname pribadi lengkap, username SSH, fingerprint/key, private key path, token, sesi/browser cookies, isi screenshot, atau rincian target koneksi ke file ASB publik.
- Nama/peran perangkat dan hardware kelas umum saja yang ditulis di sini. **Hostname lengkap laptop lama dan hasil pemeriksaan SSH** disimpan di laporan **PRIVATE**: [Issue #10 — AGY connect result](https://github.com/progamer6918/airo-dev-bridge/issues/10#issuecomment-6317486853). Catatan hostname Owner terpisah: [Issue #10 — Owner host readback](https://github.com/progamer6918/airo-dev-bridge/issues/10#issuecomment-6317143167).
- Jangan menganggap alias historis router `laptop-lama` otomatis mengarah ke laptop lama Owner. Preflight menemukannya tetapi **belum memvalidasi binding ke identitas**: [Issue #10 — device preflight](https://github.com/progamer6918/airo-dev-bridge/issues/10#issuecomment-6316901686).
- Ada **12 job legacy** berstatus in-progress pada route historis `laptop-lama` ketika preflight. Jangan replay, relabel, atau transfer diam-diam ke perangkat baru.
- Perangkat lain bernama `laptop-nurul` mempunyai trust/credential/queue sendiri. **Jangan salin SSH key, browser profile, atau auth session Nurul ke laptop lama**.

## Topologi/keputusan eksekusi terkini (bukan jaminan deployment)

1. **Owner + canonical ASB governance** menentukan arah; **VPS/Hermes** tetap titik koordinasi/worker yang sudah ada, bukan pemilik identitas AIRO.
2. **AGY Windows native pada PC utama** telah memverifikasi satu SSH read-only ke laptop lama (21 Okt). **Tidak memakai WSL**; ini tidak membatalkan pembekuan jalur AGY sebagai *parallel reviewer* untuk pilot COO Oktober yang spesifik.
3. **Laptop lama** adalah target migrasi yang lebih lapang RAM-nya, tetapi **belum dialihkan** menjadi endpoint yang terverifikasi bagi VPS/Hermes. SSH dari LAN Windows ≠ kendali GUI ≠ koneksi remote VPS ≠ otomasi bisnis.
4. **Nurul** tetap ada sebagai perangkat terpisah. Bridge outbound dan satu draft tersimpan merupakan **bukti historis**, bukan bukti ketersediaan saat ini. Jam malam saja sesuai batasan Owner sebelumnya kecuali Owner memperbarui keputusan.
5. **Tidak ada** setup ulang, instalasi, service restart, perubahan konfigurasi/keys, transfer sesi sosial, atau cutover yang dilakukan oleh pencatatan ini.

## Bukti sumber (PRIVATE, akses hanya jika diizinkan)

- [#10: AGY direct SSH verified to Owner old laptop, 21 Okt 2026](https://github.com/progamer6918/airo-dev-bridge/issues/10#issuecomment-6317486853) — sumber utama hardware/perangkat lama.
- [#10: Codex VPS read-only migration preflight, 21 Okt 2026](https://github.com/progamer6918/airo-dev-bridge/issues/10#issuecomment-6316901686) — identitas route legacy dan pembeda Nurul.
- [#10: Nurul read-only browser/bridge feasibility, 12 Okt 2026](https://github.com/progamer6918/airo-dev-bridge/issues/10#issuecomment-6123259717) — snapshot RAM dan bridge.
- [#10: Nurul Facebook draft saved, 12 Okt 2026](https://github.com/progamer6918/airo-dev-bridge/issues/10#issuecomment-6123637098) — bukti browser GUI historis dan batasannya.
- [#10: Owner night-only Nurul decision](https://github.com/progamer6918/airo-dev-bridge/issues/10#issuecomment-6123191753) — batasan jam kerja historis.
- [#10: Owner canceled AGY parallel COO pilot lane](https://github.com/progamer6918/airo-dev-bridge/issues/10#issuecomment-6192809263) — pembatalan lane **khusus** pilot COO, bukan berarti semua akses AGY-PC historis dihapus.

## Panduan untuk sesi berikutnya

**Sebelum bertanya OS, meminta instal ulang, atau menyuruh test hostname lagi:**
1. Baca file ini serta status terbaru dari Issue #10 yang relevan.
2. Sebut perangkat dengan nama **OWNER_OLD_MINT** atau **NURUL_MINT**, bukan sekadar “laptop Linux Mint”.
3. Bedakan **VERIFIED SSH**, **VERIFIED GUI**, **HISTORICAL PASS**, **UNKNOWN saat ini**, dan **NOT_DEPLOYED** dengan jelas.
4. Untuk migrasi berikutnya, uji satu operasi aman dan terotorisasi yang membuktikan GUI/status, serta jalur VPS↔laptop lama bila dibutuhkan. Mintakan approval sesuai cakupan. Pertahankan Nurul dan jangan lanjutkan antrean lama.
5. Jangan membuat *device registry* baru untuk hal ini; ADR V1 secara eksplisit menunda registry perangkat formal.

**Status akhir snapshot 21 Okt 2026:** `OWNER_OLD_MINT_DIRECT_SSH=PASS`; `OWNER_OLD_MINT_GUI=NOT_VERIFIED`; `OWNER_OLD_MINT_VPS_BRIDGE=NOT_VERIFIED`; `NURUL_VPS_BRIDGE=HISTORICAL_PASS`; `MIGRATION_CUTOVER=NOT_DONE`.
