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
  const start = "// AIRO_SPRINT7B_EMAIL_SANDBOX_FIXTURES_READBACK_START";
  const end = "// AIRO_SPRINT7B_EMAIL_SANDBOX_FIXTURES_READBACK_END";
  const s = text.indexOf(start);
  const e = text.indexOf(end);
  assert(s >= 0, `${rel} missing sandbox fixtures start marker`);
  assert(e > s, `${rel} missing sandbox fixtures end marker`);
  return text.slice(s, e + end.length);
}

for (const rel of sourcePaths) {
  const text = read(rel);
  const block = extractBlock(text, rel);

  assert(text.includes("sprint7BEmailSandboxFixturesResult"), `${rel} missing doPost sandbox fixtures route`);
  assert(block.includes("admin email sprint7b sandbox fixtures"), `${rel} missing command`);
  assert(block.includes("email_sandbox_fixtures_design_ready"), `${rel} missing status`);
  assert(block.includes("sendTelegram_"), `${rel} missing telegram reply path`);
  assert(block.includes("telegramReplyAttempted"), `${rel} missing telegram reply tracking`);

  const categories = [
    "safe_expense_bank",
    "safe_income_bank",
    "safe_credit_card_purchase",
    "safe_credit_card_payment",
    "safe_refund_reversal",
    "safe_internal_transfer",
    "ambiguous_direction",
    "ambiguous_status",
    "missing_category",
    "missing_account_mapping",
    "duplicate_candidate",
    "low_confidence_parse",
    "sensitive_otp_block",
    "sensitive_login_block",
    "sensitive_password_reset_block",
    "unknown_sender_block",
    "missing_required_label_block",
    "failed_transaction_no_write",
    "pending_transaction_no_write",
    "malformed_metadata",
  ];

  for (const category of categories) {
    assert(block.includes(`"${category}"`), `${rel} missing fixture category ${category}`);
  }

  const requiredFlags = [
    "synthetic_fixtures_only: true",
    "write_allowed: false",
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

  const forbiddenContent = [
    "real_email_body",
    "real_otp_code",
    "real_auth_code",
    "real_login_link",
    "real_password_reset_link",
    "full_card_number",
    "full_account_number",
    "private_security_content",
  ];

  for (const forbidden of forbiddenContent) {
    assert(block.includes(`"${forbidden}"`), `${rel} missing forbidden fixture content ${forbidden}`);
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
    assert(!block.includes(forbidden), `${rel} sandbox fixtures block contains forbidden runtime call ${forbidden}`);
  }
}

const docPath = path.join(repoRoot, "docs/AIRO_FINANCE_SPRINT7B_EMAIL_SANDBOX_FIXTURES_READBACK_COMMAND.md");
assert(fs.existsSync(docPath), "sandbox fixtures readback command doc missing");
const doc = fs.readFileSync(docPath, "utf8");
assert(doc.includes("admin email sprint7b sandbox fixtures"), "doc missing command");
assert(doc.includes("Synthetic fixtures only: true"), "doc missing synthetic safety");
assert(doc.includes("Gmail read performed: false"), "doc missing Gmail read safety");
assert(doc.includes("Finance write performed: false"), "doc missing finance write safety");
assert(doc.includes("Fixture categories: 20"), "doc missing fixture category count");

console.log("RESULT=PASS_SPRINT7B_EMAIL_SANDBOX_FIXTURES_READBACK_STATIC_TEST");
console.log("COMMAND=admin email sprint7b sandbox fixtures");
console.log("STATUS=email_sandbox_fixtures_design_ready");
