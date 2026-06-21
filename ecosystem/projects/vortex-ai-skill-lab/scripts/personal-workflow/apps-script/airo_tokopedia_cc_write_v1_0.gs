/**
 * AIRO Tokopedia CC Write v1.0
 *
 * Scope:
 * - Appends one Tokopedia CC transaction to 💸 Transactions if missing.
 * - Appends one mirror row to 💳 Credit Card if missing.
 * - Appends one audit row to 🔄 Sync Log.
 *
 * Idempotency:
 * - 💸 Transactions: duplicate_key = transactions:trx_41a84be31c7e
 * - 💳 Credit Card: linked_txn_id = trx_41a84be31c7e
 *
 * Approval gate:
 * - ⚙️ Settings / Google Write Approval Phrase
 * - I APPROVE GOOGLE SHEETS WRITE FOR AIRO FINANCE
 */

function airoFinanceTokopediaCcWriteV10() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const approval = getAiroSettingValueV10_(ss, 'Google Write Approval Phrase');
  const expectedApproval = 'I APPROVE GOOGLE SHEETS WRITE FOR AIRO FINANCE';

  if (approval !== expectedApproval) {
    throw new Error('ABORT: Google Sheets write approval phrase missing or invalid.');
  }

  const txSheet = ss.getSheetByName('💸 Transactions');
  const ccSheet = ss.getSheetByName('💳 Credit Card');
  const syncLog = ss.getSheetByName('🔄 Sync Log');

  if (!txSheet) throw new Error('ABORT: 💸 Transactions tab not found.');
  if (!ccSheet) throw new Error('ABORT: 💳 Credit Card tab not found.');
  if (!syncLog) throw new Error('ABORT: 🔄 Sync Log tab not found.');

  validateTransactionsHeaderV10_(txSheet);
  validateCreditCardHeaderV10_(ccSheet);
  validateSyncLogHeaderV10_(syncLog);

  const now = new Date();
  const timestamp = Utilities.formatDate(now, 'Asia/Jakarta', 'yyyy-MM-dd HH:mm:ss');
  const runId = 'tokopedia_cc_write_v1_0_' + Utilities.formatDate(now, 'Asia/Jakarta', 'yyyyMMdd_HHmmss') + '_' + randomHexV10_(6);

  const txHeaders = ["transaction_id", "date", "month", "type", "category", "subcategory", "description", "merchant", "amount", "account", "source", "status", "confidence", "raw_text", "synced_at", "notes", "currency", "review_status", "local_db_table", "local_db_rowid", "sync_hash", "duplicate_key", "created_at", "updated_at", "from_account", "to_account", "transfer_purpose", "asset_bucket", "pocket_name", "cashflow_treatment"];
  const txValues = ["trx_41a84be31c7e", "2026-05-10", "2026-05", "expense", "Belanja", "", "catat beli barang tokopedia 100rb pakai tokopedia credit card", "belanja", 100000, "Tokopedia CC", "telegram", "synced", 0.9, "catat beli barang tokopedia 100rb pakai tokopedia credit card", "", "", "IDR", "auto_approved", "transactions", 3, "1ed99b1b6f6bbf1e429c76b3", "transactions:trx_41a84be31c7e", "2026-05-10 09:33:21", "2026-05-10 09:33:21", "", "", "", "", "", "operating_expense"];
  const ccHeaders = ["cc_entry_id", "date", "merchant_app", "amount", "description", "status_pocket_blu", "transferred_at", "linked_txn_id", "notes", "billing_cycle_id", "billing_start", "billing_end", "statement_month", "due_date", "is_statement_locked"];
  const ccValues = ["cc_2a09abd97f9b", "2026-05-10", "belanja", 100000, "catat beli barang tokopedia 100rb pakai tokopedia credit card", "pending_transfer", "", "trx_41a84be31c7e", "auto_mirror_from_transactions_v0_9", "TOKPED_CC_2026-05", "2026-04-16", "2026-05-15", "2026-05", "", "FALSE"];

  setValueByHeaderV10_(txHeaders, txValues, 'synced_at', timestamp);
  setValueByHeaderV10_(txHeaders, txValues, 'status', 'synced');
  setValueByHeaderV10_(txHeaders, txValues, 'notes', 'tokopedia_cc_write_v1_0');

  const txDuplicateKey = getValueByHeaderV10_(txHeaders, txValues, 'duplicate_key');
  const ccLinkedTxnId = getValueByHeaderV10_(ccHeaders, ccValues, 'linked_txn_id');

  const existingTx = findRowByHeaderValueV10_(txSheet, 1, 'duplicate_key', txDuplicateKey);
  const existingCc = findRowByHeaderValueV10_(ccSheet, 3, 'linked_txn_id', ccLinkedTxnId);

  let txInserted = 0;
  let ccInserted = 0;
  let skipped = 0;

  if (existingTx.rowNumber) {
    skipped += 1;
  } else {
    txSheet.appendRow(txValues);
    txInserted = 1;
  }

  if (existingCc.rowNumber) {
    skipped += 1;
  } else {
    ccSheet.appendRow(ccValues);
    ccInserted = 1;
  }

  const status = txInserted + ccInserted > 0 ? 'PASS' : 'SKIP_DUPLICATE';

  appendSyncLogV10_(syncLog, {
    run_id: runId,
    source_table: 'transactions',
    source_rowid: getValueByHeaderV10_(txHeaders, txValues, 'local_db_rowid'),
    target_tab: '💸 Transactions + 💳 Credit Card',
    transaction_id: getValueByHeaderV10_(txHeaders, txValues, 'transaction_id'),
    action: status === 'PASS' ? 'insert' : 'skip_duplicate',
    status: status === 'PASS' ? 'success' : 'skipped',
    records_seen: 2,
    records_inserted: txInserted + ccInserted,
    records_updated: 0,
    records_skipped: skipped,
    records_failed: 0,
    error_message: '',
    notes: 'tokopedia cc transaction + credit card mirror v1.0'
  });

  Logger.log('AIRO_TOKOPEDIA_CC_WRITE_V10=' + status);
  Logger.log('google_write_performed=true');
  Logger.log('finance_ledger_write_performed=' + String(txInserted + ccInserted > 0));
  Logger.log('write_scope=transactions_plus_credit_card');
  Logger.log('transaction_id=' + getValueByHeaderV10_(txHeaders, txValues, 'transaction_id'));
  Logger.log('transactions_inserted=' + String(txInserted));
  Logger.log('credit_card_inserted=' + String(ccInserted));
  Logger.log('records_skipped=' + String(skipped));
  Logger.log('billing_cycle_id=' + getValueByHeaderV10_(ccHeaders, ccValues, 'billing_cycle_id'));
  Logger.log('run_id=' + runId);

  return {
    status: status,
    google_write_performed: true,
    finance_ledger_write_performed: txInserted + ccInserted > 0,
    write_scope: 'transactions_plus_credit_card',
    transaction_id: getValueByHeaderV10_(txHeaders, txValues, 'transaction_id'),
    linked_txn_id: ccLinkedTxnId,
    transactions_inserted: txInserted,
    credit_card_inserted: ccInserted,
    records_skipped: skipped,
    billing_cycle_id: getValueByHeaderV10_(ccHeaders, ccValues, 'billing_cycle_id'),
    run_id: runId
  };
}

