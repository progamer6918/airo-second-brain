# Master Validation Checklist — AIRO Second Brain v0.4.1

Dokumen ini berisi checklist pengujian formal yang wajib dipenuhi seluruhnya (PASS) sebelum rilis v0.4.1 dianggap selesai secara sah.

## Checklist Tata Kelola Dokumen & File
* [ ] **PRD Canonical Markdown Exists:** File [docs/AIRO_SECOND_BRAIN_PRD_v0.4.1_NO_BRAINER.md](file:///home/egitaristorandas/AI_WORKSPACES/airo-second-brain/docs/AIRO_SECOND_BRAIN_PRD_v0.4.1_NO_BRAINER.md) telah dibuat dan berisi teks PRD v0.4.1 No-Brainer Edition secara utuh.
* [ ] **Implementation Plan Exists:** File [docs/implementation/AIRO_SECOND_BRAIN_v0.4.1_IMPLEMENTATION_PLAN.md](file:///home/egitaristorandas/AI_WORKSPACES/airo-second-brain/docs/implementation/AIRO_SECOND_BRAIN_v0.4.1_IMPLEMENTATION_PLAN.md) ada dan menjabarkan rincian gol, file wajib, dan perintah validasi tiap fase.
* [ ] **Script Contracts Exist:** File [docs/contracts/AIRO_SECOND_BRAIN_SCRIPT_CONTRACTS.md](file:///home/egitaristorandas/AI_WORKSPACES/airo-second-brain/docs/contracts/AIRO_SECOND_BRAIN_SCRIPT_CONTRACTS.md) mendefinisikan batas masukan, keluaran, exit codes, dan validasi untuk kesembilan modul script.
* [ ] **Validation Checklist Exists:** File [docs/validation/AIRO_SECOND_BRAIN_v0.4.1_VALIDATION_CHECKLIST.md](file:///home/egitaristorandas/AI_WORKSPACES/airo-second-brain/docs/validation/AIRO_SECOND_BRAIN_v0.4.1_VALIDATION_CHECKLIST.md) (dokumen ini) tersedia secara fisik di repository.
* [ ] **Antigravity Handoff Prompt Exists:** File [docs/handoff/ANTIGRAVITY_AIRO_SECOND_BRAIN_v0.4.1_EXECUTION_PROMPT.md](file:///home/egitaristorandas/AI_WORKSPACES/airo-second-brain/docs/handoff/ANTIGRAVITY_AIRO_SECOND_BRAIN_v0.4.1_EXECUTION_PROMPT.md) berisi instruksi eksekusi terstruktur untuk fase berikutnya.

## Checklist Registry & Tata Kelola Workspace
* [ ] **Registry Files Exist:** Folder `registry/` berisi file `repos.yaml`, `sync-policy.yaml`, `capture-policy.yaml`, dan `consumer-policy.yaml`.
* [ ] **Registry Validates:** File `registry/repos.yaml` lolos verifikasi sintaksis YAML dan memetakan repositori terdaftar dengan benar.
* [ ] **AIRO Second Brain Registered:** Status tata kelola repositori brain terdaftar dengan tier `GOVERNED-BRAIN`.
* [ ] **Vortex AI Skill Lab Registered:** Repositori project terdaftar dengan tier `GOVERNED-GUARDED`.
* [ ] **AIRO Manifest Exists:** File `AIRO_MANIFEST.md` tersedia di repositori project target (`vortex-ai-skill-lab`).

## Checklist Fungsionalitas Script & Modul
* [ ] **All 9 Scripts Exist:** Seluruh 9 modul script (airo-inventory, airo-bootstrap, airo-preflight, airo-capture, airo-sync, airo-organize, airo-distill, airo-promote, airo-health) telah dibuat di bawah folder `scripts/`.
* [ ] **Scripts Support --help:** Semua 9 script dapat dijalankan dengan flag `--help` tanpa menghasilkan error.
* [ ] **Scripts Support --dry-run:** Semua script yang memicu perubahan mendukung opsi `--dry-run` untuk simulasi aman.
* [ ] **Scripts Support --json:** Semua script keluaran data mendukung format `--json`.
* [ ] **Bootstrap Calls Preflight Automatically:** Menjalankan `airo-bootstrap` memicu preflight check secara otomatis tanpa memerlukan input manual tambahan dari consumer.
* [ ] **Preflight State Detection:** `airo-preflight` mampu memetakan 5 status parity repositori: `current`, `stale`, `dirty`, `conflict`, dan `unknown`.
* [ ] **Capture Writes NDJSON Locally:** Menjalankan `airo-capture` sukses menyisipkan event operasional baru ke folder `events/raw/` dalam format NDJSON tanpa melakukan sinkronisasi Git.
* [ ] **Health File Exists:** Berkas status kesehatan [state/system-health.md](file:///home/egitaristorandas/AI_WORKSPACES/airo-second-brain/state/system-health.md) sukses digenerasikan.
* [ ] **Sync Has Lock:** Script `airo-sync` sukses mendeteksi dan menggunakan file lock `locks/airo-sync.lock` untuk mencegah tabrakan eksekusi parallel.

## Checklist Keamanan & Safety Guard
* [ ] **Secret Guard Blocks Risky Files:** Kebijakan pemblokiran file berekstensi/nama sensitif (seperti `.env`, `.pem`, `.key`, `credentials*.json`, `.clasp.json`, dll) berhasil memblokir proses git push.
* [ ] **Secret Guard Blocks Risky Content:** Deteksi regex terhadap pola content rahasia (seperti token `ghp_`, prefix kunci `AIza`/`AKIA`, token telegram, dsb) memicu status BLOCK pada commit/push.
* [ ] **No Secrets Committed:** Dipastikan tidak ada riwayat kunci rahasia yang terlanjur ter-commit ke dalam repositori lokal maupun remote.
* [ ] **No Raw Transcript Committed:** Tidak ada log transkrip obrolan kasar yang dijadikan dokumen kanonikal.

## Checklist Lifecycle & Gate Promotion
* [ ] **Organize Does Not Promote Automatically:** Script `airo-organize` tidak memindahkan proposal semantik langsung menjadi berkas kanonikal tanpa persetujuan Owner.
* [ ] **Distill Semantic Writes Proposals Only:** Hasil ekstraksi semantik hanya ditulis ke folder `distill/proposals/` dalam bentuk draf proposal.
* [ ] **Promote Gate Enforced:** Promosi proposal ke file kanonikal di Second Brain mewajibkan adanya identitas aktor penanggung jawab serta bukti pendukung (`source_evidence`).
* [ ] **Earesmes Promotion Restriction:** Sistem secara eksplisit membatasi agen Earesmes untuk memicu promosi konten semantik secara otomatis.

## Checklist Finalisasi Git & Remote State
* [ ] **Validation Commands Execute Cleanly:** Rangkaian perintah validasi wajib pada akhir eksekusi berhasil dijalankan tanpa peringatan kegagalan.
* [ ] **Git Push Successful:** Perubahan telah terdorong ke repositori remote pribadi (`origin/main`).
* [ ] **Repo Clean After Final Commit:** Hasil pemeriksaan `git status` menunjukkan kondisi workspace yang bersih tanpa berkas untracked atau modifikasi yang menggantung.
