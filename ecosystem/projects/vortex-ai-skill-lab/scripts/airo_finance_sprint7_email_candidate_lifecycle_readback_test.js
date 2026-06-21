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
  const start = "// AIRO_SPRINT7_EMAIL_CANDIDATE_LIFECYCLE_READBACK_START";
  const end = "// AIRO_SPRINT7_EMAIL_CANDIDATE_LIFECYCLE_READBACK_END";
  const s = text.indexOf(start);
  const e = text.indexOf(end);
  assert(s >= 0, `${rel} missing lifecycle start marker`);
  assert(e > s, `${rel} missing lifecycle end marker`);
  return text.slice(s, e + end.length);
}

for (const rel of sourcePaths) {
  const text = read(rel);
  const block = extractBlock(text, rel);

  assert(text.includes("sprint7EmailCandidateLifecycleResult"), `${rel} missing doPost lifecycle route`);
  assert(block.includes("admin email sprint7 candidate lifecycle"), `${rel} missing command`);
  assert(block.includes("email_candidate_lifecycle_design_ready"), `${rel} missing status`);
  assert(block.includes("sendTelegram_"), `${rel} missing telegram reply path`);
  assert(block.includes("telegramReplyAttempted"), `${rel} missing telegram reply tracking`);

  const lifecycleStates = [
    "disabled_default_off",
    "source_contract_blocked",
    "skipped_sensitive",
    "metadata_logged",
    "parse_candidate",
    "needs_clarification",
    "awaiting_telegram_answer",
    "clarification_resolved",
    "needs_review",
    "ready_for_router",
    "routed_dry_run",
    "committed_future",
    "failed",
  ];

  for (const state of lifecycleStates) {
    assert(block.includes(`"${state}"`), `${rel} missing lifecycle state ${state}`);
  }

  const forbiddenTransitions = [
    "routed_dry_run_to_committed_future",
    "parse_candidate_to_account_ledger_write",
    "parse_candidate_to_finance_events_write",
    "parse_candidate_to_review_queue_write",
    "skipped_sensitive_to_telegram_clarification",
    "skipped_sensitive_to_finance_parser",
    "skipped_sensitive_to_review_queue",
    "skipped_sensitive_to_finance_events",
  ];

  for (const transition of forbiddenTransitions) {
    assert(block.includes(`"${transition}"`), `${rel} missing forbidden transition ${transition}`);
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
    assert(!block.includes(forbidden), `${rel} lifecycle block contains forbidden runtime call ${forbidden}`);
  }
}

const docPath = path.join(repoRoot, "docs/AIRO_FINANCE_SPRINT7_EMAIL_CANDIDATE_LIFECYCLE_READBACK_COMMAND.md");
assert(fs.existsSync(docPath), "lifecycle readback command doc missing");
const doc = fs.readFileSync(docPath, "utf8");
assert(doc.includes("admin email sprint7 candidate lifecycle"), "doc missing command");
assert(doc.includes("Gmail read performed: false"), "doc missing Gmail read safety");
assert(doc.includes("Finance write performed: false"), "doc missing finance write safety");
assert(doc.includes("Lifecycle states: 13"), "doc missing state count");

console.log("RESULT=PASS_SPRINT7_EMAIL_CANDIDATE_LIFECYCLE_READBACK_STATIC_TEST");
console.log("COMMAND=admin email sprint7 candidate lifecycle");
console.log("STATUS=email_candidate_lifecycle_design_ready");
