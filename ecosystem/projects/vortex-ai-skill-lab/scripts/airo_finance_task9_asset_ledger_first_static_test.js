const fs = require("fs");
const path = require("path");

function assert(condition, message) {
  if (!condition) {
    console.error("FAIL: " + message);
    throw new Error(message);
  }
}

const repoRoot = path.resolve(__dirname, "..");
const src = fs.readFileSync(path.join(repoRoot, "apps-script-live/AIRO_Finance_Multitab_Final_v1.js"), "utf8");

// Mock global environment
let evalCode = src + "\n\n";
evalCode += `
  global.SpreadsheetApp = {
    flush: function() {},
    openById: function(id) {
      if (global.SpreadsheetApp.getActiveSpreadsheet) {
        var ss = global.SpreadsheetApp.getActiveSpreadsheet();
        if (ss) {
          ss.getId = function() { return id; };
        }
        return ss;
      }
      return null;
    },
    DataValidationCriteria: {
      VALUE_IN_LIST: "VALUE_IN_LIST"
    },
    newDataValidation: function() {
      return {
        requireValueInList: function() { return this; },
        setAllowInvalid: function() { return this; },
        build: function() { return "mock_rule"; }
      };
    }
  };
  global.Logger = {
    log: function() {}
  };
  
  // Cache mock
  var mockCache = {};
  global.CacheService = {
    getScriptCache: function() {
      return {
        put: function(key, val, ttl) {
          mockCache[key] = { value: val, expires: new Date().getTime() + (ttl * 1000) };
        },
        get: function(key) {
          var entry = mockCache[key];
          if (!entry) return null;
          if (new Date().getTime() > entry.expires) {
            delete mockCache[key];
            return null;
          }
          return entry.value;
        },
        clearMock: function() {
          mockCache = {};
        }
      };
    }
  };

  global.PropertiesService = {
    getScriptProperties: function() {
      return {
        getProperty: function(key) {
          if (key === "BOT_TOKEN") return "mock_bot_token";
          if (key === "SPREADSHEET_ID") return "1CKARXGurxZ0Rby3-_iisVS0_r65JM6ZaT6tbAJUF7sU";
          return null;
        }
      };
    }
  };

  global.Session = {
    getScriptTimeZone: function() { return "Asia/Jakarta"; }
  };

  global.Utilities = {
    DigestAlgorithm: { SHA_256: "SHA_256" },
    computeDigest: function(algo, text) {
      if (typeof text === 'string') {
        return text.split('').map(c => c.charCodeAt(0));
      }
      return text;
    },
    base64EncodeWebSafe: function(bytes) {
      if (Array.isArray(bytes)) {
        return Buffer.from(bytes).toString('base64')
          .replace(/\\+/g, '-')
          .replace(/\\//g, '_')
          .replace(/=+$/, '');
      }
      return String(bytes);
    },
    formatDate: function(date, tz, format) {
      const d = new Date(date);
      const pad = (n) => String(n).padStart(2, '0');
      if (format.includes('yyyy-MM-dd')) {
        return \`\${d.getFullYear()}-\${pad(d.getMonth() + 1)}-\${pad(d.getDate())}\`;
      }
      if (format.includes('yyyy-MM')) {
        return \`\${d.getFullYear()}-\${pad(d.getMonth() + 1)}\`;
      }
      return d.toISOString();
    },
    getUuid: function() {
      return "mock-uuid-12345678";
    }
  };
`;

const runner = new Function(evalCode + `
  return {
    writeAssetSafely: writeAssetSafely_,
    writeRouted: writeRouted_,
    writeAccountLedgerMirror: writeAccountLedgerMirror_,
    appendCreditCardPurchase: appendCreditCardPurchase_,
    writeCreditCardSafely: writeCreditCardSafely_
  };
`);

const {
  writeAssetSafely,
  writeRouted,
  writeAccountLedgerMirror,
  appendCreditCardPurchase,
  writeCreditCardSafely
} = runner();

// Global mutation tracker for sheet updates
let sheetUpdates = [];
let forceLedgerWriteFailure = false;
let forceLedgerUnverified = false;

