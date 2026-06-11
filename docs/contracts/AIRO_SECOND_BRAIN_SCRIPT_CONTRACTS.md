# AIRO Second Brain Script Contracts

Dokumen ini berisi spesifikasi formal dan kontrak eksekusi untuk 9 script utama dalam sistem tata kelola AIRO Second Brain v0.4.1.

## Ketentuan Umum Script (Shared Contract)
Setiap script di bawah folder `scripts/` wajib memenuhi ketentuan berikut:
1. **Required Flags:** Wajib mendukung flag `--help`, `--dry-run`, dan `--json`.
2. **Logging:** Wajib mencatat riwayat eksekusi ke dalam folder `logs/`.
3. **Exit Codes:**
   * `0` = Success (Sukses tanpa masalah)
   * `1` = Warning/Degraded (Sistem berjalan dalam kondisi terbatas)
   * `2` = Blocked/Failure (Terjadi error fatal atau pelanggaran kebijakan keamanan)
4. **Safety:** Dilarang mencetak kunci rahasia (secrets) atau credentials ke console output atau file logs.

---

## 1. `scripts/airo-inventory`
* **Purpose:** Memindai folder/direktori WSL yang ada dan memperbarui registry repositori secara dinamis.
* **Allowed writes:**
  * `registry/repos.yaml`
  * `inbox/workspace-scans/`
  * `logs/`
  * `state/system-health.md`
* **Forbidden writes:**
  * File kode sumber project di repository governed lainnya.
  * Ringkasan dokumen kanonikal (kecuali proposal metadata baru).
* **Required flags:** `--help`, `--dry-run`, `--json`
* **Expected output:** Berkas registry repositori yang telah terisi dan terformat dengan benar dalam YAML.
* **Exit codes:** `0` (Success), `1` (Scan warning), `2` (Fatal disk error)
* **Validation:**
  ```bash
  scripts/airo-inventory --dry-run
  scripts/airo-inventory --json
  ```

---

## 2. `scripts/airo-bootstrap`
* **Purpose:** Menyediakan gerbang/titik awal sesi yang standar untuk semua AI consumer.
* **Allowed writes:**
  * `logs/`
  * `state/active-sessions.md`
  * `state/system-health.md`
  * `events/raw/`
* **Forbidden writes:**
  * Dokumen kanonikal semantik secara langsung tanpa melalui distill/promote.
* **Required flags:** `--help`, `--project <name>`, `--dry-run`, `--json`
* **Expected output:**
  * Ringkasan pembacaan `BOOT.md`, `CURRENT.md`
  * Informasi status kesehatan sistem saat ini (`state/system-health.md`)
  * Hasil check preflight (`truth_status` dan `safe_to_work`)
* **Exit codes:** `0` (Success), `1` (Degraded status), `2` (Blocked/Preflight failed)
* **Validation:**
  ```bash
  scripts/airo-bootstrap --project airo-finance
  ```

---

## 3. `scripts/airo-preflight`
* **Purpose:** Membandingkan memori registry di Second Brain dengan status repositori riil saat ini (Git HEAD, dirty check).
* **Allowed writes:**
  * `registry/repos.yaml`
  * `state/system-health.md`
  * `logs/`
  * `events/raw/`
* **Forbidden writes:**
  * File kode sumber project utama maupun Second Brain.
* **Required flags:** `--help`, `--project <name>`, `--json`
* **Expected output:** Struktur JSON/YAML yang melaporkan `project_id`, `repo_path`, `repo_head`, `last_known_commit`, `git_dirty`, `truth_status`, `safe_to_execute`, dan `required_action`.
* **Exit codes:** `0` (Current/Parity OK), `1` (Dirty/Stale detected), `2` (Conflict/Unreachable)
* **Validation:**
  ```bash
  scripts/airo-preflight --project airo-finance --json
  ```

---

## 4. `scripts/airo-capture`
* **Purpose:** Mencatat aktivitas operasional harian yang aman ke dalam log lokal.
* **Allowed writes:**
  * `events/raw/`
  * `logs/`
* **Forbidden writes:**
  * Dilarang melakukan sinkronisasi Git, distill, organize, atau promote.
* **Required flags:** `--help`, `--event <type>`, `--summary <message>`, `--project <name>`, `--json`
* **Expected output:** Satu baris data event berformat NDJSON (Newline Delimited JSON) yang aman dari informasi rahasia.
* **Exit codes:** `0` (Success), `2` (Write failure / Invalid event schema)
* **Validation:**
  ```bash
  scripts/airo-capture --event checkpoint --summary "test event" --project airo-second-brain
  ```

---

## 5. `scripts/airo-sync`
* **Purpose:** Melakukan commit dan push otomatis yang aman dari folder brain-safe ke repositori GitHub.
* **Allowed writes:**
  * `logs/sync/`
  * `logs/sync-errors/`
  * `state/system-health.md`
  * `registry/repos.yaml`
* **Forbidden writes:**
  * Dilarang keras melakukan commit atau push pada file berkode sumber proyek utama tanpa review yang tepat.
* **Required flags:** `--help`, `--dry-run`, `--json`
* **Expected output:** Penguncian berkas sync, penyaringan berkas sensitif lewat Secret Guard, dan proses git push yang aman.
* **Exit codes:** `0` (Success), `1` (Sync degraded), `2` (Secret guard hit / Git conflict)
* **Validation:**
  ```bash
  scripts/airo-sync --dry-run
  scripts/airo-sync --json
  ```

---

## 6. `scripts/airo-organize`
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
