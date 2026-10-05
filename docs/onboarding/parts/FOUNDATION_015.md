* **Purpose:** Memilah-milah berkas mentah dan inbox, serta membersihkan workspace untuk mencegah penumpukan sampah data.
* **Allowed writes:**
  * `events/synced/`
  * `events/failed/`
  * `inbox/`
  * `distill/`
  * `archive/`
  * `projects/_index.md`
  * `logs/`
* **Forbidden writes:**
  * Mengubah dokumen kanonikal tanpa persetujuan (approval).
  * Menghapus log mentah secara permanen sebelum masa retensinya habis.
* **Required flags:** `--help`, `--dry-run`
* **Expected output:** Pemindahan berkas dari folder `inbox/` dan `events/raw/` ke folder lifecycle yang sesuai.
* **Exit codes:** `0` (Success), `1` (Organize warnings), `2` (Fatal execution failure)
* **Validation:**
  ```bash
  scripts/airo-organize --dry-run
  ```

---

## 7. `scripts/airo-distill`
* **Purpose:** Menyaring data operasional kasar (raw/inbox) menjadi metadata terstruktur (deterministic) atau draf proposal pengetahuan (semantic-proposal).
* **Allowed writes:**
  * Deterministic mode: `registry/repos.yaml`, `state/system-health.md`, `projects/_index.md`
  * Semantic-proposal mode: `distill/proposals/`
* **Forbidden writes:**
  * Menimpa langsung berkas kanonikal utama seperti `CURRENT.md` atau `decisions/decision-log.md`.
* **Required flags:** `--help`, `--mode <deterministic|semantic-proposal>`, `--project <name>`, `--dry-run`
* **Expected output:** Berkas proposal berformat Markdown di folder `distill/proposals/` untuk ditinjau oleh Owner.
* **Exit codes:** `0` (Success), `1` (Distill empty), `2` (Distill syntax error)
* **Validation:**
  ```bash
  scripts/airo-distill --mode deterministic --dry-run
  scripts/airo-distill --mode semantic-proposal --project airo-finance --dry-run
  ```

---

## 8. `scripts/airo-promote`
* **Purpose:** Mempromosikan proposal yang telah disetujui Owner menjadi dokumen kanonikal resmi di Second Brain.
* **Allowed writes:**
  * Dokumen kanonikal: `CURRENT.md`, `projects/*.md`, `decisions/*.md`, dll.
  * Folder accepted/rejected proposal: `distill/accepted/`, `distill/rejected/`
* **Forbidden writes:**
  * Earesmes dilarang keras melakukan promote atas proposal semantik secara mandiri.
* **Required flags:** `--help`, `--proposal <file>`, `--target <file>`, `--dry-run`
* **Expected output:** Pembaruan file target kanonikal dengan menyisipkan tanda tangan/metadata pelaku promote (`promoted_by`, `awaiting_owner_review`).
* **Exit codes:** `0` (Success), `2` (Unauthorized promoter / Validation fail)
* **Validation:**
  ```bash
  scripts/airo-promote --proposal <file> --target <file> --dry-run
  ```

---

## 9. `scripts/airo-health`
* **Purpose:** Memindai kondisi kesehatan sistem dan menuliskan status tersebut ke berkas system-health.md.
* **Allowed writes:**
  * `state/system-health.md`
* **Forbidden writes:**
  * Penulisan logs sensitif yang mengekspos isi file credentials.
* **Required flags:** `--help`, `--json`
* **Expected output:** Berkas status kesehatan `state/system-health.md` berisi detail timestamp, key status `safe_to_work`, parity repositori, serta error summary.
* **Exit codes:** `0` (Healthy), `1` (Degraded), `2` (Blocked)
* **Validation:**
  ```bash
  scripts/airo-health --json
  ```

---

## 10. `scripts/airo-run-and-copy`
* **Purpose:** Menjalankan perintah (commands) di terminal, merekam output-nya ke folder `/tmp`, dan menyalin output yang aman secara otomatis ke Windows clipboard via `clip.exe` di WSL.
* **Allowed writes:**
  * `/tmp/airo_<task-name>_<timestamp>.txt`
* **Forbidden writes:**
  * Mengubah repository git secara langsung selain efek dari command yang di-run.
