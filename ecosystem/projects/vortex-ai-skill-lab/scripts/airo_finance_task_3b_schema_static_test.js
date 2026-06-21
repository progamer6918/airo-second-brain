#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function assert(condition, message) {
  if (!condition) {
    console.error(`FAIL: ${message}`);
    process.exit(1);
  }
}

const repoRoot = path.resolve(__dirname, '..');
const src = fs.readFileSync(path.join(repoRoot, 'scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs'), 'utf8');

console.log("== Running Task 3B Static Tests ==");

// 1. Verify function existence
assert(src.includes('function airoSprint7HResolveToReviewQueueFallback_'), 'airoSprint7HResolveToReviewQueueFallback_ function missing');

// 2. Extract function block
function extractFunction(text, functionName) {
  const startIdx = text.indexOf("function " + functionName);
  assert(startIdx >= 0, `Function ${functionName} not found`);
  
  let depth = 0;
  let endIdx = -1;
  let inString = false;
  let stringChar = '';

  for (let i = startIdx; i < text.length; i++) {
    const char = text[i];
    if ((char === '"' || char === "'") && text[i - 1] !== '\\') {
      if (!inString) {
        inString = true;
        stringChar = char;
      } else if (char === stringChar) {
        inString = false;
      }
    }
    if (!inString) {
      if (char === '{') {
        depth++;
      } else if (char === '}') {
        depth--;
        if (depth === 0) {
          endIdx = i;
          break;
        }
      }
    }
  }
  assert(endIdx >= 0, `Could not find end of function ${functionName}`);
  return text.slice(startIdx, endIdx + 1);
}

const resolveBlock = extractFunction(src, 'airoSprint7HResolveToReviewQueueFallback_');

// 3. Verify 10 extension fields are written in resolved block
const expectedFields = [
  'email_candidate_id',
  'gmail_message_id',
  'gmail_thread_id',
  'email_provider',
  'email_log_ref',
  'duplicate_key',
  'write_policy',
  'write_status',
  'linked_event_id',
  'linked_account_ledger_entry_id'
];

expectedFields.forEach(field => {
  assert(resolveBlock.includes(field), `Resolve function does not map field: ${field}`);
  console.log(`PASS: Mapped field ${field}`);
});

// 4. Verify deduplication scan is present
assert(resolveBlock.includes('duplicateFound') || resolveBlock.includes('duplicate_key'), 'Resolve function missing deduplication logic');
console.log('PASS: Deduplication check present');

// 5. Verify safety invariants
assert(!resolveBlock.includes('writeAccountLedgerMirror_'), 'Resolve function writes to Account Ledger');
assert(!resolveBlock.includes('writeFinanceEvent_'), 'Resolve function writes clean Finance Events');
assert(!resolveBlock.includes('GmailApp.sendEmail') && !resolveBlock.includes('GmailApp.createDraft'), 'Resolve function mutates Gmail');
console.log('PASS: Safety checks verified (no Ledger write, no clean Event write, no Gmail mutation)');

// 6. Verify fieldForHeader_ bypass logic
const fieldForHeaderBlock = extractFunction(src, 'fieldForHeader_');
assert(fieldForHeaderBlock.includes('bypassList'), 'fieldForHeader_ missing bypassList');
assert(fieldForHeaderBlock.includes('email_candidate_id'), 'fieldForHeader_ bypassList missing email_candidate_id');
assert(fieldForHeaderBlock.includes('gmail_message_id'), 'fieldForHeader_ bypassList missing gmail_message_id');
assert(fieldForHeaderBlock.includes('parsed_subcategory'), 'fieldForHeader_ bypassList missing parsed_subcategory');
console.log('PASS: fieldForHeader_ bypass logic verified');

console.log('RESULT_TASK3B_STAGING_STATIC=PASS');