function getAiroSettingValueV10_(ss, key) {
  const sheet = ss.getSheetByName('⚙️ Settings');
  if (!sheet) throw new Error('ABORT: ⚙️ Settings tab not found.');

  const values = sheet.getRange(1, 1, Math.max(sheet.getLastRow(), 1), 2).getDisplayValues();

  for (let i = 0; i < values.length; i++) {
    if (String(values[i][0] || '').trim() === key) {
      return String(values[i][1] || '').trim();
    }
  }

  throw new Error('ABORT: setting key not found: ' + key);
}

function validateTransactionsHeaderV10_(sheet) {
  const expected = ["transaction_id", "date", "month", "type", "category", "subcategory", "description", "merchant", "amount", "account", "source", "status", "confidence", "raw_text", "synced_at", "notes", "currency", "review_status", "local_db_table", "local_db_rowid", "sync_hash", "duplicate_key", "created_at", "updated_at", "from_account", "to_account", "transfer_purpose", "asset_bucket", "pocket_name", "cashflow_treatment"];
  const seen = sheet.getRange('A1:AD1').getDisplayValues()[0].map(function (value) {
    return String(value || '').trim();
  });
  validateHeaderArrayV10_('💸 Transactions', expected, seen);
}

function validateCreditCardHeaderV10_(sheet) {
  const expected = ["cc_entry_id", "date", "merchant_app", "amount", "description", "status_pocket_blu", "transferred_at", "linked_txn_id", "notes", "billing_cycle_id", "billing_start", "billing_end", "statement_month", "due_date", "is_statement_locked"];
  const seen = sheet.getRange('A3:O3').getDisplayValues()[0].map(function (value) {
    return String(value || '').trim();
  });
  validateHeaderArrayV10_('💳 Credit Card', expected, seen);
}

