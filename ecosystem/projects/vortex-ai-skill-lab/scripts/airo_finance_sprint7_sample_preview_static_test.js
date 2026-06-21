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

assert(targets.length > 0, "no Apps Script target found");

for (const target of targets) {
  const text = fs.readFileSync(target, "utf8");
  const rel = path.relative(repo, target);

  assert(text.includes("function airoOriginalDoPostForSprint7SamplePreview_"), `${rel} original doPost wrapper missing`);
  assert(text.includes("function doPost(e)") || text.includes("function doPost("), `${rel} doPost wrapper missing`);
  assert(text.includes("admin email sprint7 sample preview"), `${rel} missing sample preview command`);
  assert(text.includes("function airoSprint7ManualSampleEmailPreview_"), `${rel} missing preview function`);
  assert(text.includes("function airoSprint7SamplePreviewMaybeHandleRoute_"), `${rel} missing route function`);

  const blockMatch = text.match(/\/\* AIRO_SPRINT7_MANUAL_SAMPLE_PREVIEW_START \*\/([\s\S]*?)\/\* AIRO_SPRINT7_MANUAL_SAMPLE_PREVIEW_END \*\//);
  assert(blockMatch, `${rel} missing managed block`);
  const block = blockMatch[1];

  const requiredSnippets = [
    "mode: \"dry-run\"",
    "write_performed: false",
    "email_ingestion_enabled: false",
    "email_default_off: true",
    "dry_run_only: true",
    "input_mode: \"manual sample text or mock payload only\"",
    "output_mode: \"preview object only\"",
    "live_email_scan_allowed: false",
    "auto_write_allowed: false",
    "gmail_read_performed: false",
    "mailbox_read_performed: false",
    "mail_trigger_created: false",
    "finance_write_performed: false",
    "account_ledger_write_performed: false",
    "finance_events_write_performed: false",
    "review_queue_write_performed: false",
    "full_email_body_storage_allowed: false",
    "sample_text_stored: false",
    "otp_security_hard_block_before_finance_parse: true",
    "source_message_id",
    "sender",
    "subject",
    "received_at",
    "merchant",
    "amount",
    "currency",
    "transaction_date",
    "payment_method",
    "category_guess",
    "confidence",
    "duplicate_key",
    "needs_review_reason",
    "skipped_sensitive"
  ];

  for (const snippet of requiredSnippets) {
    assert(block.includes(snippet), `${rel} missing required snippet ${snippet}`);
  }

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

console.log("RESULT_STATIC_TEST=PASS");
console.log("TESTED_TARGETS=" + targets.map((p) => path.relative(repo, p)).join(","));
