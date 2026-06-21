#!/usr/bin/env node
const fs = require('fs');

const srcPath = 'scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs';
const src = fs.readFileSync(srcPath, 'utf8');

function assertTrue(name, condition) {
  if (!condition) {
    console.error(`FAIL ${name}`);
    process.exitCode = 1;
  } else {
    console.log(`PASS ${name}`);
  }
}

assertTrue('7F-D status exists', src.includes('sprint7fd_email_answer_route_preview_no_write'));
assertTrue('7F-D helper exists', src.includes('function airoSprint7FDBuildNoWriteRoutePreview_'));
assertTrue('7F-D reply says no-write', src.includes('Sprint 7F-D: Route Preview') && src.includes('Mode: no-write'));
assertTrue('7F-D response returns route_preview', src.includes('route_preview_generated: true') && src.includes('route_preview: routePreview'));

const helperStart = src.indexOf('function airoSprint7FDBuildNoWriteRoutePreview_');
const helperEnd = src.indexOf('function airoSprint7FDRoutePreviewMessage_', helperStart);
const helperBlock = src.slice(helperStart, helperEnd);

[
  'writeRouted_',
  'GmailApp.',
  'ScriptApp.newTrigger',
  'createTrigger',
  'markRead',
  'moveToTrash'
].forEach(token => {
  assertTrue(`helper does not call ${token}`, !helperBlock.includes(token));
});

const responseStart = src.indexOf('status: updateResult.updated ? "sprint7fd_email_answer_route_preview_no_write"');
const responseBlock = src.slice(responseStart, responseStart + 1800);

[
  'finance_write_performed: false',
  'account_ledger_write_performed: false',
  'finance_events_write_performed: false',
  'review_queue_write_performed: false',
  'domain_tab_write_performed: false',
  'write_allowed: false',
  'write_approved: false',
  'write_performed: false'
].forEach(token => {
  assertTrue(`response has ${token}`, responseBlock.includes(token));
});

if (process.exitCode) process.exit(process.exitCode);
console.log('RESULT_SPRINT7FD_STATIC=PASS');
