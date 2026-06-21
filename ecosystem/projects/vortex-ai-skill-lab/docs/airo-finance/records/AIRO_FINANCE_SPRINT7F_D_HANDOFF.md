# AIRO Finance - Sprint 7F-D Handoff Record

Timestamp: 2026-05-28 23:35 WIB

## Current state

Sprint 7F-D has been partially implemented and deployed for Telegram email-answer route preview.

Latest known deployment:

- Apps Script deployment version: `73`
- Deployment description: `Sprint 7F-D amount pointer fix no-write`

## What works

PASS:

- Telegram email candidate clarification is sent from the manual editor runner.
- User can answer A/B/C/D/E from Telegram.
- Telegram answer reaches the Sprint 7F-D handler.
- Bot replies with `Sprint 7F-D: Route Preview`.
- Route preview remains no-write.
- Finance write remains disabled.
- Account Ledger write remains disabled.
- Finance Events write remains disabled.
- Review Queue write remains disabled.
- Gmail trigger is not created.
- Email is not modified.
- Full email body is not stored.
- Raw email body is not forwarded to Telegram.

## Known failing behavior

FAIL / open bug:

- Route preview still shows `Nominal: Nominal belum terbaca`.
- Expected route preview amount is `Rp101.000`.
- 7F-B transient poller already extracts `display_amount: 101000` and `detected_amount: 101000`.
- The bug is likely in pending pointer persistence / candidate payload handoff, not in transient amount extraction.

## Safety state

Keep these locked until explicit owner approval:

- Do not enable Gmail trigger.
- Do not enable finance write from email.
- Do not write email candidates to Account Ledger.
- Do not write email candidates to Finance Events.
- Do not write email candidates to Review Queue.
- Do not store full email body.
- Do not forward raw email body to Telegram.
- Keep OTP/security hard-block before parsing or forwarding.

## Owner-approved category decision

Category Clarification Policy v1 is approved.

Policy:

1. Applies globally to Telegram and Email category clarification flows, from Sprint 0 onward.
2. Final resolved data should include `Category`, `Subcategory`, `Cashflow Class`, and `Domain`.
3. If category is unknown, ask in two layers: category first, then subcategory.
4. Option E remains available, but means category picker / manual resolver, not automatic `Other`.
5. `Other / Review` is used only when the owner chooses review or the mapping remains unclear.
6. AIRO may auto-category only when confidence is high.
7. Success replies must show category and subcategory.
8. The owner must be able to correct via `edit kategori ...`, `ganti kategori`, `undo`, `/kategori`, and `/kategori <query>`.

Approved Category Contract v1:

| Category | Subcategory initial set |
|---|---|
| Housing | KPR Rumah, Sewa, Maintenance Rumah |
| Debt & Obligations | Pinjaman Lainnya, Cicilan Non-KPR |
| Groceries | Belanja Harian, Belanja Bulanan, Kebutuhan Pokok, Peralatan Rumah |
| Food & Drink | Jajan, Makan di Luar, Kopi |
| Utilities | Listrik, Air/PDAM, Wifi, Gas, Sampah, Air Minum |
| Transport | BBM, Servis Motor, Parkir, Tol, Ojek/Taxi |
| Health | Obat, Dokter, Vitamin |
| Insurance | Asuransi Jiwa, Asuransi Kesehatan, BPJS, Asuransi Kendaraan |
| Pets | Makanan Hewan, Obat Hewan, Vet, Grooming, Perlengkapan Hewan |
| Subscriptions | Streaming, Apps, Membership, Cloud |
| Personal Care | Salon/Barber, Skincare, Hygiene |
| Lifestyle & Entertainment | Hiburan, Hobi, Belanja Umum |
| Savings | Dana Darurat, Transfer Tabungan, Sinking Fund |
| Investment | Emas, Saham, Reksadana |
| Giving & Family | Hadiah, Keluarga, Donasi |
| Fees & Admin | Biaya Admin, Pajak, Denda, Bunga |
| Other / Review | Lainnya, Butuh Review |

## Next recommended task for Antigravity

Priority 1:

Fix Sprint 7F-D pending pointer amount handoff.

Acceptance:

- Run `runSprint7FSendOneClarificationAndLogPendingFromEditor`.
- Telegram receives Blu candidate with `Rp101.000`.
- User replies `A`.
- Bot replies `Sprint 7F-D: Route Preview`.
- Bot shows `Nominal: Rp101.000`.
- Bot shows `Status: ready_for_router_preview_only`.
- Safety fields remain false/no-write/no-trigger.

Priority 2:

After 7F-D amount PASS, update Living PRD and create final Sprint 7F-D closeout.

Priority 3:

Implement Category Contract v1 in PRD/Settings as source of truth before changing category prompts globally.