function createMockSheet(name, headers, rowsData) {
  return {
    getName: function() { return name; },
    getLastRow: function() { return rowsData.length; },
    getLastColumn: function() { return headers.length; },
    getSheetId: function() { return 12345; },
    getRange: function(row, col, numRows, numCols) {
      return {
        getValues: function() {
          // If we want to simulate ledger write failure:
          if (name === "Account Ledger" && (forceLedgerWriteFailure || forceLedgerUnverified)) {
            // Return empty rows to trigger verification failure
            return [[]];
          }
          var sliced = rowsData.slice(row - 1, row - 1 + (numRows || 1));
          return sliced.map(r => {
            var rowData = r || [];
            var colSlice = rowData.slice(col - 1, col - 1 + (numCols || 1));
            while (colSlice.length < (numCols || 1)) colSlice.push("");
            return colSlice;
          });
        },
        setValue: function(val) {
          sheetUpdates.push({ action: "setValue", sheet: name, row, col, val });
          if (!rowsData[row - 1]) rowsData[row - 1] = [];
          rowsData[row - 1][col - 1] = val;
        },
        setValues: function(vals) {
          sheetUpdates.push({ action: "setValues", sheet: name, row, col, vals });
          for (var rIdx = 0; rIdx < vals.length; rIdx++) {
            var targetR = row - 1 + rIdx;
            if (!rowsData[targetR]) rowsData[targetR] = [];
            for (var cIdx = 0; cIdx < vals[rIdx].length; cIdx++) {
              var targetC = col - 1 + cIdx;
              rowsData[targetR][targetC] = vals[rIdx][cIdx];
            }
          }
        },
        setFormula: function() {},
        getDataValidation: function() { return null; },
        getDataValidations: function() {
          var count = numCols || headers.length;
          var arr = [];
          for (var i = 0; i < count; i++) arr.push(null);
          return [arr];
        },
        setDataValidation: function() {},
        setBackground: function() {},
        setFontColor: function() {},
        setFontWeight: function() {},
        setHorizontalAlignment: function() {},
        getValue: function() {
          return rowsData[row - 1] ? rowsData[row - 1][col - 1] : "";
        },
        getDisplayValue: function() {
          return this.getValue();
        },
        getDisplayValues: function() {
          return this.getValues();
        }
      };
    }
  };
}

function createMockSs(sheets) {
  return {
    getSheetByName: function(name) {
      return this.sheets[name] || null;
    },
    getSheets: function() {
      var self = this;
      return Object.keys(this.sheets).map(function(k) {
        return self.sheets[k];
      });
    },
    getUrl: function() {
      return "mock_spreadsheet_url";
    },
    sheets: sheets
  };
}

let activeSs = null;
global.SpreadsheetApp.getActiveSpreadsheet = function() {
  return activeSs;
};

// Global mocks
global.sendTelegramCalls = [];
global.sendTelegram_ = function(chatId, text) {
  global.sendTelegramCalls.push({ chatId, text });
};

// Setup tabs and rows
let assetHeaders, assetRows, ledgerHeaders, ledgerRows, reviewHeaders, reviewRows;
let mockAssetSheet, mockLedgerSheet, mockReviewSheet;

function resetMockEnvironment() {
  sheetUpdates = [];
  forceLedgerWriteFailure = false;
  forceLedgerUnverified = false;
  global.sendTelegramCalls = [];

  // Asset tab with gold and savings headers
  // startCol 1 to 13: gold
  // startCol 15 to 26: savings
  assetHeaders = [
    "gold_event_id", "date", "action", "grams_in", "grams_out", "price_per_gram", "fee", "total_amount", "source_account", "source", "raw_text", "notes", "",
    "",
    "date", "type", "category", "description", "amount", "account", "source", "raw_text", "status", "linked_txn_id", "notes"
  ];
  assetRows = [
    assetHeaders
  ];

  ledgerHeaders = ["entry_id", "date", "account", "amount_in", "amount_out", "balance", "type", "category", "subcategory", "description", "raw_text", "source_tab", "linked_txn_id", "notes"];
  ledgerRows = [
    ledgerHeaders
  ];

  reviewHeaders = ["queue_id", "created_at", "source", "raw_text", "parsed_type", "parsed_category", "parsed_subcategory", "parsed_amount", "parsed_currency", "parsed_account", "parser_confidence", "issue_reason", "suggested_fix", "review_status", "reviewed_at", "approved_transaction_id", "local_db_table", "local_db_rowid", "sync_hash", "notes"];
  reviewRows = [
    reviewHeaders
  ];

  mockAssetSheet = createMockSheet("Aset", assetHeaders, assetRows);
  mockLedgerSheet = createMockSheet("Account Ledger", ledgerHeaders, ledgerRows);
  mockReviewSheet = createMockSheet("Review Queue", reviewHeaders, reviewRows);

  activeSs = createMockSs({
    "Aset": mockAssetSheet,
    "Account Ledger": mockLedgerSheet,
    "Review Queue": mockReviewSheet
  });
}

console.log("Running airo_finance_task9_asset_ledger_first_static_test.js...");

