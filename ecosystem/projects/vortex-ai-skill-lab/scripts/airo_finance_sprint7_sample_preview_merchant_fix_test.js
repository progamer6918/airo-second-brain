const fs = require("fs");
const path = require("path");

const repo = "/home/egitaristorandas/vortex-ai-skill-lab";
const targets = [
  "scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs",
  "apps-script-prod-v2/AIRO_Finance_Multitab_Final_v1.js",
].map((p) => path.join(repo, p)).filter((p) => fs.existsSync(p));

function assertEqual(actual, expected, message) {
  if (actual !== expected) {
    console.error("ASSERT_FAIL=" + message);
    console.error("EXPECTED=" + expected);
    console.error("ACTUAL=" + actual);
    process.exit(1);
  }
}

function assert(condition, message) {
  if (!condition) {
    console.error("ASSERT_FAIL=" + message);
    process.exit(1);
  }
}

function normalize(value) {
  return String(value || "").replace(/\s+/g, " ").trim();
}

function cleanMerchant(value) {
  let text = normalize(value);

  text = text.replace(/\b(?:rp|idr)\s*[0-9][0-9\.\,]*/ig, " ");
  text = text.replace(/\b[0-9]{1,3}(?:[\.][0-9]{3})+\b/g, " ");
  text = text.replace(/\b[0-9]{4,}\b/g, " ");
  text = text.replace(/^[\s\-:=]+/g, " ");

  const blocked = {
    di: true,
    at: true,
    amount: true,
    nominal: true,
    sebesar: true,
    transaksi: true,
    transaction: true,
    notification: true,
    sample: true,
    debit: true,
    credit: true,
    payment: true,
    purchase: true,
    pembayaran: true,
    merchant: true,
    toko: true,
    store: true,
  };

  const kept = [];

  for (const rawToken of text.split(/\s+/)) {
    const token = String(rawToken || "").replace(/^[:=\-]+|[:=\-]+$/g, "");
    const lower = token.toLowerCase();

    if (!token) continue;
    if (blocked[lower]) continue;

    kept.push(token);
  }

  return kept.join(" ").replace(/\s+/g, " ").trim().slice(0, 60);
}

function tokenKey(token) {
  return String(token || "").toLowerCase().replace(/^[:=\-]+|[:=\-]+$/g, "");
}

function extractMerchant(sampleText) {
  const text = normalize(sampleText);
  const tokens = text.split(/\s+/);

  const labelKeys = {
    merchant: true,
    toko: true,
    store: true,
  };

  for (let i = 0; i < tokens.length; i++) {
    const raw = String(tokens[i] || "");
    const key = tokenKey(raw);

    if (labelKeys[key]) {
      return cleanMerchant(tokens.slice(i + 1).join(" "));
    }

    const inlineLabel = raw.match(/^(merchant|toko|store)[:=\-](.+)$/i);
    if (inlineLabel && inlineLabel[2]) {
      return cleanMerchant(inlineLabel[2] + " " + tokens.slice(i + 1).join(" "));
    }
  }

  for (let j = 0; j < tokens.length; j++) {
    const placeKey = tokenKey(tokens[j]);

    if (placeKey === "di" || placeKey === "at") {
      return cleanMerchant(tokens.slice(j + 1).join(" "));
    }
  }

  return "";
}

const samples = [
  ["Blu debit notification sample Rp125000 merchant Kopi Kenangan", "Kopi Kenangan"],
  ["BCA transaksi Rp240000 di Tokopedia", "Tokopedia"],
  ["credit card purchase at Starbucks Rp58000", "Starbucks"],
  ["Blu debit notification sample Rp125000 merchant: Kopi Kenangan", "Kopi Kenangan"],
  ["Blu debit notification sample Rp125000 merchant=Kopi Kenangan", "Kopi Kenangan"],
];

for (const [input, expected] of samples) {
  const actual = extractMerchant(input);
  console.log(`MERCHANT_TEST input="${input}" actual="${actual}" expected="${expected}"`);
  assertEqual(actual, expected, `merchant extraction failed for ${input}`);
}

assert(!extractMerchant("Blu debit notification sample Rp125000 merchant Kopi Kenangan").startsWith("ion sample"), "must not match di inside notification");

assert(targets.length > 0, "no Apps Script target found");

for (const target of targets) {
  const text = fs.readFileSync(target, "utf8");
  const rel = path.relative(repo, target);

  assert(text.includes("function airoSprint7SamplePreviewCleanMerchant_"), `${rel} missing clean merchant helper`);
  assert(text.includes("function airoSprint7SamplePreviewTokenKey_"), `${rel} missing token key helper`);
  assert(text.includes("function airoSprint7SamplePreviewExtractMerchant_"), `${rel} missing merchant extractor`);
  assert(text.includes('"merchant": true'), `${rel} missing merchant label token`);
  assert(text.includes('placeKey === "di" || placeKey === "at"'), `${rel} missing deterministic di/at token logic`);
  assert(!text.includes("/(?:merchant|toko|di|at)\\s*[:\\-]?"), `${rel} still contains unsafe old merchant regex`);

  const blockMatch = text.match(/\/\* AIRO_SPRINT7_MANUAL_SAMPLE_PREVIEW_START \*\/([\s\S]*?)\/\* AIRO_SPRINT7_MANUAL_SAMPLE_PREVIEW_END \*\//);
  assert(blockMatch, `${rel} missing managed block`);
  const block = blockMatch[1];

  const forbiddenCalls = [
    "GmailApp.",
    "MailApp.",
    "ScriptApp.newTrigger",
    ".appendRow(",
    ".setValues(",
    ".setValue(",
    ".markRead(",
    ".moveToTrash("
  ];

  for (const call of forbiddenCalls) {
    assert(!block.includes(call), `${rel} managed block contains forbidden live/write call ${call}`);
  }

  const requiredSafety = [
    "write_performed: false",
    "email_ingestion_enabled: false",
    "email_default_off: true",
    "dry_run_only: true",
    "gmail_read_performed: false",
    "mailbox_read_performed: false",
    "mail_trigger_created: false",
    "finance_write_performed: false",
    "account_ledger_write_performed: false",
    "finance_events_write_performed: false",
    "review_queue_write_performed: false",
    "full_email_body_storage_allowed: false",
    "sample_text_stored: false"
  ];

  for (const snippet of requiredSafety) {
    assert(block.includes(snippet), `${rel} missing safety snippet ${snippet}`);
  }
}

console.log("RESULT_MERCHANT_FIX_TEST=PASS");
console.log("EXPECTED_MERCHANT=Kopi Kenangan");
console.log("EXPECTED_DI_SAMPLE_MERCHANT=Tokopedia");
console.log("TESTED_TARGETS=" + targets.map((p) => path.relative(repo, p)).join(","));
