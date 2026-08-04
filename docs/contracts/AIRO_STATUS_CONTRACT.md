# AIRO Status Receipt Contract

- **Status:** `ACTIVE_CONTRACT`
- **Version:** `1.0.0`
- **Scope:** `ASB_GLOBAL`

---

## 1. Purpose

This contract defines the format and rules for the standardized human-facing status receipt: `🧭 AIRO STATUS`.

---

## 2. Receipt Specification

All human-facing status outputs produced by AI consumers or tools MUST conform to this exact structure:

```text
🧭 AIRO STATUS

📍 Project — <Project Name>
📌 Lagi di — <Milestone / Position>
📈 Progress — <Evidence-based progress summary>

🧪 Bukti
Yang wajib ada — <Required evidence items>
Yang sudah ada — <Actual evidence items>
Kesimpulan — BERHASIL | BERHASIL_DENGAN_BATASAN | BELUM_TERBUKTI | TERHAMBAT | GAGAL
Boleh lanjut — YA | TIDAK

⛔ Hambatan — <Blocker description or "Tidak ada">
➡️ Berikutnya — <Canonical next action>
🏁 Selesai kalau — <Definition of Done>
```

---

## 3. Validation Rules

1. **Header Invariant:** Output MUST start with `🧭 AIRO STATUS`.
2. **Indonesian Terminology:** Field labels MUST use simple Indonesian terms as defined above.
3. **No False Advancement:** `Boleh lanjut` MUST be `YA` ONLY IF `Kesimpulan` is `BERHASIL`.
4. **No Raw Enums / UUIDs:** UUIDs and raw machine enums are forbidden in the human receipt.
