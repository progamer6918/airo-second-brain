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
  const start = "// AIRO_SPRINT7_EMAIL_INGESTION_LOG_READBACK_START";
  const end = "// AIRO_SPRINT7_EMAIL_INGESTION_LOG_READBACK_END";
  const s = text.indexOf(start);
  const e = text.indexOf(end);
  assert(s >= 0, `${rel} missing readback start marker`);
  assert(e > s, `${rel} missing readback end marker`);
  return text.slice(s, e + end.length);
}

for (const rel of sourcePaths) {
  const text = read(rel);
  const block = extractBlock(text, rel);

  assert(text.includes("var sprint7EmailIngestionLogResult = airoSprint7EmailIngestionLogMaybeHandleRoute_(e);"), `${rel} missing route hook`);
  assert(text.includes("return sprint7EmailIngestionLogResult;"), `${rel} missing route return`);
  assert(text.includes("route: \"gmail_label_filter_piggyback\""), `${rel} missing piggyback route marker`);
  assert(text.includes("text === \"admin email sprint7 ingestion log\""), `${rel} missing piggyback command guard`);
  assert(text.includes("sprint7EmailIngestionLogEntryResult"), `${rel} missing safe doPost entry route`);
  assert(block.includes("admin email sprint7 ingestion log"), `${rel} missing command`);
  assert(block.includes("_AIRO_Email_Ingestion_Log"), `${rel} missing sheet name`);
  assert(block.includes("email_ingestion_log_design_ready"), `${rel} missing status`);
  assert(block.includes("telegramReplyAttempted"), `${rel} missing telegram reply attempt tracking`);
  assert(block.includes("telegramReplyDelivered"), `${rel} missing telegram reply delivery tracking`);
  assert(block.includes("sendTelegram_"), `${rel} missing primary sendTelegram reply path`);

  const requiredColumns = [
    "email_log_id",
    "message_id",
    "thread_id",
    "source_id",
    "from_email",
    "subject_hash",
    "received_at",
    "processed_at",
    "parse_status",
    "parse_confidence",
    "detected_amount",
    "detected_date",
    "detected_merchant",
    "detected_last4",
    "sensitive_skip_reason",
    "clarification_ref",
    "event_ref",
    "review_queue_ref",
    "error_message",
    "notes",
  ];

  for (const col of requiredColumns) {
    assert(block.includes(`"${col}"`), `${rel} missing required column ${col}`);
  }

  const parseStatuses = [
    "dry_run_ready",
    "blocked_source_contract",
    "skipped_sensitive",
    "missing_required_label",
    "sender_not_allowed",
    "parse_candidate",
    "needs_clarification",
    "needs_review",
    "duplicate_candidate",
    "parse_failed",
    "disabled_default_off",
  ];

  for (const status of parseStatuses) {
    assert(block.includes(`"${status}"`), `${rel} missing parse_status ${status}`);
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
    "finance_write_performed: false",
    "account_ledger_write_performed: false",
    "finance_events_write_performed: false",
    "review_queue_write_performed: false",
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
    assert(!block.includes(forbidden), `${rel} readback block contains forbidden runtime call ${forbidden}`);
  }
}

const docPath = path.join(repoRoot, "docs/AIRO_FINANCE_SPRINT7_EMAIL_INGESTION_LOG_READBACK_COMMAND.md");
assert(fs.existsSync(docPath), "readback command doc missing");
const doc = fs.readFileSync(docPath, "utf8");
assert(doc.includes("admin email sprint7 ingestion log"), "doc missing command");
assert(doc.includes("Gmail read performed: false"), "doc missing Gmail read safety");
assert(doc.includes("Finance write performed: false"), "doc missing finance write safety");
assert(doc.includes("_AIRO_Email_Ingestion_Log"), "doc missing sheet name");

console.log("RESULT=PASS_SPRINT7_EMAIL_INGESTION_LOG_READBACK_STATIC_TEST");
console.log("COMMAND=admin email sprint7 ingestion log");
console.log("STATUS=email_ingestion_log_design_ready");
