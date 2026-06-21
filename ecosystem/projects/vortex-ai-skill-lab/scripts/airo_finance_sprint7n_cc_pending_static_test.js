const fs = require("fs");
const path = require("path");

function assert(condition, message) {
  if (!condition) throw new Error("FAIL: " + message);
}

const repoRoot = path.resolve(__dirname, "..");
const src = fs.readFileSync(path.join(repoRoot, "apps-script-live/AIRO_Finance_Multitab_Final_v1.js"), "utf8");

// Mock block
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

  var mockCache = {};
  global.CacheService = {
    getScriptCache: function() {
      return {
        put: function(key, val, ttl) {
          mockCache[key] = val;
        },
        get: function(key) {
          return mockCache[key] || null;
        }
      };
    }
  };
`;

const runner = new Function(evalCode + `
  return {
    airoTask9CcPendingPocketCommandMaybeHandleRoute: airoTask9CcPendingPocketCommandMaybeHandleRoute_,
    formatBalanceRupiah: formatBalanceRupiah_
  };
`);

const { airoTask9CcPendingPocketCommandMaybeHandleRoute, formatBalanceRupiah } = runner();

// Setup mock spreadsheet helpers
function createMockSs(sheets) {
  return {
    getSheetByName: function(name) {
      return this.sheets[name] || null;
    },
    getSheets: function() {
      var self = this;
      return Object.keys(this.sheets).map(function(k) {
        var sheetObj = self.sheets[k];
        sheetObj.getName = function() { return k; };
        return sheetObj;
      });
    },
    sheets: sheets
  };
}

// Global mocks
global.sendTelegramCalls = [];
global.sendTelegram_ = function(chatId, text) {
  global.sendTelegramCalls.push({ chatId, text });
};

let activeSs = null;
global.SpreadsheetApp.getActiveSpreadsheet = function() {
  return activeSs;
};

console.log("Running airo_finance_sprint7n_cc_pending_static_test...");

// 1. Command detection check
{
  global.sendTelegramCalls = [];
  const eUnrelated = {
    postData: {
      contents: JSON.stringify({
        message: { text: "unrelated command", chat: { id: 12345 } }
      })
    }
  };
  const res = airoTask9CcPendingPocketCommandMaybeHandleRoute(eUnrelated);
  assert(res === null, "Unrelated command must return null immediately");
  assert(global.sendTelegramCalls.length === 0, "Unrelated command must not trigger telegram reply");
  console.log("  Case 1 (Command detection check) passed.");
}

// 2. Pending filter check (excluding Sudah/Paid/Posted/Transferred, ignore empty, require amount > 0, require description)
{
  global.sendTelegramCalls = [];
  // Mock headers: cc_entry_id, amount, status_pocket_blu, description, merchant_app
  const ccHeaders = ["cc_entry_id", "amount", "status_pocket_blu", "description", "merchant_app"];
  const ccRows = [
    // Header row
    ccHeaders,
    // Row 1: pending, description present
    ["id1", 35000, "Belum", "Nasgor ShopeeFood", ""],
    // Row 2: pending, falls back to merchant_app
    ["id2", 81000, "⏳ Belum", "", "UPS Wifi Shopee"],
    // Row 3: exclude - status contains "sudah"
    ["id3", 15000, "sudah disiapkan", "Exclude sudah", ""],
    // Row 4: exclude - status contains "paid"
    ["id4", 20000, "PAID", "Exclude paid", ""],
    // Row 5: exclude - status contains "posted"
    ["id5", 25000, "Posted", "Exclude posted", ""],
    // Row 6: exclude - status contains "transferred"
    ["id6", 30000, "transferred", "Exclude transferred", ""],
    // Row 7: ignore empty row / amount = 0
    ["id7", 0, "Belum", "Empty amount", ""],
    // Row 8: ignore row with blank desc and merchant
    ["id8", 50000, "Belum", "", ""]
  ];

  const mockCcSheet = {
    getLastRow: function() { return ccRows.length; },
    getLastColumn: function() { return ccHeaders.length; },
    getRange: function(row, col, numRows, numCols) {
      assert(row >= 1, "Row must be 1-based");
      return {
        getValues: function() {
          // Slice the rows requested
          return ccRows.slice(row - 1, row - 1 + numRows).map(r => r.slice(col - 1, col - 1 + numCols));
        }
      };
    }
  };

  activeSs = createMockSs({
    "💳 Credit Card": mockCcSheet
  });

  const ePending = {
    postData: {
      contents: JSON.stringify({
        message: { text: "cek tagihan pending cc", chat: { id: 12345 } }
      })
    }
  };

  const res = airoTask9CcPendingPocketCommandMaybeHandleRoute(ePending);
  assert(res !== null, "Command should handle route");
  
  // Verify returned json structure
  const resultJson = JSON.parse(res.getContent());
  console.log("DEBUG: resultJson =", resultJson);
  assert(resultJson.ok === true, "Result ok should be true");
  assert(resultJson.item_count === 2, "Should find exactly 2 pending items");
  assert(resultJson.total_amount === 116000, "Total pending amount should be 116000");

  // Verify Telegram reply
  assert(global.sendTelegramCalls.length === 1, "Telegram reply should be sent");
  const replyText = global.sendTelegramCalls[0].text;
  assert(replyText.includes("💳 Pending Dana CC"), "Header mismatch");
  assert(replyText.includes("1. Nasgor ShopeeFood — Rp35.000"), "First item display mismatch");
  assert(replyText.includes("2. UPS Wifi Shopee — Rp81.000"), "Second item fallback display mismatch");
  assert(replyText.includes("Total belum disisihkan ke Blu Pocket CC: Rp116.000"), "Total formatted mismatch");
  assert(replyText.includes("cc sudah <nomor>"), "Footer mismatch");

  // Verify contract requirements
  // 1. pending command uses configured target workbook helper
  assert(src.includes("airoTask9OpenConfiguredSpreadsheet_"), "Must use configured target workbook helper");
  // 2. pending command stores target_spreadsheet_id
  const cachedVal = global.CacheService.getScriptCache().get("cc_pending_snapshot_12345");
  assert(cachedVal !== null, "Cache key cc_pending_snapshot_12345 must exist");
  const snapshot = JSON.parse(cachedVal);
  assert(snapshot !== null && snapshot.target_spreadsheet_id !== undefined, "Must store target_spreadsheet_id in CacheService");
  // 3. pending command remains read-only
  assert(resultJson.write_performed === false, "Pending command must remain read-only");
  // 4. pending reply says "Total belum disisihkan ke Blu Pocket CC"
  assert(replyText.includes("Total belum disisihkan ke Blu Pocket CC"), "Total footer wording mismatch");

  console.log("  Case 2 (Pending filter & formatting check) passed.");
}

// 3. Empty state check
{
  global.sendTelegramCalls = [];
  const ccHeaders = ["cc_entry_id", "amount", "status_pocket_blu", "description", "merchant_app"];
  const ccRows = [
    ccHeaders,
    ["id3", 15000, "sudah disiapkan", "Exclude sudah", ""]
  ];

  const mockCcSheet = {
    getLastRow: function() { return ccRows.length; },
    getLastColumn: function() { return ccHeaders.length; },
    getRange: function(row, col, numRows, numCols) {
      return {
        getValues: function() {
          return ccRows.slice(row - 1, row - 1 + numRows).map(r => r.slice(col - 1, col - 1 + numCols));
        }
      };
    }
  };

  activeSs = createMockSs({
    "💳 Credit Card": mockCcSheet
  });

  const ePending = {
    postData: {
      contents: JSON.stringify({
        message: { text: "cek tagihan pending cc", chat: { id: 12345 } }
      })
    }
  };

  const res = airoTask9CcPendingPocketCommandMaybeHandleRoute(ePending);
  const resultJson = JSON.parse(res.getContent());
  assert(resultJson.ok === true, "Result ok should be true");
  assert(resultJson.item_count === 0, "Should find 0 pending items");
  
  assert(global.sendTelegramCalls.length === 1, "Telegram reply should be sent");
  assert(global.sendTelegramCalls[0].text === "Tidak ada pending CC.", "Empty state reply mismatch");
  console.log("  Case 3 (Empty state check) passed.");
}

// 4. Missing schema/tab check
{
  global.sendTelegramCalls = [];
  activeSs = createMockSs({}); // empty sheets

  const ePending = {
    postData: {
      contents: JSON.stringify({
        message: { text: "cek tagihan pending cc", chat: { id: 12345 } }
      })
    }
  };

  const res = airoTask9CcPendingPocketCommandMaybeHandleRoute(ePending);
  const resultJson = JSON.parse(res.getContent());
  assert(resultJson.ok === false, "Result ok should be false");
  assert(resultJson.error === "credit_card_tab_not_found", "Should report credit_card_tab_not_found");
  assert(global.sendTelegramCalls.length === 1, "Should notify user about missing tab");
  assert(global.sendTelegramCalls[0].text.includes("Error: Tab Credit Card tidak ditemukan."), "Error text mismatch");
  console.log("  Case 4 (Missing tab check) passed.");
}

console.log("All airo_finance_sprint7n_cc_pending_static_test cases passed!");
