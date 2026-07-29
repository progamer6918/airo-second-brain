# EAB Scope-Locked Behavior & Acceptance Specification

- **STATUS**: `SCOPE_LOCKED`
- **OWNER_SCOPE_LOCK**: `APPROVED`
- **CANONICAL_STATUS**: `PROPOSED_PENDING_INTEGRATION`
- **IMPLEMENTATION_STATE**: `NOT_STARTED`
- **IMPLEMENTATION_AUTHORIZED**: `NO`
- **AFPD_INC_011_IMPLEMENTATION_BLOCKER**: `YES`
- **OWNER_SCOPE_LOCK**: `APPROVED`
- **PROJECT**: `EARESMES_ARFIN_CLARIFICATION_BRIDGE` (`EAB`)

---

## 1. Indonesian Chat Examples (Scope-Locked UX)

### Scenario A: Multi-Pending List with Stable Short References
- **Earesmes Prompt**:
  > 📥 **Daftar Pending Clarification Arfin (2 item)**
  > `AF-1042` · Rp50.000 · GrabFood (butuh akun & kategori)
  > `AF-1043` · Rp200.000 · Tokopedia (butuh kategori)
  >
  > Balas: `AF-1042 blu pocket makan luar` atau `#1 blu pocket makan luar`
- **Owner Input**: `"AF-1042 blu pocket makan luar"`
- **Earesmes Response**:
  > ✅ Item `AF-1042` (Rp50.000) berhasil diklarifikasi ke **Blu Pocket / Makan Luar**.
  > Staged ke Review Queue (`TX-20260728-001`). Tersisa 1 item pending (`AF-1043`).

### Scenario B: Batch Partial Success (FND-001 Remediation)
- **Owner Input**:
  ```text
  AF-1042 blu pocket makan luar
  catat 20rb jago transport online
  ```
- **Earesmes Response**:
  > 🔄 **Hasil Pemrosesan Batch:**
  > ✅ `AF-1042`: Staged ke Review Queue (**Blu Pocket / Makan Luar**)
  > ❌ `Line 2`: Gagal — Akun *"jago"* tidak ditemukan. Mohon sebutkan nama akun canonical.

### Scenario C: Direct Arfin Resolution Sync (FND-002 Remediation)
- **Context**: Owner resolved `AF-1042` directly in Arfin Bot 5 minutes ago. Owner now sends `"AF-1042 blu pocket makan luar"` to Earesmes.
- **Pre-Submission Revalidation**: Worker calls `eabGetPending("uuid-v4-af-1042")` -> Status is `RESOLVED_DIRECT_ARFIN`.
- **Earesmes Response**:
  > ℹ️ Transaksi `AF-1042` sudah diselesaikan secara langsung di Arfin Bot. Balasan diabaikan.

### Scenario D: Manual Multi-line `catat` (FND-003 Remediation)
- **Owner Input**:
  ```text
  catat 50rb blu pocket makan luar
  catat 20rb bca transport online
  ```
- **Earesmes Response**:
  > 📝 **2 Catatan Manual Diterima & Staged ke Review Queue:**
  > 1. Rp50.000 · Blu Pocket · Food & Drink (Makan Luar)
  > 2. Rp20.000 · BCA Main · Transport (Transport Online)

---

## 2. Acceptance Criteria & Test Gates
1. Static Schema & Syntax Check (`node --check`).
2. Itemized Batch Parser Unit Tests (`TEST-WF-005-PARTIAL`).
3. Pre-Submission Revalidation Unit Tests (`TEST-WF-020-SYNC`).
4. Multi-line Manual Parser Unit Tests (`TEST-WF-007-MULTILINE`).
5. Concurrency & Stale Version Rejection Tests (`TEST-WF-012`).
6. Security Allowlist Tests (`TEST-WF-026`).
7. Fresh Live Canary Test.
8. Owner Acceptance Test.
