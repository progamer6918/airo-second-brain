/**
 * AIRO Finance Sheet Key Exporter v0.3
 *
 * Read-only:
 * - reads duplicate_key/sync_hash-compatible keys from sync target tabs
 * - logs compact JSON snapshot
 * - performs no writes
 * - reads no SQLite
 * - reads no credentials
 *
 * Usage:
 * - Run exportAiroFinanceSheetKeysV03
 * - Copy SHEET_KEYS_JSON=... from execution log if needed
 */

function exportAiroFinanceSheetKeysV03() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();

  const snapshot = {
    title: 'AIRO FINANCE SHEET KEYS SNAPSHOT',
    version: 'v0.3',
    mode: 'read_only',
    google_write_performed: false,
    spreadsheet_name: ss.getName(),
    generated_at: Utilities.formatDate(new Date(), 'Asia/Jakarta', 'yyyy-MM-dd HH:mm:ss'),
    tabs: {
      '💸 Transactions': exportByHeaderV03_(ss, '💸 Transactions', 1, 'duplicate_key', 'sync_hash'),
      '💳 Credit Card': exportByHeaderV03_(ss, '💳 Credit Card', 3, 'linked_txn_id', null),
      '🧾 Review Queue': exportByHeaderV03_(ss, '🧾 Review Queue', 1, 'queue_id', 'sync_hash'),
      '🏠 Cicilan Rumah': exportByHeaderV03_(ss, '🏠 Cicilan Rumah', 11, 'payment_id', null),
      '🔄 Sync Log': exportByHeaderV03_(ss, '🔄 Sync Log', 2, 'sync_id', null)
    }
  };

  Logger.log('SHEET_KEYS_JSON=' + JSON.stringify(snapshot));
  return snapshot;
}

function exportByHeaderV03_(ss, tabName, headerRow, keyHeader, hashHeader) {
  const sheet = ss.getSheetByName(tabName);
  if (!sheet) {
    return [];
  }

  const lastRow = sheet.getLastRow();
  const lastCol = sheet.getLastColumn();

  if (lastRow <= headerRow || lastCol < 1) {
    return [];
  }

  const headers = sheet.getRange(headerRow, 1, 1, lastCol).getDisplayValues()[0].map(function (value) {
    return String(value || '').trim();
  });

  const keyIndex = headers.indexOf(keyHeader);
  const hashIndex = hashHeader ? headers.indexOf(hashHeader) : -1;

  if (keyIndex === -1) {
    return [];
  }

  const data = sheet.getRange(headerRow + 1, 1, lastRow - headerRow, lastCol).getDisplayValues();
  const out = [];

  data.forEach(function (row, idx) {
    const key = String(row[keyIndex] || '').trim();

    if (!key) {
      return;
    }

    out.push({
      row_number: headerRow + 1 + idx,
      duplicate_key: key,
      sync_hash: hashIndex >= 0 ? String(row[hashIndex] || '').trim() : ''
    });
  });

  return out;
}