function validateSyncLogHeaderV10_(sheet) {
  const expected = [
    'sync_id', 'run_id', 'source_db', 'source_table', 'source_rowid',
    'target_tab', 'transaction_id', 'action', 'status', 'records_seen',
    'records_inserted', 'records_updated', 'records_skipped', 'records_failed',
    'error_message', 'started_at', 'finished_at', 'synced_at', 'notes'
  ];
  const seen = sheet.getRange('A2:S2').getDisplayValues()[0].map(function (value) {
    return String(value || '').trim();
  });
  validateHeaderArrayV10_('🔄 Sync Log', expected, seen);
}

function validateHeaderArrayV10_(label, expected, seen) {
  for (let i = 0; i < expected.length; i++) {
    if (seen[i] !== expected[i]) {
      throw new Error('ABORT: ' + label + ' header mismatch at position ' + String(i + 1) + '. Expected ' + expected[i] + ', saw ' + seen[i]);
    }
  }
}

function findRowByHeaderValueV10_(sheet, headerRow, keyHeader, keyValue) {
  const lastRow = sheet.getLastRow();
  const lastCol = sheet.getLastColumn();

  if (lastRow <= headerRow) {
    return { rowNumber: null };
  }

  const headers = sheet.getRange(headerRow, 1, 1, lastCol).getDisplayValues()[0].map(function (value) {
    return String(value || '').trim();
  });

  const keyIndex = headers.indexOf(keyHeader);
  if (keyIndex === -1) {
    throw new Error('ABORT: header not found: ' + keyHeader);
  }

  const values = sheet.getRange(headerRow + 1, 1, lastRow - headerRow, lastCol).getDisplayValues();

  for (let i = 0; i < values.length; i++) {
    if (String(values[i][keyIndex] || '').trim() === String(keyValue || '').trim()) {
      return { rowNumber: headerRow + 1 + i };
    }
  }

  return { rowNumber: null };
}

function appendSyncLogV10_(sheet, entry) {
  const now = new Date();
  const timestamp = Utilities.formatDate(now, 'Asia/Jakarta', 'yyyy-MM-dd HH:mm:ss');

  sheet.appendRow([
    'sync_' + randomHexV10_(12),
    entry.run_id,
    'not_read_by_apps_script',
    entry.source_table,
    entry.source_rowid,
    entry.target_tab,
    entry.transaction_id,
    entry.action,
    entry.status,
    entry.records_seen,
    entry.records_inserted,
    entry.records_updated,
    entry.records_skipped,
    entry.records_failed,
    entry.error_message,
    timestamp,
    timestamp,
    timestamp,
    entry.notes
  ]);
}

function getValueByHeaderV10_(headers, values, header) {
  const idx = headers.indexOf(header);
  return idx === -1 ? '' : values[idx];
}

function setValueByHeaderV10_(headers, values, header, value) {
  const idx = headers.indexOf(header);
  if (idx !== -1) {
    values[idx] = value;
  }
}

function randomHexV10_(length) {
  const chars = '0123456789abcdef';
  let out = '';
  for (let i = 0; i < length; i++) {
    out += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return out;
}
