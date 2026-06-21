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

const saveStart = src.indexOf('function airoSprint7FSavePendingPointer_');
const saveEnd = src.indexOf('function runSprint7FSendOneClarificationAndLogPendingFromEditor', saveStart);
const saveBlock = src.slice(saveStart, saveEnd);

pass('stable amount helper exists', src.includes('function airoSprint7FDStableCandidateAmount_'));
pass('pending pointer stores display_amount', saveBlock.includes('display_amount: airoSprint7FDStableCandidateAmount_(candidate, logResult)'));
pass('pending pointer stores detected_amount', saveBlock.includes('detected_amount: airoSprint7FDStableCandidateAmount_(candidate, logResult)'));
pass('pending pointer stores amount_idr', saveBlock.includes('amount_idr: airoSprint7FDStableCandidateAmount_(candidate, logResult)'));
pass('pending pointer stores amount_source', saveBlock.includes('amount_source:'));
pass('route preview still no-write', src.includes('sprint7fd_email_answer_route_preview_no_write'));
pass('route preview safety finance false', src.includes('finance_write_performed: false'));
pass('no Gmail trigger created in patch helper', !src.slice(src.indexOf('function airoSprint7FDStableCandidateAmount_'), src.indexOf('function airoSprint7FSavePendingPointer_')).includes('ScriptApp.newTrigger'));
pass('no Gmail mutation in patch helper', !src.slice(src.indexOf('function airoSprint7FDStableCandidateAmount_'), src.indexOf('function airoSprint7FSavePendingPointer_')).includes('GmailApp.'));

const wrapperStart = src.indexOf('function aaRun7FD()');
pass('aaRun7FD wrapper exists', wrapperStart !== -1);
if (wrapperStart !== -1) {
  const wrapperEnd = src.indexOf('}', wrapperStart);
  const wrapperBlock = src.slice(wrapperStart, wrapperEnd + 1);
  const wrapperNormalized = wrapperBlock.replace(/\s+/g, ' ').trim();
  pass('aaRun7FD calls only expected function', wrapperNormalized === 'function aaRun7FD() { return runSprint7FSendOneClarificationAndLogPendingFromEditor(); }');
}

if (process.exitCode) process.exit(process.exitCode);
console.log('RESULT_SPRINT7FD_AMOUNT_POINTER_STATIC=PASS');
