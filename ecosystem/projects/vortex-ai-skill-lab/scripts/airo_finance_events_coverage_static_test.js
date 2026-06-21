/**
 * AIRO Finance Events Coverage Static Test
 *
 * Verifies that the BCA/Blu wallet expense branch in writeRouted_ correctly
 * emits a Finance Events index row after a successful Account Ledger write.
 *
 * Scope: static source analysis only.
 * No runtime execution. No spreadsheet access. No Gmail. No deployment.
 *
 * Safety assertions:
 * - finance_write_performed: false for email paths (not touched)
 * - No Gmail trigger introduced
 * - No schema/header changes
 */

'use strict';

const fs = require('fs');
const path = require('path');

const GS_FILE = path.join(
  __dirname,
  'personal-workflow/apps-script/airo_finance_multitab_final_v1.gs'
);

let PASS = 0;
let FAIL = 0;
const FAILURES = [];

function assert(label, condition) {
  if (condition) {
    console.log('  PASS: ' + label);
    PASS++;
  } else {
    console.error('  FAIL: ' + label);
    FAIL++;
    FAILURES.push(label);
  }
}

function extractBcaBluBranch(src) {
  // Extract from the BCA/Blu guard through its closing brace
  const startMarker = "parsed.account === 'Blu' || parsed.account === 'BCA'";
  const startIdx = src.indexOf(startMarker);
  if (startIdx === -1) return null;
  // Walk back to the 'if (' that opens this block
  const ifIdx = src.lastIndexOf('if (', startIdx);
  if (ifIdx === -1) return null;
  // Walk forward to find the matching closing brace of this if block
  let depth = 0;
  let i = ifIdx;
  let blockStart = -1;
  while (i < src.length) {
    if (src[i] === '{') {
      if (depth === 0) blockStart = i;
      depth++;
    } else if (src[i] === '}') {
      depth--;
      if (depth === 0) {
        return src.slice(ifIdx, i + 1);
      }
    }
    i++;
  }
  return null;
}

console.log('\n=== AIRO Finance Events Coverage Static Test ===\n');

// --- Load source ---
let src;
try {
  src = fs.readFileSync(GS_FILE, 'utf8');
  console.log('Loaded: ' + GS_FILE);
  console.log('File size: ' + src.length + ' bytes\n');
} catch (e) {
  console.error('FATAL: Cannot read source file: ' + e.message);
  process.exit(1);
}

// --- Test 1: writeRouted_ function exists ---
console.log('--- Group 1: writeRouted_ function presence ---');
assert(
  'writeRouted_ function is defined in source',
  src.includes('function writeRouted_(')
);

// --- Test 2: BCA/Blu branch exists ---
console.log('\n--- Group 2: BCA/Blu branch existence ---');
const bcaBluGuard = "parsed.account === 'Blu' || parsed.account === 'BCA'";
assert(
  "BCA/Blu guard condition exists in writeRouted_",
  src.includes(bcaBluGuard)
);

const bcaBluBranch = extractBcaBluBranch(src);
assert(
  'BCA/Blu branch block could be extracted',
  bcaBluBranch !== null
);

// --- Test 3: Emission marker comment ---
console.log('\n--- Group 3: Finance Events emission marker ---');
assert(
  'AIRO_BCA_BLU_EXPENSE_FINANCE_EVENT_EMISSION_V1 marker present in source',
  src.includes('AIRO_BCA_BLU_EXPENSE_FINANCE_EVENT_EMISSION_V1')
);
if (bcaBluBranch) {
  assert(
    'AIRO_BCA_BLU_EXPENSE_FINANCE_EVENT_EMISSION_V1 marker is inside the BCA/Blu branch',
    bcaBluBranch.includes('AIRO_BCA_BLU_EXPENSE_FINANCE_EVENT_EMISSION_V1')
  );
}

