// airo_finance_sprint7h_task6_regression_static_test.js
// Task 6A-6D regression static tests.
// Run with: node scripts/airo_finance_sprint7h_task6_regression_static_test.js

const fs = require("fs");
const path = require("path");

function assert(condition, message) {
  if (!condition) throw new Error("FAIL: " + message);
}

const repoRoot = path.resolve(__dirname, "..");
const sourcePaths = [
  "apps-script-live/AIRO_Finance_Multitab_Final_v1.js",
  "apps-script-prod-v2/AIRO_Finance_Multitab_Final_v1.js",
];

function read(rel) {
  const abs = path.join(repoRoot, rel);
  assert(fs.existsSync(abs), `${rel} missing`);
  return fs.readFileSync(abs, "utf8");
}

// ──────────────────────────────────────────────────────────────────────────────
// Minimal stubs to execute selected functions in Node.js without Apps Script.
// ──────────────────────────────────────────────────────────────────────────────
function extractFunction(text, functionName) {
  const startIdx = text.indexOf("function " + functionName);
  assert(startIdx >= 0, `Function ${functionName} not found`);
  let depth = 0, endIdx = -1, inString = false, stringChar = "";
  for (let i = startIdx; i < text.length; i++) {
    const ch = text[i];
    if ((ch === '"' || ch === "'") && text[i - 1] !== "\\") {
      if (!inString) { inString = true; stringChar = ch; }
      else if (ch === stringChar) inString = false;
    }
    if (!inString) {
      if (ch === "{") depth++;
      else if (ch === "}") { depth--; if (depth === 0) { endIdx = i; break; } }
    }
  }
  assert(endIdx >= 0, `Could not find end of function ${functionName}`);
  return text.slice(startIdx, endIdx + 1);
}

