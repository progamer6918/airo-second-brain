const fs = require("fs");
const path = require("path");

const repo = "/home/egitaristorandas/vortex-ai-skill-lab";
const targets = [
  "scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs",
  "apps-script-prod-v2/AIRO_Finance_Multitab_Final_v1.js",
].map((p) => path.join(repo, p)).filter((p) => fs.existsSync(p));

function assert(condition, message) {
  if (!condition) {
    console.error("ASSERT_FAIL=" + message);
    process.exit(1);
  }
}

function assertOrder(text, before, after, label) {
  const beforeIdx = text.indexOf(before);
  const afterIdx = text.indexOf(after);

  assert(beforeIdx >= 0, `${label} missing before snippet ${before}`);
  assert(afterIdx >= 0, `${label} missing after snippet ${after}`);
  assert(beforeIdx < afterIdx, `${label} order invalid: ${before} must appear before ${after}`);
}

assert(targets.length > 0, "no Apps Script target found");

for (const target of targets) {
  const text = fs.readFileSync(target, "utf8");
  const rel = path.relative(repo, target);

  const fnMatch = text.match(/function airoSprint7ManualSampleEmailPreview_\([\s\S]*?\n\}/);
  assert(fnMatch, `${rel} preview function missing`);
  const fn = fnMatch[0];

  assert(fn.includes("var sensitiveKeyword = airoSprint7SamplePreviewHasSensitiveKeyword_(sampleText);"), `${rel} missing early sensitive keyword`);
  assert(fn.includes("if (sensitiveKeyword)"), `${rel} missing sensitive early return branch`);
  assert(fn.includes("finance_parser_skipped_due_to_sensitive: true"), `${rel} missing sensitive skip flag true`);
  assert(fn.includes("finance_parser_skipped_due_to_sensitive: false"), `${rel} missing normal skip flag false`);

  assertOrder(fn, "if (sensitiveKeyword)", "var amount = airoSprint7SamplePreviewExtractAmount_(sampleText);", `${rel} sensitive branch must be before amount extraction`);
  assertOrder(fn, "if (sensitiveKeyword)", "var merchant = airoSprint7SamplePreviewExtractMerchant_(sampleText);", `${rel} sensitive branch must be before merchant extraction`);
  assertOrder(fn, "if (sensitiveKeyword)", "var paymentMethod = airoSprint7SamplePreviewExtractPaymentMethod_(sampleText);", `${rel} sensitive branch must be before payment method extraction`);

  const sensitiveBranch = fn.slice(fn.indexOf("if (sensitiveKeyword)"), fn.indexOf("var amount = airoSprint7SamplePreviewExtractAmount_(sampleText);"));

  const requiredSensitiveSnippets = [
    "amount: 0",
    'currency: ""',
    'payment_method: ""',
    'merchant: ""',
    'category_guess: ""',
    "confidence: 0",
    'parse_status: "skipped_sensitive"',
    '"skipped_sensitive"',
    '"blocked_keyword_" + sensitiveKeyword',
    "write_performed: false",
    "email_ingestion_enabled: false",
    "gmail_read_performed: false",
    "mailbox_read_performed: false",
    "mail_trigger_created: false",
    "finance_write_performed: false",
    "account_ledger_write_performed: false",
    "finance_events_write_performed: false",
    "review_queue_write_performed: false",
    "full_email_body_storage_allowed: false",
    "sample_text_stored: false"
  ];

  for (const snippet of requiredSensitiveSnippets) {
    assert(sensitiveBranch.includes(snippet), `${rel} sensitive branch missing ${snippet}`);
  }

  const blockMatch = text.match(/\/\* AIRO_SPRINT7_MANUAL_SAMPLE_PREVIEW_START \*\/([\s\S]*?)\/\* AIRO_SPRINT7_MANUAL_SAMPLE_PREVIEW_END \*\//);
  assert(blockMatch, `${rel} missing managed block`);
  const block = blockMatch[1];

  const forbiddenCalls = [
    "GmailApp.",
    "MailApp.",
    "ScriptApp.newTrigger",
    ".appendRow(",
    ".setValues(",
    ".setValue(",
    ".markRead(",
    ".moveToTrash("
  ];

  for (const call of forbiddenCalls) {
    assert(!block.includes(call), `${rel} managed block contains forbidden live/write call ${call}`);
  }
}

console.log("RESULT_SENSITIVE_HARDBLOCK_TEST=PASS");
console.log("EXPECTED_NEGATIVE_AMOUNT=0");
console.log("EXPECTED_NEGATIVE_PAYMENT_METHOD=BLANK");
console.log("EXPECTED_NEGATIVE_STATUS=skipped_sensitive");
console.log("TESTED_TARGETS=" + targets.map((p) => path.relative(repo, p)).join(","));
