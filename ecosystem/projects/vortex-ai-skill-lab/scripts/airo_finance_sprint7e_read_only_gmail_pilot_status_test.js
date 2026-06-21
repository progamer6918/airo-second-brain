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

function extractBlock(text, rel) {
  const start = "// AIRO_SPRINT7E_READ_ONLY_GMAIL_PILOT_STATUS_START";
  const end = "// AIRO_SPRINT7E_READ_ONLY_GMAIL_PILOT_STATUS_END";
  const s = text.indexOf(start);
  const e = text.indexOf(end);
  assert(s >= 0, `${rel} missing Sprint 7E status start marker`);
  assert(e > s, `${rel} missing Sprint 7E status end marker`);
  return text.slice(s, e + end.length);
}

for (const rel of sourcePaths) {
  const text = read(rel);
  const block = extractBlock(text, rel);

  assert(text.includes("sprint7EReadOnlyPilotStatusResult"), `${rel} missing doPost Sprint 7E status route`);
  assert(block.includes("admin email sprint7e read only pilot status"), `${rel} missing command`);
  assert(block.includes("read_only_gmail_pilot_static_default_off_ready"), `${rel} missing status`);
  assert(block.includes("sendTelegram_"), `${rel} missing telegram reply path`);
  assert(block.includes("telegramReplyAttempted"), `${rel} missing telegram reply tracking`);

  const requiredFlags = [
    "gmail_pilot_enabled: false",
    "manual_approval_required: true",
    "email_ingestion_enabled: false",
    "email_default_off: true",
    "dry_run_only: true",
    "gmail_label_required: \"Info Terbaru\"",
    "max_messages_per_run: 5",
    "max_threads_per_run: 5",
    "source_count: 2",
    "allowed_sender_count: 2",
    "gmail_live_read_performed: false",
    "mailbox_read_performed: false",
    "gmail_modified: false",
    "mail_trigger_created: false",
    "full_email_body_stored: false",
    "sensitive_content_stored: false",
    "raw_email_forwarded_to_telegram: false",
    "finance_write_performed: false",
    "account_ledger_write_performed: false",
    "finance_events_write_performed: false",
    "review_queue_write_performed: false",
    "domain_tab_write_performed: false",
  ];

  for (const flag of requiredFlags) {
    assert(block.includes(flag), `${rel} missing flag ${flag}`);
  }

  assert(block.includes("receipts@blubybcadigital.id"), `${rel} missing Blu sender`);
  assert(block.includes("noreply@tokopedia.com"), `${rel} missing Tokopedia sender`);

  const forbiddenRuntimeCalls = [
    "GmailApp",
    "MailApp",
    "SpreadsheetApp",
    "getInboxThreads",
    "search(",
    "markRead",
    "markUnread",
    "moveToArchive",
    "moveToTrash",
    "createLabel",
    "addLabel",
    "removeLabel",
    "." + "delete",
  ];

  for (const forbidden of forbiddenRuntimeCalls) {
    assert(!block.includes(forbidden), `${rel} Sprint 7E status block contains forbidden runtime call ${forbidden}`);
  }
}

const docPath = path.join(repoRoot, "docs/AIRO_FINANCE_SPRINT7E_READ_ONLY_GMAIL_PILOT_STATUS_COMMAND.md");
assert(fs.existsSync(docPath), "Sprint 7E status command doc missing");
const doc = fs.readFileSync(docPath, "utf8");
assert(doc.includes("admin email sprint7e read only pilot status"), "doc missing command");
assert(doc.includes("Gmail pilot enabled: false"), "doc missing disabled proof");
assert(doc.includes("Manual approval required: true"), "doc missing approval proof");
assert(doc.includes("Finance write performed: false"), "doc missing finance write safety");

console.log("RESULT=PASS_SPRINT7E_READ_ONLY_GMAIL_PILOT_STATUS_STATIC_TEST");
console.log("COMMAND=admin email sprint7e read only pilot status");
console.log("STATUS=read_only_gmail_pilot_static_default_off_ready");
