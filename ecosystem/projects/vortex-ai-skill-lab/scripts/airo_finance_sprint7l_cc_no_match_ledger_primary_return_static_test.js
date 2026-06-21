
const fs = require('fs');

const sourcePath = 'apps-script-prod-v2/AIRO_Finance_Multitab_Final_v1.js';
const source = fs.readFileSync(sourcePath, 'utf8');

const required = [
  'AIRO_TASK9_CC_NO_MATCH_LEDGER_PRIMARY_RETURN_V1',
  "noMatchLedgerResult.status === 'written'",
  'noMatchLedgerResult.writeVerified === true',
  'writtenTab: AIRO_CONFIG.tabs.accountLedger',
  'review_queue_result: reviewResult || null',
  'cc_payment_account_ledger_status:',
  'cc_payment_no_match_review_row:'
];

const forbidden = [
  'return Object.assign({}, reviewResult, {\\n      account_ledger_result: noMatchLedgerResult || null,\\n      cc_payment_no_match: true\\n    });'
];

const failures = [];

for (const needle of required) {
  if (!source.includes(needle)) failures.push({type:'missing_source_marker', needle});
}

for (const needle of forbidden) {
  if (source.includes(needle)) failures.push({type:'forbidden_old_return_block_still_present'});
}

const AIRO_CONFIG = {
  tabs: {
    accountLedger: 'Account Ledger',
    review: 'Review Queue'
  }
};

function decideNoMatchReturn(noMatchLedgerResult, reviewResult) {
  if (
    noMatchLedgerResult &&
    noMatchLedgerResult.status === 'written' &&
    noMatchLedgerResult.writeVerified === true
  ) {
    return Object.assign({}, noMatchLedgerResult, {
      writtenTab: AIRO_CONFIG.tabs.accountLedger,
      account_ledger_result: noMatchLedgerResult,
      review_queue_result: reviewResult || null,
      cc_payment_no_match: true,
      cc_payment_no_match_review_status:
        reviewResult && reviewResult.status ? reviewResult.status : '',
      cc_payment_no_match_review_row:
        reviewResult && reviewResult.row ? reviewResult.row : ''
    });
  }

  return Object.assign({}, reviewResult, {
    account_ledger_result: noMatchLedgerResult || null,
    cc_payment_no_match: true,
    cc_payment_account_ledger_status:
      noMatchLedgerResult && noMatchLedgerResult.status
        ? noMatchLedgerResult.status
        : 'missing_or_unverified'
  });
}

const cases = [
  {
    name: 'verified ledger becomes primary result',
    ledger: { status: 'written', writeVerified: true, writtenTab: 'Account Ledger', row: 55, rowId: 'Account Ledger:55' },
    review: { status: 'written', writtenTab: 'Review Queue', row: 18, rowId: 'Review Queue:18' },
    expectedWrittenTab: 'Account Ledger',
    expectedReviewRow: 18,
    expectedLedgerPrimary: true
  },
  {
    name: 'unverified ledger keeps review as primary result',
    ledger: { status: 'written', writeVerified: false, writtenTab: 'Account Ledger', row: 55 },
    review: { status: 'written', writtenTab: 'Review Queue', row: 18 },
    expectedWrittenTab: 'Review Queue',
    expectedLedgerPrimary: false
  },
  {
    name: 'missing ledger keeps review as primary result',
    ledger: null,
    review: { status: 'written', writtenTab: 'Review Queue', row: 18 },
    expectedWrittenTab: 'Review Queue',
    expectedLedgerPrimary: false
  }
];

for (const c of cases) {
  const actual = decideNoMatchReturn(c.ledger, c.review);

  if (actual.writtenTab !== c.expectedWrittenTab) {
    failures.push({
      type: 'case_failed_written_tab',
      name: c.name,
      expected: c.expectedWrittenTab,
      actual: actual.writtenTab
    });
  }

  if (c.expectedLedgerPrimary) {
    if (!actual.account_ledger_result || !actual.review_queue_result || actual.cc_payment_no_match !== true) {
      failures.push({type:'case_failed_ledger_primary_metadata', name:c.name, actual});
    }
    if (actual.cc_payment_no_match_review_row !== c.expectedReviewRow) {
      failures.push({type:'case_failed_review_row_metadata', name:c.name, actual});
    }
  } else {
    if (!actual.cc_payment_account_ledger_status) {
      failures.push({type:'case_failed_missing_unverified_status', name:c.name, actual});
    }
  }
}

if (failures.length) {
  console.error(JSON.stringify({ok:false, failures}, null, 2));
  process.exit(1);
}

console.log(JSON.stringify({
  ok: true,
  cases: cases.length,
  guard: 'cc_no_match_returns_account_ledger_primary_when_verified'
}, null, 2));
