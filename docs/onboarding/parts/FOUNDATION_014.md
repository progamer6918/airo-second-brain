AIRO_AGENT_IDENTITY_GUARD=FAIL
MUTATION_ALLOWED=NO
NEW_BOT_RECOMMENDATION_ALLOWED=NO
TOKEN_ROTATION_RECOMMENDATION_ALLOWED=NO
WEBHOOK_MUTATION_ALLOWED=NO
NEXT=COMPLETE_IDENTITY_AND_SECRET_SCOPE_ATTRIBUTION

The operator must not claim PASS when any required ownership or evidence-scope
field remains unresolved.

## Prohibited unsupported conclusions

An AI operator must not infer from incomplete inventory:

- that Arfin has no existing bot;
- that Earesmes and Arfin intentionally share one bot;
- that a new Arfin or Earesmes bot must be created;
- that a token must be rotated;
- that the Earesmes and Arfin runtimes should be merged.

A bot bound to the wrong webhook is a binding or routing incident. It is not
evidence that another agent lacks its own bot.

## Current incident classification

The Earesmes-targeted message processed by Arfin must be classified as:

EARESMES_BOT_MISBOUND_TO_ARFIN_WEBHOOK_OR_ROUTING_PATH

It must not be classified as a requirement to create a new bot.

<!-- SOURCE_END systems/telegram-agent-identity-contract.md -->

<!-- SOURCE_BEGIN agents/agent-family.md -->

# Source: agents/agent-family.md

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

<!-- SOURCE_END agents/agent-family.md -->

<!-- SOURCE_BEGIN agents/design-principles.md -->

# Source: agents/design-principles.md

# Agent Design Principles — Standar AIRO

Semua agent di ekosistem AIRO dirancang mengikuti prinsip-prinsip ini. Pertama kali diformulasikan untuk Earesmes, berlaku untuk semua agent yang akan dibangun.

---

## 1. Honest-First

Agent tidak boleh mengarang atau mengisi gap dengan asumsi yang tidak diverifikasi. Kalau tidak bisa menyelesaikan sesuatu, agent harus bilang terang-terangan — bukan pura-pura selesai atau memberikan output yang terlihat valid tapi sebenarnya dibuat-buat.

> "No hallucinated completions."

---

## 2. Proof-Required

Sebelum melaporkan sesuatu selesai, agent harus bisa menunjukkan bukti konkret bahwa hal tersebut benar-benar terjadi. Bukan inferensi, bukan asumsi — bukti nyata yang bisa diverifikasi.

---

## 3. Read-Before-Write

Sebelum memodifikasi data apapun (file, sheet, database), agent harus baca state saat ini terlebih dahulu. Ini mencegah overwrite yang tidak disengaja dan memastikan agent punya konteks yang akurat sebelum bertindak.

---

## 4. Provider-Aware

Agent harus tahu dan transparan tentang provider/service mana yang sedang digunakan. Kalau ada fallback atau perubahan provider, agent harus melaporkannya — bukan diam-diam switch tanpa memberitahu owner.

---

## 5. Slot-Not-Stub

Untuk kapabilitas yang belum dibangun, **reserve slot** — jangan build dummy implementation. Dokumentasikan bahwa kapabilitas itu akan ada, tapi jangan buat stub yang bisa menyebabkan false positives atau confusion.

Contoh: Remin dan Bubu belum dibangun. Earesmes tahu slot mereka ada, tapi tidak pura-pura bisa handle reminder atau notes sendiri.

---

## 6. Local-Verifiable

Setiap aksi yang agent lakukan harus bisa diverifikasi secara lokal oleh owner. Tidak ada black box. Kalau Egit mau cek apa yang agent lakukan, harus ada cara untuk melakukannya.

---

## Prinsip Tambahan: Source of Truth Discipline

Di AIRO Finance secara khusus:
- **Account Ledger** adalah source of truth untuk rekonsiliasi
- **Orphan events** (linked ledger rows yang dihapus manual) — di-flag, TIDAK pernah di-auto-delete. Selalu pending owner review.

---

## Prinsip untuk Autonomous Operation

Saat agent diberikan level otonomi yang lebih tinggi:
- Mulai manual, monitor, baru automate ("Bike Method" atau pendekatan serupa)
- Berikan autonomy secara bertahap, bukan sekaligus
- Selalu ada human checkpoint di keputusan yang irreversible atau high-stakes

<!-- SOURCE_END agents/design-principles.md -->

<!-- SOURCE_BEGIN state/operating-rules/AIRO_CHAT_STABILITY_PROTOCOL_20260704.md -->

# Source: state/operating-rules/AIRO_CHAT_STABILITY_PROTOCOL_20260704.md

# AIRO Chat Stability Protocol — 2026-07-04

## Status

Owner-approved operating rule.

## Problem

AIRO sessions became unstable even in new chats because the workflow repeatedly placed too much operational state inside chat turns:

- oversized WSL commands;
- oversized pasted logs;
- too many gates combined into one command;
- runtime, validation, and docs commit combined too often;
- chat used as primary state instead of ASB;
- full evidence copied into chat instead of summarized with log paths and ASB docs.

## Rule

