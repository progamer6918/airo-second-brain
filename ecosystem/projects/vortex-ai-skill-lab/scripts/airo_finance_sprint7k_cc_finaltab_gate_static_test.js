
const fs = require('fs');

const sourcePath = 'apps-script-prod-v2/AIRO_Finance_Multitab_Final_v1.js';
const source = fs.readFileSync(sourcePath, 'utf8');

const required = [
  'AIRO_TASK9_CC_PAYMENT_INTENT_BYPASS_GENERIC_CATEGORY_REVIEW_V1',
  'const clearCreditCardPaymentRoute =',
  'isCreditCardPaymentText_(effectiveRawText)',
  "canonicalSheetName_(plannedTab).includes('credit card')",
  'Number(parsed && parsed.amount ? parsed.amount : 0) > 0',
  "String((parsed && parsed.account) || '').trim().toLowerCase() !== 'unknown'",
  'const finalTab = (parsed.needsReview && !clearCreditCardPaymentRoute)'
];

const failures = [];
for (const needle of required) {
  if (!source.includes(needle)) failures.push({type:'missing_source_marker', needle});
}

function canonicalSheetName_(name) {
  return String(name || '')
    .toLowerCase()
    .replace(/[^\w\s]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function isCreditCardPaymentText_(text) {
  const t = String(text || '').toLowerCase().trim();
  return (
    /^bayar\s+cc\b/i.test(t) ||
    /^bayar\s+tagihan\b.*\b(cc|credit card|kartu kredit|tokopedia cc|tokopedia card)\b/i.test(t)
  );
}

const AIRO_CONFIG = { tabs: { review: '🧾 Review Queue', creditCard: '💳 Credit Card' } };

function decideFinalTab(parsed, rawText, plannedTab) {
  const clearCreditCardPaymentRoute =
    isCreditCardPaymentText_(rawText) &&
    canonicalSheetName_(plannedTab).includes('credit card') &&
    Number(parsed && parsed.amount ? parsed.amount : 0) > 0 &&
    Boolean(String((parsed && parsed.account) || '').trim()) &&
    String((parsed && parsed.account) || '').trim().toLowerCase() !== 'unknown';

  const finalTab = (parsed.needsReview && !clearCreditCardPaymentRoute)
    ? AIRO_CONFIG.tabs.review
    : plannedTab;

  return { clearCreditCardPaymentRoute: Boolean(clearCreditCardPaymentRoute), finalTab };
}

const cases = [
  {
    name: 'clear cc payment bypasses generic review',
    parsed: { needsReview: true, amount: 9021, account: 'Blu' },
    rawText: 'bayar cc 9021 dari blu SMK_T9_CC_PAY_LEDGER_20260612_220244',
    plannedTab: '💳 Credit Card',
    expectedFinalTab: '💳 Credit Card',
    expectedBypass: true
  },
  {
    name: 'cc payment missing account stays review',
    parsed: { needsReview: true, amount: 9021, account: 'Unknown' },
    rawText: 'bayar cc 9021',
    plannedTab: '💳 Credit Card',
    expectedFinalTab: '🧾 Review Queue',
    expectedBypass: false
  },
  {
    name: 'cc payment missing amount stays review',
    parsed: { needsReview: true, amount: 0, account: 'Blu' },
    rawText: 'bayar cc dari blu',
    plannedTab: '💳 Credit Card',
    expectedFinalTab: '🧾 Review Queue',
    expectedBypass: false
  },
  {
    name: 'non cc reviewed transaction stays review',
    parsed: { needsReview: true, amount: 25000, account: 'BCA' },
    rawText: 'bca keluar 25000 kopi',
    plannedTab: '📒 Account Ledger',
    expectedFinalTab: '🧾 Review Queue',
    expectedBypass: false
  },
  {
    name: 'non reviewed planned tab remains planned',
    parsed: { needsReview: false, amount: 25000, account: 'BCA' },
    rawText: 'bca keluar 25000 kopi',
    plannedTab: '📒 Account Ledger',
    expectedFinalTab: '📒 Account Ledger',
    expectedBypass: false
  }
];

for (const c of cases) {
  const actual = decideFinalTab(c.parsed, c.rawText, c.plannedTab);
  if (actual.finalTab !== c.expectedFinalTab || actual.clearCreditCardPaymentRoute !== c.expectedBypass) {
    failures.push({
      type: 'case_failed',
      name: c.name,
      expectedFinalTab: c.expectedFinalTab,
      actualFinalTab: actual.finalTab,
      expectedBypass: c.expectedBypass,
      actualBypass: actual.clearCreditCardPaymentRoute
    });
  }
}

if (failures.length) {
  console.error(JSON.stringify({ok:false, failures}, null, 2));
  process.exit(1);
}

console.log(JSON.stringify({
  ok: true,
  cases: cases.length,
  guard: 'cc_payment_intent_bypasses_generic_category_review_only_when_clear'
}, null, 2));
