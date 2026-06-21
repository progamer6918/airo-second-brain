#!/usr/bin/env node
const fs = require('fs');

const src = fs.readFileSync('scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs', 'utf8');

function pass(name, ok) {
  if (!ok) {
    console.error(`FAIL: ${name}`);
    process.exitCode = 1;
  } else {
    console.log(`PASS: ${name}`);
  }
}

// Simple extractor for self-contained functions
function extractFunction(name) {
  const start = src.indexOf(`function ${name}`);
  if (start === -1) throw new Error(`Function ${name} not found`);

  let depth = 0;
  let end = -1;
  let inString = false;
  let stringChar = '';

  for (let i = start; i < src.length; i++) {
    const char = src[i];

    if ((char === '"' || char === "'") && src[i - 1] !== '\\') {
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
          end = i;
          break;
        }
      }
    }
  }

  if (end === -1) throw new Error(`Could not find end of function ${name}`);
  return src.slice(start, end + 1);
}

try {
  // Extract and eval functions
  const getRegistryCode = extractFunction('airoSprint7CategoryContractGetRegistry_');
  const resolveCode = extractFunction('airoSprint7CategoryContractResolve_');
  const maybeRouteCode = extractFunction('airoSprint7CategoryContractKategoriCommandMaybeHandleRoute_');
  const buildReplyCode = extractFunction('airoSprint7CategoryContractKategoriCommandBuildReply_');
  const handleReplyCode = extractFunction('airoSprint7CategoryContractMissingCategoryHandleReply_');
  const buildSubPromptCode = extractFunction('airoSprint7CategoryContractBuildSubcategoryPrompt_');
  const resolveFlowCode = extractFunction('airoSprint7CategoryContractResolveMissingCategoryFlow_');

  eval(getRegistryCode);
  eval(resolveCode);
  eval(maybeRouteCode);
  eval(buildReplyCode);
  eval(handleReplyCode);
  eval(buildSubPromptCode);
  eval(resolveFlowCode);

  pass('Functions successfully extracted and evaluated', true);

  function assertMapping(inputCat, inputSub, expectedCat, expectedSub, expectedClass, expectedDomain, expectedValid) {
    const res = airoSprint7CategoryContractResolve_(inputCat, inputSub);

    const ok = res.category === expectedCat &&
               res.subcategory === expectedSub &&
               res.cashflow_class === expectedClass &&
               res.domain === expectedDomain &&
               res.valid === expectedValid;

    if (!ok) {
      console.error(`Mismatch for [${inputCat} / ${inputSub}]: Expected {${expectedCat}, ${expectedSub}, ${expectedClass}, ${expectedDomain}, ${expectedValid}}, got ${JSON.stringify(res)}`);
    }
    pass(`Resolve [${inputCat} / ${inputSub}] -> [${expectedCat} / ${expectedSub}] (${expectedClass} / ${expectedDomain})`, ok);
  }

  // Mappings validation
  assertMapping('Food & Drink', 'Kopi', 'Food & Drink', 'Kopi', 'expense', 'Wallet', true);
  assertMapping('Groceries', 'Belanja Harian', 'Groceries', 'Belanja Harian', 'expense', 'Wallet', true);
  assertMapping('Savings', 'Dana Darurat', 'Savings', 'Dana Darurat', 'saving_allocation', 'Aset', true);
  assertMapping('Investment', 'Emas', 'Investment', 'Emas', 'investment', 'Aset', true);
  assertMapping('Unknown', 'Any', 'Other / Review', 'Lainnya', 'manual_review', 'Review', false);

  // 1. route function exists
  pass('route function exists', src.includes('function airoSprint7CategoryContractKategoriCommandMaybeHandleRoute_'));
  pass('reply builder function exists', src.includes('function airoSprint7CategoryContractKategoriCommandBuildReply_'));

  // 2. doPost integrates route
  const doPostIndex = src.indexOf('function doPost(e)');
  const callIndex = src.indexOf('airoSprint7CategoryContractKategoriCommandMaybeHandleRoute_(e)', doPostIndex);
  pass('doPost integrates route', callIndex !== -1 && callIndex < src.indexOf('airoSprint7FEmailAnswerMaybeHandleRoute_(e)', doPostIndex));

  // 3. /kategori list reply contains Housing and Food & Drink
  const listReply = airoSprint7CategoryContractKategoriCommandBuildReply_('');
  pass('/kategori list contains Housing', listReply.includes('Housing'));
  pass('/kategori list contains Food & Drink', listReply.includes('Food & Drink'));

  // 4. /kategori Groceries returns Belanja Harian and Belanja Bulanan with expense / Wallet
  const groceriesReply = airoSprint7CategoryContractKategoriCommandBuildReply_('Groceries');
  pass('/kategori Groceries contains Belanja Harian', groceriesReply.includes('Belanja Harian'));
  pass('/kategori Groceries contains Belanja Bulanan', groceriesReply.includes('Belanja Bulanan'));
  pass('/kategori Groceries contains class expense', groceriesReply.includes('Class: expense'));
  pass('/kategori Groceries contains domain Wallet', groceriesReply.includes('Domain: Wallet'));

  // 5. /kategori Dana Darurat returns Savings, saving_allocation, Aset
  const savingsReply = airoSprint7CategoryContractKategoriCommandBuildReply_('Dana Darurat');
  pass('/kategori Dana Darurat contains Savings', savingsReply.includes('Savings'));
  pass('/kategori Dana Darurat contains saving_allocation', savingsReply.includes('saving_allocation'));
  pass('/kategori Dana Darurat contains Aset', savingsReply.includes('Aset'));

  // 6. invalid query returns not found
  const invalidReply = airoSprint7CategoryContractKategoriCommandBuildReply_('InvalidNameHere');
  pass('/kategori invalid query returns not found message', invalidReply.includes('tidak ditemukan'));

  // 7. route match is strict for /kategori only
  let mockTelegramText = '';
  let payloadCalled = false;
  let textCalled = false;

  global.airoSprint7FParseTelegramPayload_ = function(e) {
    payloadCalled = true;
    return {
      chat_id: 12345,
      text_raw: mockTelegramText,
      text: mockTelegramText.toLowerCase()
    };
  };

  global.airoSprint7FParseTelegramText_ = function(e) {
    textCalled = true;
    return {
      chat_id: 12345,
      text: mockTelegramText.toLowerCase()
    };
  };

  global.sendTelegram_ = function(chatId, text) {};
  global.json_ = function(obj) { return obj; };

  mockTelegramText = '/kategori';
  pass('/kategori command is matched', airoSprint7CategoryContractKategoriCommandMaybeHandleRoute_({}) !== null);

  // Assert parser usage
  pass('Parser airoSprint7FParseTelegramPayload_ was called', payloadCalled === true);
  pass('Parser airoSprint7FParseTelegramText_ was NOT called', textCalled === false);

  mockTelegramText = '/kategori groceries';
  pass('/kategori <query> command is matched', airoSprint7CategoryContractKategoriCommandMaybeHandleRoute_({}) !== null);

  mockTelegramText = '/kategori@bot';
  pass('/kategori@bot command is matched', airoSprint7CategoryContractKategoriCommandMaybeHandleRoute_({}) !== null);

  mockTelegramText = '/kategori_invalid';
  pass('/kategori_invalid command is NOT matched', airoSprint7CategoryContractKategoriCommandMaybeHandleRoute_({}) === null);

  mockTelegramText = 'kategori';
  pass('Plain kategori text is NOT matched', airoSprint7CategoryContractKategoriCommandMaybeHandleRoute_({}) === null);

  mockTelegramText = 'ganti /kategori';
  pass('/kategori in mid-text is NOT matched', airoSprint7CategoryContractKategoriCommandMaybeHandleRoute_({}) === null);

  // 8. Asserting that the route uses airoSprint7FParseTelegramPayload_, not airoSprint7FParseTelegramText_ (source check)
  const routeFuncStr = maybeRouteCode;
  pass('Source code contains airoSprint7FParseTelegramPayload_ inside route', routeFuncStr.includes('airoSprint7FParseTelegramPayload_'));
  pass('Source code does NOT contain airoSprint7FParseTelegramText_ inside route', !routeFuncStr.includes('airoSprint7FParseTelegramText_'));

  // 9. Category Contract v1C workflow tests
  let savedPending = null;
  let sentTelegramMsg = "";
  let clearedPending = false;

  global.savePendingClarification_ = function(chatId, pending) {
    savedPending = pending;
  };
  global.sendTelegram_ = function(chatId, msg) {
    sentTelegramMsg = msg;
  };
  global.clearPendingClarification_ = function(chatId) {
    clearedPending = true;
  };

  // Test A -> Food & Drink Step 2
  savedPending = null;
  sentTelegramMsg = "";
  let resA = airoSprint7CategoryContractMissingCategoryHandleReply_(12345, { step: 1, original_text: "15000 buat makan" }, "A", function() {});
  pass("Choice A transitions step 1 to step 2", savedPending && savedPending.step === 2 && savedPending.selected_category === "Food & Drink");
  pass("Choice A prompts subcategories", sentTelegramMsg.includes("Jajan") && sentTelegramMsg.includes("Kopi"));

  // Test E -> Step 1.5
  savedPending = null;
  sentTelegramMsg = "";
  let resE = airoSprint7CategoryContractMissingCategoryHandleReply_(12345, { step: 1, original_text: "50000 wifi" }, "E", function() {});
  pass("Choice E transitions step 1 to step 1.5", savedPending && savedPending.step === 1.5);
  pass("Choice E prompts manual advice", sentTelegramMsg.includes("supports") || sentTelegramMsg.includes("mendukung"));

  // Test manual Utilities -> Step 2
  savedPending = null;
  sentTelegramMsg = "";
  let resUtil = airoSprint7CategoryContractMissingCategoryHandleReply_(12345, { step: 1.5, original_text: "50000 wifi" }, "Utilities", function() {});
  pass("Manual Utilities transitions step 1.5 to step 2", savedPending && savedPending.step === 2 && savedPending.selected_category === "Utilities");

  // Test Food & Drink C -> Kopi final metadata and suffix
  savedPending = null;
  sentTelegramMsg = "";
  clearedPending = false;
  let resC = airoSprint7CategoryContractMissingCategoryHandleReply_(12345, { step: 2, selected_category: "Food & Drink", original_text: "15001 bca" }, "C", function() {});
  pass("Choice C resolves the flow", resC && resC.resolved === true);
  pass("Choice C resolves with makan suffix", resC.resolved_text === "15001 bca makan");
  pass("Choice C clears pending clarification", clearedPending === true);
  pass("Choice C sends confirmation details", sentTelegramMsg.includes("Class: expense") && sentTelegramMsg.includes("Domain: Wallet"));

  // Test invalid Savings/Investment blocked in v1C flow
  let failCalled = false;
  let mockFailOrRetry = function(msg) {
    failCalled = true;
    return { failed: true };
  };
  let resSavings = airoSprint7CategoryContractMissingCategoryHandleReply_(12345, { step: 1.5, original_text: "100000 savings" }, "Savings", mockFailOrRetry);
  pass("Savings is rejected in missing-category manual flow", failCalled === true);

  failCalled = false;
  let resInvest = airoSprint7CategoryContractMissingCategoryHandleReply_(12345, { step: 1.5, original_text: "100000 investment" }, "Investment", mockFailOrRetry);
  pass("Investment is rejected in missing-category manual flow", failCalled === true);

  // 10. Verify no schema changes (no subcategory, cashflow_class, domain headers in sheet append)
  const forbiddenHeaders = ["subcategory", "cashflow_class", "domain"];
  let schemaViolated = false;
  for (let header of forbiddenHeaders) {
    if (src.includes(`"${header}"`) || src.includes(`'${header}'`)) {
      try {
        const writeAL = extractFunction('writeAccountLedgerMirror_');
        if (writeAL.includes(`"${header}"`) || writeAL.includes(`'${header}'`)) {
          schemaViolated = true;
        }
      } catch (e) {}
      try {
        const appendH = extractFunction('appendByHeader_');
        if (appendH.includes(`"${header}"`) || appendH.includes(`'${header}'`)) {
          schemaViolated = true;
        }
      } catch (e) {}
    }
  }
  pass("No schema header changes introduced to writing functions", schemaViolated === false);

  // 11. Asserting no new Review Queue write paths are introduced by v1C
  const reviewWrites = (src.match(/tabs\.review/g) || []).length;
  pass("No new Review Queue write path is introduced by v1C", reviewWrites <= 35);

} catch (err) {
  console.error(err);
  process.exitCode = 1;
}

if (process.exitCode) process.exit(process.exitCode);
console.log('RESULT_CATEGORY_CONTRACT_STATIC=PASS');
