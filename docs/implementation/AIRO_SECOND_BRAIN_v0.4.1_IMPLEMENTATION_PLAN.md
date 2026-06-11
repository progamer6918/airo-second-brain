# AIRO Second Brain v0.4.1 Implementation Plan

## Overview
Rencana implementasi ini dirancang untuk mewujudkan governance layer lokal untuk workspace AIRO sesuai dengan AIRO Second Brain PRD v0.4.1.

## Phase Execution

### Phase 0: Canonicalize PRD
* **Goal:** Mendokumentasikan PRD v0.4.1 dan rencana eksekusi resmi ke dalam repository.
* **Required files:**
  * `docs/AIRO_SECOND_BRAIN_PRD_v0.4.1_NO_BRAINER.md`
  * `docs/implementation/AIRO_SECOND_BRAIN_v0.4.1_IMPLEMENTATION_PLAN.md`
  * `docs/contracts/AIRO_SECOND_BRAIN_SCRIPT_CONTRACTS.md`
  * `docs/validation/AIRO_SECOND_BRAIN_v0.4.1_VALIDATION_CHECKLIST.md`
  * `docs/handoff/ANTIGRAVITY_AIRO_SECOND_BRAIN_v0.4.1_EXECUTION_PROMPT.md`
* **Forbidden actions:**
  * Jangan menulis file project di luar folder `docs/` (kecuali patch minimal ke `meta/changelog.md`, `state/active-context.md`, dan `CURRENT.md`).
  * Jangan membuat program atau script di phase ini.
* **Validation commands:**
  ```bash
  test -f docs/AIRO_SECOND_BRAIN_PRD_v0.4.1_NO_BRAINER.md
  test -f docs/implementation/AIRO_SECOND_BRAIN_v0.4.1_IMPLEMENTATION_PLAN.md
  test -f docs/contracts/AIRO_SECOND_BRAIN_SCRIPT_CONTRACTS.md
  test -f docs/validation/AIRO_SECOND_BRAIN_v0.4.1_VALIDATION_CHECKLIST.md
  test -f docs/handoff/ANTIGRAVITY_AIRO_SECOND_BRAIN_v0.4.1_EXECUTION_PROMPT.md
  git status --short
  ```
* **PASS criteria:**
  * Semua 5 file dokumentasi di atas telah berhasil dibuat di folder target.
  * Dokumen PRD v0.4.1 No-Brainer Execution Edition tersimpan lengkap dan valid.
  * Tidak ada perubahan yang tidak disetujui di file lain.
* **Commit message:** `docs: canonicalize AIRO Second Brain PRD v0.4.1`

---

### Phase 1: Registry & Inventory
* **Goal:** Menghasilkan inventory registry yang mengenali semua repositori dan workspace WSL, serta mendefinisikan manifest untuk repo project utama.
* **Required files:**
  * `registry/repos.yaml`
  * `registry/sync-policy.yaml`
  * `registry/capture-policy.yaml`
  * `registry/consumer-policy.yaml`
  * `scripts/airo-inventory`
  * `inbox/workspace-scans/`
  * `logs/`
  * `/home/egitaristorandas/vortex-ai-skill-lab/AIRO_MANIFEST.md` (di repo project)
* **Forbidden actions:**
  * Jangan memodifikasi kode sumber project selain menambahkan manifest file.
  * Jangan melakukan deep-scanning pada repositori bertipe `UNKNOWN`.
* **Validation commands:**
  ```bash
  scripts/airo-inventory --dry-run
  scripts/airo-inventory --json
  python3 -c "import yaml, pathlib; p=pathlib.Path('registry/repos.yaml'); assert p.exists(); data=yaml.safe_load(p.read_text()); assert data; print('PASS registry yaml')"
  ```
* **PASS criteria:**
  * Repository `airo-second-brain` terdaftar sebagai `GOVERNED-BRAIN`.
  * Repository `vortex-ai-skill-lab` terdaftar sebagai `GOVERNED-GUARDED`.
  * Manifest file `AIRO_MANIFEST.md` ada di repo project utama.
* **Commit message:** `feat(airo-brain): add registry and inventory foundation`

---

### Phase 2: Capture & Health
* **Goal:** Memastikan event capture lokal berjalan lancar dan status kesehatan sistem (system health) selalu terbarui.
* **Required files:**
  * `scripts/airo-capture`
  * `scripts/airo-health`
  * `events/raw/`
  * `state/system-health.md`
  * `logs/errors/`
* **Forbidden actions:**
  * Jangan melakukan push ke GitHub atau sinkronisasi git di fase ini.
  * Jangan melakukan distill atau promotion proposal otomatis.
* **Validation commands:**
  ```bash
  scripts/airo-capture --event checkpoint --summary "phase 2 validation" --project airo-second-brain
  scripts/airo-health --json
  test -f state/system-health.md
  find events/raw -type f | head
  ```
