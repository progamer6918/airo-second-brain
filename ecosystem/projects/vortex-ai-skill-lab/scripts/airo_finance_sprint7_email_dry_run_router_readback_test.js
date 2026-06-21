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
  const start = "// AIRO_SPRINT7_EMAIL_DRY_RUN_ROUTER_READBACK_START";
  const end = "// AIRO_SPRINT7_EMAIL_DRY_RUN_ROUTER_READBACK_END";
  const s = text.indexOf(start);
  const e = text.indexOf(end);
  assert(s >= 0, `${rel} missing dry run router start marker`);
  assert(e > s, `${rel} missing dry run router end marker`);
  return text.slice(s, e + end.length);
}

for (const rel of sourcePaths) {
  const text = read(rel);
  const block = extractBlock(text, rel);

  assert(text.includes("sprint7EmailDryRunRouterResult"), `${rel} missing doPost dry run router route`);
  assert(block.includes("admin email sprint7 dry run router"), `${rel} missing command`);
  assert(block.includes("email_dry_run_router_design_ready"), `${rel} missing status`);
  assert(block.includes("sendTelegram_"), `${rel} missing telegram reply path`);
  assert(block.includes("telegramReplyAttempted"), `${rel} missing telegram reply tracking`);

  const destinations = [
    "account_ledger_expense",
    "account_ledger_income",
    "account_ledger_transfer",
    "credit_card_purchase",
    "credit_card_payment",
    "refund_or_reversal",
    "internal_transfer",
    "review_queue_future",
    "blocked_sensitive",
    "blocked_duplicate",
    "blocked_low_confidence",
    "blocked_missing_field",
    "no_route",
  ];

  for (const destination of destinations) {
    assert(block.includes(`"${destination}"`), `${rel} missing destination ${destination}`);
  }

  const blockedOutcomes = [
    "sensitive_content_detected",
    "duplicate_risk_exists",
    "amount_missing",
    "date_missing",
    "account_mapping_missing",
    "source_contract_failed",
    "required_label_missing",
    "parser_confidence_too_low",
    "status_unclear",
    "category_required_but_missing",
    "merchant_required_but_missing",
    "direction_unclear",
  ];

  for (const outcome of blockedOutcomes) {
    assert(block.includes(`"${outcome}"`), `${rel} missing blocked outcome ${outcome}`);
  }

  const requiredFlags = [
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
    assert(!block.includes(forbidden), `${rel} dry run router block contains forbidden runtime call ${forbidden}`);
  }
}

const docPath = path.join(repoRoot, "docs/AIRO_FINANCE_SPRINT7_EMAIL_DRY_RUN_ROUTER_READBACK_COMMAND.md");
assert(fs.existsSync(docPath), "dry run router readback command doc missing");
const doc = fs.readFileSync(docPath, "utf8");
assert(doc.includes("admin email sprint7 dry run router"), "doc missing command");
assert(doc.includes("Write allowed: false"), "doc missing write allowed safety");
assert(doc.includes("Finance write performed: false"), "doc missing finance write safety");
assert(doc.includes("Proposed destinations: 13"), "doc missing destination count");

console.log("RESULT=PASS_SPRINT7_EMAIL_DRY_RUN_ROUTER_READBACK_STATIC_TEST");
console.log("COMMAND=admin email sprint7 dry run router");
console.log("STATUS=email_dry_run_router_design_ready");