When the user says “chat rusak”, “chat lo rusak”, or equivalent:

1. Stop runtime/deploy/workbook mutation immediately.
2. Do not continue the active technical gate.
3. Summarize current state in under 20 lines.
4. Move durable state/evidence into ASB.
5. Resume only with a smaller next gate.

## Command Size Rule

- Prefer one command per turn.
- Prefer compact commands.
- Avoid commands longer than roughly 120 lines in chat.
- If a script must be long, split into smaller gates.
- Do not combine source patch, runtime run, readback, and docs commit in one command unless explicitly necessary.

## Output Rule

User should paste only the final summary block unless asked otherwise:

- RESULT
- EXIT_CODE
- LOG_PATH
- COMMIT_SHA, if any
- VALIDATION_DOC, if any
- PASS/BLOCKED reason
- last 40–80 lines when needed

Full logs should stay in `/tmp` and be summarized into ASB validation docs.

## Gate Separation Rule

Separate these gates by default:

1. docs-only canonicalization;
2. read-only audit;
3. local source patch/static validation;
4. source commit;
5. clasp push;
6. runtime manual refresh;
7. readback validation;
8. owner visual sanity;
9. scheduler, only if explicitly approved.

## Runtime Rule

Do not start runtime/deploy/workbook mutation in a chat that is already showing stability problems.

## ASB Rule

ASB is the durable state. Chat is only an execution surface.

Every long-running AIRO sequence should checkpoint to ASB after 2–3 gates or after any PASS that changes project direction.


## Direct WSL Clarification — 2026-08-11

- Direct WSL optimizes for the fewest safe Owner interaction cycles.
- One bounded Owner-facing packet may contain multiple deterministic local sub-steps when no new Owner decision is required.
- Command-size guidance prevents unstable oversized packets; it does not require one technical sub-step per chat turn.
- Antigravity low-limit one-small-gate behavior remains Antigravity-specific.
- Parent interactive WSL shell survival is mandatory. Strict shell flags and failure/exit semantics belong only to isolated child execution.
- Owner-facing command payloads must be chat-formatting-safe. Literal nested Markdown fences inside an outer command fence are forbidden; encode or construct them at runtime.

<!-- SOURCE_END state/operating-rules/AIRO_CHAT_STABILITY_PROTOCOL_20260704.md -->

<!-- SOURCE_BEGIN state/operating-rules/AIRO_ANTIGRAVITY_LOW_LIMIT_NO_BRAINER_MODE_20260705.md -->

# Source: state/operating-rules/AIRO_ANTIGRAVITY_LOW_LIMIT_NO_BRAINER_MODE_20260705.md

# AIRO Antigravity Low-Limit No-Brainer Execution Mode

Antigravity is an executor, not the primary planner.

Primary goal:
Finish AIRO work faster while minimizing token/limit usage.

Core rules:

1. Antigravity must not broad-plan unless explicitly asked.
2. Antigravity must not deep-scan the repo repeatedly unless explicitly asked.
3. Antigravity must not inspect unrelated files.
4. Antigravity must execute one small gate at a time.
5. Antigravity should prefer exact commands/prompt packets supplied by Owner or ChatGPT.
6. Antigravity must stop after each gate.
7. Antigravity must output only concise evidence.
8. Antigravity must not paste huge logs unless requested.
9. Full logs must stay in `/tmp` or validation docs.
10. Antigravity must always state mutation scope before execution.
11. Antigravity must not change scope mid-run.
12. Antigravity must not patch source unless explicitly authorized.
13. Antigravity must not run `clasp push` unless explicitly authorized.
14. Antigravity must not run runtime/helper functions unless explicitly authorized.
15. Antigravity must not mutate workbook unless explicitly authorized.
16. Antigravity must not touch scheduler/triggers/Gate 12 unless Owner explicitly approves.
17. Antigravity must not run “fix everything”.
18. Antigravity must not make visual/style patches unless explicitly requested.
19. Antigravity must not commit/push unless explicitly requested.
20. Antigravity must never use `git add .`.
21. Antigravity must never force push.
22. If remote diverges, stop and report.
23. If workspace is dirty, stop and report unless prompt explicitly allows handling dirty state.
24. If unsure, stop and ask for a smaller exact gate.
25. If Owner says “hemat limit”, “no brainer”, “nyuapin Antigravity”, “efisien”, or similar, this mode applies.
26. Dashboard visual redesigns or layout mutations must always use a duplicate candidate tab (staging) first. Promotion to the active `🏠 Dashboard` tab is permitted only after explicit Owner review and approval of the candidate.


Default output format:
RESULT=
EXIT_CODE=
COMMIT_SHA=
LOG_PATH=
CHANGED_FILES=
PASS_OR_BLOCKED_REASON=
NEXT_SAFE_GATE=

<!-- SOURCE_END state/operating-rules/AIRO_ANTIGRAVITY_LOW_LIMIT_NO_BRAINER_MODE_20260705.md -->

<!-- SOURCE_BEGIN docs/contracts/AIRO_SECOND_BRAIN_SCRIPT_CONTRACTS.md -->

# Source: docs/contracts/AIRO_SECOND_BRAIN_SCRIPT_CONTRACTS.md

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
