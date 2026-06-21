const fs = require("fs");
const path = require("path");

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
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

function extractBlock(text, rel) {
  const start = "// AIRO_SPRINT7_EMAIL_CLARIFICATION_BRIDGE_READBACK_START";
  const end = "// AIRO_SPRINT7_EMAIL_CLARIFICATION_BRIDGE_READBACK_END";
  const s = text.indexOf(start);
  const e = text.indexOf(end);
  assert(s >= 0, `${rel} missing clarification bridge start marker`);
  assert(e > s, `${rel} missing clarification bridge end marker`);
  return text.slice(s, e + end.length);
}

for (const rel of sourcePaths) {
  const text = read(rel);
  const block = extractBlock(text, rel);

  assert(text.includes("sprint7EmailClarificationBridgeResult"), `${rel} missing doPost clarification bridge route`);
  assert(block.includes("admin email sprint7 clarification bridge"), `${rel} missing command`);
  assert(block.includes("email_clarification_bridge_design_ready"), `${rel} missing status`);
  assert(block.includes("sendTelegram_"), `${rel} missing telegram reply path`);
  assert(block.includes("telegramReplyAttempted"), `${rel} missing telegram reply tracking`);

  const safeFields = [
    "provider_or_source_name",
    "detected_amount",
    "detected_date",
    "merchant_or_counterparty",
    "card_last4",
    "detected_direction",
    "detected_transaction_status",
    "candidate_reference_id",
    "short_action_options",
  ];

  for (const field of safeFields) {
    assert(block.includes(`"${field}"`), `${rel} missing safe prompt field ${field}`);
  }

  const forbiddenFields = [
    "full_email_body",
    "otp_code",
    "auth_code",
    "password_reset_link",
    "login_link",
    "security_link",
    "full_card_number",
    "full_account_number",
    "unredacted_sensitive_email_content",
    "raw_email_headers",
    "raw_email_body",
  ];

  for (const field of forbiddenFields) {
    assert(block.includes(`"${field}"`), `${rel} missing forbidden prompt field ${field}`);
  }

  const clarificationTypes = [
    "email_missing_category",
    "email_direction_ambiguous",
    "email_source_account_missing",
    "email_destination_account_missing",
    "email_status_unclear",
    "email_cc_purchase_vs_payment",
    "email_refund_vs_income",
    "email_failed_vs_success",
    "email_transfer_internal_vs_expense",
    "email_merchant_unclear",
    "email_duplicate_possible",
    "email_low_confidence_parse",
  ];

  for (const type of clarificationTypes) {
    assert(block.includes(`"${type}"`), `${rel} missing clarification type ${type}`);
  }

  const requiredFlags = [
    "write_performed: false",
    "email_ingestion_enabled: false",
    "email_default_off: true",
    "dry_run_only: true",
    "gmail_read_performed: false",
    "mailbox_read_performed: false",
    "gmail_modified: false",
    "mail_trigger_created: false",
    "full_email_body_stored: false",
    "sensitive_content_stored: false",
    "telegram_security_content_forwarded: false",
    "raw_email_forwarded_to_telegram: false",
    "finance_write_performed: false",
    "account_ledger_write_performed: false",
    "finance_events_write_performed: false",
    "review_queue_write_performed: false",
    "domain_tab_write_performed: false",
  ];

  for (const flag of requiredFlags) {
    assert(block.includes(flag), `${rel} missing safety flag ${flag}`);
  }

  const forbiddenRuntimeCalls = [
    "GmailApp",
    "MailApp",
    "SpreadsheetApp",
    "getInboxThreads",
    "markRead",
    "moveTo",
    "createLabel",
    "addLabel",
    "removeLabel",
    "." + "delete",
  ];

  for (const forbidden of forbiddenRuntimeCalls) {
    assert(!block.includes(forbidden), `${rel} clarification bridge block contains forbidden runtime call ${forbidden}`);
  }
}

const docPath = path.join(repoRoot, "docs/AIRO_FINANCE_SPRINT7_EMAIL_CLARIFICATION_BRIDGE_READBACK_COMMAND.md");
assert(fs.existsSync(docPath), "clarification bridge readback command doc missing");
const doc = fs.readFileSync(docPath, "utf8");
assert(doc.includes("admin email sprint7 clarification bridge"), "doc missing command");
assert(doc.includes("Gmail read performed: false"), "doc missing Gmail read safety");
assert(doc.includes("Finance write performed: false"), "doc missing finance write safety");
assert(doc.includes("Safe prompt fields: 9"), "doc missing safe field count");

console.log("RESULT=PASS_SPRINT7_EMAIL_CLARIFICATION_BRIDGE_READBACK_STATIC_TEST");
console.log("COMMAND=admin email sprint7 clarification bridge");
console.log("STATUS=email_clarification_bridge_design_ready");
