/**
 * AIRO Credit Card Billing Cycle v0.8
 *
 * Purpose:
 * - Patch 💳 Credit Card header to support Tokopedia Card billing cycle.
 * - Validate cycle logic for 16th-to-15th statement periods.
 *
 * This writes only 💳 Credit Card header/formatting cells.
 * It does not write finance transaction rows.
 */

function patchCreditCardBillingCycleHeaderV08() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName('💳 Credit Card');

  if (!sheet) {
    throw new Error('ABORT: 💳 Credit Card tab not found.');
  }

  const expectedBase = [
    'cc_entry_id',
    'date',
    'merchant_app',
    'amount',
    'description',
    'status_pocket_blu',
    'transferred_at',
    'linked_txn_id',
    'notes'
  ];

  const currentBase = sheet.getRange('A3:I3').getDisplayValues()[0].map(function (value) {
    return String(value || '').trim();
  });

  for (let i = 0; i < expectedBase.length; i++) {
    if (currentBase[i] !== expectedBase[i]) {
      throw new Error('ABORT: base Credit Card header mismatch at position ' + String(i + 1) + '. Expected ' + expectedBase[i] + ', saw ' + currentBase[i]);
    }
  }

  const billingHeaders = [
    'billing_cycle_id',
    'billing_start',
    'billing_end',
    'statement_month',
    'due_date',
    'is_statement_locked'
  ];

  sheet.getRange('J3:O3').setValues([billingHeaders]);
  sheet.getRange('J3:O3')
    .setBackground('#6A1B9A')
    .setFontColor('#FFFFFF')
    .setFontWeight('bold')
    .setHorizontalAlignment('center')
    .setVerticalAlignment('middle')
    .setWrap(true);

  sheet.getRange('K4:L2000').setNumberFormat('yyyy-mm-dd');
  sheet.getRange('N4:N2000').setNumberFormat('yyyy-mm-dd');

  const lockRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(['TRUE', 'FALSE'], true)
    .setAllowInvalid(false)
    .build();

  sheet.getRange('O4:O2000').setDataValidation(lockRule);

  const widths = [150, 120, 120, 130, 120, 140];
  widths.forEach(function (width, index) {
    sheet.setColumnWidth(10 + index, width);
  });

  Logger.log('AIRO_CC_BILLING_CYCLE_HEADER_V08=PASS');
  Logger.log('google_write_performed=true');
  Logger.log('write_scope=credit_card_header_only');
  Logger.log('finance_ledger_write_performed=false');
}

function validateCreditCardBillingCycleHeaderV08() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName('💳 Credit Card');

  if (!sheet) {
    throw new Error('ABORT: 💳 Credit Card tab not found.');
  }

  const expected = [
    'cc_entry_id',
    'date',
    'merchant_app',
    'amount',
    'description',
    'status_pocket_blu',
    'transferred_at',
    'linked_txn_id',
    'notes',
    'billing_cycle_id',
    'billing_start',
    'billing_end',
    'statement_month',
    'due_date',
    'is_statement_locked'
  ];

  const seen = sheet.getRange('A3:O3').getDisplayValues()[0].map(function (value) {
    return String(value || '').trim();
  });

  const mismatches = [];

  for (let i = 0; i < expected.length; i++) {
    if (seen[i] !== expected[i]) {
      mismatches.push({
        position: i + 1,
        expected: expected[i],
        seen: seen[i]
      });
    }
  }

  const status = mismatches.length === 0 ? 'PASS' : 'FAIL';

  Logger.log('AIRO_CC_BILLING_CYCLE_HEADER_VALIDATE_V08=' + status);
  Logger.log(JSON.stringify({
    status: status,
    google_write_performed: false,
    checked_range: '💳 Credit Card!A3:O3',
    mismatches: mismatches
  }));

  return {
    status: status,
    google_write_performed: false,
    mismatches: mismatches
  };
}

function computeTokpedCardBillingCycleV08(transactionDate) {
  const dateObj = new Date(transactionDate + 'T00:00:00+07:00');
  const day = dateObj.getDate();
  const year = dateObj.getFullYear();
  const month = dateObj.getMonth();

  let start;
  let end;

  if (day >= 16) {
    start = new Date(year, month, 16);
    end = new Date(year, month + 1, 15);
  } else {
    start = new Date(year, month - 1, 16);
    end = new Date(year, month, 15);
  }

  const statementMonth = formatYearMonthV08_(end);

  return {
    billing_cycle_id: 'TOKPED_CC_' + statementMonth,
    billing_start: formatDateV08_(start),
    billing_end: formatDateV08_(end),
    statement_month: statementMonth
  };
}

function smokeTestTokpedCardBillingCycleV08() {
  const cases = [
    ['2026-04-15', '2026-03-16', '2026-04-15', '2026-04', 'TOKPED_CC_2026-04'],
    ['2026-04-16', '2026-04-16', '2026-05-15', '2026-05', 'TOKPED_CC_2026-05'],
    ['2026-05-15', '2026-04-16', '2026-05-15', '2026-05', 'TOKPED_CC_2026-05'],
    ['2026-05-16', '2026-05-16', '2026-06-15', '2026-06', 'TOKPED_CC_2026-06']
  ];

  const failures = [];

  cases.forEach(function (item) {
    const got = computeTokpedCardBillingCycleV08(item[0]);

    if (
      got.billing_start !== item[1] ||
      got.billing_end !== item[2] ||
      got.statement_month !== item[3] ||
      got.billing_cycle_id !== item[4]
    ) {
      failures.push({
        input: item[0],
        expected: item.slice(1),
        got: got
      });
    }
  });

  if (failures.length > 0) {
    throw new Error('Billing cycle smoke test failed: ' + JSON.stringify(failures));
  }

  Logger.log('AIRO_CC_BILLING_CYCLE_SMOKE_V08=PASS');
  return {
    status: 'PASS',
    cases: cases.length
  };
}

function formatDateV08_(dateObj) {
  return dateObj.getFullYear() + '-' + pad2V08_(dateObj.getMonth() + 1) + '-' + pad2V08_(dateObj.getDate());
}

function formatYearMonthV08_(dateObj) {
  return dateObj.getFullYear() + '-' + pad2V08_(dateObj.getMonth() + 1);
}

function pad2V08_(value) {
  return String(value).padStart(2, '0');
}
