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

for (const rel of sourcePaths) {
  const text = read(rel);
  const block = extractFunction(text, "runSprint7GManualWritePilotFromEditor");

  assert(block.includes("review:emc:19e7da2619bb892e"), `${rel} missing idempotency key`);
  assert(block.includes("appendByHeader_"), `${rel} missing appendByHeader_`);
  assert(!block.includes("GmailApp"), `${rel} calls GmailApp`);
  assert(!block.includes("ScriptApp.newTrigger"), `${rel} calls ScriptApp.newTrigger`);
  assert(!block.includes("writeRouted_"), `${rel} calls writeRouted_`);
  assert(!block.includes("writeAccountLedgerMirror_"), `${rel} calls writeAccountLedgerMirror_`);
  assert(!block.includes("writeFinanceEvent_"), `${rel} calls writeFinanceEvent_`);
  assert(block.includes("airoEnsureDateObject_"), `${rel} missing date normalization helper`);
  assert(block.includes("received_at"), `${rel} missing received_at fallback checking`);
  assert(block.includes("created_at"), `${rel} missing created_at fallback checking`);
  assert(block.includes("isAlreadyCommitted"), `${rel} missing isAlreadyCommitted check`);

  const requiredSafetyFlags = [
    "gmail_read_performed: false",
    "gmail_modified: false",
    "mail_trigger_created: false",
    "account_ledger_write_performed: false",
    "finance_events_write_performed: false",
    "domain_tab_write_performed: false"
  ];

  for (const flag of requiredSafetyFlags) {
    assert(block.includes(flag), `${rel} missing safety flag: ${flag}`);
  }
  assert(text.includes("function runSprint7GTask5TargetedReadbackVerifierFromEditor"), `${rel} missing runSprint7GTask5TargetedReadbackVerifierFromEditor`);
}

console.log("RESULT_SPRINT7G_STATIC_TEST=PASS");
console.log("FUNCTION=runSprint7GManualWritePilotFromEditor");
console.log("STATUS=ready");