// --- Test 4: recordFinanceEventForWriteResult_ call inside BCA/Blu branch ---
console.log('\n--- Group 4: recordFinanceEventForWriteResult_ call ---');
assert(
  'recordFinanceEventForWriteResult_ is defined in source',
  src.includes('function recordFinanceEventForWriteResult_(')
);
if (bcaBluBranch) {
  assert(
    'recordFinanceEventForWriteResult_ is called inside the BCA/Blu branch',
    bcaBluBranch.includes('recordFinanceEventForWriteResult_(')
  );
}

// --- Test 5: event_type: 'transaction_created' inside BCA/Blu branch ---
console.log('\n--- Group 5: event_type assertion ---');
if (bcaBluBranch) {
  assert(
    "BCA/Blu branch uses event_type: 'transaction_created'",
    bcaBluBranch.includes("event_type: 'transaction_created'")
  );
  assert(
    "BCA/Blu branch uses event_source: 'telegram'",
    bcaBluBranch.includes("event_source: 'telegram'")
  );
  assert(
    'BCA/Blu branch passes finalResult (not result) to recordFinanceEventForWriteResult_',
    bcaBluBranch.includes('recordFinanceEventForWriteResult_(ss, finalResult,')
  );
  assert(
    'BCA/Blu branch returns finalResult after Finance Events call',
    bcaBluBranch.includes('return finalResult;')
  );
}

// --- Test 6: No Gmail trigger / email write flags introduced in patch ---
console.log('\n--- Group 6: Email / Gmail safety (source-wide) ---');
// These should remain false-only string occurrences (not enabling calls)
const gmailTriggerCreateMatch = src.match(/ScriptApp\.newTrigger\([^)]*gmail/gi) || [];
assert(
  'No ScriptApp.newTrigger Gmail activation found in source',
  gmailTriggerCreateMatch.length === 0
);

// The BCA/Blu branch must not introduce any Gmail references
if (bcaBluBranch) {
  assert(
    'BCA/Blu branch does not reference Gmail',
    !bcaBluBranch.toLowerCase().includes('gmail')
  );
  assert(
    'BCA/Blu branch does not reference email write',
    !bcaBluBranch.toLowerCase().includes('email_write') &&
    !bcaBluBranch.toLowerCase().includes('finance_write_from_email')
  );
  assert(
    'BCA/Blu branch does not reference mail trigger',
    !bcaBluBranch.toLowerCase().includes('mail_trigger')
  );
}

// --- Test 7: No schema/header changes for subcategory / cashflow_class / domain ---
console.log('\n--- Group 7: Schema safety (no new header columns) ---');
// getFinanceEventsHeaders_ must NOT include subcategory, cashflow_class, or domain
// (unless they existed before this patch - we check the header builder function)
const headerFnStart = src.indexOf('function getFinanceEventsHeaders_()');
const headerFnEnd = src.indexOf('\n}', headerFnStart) + 2;
const headerFnBody = headerFnStart !== -1 ? src.slice(headerFnStart, headerFnEnd) : '';

// These are schema expansions that require explicit owner approval
// and must NOT be added by this patch
assert(
  'getFinanceEventsHeaders_ does not add cashflow_class column (schema guard)',
  !headerFnBody.includes('cashflow_class')
);
assert(
  'getFinanceEventsHeaders_ does not add domain column (schema guard)',
  !headerFnBody.includes("'domain'") && !headerFnBody.includes('"domain"')
);

// Verify writeAccountLedgerMirror_ signature not changed
assert(
  'writeAccountLedgerMirror_ function signature unchanged',
  src.includes('function writeAccountLedgerMirror_(ss, parsed, rawText, common, sourceTab)')
);

// Verify recordFinanceEventForWriteResult_ still guards on result.status === written
assert(
  "recordFinanceEventForWriteResult_ still guards on result.status !== 'written'",
  src.includes("result.status !== 'written'")
);

// --- Summary ---
console.log('\n=== RESULTS ===');
console.log('PASS: ' + PASS);
console.log('FAIL: ' + FAIL);
if (FAILURES.length > 0) {
  console.log('\nFailed assertions:');
  FAILURES.forEach(function(f) { console.log('  - ' + f); });
  process.exit(1);
} else {
  console.log('\nAll assertions passed. Finance Events coverage patch verified.');
  process.exit(0);
}
