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
  const start = "// AIRO_SPRINT7B_FIXTURE_MATRIX_READBACK_START";
  const end = "// AIRO_SPRINT7B_FIXTURE_MATRIX_READBACK_END";
  const s = text.indexOf(start);
  const e = text.indexOf(end);
  assert(s >= 0, `${rel} missing fixture matrix start marker`);
  assert(e > s, `${rel} missing fixture matrix end marker`);
  return text.slice(s, e + end.length);
}

for (const rel of sourcePaths) {
  const text = read(rel);
  const block = extractBlock(text, rel);

  assert(text.includes("sprint7BFixtureMatrixResult"), `${rel} missing doPost fixture matrix route`);
  assert(block.includes("admin email sprint7b fixture matrix"), `${rel} missing command`);
  assert(block.includes("email_fixture_matrix_ready"), `${rel} missing status`);
  assert(block.includes("sendTelegram_"), `${rel} missing telegram reply path`);
  assert(block.includes("telegramReplyAttempted"), `${rel} missing telegram reply tracking`);

  const requiredFlags = [
    "design_only: true",
    "synthetic_fixtures_only: true",
    "fixture_matrix_built: true",
    "fixture_count: 20",
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
    "all_writes_disabled: true",
  ];

  for (const flag of requiredFlags) {
    assert(block.includes(flag), `${rel} missing flag ${flag}`);
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
    assert(!block.includes(forbidden), `${rel} fixture matrix block contains forbidden runtime call ${forbidden}`);
  }
}

const matrixPath = path.join(repoRoot, "docs/airo-finance/sprint7b/email_sandbox_fixture_matrix_20260527.json");
assert(fs.existsSync(matrixPath), "fixture matrix json missing");
const matrix = JSON.parse(fs.readFileSync(matrixPath, "utf8"));
assert(matrix.fixture_count === 20, "fixture matrix count mismatch");
assert(matrix.mode === "synthetic-only", "fixture matrix mode mismatch");
assert(matrix.gmail_live_read_performed === false, "matrix Gmail read guard mismatch");
assert(matrix.finance_write_performed === false, "matrix finance write guard mismatch");
for (const fx of matrix.fixtures) {
  assert(fx.expected_write_allowed === false, `${fx.fixture_id} expected_write_allowed not false`);
  assert(fx.expected_write_performed === false, `${fx.fixture_id} expected_write_performed not false`);
}

const docPath = path.join(repoRoot, "docs/AIRO_FINANCE_SPRINT7B_FIXTURE_MATRIX_READBACK_COMMAND.md");
assert(fs.existsSync(docPath), "fixture matrix readback command doc missing");
const doc = fs.readFileSync(docPath, "utf8");
assert(doc.includes("admin email sprint7b fixture matrix"), "doc missing command");
assert(doc.includes("Fixture count: 20"), "doc missing fixture count");
assert(doc.includes("All writes disabled: true"), "doc missing write disabled proof");

console.log("RESULT=PASS_SPRINT7B_FIXTURE_MATRIX_READBACK_STATIC_TEST");
console.log("COMMAND=admin email sprint7b fixture matrix");
console.log("STATUS=email_fixture_matrix_ready");
