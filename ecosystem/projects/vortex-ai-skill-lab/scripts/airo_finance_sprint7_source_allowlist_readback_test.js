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

  assert(text.includes("admin email sprint7 source allowlist"), `${rel} missing source allowlist command`);
  assert(text.includes("function airoSprint7SourceAllowlistDesign_"), `${rel} missing design function`);
  assert(text.includes("function airoSprint7SourceAllowlistReadbackText_"), `${rel} missing text function`);
  assert(text.includes("function airoSprint7SourceAllowlistMaybeHandleRoute_"), `${rel} missing route function`);
  assert(text.includes("function airoOriginalDoPostForSprint7SourceAllowlist_"), `${rel} missing doPost wrapper`);

  const blockMatch = text.match(/\/\* AIRO_SPRINT7_SOURCE_ALLOWLIST_READBACK_START \*\/([\s\S]*?)\/\* AIRO_SPRINT7_SOURCE_ALLOWLIST_READBACK_END \*\//);
  assert(blockMatch, `${rel} missing managed block`);
  const block = blockMatch[1];

  const requiredSnippets = [
    "mode: \"dry-run\"",
    "design_only: true",
    "write_performed: false",
    "email_ingestion_enabled: false",
    "email_default_off: true",
    "dry_run_only: true",
    "gmail_read_performed: false",
    "mailbox_read_performed: false",
    "mail_trigger_created: false",
    "finance_write_performed: false",
    "account_ledger_write_performed: false",
    "finance_events_write_performed: false",
    "review_queue_write_performed: false",
    "full_email_body_storage_allowed: false",
    "auto_write_allowed: false",
    "live_email_scan_allowed: false",
    "live_sender_approved: false",
    "live_allowlist_enabled: false",
    "wildcard_allowlist_allowed: false",
    "unknown_sender_parse_status: \"blocked_source_contract\"",
    "sensitive_priority_parse_status: \"skipped_sensitive\"",
    "allowlist_entry_count: 6",
    "allowlist_id: \"allow_bca_transaction_notification_design\"",
    "allowlist_id: \"allow_blu_transaction_notification_design\"",
    "allowlist_id: \"allow_credit_card_purchase_notification_design\"",
    "allowlist_id: \"allow_refund_reversal_notification_design\"",
    "allowlist_id: \"allow_failed_transaction_notification_design\"",
    "allowlist_id: \"block_otp_security_notification_design\"",
    "wildcard_all",
    "unknown_sender",
    "blocked_source_contract",
    "skipped_sensitive",
    "sender_not_allowlisted"
  ];

  for (const snippet of requiredSnippets) {
    assert(block.includes(snippet), `${rel} missing snippet ${snippet}`);
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
    assert(!block.includes(call), `${rel} managed block contains forbidden call ${call}`);
  }
}

const docPath = path.join(repo, "docs/AIRO_FINANCE_SPRINT7_SOURCE_ALLOWLIST_READBACK_COMMAND.md");
assert(fs.existsSync(docPath), "source allowlist readback doc missing");
const doc = fs.readFileSync(docPath, "utf8");

assert(doc.includes("admin email sprint7 source allowlist"), "doc missing command");
assert(doc.includes("RESULT=PASS_SPRINT7_SOURCE_ALLOWLIST_READBACK_COMMAND_IMPLEMENTED"), "doc missing result marker");
assert(doc.includes("Gmail read performed: false"), "doc missing gmail safety");
assert(doc.includes("Finance write performed: false"), "doc missing finance write safety");
assert(doc.includes("unknown sender parse_status: blocked_source_contract"), "doc missing unknown sender rule");
assert(doc.includes("sensitive priority parse_status: skipped_sensitive"), "doc missing sensitive priority rule");

console.log("RESULT_SOURCE_ALLOWLIST_READBACK_TEST=PASS");
console.log("COMMAND=admin email sprint7 source allowlist");
console.log("TESTED_TARGETS=" + targets.map((p) => path.relative(repo, p)).join(","));
