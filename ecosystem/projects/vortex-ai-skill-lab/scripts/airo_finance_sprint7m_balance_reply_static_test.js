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
    flush: function() {}
  };
  global.Logger = {
    log: function() {}
  };
`;

const runner = new Function(evalCode + `
  return {
    formatBalanceRupiah: formatBalanceRupiah_,
    airoBuildFinanceWriteSuccessReply: airoBuildFinanceWriteSuccessReply_
  };
`);

const { formatBalanceRupiah, airoBuildFinanceWriteSuccessReply } = runner();

function createMockSs(sheets) {
  return {
    getSheetByName: function(name) {
      return this.sheets[name] || null;
    },
    getSheets: function() {
      var self = this;
      return Object.keys(this.sheets).map(function(k) {
        return {
          getName: function() { return k; },
          getRange: self.sheets[k].getRange
        };
      });
    },
    sheets: sheets
  };
}

console.log("Running airo_finance_sprint7m_balance_reply_static_test...");

// Test formatBalanceRupiah_
assert(formatBalanceRupiah(1234567) === "Rp1.234.567", "formatBalanceRupiah of positive value failed");
assert(formatBalanceRupiah(0) === "Rp0", "formatBalanceRupiah of zero failed");
assert(formatBalanceRupiah(-50000) === "-Rp50.000", "formatBalanceRupiah of negative value failed");

// Test Cases

// Case 1: Standard Outflow
{
  const mockSs = createMockSs({
    "📒 Account Ledger": {
      getRange: function(row, col, rows, cols) {
        return {
          getValues: function() {
            // Row details: Account, Amount In, Amount Out, Balance
            return [["BCA", "", 25000, 1234567]];
          }
        };
      }
    }
  });
  const parsed = { account: "BCA", amount: 25000, category: "Kopi" };
  const routedResult = { status: "written", writtenTab: "📒 Account Ledger", row: 10 };
  const reply = airoBuildFinanceWriteSuccessReply(mockSs, "📒 Account Ledger", "📒 Account Ledger", parsed, routedResult, "https://mock-url");
  
  assert(reply.includes("✅ Transaksi dicatat."), "Case 1 should mention Transaksi dicatat");
  assert(reply.includes("BCA keluar Rp25.000"), "Case 1 should mention BCA keluar Rp25.000");
  assert(reply.includes("Kategori: Kopi"), "Case 1 should mention Kopi category");
  assert(reply.includes("Saldo BCA sekarang: Rp1.234.567"), "Case 1 should mention Saldo BCA sekarang: Rp1.234.567");
  console.log("  Case 1 (Standard Outflow) passed.");
}

// Case 2: Standard Inflow
{
  const mockSs = createMockSs({
    "📒 Account Ledger": {
      getRange: function(row, col, rows, cols) {
        return {
          getValues: function() {
            return [["Blu", 100000, "", 1234567]];
          }
        };
      }
    }
  });
  const parsed = { account: "Blu", amount: 100000, category: "Refund" };
  const routedResult = { status: "written", writtenTab: "📒 Account Ledger", row: 12 };
  const reply = airoBuildFinanceWriteSuccessReply(mockSs, "📒 Account Ledger", "📒 Account Ledger", parsed, routedResult, "https://mock-url");

  assert(reply.includes("✅ Transaksi dicatat."), "Case 2 should mention Transaksi dicatat");
  assert(reply.includes("Blu masuk Rp100.000"), "Case 2 should mention Blu masuk Rp100.000");
  assert(reply.includes("Kategori: Refund"), "Case 2 should mention Refund category");
  assert(reply.includes("Saldo Blu sekarang: Rp1.234.567"), "Case 2 should mention Saldo Blu sekarang: Rp1.234.567");
  console.log("  Case 2 (Standard Inflow) passed.");
}

// Case 3: Transfer
{
  const mockSs = createMockSs({
    "📒 Account Ledger": {
      getRange: function(row, col, rows, cols) {
        return {
          getValues: function() {
            if (row === 5) {
              // Outflow: BCA
              return [["BCA", "", 50000, 950000]];
            } else {
              // Inflow: Blu
              return [["Blu", 50000, "", 300000]];
            }
          }
        };
      }
    }
  });
  const parsed = { amount: 50000 };
  const routedResult = {
    status: "written",
    writtenTab: "📒 Account Ledger",
    transferInternal: true,
    sourceAccount: "BCA",
    targetAccount: "Blu",
    accountLedgerRows: [5, 6]
  };
  const reply = airoBuildFinanceWriteSuccessReply(mockSs, "📒 Account Ledger", "📒 Account Ledger", parsed, routedResult, "https://mock-url");

  assert(reply.includes("✅ Transfer dicatat."), "Case 3 should mention Transfer dicatat");
  assert(reply.includes("BCA → Blu: Rp50.000"), "Case 3 should format transfer header");
  assert(reply.includes("Saldo BCA sekarang: Rp950.000"), "Case 3 should show source balance");
  assert(reply.includes("Saldo Blu sekarang: Rp300.000"), "Case 3 should show destination balance");
  console.log("  Case 3 (Transfer) passed.");
}

// Case 4: CC purchase domain-only (no balance displayed)
{
  const parsed = { account: "Credit Card", amount: 150000, category: "Groceries" };
  const routedResult = { status: "written", writtenTab: "💳 Credit Card", row: 15 };
  const reply = airoBuildFinanceWriteSuccessReply(null, "💳 Credit Card", "💳 Credit Card", parsed, routedResult, "https://mock-url");

  assert(!reply.includes("Saldo"), "Case 4 should not include any wallet balance");
  assert(reply.includes("Tercatat ke Google Sheet."), "Case 4 fallback message check");
  console.log("  Case 4 (CC purchase domain-only) passed.");
}

// Case 5: Fallback balance read failure (does not crash reply)
{
  const mockSs = createMockSs({
    "📒 Account Ledger": {
      getRange: function(row, col, rows, cols) {
        throw new Error("Simulated balance read failure");
      }
    }
  });
  const parsed = { account: "BCA", amount: 25000, category: "Kopi" };
  const routedResult = { status: "written", writtenTab: "📒 Account Ledger", row: 10 };
  const reply = airoBuildFinanceWriteSuccessReply(mockSs, "📒 Account Ledger", "📒 Account Ledger", parsed, routedResult, "https://mock-url");

  assert(reply.includes("✅ Transaksi dicatat."), "Case 5 should mention Transaksi dicatat");
  assert(reply.includes("BCA keluar Rp25.000"), "Case 5 should mention BCA keluar Rp25.000");
  assert(reply.includes("Saldo terbaru belum bisa dibaca otomatis. Cek Account Ledger untuk verifikasi."), "Case 5 should display read failure fallback");
  console.log("  Case 5 (Fallback balance read failure) passed.");
}

console.log("All sprint7m_balance_reply_static_test cases passed!");
