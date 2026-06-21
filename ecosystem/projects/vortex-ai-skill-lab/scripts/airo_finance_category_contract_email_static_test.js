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
  // Extract functions
  const funcs = [
    'airoSprint7FBuildFriendlyClarificationMessage_',
    'airoSprint7FResolveAnswerLabel_',
    'airoSprint7FDBuildNoWriteRoutePreview_',
    'airoSprint7FDRoutePreviewMessage_',
    'airoSprint7FEmailAnswerMaybeHandleRoute_',
    'airoSprint7CategoryContractGetRegistry_',
    'airoSprint7CategoryContractResolve_',
    'airoSprint7FFormatRupiah_',
    'airoSprint7FDAmount_',
    'airoSprint7FDPrimaryAccount_',
    'airoSprint7FDNormalizeSourceChannel_',
    'airoSprint7FDInferAction_',
    'airoSprint7FDAnswerChoice_',
    'airoSprint7FDEventTypeForAction_',
    'airoSprint7FDDomainForAction_',
    'airoSprint7FDTargetTabsForAction_',
    'airoSprint7FDCategoryFromResolution_',
    'airoSprint7FParseTelegramPayload_',
    'airoSprint7CategoryContractKategoriCommandMaybeHandleRoute_',
    'airoSprint7CategoryContractKategoriCommandBuildReply_'
  ];

  for (let f of funcs) {
    eval(extractFunction(f));
  }
  pass('All email clarification and preview functions successfully extracted and evaluated', true);

  // Set up mock context
  global.Utilities = {
    formatDate: function(date, tz, format) {
      return "2026-05-29T21:00:00Z";
    }
  };
  global.Session = {
    getScriptTimeZone: function() {
      return "GMT+7";
    }
  };

  let mockTelegramText = '';
  let telegramSentText = '';
  let propertiesDeleted = [];
  let loadedPending = null;
  let ingestionLogUpdated = false;

  global.sendTelegram_ = function(chatId, text) {
    telegramSentText = text;
  };
  global.json_ = function(obj) { return obj; };

  global.PropertiesService = {
    getScriptProperties: function() {
      return {
        getProperty: function(key) {
          return loadedPending ? JSON.stringify(loadedPending) : '';
        },
        setProperty: function(key, val) {
          if (loadedPending) {
            loadedPending = JSON.parse(val);
          }
        },
        deleteProperty: function(key) {
          propertiesDeleted.push(key);
        }
      };
    }
  };

  global.airoSprint7CategoryContractBuildSubcategoryPrompt_ = function(cat) {
    return "Mock prompt for subcategories under " + cat;
  };

  global.airoSprint7HResolveToReviewQueueFallback_ = function(parsed, pending, cat, sub) {
    ingestionLogUpdated = true;
    var propertyKey = pending._property_key || ('AIRO_SPRINT7F_PENDING_EMAIL_' + parsed.chat_id);
    propertiesDeleted.push(propertyKey);
    return {
      ok: true,
      sprint: "7H",
      status: "success",
      handled: true,
      resolved: true,
      write_performed: true
    };
  };

  global.airoSprint7FLoadPendingEmailCandidate_ = function(chatId) {
    if (loadedPending) {
      loadedPending._property_key = 'AIRO_SPRINT7F_PENDING_EMAIL_' + chatId;
    }
    return loadedPending;
  };

  global.airoSprint7FUpdatePendingEmailResolution_ = function(pending, resolved) {
    ingestionLogUpdated = true;
    return {
      updated: true,
      row_number: 5,
      resolved_at: "2026-05-29T21:00:00Z"
    };
  };

  // 1. Verify Prompt Text contains v1 Category Contract options
  const mockCandidate = {
    display_amount: 24000,
    inferred_direction: 'pengeluaran',
    provider: 'Blu',
    received_at: '2026-05-29 12:00'
  };
  const promptMessage = airoSprint7FBuildFriendlyClarificationMessage_('cand123', mockCandidate);
  pass('Prompt contains Food & Drink', promptMessage.includes('A. Food & Drink'));
  pass('Prompt contains Groceries', promptMessage.includes('C. Groceries'));
  pass('Prompt contains Cari kategori option', promptMessage.includes('E. Cari kategori / lihat bantuan'));

  // 2. Verify mappings
  const mockPending = {
    clarification_question_type: 'category_expense',
    candidate_type: 'blu_transaction'
  };
  pass('Mapping A -> Food & Drink', airoSprint7FResolveAnswerLabel_('A', mockPending).label === 'Food & Drink');
  pass('Mapping C -> Groceries', airoSprint7FResolveAnswerLabel_('C', mockPending).label === 'Groceries');
  pass('Mapping E -> Cari kategori', airoSprint7FResolveAnswerLabel_('E', mockPending).label === 'Cari kategori / lihat bantuan');

  // 3. Verify Route Preview Enrichment (Choice A)
  const resolvedA = { label: 'Food & Drink', answer: 'A' };
  const previewA = airoSprint7FDBuildNoWriteRoutePreview_(
    { display_amount: 24000, provider: 'Blu', candidate_id: 'cand123' },
    resolvedA,
    'A'
  );
  pass('Route preview category resolved to Food & Drink', previewA.category === 'Food & Drink');
  pass('Route preview default subcategory resolved to Jajan', previewA.subcategory === 'Jajan');
  pass('Route preview domain is Wallet', previewA.domain === 'Wallet');
  pass('Route preview event_type is expense', previewA.event_type === 'expense');

  // 4. Verify Subcategory output is preview only, not final
  const messageA = airoSprint7FDRoutePreviewMessage_(
    { display_amount: 24000, provider: 'Blu' },
    resolvedA,
    previewA
  );
  pass('Message contains Subkategori preview: Jajan', messageA.includes('Subkategori preview: Jajan'));
  pass('Message contains Subkategori final: belum dikonfirmasi', messageA.includes('Subkategori final: belum dikonfirmasi'));

  // 5. Verify Option E routes to manual_review and prints instructions
  const resolvedE = { label: 'Cari kategori / lihat bantuan', answer: 'E' };
  const previewE = airoSprint7FDBuildNoWriteRoutePreview_(
    { display_amount: 24000, provider: 'Blu', candidate_id: 'cand123' },
    resolvedE,
    'E'
  );
  pass('Option E action is manual_review', previewE.action === 'manual_review');
  pass('Option E domain is Review', previewE.domain === 'Review');
  pass('Option E target preview is Review Queue', previewE.target_tabs_preview[0] === 'Review Queue future preview');

  const messageE = airoSprint7FDRoutePreviewMessage_(
    { display_amount: 24000, provider: 'Blu' },
    resolvedE,
    previewE
  );
  pass('Option E message contains /kategori <query> instruction', messageE.includes('/kategori <query>'));
  pass('Option E message has subcategory preview muted', messageE.includes('Subkategori preview: -'));

  // 6. Verify strict safety invariants on generated preview object
  pass('Safety: finance_write_performed is false', previewA.finance_write_performed === false);
  pass('Safety: write_approved is false', previewA.write_approved === false);
  pass('Safety: write_allowed is false', previewA.write_allowed === false);
  pass('Safety: account_ledger_write_performed is false', previewA.account_ledger_write_performed === false);
  pass('Safety: finance_events_write_performed is false', previewA.finance_events_write_performed === false);
  pass('Safety: review_queue_write_performed is false', previewA.review_queue_write_performed === false);

  // 7. Verify two-step classification state machine
  loadedPending = {
    candidate_id: 'cand123',
    message_id: 'msg123',
    provider: 'Blu',
    display_amount: 24000,
    clarification_question_type: 'category_expense',
    clarification_state: 'category_pending',
    _property_key: 'AIRO_SPRINT7F_PENDING_EMAIL_12345'
  };
  telegramSentText = '';
  ingestionLogUpdated = false;
  propertiesDeleted = [];

  const mockPayload = {
    postData: {
      contents: JSON.stringify({
        message: {
          chat: { id: 12345 },
          text: 'A'
        }
      })
    }
  };

  // Step 1: select A (Food & Drink) -> expect transition to subcategory_pending
  const result1 = airoSprint7FEmailAnswerMaybeHandleRoute_(mockPayload);
  pass('Step 1 returned ok', result1 && result1.ok === true);
  pass('Step 1 status is category selected', result1.status === 'sprint7h_email_category_selected');
  pass('Step 1 telegram prompt sent', telegramSentText.includes('Mock prompt for subcategories under Food & Drink'));
  pass('Step 1 state transitioned to subcategory_pending', loadedPending.clarification_state === 'subcategory_pending');
  pass('Step 1 category is Food & Drink', loadedPending.selected_category === 'Food & Drink');

  // Step 2: select subcategory 'a' (Jajan) -> expect resolution
  mockPayload.postData.contents = JSON.stringify({
    message: {
      chat: { id: 12345 },
      text: 'a'
    }
  });

  const result2 = airoSprint7FEmailAnswerMaybeHandleRoute_(mockPayload);
  pass('Step 2 returned ok', result2 && result2.ok === true);
  pass('Step 2 status is success', result2.status === 'success');
  pass('Ingestion log was updated', ingestionLogUpdated === true);
  pass('Pending properties were deleted', propertiesDeleted.includes('AIRO_SPRINT7F_PENDING_EMAIL_12345'));

  // New E-path UX tests
  
  // Test case E1: E does not directly become Other / Review, immediately returns full numbered category registry menu.
  loadedPending = {
    candidate_id: 'cand123',
    message_id: 'msg123',
    provider: 'Blu',
    display_amount: 24000,
    clarification_question_type: 'category_expense',
    clarification_state: 'category_pending',
    _property_key: 'AIRO_SPRINT7F_PENDING_EMAIL_12345'
  };
  telegramSentText = '';
  mockPayload.postData.contents = JSON.stringify({
    message: {
      chat: { id: 12345 },
      text: 'E'
    }
  });
  const resE = airoSprint7FEmailAnswerMaybeHandleRoute_(mockPayload);
  pass('E transitions to category_search_pending', loadedPending.clarification_state === 'category_search_pending');
  pass('E returns sprint7h_email_category_search_pending status', resE.status === 'sprint7h_email_category_search_pending');
  pass('E prompt immediately returns numbered registry menu', telegramSentText.includes('Pilih kategori:'));
  pass('E prompt menu includes Personal Care', telegramSentText.includes('Personal Care'));
  pass('E prompt menu includes 0. Other / Review', telegramSentText.includes('0. Other / Review'));

  // Test case E2: Replying with the number for Personal Care resolves to subcategory prompt.
  const registry = airoSprint7CategoryContractGetRegistry_();
  const categories = Object.keys(registry);
  const allowedCats = [];
  for (var c = 0; c < categories.length; c++) {
    if (categories[c] !== "Other / Review") allowedCats.push(categories[c]);
  }
  const pcIndex = allowedCats.indexOf("Personal Care");
  const pcNum = pcIndex + 1; // 1-based index
  
  telegramSentText = '';
  mockPayload.postData.contents = JSON.stringify({
    message: {
      chat: { id: 12345 },
      text: String(pcNum)
    }
  });
  const resNumMatch = airoSprint7FEmailAnswerMaybeHandleRoute_(mockPayload);
  pass('Replying with number for Personal Care transitions to subcategory_pending', loadedPending.clarification_state === 'subcategory_pending');
  pass('Replying with number sets category to Personal Care', loadedPending.selected_category === 'Personal Care');
  pass('Replying with number prompts subcategories', telegramSentText.includes('Mock prompt for subcategories under Personal Care'));

  // Test case E3: Replying with exact category text resolves.
  loadedPending = {
    candidate_id: 'cand123',
    message_id: 'msg123',
    provider: 'Blu',
    display_amount: 24000,
    clarification_question_type: 'category_expense',
    clarification_state: 'category_search_pending',
    _property_key: 'AIRO_SPRINT7F_PENDING_EMAIL_12345'
  };
  telegramSentText = '';
  mockPayload.postData.contents = JSON.stringify({
    message: {
      chat: { id: 12345 },
      text: 'Personal Care'
    }
  });
  const resTextMatch = airoSprint7FEmailAnswerMaybeHandleRoute_(mockPayload);
  pass('Replying with exact Personal Care transitions to subcategory_pending', loadedPending.clarification_state === 'subcategory_pending');
  pass('Replying with exact text sets category to Personal Care', loadedPending.selected_category === 'Personal Care');

  // Test case E4: Replying with lowercase exact category text resolves case-insensitively.
  loadedPending = {
    candidate_id: 'cand123',
    message_id: 'msg123',
    provider: 'Blu',
    display_amount: 24000,
    clarification_question_type: 'category_expense',
    clarification_state: 'category_search_pending',
    _property_key: 'AIRO_SPRINT7F_PENDING_EMAIL_12345'
  };
  telegramSentText = '';
  mockPayload.postData.contents = JSON.stringify({
    message: {
      chat: { id: 12345 },
      text: 'personal care'
    }
  });
  const resTextLowerMatch = airoSprint7FEmailAnswerMaybeHandleRoute_(mockPayload);
  pass('Replying with lowercase personal care transitions to subcategory_pending', loadedPending.clarification_state === 'subcategory_pending');
  pass('Replying with lowercase sets category to Personal Care', loadedPending.selected_category === 'Personal Care');

  // Test case E5: Replying with "0", "Other", or "Other / Review" routes safely to Review Queue fallback.
  loadedPending = {
    candidate_id: 'cand123',
    message_id: 'msg123',
    provider: 'Blu',
    display_amount: 24000,
    clarification_question_type: 'category_expense',
    clarification_state: 'category_search_pending',
    _property_key: 'AIRO_SPRINT7F_PENDING_EMAIL_12345'
  };
  ingestionLogUpdated = false;
  mockPayload.postData.contents = JSON.stringify({
    message: {
      chat: { id: 12345 },
      text: '0'
    }
  });
  const resZero = airoSprint7FEmailAnswerMaybeHandleRoute_(mockPayload);
  pass('Replying with 0 resolves to success status', resZero && resZero.ok === true && resZero.status === 'success');
  pass('Replying with 0 resolves to Review Queue', ingestionLogUpdated === true);

  // Test case E6: Invalid category input is rejected, sends warning message, keeps pending active.
  loadedPending = {
    candidate_id: 'cand123',
    message_id: 'msg123',
    provider: 'Blu',
    display_amount: 24000,
    clarification_question_type: 'category_expense',
    clarification_state: 'category_search_pending',
    _property_key: 'AIRO_SPRINT7F_PENDING_EMAIL_12345'
  };
  telegramSentText = '';
  mockPayload.postData.contents = JSON.stringify({
    message: {
      chat: { id: 12345 },
      text: 'random category name'
    }
  });
  const resInvalid = airoSprint7FEmailAnswerMaybeHandleRoute_(mockPayload);
  pass('Invalid category returns search invalid status', resInvalid && resInvalid.status === 'sprint7h_email_category_search_invalid');
  pass('Invalid category warns user and prints list', telegramSentText.includes('Kategori tidak didukung') && telegramSentText.includes('Personal Care'));
  pass('Invalid category keeps pending state active', loadedPending.clarification_state === 'category_search_pending');

  // Test case E7: /kategori while pending does not clear pending state.
  telegramSentText = '';
  mockPayload.postData.contents = JSON.stringify({
    message: {
      chat: { id: 12345 },
      text: '/kategori'
    }
  });
  const resKategoriCommand = airoSprint7CategoryContractKategoriCommandMaybeHandleRoute_(mockPayload);
  pass('/kategori command is handled', resKategoriCommand && resKategoriCommand.handled === true);
  pass('/kategori command shows full list', telegramSentText.includes('Category Registry v1') && telegramSentText.includes('Personal Care'));
  pass('/kategori command does not clear pending', loadedPending.clarification_state === 'category_search_pending');

  // Test case E8: After /kategori, user can still reply with number/exact text
  telegramSentText = '';
  mockPayload.postData.contents = JSON.stringify({
    message: {
      chat: { id: 12345 },
      text: String(pcNum)
    }
  });
  const resPostKategori = airoSprint7FEmailAnswerMaybeHandleRoute_(mockPayload);
  pass('Replying with number after /kategori transitions to subcategory_pending', loadedPending.clarification_state === 'subcategory_pending');
  pass('Replying with number after /kategori sets category to Personal Care', loadedPending.selected_category === 'Personal Care');

  // 8. Assert that write code functions are NOT referenced inside airoSprint7FEmailAnswerMaybeHandleRoute_
  const codeEmailRoute = extractFunction('airoSprint7FEmailAnswerMaybeHandleRoute_');
  const forbiddenKeywords = [
    'writeAccountLedgerMirror_',
    'appendByHeader_',
    'GmailApp',
    'thread.addLabel',
    'thread.moveToArchive',
    'createLabel'
  ];

  for (let keyword of forbiddenKeywords) {
    pass(`Safety: ${keyword} is NOT present in handle function`, !codeEmailRoute.includes(keyword));
  }

} catch (err) {
  console.error(err);
  process.exitCode = 1;
}

if (process.exitCode) process.exit(process.exitCode);
console.log('RESULT_CATEGORY_CONTRACT_EMAIL_STATIC=PASS');
