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

  assert(text.includes("admin email sprint7 gmail label filter"), `${rel} missing gmail label filter command`);
  assert(text.includes("function airoSprint7GmailLabelFilterDesign_"), `${rel} missing design function`);
  assert(text.includes("function airoSprint7GmailLabelFilterReadbackText_"), `${rel} missing text function`);
  assert(text.includes("function airoSprint7GmailLabelFilterMaybeHandleRoute_"), `${rel} missing route function`);
  assert(text.includes("function airoOriginalDoPostForSprint7GmailLabelFilter_"), `${rel} missing doPost wrapper`);

  const blockMatch = text.match(/\/\* AIRO_SPRINT7_GMAIL_LABEL_FILTER_READBACK_START \*\/([\s\S]*?)\/\* AIRO_SPRINT7_GMAIL_LABEL_FILTER_READBACK_END \*\//);
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
    "gmail_label_created: false",
    "gmail_filter_created: false",
    "mail_trigger_created: false",
    "email_modified: false",
    "mark_read_performed: false",
    "archive_performed: false",
    "delete_performed: false",
    "move_to_trash_performed: false",
    "label_modification_performed: false",
    "finance_write_performed: false",
    "account_ledger_write_performed: false",
    "finance_events_write_performed: false",
    "review_queue_write_performed: false",
    "full_email_body_storage_allowed: false",
    "auto_write_allowed: false",
    "live_email_scan_allowed: false",
    "required_label: \"Finance/ToProcess\"",
    "missing_label_parse_status: \"blocked_source_contract\"",
    "missing_label_needs_review_reason: \"missing_required_label\"",
    "script_may_create_label_in_this_phase: false",
    "script_may_create_filter_in_this_phase: false",
    "script_may_modify_email_in_this_phase: false",
    "parse_status: \"blocked_source_contract\"",
    "needs_review_reason: \"missing_required_label\"",
    "needs_review_reason: \"sender_not_allowlisted, missing_required_label\"",
    "parse_status: \"skipped_sensitive\"",
    "sensitive content wins before sender and label checks",
    "filter_status: \"design_only_not_created\"",
    "filter_status: \"never_finance_filter\""
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
    ".moveToTrash(",
    ".createLabel(",
    ".createFilter(",
    ".moveToArchive(",
    ".delete"
  ];

  for (const call of forbiddenCalls) {
    assert(!block.includes(call), `${rel} managed block contains forbidden call ${call}`);
  }
}

const docPath = path.join(repo, "docs/AIRO_FINANCE_SPRINT7_GMAIL_LABEL_FILTER_READBACK_COMMAND.md");
assert(fs.existsSync(docPath), "gmail label/filter readback doc missing");
const doc = fs.readFileSync(docPath, "utf8");

assert(doc.includes("admin email sprint7 gmail label filter"), "doc missing command");
assert(doc.includes("RESULT=PASS_SPRINT7_GMAIL_LABEL_FILTER_READBACK_COMMAND_IMPLEMENTED"), "doc missing result marker");
assert(doc.includes("Gmail read performed: false"), "doc missing gmail safety");
assert(doc.includes("Gmail label created: false"), "doc missing label creation safety");
assert(doc.includes("Gmail filter created: false"), "doc missing filter creation safety");
assert(doc.includes("Email modified: false"), "doc missing email modification safety");
assert(doc.includes("Finance write performed: false"), "doc missing finance write safety");

console.log("RESULT_GMAIL_LABEL_FILTER_READBACK_TEST=PASS");
console.log("COMMAND=admin email sprint7 gmail label filter");
console.log("TESTED_TARGETS=" + targets.map((p) => path.relative(repo, p)).join(","));