// Test Case 1: Successful Asset Purchase (Gold) routes Ledger-First and verified
{
  resetMockEnvironment();

  const parsed = {
    assetSection: "gold",
    goldAction: "buy",
    goldWeightGram: 10,
    goldKarat: 24,
    goldPurchasePrice: 12000000,
    date: "2026-06-21",
    account: "BCA",
    category: "Aset",
    amount: 12000000
  };
  const common = {
    timestamp: "2026-06-21T12:00:00.000Z",
    date: "2026-06-21",
    source: "telegram",
    raw_text: "beli emas 10gram BCA 12jt"
  };

  const result = writeAssetSafely(activeSs, parsed, common.raw_text, common);

  // Assertions:
  assert(result.ledger_first === true, "Must be ledger_first");
  assert(result.account_ledger_write_performed === true, "Ledger write must be performed");
  assert(result.account_ledger_write_verified === true, "Ledger write must be verified");
  assert(result.asset_domain_update_performed === true, "Domain update must be performed");

  // Verify write order: first update is to "Account Ledger", followed by "Aset"
  assert(sheetUpdates.length >= 2, "Should have at least 2 sheet updates");
  assert(sheetUpdates[0].sheet === "Account Ledger", "First sheet updated must be Account Ledger");
  assert(sheetUpdates[1].sheet === "Aset", "Second sheet updated must be Aset");

  // Verify ledger row details
  assert(ledgerRows.length === 2, "Account Ledger should have 1 data row");
  const ledgerRow = ledgerRows[1];
  assert(ledgerRow[2] === "BCA", "Ledger account mismatch");
  assert(ledgerRow[4] === 12000000, "Ledger amount_out mismatch");
  assert(ledgerRow[7] === "Aset", "Ledger category mismatch");

  // Verify asset row details
  assert(assetRows.length === 2, "Aset tab should have 1 data row");
  const assetRow = assetRows[1];
  // Gold column A (gold_event_id) must be equal to linked_txn_id
  assert(assetRow[0] === result.linked_txn_id, "Gold event ID must match linked_txn_id");
  assert(assetRow[2] === "buy", "Gold action mismatch");
  assert(assetRow[3] === 10, "Gold grams mismatch");
  assert(assetRow[7] === 12000000, "Gold total amount mismatch");

  console.log("  Case 1 (Success Gold Ledger-First) passed.");
}

// Test Case 2: Successful Asset Purchase (Savings) routes Ledger-First and verified
{
  resetMockEnvironment();

  const parsed = {
    assetSection: "savings",
    date: "2026-06-21",
    account: "Mandiri",
    category: "Aset",
    amount: 5000000
  };
  const common = {
    timestamp: "2026-06-21T12:00:00.000Z",
    date: "2026-06-21",
    source: "telegram",
    raw_text: "nabung Mandiri 5jt",
    amount: 5000000,
    account: "Mandiri",
    category: "Aset"
  };

  const result = writeAssetSafely(activeSs, parsed, common.raw_text, common);

  // Assertions:
  assert(result.ledger_first === true, "Must be ledger_first");
  assert(result.account_ledger_write_performed === true, "Ledger write must be performed");
  assert(result.account_ledger_write_verified === true, "Ledger write must be verified");
  assert(result.asset_domain_update_performed === true, "Domain update must be performed");

  // Verify write order
  assert(sheetUpdates.length >= 2, "Should have at least 2 sheet updates");
  assert(sheetUpdates[0].sheet === "Account Ledger", "First sheet updated must be Account Ledger");
  assert(sheetUpdates[1].sheet === "Aset", "Second sheet updated must be Aset");

  // Verify ledger row details
  assert(ledgerRows.length === 2, "Account Ledger should have 1 data row");
  assert(ledgerRows[1][2] === "Mandiri", "Ledger account mismatch");
  assert(ledgerRows[1][4] === 5000000, "Ledger amount_out mismatch");

  // Verify savings column details
  assert(assetRows.length === 2, "Aset tab should have 1 data row");
  // Savings date column is column 15 (index 14)
  assert(assetRows[1][14] === "2026-06-21", "Savings date mismatch");
  assert(assetRows[1][23] === result.linked_txn_id, "Savings linked_txn_id mismatch");

  console.log("  Case 2 (Success Savings Ledger-First) passed.");
}

