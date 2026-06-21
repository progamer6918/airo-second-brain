# Panduan Penggunaan Perintah Telegram AIRO Finance

Dokumen ini berisi panduan praktis dalam bahasa Indonesia untuk mempermudah pemilik (*owner*) dalam memproses penyelesaian pembayaran kartu kredit menggunakan bot Telegram AIRO.

---

## 1. Perintah: `cek tagihan pending cc`

### Kegunaan
Menampilkan semua transaksi kartu kredit berjalan (*unbilled*) yang belum disisihkan saldonya ke rekening penampung (`Blu Pocket CC`).

### Cara Menjalankan
Kirimkan pesan berikut ke bot Telegram:
```text
cek tagihan pending cc
```

### Contoh Balasan dari Bot
```text
💳 Pending Dana CC
Workbook: ...
Total belum disisihkan ke Blu Pocket CC: Rp81.000

1. cc beli 24000 — Rp24.000
2. cc bayar pdam 57rb — Rp57.000

Ketik 'cc sudah <nomor>' untuk menyisihkan dana tagihan.
```

---

## 2. Perintah: `cc sudah <nomor>`

### Kegunaan
Menyisihkan dana tagihan dari rekening utama (`Blu Pocket`) ke rekening penampung kartu kredit (`Blu Pocket CC`) sesuai dengan nomor urut transaksi pada hasil pencarian `cek tagihan pending cc` terakhir.

### Cara Menjalankan
Ketik perintah sesuai nomor urut transaksi yang ingin diselesaikan. Contoh untuk menyelesaikan item nomor 1:
```text
cc sudah 1
```

> [!IMPORTANT]
> Nomor yang dimasukkan adalah **nomor urut daftar pada balasan Telegram**, bukan nomor baris di Google Sheets.

### Contoh Balasan dari Bot (Sukses)
```text
✅ Dana CC Disisihkan
Item: cc beli 24000
Amount: Rp24.000
Transfer: Blu Pocket → Blu Pocket CC
Ledger Row: 📒 Account Ledger:119
Saldo Blu Pocket sekarang: Rp477.000
Saldo Blu Pocket CC sekarang: Rp24.000
```

---

## 3. Penanganan Kasus / Pemecahan Masalah

### A. Jika Balasan Mengatakan "Nomor pending CC belum terdaftar atau sudah kedaluwarsa"
* **Penyebab:** Anda belum menjalankan `cek tagihan pending cc` sebelumnya, atau sesi pencarian terakhir sudah kedaluwarsa (berumur lebih dari beberapa menit).
* **Solusi:** Jalankan kembali perintah `cek tagihan pending cc` untuk memperbarui daftar, lalu ketik `cc sudah <nomor>` kembali.

### B. Jika Balasan Mengatakan "Transaksi sudah disiapkan ke Blu (Already Settled)"
* **Penyebab:** Transaksi tersebut sudah pernah diselesaikan sebelumnya di masa lalu. Sistem memblokir penulisan ulang untuk mencegah duplikasi saldo di buku kas.
* **Solusi:** Abaikan pesan ini. Transaksi sudah aman dan tercatat di Ledger.

### C. Jika Tidak Ada Item Pending yang Muncul
* **Penyebab:** Semua tagihan kartu kredit Anda sudah tercatat "Sudah" di Google Sheets.
* **Solusi:** Tidak perlu melakukan tindakan apa pun. Buku kas Anda sudah sinkron.

---

## 4. Larangan Penting (Jangan Dilakukan)
* **Jangan mengetik nominal uang:** Cukup gunakan nomor urut list (misal: `cc sudah 1` atau `cc sudah 2`, **bukan** `cc sudah 24000`).
* **Jangan mengubah status secara manual di spreadsheet tanpa membuat baris ledger:** Mengubah kolom status di tab `Credit Card` menjadi "Sudah" secara manual tanpa mencatat transfer di `Account Ledger` akan menyebabkan ketidakseimbangan buku kas (*reconciliation error*). Gunakan selalu perintah bot Telegram untuk otomatisasi yang aman.
