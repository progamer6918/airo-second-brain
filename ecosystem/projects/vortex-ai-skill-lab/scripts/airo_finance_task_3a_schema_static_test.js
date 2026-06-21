#!/usr/bin/env node
const fs = require('fs');

const src = fs.readFileSync('scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs', 'utf8');

function pass(name, ok) {
  if (!ok) {
    console.error(`FAIL ${name}`);
    process.exitCode = 1;
  } else {
    console.log(`PASS ${name}`);
  }
}

// 1. Helper function existence
pass('extendReviewQueueSchema_ exists', src.includes('function extendReviewQueueSchema_('));
pass('runTask3AReviewQueueSchemaExtensionFromEditor exists', src.includes('function runTask3AReviewQueueSchemaExtensionFromEditor('));
pass('runTask3AReviewQueueSchemaVerifierFromEditor exists', src.includes('function runTask3AReviewQueueSchemaVerifierFromEditor('));

// 2. Schema check integration exists
pass('airoLiveSchemaVerifyOnly checks Review Queue schema', src.includes('reviewQueueSchemaStatus'));
pass('airoLiveSchemaVerifyOnly includes reviewQueueSchemaStatus in return', src.includes('reviewQueueSchemaStatus: reviewQueueSchemaStatus'));

// 3. Targets all 10 extension fields
const targetExtensions = [
  "email_candidate_id",
  "gmail_message_id",
  "gmail_thread_id",
  "email_provider",
  "email_log_ref",
  "duplicate_key",
  "write_policy",
  "write_status",
  "linked_event_id",
  "linked_account_ledger_entry_id"
];

targetExtensions.forEach(ext => {
  pass(`Schema contains extension field: ${ext}`, src.includes(`"${ext}"`) || src.includes(`'${ext}'`));
});

// 4. Safety verifications (no write, no triggers, no gmail mutations in schema helper)
const schemaStart = src.indexOf('function extendReviewQueueSchema_()');
const schemaEnd = src.indexOf('function runTask3AReviewQueueSchemaExtensionFromEditor()');
const schemaBlock = src.slice(schemaStart, schemaEnd);

pass('schema helper does not perform Account Ledger writes', !schemaBlock.includes('writeAccountLedgerMirror_'));
pass('schema helper does not perform Finance Events writes', !schemaBlock.includes('writeFinanceEvent_'));
pass('schema helper does not perform Gmail mutations', !schemaBlock.includes('GmailApp.'));
pass('schema helper does not install scheduled triggers', !schemaBlock.includes('ScriptApp.newTrigger'));

if (process.exitCode) process.exit(process.exitCode);
console.log('RESULT_TASK3A_SCHEMA_STATIC=PASS');
