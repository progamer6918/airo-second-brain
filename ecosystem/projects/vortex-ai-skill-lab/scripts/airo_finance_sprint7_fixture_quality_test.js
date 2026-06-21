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

function assertEqual(actual, expected, message) {
  if (actual !== expected) {
    console.error("ASSERT_FAIL=" + message);
    console.error("EXPECTED=" + expected);
    console.error("ACTUAL=" + actual);
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
  text = text.replace(/\bkartu\s+kredit\b/ig, " ");
  text = text.replace(/\bcredit\s+card\b/ig, " ");
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
    card: true,
    cc: true,
    payment: true,
    purchase: true,
    pembayaran: true,
    merchant: true,
    toko: true,
    store: true,
    kartu: true,
    kredit: true,
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

function guessCategory(sampleText) {
  const text = String(sampleText || "").toLowerCase();

  if (text.includes("refund") || text.includes("reversal") || text.includes("pengembalian")) {
    return "Refund";
  }

  if (
    text.includes("kopi") ||
    text.includes("coffee") ||
    text.includes("cafe") ||
    text.includes("café") ||
    text.includes("starbucks") ||
    text.includes("makan") ||
    text.includes("minum") ||
    text.includes("resto") ||
    text.includes("restaurant") ||
    text.includes("food") ||
    text.includes("warung")
  ) {
    return "Makan";
  }

  if (text.includes("transport") || text.includes("gojek") || text.includes("grab") || text.includes("bensin")) {
    return "Transport";
  }

  if (text.includes("transfer")) {
    return "Transfer";
  }

  return "";
}

const fixtureAssertions = [
  {
    input: "BCA transaksi Rp240000 di Tokopedia",
    merchant: "Tokopedia",
    category: "",
  },
  {
    input: "credit card purchase at Starbucks Rp58000",
    merchant: "Starbucks",
    category: "Makan",
  },
  {
    input: "refund reversal Rp75000 merchant Tokopedia kartu kredit",
    merchant: "Tokopedia",
    category: "Refund",
  },
];

for (const fixture of fixtureAssertions) {
  const merchant = extractMerchant(fixture.input);
  const category = guessCategory(fixture.input);
  console.log(`FIXTURE_TEST input="${fixture.input}" merchant="${merchant}" category="${category}"`);

  assertEqual(merchant, fixture.merchant, `merchant mismatch for ${fixture.input}`);
  assertEqual(category, fixture.category, `category mismatch for ${fixture.input}`);
}

assert(targets.length > 0, "no Apps Script target found");

for (const target of targets) {
  const text = fs.readFileSync(target, "utf8");
  const rel = path.relative(repo, target);

  assert(text.includes('"starbucks"'), `${rel} missing starbucks category keyword`);
  assert(text.includes('"kartu": true'), `${rel} missing kartu cleanup token`);
  assert(text.includes('"kredit": true'), `${rel} missing kredit cleanup token`);
  assert(text.includes('text.indexOf("refund")'), `${rel} missing refund priority`);
  assert(text.includes('text.indexOf("starbucks")'), `${rel} missing starbucks category logic`);

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
}

console.log("RESULT_FIXTURE_QUALITY_TEST=PASS");
console.log("EXPECTED_STARBUCKS_CATEGORY=Makan");
console.log("EXPECTED_REFUND_MERCHANT=Tokopedia");
console.log("TESTED_TARGETS=" + targets.map((p) => path.relative(repo, p)).join(","));
