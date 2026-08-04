# AIRO Status Receipt Contract

- **Status:** `ACTIVE_CONTRACT`
- **Version:** `1.1.0`
- **Scope:** `ASB_GLOBAL`
- **Owner Approved Date:** 2026-08-04

---

## 1. Purpose & Core Invariant

This contract defines the standard human-facing receipt (`🧭 AIRO STATUS`), the machine-facing structured JSON receipt, and the deterministic mapping between them.

### Critical Invariant
Chat responses, Session worklogs, and Daily navigation views **MUST NOT** independently re-infer or recalculate current task outcomes. All interfaces MUST render their status directly from the same single structured machine receipt computed by `scripts/airo-task-verdict`.

---

## 2. Section A — Human-Facing Receipt Specification (`🧭 AIRO STATUS`)

All human-facing status outputs produced by AI consumers or tools MUST conform to this exact structure:

```text
🧭 AIRO STATUS

📍 Project — <Project Name>
📌 Lagi di — <Milestone / Position Name>
📈 Progress — <Evidence-based progress summary>

🧪 Bukti
Yang wajib ada — <Required evidence items>
Yang sudah ada — <Actual evidence items>
Kesimpulan — BERHASIL | BERHASIL_DENGAN_BATASAN | BELUM_TERBUKTI | TERHAMBAT | GAGAL
Boleh lanjut — YA | TIDAK

⛔ Hambatan — <Blocker description or "Tidak ada">
➡️ Berikutnya — <Canonical next action>
🏁 Selesai kalau — <Definition of Done / DoD>
```

---

## 3. Section B — Machine-Facing Receipt Specification (JSON Schema)

Every execution task MUST generate or evaluate a structured JSON receipt with these minimum fields:

```json
{
  "project_id": "ASB_GLOBAL",
  "position_id": "M1",
  "position_name": "Governance & Execution Assurance",
  "script_status": "SCRIPT_SUCCESS",
  "required_evidence": ["PRD_v06_DesignSpec_Contracts_Validator"],
  "actual_evidence": ["Validator_Tests_Passed"],
  "limitations": ["Canonical local repo workspace adoption pending"],
  "blockers": [],
  "task_status": "BERHASIL_DENGAN_BATASAN",
  "can_advance": "NO",
  "next_exact_action": "SAFE_ADOPT_CORRECTED_REMOTE_M1_IN_CANONICAL_LOCAL_WORKSPACE",
  "done_when": "M1 remote governance corrected and canonical local workspace safely adopted",
  "evidence_references": [
    "docs/prd/AIRO_SECOND_BRAIN_PRD_v0.6.0.md",
    "docs/specs/asb/AIRO_SECOND_BRAIN_v0.6_DESIGN_SPEC.md"
  ]
}
```

---

## 4. Section C — Deterministic Mapping Rules

1. `project_id` -> `📍 Project`
2. `position_id` / `position_name` -> `📌 Lagi di`
3. `script_status` + `actual_evidence` -> `📈 Progress`
4. `required_evidence` -> `Yang wajib ada`
5. `actual_evidence` -> `Yang sudah ada`
6. `task_status` -> `Kesimpulan` (`BERHASIL`, `BERHASIL_DENGAN_BATASAN`, `BELUM_TERBUKTI`, `TERHAMBAT`, `GAGAL`)
7. `can_advance` -> `Boleh lanjut` (`YES` -> `YA`, `NO` -> `TIDAK`)
8. `blockers` -> `⛔ Hambatan` (If empty -> `Tidak ada`)
9. `next_exact_action` -> `➡️ Berikutnya`
10. `done_when` -> `🏁 Selesai kalau`

### Validation Enforcement Rules
- `script_status != SCRIPT_SUCCESS` => `Kesimpulan = GAGAL`, `can_advance = NO`.
- `blockers` non-empty => `Kesimpulan = TERHAMBAT`, `can_advance = NO`.
- `required_evidence` missing or unsatisfied => `Kesimpulan = BELUM_TERBUKTI`, `can_advance = NO`.
- `limitations` non-empty => `Kesimpulan = BERHASIL_DENGAN_BATASAN`, `can_advance = NO`.
- All `required_evidence` satisfied, no blockers, no limitations => `Kesimpulan = BERHASIL`, `can_advance = YES`.
