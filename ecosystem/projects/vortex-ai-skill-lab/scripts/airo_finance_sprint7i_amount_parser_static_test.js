
const fs = require('fs');

const sourcePath = 'apps-script-prod-v2/AIRO_Finance_Multitab_Final_v1.js';
const source = fs.readFileSync(sourcePath, 'utf8');

function extractFunction(name) {
  const re = new RegExp('function\\s+' + name + '\\s*\\(');
  const m = re.exec(source);
  if (!m) throw new Error('Function not found: ' + name);
  const start = m.index;
  const brace = source.indexOf('{', start);
  let depth = 0;
  for (let i = brace; i < source.length; i++) {
    const ch = source[i];
    if (ch === '{') depth++;
    if (ch === '}') depth--;
    if (depth === 0) return source.slice(start, i + 1);
  }
  throw new Error('Function end not found: ' + name);
}

const code = [
  extractFunction('sanitizeAmountExtractionText_'),
  extractFunction('parseAmount_'),
  extractFunction('extractHumanAmountFromText_'),
  extractFunction('amountForIntent_'),
  `
  const cases = [
    ['bayar cc 9021 dari blu SMK_T9_CC_PAY_LEDGER_20260612_170925', 9021],
    ['bayar cc 9021 dari blu SMK_T9_CC_PAY_LEDGER_20260611_205927', 9021],
    ['bca keluar 25000 kopi SMK_T9_BCA_20260611_123456', 25000],
    ['bca keluar 25000 kue SMK_T9_BCA_20260611_123456', 25000],
    ['transfer 50000 dari bca ke blu SMK_T9_TRANSFER_20260611_123456', 50000],
    ['cc 75000 tokopedia skincare SMK_T9_CC_PURCHASE_20260611_123456', 75000],
    ['Rp125000', 125000],
    ['bayar cc 9.021 dari blu SMK_T9_CC_PAY_LEDGER_20260611_205927', 9021],
    ['bca keluar 25rb kopi SMK_T9_BCA_20260611_123456', 25000]
  ];

  const forbidden = [20260612, 20260611, 170925, 205927, 123456, 25000000];

  const failures = [];
  for (const [input, expected] of cases) {
    const parsed = parseAmount_(input);
    const extracted = extractHumanAmountFromText_(input);
    const intentZero = amountForIntent_({amount: 0}, input);
    const intentParsed = amountForIntent_({amount: parsed}, input);

    if (parsed !== expected) failures.push({input, fn:'parseAmount_', expected, actual: parsed});
    if (extracted !== expected) failures.push({input, fn:'extractHumanAmountFromText_', expected, actual: extracted});
    if (intentZero !== expected) failures.push({input, fn:'amountForIntent_zero', expected, actual: intentZero});
    if (intentParsed !== expected) failures.push({input, fn:'amountForIntent_parsed', expected, actual: intentParsed});

    for (const bad of forbidden) {
      if (parsed === bad && bad !== expected) failures.push({input, fn:'parseAmount_forbidden', bad});
      if (extracted === bad && bad !== expected) failures.push({input, fn:'extractHumanAmount_forbidden', bad});
      if (intentZero === bad && bad !== expected) failures.push({input, fn:'amountForIntent_forbidden', bad});
    }
  }

  if (failures.length) {
    console.error(JSON.stringify({ok:false, failures}, null, 2));
    process.exit(1);
  }

  console.log(JSON.stringify({
    ok: true,
    cases: cases.length,
    functions: ['sanitizeAmountExtractionText_', 'parseAmount_', 'extractHumanAmountFromText_', 'amountForIntent_']
  }, null, 2));
  `
].join('\n\n');

eval(code);