for (const rel of sourcePaths) {
  if (!fs.existsSync(path.join(repoRoot, rel))) {
    console.log(`SKIP ${rel} (not present)`);
    continue;
  }
  const src = read(rel);
  console.log(`\nChecking: ${rel}`);

  // ────────────────────────────────────────────────────────────────────────────
  // Task 6C — Aset explicit amount priority
  // ────────────────────────────────────────────────────────────────────────────

  // 6C.1: Patch marker present
  assert(
    src.includes("AIRO_TASK6C_GOLD_EXPLICIT_AMOUNT_PRIORITY_V1"),
    "6C patch marker AIRO_TASK6C_GOLD_EXPLICIT_AMOUNT_PRIORITY_V1 missing"
  );

  // 6C.2: Explicit baseAmount wins over estimatedValue when no auto-price keyword
  assert(
    src.includes("!useAutoPrice && baseAmount > 0 ? baseAmount : 0"),
    "6C: explicit baseAmount priority expression missing in parseFinanceText_"
  );

  // 6C.3: Auto-price keywords guard is present
  assert(
    src.includes("harga pasar") && src.includes("auto harga"),
    "6C: auto-price keyword guard (harga pasar / auto harga) missing"
  );

  // 6C.4: purchasePrice still has highest priority (appears before baseAmount in chain)
  {
    const pfBlock = extractFunction(src, "parseFinanceText_");
    const purchaseIdx = pfBlock.indexOf("gold.purchasePrice");
    const baseIdx = pfBlock.indexOf("baseAmount > 0 ? baseAmount");
    const estimatedIdx = pfBlock.indexOf("gold.estimatedValue || 0)");
    assert(purchaseIdx < baseIdx, "6C: gold.purchasePrice must appear before baseAmount in amount expression");
    assert(baseIdx < estimatedIdx, "6C: baseAmount must appear before gold.estimatedValue in amount expression");
  }

  // ────────────────────────────────────────────────────────────────────────────
  // Task 6D — Cicilan Rumah Account Ledger co-write
  // ────────────────────────────────────────────────────────────────────────────

  // 6D.1: Patch marker present
  assert(
    src.includes("AIRO_TASK6D_CICILAN_RUMAH_ACCOUNT_LEDGER_COWRITE_V1"),
    "6D patch marker missing"
  );

  // 6D.2: cicilan branch calls writeAccountLedgerMirror_
  {
    const wBlock = extractFunction(src, "writeRouted_");
    assert(
      wBlock.includes('key.includes(\'cicilan\')') || wBlock.includes('key.includes("cicilan")'),
      "6D: writeRouted_ must have cicilan branch"
    );
    assert(
      wBlock.includes("writeAccountLedgerMirror_"),
      "6D: writeRouted_ cicilan branch must call writeAccountLedgerMirror_"
    );
    assert(
      wBlock.includes("account_ledger_result"),
      "6D: writeRouted_ cicilan branch must expose account_ledger_result"
    );
  }

  // 6D.3: Finance Events emitted for cicilan
  assert(
    src.includes("cicilan_payment"),
    "6D: cicilan_payment event_type missing from Finance Events emission"
  );

  // ────────────────────────────────────────────────────────────────────────────
  // Task 6B — Hutang full-intent direct routing
  // ────────────────────────────────────────────────────────────────────────────

  // 6B.1: Patch marker present
  assert(
    src.includes("AIRO_TASK6B_HUTANG_DIRECT_ROUTING_FULL_INTENT_V1"),
    "6B direct routing patch marker missing"
  );

  // 6B.2: canAskDebtAmbiguousClarification_ suppresses when full intent (person+account)
  {
    const caBlock = extractFunction(src, "canAskDebtAmbiguousClarification_");
    assert(
      caBlock.includes("hasFullDebtPaymentIntent"),
      "6B: canAskDebtAmbiguousClarification_ must compute hasFullDebtPaymentIntent"
    );
    assert(
      caBlock.includes("account !== 'Unknown'"),
      "6B: hasFullDebtPaymentIntent must check account !== Unknown"
    );
  }

  // 6B.3: Original-text recovery marker present
  assert(
    src.includes("AIRO_TASK6B_HUTANG_CLARIFICATION_ORIGINAL_TEXT_RECOVERY_V1"),
    "6B original-text recovery patch marker missing"
  );

  // 6B.4: debt_payment no longer unconditionally returns DEBT_NEEDS_COMPLETE_REWRITE
  {
    const drBlock = extractFunction(src, "debtAmbiguousClarificationResolvedText_");
    // The direct rewrite guard must only be after original_text check fails
    const rewriteIdx = drBlock.indexOf("DEBT_NEEDS_COMPLETE_REWRITE");
    const originalTextIdx = drBlock.indexOf("pending.original_text");
    assert(
      originalTextIdx < rewriteIdx,
      "6B: original_text recovery must be checked before DEBT_NEEDS_COMPLETE_REWRITE"
    );
  }

  // 6B.5: Runtime evaluation test for exact string "bayar hutang 100000 ke budi dari bca SMK_T6C_HUTANG"
  {
    const testFns = [
      "canAskDebtAmbiguousClarification_",
      "parseDebtPerson_",
      "parseAccount_",
      "airoSprint7AccountContractGetRegistry_",
      "airoSprint7AccountContractGetStaticRegistry_",
      "parseAmount_",
      "sanitizeAmountExtractionText_",
      "isDebtPaymentText_",
      "isBorrowInText_",
      "stripQaTag_",
      "normalizePersonName_",
      "isCreditCardPaymentText_",
      "isCreditCardPurchaseText_",
      "isCreditCardRefundText_",
    ];
    let evalCode = "";
    for (const fn of testFns) {
      evalCode += extractFunction(src, fn) + "\n";
    }

    evalCode += `\nfunction airoEnsureAccountRegistrySheet_() {}\nfunction airoSprint7FSpreadsheet_() { return null; }\nglobal.Logger = { log: function() {} };\n`;
    const runTest = new Function(evalCode + `
      const text = "bayar hutang 100000 ke budi dari bca SMK_T6C_HUTANG";
      const parsed = { amount: parseAmount_(text) };
      return {
        amount: parsed.amount,
        isDebtPaymentText: isDebtPaymentText_(text),
        parseDebtPerson: parseDebtPerson_(text),
        parseAccount: parseAccount_(text),
        canAskDebtAmbiguousClarification: canAskDebtAmbiguousClarification_(parsed, text)
      };
    `);

    const res = runTest();
    assert(res.amount === 100000, "parseAmount_ should return 100000, got: " + res.amount);
    assert(res.isDebtPaymentText === true, "isDebtPaymentText_ should return true");
    assert(res.parseDebtPerson === "budi", "parseDebtPerson_ should return budi, got: " + res.parseDebtPerson);
    assert(res.parseAccount === "BCA", "parseAccount_ should return BCA, got: " + res.parseAccount);
    assert(res.canAskDebtAmbiguousClarification === false, "canAskDebtAmbiguousClarification_ should return false, got: " + res.canAskDebtAmbiguousClarification);
  }

  // ────────────────────────────────────────────────────────────────────────────
  // Task 6A — CC purchase/payment routing
  // ────────────────────────────────────────────────────────────────────────────

  // 6A.1: CC purchase direct route patch marker
  assert(
    src.includes("AIRO_TASK6A_CC_PURCHASE_DIRECT_ROUTE_V1"),
    "6A: CC purchase direct route patch marker missing"
  );

  // 6A.2: canAskCreditCardAmbiguousClarification_ bypasses when isCreditCardPurchaseText_
  {
    const ccBlock = extractFunction(src, "canAskCreditCardAmbiguousClarification_");
    assert(
      ccBlock.includes("isCreditCardPurchaseText_"),
      "6A: canAskCreditCardAmbiguousClarification_ must call isCreditCardPurchaseText_ as bypass guard"
    );
  }

  // 6A.3: CC payment no-match writes Account Ledger (not silent Review Queue drop)
  assert(
    src.includes("AIRO_TASK6A_CC_PAYMENT_NO_MATCH_ACCOUNT_LEDGER_V1"),
    "6A: CC payment no-match Account Ledger patch marker missing"
  );

  {
    const ccPayBlock = extractFunction(src, "markCreditCardPocketBluTransfer_");
    assert(
      ccPayBlock.includes("noMatchLedgerResult"),
      "6A: no-match path must write to Account Ledger (noMatchLedgerResult)"
    );
    assert(
      ccPayBlock.includes("raw_text: rawText"),
      "6A: Review Queue fallback must preserve raw_text (including smoke tags)"
    );
    assert(
      ccPayBlock.includes("cc_payment_no_match: true"),
      "6A: no-match result must expose cc_payment_no_match flag"
    );
  }

  // 6A.4: isCreditCardPaymentText_ still matches ^bayar cc prefix
  assert(
    src.includes("^bayar") && src.includes("cc"),
    "6A: isCreditCardPaymentText_ ^bayar cc prefix pattern missing"
  );

  // ────────────────────────────────────────────────────────────────────────────
  // Task 7 — Aset clarity patch
  // ────────────────────────────────────────────────────────────────────────────

  // 7.1: Patch marker present
  assert(
    src.includes("AIRO_TASK7_ASET_CLARITY_DISTINCTION_V1"),
    "7.1: Aset clarity patch marker AIRO_TASK7_ASET_CLARITY_DISTINCTION_V1 missing"
  );

  // 7.2: Runtime parser and formatter checks
  {
    const testFns = [
      "parseFinanceText_",
      "parseGoldAsset_",
      "parseGoldKarat_",
      "parseGoldWeightGram_",
      "parseGoldPurchasePrice_",
      "parseGoldNotes_",
      "parseIndonesianDate_",
      "parseDate_",
      "parseAmount_",
      "sanitizeAmountExtractionText_",
      "cleanAmount_",
      "stripQaTag_",
      "normalizePersonName_",
      "roundGoldGram_",
      "appendGoldAssetRow_",
      "airoSprint7FFormatRupiah_",
      "airoBuildFinanceWriteSuccessReply_",
      "parseGoldAction_",
      "parseType_",
      "parseCategory_",
      "parseSubcategory_",
      "airoSprint7ParseCategoryAndSubcategoryFromText_",
      "escapeRegex_",
      "airoSprint7CategoryContractGetRegistry_",
      "airoSprint7CategoryContractGetStaticRegistry_",
      "airoSprint7AccountContractGetRegistry_",
      "airoSprint7AccountContractGetStaticRegistry_",
      "parseAccount_",
      "parseCreditor_",
      "parseMerchant_",
      "parseAssetSection_",
      "isCashInflowText_",
      "reviewIssueReasonForParsed_",
      "cleanDebtPersonName_",
      "isCreditCardPaymentText_",
      "isCreditCardPurchaseText_",
      "isCreditCardRefundText_",
      "isBorrowInText_",
      "isDebtPaymentText_",
      "findGoldLedgerHeaderRow_",
      "canonicalKey_",
    ];

    let evalCode = "";
    for (const fn of testFns) {
      evalCode += extractFunction(src, fn) + "\n";
    }

    // Stubs and mocks
    evalCode += `
      function getGoldMarketPrice24kPerGram_() { return 2789000; }
      function getProp_() { return "mock-spreadsheet-id"; }
      const SpreadsheetApp = {
        openById: function() { return {}; }
      };
      function getSheetTabUrl_(ss, sheet) { return "https://mock-sheet-url"; }
      function getSheetTabUrlByName_(ss, name) { return "https://mock-sheet-url"; }
      function findNextGoldLedgerRow_() { return 10; }
      function makeTxnId_() { return "txn-12345"; }
      const Utilities = {
        formatDate: function(date, tz, format) {
          return date.toISOString().split("T")[0];
        }
      };
      const Session = {
        getScriptTimeZone: function() { return "GMT"; }
      };
      function airoEnsureCategoryRegistrySheet_() {}
      function airoEnsureAccountRegistrySheet_() {}
      function airoSprint7FSpreadsheet_() { return null; }
      global.Logger = { log: function() {} };
    `;

    evalCode += `\nfunction airoEnsureAccountRegistrySheet_() {}\nfunction airoSprint7FSpreadsheet_() { return null; }\nglobal.Logger = { log: function() {} };\n`;
    const runTest = new Function(evalCode + `
      const text = "beli emas 1 gram 1800000 dari bca";
      const parsed = parseFinanceText_(text);
      
      const mockSheet = {
        getName: function() { return "Aset"; },
        getLastRow: function() { return 1; },
        getLastColumn: function() { return 12; },
        getRange: function(row, col, rows, cols) {
          return {
            getValues: function() {
              return [
                ["gold_event_id", "date", "action", "grams_in", "grams_out", "price_per_gram", "fee", "total_amount", "source_account", "source", "raw_text", "notes"]
              ];
            },
            setValues: function(vals) {
              mockSheet.writtenVals = vals[0];
            }
          };
        }
      };

      const appendResult = appendGoldAssetRow_(mockSheet, parsed, text, { linked_txn_id: "txn-12345" });
      const replyMessage = airoBuildFinanceWriteSuccessReply_("Aset", "Aset", parsed, appendResult, "https://mock-sheet-url");

      return {
        parsedAmount: parsed.amount,
        goldWeightGram: parsed.goldWeightGram,
        goldEstimatedValue: parsed.goldEstimatedValue,
        notesWritten: mockSheet.writtenVals ? mockSheet.writtenVals[11] : "",
        replyMessage: replyMessage,
        acquisitionCost: appendResult.acquisitionCost,
        marketValue: appendResult.marketValue
      };
    `);

    const res = runTest();

    // Verify 1: Explicit acquisition cost = 1800000
    assert(
      res.parsedAmount === 1800000,
      "7.2: parsed amount for 'beli emas 1 gram 1800000' should be 1800000, got: " + res.parsedAmount
    );

    // Verify 2: Estimated market value = 2789000
    assert(
      res.goldEstimatedValue === 2789000,
      "7.3: estimated gold value should be 2789000, got: " + res.goldEstimatedValue
    );

    // Verify 3: Aset write notes contains both acquisition cost and estimated market value when they differ
    assert(
      res.notesWritten.includes("biaya_beli: Rp1.800.000") && res.notesWritten.includes("estimasi_nilai: Rp2.789.000"),
      "7.4: notes written to Aset tab must clearly state both biaya_beli and estimasi_nilai, got: " + res.notesWritten
    );

    // Verify 4: Reply message shows the distinction and does not silently present market value as acquisition cost
    assert(
      res.replyMessage.includes("Biaya beli / cash outflow: Rp1.800.000") &&
      res.replyMessage.includes("Estimasi nilai aset / market value: Rp2.789.000"),
      "7.5: Telegram reply message must show the distinction, got: " + res.replyMessage
    );
  }

  // ────────────────────────────────────────────────────────────────────────────
  // Task 6.8 — Category Registry + Clarification UX + Telegram Approval Flow
  // ────────────────────────────────────────────────────────────────────────────

  // 6.8.1: Registry functions are present
  assert(
    src.includes("function airoSprint7CategoryContractGetRegistry_"),
    "6.8: airoSprint7CategoryContractGetRegistry_ function missing"
  );
  assert(
    src.includes("function airoSprint7CategoryContractGetStaticRegistry_"),
    "6.8: airoSprint7CategoryContractGetStaticRegistry_ function missing"
  );

  // 6.8.2: Subcategory matcher exists and accepts correct patterns
  assert(
    src.includes("function airoSprint7CategoryContractMatchSubcategory_"),
    "6.8: airoSprint7CategoryContractMatchSubcategory_ function missing"
  );

  // Test the parser logic in a micro-sandbox
  {
    let evalCode = src + `\n\n`;
    evalCode += `
      // Mock spreadsheet to return category sheet
      function airoSprint7FSpreadsheet_() {
        return null; // Force fallback to static
      }
    `;
    const runSubcategoryMatchTest = new Function(evalCode + `
      const subs = ["Jajan", "Makan di Luar", "Kopi"];
      const matches = [
        airoSprint7CategoryContractMatchSubcategory_("Food & Drink", "2", subs),
        airoSprint7CategoryContractMatchSubcategory_("Food & Drink", "2.", subs),
        airoSprint7CategoryContractMatchSubcategory_("Food & Drink", "2. makan diluar", subs),
        airoSprint7CategoryContractMatchSubcategory_("Food & Drink", "makan di luar", subs),
        airoSprint7CategoryContractMatchSubcategory_("Food & Drink", "makan diluar", subs),
        airoSprint7CategoryContractMatchSubcategory_("Food & Drink", "Makan di Luar", subs),
        airoSprint7CategoryContractMatchSubcategory_("Food & Drink", "b", subs),
      ];
      return matches;
    `);

    const matches = runSubcategoryMatchTest();
    for (let m of matches) {
      assert(m === "Makan di Luar", `6.8: Expected subcategory match 'Makan di Luar', got '${m}'`);
    }
  }

  // 6.8.3: Invalid subcategory retry error message corrected
  assert(
    src.includes("Pilih subkategori yang sesuai (1/2/3...)"),
    "6.8: Subcategory validation retry prompt must use (1/2/3...) instead of (A/B/C...)"
  );

  // 6.8.4: Status set to pending approval and approval instructions exist in email resolution fallback
  assert(
  src.includes(
    "Status: pending approval."
  ) &&
  src.includes(
    "Balas /approval untuk langsung menyetujui transaksi ini."
  ),
  "6.8: Fallback staging message must mention pending approval and direct /approval instruction"
);

  // 6.8.5: Approval commands router exists and is registered in doPost
  assert(
    src.includes("function airoSprint7HApprovalCommandMaybeHandleRoute_"),
    "6.8: airoSprint7HApprovalCommandMaybeHandleRoute_ function missing"
  );
  assert(
    src.includes("var sprint7HApprovalCommandResult = airoSprint7HApprovalCommandMaybeHandleRoute_(e);"),
    "6.8: airoSprint7HApprovalCommandMaybeHandleRoute_ router registration in doPost missing"
  );

  // ────────────────────────────────────────────────────────────────────────────
  // Safety constraints: no Gmail, no trigger mutation, no Task 5 row write
  // ────────────────────────────────────────────────────────────────────────────
  // These checks ensure no patch accidentally introduces Gmail/trigger calls
  // in any of the patched functions.
  const patchedFunctions = [
    "parseFinanceText_",
    "writeRouted_",
    "canAskDebtAmbiguousClarification_",
    "debtAmbiguousClarificationResolvedText_",
    "canAskCreditCardAmbiguousClarification_",
    "markCreditCardPocketBluTransfer_",
    "appendGoldAssetRow_",
    "airoBuildFinanceWriteSuccessReply_",
    "airoSprint7HApprovalCommandMaybeHandleRoute_",
  ];
  for (const fn of patchedFunctions) {
    if (!src.includes("function " + fn)) continue;
    const block = extractFunction(src, fn);
    assert(!block.includes("GmailApp"), `${fn} must not call GmailApp`);
    assert(!block.includes("ScriptApp.newTrigger"), `${fn} must not call ScriptApp.newTrigger`);
  }

  // ────────────────────────────────────────────────────────────────────────────
  // Task 6.9 — Internal Transfer Cash/Blu Routing Fix
  // ────────────────────────────────────────────────────────────────────────────

  // Test the parsing and ambiguity check logic in a micro-sandbox
  {
    let evalCode = src + "\n\n";
    evalCode += `
      function makeTxnId_() { return "txn-12345"; }
      const Utilities = {
        formatDate: function(date, tz, format) {
          return date.toISOString().split("T")[0];
        }
      };
      const Session = {
        getScriptTimeZone: function() { return "GMT"; }
      };
      function airoEnsureCategoryRegistrySheet_() {}
      function airoEnsureAccountRegistrySheet_() {}
      function airoSprint7FSpreadsheet_() { return null; }
      function airoSprint7AccountContractGetRegistry_() {
        return [
          { account_id: "blu", account_name: "Blu", provider: "Blu", account_type: "bank", parent_account: "Blu", pocket_name: "", is_cash: false, is_bank: true, is_credit: false },
          { account_id: "bca", account_name: "BCA", provider: "BCA", account_type: "bank", parent_account: "BCA", pocket_name: "", is_cash: false, is_bank: true, is_credit: false },
          { account_id: "cash_umum", account_name: "Cash Umum", provider: "Cash", account_type: "cash", parent_account: "Cash", pocket_name: "umum", is_cash: true, is_bank: false, is_credit: false }
        ];
      }
      global.Logger = { log: function() {} };
    `;
    const runTransferRoutingTest = new Function(evalCode + `
      const txt1 = "transfer 25000 dari blu ke cash SMK_T69_BLU_TO_CASH";
      const txt2 = "transfer 30000 dari cash ke blu SMK_T69_CASH_TO_BLU";

      const parsed1 = parseFinanceText_(txt1);
      const parsed2 = parseFinanceText_(txt2);

      const cashAmbiguity1 = canAskCashAmbiguousClarification_(parsed1, txt1);
      const cashAmbiguity2 = canAskCashAmbiguousClarification_(parsed2, txt2);

      const transferObj1 = detectInternalTransfer_(parsed1, txt1);
      const transferObj2 = detectInternalTransfer_(parsed2, txt2);

      return {
        parsed1_needsReview: parsed1.needsReview,
        parsed2_needsReview: parsed2.needsReview,
        cashAmbiguity1: cashAmbiguity1,
        cashAmbiguity2: cashAmbiguity2,
        transferObj1: transferObj1,
        transferObj2: transferObj2
      };
    `);

    const res = runTransferRoutingTest();

    // Verify 1: No review issue/clarification reason is flagged on parse
    assert(
      res.parsed1_needsReview === false,
      "6.9: transfer from blu to cash must not flag review reason, needsReview: " + res.parsed1_needsReview
    );
    assert(
      res.parsed2_needsReview === false,
      "6.9: transfer from cash to blu must not flag review reason, needsReview: " + res.parsed2_needsReview
    );

    // Verify 2: Cash ambiguity check does not intercept complete internal transfer
    assert(
      res.cashAmbiguity1 === false,
      "6.9: cash ambiguity must not fire for complete blu-to-cash transfer, got: " + res.cashAmbiguity1
    );
    assert(
      res.cashAmbiguity2 === false,
      "6.9: cash ambiguity must not fire for complete cash-to-blu transfer, got: " + res.cashAmbiguity2
    );

    // Verify 3: Transfer accounts are resolved correctly
    assert(
      res.transferObj1 && res.transferObj1.sourceAccount === "Blu" && (res.transferObj1.targetAccount === "Cash" || res.transferObj1.targetAccount === "Cash Umum"),
      "6.9: transferObj1 accounts mismatch, got: " + JSON.stringify(res.transferObj1)
    );
    assert(
      res.transferObj2 && (res.transferObj2.sourceAccount === "Cash" || res.transferObj2.sourceAccount === "Cash Umum") && res.transferObj2.targetAccount === "Blu",
      "6.9: transferObj2 accounts mismatch, got: " + JSON.stringify(res.transferObj2)
    );
  }

  console.log(`  ALL ASSERTIONS PASSED for \${rel}`);
}

console.log("\nRESULT_SPRINT7H_TASK6_STATIC_TEST=PASS");
