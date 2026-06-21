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

  assert(text.includes("function airoOriginalDoPostForSprint7ParserPlan_"), `${rel} original doPost wrapper missing`);
  assert(text.includes("function doPost(e)") || text.includes("function doPost("), `${rel} doPost wrapper missing`);
  assert(text.includes("admin email sprint7 parser plan"), `${rel} missing parser plan command`);
  assert(text.includes("function airoSprint7DryRunParserPlan_"), `${rel} missing parser plan function`);
  assert(text.includes("function airoAdminEmailSprint7ParserPlan_"), `${rel} missing admin function`);
  assert(text.includes("function airoSprint7ParserPlanMaybeHandleRoute_"), `${rel} missing route function`);

  const blockMatch = text.match(/\/\* AIRO_SPRINT7_DRY_RUN_PARSER_PLAN_RECOVERY_START \*\/([\s\S]*?)\/\* AIRO_SPRINT7_DRY_RUN_PARSER_PLAN_RECOVERY_END \*\//);
  assert(blockMatch, `${rel} missing recovery managed block`);
  const block = blockMatch[1];

  const requiredSnippets = [
    "mode: \"dry-run\"",
    "write_performed: false",
    "email_ingestion_enabled: false",
    "email_default_off: true",
    "dry_run_only: true",
    "manual_sample_or_mock_payload_only: true",
    "mailbox_read_performed: false",
    "mail_trigger_created: false",
    "finance_write_performed: false",
    "account_ledger_write_performed: false",
    "finance_events_write_performed: false",
    "review_queue_write_performed: false",
    "full_email_body_storage_allowed: false",
    "message_modification_allowed: false",
    "auto_post_threshold_enabled: false",
    "duplicate_detection_required_before_write: true",
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
    "manual sample email preview command only"
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
