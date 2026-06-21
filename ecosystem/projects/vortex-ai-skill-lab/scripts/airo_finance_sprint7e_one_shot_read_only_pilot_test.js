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
  const start = "// AIRO_SPRINT7E_ONE_SHOT_READ_ONLY_GMAIL_PILOT_START";
  const end = "// AIRO_SPRINT7E_ONE_SHOT_READ_ONLY_GMAIL_PILOT_END";
  const s = text.indexOf(start);
  const e = text.indexOf(end);
  assert(s >= 0, `${rel} missing one-shot pilot start marker`);
  assert(e > s, `${rel} missing one-shot pilot end marker`);
  return text.slice(s, e + end.length);
}

for (const rel of sourcePaths) {
  const text = read(rel);
  const block = extractBlock(text, rel);

  assert(text.includes("sprint7EOneShotReadOnlyPilotResult"), `${rel} missing doPost one-shot route`);
  assert(block.includes("admin email sprint7e one shot read only pilot"), `${rel} missing command`);
  assert(block.includes("GmailApp.search"), `${rel} missing approved read-only Gmail search`);
  assert(block.includes("Info Terbaru"), `${rel} missing label`);
  assert(block.includes("receipts@blubybcadigital.id"), `${rel} missing Blu sender`);
  assert(block.includes("noreply@tokopedia.com"), `${rel} missing Tokopedia sender`);
  assert(block.includes("max_messages_per_run: 5"), `${rel} missing max message limit`);
  assert(block.includes("finance_write_performed: false"), `${rel} missing finance write false`);
  assert(block.includes("full_email_body_stored: false"), `${rel} missing full body false`);
  assert(block.includes("raw_email_forwarded_to_telegram: false"), `${rel} missing raw forwarding false`);
  assert(block.includes("mail_trigger_created: false"), `${rel} missing trigger false`);
  assert(block.includes("email_modified: false"), `${rel} missing email modified false`);
  assert(block.includes("dry_run_route_count"), `${rel} missing dry_run_route_count`);

  const requiredRuntimeFlags = [
    "gmail_live_read_performed: true",
    "mailbox_read_performed: true",
    "account_ledger_write_performed: false",
    "finance_events_write_performed: false",
    "review_queue_write_performed: false",
    "domain_tab_write_performed: false",
  ];

  for (const flag of requiredRuntimeFlags) {
    assert(block.includes(flag), `${rel} missing runtime flag ${flag}`);
  }

  const forbiddenRuntimeCalls = [
    "getPlainBody",
    "getBody",
    "getRawContent",
    "createDraft",
    "sendEmail",
    "createLabel",
    "addLabel",
    "removeLabel",
    "markRead",
    "markUnread",
    "moveToArchive",
    "moveToInbox",
    "moveToTrash",
    ".delete",
    "SpreadsheetApp",
    "DriveApp",
    "CalendarApp"
  ];

  for (const forbidden of forbiddenRuntimeCalls) {
    assert(!block.includes(forbidden), `${rel} one-shot pilot block contains forbidden call ${forbidden}`);
  }
}

console.log("RESULT=PASS_SPRINT7E_ONE_SHOT_READ_ONLY_GMAIL_PILOT_STATIC_TEST");
console.log("COMMAND=admin email sprint7e one shot read only pilot");
console.log("STATUS=one_shot_read_only_pilot_ready");
