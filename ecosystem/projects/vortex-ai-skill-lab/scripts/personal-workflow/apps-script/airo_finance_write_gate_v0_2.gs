/**
 * AIRO Finance Write-gate Probe v0.2
 *
 * Scope:
 * - Appends one probe row to 🔄 Sync Log only.
 * - Does not write finance ledger rows.
 * - Does not read SQLite.
 * - Does not read credentials.
 * - Does not create/delete/clear tabs.
 *
 * Approval:
 * - Put the exact phrase in ⚙️ Settings column B where column A is:
 *   Google Write Approval Phrase
 *
 * Exact phrase:
 * I APPROVE GOOGLE SHEETS WRITE FOR AIRO FINANCE
 */

function airoFinanceWriteGateProbeV02() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const approval = getAiroSettingValueV02_(ss, 'Google Write Approval Phrase');
  const expectedApproval = 'I APPROVE GOOGLE SHEETS WRITE FOR AIRO FINANCE';

  if (approval !== expectedApproval) {
    throw new Error('ABORT: Google Sheets write approval phrase missing or invalid.');
  }

  const syncLog = ss.getSheetByName('🔄 Sync Log');
  if (!syncLog) {
    throw new Error('ABORT: 🔄 Sync Log tab not found.');
  }

  validateSyncLogHeaderV02_(syncLog);

  const now = new Date();
  const timestamp = Utilities.formatDate(now, 'Asia/Jakarta', 'yyyy-MM-dd HH:mm:ss');
  const runId = 'write_probe_' + Utilities.formatDate(now, 'Asia/Jakarta', 'yyyyMMdd_HHmmss') + '_' + randomHexV02_(6);
  const syncId = 'sync_' + randomHexV02_(12);

  const row = [
    syncId,
    runId,
    'not_read',
    'write_gate_probe',
    '',
    '🔄 Sync Log',
    '',
    'dry_run',
    'success',
    0,
    0,
    0,
    0,
    0,
    '',
    timestamp,
    timestamp,
    timestamp,
    'write_gate_probe_v0_2_no_finance_ledger_write'
  ];

  syncLog.appendRow(row);

  Logger.log('AIRO_WRITE_GATE_PROBE_V02=PASS');
  Logger.log('google_write_performed=true');
  Logger.log('write_scope=sync_log_only');
  Logger.log('finance_ledger_write_performed=false');
  Logger.log('run_id=' + runId);

  return {
    status: 'PASS',
    google_write_performed: true,
    write_scope: 'sync_log_only',
    finance_ledger_write_performed: false,
    run_id: runId,
    sync_id: syncId
  };
}

function getAiroSettingValueV02_(ss, key) {
  const sheet = ss.getSheetByName('⚙️ Settings');
  if (!sheet) {
    throw new Error('ABORT: ⚙️ Settings tab not found.');
  }

  const lastRow = Math.max(sheet.getLastRow(), 1);
  const values = sheet.getRange(1, 1, lastRow, 2).getDisplayValues();

  for (let i = 0; i < values.length; i++) {
    const settingKey = String(values[i][0] || '').trim();
    if (settingKey === key) {
      return String(values[i][1] || '').trim();
    }
  }

  throw new Error('ABORT: setting key not found: ' + key);
}

function validateSyncLogHeaderV02_(sheet) {
  const expected = [
    'sync_id',
    'run_id',
    'source_db',
    'source_table',
    'source_rowid',
    'target_tab',
    'transaction_id',
    'action',
    'status',
    'records_seen',
    'records_inserted',
    'records_updated',
    'records_skipped',
    'records_failed',
    'error_message',
    'started_at',
    'finished_at',
    'synced_at',
    'notes'
  ];

  const seen = sheet.getRange('A2:S2').getDisplayValues()[0].map(function (value) {
    return String(value || '').trim();
  });

  const missing = expected.filter(function (header) {
    return seen.indexOf(header) === -1;
  });

  if (missing.length > 0) {
    throw new Error('ABORT: 🔄 Sync Log missing headers: ' + missing.join(', '));
  }

  for (let i = 0; i < expected.length; i++) {
    if (seen[i] !== expected[i]) {
      throw new Error(
        'ABORT: 🔄 Sync Log header order mismatch at position ' +
        String(i + 1) +
        '. Expected ' +
        expected[i] +
        ', saw ' +
        seen[i]
      );
    }
  }
}

function randomHexV02_(length) {
  const chars = '0123456789abcdef';
  let out = '';

  for (let i = 0; i < length; i++) {
    out += chars.charAt(Math.floor(Math.random() * chars.length));
  }

  return out;
}
