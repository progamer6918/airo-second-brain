# Batch intake and verified learning

Send several transactions in one Telegram message, with a common date header when known. Actual amounts govern the ledger; budgets do not create transactions.

Example (synthetic):

```text
tanggal 3 Oktober 2026
blu bayar 12rb makan siang
gether terima 203rb dari Partner untuk listrik
gether terima 50rb dari Partner untuk listrik
```

Hermes returns one numbered review. Reply to that message:

```text
no. 1 jam 12:04:09; no. 3 tanggal 5 Oktober 2026
```

Choose **Simpan yang siap**, or reply `simpan yang siap kecuali 2`. Unresolved rows remain persistent drafts. Choosing this action also approves the displayed classification proposals. A complete single transaction with an existing classification can receive its receipt directly.

For an aggregate bank payment, reply to its email card:

```text
pecah: makan siang 12rb dari saving; makan malam 12rb dari gether
```

The payment account stays Blu. Detail amounts must equal the bank payment. Existing paired funding transfers are linked, with capacity checks. If evidence is missing, answer each part once (`no. 1 bagian 1 sudah ditransfer tanggal 2 Oktober 2026`) or explicitly choose allocation only (`no. 1 bagian 1 alokasi`). An owner-confirmed missing transfer is tracked separately and does not block the known payment. No additional transfer is invented. The preview and receipt name the selected source first, identify Blu separately as the payment route, and read each actual committed account balance. If the source transfer is not linked to ledger evidence, the receipt explicitly says that its source balance does not yet reflect that transfer. This is not an account reclassification; cash ledger entries retain their actual posting account. Cancelled cards close without edit/save controls.

Use **Sudah tercatat** and supply the ledger reference, or let a unique matching reference be found. **Bukan transaksi** is a separate decision. A generic cancellation is not a negative classification label. Legacy editor buttons remain supported. Card payment corrections/cancellations use the existing card editor to preserve liability accounting.

A pending replacement of borrowed purpose-specific cash closes only after `no. 1 sudah diganti`. Actual payment purpose determines classification.

`status belajar finance` reports verified observations, field changes, questions, answers, clicks and unresolved drafts. `pola finance` lists rule IDs. `aktifkan pola ID` requires at least seven days of observation for that rule and five matching confirmations without conflicts. All email automation starts disabled. Complete bank evidence remains mandatory, and conflicting corrections disable the affected rule.

Occurrence, original message and capture times are independent. Message-derived time is marked estimated; old transactions with only a date keep their time unknown.

Tests use temporary SQLite and mocked Telegram. Run from project root:

```bash
AIRO_FINANCE_OFFLINE_TEST=1 PYTHONPATH=src python3 -m unittest discover -s tests -p test_intake.py -v
AIRO_FINANCE_OFFLINE_TEST=1 PYTHONPATH=src python3 -m unittest discover -s tests -p test_gmail_recovery.py -v
```

Schema migrations are additive. Rollback restores code and keeps the latest database. Never restore a stale backup over newer transactions. Full email bodies, credentials and real transaction fixtures must not enter Git or logs.
