#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const srcPath = path.join(root, 'apps-script-prod-v2', 'AIRO_Finance_Multitab_Final_v1.js');
const src = fs.readFileSync(srcPath, 'utf8');

function assert(condition, message) {
  if (!condition) {
    console.error(JSON.stringify({ ok: false, error: message }, null, 2));
    process.exit(1);
  }
}

function sheetName(key, fallback) {
  const re = new RegExp(key + "\\s*:\\s*'([^']+)'");
  const m = src.match(re);
  return m ? m[1] : fallback;
}

const accountLedger = sheetName('accountLedger', '📒 Account Ledger');

const buildStart = src.indexOf('function airoSprint6DashboardV2Build_');
assert(buildStart >= 0, 'Dashboard V2 builder function missing');

const readbackStart = src.indexOf('function airoSprint6DashboardV2Readback_', buildStart);
const block = src.slice(buildStart, readbackStart > buildStart ? readbackStart : buildStart + 14000);

const forbidden = [
  /SUMIFS\('[^']*Finance Events'!/i,
  /COUNTIFS\('[^']*Finance Events'!/i,
  /Finance Events domain set/i,
  /Finance Events tanpa domain ref/i,
  /FinanceEvents,\s*category/i,
  /Transactions/i
];

for (const re of forbidden) {
  assert(!re.test(block), `Dashboard V2 builder still has forbidden dependency: ${re}`);
}

assert(block.includes(`SUMIFS('${accountLedger}'!E:E`), 'Dashboard V2 does not use Account Ledger amount_out column E');
assert(block.includes(`'${accountLedger}'!H:H`), 'Dashboard V2 does not use Account Ledger category column H');
assert(block.includes(`'${accountLedger}'!B:B`), 'Dashboard V2 does not use Account Ledger date column B');
assert(/Account Ledger category set/i.test(block), 'Dashboard V2 quality label does not mention Account Ledger category set');

const feNoOp = src.indexOf('function writeFinanceEvent_');
assert(feNoOp >= 0, 'Finance Events no-op/deprecation guard function missing');
const feBlock = src.slice(feNoOp, feNoOp + 1200);
assert(/deprecated|finance_events_write_performed\s*:\s*false/i.test(feBlock), 'Finance Events no-op/deprecation guard not visible');

console.log(JSON.stringify({
  ok: true,
  guard: 'task9_dashboard_migration_away_from_finance_events',
  accountLedger,
  checks: [
    'no Finance Events SUMIFS in Dashboard V2 builder',
    'no Finance Events COUNTIFS in Dashboard V2 builder',
    'Account Ledger amount_out/category/date formulas present',
    'Finance Events remains deprecated/no-op',
    'Transactions not recreated'
  ]
}, null, 2));
