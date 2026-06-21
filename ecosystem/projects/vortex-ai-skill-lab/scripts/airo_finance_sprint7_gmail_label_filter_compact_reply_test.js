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

  const fnMatch = text.match(/function airoSprint7GmailLabelFilterReadbackText_\([\s\S]*?\n\}/);
  assert(fnMatch, `${rel} readback text function missing`);
  const fn = fnMatch[0];

  const requiredText = [
    "Sprint 7 Gmail Label/Filter selesai.",
    "Mode: ",
    "Design only: ",
    "Write performed: ",
    "Email ingestion enabled: ",
    "Gmail read performed",
    "Gmail label created",
    "Gmail filter created",
    "Email modified",
    "Finance write performed",
    "Required label",
    "Missing label parse_status",
    "Sensitive parse_status",
    "Still forbidden",
    "Status: gmail_label_filter_design_ready"
  ];

  for (const snippet of requiredText) {
    assert(fn.includes(snippet), `${rel} compact readback missing ${snippet}`);
  }

  assert(fn.length < 4500, `${rel} compact function too long: ${fn.length}`);

  const blockMatch = text.match(/\/\* AIRO_SPRINT7_GMAIL_LABEL_FILTER_READBACK_START \*\/([\s\S]*?)\/\* AIRO_SPRINT7_GMAIL_LABEL_FILTER_READBACK_END \*\//);
  assert(blockMatch, `${rel} missing managed block`);
  const block = blockMatch[1];

  const requiredBlockSnippets = [
    "mode: \"dry-run\"",
    "design_only: true",
    "write_performed: false",
    "email_ingestion_enabled: false",
    "email_default_off: true",
    "dry_run_only: true",
    "gmail_read_performed: false",
    "gmail_label_created: false",
    "gmail_filter_created: false",
    "email_modified: false",
    "finance_write_performed: false",
    "required_label: \"Finance/ToProcess\"",
    "missing_label_parse_status: \"blocked_source_contract\"",
    "missing_label_needs_review_reason: \"missing_required_label\"",
    "script_may_create_label_in_this_phase: false",
    "script_may_create_filter_in_this_phase: false",
    "script_may_modify_email_in_this_phase: false",
    "parse_status: \"skipped_sensitive\""
  ];

  for (const snippet of requiredBlockSnippets) {
    assert(block.includes(snippet), `${rel} managed block missing ${snippet}`);
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

console.log("RESULT_GMAIL_LABEL_FILTER_COMPACT_REPLY_TEST=PASS");
console.log("COMMAND=admin email sprint7 gmail label filter");
console.log("TESTED_TARGETS=" + targets.map((p) => path.relative(repo, p)).join(","));
