const fs = require("fs");
const path = require("path");

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

const repoRoot = path.resolve(__dirname, "..");
const sourcePaths = [
  "scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs",
  "apps-script-prod-v2/AIRO_Finance_Multitab_Final_v1.js",
];

function read(rel) {
  const abs = path.join(repoRoot, rel);
  assert(fs.existsSync(abs), `${rel} missing`);
  return fs.readFileSync(abs, "utf8");
}

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

// Test amount normalization behavior
function testNormalization(normFnText) {
  // Create a executable function from the text
  const cleanFnText = normFnText.replace(/function airoSprint7GNormalizeAmountForReadback_/, "function normalize");
  const fn = new Function(`
    ${cleanFnText}
    return normalize(arguments[0]);
  `);

  const testCases = [
    { input: 336541, expected: 336541 },
    { input: "336541", expected: 336541 },
    { input: "Rp336.541", expected: 336541 },
    { input: "Rp 336.541", expected: 336541 },
    { input: "336.541", expected: 336541 },
    { input: "Rp 336.541,00", expected: 336541 },
    { input: "336,541.00", expected: 336541 },
    { input: "", expected: 0 },
    { input: null, expected: 0 },
  ];

  for (const tc of testCases) {
    const res = fn(tc.input);
    assert(res === tc.expected, `Normalization failed for: ${tc.input}. Expected ${tc.expected}, got ${res}`);
  }
}

for (const rel of sourcePaths) {
  const text = read(rel);
  
  // Verify verifier function exists
  const verifierBlock = extractFunction(text, "runSprint7GReviewQueueReadbackVerifierFromEditor");
  
  // Verify normalization function exists and passes tests
  const normBlock = extractFunction(text, "airoSprint7GNormalizeAmountForReadback_");
  testNormalization(normBlock);

  // Safety checks on verifier
  assert(verifierBlock.includes("review:emc:19e7da2619bb892e"), `${rel} verifier missing target key`);
  assert(!verifierBlock.includes("appendByHeader_"), `${rel} verifier calls appendByHeader_`);
  assert(!verifierBlock.includes("GmailApp"), `${rel} verifier calls GmailApp`);
  assert(!verifierBlock.includes("ScriptApp.newTrigger"), `${rel} verifier calls ScriptApp.newTrigger`);
  assert(!verifierBlock.includes("writeRouted_"), `${rel} verifier calls writeRouted_`);
  assert(!verifierBlock.includes("writeAccountLedgerMirror_"), `${rel} verifier calls writeAccountLedgerMirror_`);
  assert(!verifierBlock.includes("writeFinanceEvent_"), `${rel} verifier calls writeFinanceEvent_`);

  const requiredSafetyFlags = [
    "write_performed: false",
    "gmail_read_performed: false",
    "gmail_modified: false",
    "mail_trigger_created: false",
    "account_ledger_write_performed: false",
    "finance_events_write_performed: false",
    "review_queue_write_performed: false",
    "domain_tab_write_performed: false"
  ];

  for (const flag of requiredSafetyFlags) {
    assert(verifierBlock.includes(flag), `${rel} verifier missing safety flag: ${flag}`);
  }
}

console.log("RESULT_SPRINT7G_READBACK_VERIFIER_STATIC_TEST=PASS");
console.log("FUNCTION=runSprint7GReviewQueueReadbackVerifierFromEditor");
console.log("STATUS=ready");