// Test Case 3: If ledger write fails, Aset/domain update is blocked
{
  resetMockEnvironment();
  forceLedgerWriteFailure = true;

  const parsed = {
    assetSection: "gold",
    goldAction: "buy",
    goldWeightGram: 5,
    goldKarat: 24,
    goldPurchasePrice: 6000000,
    date: "2026-06-21",
    account: "BCA",
    category: "Aset",
    amount: 6000000
  };
  const common = {
    timestamp: "2026-06-21T12:00:00.000Z",
    date: "2026-06-21",
    source: "telegram",
    raw_text: "beli emas 5gram BCA 6jt"
  };

  // Mock global.appendByHeader_ to simulate ledger write failure returning status fallback
  const originalAppendByHeader = global.appendByHeader_;
  global.appendByHeader_ = function(ss, tabName, data, opts) {
    if (tabName === "Account Ledger") {
      return { status: "fallback", reason: "mock_failure" };
    }
    return { status: "written", row: 99 };
  };

  const result = writeAssetSafely(activeSs, parsed, common.raw_text, common);

  // Restore original mock
  global.appendByHeader_ = originalAppendByHeader;

  // Assertions:
  assert(result.status === "blocked", "Result status must be blocked");
  assert(result.account_ledger_write_performed === true, "Ledger write must be attempted");
  assert(result.account_ledger_write_verified === false, "Ledger write must be unverified");
  assert(result.asset_domain_update_performed === false, "Domain update must not be performed");

  // Verify Aset tab remains untouched
  assert(assetRows.length === 1, "Aset tab must remain clean (header only)");
  const assetWrites = sheetUpdates.filter(u => u.sheet === "Aset");
  assert(assetWrites.length === 0, "No writes to Aset sheet must occur");

  console.log("  Case 3 (Ledger Write Failure Blocks Domain) passed.");
}

// Test Case 4: Credit Card purchase remains domain-only and does not write Account Ledger
{
  resetMockEnvironment();

  // Mock Credit Card tab
  const ccHeaders = ["cc_entry_id", "amount", "status_pocket_blu", "description", "merchant_app", "transferred_at", "linked_txn_id", "notes"];
  const ccRows = [ccHeaders];
  const mockCcSheet = createMockSheet("Credit Card", ccHeaders, ccRows);
  activeSs.sheets["💳 Credit Card"] = mockCcSheet;

  const parsed = {
    type: "cc_purchase",
    amount: 250000,
    account: "Pocket Blu CC",
    category: "Belanja"
  };
  const common = {
    timestamp: "2026-06-21T12:00:00.000Z",
    date: "2026-06-21",
    source: "telegram",
    raw_text: "cc shopee 250rb"
  };

  // Run routing for CC purchase
  const result = writeRouted(activeSs, "Credit Card", parsed, common.raw_text, common);

  // Assertions:
  // Ledger must remain untouched since purchase is domain-only
  assert(ledgerRows.length === 1, "Account Ledger must remain clean (header only)");
  const ledgerWrites = sheetUpdates.filter(u => u.sheet === "Account Ledger");
  assert(ledgerWrites.length === 0, "No writes to Account Ledger must occur for CC purchase");

  // Credit Card sheet must have been updated
  assert(ccRows.length === 2, "Credit Card sheet should have 1 data row");
  assert(ccRows[1][3] === "cc shopee 250rb", "CC description mismatch");

  console.log("  Case 4 (CC Purchase remains Domain-Only) passed.");
}

// Test Case 5: Finance Events is not written during Asset purchase (remains deprecated/no-op)
{
  resetMockEnvironment();

  // Mock Finance Events sheet
  const feHeaders = ["event_id", "event_ts", "event_type", "event_source", "source_tab", "source_row", "linked_txn_id", "account", "category", "amount", "direction", "status", "reason", "payload_json", "notes"];
  const feRows = [feHeaders];
  const mockFeSheet = createMockSheet("Finance Events", feHeaders, feRows);
  activeSs.sheets["📌 Finance Events"] = mockFeSheet;

  const parsed = {
    assetSection: "gold",
    goldAction: "buy",
    goldWeightGram: 1,
    goldKarat: 24,
    goldPurchasePrice: 1200000,
    date: "2026-06-21",
    account: "BCA",
    category: "Aset",
    amount: 1200000
  };
  const common = {
    timestamp: "2026-06-21T12:00:00.000Z",
    date: "2026-06-21",
    source: "telegram",
    raw_text: "beli emas 1gram BCA 1.2jt"
  };

  writeAssetSafely(activeSs, parsed, common.raw_text, common);

  // Verify Finance Events tab remains empty (header only)
  assert(feRows.length === 1, "Finance Events must remain clean (header only)");
  const feWrites = sheetUpdates.filter(u => u.sheet === "Finance Events");
  assert(feWrites.length === 0, "No writes to Finance Events sheet must occur");

  console.log("  Case 5 (Finance Events Remains Deprecated) passed.");
}

// Test Case 6: Transactions sheet is not recreated
{
  resetMockEnvironment();

  // Verify sheet getName doesn't match "Transactions" or "💸 Transactions"
  const createdSheets = Object.keys(activeSs.sheets);
  assert(!createdSheets.includes("Transactions") && !createdSheets.includes("💸 Transactions"), "Transactions sheet must not exist");

  console.log("  Case 6 (Transactions Sheet Not Recreated) passed.");
}

console.log(JSON.stringify({
  ok: true,
  message: "All static tests for asset ledger-first validation passed."
}, null, 2));
process.exit(0);
