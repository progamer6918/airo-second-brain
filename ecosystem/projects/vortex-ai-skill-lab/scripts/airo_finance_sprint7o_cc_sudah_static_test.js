const fs = require("fs");
const path = require("path");

function assert(condition, message) {
  if (!condition) throw new Error("FAIL: " + message);
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
  global.UrlFetchApp = {
    fetch: function(url, params) {
      if (url.includes("sendMessage")) {
        const payload = JSON.parse(params.payload);
        global.sendTelegramCalls.push({ chatId: payload.chat_id, text: payload.text });
      }
      return {
        getContentText: function() { return "{}"; }
      };
    }
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
        },
        expireKey: function(key) {
          if (mockCache[key]) {
            mockCache[key].expires = new Date().getTime() - 1000;
          }
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
  global.ContentService = {
    MimeType: { JSON: "application/json" },
    createTextOutput: function(text) {
      return {
        setMimeType: function(type) {
          return {
            getContent: function() { return text; },
            getMimeType: function() { return type; }
          };
        }
      };
    }
  };
`;

const runner = new Function(evalCode + `
  return {
    airoTask9CcPendingPocketCommandMaybeHandleRoute: airoTask9CcPendingPocketCommandMaybeHandleRoute_,
    airoTask9CcSudahNumberMaybeHandleRoute: airoTask9CcSudahNumberMaybeHandleRoute_,
    formatBalanceRupiah: formatBalanceRupiah_,
    airoSprint7AccountContractGetStaticRegistry: airoSprint7AccountContractGetStaticRegistry_,
    writeFinanceEvent: writeFinanceEvent_
  };
`);

const {
  airoTask9CcPendingPocketCommandMaybeHandleRoute,
  airoTask9CcSudahNumberMaybeHandleRoute,
  formatBalanceRupiah,
  airoSprint7AccountContractGetStaticRegistry,
  writeFinanceEvent
} = runner();

// Global mocks
global.sendTelegramCalls = [];
global.sendTelegram_ = function(chatId, text) {
  global.sendTelegramCalls.push({ chatId, text });
};

global.mockPutCcPendingSnapshot = function(entryIds, spreadsheetId) {
  var targetId = spreadsheetId || "1CKARXGurxZ0Rby3-_iisVS0_r65JM6ZaT6tbAJUF7sU";
  var snapshot = {
    target_spreadsheet_id: targetId,
    generated_at: new Date().toISOString(),
    items: entryIds.map(function(id) {
      return {
        cc_entry_id: id,
        amount: 24000,
        description: "mock item",
        billing_cycle_id: ""
      };
    })
  };
  global.CacheService.getScriptCache().put("cc_pending_snapshot_12345", JSON.stringify(snapshot), 900);
};

let activeSs = null;
global.SpreadsheetApp.getActiveSpreadsheet = function() {
  return activeSs;
};

// Global mutation trackers
var ccUpdates = [];
var simulateVerificationFailure = false;

function createMockSheet(name, headers, rowsData) {
  return {
    getName: function() { return name; },
    getLastRow: function() { return rowsData.length; },
    getLastColumn: function() { return headers.length; },
    getSheetId: function() { return 12345; },
    getRange: function(row, col, numRows, numCols) {
      return {
        getValues: function() {
          if (name === "Account Ledger" && simulateVerificationFailure) {
            // Return polluted values to trigger verifyAppendWrite_ failure
            var arr = [];
            var count = numCols || headers.length;
            for (var i = 0; i < count; i++) arr.push("polluted_val");
            return [arr];
          }
          var sliced = rowsData.slice(row - 1, row - 1 + (numRows || 1));
          return sliced.map(r => {
            var rowData = r || [];
            var colSlice = rowData.slice(col - 1, col - 1 + (numCols || 1));
            // Pad if short
            while (colSlice.length < (numCols || 1)) colSlice.push("");
            return colSlice;
          });
        },
        setValue: function(val) {
          ccUpdates.push({ sheet: name, row, col, val });
          if (!rowsData[row - 1]) rowsData[row - 1] = [];
          rowsData[row - 1][col - 1] = val;
        },
        setValues: function(vals) {
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

// Reset functions
var ccHeaders, ccRows, ledgerHeaders, ledgerRows, mockCcSheet, mockLedgerSheet;
function resetMockEnvironment() {
  global.sendTelegramCalls = [];
  ccUpdates = [];
  simulateVerificationFailure = false;
  
  ccHeaders = ["cc_entry_id", "amount", "status_pocket_blu", "description", "merchant_app", "transferred_at", "linked_txn_id", "notes"];
  ccRows = [
    ccHeaders,
    ["cc_entry_001", 24000, "Belum", "cc beli shopee", "", "", "", "cc_purchase"],
    ["cc_entry_002", 57000, "⏳ Belum", "cc bayar pdam", "", "", "", "cc_purchase"],
    ["cc_entry_003", 10000, "Sudah", "cc shopee settled", "", "2026-06-14", "tx_003", "cc_purchase"],
    ["cc_entry_004", 15000, "✅ Sudah", "cc shopee linkless", "", "2026-06-14", "", "cc_purchase"]
  ];

  ledgerHeaders = ["entry_id", "date", "account", "amount_in", "amount_out", "balance", "type", "category", "description", "raw_text", "source_tab", "linked_txn_id", "notes"];
  ledgerRows = [
    ledgerHeaders
  ];

  mockCcSheet = createMockSheet("Credit Card", ccHeaders, ccRows);
  mockLedgerSheet = createMockSheet("Account Ledger", ledgerHeaders, ledgerRows);

  activeSs = createMockSs({
    "💳 Credit Card": mockCcSheet,
    "📒 Account Ledger": mockLedgerSheet
  });
}

console.log("Running airo_finance_sprint7o_cc_sudah_static_test...");

// Test 1: cek tagihan pending cc stores mapping in CacheService
{
  resetMockEnvironment();
  global.CacheService.getScriptCache().clearMock();
  
  const ePending = {
    postData: {
      contents: JSON.stringify({
        message: { text: "cek tagihan pending cc", chat: { id: 12345 } }
      })
    }
  };

  const res = airoTask9CcPendingPocketCommandMaybeHandleRoute(ePending);
  const resultJson = JSON.parse(res.getContent());
  assert(resultJson.ok === true, "Pending command should run successfully");
  assert(resultJson.item_count === 2, "Should have 2 pending items");

  // Verify stored cache mapping
  var cachedStr = global.CacheService.getScriptCache().get("cc_pending_snapshot_12345");
  assert(cachedStr !== null, "Cache key cc_pending_snapshot_12345 must exist");
  var snapshot = JSON.parse(cachedStr);
  assert(snapshot.target_spreadsheet_id === "1CKARXGurxZ0Rby3-_iisVS0_r65JM6ZaT6tbAJUF7sU", "Target spreadsheet ID mismatch");
  assert(snapshot.items.length === 2, "Cache should store 2 items");
  assert(snapshot.items[0].cc_entry_id === "cc_entry_001", "Item index 1 should map to cc_entry_001");
  assert(snapshot.items[1].cc_entry_id === "cc_entry_002", "Item index 2 should map to cc_entry_002");
  console.log("  Case 1 (cek tagihan pending cc stores mapping) passed.");
}

// Test 2: cc sudah 1 resolves to cc_entry_id, not row number, and runs successfully with ledger-first flow
{
  resetMockEnvironment();
  // Populate mapping cache
  global.mockPutCcPendingSnapshot(["cc_entry_001", "cc_entry_002"]);

  const eSudah = {
    postData: {
      contents: JSON.stringify({
        message: { text: "cc sudah 1", chat: { id: 12345 } }
      })
    }
  };

  const res = airoTask9CcSudahNumberMaybeHandleRoute(eSudah);
  const resultJson = JSON.parse(res.getContent());
  
  assert(resultJson.ok === true, "CC sudah 1 should run successfully: " + (resultJson.error || ""));
  assert(resultJson.item === "cc beli shopee", "Mapped description should be cc beli shopee");
  assert(resultJson.amount === 24000, "Mapped amount should be 24000");
  
  // Verify Account Ledger write occurred (writes 2 rows for internal transfer: outflow + inflow)
  assert(ledgerRows.length === 3, "Account Ledger must have 3 rows (header + outflow + inflow)");
  
  var ledgerOutflow = ledgerRows[1];
  assert(ledgerOutflow[0] === "cc_entry_001:out", "Outflow ledger entry_id mismatch");
  assert(ledgerOutflow[2] === "Blu Pocket", "Settlement source account must be exactly Blu Pocket");
  assert(ledgerOutflow[4] === 24000, "Outflow amount out mismatch");
  assert(ledgerOutflow[6] === "transfer_out", "Outflow type mismatch");
  assert(ledgerOutflow[7] === "Transfer", "Outflow category mismatch");
  
  var ledgerInflow = ledgerRows[2];
  assert(ledgerInflow[0] === "cc_entry_001:in", "Inflow ledger entry_id mismatch");
  assert(ledgerInflow[2] === "Blu Pocket CC", "Settlement destination account must be exactly Blu Pocket CC");
  assert(ledgerInflow[3] === 24000, "Inflow amount in mismatch");
  assert(ledgerInflow[6] === "transfer_in", "Inflow type mismatch");
  assert(ledgerInflow[7] === "Transfer", "Inflow category mismatch");

  // Verify Credit Card row updated
  assert(ccRows[1][2] === "✅ Sudah", "Credit Card status must be updated to Sudah");
  assert(ccRows[1][6] === "cc_entry_001", "Credit Card linked_txn_id mismatch");

  // Verify success reply
  assert(global.sendTelegramCalls.length === 1, "Telegram success reply should be sent");
  const successText = global.sendTelegramCalls[0].text;
  assert(successText.includes("✅ Dana CC Disisihkan"), "Success header mismatch");
  assert(successText.includes("Transfer: Blu Pocket → Blu Pocket CC"), "Transfer info mismatch");
  assert(!successText.includes("Blu keluar"), "Must not contain 'Blu keluar'");
  
  console.log("  Case 2 (cc sudah 1 resolves to correct ID and succeeds ledger-first) passed.");
}

// Test 3: expired mapping rejects command
{
  resetMockEnvironment();
  global.CacheService.getScriptCache().clearMock(); // expired / missing

  const eSudah = {
    postData: {
      contents: JSON.stringify({
        message: { text: "cc sudah 1", chat: { id: 12345 } }
      })
    }
  };

  const res = airoTask9CcSudahNumberMaybeHandleRoute(eSudah);
  const resultJson = JSON.parse(res.getContent());
  assert(resultJson.ok === false, "CC sudah 1 must fail due to expired cache");
  assert(resultJson.error === "cc_pending_mapping_expired", "Should return cc_pending_mapping_expired");
  assert(global.sendTelegramCalls[0].text.includes("Nomor pending CC belum terdaftar atau sudah kedaluwarsa"), "Error response mismatch");
  console.log("  Case 3 (expired mapping rejection) passed.");
}

// Test 4: invalid number rejects command
{
  resetMockEnvironment();
  global.mockPutCcPendingSnapshot(["cc_entry_001", "cc_entry_002"]);

  const eSudah = {
    postData: {
      contents: JSON.stringify({
        message: { text: "cc sudah 3", chat: { id: 12345 } }
      })
    }
  };

  const res = airoTask9CcSudahNumberMaybeHandleRoute(eSudah);
  const resultJson = JSON.parse(res.getContent());
  assert(resultJson.ok === false, "Out of range index must fail");
  assert(resultJson.error === "cc_pending_index_out_of_range", "Should return index out of range");
  console.log("  Case 4 (invalid index rejection) passed.");
}

// Test 5: already settled item skips new ledger write
{
  resetMockEnvironment();
  global.mockPutCcPendingSnapshot(["cc_entry_001", "cc_entry_002", "cc_entry_003"]);

  const eSudah = {
    postData: {
      contents: JSON.stringify({
        message: { text: "cc sudah 3", chat: { id: 12345 } }
      })
    }
  };

  const res = airoTask9CcSudahNumberMaybeHandleRoute(eSudah);
  const resultJson = JSON.parse(res.getContent());
  assert(resultJson.ok === true, "Should handle skip gracefully as ok: true");
  assert(resultJson.error === "cc_already_settled", "Should report cc_already_settled");
  assert(ledgerRows.length === 1, "No new ledger write should be made");
  console.log("  Case 5 (already settled skip) passed.");
}

// Test 6: Sudah without linked_txn_id prints audit warning and skips write
{
  resetMockEnvironment();
  global.mockPutCcPendingSnapshot(["cc_entry_001", "cc_entry_002", "cc_entry_003", "cc_entry_004"]);

  const eSudah = {
    postData: {
      contents: JSON.stringify({
        message: { text: "cc sudah 4", chat: { id: 12345 } }
      })
    }
  };

  const res = airoTask9CcSudahNumberMaybeHandleRoute(eSudah);
  const resultJson = JSON.parse(res.getContent());
  assert(resultJson.ok === false, "Should fail audit validation");
  assert(resultJson.error === "CC_STATUS_SUDAH_WITHOUT_LEDGER_LINK", "Should return CC_STATUS_SUDAH_WITHOUT_LEDGER_LINK");
  assert(global.sendTelegramCalls[0].text.includes("Audit Warning"), "Should send audit warning text");
  assert(ledgerRows.length === 1, "No new ledger write should be made");
  console.log("  Case 6 (Sudah without ledger link warning) passed.");
}

// Test 7: ledger write failure blocks CC status update
{
  resetMockEnvironment();
  global.mockPutCcPendingSnapshot(["cc_entry_001", "cc_entry_002"]);

  // Trigger verify failure by simulating value mismatch
  simulateVerificationFailure = true;

  const eSudah = {
    postData: {
      contents: JSON.stringify({
        message: { text: "cc sudah 2", chat: { id: 12345 } }
      })
    }
  };

  const res = airoTask9CcSudahNumberMaybeHandleRoute(eSudah);
  const resultJson = JSON.parse(res.getContent());
  assert(resultJson.ok === false, "Should fail");
  assert(resultJson.error === "cc_ledger_write_verification_failed", "Verification failed expected");
  assert(ccRows[2][2] === "⏳ Belum", "CC status must not be updated if ledger write verification fails");
  console.log("  Case 7 (ledger write failure blocks CC update) passed.");
}

// Test 8: duplicate ledger entry guard
{
  resetMockEnvironment();
  global.mockPutCcPendingSnapshot(["cc_entry_001", "cc_entry_002"]);
  
  // Add duplicate to ledger
  ledgerRows.push(
    ["cc_entry_002", "2026-06-14", "Blu", "", 57000, "", "cc_payment", "Credit Card Payment", "cc bayar pdam", "cc bayar pdam", "Credit Card", "cc_entry_002", ""]
  );

  const eSudah = {
    postData: {
      contents: JSON.stringify({
        message: { text: "cc sudah 2", chat: { id: 12345 } }
      })
    }
  };

  const res = airoTask9CcSudahNumberMaybeHandleRoute(eSudah);
  const resultJson = JSON.parse(res.getContent());
  assert(resultJson.ok === false, "Duplicate entry checking must fail the write");
  assert(resultJson.error === "cc_ledger_duplicate_found", "Should report duplicate found");
  assert(ledgerRows.length === 2, "No new ledger write should be made (length should remain 2)");
  assert(ccRows[2][2] === "⏳ Belum", "CC update should not be made");
  console.log("  Case 8 (duplicate ledger entry guard) passed.");
}

// Test 9: Configured target spreadsheet mismatch aborts before ledger write
{
  resetMockEnvironment();
  global.mockPutCcPendingSnapshot(["cc_entry_001"], "WRONG_SPREADSHEET_ID");
  
  // Temporarily override PropertiesService to return mismatching spreadsheet ID
  var originalGetScriptProperties = global.PropertiesService.getScriptProperties;
  global.PropertiesService.getScriptProperties = function() {
    return {
      getProperty: function(key) {
        if (key === "SPREADSHEET_ID") return "WRONG_SPREADSHEET_ID";
        return "mock_bot_token";
      }
    };
  };

  const eSudah = {
    postData: {
      contents: JSON.stringify({
        message: { text: "cc sudah 1", chat: { id: 12345 } }
      })
    }
  };

  const res = airoTask9CcSudahNumberMaybeHandleRoute(eSudah);
  const resultJson = JSON.parse(res.getContent());
  
  assert(resultJson.ok === false, "Must abort on target spreadsheet mismatch");
  assert(resultJson.reason === "unexpected_target_spreadsheet_id", "Expected unexpected_target_spreadsheet_id");
  assert(ledgerRows.length === 1, "No ledger write must occur on mismatch");
  assert(ccRows[1][2] === "Belum", "CC status must not change on mismatch");

  // Restore
  global.PropertiesService.getScriptProperties = originalGetScriptProperties;
  console.log("  Case 9 (Configured target spreadsheet mismatch) passed.");
}

// Test 10: Snapshot target mismatch aborts before ledger write
{
  resetMockEnvironment();
  // Put snapshot with mismatching spreadsheet ID
  global.mockPutCcPendingSnapshot(["cc_entry_001"], "SOME_OTHER_SPREADSHEET_ID");

  const eSudah = {
    postData: {
      contents: JSON.stringify({
        message: { text: "cc sudah 1", chat: { id: 12345 } }
      })
    }
  };

  const res = airoTask9CcSudahNumberMaybeHandleRoute(eSudah);
  const resultJson = JSON.parse(res.getContent());

  assert(resultJson.ok === false, "Must abort on snapshot spreadsheet ID mismatch");
  assert(resultJson.reason === "target_spreadsheet_mismatch", "Expected target_spreadsheet_mismatch");
  assert(ledgerRows.length === 1, "No ledger write must occur on snapshot target mismatch");
  
  console.log("  Case 10 (Snapshot target mismatch) passed.");
}

// Test 11: Verify static prohibitions, registry, and copy assertions
{
  // 1. cc sudah route does not use SpreadsheetApp.getActiveSpreadsheet()
  const routeFuncStr = airoTask9CcSudahNumberMaybeHandleRoute.toString();
  assert(!routeFuncStr.includes("getActiveSpreadsheet"), "cc sudah handler must not use getActiveSpreadsheet()");
  
  // 2. cc sudah route uses airoTask9OpenConfiguredSpreadsheet_
  assert(routeFuncStr.includes("airoTask9OpenConfiguredSpreadsheet_"), "cc sudah handler must use airoTask9OpenConfiguredSpreadsheet_()");
  
  // 3. Account registry has Blu Pocket CC registered
  const registryObj = airoSprint7AccountContractGetStaticRegistry();
  const registeredAcc = registryObj.find(acc => acc.account_name === "Blu Pocket CC");
  assert(registeredAcc !== undefined, "Blu Pocket CC must be registered in static account registry");
  assert(registeredAcc.provider === "Blu", "Provider must be Blu");
  assert(registeredAcc.account_type === "bank", "Type must be bank");
  
  // 4. Finance events deprecated (and not written)
  const feResult = writeFinanceEvent(activeSs, {});
  assert(feResult.finance_events_write_performed === false || feResult.status === 'skipped', "Finance events must not be written");
  
  console.log("  Case 11 (Prohibitions and Static Invariants) passed.");
}

console.log("All static tests for cc sudah command passed successfully!");