* **PASS criteria:**
  * `airo-capture` berhasil menulis file event berformat NDJSON.
  * `airo-health` sukses memperbarui file `state/system-health.md` dengan skema yang benar.
* **Commit message:** `feat(airo-brain): add capture and health reporting`

---

### Phase 3: Sync & Preflight
* **Goal:** Menerapkan otomatisasi sinkronisasi git yang aman (dilengkapi locking dan secret guard) dan preflight check untuk mendeteksi perubahan.
* **Required files:**
  * `scripts/airo-sync`
  * `scripts/airo-preflight`
  * `logs/sync/`
  * `logs/sync-errors/`
  * `locks/`
  * (Optional) `systemd/airo-sync.service` & `systemd/airo-sync.timer`
* **Forbidden actions:**
  * Jangan melakukan commit paksa (`force push`) saat mendeteksi conflict.
  * Jangan melakukan commit jika terdeteksi secret/kunci rahasia (Secret Guard hit).
* **Validation commands:**
  ```bash
  scripts/airo-preflight --project airo-finance --json
  scripts/airo-sync --dry-run --json
  test ! -f locks/airo-sync.lock || echo "lock exists"
  ```
* **PASS criteria:**
  * Preflight check dapat mendeteksi parity status repo target dengan benar.
  * Sync engine melakukan validasi secret guard secara penuh sebelum melakukan commit/push.
  * Lock file berhasil mencegah sinkronisasi ganda.
* **Commit message:** `feat(airo-brain): add sync and preflight automation`

---

### Phase 4: Bootstrap & Organize
* **Goal:** Menyatukan titik masuk seluruh AI consumer melalui bootstrap script, serta memelihara lifecycle folder melalui pengaturan otomatis.
* **Required files:**
  * `scripts/airo-bootstrap`
  * `scripts/airo-organize`
  * `events/synced/`
  * `events/failed/`
  * `distill/proposals/`
  * `archive/`
  * `state/active-sessions.md`
* **Forbidden actions:**
  * Jangan mempromosikan proposal semantik ke dokumen kanonikal secara otomatis tanpa gerbang approval.
  * Jangan menghapus event mentah tanpa aturan retensi yang sah.
* **Validation commands:**
  ```bash
  scripts/airo-bootstrap --project airo-finance
  scripts/airo-organize --dry-run
  ```
* **PASS criteria:**
  * Bootstrap berhasil menjalankan preflight secara otomatis dan memvalidasi `safe_to_work`.
  * Organize memindahkan file mentah/inbox yang tersinkronisasi ke folder arsip yang tepat tanpa memengaruhi file kanonikal.
* **Commit message:** `feat(airo-brain): add bootstrap and organization lifecycle`

---

### Phase 5: Distill & Promote
* **Goal:** Memproses file mentah/inbox menjadi proposal metadata objektif maupun proposal semantik, lalu mempromosikannya setelah diverifikasi.
* **Required files:**
  * `scripts/airo-distill`
  * `scripts/airo-promote`
  * `distill/proposals/`
  * `distill/accepted/`
  * `distill/rejected/`
  * `distill/superseded/`
* **Forbidden actions:**
  * Jangan menulis langsung ke file kanonikal (`CURRENT.md` dll) dari proses distillation tanpa promote gate.
  * Earesmes tidak boleh diizinkan memicu promote untuk proposal semantik.
* **Validation commands:**
  ```bash
  scripts/airo-distill --mode deterministic --dry-run
  scripts/airo-distill --mode semantic-proposal --project airo-finance --dry-run
  scripts/airo-promote --help
  ```
* **PASS criteria:**
  * Distill dapat mengelompokkan proposal dengan benar.
  * Promote mewajibkan bukti pendukung (`source_evidence`) dan mencatat identitas aktor eksekutor.
* **Commit message:** `feat(airo-brain): add distill and promote workflow`

---

### Phase 6: Stabilization & Abuse Testing
* **Goal:** Menguji ketahanan sistem dalam berbagai skenario kegagalan ekstrim untuk menjamin stabilitas.
* **Required files:**
  * Unit test dan simulasi mock test script.
* **Forbidden actions:**
  * Jangan mengabaikan sinyal bahaya (misal, registry rusak, git conflict) — sistem harus fail-fast dan berhenti otomatis.
* **Validation commands:**
  * Menjalankan rentetan skenario simulasi:
    1. Secret guard trigger test.
    2. Git conflict simulation.
    3. Dirty repository test.
    4. Push failure mock.
    5. Registry yaml corruption recovery.
* **PASS criteria:**
  * Sistem terbukti memblokir push jika mendeteksi secret.
  * Ketika ada conflict atau kegagalan parsing registry, sistem secara otomatis menghentikan sinkronisasi, memperbarui health status menjadi degraded/blocked, dan meminta intervensi manual.
* **Commit message:** `test(airo-brain): add v0.4.1 validation coverage`
