# AIRO Finance — Task 9 Credit Card "cc sudah <nomor>" Numbered Settlement Workflow PRD Amendment

**Date:** 2026-06-14  
**Audit/Amendment Mode:** `PRD_AMENDMENT_ONLY_CC_SUDAH_NUMBER_WORKFLOW_NO_SOURCE_PATCH_NO_DEPLOY_NO_WORKBOOK`  
**Auditor/Operator:** AIRO Sync (Antigravity)  

---

## 1. Context and Objective

The owner has approved a streamlined Credit Card settlement workflow for daily Telegram use to avoid typing long commands. Instead of typing `bayar tagihan cc ...`, the owner will interact with AIRO using list-based item numbers.

This document formally records the PRD amendment for this workflow. No source code changes or spreadsheet writes are performed in this session.

---

## 2. Numbered Settlement Workflow Specifications

1.  **Daftar Pending CC (`cek tagihan pending cc`)**:
    *   Command read-only untuk menampilkan item Credit Card yang `status_pocket_blu` masih pending/belum disiapkan.
    *   AIRO membalas dengan list bernomor `1..N`.
    *   Setiap item menampilkan minimal: nomor item, `description`, dan `amount`. Optional: date/merchant/billing_cycle jika ringkas.
    *   Total amount pending ditampilkan di bawah list.
2.  **Penyelesaian Tagihan (`cc sudah <nomor>`)**:
    *   Nomor pada command `cc sudah <nomor>` adalah nomor urut list (list index) dari output `cek tagihan pending cc` terakhir, **bukan nomor baris spreadsheet**.
3.  **Temporary Mapping & TTL**:
    *   AIRO menyimpan mapping sementara di memory/state:
        *   nomor item -> `cc_entry_id`
        *   amount
        *   description
        *   billing_cycle_id
        *   timestamp list dibuat
    *   Mapping memiliki TTL pendek (misal 15 menit) atau dibersihkan saat list pending CC baru dibuat.
    *   Jika command `cc sudah` dikirim tanpa mapping aktif, AIRO menolak dengan pesan meminta owner menjalankan `cek tagihan pending cc` kembali.
    *   Jika nomor tidak valid / out of range, AIRO menolak tanpa melakukan penulisan.
4.  **Idempotensi (Idempotency)**:
    *   Jika status item CC sudah `Sudah`, command dilewati (no-op) untuk mencegah double write ledger.
5.  **Ledger-First Enforcement**:
    *   Mapping di-resolve ke `cc_entry_id`.
    *   Membaca ulang baris CC live di spreadsheet untuk memastikan status masih pending.
    *   Menulis `writeAccountLedgerMirror_` (cash outflow) terlebih dahulu.
    *   Verifikasi keberhasilan penulisan ledger (`writeVerified === true`).
    *   Hanya jika terverifikasi, update baris Credit Card:
        *   `status_pocket_blu = ✅ Sudah`
        *   `transferred_at = timestamp`
        *   `linked_txn_id = Account Ledger reference`
        *   notes di-append.
    *   Jika penulisan ledger gagal, status CC tidak boleh berubah.
6.  **Cycle Header Auto-Refresh**:
    *   Setelah settlement berhasil, jalankan refresh header Credit Card agar `PERIODE BERJALAN / UNBILLED` dan total pending tidak stale di spreadsheet.
7.  **Manual Override & Audit Flag**:
    *   Manual edit langsung dari `Belum` ke `Sudah` di spreadsheet tanpa `linked_txn_id` yang valid dianggap bypass ledger.
    *   Sistem audit harus menandai baris tersebut dengan flag `CC_STATUS_SUDAH_WITHOUT_LEDGER_LINK` agar muncul sebagai warning di Dashboard.

---

## 3. Command Examples

```text
cek tagihan pending cc
cc sudah 1
cc sudah 2
```

---

## 4. Expected Output Example

```text
💳 Pending Pocket Blu CC

1. Nasgor ShopeeFood — Rp35.000
2. UPS Wifi Shopee — Rp81.000

Total belum disiapkan ke Blu: Rp116.000

Balas:
cc sudah <nomor>
```

---

## 5. Explicit Non-Goals

*   **No CC Purchase Ledger Outflow**: Pembelian kartu kredit (`cc_purchase`) tetap domain-only di tab Credit Card (bukan wallet outflow).
*   **No Raw Row Numbers**: Nomor referensi bukan representasi row number spreadsheet.
*   **No Unverified Status Change**: Status CC tidak boleh berubah menjadi `Sudah` jika penulisan ledger belum diverifikasi.
*   **No Telegram Live Test**: Dilarang melakukan live testing Telegram selama status WebApp masih 403.