* **Required arguments:** `scripts/airo-run-and-copy <task-name> -- <command...>`
* **Expected output:** File output disimpan di `/tmp`, dicetak di console (tee), dan data disalin ke clipboard. Cetak `COPIED_TO_CLIPBOARD=<path>` atau `CLIPBOARD_COPY=SKIPPED`.
* **Exit codes:** Mengikuti exit code asli dari command yang dijalankan, atau `2` jika kegagalan argumen.
* **Validation:**
  ```bash
  scripts/airo-run-and-copy test_echo -- echo "hello"
  ```

---

## 11. `scripts/airo-manual-queue-status`
* **Purpose:** Memeriksa status `inbox/manual-sync-queue.md` secara lokal dan membandingkannya dengan `origin/main`.
* **Allowed writes:** Hanya mencetak laporan status ke stdout (read-only).
* **Forbidden writes:** Mengubah file markdown atau repositori.
* **Required flags:** `--help`
* **Expected output:** Laporan status lengkap manual queue.
* **Exit codes:** `0` (Success), `2` (Fatal error)
* **Validation:**
  ```bash
  scripts/airo-manual-queue-status
  ```

---

## 12. `scripts/airo-manual-queue-list`
* **Purpose:** Mengurai seluruh blok capture di `inbox/manual-sync-queue.md` dan mencetak daftar metadata capture dalam format JSON.
* **Allowed writes:** Hanya membaca file antrean (read-only).
* **Exit codes:** `0` (Success), `2` (Fatal error)

---

## 13. `scripts/airo-manual-queue-summarize`
* **Purpose:** Menghasilkan ringkasan singkat yang ramah bagi owner untuk capture ID tertentu.
* **Allowed writes:** Read-only.
* **Exit codes:** `0` (Success)

---

## 14. `scripts/airo-manual-queue-process`
* **Purpose:** Memproses capture dalam antrean manual (detail, ringkas, canonicalize, defer, archive).
* **Allowed writes:** `inbox/manual-sync-queue.md` (pembaruan status/canonical flag).
* **Exit codes:** `0` (Success), `2` (Error/Not approved)

---

## 15. `scripts/airo-manual-queue-compact`
* **Purpose:** Melakukan pemadatan (compaction) pada antrean aktif, mengarsipkan item yang sukses diproses, memindahkan item yang ditunda, dan menulis ulang indeks arsip.
* **Allowed writes:**
  * `inbox/manual-sync-queue.md`
  * `archive/manual-sync-queue/`
  * `inbox/deferred/`
* **Exit codes:** `0` (Success)

---

## 16. `ops/telegram/telegram-action-poller.sh`
* **Purpose:** Menarik callback query Telegram terbaru dari API Telegram (getUpdates) dan menyimpan aksi milik owner yang terverifikasi ke `inbox/telegram-actions/`.
* **Allowed writes:** `inbox/telegram-actions/`
* **Exit codes:** `0` (Success/Skipped), `1` (API Error)

---

## 17. `ops/telegram/telegram-action-processor.sh`
* **Purpose:** Membaca file aksi JSON pending di `inbox/telegram-actions/`, menjalankan perintah/script yang sesuai, memperbarui status aksi, dan mengirim pesan konfirmasi ke Telegram.
* **Allowed writes:**
  * `inbox/telegram-actions/`
  * File-file yang diubah oleh script pemroses terkait.
* **Exit codes:** `0` (Success)

---

## 18. `scripts/airo-session-projection-sync`
* **Purpose:** Mensinkronisasikan status sesi aktif dari runtime state (`bin/airo-session`) ke berkas proyeksi Markdown (`state/active-session.md`) untuk display Obsidian.
* **Allowed writes:**
  * `state/active-session.md` (lokal repo dan vault kanonikal `/mnt/c/Users/Admin/AI_WORKSPACES/airo-second-brain`)
* **Forbidden writes:**
  * Dilarang memodifikasi runtime state JSON secara langsung (wewenang eksklusif `bin/airo-session`).
  * Dilarang melakukan git commit atau git push otomatis.
* **Required subcommands:** `update`, `reset`, `status`
* **Expected output:** Kartu Markdown aktif (🟢) dengan metadata sesi lengkap saat sesi aktif, atau kartu idle kanonikal (⚪) saat sesi ditutup.
* **Exit codes:** `0` (Success), `1` (Filesystem warning / Degraded)
* **Contract:** `docs/contracts/AIRO_SESSION_PROJECTION_SYNC_CONTRACT.md`
* **Validation:**
  ```bash
  python3 scripts/airo-session-projection-sync status
  ```


<!-- SOURCE_END docs/contracts/AIRO_SECOND_BRAIN_SCRIPT_CONTRACTS.md -->
