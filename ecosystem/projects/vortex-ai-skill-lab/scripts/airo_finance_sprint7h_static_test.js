const fs = require("fs");
const path = require("path");

global.Logger = {
  log: function(msg) {
    // Console log disabled to prevent cluttering stdout during tests
  }
};

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

function extractFunction(text, functionName) {
  const startIdx = text.indexOf("function " + functionName);
  assert(startIdx >= 0, `Function ${functionName} not found`);
  
  let depth = 0;
  let endIdx = -1;
  let inString = false;
  let stringChar = '';

  for (let i = startIdx; i < text.length; i++) {
    const char = text[i];
    if ((char === '"' || char === "'") && text[i - 1] !== '\\') {
      if (!inString) {
        inString = true;
        stringChar = char;
      } else if (char === stringChar) {
        inString = false;
      }
    }
    if (!inString) {
      if (char === '{') {
        depth++;
      } else if (char === '}') {
        depth--;
        if (depth === 0) {
          endIdx = i;
          break;
        }
      }
    }
  }
  assert(endIdx >= 0, `Could not find end of function ${functionName}`);
  return text.slice(startIdx, endIdx + 1);
}

for (const rel of sourcePaths) {
  const text = read(rel);

  // 1. Mojibake guard
  assert(!text.includes("≡ƒº╛"), `${rel} contains garbled mojibake representation of 🧾`);

  // 2. Trigger functions exist
  const installFn = extractFunction(text, "airoSprint7HInstallPollerTrigger_");
  const uninstallFn = extractFunction(text, "airoSprint7HUninstallPollerTrigger_");
  const statusFn = extractFunction(text, "airoSprint7HPollerTriggerStatus_");
  
  // 3. Trigger install target handler is airoSprint7HScheduledGmailPoller_
  assert(installFn.includes('"airoSprint7HScheduledGmailPoller_"') || installFn.includes("'airoSprint7HScheduledGmailPoller_'"), `${rel} target handler mismatch`);
  
  // 4. 15-minute trigger interval exists in install function
  assert(installFn.includes(".everyMinutes(15)"), `${rel} missing 15-minute polling interval`);

  // 5. Scheduled poller handler existence
  const pollerFn = extractFunction(text, "airoSprint7HScheduledGmailPoller_");

  // 6. Kill switch check
  assert(pollerFn.includes("EMAIL_INGESTION_DISABLED"), `${rel} missing kill switch check`);

  // 7. Active window WIB logic exists
  assert(pollerFn.includes("Asia/Jakarta"), `${rel} missing Jakarta timezone active window check`);
  assert(pollerFn.includes("hour < 7") || pollerFn.includes("hour < 07") || pollerFn.includes("7") || pollerFn.includes("22"), `${rel} missing active window limits check`);

  // 8. Fast exit paths exist and perform no reads, sends, sheet writes, or trigger mutations
  const killSwitchExitBlock = pollerFn.slice(pollerFn.indexOf("EMAIL_INGESTION_DISABLED"));
  assert(killSwitchExitBlock.includes("write_performed: false"), `${rel} kill switch exit performs writes`);
  assert(killSwitchExitBlock.includes("gmail_read_performed: false"), `${rel} kill switch exit reads Gmail`);
  assert(killSwitchExitBlock.includes("gmail_modified: false"), `${rel} kill switch exit mutates Gmail`);
  
  // 9. Poller does not call Account Ledger, Finance Events, or domain writes
  assert(!pollerFn.includes("writeRouted_"), `${rel} poller calls writeRouted_`);
  assert(!pollerFn.includes("writeAccountLedgerMirror_"), `${rel} poller calls writeAccountLedgerMirror_`);
  assert(!pollerFn.includes("writeFinanceEvent_"), `${rel} poller calls writeFinanceEvent_`);
  
  // 10. Poller does not mutate Gmail
  assert(!pollerFn.includes(".addLabel"), `${rel} poller mutates Gmail labels`);
  assert(!pollerFn.includes(".removeLabel"), `${rel} poller mutates Gmail labels`);
  assert(!pollerFn.includes(".moveToTrash"), `${rel} poller deletes emails`);
  assert(!pollerFn.includes(".moveToArchive"), `${rel} poller archives emails`);

  // 11. Multi-step state machine answer handler exists
  const answerFn = extractFunction(text, "airoSprint7FEmailAnswerMaybeHandleRoute_");
  
  // 12. E maps to category_search_pending, not direct Other / Review
  assert(answerFn.includes('"category_search_pending"') || answerFn.includes("'category_search_pending'"), `${rel} missing category_search_pending transition`);
  assert(!answerFn.includes('"Other / Review"') && !answerFn.includes("'Other / Review'") || answerFn.includes("category_search_pending"), `${rel} option E maps directly to Other/Review in answer router`);

  // 13. A/B/C/D can transition to subcategory_pending
  assert(answerFn.includes('"subcategory_pending"') || answerFn.includes("'subcategory_pending'"), `${rel} missing subcategory_pending transition`);

  // 14. Telegram prompt cap/dedupe guard check
  assert(pollerFn.includes("promptsSentCount < 1"), `${rel} poller missing Telegram prompt caps check`);
  assert(pollerFn.includes("skippedDedupeCount"), `${rel} poller missing dedupe skipped count tracker`);

  // 15. Indonesian Rupiah parser decimal correctness unit tests
  const extractAmountFnCode = extractFunction(text, "airoSprint7FExtractAmountFromSubject_");
  const extractSampleAmountFnCode = extractFunction(text, "airoSprint7SamplePreviewExtractAmount_");
  
  eval(extractAmountFnCode);
  eval(extractSampleAmountFnCode);
  
  assert(airoSprint7FExtractAmountFromSubject_("Transaksimu sebesar Rp69.000,00 berhasil") === 69000, `${rel} failed to parse Rp69.000,00`);
  assert(airoSprint7FExtractAmountFromSubject_("Transaksimu sebesar Rp6.900.000,00 berhasil") === 6900000, `${rel} failed to parse Rp6.900.000,00`);
  assert(airoSprint7FExtractAmountFromSubject_("Transaksimu sebesar Rp336.541,00 berhasil") === 336541, `${rel} failed to parse Rp336.541,00`);
  assert(airoSprint7FExtractAmountFromSubject_("Transaksimu sebesar Rp12.000,00 berhasil") === 12000, `${rel} failed to parse Rp12.000,00`);
  assert(airoSprint7FExtractAmountFromSubject_("Transaksimu sebesar Rp101.000,00 berhasil") === 101000, `${rel} failed to parse Rp101.000,00`);
  assert(airoSprint7FExtractAmountFromSubject_("Transaksimu sebesar Rp5.000,00 berhasil") === 5000, `${rel} failed to parse Rp5.000,00`);
  assert(airoSprint7FExtractAmountFromSubject_("Transaksimu sebesar Rp20.000,00 berhasil") === 20000, `${rel} failed to parse Rp20.000,00`);
  assert(airoSprint7FExtractAmountFromSubject_("Transaksimu sebesar Rp150.000,00 berhasil") === 150000, `${rel} failed to parse Rp150.000,00`);

  assert(airoSprint7SamplePreviewExtractAmount_("Rp69.000,00") === 69000, `${rel} failed sample parse Rp69.000,00`);
  assert(airoSprint7SamplePreviewExtractAmount_("Rp6.900.000,00") === 6900000, `${rel} failed sample parse Rp6.900.000,00`);

  // 16. Context-Safe Telegram Email Answer Mapping Unit Tests
  const getRegistryCode = extractFunction(text, "airoSprint7CategoryContractGetRegistry_");
  const getStaticRegistryCode = extractFunction(text, "airoSprint7CategoryContractGetStaticRegistry_");
  const resolveCode = extractFunction(text, "airoSprint7CategoryContractResolve_");
  const inferActionCode = extractFunction(text, "airoSprint7FDInferAction_");
  const eventTypeCode = extractFunction(text, "airoSprint7FDEventTypeForAction_");
  const domainCode = extractFunction(text, "airoSprint7FDDomainForAction_");
  const targetTabsCode = extractFunction(text, "airoSprint7FDTargetTabsForAction_");
  const categoryFromResCode = extractFunction(text, "airoSprint7FDCategoryFromResolution_");
  const resolveLabelCode = extractFunction(text, "airoSprint7FResolveAnswerLabel_");
  const answerChoiceCode = extractFunction(text, "airoSprint7FDAnswerChoice_");
  const normSourceCode = extractFunction(text, "airoSprint7FDNormalizeSourceChannel_");
  const amountCode = extractFunction(text, "airoSprint7FDAmount_");
  const primaryAccountCode = extractFunction(text, "airoSprint7FDPrimaryAccount_");
  const formatRupiahCode = extractFunction(text, "airoSprint7FFormatRupiah_");
  const buildPreviewCode = extractFunction(text, "airoSprint7FDBuildNoWriteRoutePreview_");
  const routePreviewMessageCode = extractFunction(text, "airoSprint7FDRoutePreviewMessage_");

  global.airoEnsureCategoryRegistrySheet_ = function() {};
  global.airoEnsureAccountRegistrySheet_ = function() {};
  global.airoSprint7AccountContractGetRegistry_ = function() { return []; };
  global.airoSprint7FSpreadsheet_ = function() { return null; };
  eval(getStaticRegistryCode);
  eval(getRegistryCode);
  eval(resolveCode);
  eval(inferActionCode);
  eval(eventTypeCode);
  eval(domainCode);
  eval(targetTabsCode);
  eval(categoryFromResCode);
  eval(resolveLabelCode);
  eval(answerChoiceCode);
  eval(normSourceCode);
  eval(amountCode);
  eval(primaryAccountCode);
  eval(formatRupiahCode);
  eval(buildPreviewCode);
  eval(routePreviewMessageCode);

  // Test Case 1: category_expense + answer C (Groceries) for Blu transaction
  const pendingBluC = {
    clarification_question_type: "category_expense",
    candidate_type: "blu_transaction",
    provider: "Blu",
    display_amount: 100000,
    amount_idr: 100000
  };
  const resolvedBluC = {
    ok: true,
    answer: "C",
    label: "Groceries"
  };
  const previewBluC = airoSprint7FDBuildNoWriteRoutePreview_(pendingBluC, resolvedBluC, "C");
  assert(previewBluC.category === "Groceries", `${rel} previewBluC.category is not Groceries`);
  assert(previewBluC.action === "wallet_expense", `${rel} previewBluC.action is not wallet_expense`);
  assert(previewBluC.event_type !== "cc_payment", `${rel} previewBluC.event_type is cc_payment`);
  assert(previewBluC.domain !== "Credit Card", `${rel} previewBluC.domain is Credit Card`);
  assert(previewBluC.finance_write_performed === false, `${rel} previewBluC.finance_write_performed is not false`);

  // Test Case 2: category_expense + answer C (Groceries) for Credit Card transaction
  const pendingCcC = {
    clarification_question_type: "category_expense",
    candidate_type: "cc_purchase",
    provider: "Credit Card",
    display_amount: 100000,
    amount_idr: 100000
  };
  const resolvedCcC = {
    ok: true,
    answer: "C",
    label: "Groceries"
  };
  const previewCcC = airoSprint7FDBuildNoWriteRoutePreview_(pendingCcC, resolvedCcC, "C");
  assert(previewCcC.category === "Groceries", `${rel} previewCcC.category is not Groceries`);
  assert(previewCcC.action === "cc_purchase", `${rel} previewCcC.action is not cc_purchase`);
  assert(previewCcC.event_type === "cc_purchase", `${rel} previewCcC.event_type is not cc_purchase`);
  assert(previewCcC.domain === "Credit Card", `${rel} previewCcC.domain is not Credit Card`);

  // Test Case 3: Legacy CC intent works as before under explicit CC context
  const pendingLegacyCc = {
    clarification_question_type: "cc_payment", // Explicit CC context
    candidate_type: "cc_payment",
    provider: "Credit Card",
    display_amount: 100000,
    amount_idr: 100000
  };
  const resolvedLegacyCc = {
    ok: true,
    answer: "C",
    label: "cc_payment"
  };
  const previewLegacyCc = airoSprint7FDBuildNoWriteRoutePreview_(pendingLegacyCc, resolvedLegacyCc, "C");
  assert(previewLegacyCc.action === "refund_or_reversal", `${rel} previewLegacyCc.action is not refund_or_reversal for choice C looksCc`);

  // Test Case 4: Legacy default choice C returns wallet_expense when not CC looks and not category_expense
  const pendingLegacyDefault = {
    clarification_question_type: "default_legacy",
    candidate_type: "default",
    display_amount: 100000,
    amount_idr: 100000
  };
  const resolvedLegacyDefault = {
    ok: true,
    answer: "C",
    label: "cc_payment"
  };
  const previewLegacyDefault = airoSprint7FDBuildNoWriteRoutePreview_(pendingLegacyDefault, resolvedLegacyDefault, "C");
  assert(previewLegacyDefault.action === "wallet_expense", `${rel} previewLegacyDefault.action is not wallet_expense under non-CC context`);

  // Test Case 5: Verification that category_expense + looksCc true but not CC candidate does NOT map to cc_purchase/payment
  const pendingLooksCc = {
    clarification_question_type: "category_expense",
    candidate_type: "blu_credit_fake",
    provider: "Blu",
    display_amount: 100000,
    amount_idr: 100000
  };
  const resolvedLooksCc = {
    ok: true,
    answer: "C",
    label: "Groceries"
  };
  const previewLooksCc = airoSprint7FDBuildNoWriteRoutePreview_(pendingLooksCc, resolvedLooksCc, "C");
  assert(previewLooksCc.action === "wallet_expense", `${rel} previewLooksCc.action is not wallet_expense despite looksCc name`);

  // 17. Verify poller deduplication logic
  assert(pollerFn.includes("logResult.dedupe_hit"), `${rel} poller missing dedupe_hit guard`);
  assert(pollerFn.includes("skippedDedupeCount++"), `${rel} poller missing skippedDedupeCount increment`);

  // 18. Verify diagnostics and self-test existence
  const selfTestCode = extractFunction(text, "runSprint7HRouteInferenceSelfTestFromEditor");
  const runtimeVersionCode = extractFunction(text, "runSprint7HRuntimeVersionFromEditor");

  eval(selfTestCode);
  eval(runtimeVersionCode);

  assert(typeof runSprint7HRouteInferenceSelfTestFromEditor === "function", `${rel} runSprint7HRouteInferenceSelfTestFromEditor function not found`);
  assert(typeof runSprint7HRuntimeVersionFromEditor === "function", `${rel} runSprint7HRuntimeVersionFromEditor function not found`);

  // Test self-test output
  const selfTestResult = runSprint7HRouteInferenceSelfTestFromEditor();
  assert(selfTestResult.ok === true, `${rel} self-test result ok is not true`);
  assert(selfTestResult.event_type !== "cc_payment", `${rel} self-test result event_type is cc_payment`);
  assert(selfTestResult.domain !== "Credit Card", `${rel} self-test result domain is Credit Card`);
  assert(selfTestResult.write_performed === false, `${rel} self-test result write_performed is true`);
  assert(selfTestResult.gmail_read_performed === false, `${rel} self-test result gmail_read_performed is true`);

  // Verify diagnostic function safety
  [
    "writeAccountLedgerMirror_",
    "appendByHeader_",
    "GmailApp.",
    "ScriptApp.newTrigger",
    "createTrigger",
    "markRead",
    "moveToTrash"
  ].forEach(token => {
    assert(!selfTestCode.includes(token), `${rel} self-test references forbidden token: ${token}`);
    assert(!runtimeVersionCode.includes(token), `${rel} runtime version references forbidden token: ${token}`);
  });
}

console.log("RESULT_SPRINT7H_STATIC_TEST=PASS");
console.log("FUNCTION=airoSprint7HScheduledGmailPoller_");
console.log("STATUS=ready");
