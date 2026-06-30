---
title: AIRO Arfin Gate C0 Exact Body Extract 2026-06-30
status: PASS_GATE_C0_EXACT_BODY_EXTRACTED
source_sha256: add9d5a538e48ed8cde6049f0632cbb8318c28e7074428ccc00dae7985353b19
head: 8244833d74fbd1088ae040a1f33e9fbb3578844a
generated_at_commit_time: 2026-06-30T23:00:12
---

> Gate C0 read-only exact-body extraction evidence. No source patch, deploy, API call, Gmail read, Telegram send, or workbook edit.

# AIRO Arfin Gate C0 Exact Body Extract

Generated: `2026-06-30T22:58:12`

## Verdict

```text
RESULT=PASS_GATE_C0_EXACT_BODY_EXTRACTED
NO_SOURCE_PATCH=YES
NO_DEPLOY=YES
NO_API_CALL=YES
NO_GMAIL_READ=YES
NO_TELEGRAM_SEND=YES
NO_WORKBOOK_EDIT=YES
```

## Source

- Source: `ecosystem/projects/vortex-ai-skill-lab/apps-script-prod-v2/AIRO_Finance_Multitab_Final_v1.js`
- SHA256: `add9d5a538e48ed8cde6049f0632cbb8318c28e7074428ccc00dae7985353b19`
- HEAD: `8244833d74fbd1088ae040a1f33e9fbb3578844a`
- Function count parsed: `693`

## Required Function Summary

| Function | Lines | Hits | Returns | Internal calls |
|---|---:|---:|---:|---|
| `airoSprint7FEmailAnswerMaybeHandleRoute_` | 22823-23165 | 84 | 27 | `airoSprint7CategoryContractBuildSubcategoryPrompt_, airoSprint7CategoryContractGetRegistry_, airoSprint7CategoryContractParseSubcategoryOption_, airoSprint7FBuildEmailPendingDisambiguationMessage_, airoSprint7FBuildFriendlyClarificationMessage_, airoSprint7FInferQuestionTypeFromPending_, airoSprint7FParseTelegramPayload_, airoSprint7FSelectPendingEmailCandidate_, airoSprint7FUpsertPendingEmailCandidate_, airoSprint7HResolveToReviewQueueFallback_, json_, sendTelegram_` |
| `airoSprint7HApprovalCommandMaybeHandleRoute_` | 24419-24570 | 26 | 3 | `airoSprint7FParseTelegramPayload_, airoSprint7FSpreadsheet_, airoSprint7HApprovalApprove_, airoSprint7HApprovalDetail_, airoSprint7HApprovalFix_, airoSprint7HApprovalList_, airoSprint7HApprovalReject_, airoTask614ApprovalHelp_, airoTask614GetDirectApprovalQueueId_, airoTask614ResolveApprovalArg_, json_, sendTelegram_` |
| `airoSprint7HApprovalApprove_` | 24230-24417 | 44 | 18 | `airoEnsureDateObject_, airoSprint7CategoryContractGetRegistry_, airoSprint7HFindItemInSheet_, airoSprint7HGetPendingItems_, airoTask614FindReviewItemByQueueId_, findHeader_, getSheetLoose_, parseAssetSection_, parseCreditor_, parseDate_, parseMerchant_, recordFinanceEventForWriteResult_, reviewHeaderMap_, routeReviewApprovedTab_, setReviewValue_, writeRouted_` |
| `airoSprint7HResolveToReviewQueueFallback_` | 23249-23526 | 78 | 3 | `airoC3GStablePendingAccount_, airoC3GStablePendingAmount_, airoC3GValidateEmailWritebackCandidate_, airoSprint7FFormatRupiah_, airoSprint7FRemovePendingEmailCandidate_, airoSprint7FSpreadsheet_, airoSprint7FUpdatePendingEmailResolution_, airoSprint7GNormalizeAmountForReadback_, airoTask614StoreDirectApproval_, appendByHeader_, buildRowByHeader_, canonicalKey_, fieldForHeader_, findHeader_, getSheetLoose_, json_` |
| `airoSprint7FUpsertPendingEmailCandidate_` | 22172-22191 | 7 | 3 | `airoSprint7FEmailPendingCandidateIdentity_, airoSprint7FLoadPendingEmailCandidateList_, airoSprint7FNormalizePendingEmailCandidate_, airoSprint7FSavePendingEmailCandidateList_` |
| `airoSprint7FUpdatePendingEmailResolution_` | 22460-22522 | 7 | 3 | `airoSprint7FEmailLogHeaders_, airoSprint7FEnsureResolutionHeaders_` |
| `writeInternalTransferToAccountLedger_` | 14519-14604 | 18 | 1 | `makeTxnId_, recordFinanceEventForWriteResult_, writeAccountLedgerMirror_, writeCashLedgerCompatibility_` |
| `writeRouted_` | 3820-3849 | 1 | 1 | `airoTask102RefreshDashboardMetadataAfterWrite_, airoWriteRoutedCore_` |
| `airoWriteRoutedCore_` | 3536-3818 | 41 | 17 | `amountForIntent_, appendByHeader_, canonicalSheetName_, detectInternalTransfer_, findProjectionRowByLedgerEntryId_, getSheetLoose_, makeTxnId_, parseDate_, recordFinanceEventForWriteResult_, stripQaTag_, withAccountLedgerPrimaryLock_, writeAccountLedgerMirror_, writeAccountLedgerPrimary_, writeAssetSafely_, writeCashLedgerCompatibility_, writeCreditCardSafely_` |
| `getAccountLedgerRowDetails_` | 1163-1186 | 2 | 2 | `getSheetLoose_` |
| `airoBuildFinanceWriteSuccessReply_` | 1188-1318 | 18 | 6 | `airoSprint7FFormatRupiah_, canonicalSheetName_, formatBalanceRupiah_, getAccountLedgerRowDetails_` |

## Insertion Candidates

- After `airoSprint7FEmailAnswerMaybeHandleRoute_` line `23165` — candidate location near related route/helper; review before patch
- After `airoSprint7HResolveToReviewQueueFallback_` line `23526` — candidate location near related route/helper; review before patch
- After `airoSprint7HApprovalCommandMaybeHandleRoute_` line `24570` — candidate location near related route/helper; review before patch
- After `writeInternalTransferToAccountLedger_` line `14604` — candidate location near related route/helper; review before patch
- After `airoBuildFinanceWriteSuccessReply_` line `1318` — candidate location near related route/helper; review before patch

## Global Funding/Transfer/Readback Hits

- L249: `Blu Pocket` — `if (hasAcc("Blu Pocket") && hasAcc("Blu")) {`
- L250: `Blu Pocket` — `routes.push({ source: "Blu Pocket", target: "Blu" });`
- L321: `Blu Pocket` — `if (hasAcc("Blu Pocket") && hasAcc("Blu")) {`
- L322: `Blu Pocket` — `routes.push({ source: "Blu Pocket", target: "Blu" });`
- L348: `Blu Pocket` — `'Contoh manual: transfer ' + amount + ' dari Blu Pocket ke Blu';`
- L1163: `getAccountLedgerRowDetails_` — `function getAccountLedgerRowDetails_(ss, row) {`
- L1182: `getAccountLedgerRowDetails_` — `Logger.log('getAccountLedgerRowDetails_ error: ' + e.message);`
- L1188: `airoBuildFinanceWriteSuccessReply_` — `function airoBuildFinanceWriteSuccessReply_(ss, plannedTab, finalTab, parsed, routedResult, tabLink) {`
- L1236: `getAccountLedgerRowDetails_` — `var sourceDetails = getAccountLedgerRowDetails_(spreadsheet, sourceRow);`
- L1237: `getAccountLedgerRowDetails_` — `var targetDetails = getAccountLedgerRowDetails_(spreadsheet, targetRow);`
- L1260: `getAccountLedgerRowDetails_` — `var details = getAccountLedgerRowDetails_(spreadsheet, rowToRead);`
- L2575: `airoBuildFinanceWriteSuccessReply_` — `const reply = airoBuildFinanceWriteSuccessReply_(ss, plannedTab, finalTab, parsed, routedResult, tabLink);`
- L3554: `writeInternalTransferToAccountLedger_` — `return writeInternalTransferToAccountLedger_(ss, parsed, rawText, common, transfer);`
- L4611: `Blu Pocket` — `if (/\bpocket\b/i.test(t)) return 'Blu Pocket';`
- L14301: `Blu Pocket` — `if (v === 'pocket blu' || v === 'blu pocket') return 'Blu Pocket';`
- L14302: `Blu Pocket` — `if (v === 'pocket blu cc' || v === 'blu pocket cc') return 'Blu Pocket CC';`
- L14519: `writeInternalTransferToAccountLedger_` — `function writeInternalTransferToAccountLedger_(ss, parsed, rawText, common, transfer) {`
- L17698: `Blu Pocket` — `lines.push("Total belum disisihkan ke Blu Pocket CC: " + formatBalanceRupiah_(totalPending));`
- L17921: `Blu Pocket` — `// Write to Account Ledger as internal transfer: Blu Pocket -> Blu Pocket CC`
- L17932: `Blu Pocket` — `var ledgerRawText = "transfer " + amountVal + " dr blu pocket ke blu pocket cc";`
- L17933: `Blu Pocket` — `var transferInfo = { sourceAccount: "Blu Pocket", targetAccount: "Blu Pocket CC" };`
- L17934: `writeInternalTransferToAccountLedger_` — `var ledgerResult = writeInternalTransferToAccountLedger_(ss, ledgerParsed, ledgerRawText, ledgerCommon, transferInfo);`
- L17944: `getAccountLedgerRowDetails_` — `var sourceDetails = getAccountLedgerRowDetails_(ss, ledgerSourceRow);`
- L17945: `getAccountLedgerRowDetails_` — `var targetDetails = getAccountLedgerRowDetails_(ss, ledgerTargetRow);`
- L17960: `Blu Pocket` — `if (vOutAcc !== "Blu Pocket") {`
- L17969: `Blu Pocket` — `} else if (vInAcc !== "Blu Pocket CC") {`
- L18009: `Blu Pocket` — `successLines.push("Transfer: Blu Pocket → Blu Pocket CC");`
- L18015: `Blu Pocket` — `successLines.push("Saldo Blu Pocket sekarang: " + formatBalanceRupiah_(sourceDetails.balance));`
- L18016: `Blu Pocket` — `successLines.push("Saldo Blu Pocket CC sekarang: " + formatBalanceRupiah_(targetDetails.balance));`
- L18114: `Blu Pocket` — `if (String(regValues[rIdx][2]).trim() === "Blu Pocket CC") {`
- L18120: `Blu Pocket` — `regSheet.appendRow(['TRUE', 'blu_pocket_cc', 'Blu Pocket CC', 'Blu', 'bank', 'Blu', 'pocket cc', 'Blu', '#4CD2FF', 'FALSE', 'TRUE', 'FALSE', 'Blu BCA Pocket CC account']);`
- L18141: `Blu Pocket` — `if ((row73Account === "" || row73Account === "null" || row73Account === "undefined") && row73In === 24000 && row73Type === "transfer_in" && row73Desc.indexOf("transfer 24000 dr blu pocket ke blu pocket cc") !== -1) {`
- L18147: `Blu Pocket` — `if (acc === "Blu Pocket CC" && bal !== "" && bal !== null && bal !== undefined) {`
- L18154: `Blu Pocket` — `ledgerSheet.getRange(73, 3).setValue("Blu Pocket CC");`
- L24230: `airoSprint7HApprovalApprove_` — `function airoSprint7HApprovalApprove_(ss, arg) {`
- L24464: `airoSprint7HApprovalApprove_` — `replyText = airoSprint7HApprovalApprove_(`
- L24523: `airoSprint7HApprovalApprove_` — `replyText = airoSprint7HApprovalApprove_(`
- L28055: `Blu Pocket` — `['TRUE', 'blu_pocket', 'Blu Pocket', 'Blu', 'bank', 'Blu', 'pocket', 'Blu', '#4CD2FF', 'FALSE', 'TRUE', 'FALSE', 'Blu BCA Pocket account'],`
- L28056: `Blu Pocket` — `['TRUE', 'blu_pocket_cc', 'Blu Pocket CC', 'Blu', 'bank', 'Blu', 'pocket cc', 'Blu', '#4CD2FF', 'FALSE', 'TRUE', 'FALSE', 'Blu BCA Pocket CC account'],`
- L28154: `Blu Pocket` — `{ account_id: "blu_pocket", account_name: "Blu Pocket", provider: "Blu", account_type: "bank", parent_account: "Blu", pocket_name: "pocket", is_cash: false, is_bank: true, is_credit: false },`
- L28155: `Blu Pocket` — `{ account_id: "blu_pocket_cc", account_name: "Blu Pocket CC", provider: "Blu", account_type: "bank", parent_account: "Blu", pocket_name: "pocket cc", is_cash: false, is_bank: true, is_credit: false },`
- L28578: `Blu Pocket` — `"Blu Pocket": { font: "#0891B2", fill: "#CFFAFE" },`
- L29526: `Blu Pocket` — `var tc1 = (parsed1.amount === 25000 && res1 && res1.sourceAccount === "Blu Pocket" && res1.targetAccount === "Blu");`
- L29530: `Blu Pocket` — `// Case 2: transfer 25rb dari blu pocket ke blu`
- L29531: `Blu Pocket` — `var text2 = "transfer 25rb dari blu pocket ke blu";`
- L29534: `Blu Pocket` — `var tc2 = (parsed2.amount === 25000 && res2 && res2.sourceAccount === "Blu Pocket" && res2.targetAccount === "Blu");`
- L29535: `Blu Pocket` — `results.push({ test: 'transfer 25rb dari blu pocket ke blu', passed: tc2, result: { amount: parsed2.amount, route: res2 } });`

## Exact Windows

### airoSprint7FEmailAnswerMaybeHandleRoute_ L22823-23165

#### function_start L22823-22863

```javascript
22823: function airoSprint7FEmailAnswerMaybeHandleRoute_(e) {
22824:   var parsed = airoSprint7FParseTelegramPayload_(e);
22825: if (!parsed.chat_id) {
22826:     return null;
22827:   }
22828: 
22829:   var selection = airoSprint7FSelectPendingEmailCandidate_(parsed.chat_id, parsed.text_raw);
22830:   if (selection.status === "missing") {
22831:     return null;
22832:   }
22833: 
22834:   var textRaw = String(selection.text_raw || "").trim();
22835:   var text = textRaw.toLowerCase();
22836: 
22837:   if (textRaw.indexOf("/") === 0) {
22838:     return null;
22839:   }
22840: 
22841:   if (selection.status === "ambiguous" || selection.status === "invalid_selector") {
22842:     sendTelegram_(parsed.chat_id, airoSprint7FBuildEmailPendingDisambiguationMessage_(selection.list));
22843:     return json_({
22844:       ok: true,
22845:       sprint: "8",
22846:       status: "task8_email_multi_pending_disambiguation_required",
22847:       handled: true,
22848:       waiting: true,
22849:       finance_write_performed: false,
22850:       account_ledger_write_performed: false,
22851:       finance_events_write_performed: false,
22852:       review_queue_write_performed: false,
22853:       gmail_read_performed: false,
22854:       gmail_modified: false,
22855:       mail_trigger_created: false,
22856:       pending_count: selection.list.length
22857:     });
22858:   }
22859: 
22860:   var pending = selection.pending;
22861:   if (!pending) {
22862:     return null;
22863:   }
```

#### function_end L23125-23165

```javascript
23125: 
23126:       var allowed = [];
23127:       var categories = Object.keys(registry);
23128:       for (var c = 0; c < categories.length; c++) {
23129:         if (categories[c] !== "Other / Review") allowed.push(categories[c]);
23130:       }
23131:       var listLines = ["Pilih kategori untuk email:\n"];
23132:       for (var i = 0; i < allowed.length; i++) {
23133:         listLines.push((i + 1) + ". " + allowed[i]);
23134:       }
23135:       listLines.push("0. Other / Review");
23136:       sendTelegram_(parsed.chat_id, listLines.join("\n"));
23137: 
23138:       return json_({
23139:         ok: true,
23140:         sprint: "7H",
23141:         status: "sprint7h_email_category_back",
23142:         handled: true,
23143:         waiting: true,
23144:         finance_write_performed: false
23145:       });
23146:     } else if (parsedOption.action === "review") {
23147:       return airoSprint7HResolveToReviewQueueFallback_(parsed, pending, "Other / Review", "Lainnya");
23148:     } else {
23149:       var subPromptRetry = "Pilihan subkategori tidak valid. Pilih subkategori yang sesuai (1/2/3...):\n" +
23150:                            airoSprint7CategoryContractBuildSubcategoryPrompt_(pending.selected_category);
23151:       sendTelegram_(parsed.chat_id, subPromptRetry);
23152: 
23153:       return json_({
23154:         ok: true,
23155:         sprint: "7H",
23156:         status: "sprint7h_email_subcategory_invalid",
23157:         handled: true,
23158:         waiting: true,
23159:         finance_write_performed: false
23160:       });
23161:     }
23162:   }
23163: 
23164:   return null;
23165: }
```

#### term_pending L22823-22837

```javascript
22823: function airoSprint7FEmailAnswerMaybeHandleRoute_(e) {
22824:   var parsed = airoSprint7FParseTelegramPayload_(e);
22825: if (!parsed.chat_id) {
22826:     return null;
22827:   }
22828: 
22829:   var selection = airoSprint7FSelectPendingEmailCandidate_(parsed.chat_id, parsed.text_raw);
22830:   if (selection.status === "missing") {
22831:     return null;
22832:   }
22833: 
22834:   var textRaw = String(selection.text_raw || "").trim();
22835:   var text = textRaw.toLowerCase();
22836: 
22837:   if (textRaw.indexOf("/") === 0) {
```

#### term_pending L22836-22850

```javascript
22836: 
22837:   if (textRaw.indexOf("/") === 0) {
22838:     return null;
22839:   }
22840: 
22841:   if (selection.status === "ambiguous" || selection.status === "invalid_selector") {
22842:     sendTelegram_(parsed.chat_id, airoSprint7FBuildEmailPendingDisambiguationMessage_(selection.list));
22843:     return json_({
22844:       ok: true,
22845:       sprint: "8",
22846:       status: "task8_email_multi_pending_disambiguation_required",
22847:       handled: true,
22848:       waiting: true,
22849:       finance_write_performed: false,
22850:       account_ledger_write_performed: false,
```

#### term_json_ L22837-22851

```javascript
22837:   if (textRaw.indexOf("/") === 0) {
22838:     return null;
22839:   }
22840: 
22841:   if (selection.status === "ambiguous" || selection.status === "invalid_selector") {
22842:     sendTelegram_(parsed.chat_id, airoSprint7FBuildEmailPendingDisambiguationMessage_(selection.list));
22843:     return json_({
22844:       ok: true,
22845:       sprint: "8",
22846:       status: "task8_email_multi_pending_disambiguation_required",
22847:       handled: true,
22848:       waiting: true,
22849:       finance_write_performed: false,
22850:       account_ledger_write_performed: false,
22851:       finance_events_write_performed: false,
```

#### term_pending L22840-22854

```javascript
22840: 
22841:   if (selection.status === "ambiguous" || selection.status === "invalid_selector") {
22842:     sendTelegram_(parsed.chat_id, airoSprint7FBuildEmailPendingDisambiguationMessage_(selection.list));
22843:     return json_({
22844:       ok: true,
22845:       sprint: "8",
22846:       status: "task8_email_multi_pending_disambiguation_required",
22847:       handled: true,
22848:       waiting: true,
22849:       finance_write_performed: false,
22850:       account_ledger_write_performed: false,
22851:       finance_events_write_performed: false,
22852:       review_queue_write_performed: false,
22853:       gmail_read_performed: false,
22854:       gmail_modified: false,
```

#### term_pending L22850-22864

```javascript
22850:       account_ledger_write_performed: false,
22851:       finance_events_write_performed: false,
22852:       review_queue_write_performed: false,
22853:       gmail_read_performed: false,
22854:       gmail_modified: false,
22855:       mail_trigger_created: false,
22856:       pending_count: selection.list.length
22857:     });
22858:   }
22859: 
22860:   var pending = selection.pending;
22861:   if (!pending) {
22862:     return null;
22863:   }
22864: 
```

#### term_pending L22854-22868

```javascript
22854:       gmail_modified: false,
22855:       mail_trigger_created: false,
22856:       pending_count: selection.list.length
22857:     });
22858:   }
22859: 
22860:   var pending = selection.pending;
22861:   if (!pending) {
22862:     return null;
22863:   }
22864: 
22865:   var state = String(pending.clarification_state || "category_pending").toLowerCase();
22866: 
22867:   if (state === "category_pending") {
22868:     var questionType = airoSprint7FInferQuestionTypeFromPending_(pending);
```

#### term_pending L22855-22869

```javascript
22855:       mail_trigger_created: false,
22856:       pending_count: selection.list.length
22857:     });
22858:   }
22859: 
22860:   var pending = selection.pending;
22861:   if (!pending) {
22862:     return null;
22863:   }
22864: 
22865:   var state = String(pending.clarification_state || "category_pending").toLowerCase();
22866: 
22867:   if (state === "category_pending") {
22868:     var questionType = airoSprint7FInferQuestionTypeFromPending_(pending);
22869:     pending.clarification_question_type = questionType;
```

#### term_pending L22859-22873

```javascript
22859: 
22860:   var pending = selection.pending;
22861:   if (!pending) {
22862:     return null;
22863:   }
22864: 
22865:   var state = String(pending.clarification_state || "category_pending").toLowerCase();
22866: 
22867:   if (state === "category_pending") {
22868:     var questionType = airoSprint7FInferQuestionTypeFromPending_(pending);
22869:     pending.clarification_question_type = questionType;
22870:     pending.question_type = questionType;
22871: 
22872:     if (questionType !== "category_expense" && questionType !== "category_income" && questionType !== "direction") {
22873:       sendTelegram_(parsed.chat_id, "⚠️ Tipe pertanyaan tidak dikenal. Gagal melanjutkan klarifikasi.");
```

### airoSprint7HApprovalCommandMaybeHandleRoute_ L24419-24570

#### function_start L24419-24459

```javascript
24419: function airoSprint7HApprovalCommandMaybeHandleRoute_(e) {
24420:   var parsed = airoSprint7FParseTelegramPayload_(e);
24421:   var rawText = String(parsed.text_raw || "").trim();
24422: 
24423:   var isStrict = /^\/approval(\b|@|$)/i.test(rawText);
24424:   if (!isStrict) {
24425:     return null;
24426:   }
24427: 
24428:   var parts = rawText.split(/\s+/);
24429:   var cmd = parts[1] ? parts[1].toLowerCase() : "";
24430:   var arg = parts[2] ? parts[2] : "";
24431: 
24432:   var ss = airoSprint7FSpreadsheet_();
24433: 
24434:   if (!ss) {
24435:     if (parsed.chat_id) {
24436:       sendTelegram_(
24437:         parsed.chat_id,
24438:         "Error: Spreadsheet tidak ditemukan."
24439:       );
24440:     }
24441: 
24442:     return json_({
24443:       ok: false,
24444:       error: "spreadsheet_missing"
24445:     });
24446:   }
24447: 
24448:   var replyText = "";
24449:   var resolvedArg = "";
24450:   var directQueueId = "";
24451:   var writePerformed = false;
24452: 
24453:   if (cmd === "") {
24454:     directQueueId =
24455:       airoTask614GetDirectApprovalQueueId_(
24456:         parsed.chat_id
24457:       );
24458: 
24459:     if (!directQueueId) {
```

#### function_end L24530-24570

```javascript
24530:           "Transaksi berhasil disetujui"
24531:         ) !== -1;
24532: 
24533:     } else if (cmd === "reject") {
24534:       replyText = airoSprint7HApprovalReject_(
24535:         ss,
24536:         resolvedArg
24537:       );
24538: 
24539:       writePerformed =
24540:         replyText.indexOf(
24541:           "Transaksi berhasil ditolak"
24542:         ) !== -1;
24543: 
24544:     } else {
24545:       replyText = airoSprint7HApprovalFix_(
24546:         ss,
24547:         resolvedArg
24548:       );
24549:     }
24550: 
24551:   } else {
24552:     replyText =
24553:       "Perintah approval tidak dikenal.\n\n" +
24554:       airoTask614ApprovalHelp_();
24555:   }
24556: 
24557:   if (parsed.chat_id && replyText) {
24558:     sendTelegram_(parsed.chat_id, replyText);
24559:   }
24560: 
24561:   return json_({
24562:     ok: true,
24563:     handled: true,
24564:     command: "approval_" + (cmd || "direct"),
24565:     argument: arg,
24566:     resolved_queue_id:
24567:       resolvedArg || directQueueId || "",
24568:     write_performed: writePerformed
24569:   });
24570: }
```

#### term_approval L24419-24427

```javascript
24419: function airoSprint7HApprovalCommandMaybeHandleRoute_(e) {
24420:   var parsed = airoSprint7FParseTelegramPayload_(e);
24421:   var rawText = String(parsed.text_raw || "").trim();
24422: 
24423:   var isStrict = /^\/approval(\b|@|$)/i.test(rawText);
24424:   if (!isStrict) {
24425:     return null;
24426:   }
24427: 
```

#### term__approval L24419-24431

```javascript
24419: function airoSprint7HApprovalCommandMaybeHandleRoute_(e) {
24420:   var parsed = airoSprint7FParseTelegramPayload_(e);
24421:   var rawText = String(parsed.text_raw || "").trim();
24422: 
24423:   var isStrict = /^\/approval(\b|@|$)/i.test(rawText);
24424:   if (!isStrict) {
24425:     return null;
24426:   }
24427: 
24428:   var parts = rawText.split(/\s+/);
24429:   var cmd = parts[1] ? parts[1].toLowerCase() : "";
24430:   var arg = parts[2] ? parts[2] : "";
24431: 
```

#### term_sendTelegram_ L24430-24444

```javascript
24430:   var arg = parts[2] ? parts[2] : "";
24431: 
24432:   var ss = airoSprint7FSpreadsheet_();
24433: 
24434:   if (!ss) {
24435:     if (parsed.chat_id) {
24436:       sendTelegram_(
24437:         parsed.chat_id,
24438:         "Error: Spreadsheet tidak ditemukan."
24439:       );
24440:     }
24441: 
24442:     return json_({
24443:       ok: false,
24444:       error: "spreadsheet_missing"
```

#### term_json_ L24436-24450

```javascript
24436:       sendTelegram_(
24437:         parsed.chat_id,
24438:         "Error: Spreadsheet tidak ditemukan."
24439:       );
24440:     }
24441: 
24442:     return json_({
24443:       ok: false,
24444:       error: "spreadsheet_missing"
24445:     });
24446:   }
24447: 
24448:   var replyText = "";
24449:   var resolvedArg = "";
24450:   var directQueueId = "";
```

#### term_approval L24449-24463

```javascript
24449:   var resolvedArg = "";
24450:   var directQueueId = "";
24451:   var writePerformed = false;
24452: 
24453:   if (cmd === "") {
24454:     directQueueId =
24455:       airoTask614GetDirectApprovalQueueId_(
24456:         parsed.chat_id
24457:       );
24458: 
24459:     if (!directQueueId) {
24460:       replyText =
24461:         "Tidak ada transaksi terakhir yang siap disetujui.\n\n" +
24462:         "Gunakan /approval list untuk melihat transaksi pending lainnya.";
24463:     } else {
```

#### term__approval L24456-24470

```javascript
24456:         parsed.chat_id
24457:       );
24458: 
24459:     if (!directQueueId) {
24460:       replyText =
24461:         "Tidak ada transaksi terakhir yang siap disetujui.\n\n" +
24462:         "Gunakan /approval list untuk melihat transaksi pending lainnya.";
24463:     } else {
24464:       replyText = airoSprint7HApprovalApprove_(
24465:         ss,
24466:         directQueueId
24467:       );
24468: 
24469:       writePerformed =
24470:         replyText.indexOf(
```

#### term_approval L24458-24472

```javascript
24458: 
24459:     if (!directQueueId) {
24460:       replyText =
24461:         "Tidak ada transaksi terakhir yang siap disetujui.\n\n" +
24462:         "Gunakan /approval list untuk melihat transaksi pending lainnya.";
24463:     } else {
24464:       replyText = airoSprint7HApprovalApprove_(
24465:         ss,
24466:         directQueueId
24467:       );
24468: 
24469:       writePerformed =
24470:         replyText.indexOf(
24471:           "Transaksi berhasil disetujui"
24472:         ) !== -1;
```

#### term_approval L24470-24484

```javascript
24470:         replyText.indexOf(
24471:           "Transaksi berhasil disetujui"
24472:         ) !== -1;
24473:     }
24474: 
24475:   } else if (cmd === "help") {
24476:     replyText = airoTask614ApprovalHelp_();
24477: 
24478:   } else if (cmd === "list") {
24479:     replyText = airoSprint7HApprovalList_(
24480:       ss,
24481:       parsed.chat_id
24482:     );
24483: 
24484:   } else if (
```

### airoSprint7HApprovalApprove_ L24230-24417

#### function_start L24230-24270

```javascript
24230: function airoSprint7HApprovalApprove_(ss, arg) {
24231:   if (!arg) {
24232:     return "Error: Harap masukkan nomor transaksi. Contoh: `/approval approve 1`";
24233:   }
24234: 
24235:   var sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.review);
24236:   if (!sheet) return "Error: Review Queue sheet missing.";
24237: 
24238:   var header = findHeader_(sheet);
24239:   if (!header) return "Error: Review Queue header missing.";
24240: 
24241:   var map = reviewHeaderMap_(header.headers);
24242: 
24243:   var pendingItems = airoSprint7HGetPendingItems_(ss);
24244: 
24245:   var item = /^review:/i.test(
24246:     String(arg || "").trim()
24247:   )
24248:     ? airoTask614FindReviewItemByQueueId_(ss, arg)
24249:     : airoSprint7HFindItemInSheet_(
24250:         ss,
24251:         arg,
24252:         pendingItems
24253:       );
24254:   if (!item) {
24255:     return "Transaksi tidak ditemukan.";
24256:   }
24257: 
24258:   var isAlreadyCommitted = (item.write_status === "committed" || item.linked_account_ledger_entry_id !== "");
24259:   if (isAlreadyCommitted) {
24260:     return "Dedupe hit: Transaksi ini sudah disetujui sebelumnya (already_committed).\nReadback: PASS.";
24261:   }
24262: 
24263:   // Pre-checks
24264:   if (item.write_policy !== "staging") {
24265:     return "Gagal: write_policy bukan staging (" + item.write_policy + ").";
24266:   }
24267:   if (item.write_status !== "pending" && item.review_status !== "pending") {
24268:     return "Gagal: status bukan pending (write_status: " + item.write_status + ", review_status: " + item.review_status + ").";
24269:   }
24270:   if (item.linked_account_ledger_entry_id !== "" || item.linked_event_id !== "") {
```

#### function_end L24377-24417

```javascript
24377:     setReviewValue_(sheet, item.rowNumber, map, ["reviewed_at"], new Date());
24378:     setReviewValue_(sheet, item.rowNumber, map, ["issue_reason"], "processed_to_" + result.writtenTab);
24379: 
24380:     if (result.financeEventRow) {
24381:       setReviewValue_(sheet, item.rowNumber, map, ["linked_event_id"], "fe:" + result.financeEventRow);
24382:     }
24383: 
24384:     var audit = ss.getSheetByName("_AIRO_Audit_Log");
24385:     if (audit) {
24386:       try {
24387:         audit.appendRow([
24388:           new Date(),
24389:           "AIRO",
24390:           "review_queue_approval",
24391:           "INFO",
24392:           "Review Queue Approval",
24393:           "Approved Review Queue item: " + item.queue_id,
24394:           "airoSprint7HApprovalCommandMaybeHandleRoute_",
24395:           JSON.stringify({
24396:             queue_id: item.queue_id,
24397:             ledger_row: result.row,
24398:             ledger_entry_id: result.rowId
24399:           })
24400:         ]);
24401:       } catch(e) {}
24402:     }
24403:   }
24404: 
24405:   if (writePerformed) {
24406:     var reply = "✅ Transaksi berhasil disetujui!\n\n" +
24407:                 "Nominal: Rp" + item.parsed_amount.toLocaleString("id-ID") + "\n" +
24408:                 "Akun: " + item.parsed_account + "\n" +
24409:                 "Kategori: " + item.parsed_category + (item.parsed_subcategory ? (" / " + item.parsed_subcategory) : "") + "\n" +
24410:                 "Ledger Entry ID: " + result.rowId + "\n" +
24411:                 "Finance Event Row: " + (result.financeEventRow || "-") + "\n" +
24412:                 "Readback: PASS.";
24413:     return reply;
24414:   } else {
24415:     return "Gagal menulis transaksi ke ledger.";
24416:   }
24417: }
```

#### term_approval L24230-24238

```javascript
24230: function airoSprint7HApprovalApprove_(ss, arg) {
24231:   if (!arg) {
24232:     return "Error: Harap masukkan nomor transaksi. Contoh: `/approval approve 1`";
24233:   }
24234: 
24235:   var sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.review);
24236:   if (!sheet) return "Error: Review Queue sheet missing.";
24237: 
24238:   var header = findHeader_(sheet);
```

#### term__approval L24230-24240

```javascript
24230: function airoSprint7HApprovalApprove_(ss, arg) {
24231:   if (!arg) {
24232:     return "Error: Harap masukkan nomor transaksi. Contoh: `/approval approve 1`";
24233:   }
24234: 
24235:   var sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.review);
24236:   if (!sheet) return "Error: Review Queue sheet missing.";
24237: 
24238:   var header = findHeader_(sheet);
24239:   if (!header) return "Error: Review Queue header missing.";
24240: 
```

#### term_Review_Queue L24230-24244

```javascript
24230: function airoSprint7HApprovalApprove_(ss, arg) {
24231:   if (!arg) {
24232:     return "Error: Harap masukkan nomor transaksi. Contoh: `/approval approve 1`";
24233:   }
24234: 
24235:   var sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.review);
24236:   if (!sheet) return "Error: Review Queue sheet missing.";
24237: 
24238:   var header = findHeader_(sheet);
24239:   if (!header) return "Error: Review Queue header missing.";
24240: 
24241:   var map = reviewHeaderMap_(header.headers);
24242: 
24243:   var pendingItems = airoSprint7HGetPendingItems_(ss);
24244: 
```

#### term_Review_Queue L24233-24247

```javascript
24233:   }
24234: 
24235:   var sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.review);
24236:   if (!sheet) return "Error: Review Queue sheet missing.";
24237: 
24238:   var header = findHeader_(sheet);
24239:   if (!header) return "Error: Review Queue header missing.";
24240: 
24241:   var map = reviewHeaderMap_(header.headers);
24242: 
24243:   var pendingItems = airoSprint7HGetPendingItems_(ss);
24244: 
24245:   var item = /^review:/i.test(
24246:     String(arg || "").trim()
24247:   )
```

#### term_pending L24237-24251

```javascript
24237: 
24238:   var header = findHeader_(sheet);
24239:   if (!header) return "Error: Review Queue header missing.";
24240: 
24241:   var map = reviewHeaderMap_(header.headers);
24242: 
24243:   var pendingItems = airoSprint7HGetPendingItems_(ss);
24244: 
24245:   var item = /^review:/i.test(
24246:     String(arg || "").trim()
24247:   )
24248:     ? airoTask614FindReviewItemByQueueId_(ss, arg)
24249:     : airoSprint7HFindItemInSheet_(
24250:         ss,
24251:         arg,
```

#### term_pending L24246-24260

```javascript
24246:     String(arg || "").trim()
24247:   )
24248:     ? airoTask614FindReviewItemByQueueId_(ss, arg)
24249:     : airoSprint7HFindItemInSheet_(
24250:         ss,
24251:         arg,
24252:         pendingItems
24253:       );
24254:   if (!item) {
24255:     return "Transaksi tidak ditemukan.";
24256:   }
24257: 
24258:   var isAlreadyCommitted = (item.write_status === "committed" || item.linked_account_ledger_entry_id !== "");
24259:   if (isAlreadyCommitted) {
24260:     return "Dedupe hit: Transaksi ini sudah disetujui sebelumnya (already_committed).\nReadback: PASS.";
```

#### term_entry_id L24252-24266

```javascript
24252:         pendingItems
24253:       );
24254:   if (!item) {
24255:     return "Transaksi tidak ditemukan.";
24256:   }
24257: 
24258:   var isAlreadyCommitted = (item.write_status === "committed" || item.linked_account_ledger_entry_id !== "");
24259:   if (isAlreadyCommitted) {
24260:     return "Dedupe hit: Transaksi ini sudah disetujui sebelumnya (already_committed).\nReadback: PASS.";
24261:   }
24262: 
24263:   // Pre-checks
24264:   if (item.write_policy !== "staging") {
24265:     return "Gagal: write_policy bukan staging (" + item.write_policy + ").";
24266:   }
```

#### term_Readback L24254-24268

```javascript
24254:   if (!item) {
24255:     return "Transaksi tidak ditemukan.";
24256:   }
24257: 
24258:   var isAlreadyCommitted = (item.write_status === "committed" || item.linked_account_ledger_entry_id !== "");
24259:   if (isAlreadyCommitted) {
24260:     return "Dedupe hit: Transaksi ini sudah disetujui sebelumnya (already_committed).\nReadback: PASS.";
24261:   }
24262: 
24263:   // Pre-checks
24264:   if (item.write_policy !== "staging") {
24265:     return "Gagal: write_policy bukan staging (" + item.write_policy + ").";
24266:   }
24267:   if (item.write_status !== "pending" && item.review_status !== "pending") {
24268:     return "Gagal: status bukan pending (write_status: " + item.write_status + ", review_status: " + item.review_status + ").";
```

### airoSprint7HResolveToReviewQueueFallback_ L23249-23526

#### function_start L23249-23289

```javascript
23249: function airoSprint7HResolveToReviewQueueFallback_(parsed, pending, category, subcategory) {
23250: 
23251:   // AIRO_C3G_WRITEBACK_FIX_ENTRY_BEGIN
23252:   category = String(category || "").trim();
23253:   subcategory = String(subcategory || "Lainnya").trim() || "Lainnya";
23254:   // AIRO_C3G_WRITEBACK_FIX_ENTRY_END
23255: 
23256:   var ss = airoSprint7FSpreadsheet_();
23257:   var resolved = {
23258:     ok: true,
23259:     answer: "A",
23260:     label: category,
23261:     category: category,
23262:     subcategory: subcategory,
23263:     cashflow_class: category === "Other / Review" ? "manual_review" : "expense",
23264:     domain: category === "Other / Review" ? "Review" : "Wallet"
23265:   };
23266: 
23267:   var updateResult = airoSprint7FUpdatePendingEmailResolution_(pending, resolved);
23268:   if (updateResult.updated) {
23269:     airoSprint7FRemovePendingEmailCandidate_(parsed.chat_id, pending);
23270:   }
23271: 
23272:   var amount = airoC3GStablePendingAmount_(pending);
23273:   var account = airoC3GStablePendingAccount_(pending);
23274:   var airoC3GValidation_ = airoC3GValidateEmailWritebackCandidate_(pending, amount, account, category);
23275:   if (!airoC3GValidation_.ok) {
23276:     sendTelegram_(
23277:       parsed.chat_id,
23278:       "⚠️ Resolusi email dibatalkan supaya tidak menulis data rusak.\n\n" +
23279:       "Alasan: " + airoC3GValidation_.reason + "\n" +
23280:       "Silakan reprocess email transaksi ini setelah pending candidate diperbaiki."
23281:     );
23282:     return json_({
23283:       ok: false,
23284:       status: "AIRO_C3G_WRITEBACK_BLOCKED_INVALID_PENDING_CANDIDATE",
23285:       handled: true,
23286:       reason: airoC3GValidation_.reason,
23287:       finance_write_performed: false,
23288:       account_ledger_write_performed: false,
23289:       finance_events_write_performed: false,
```

#### function_end L23486-23526

```javascript
23486:       }
23487:     }
23488:   }
23489: 
23490:   var replyText = "Resolusi transaksi email tersimpan ke Review Queue.\n\n" +
23491:                   "Nominal: " + airoSprint7FFormatRupiah_(amount) + "\n" +
23492:                   "Akun: " + account + "\n" +
23493:                   "Kategori: " + category + (category === "Other / Review" ? "" : (" / " + subcategory)) + "\n" +
23494:                   "Status: pending approval.\n" +
23495:                   "Balas /approval untuk langsung menyetujui transaksi ini.\n" +
23496:                   "Readback: " + (readbackVerified ? "PASS." : "Failed.");
23497: 
23498:   if (readbackVerified && targetRow > 0) {
23499:     airoTask614StoreDirectApproval_(
23500:       parsed.chat_id,
23501:       keyToFind,
23502:       targetRow
23503:     );
23504:   }
23505: 
23506:   sendTelegram_(parsed.chat_id, replyText);
23507: 
23508:   return json_({
23509:     ok: true,
23510:     sprint: "7H",
23511:     mode: "scheduled_polling_resolution",
23512:     status: "success",
23513:     handled: true,
23514:     resolved: true,
23515:     write_performed: true,
23516:     target_row: targetRow,
23517:     readback_verified: readbackVerified,
23518:     gmail_read_performed: false,
23519:     gmail_modified: false,
23520:     mail_trigger_created: false,
23521:     account_ledger_write_performed: false,
23522:     finance_events_write_performed: false,
23523:     review_queue_write_performed: true,
23524:     domain_tab_write_performed: false
23525:   });
23526: }
```

#### term_pending L23249-23257

```javascript
23249: function airoSprint7HResolveToReviewQueueFallback_(parsed, pending, category, subcategory) {
23250: 
23251:   // AIRO_C3G_WRITEBACK_FIX_ENTRY_BEGIN
23252:   category = String(category || "").trim();
23253:   subcategory = String(subcategory || "Lainnya").trim() || "Lainnya";
23254:   // AIRO_C3G_WRITEBACK_FIX_ENTRY_END
23255: 
23256:   var ss = airoSprint7FSpreadsheet_();
23257:   var resolved = {
```

#### term_category L23249-23260

```javascript
23249: function airoSprint7HResolveToReviewQueueFallback_(parsed, pending, category, subcategory) {
23250: 
23251:   // AIRO_C3G_WRITEBACK_FIX_ENTRY_BEGIN
23252:   category = String(category || "").trim();
23253:   subcategory = String(subcategory || "Lainnya").trim() || "Lainnya";
23254:   // AIRO_C3G_WRITEBACK_FIX_ENTRY_END
23255: 
23256:   var ss = airoSprint7FSpreadsheet_();
23257:   var resolved = {
23258:     ok: true,
23259:     answer: "A",
23260:     label: category,
```

#### term_category L23249-23261

```javascript
23249: function airoSprint7HResolveToReviewQueueFallback_(parsed, pending, category, subcategory) {
23250: 
23251:   // AIRO_C3G_WRITEBACK_FIX_ENTRY_BEGIN
23252:   category = String(category || "").trim();
23253:   subcategory = String(subcategory || "Lainnya").trim() || "Lainnya";
23254:   // AIRO_C3G_WRITEBACK_FIX_ENTRY_END
23255: 
23256:   var ss = airoSprint7FSpreadsheet_();
23257:   var resolved = {
23258:     ok: true,
23259:     answer: "A",
23260:     label: category,
23261:     category: category,
```

#### term_category L23254-23268

```javascript
23254:   // AIRO_C3G_WRITEBACK_FIX_ENTRY_END
23255: 
23256:   var ss = airoSprint7FSpreadsheet_();
23257:   var resolved = {
23258:     ok: true,
23259:     answer: "A",
23260:     label: category,
23261:     category: category,
23262:     subcategory: subcategory,
23263:     cashflow_class: category === "Other / Review" ? "manual_review" : "expense",
23264:     domain: category === "Other / Review" ? "Review" : "Wallet"
23265:   };
23266: 
23267:   var updateResult = airoSprint7FUpdatePendingEmailResolution_(pending, resolved);
23268:   if (updateResult.updated) {
```

#### term_category L23255-23269

```javascript
23255: 
23256:   var ss = airoSprint7FSpreadsheet_();
23257:   var resolved = {
23258:     ok: true,
23259:     answer: "A",
23260:     label: category,
23261:     category: category,
23262:     subcategory: subcategory,
23263:     cashflow_class: category === "Other / Review" ? "manual_review" : "expense",
23264:     domain: category === "Other / Review" ? "Review" : "Wallet"
23265:   };
23266: 
23267:   var updateResult = airoSprint7FUpdatePendingEmailResolution_(pending, resolved);
23268:   if (updateResult.updated) {
23269:     airoSprint7FRemovePendingEmailCandidate_(parsed.chat_id, pending);
```

#### term_category L23256-23270

```javascript
23256:   var ss = airoSprint7FSpreadsheet_();
23257:   var resolved = {
23258:     ok: true,
23259:     answer: "A",
23260:     label: category,
23261:     category: category,
23262:     subcategory: subcategory,
23263:     cashflow_class: category === "Other / Review" ? "manual_review" : "expense",
23264:     domain: category === "Other / Review" ? "Review" : "Wallet"
23265:   };
23266: 
23267:   var updateResult = airoSprint7FUpdatePendingEmailResolution_(pending, resolved);
23268:   if (updateResult.updated) {
23269:     airoSprint7FRemovePendingEmailCandidate_(parsed.chat_id, pending);
23270:   }
```

#### term_category L23257-23271

```javascript
23257:   var resolved = {
23258:     ok: true,
23259:     answer: "A",
23260:     label: category,
23261:     category: category,
23262:     subcategory: subcategory,
23263:     cashflow_class: category === "Other / Review" ? "manual_review" : "expense",
23264:     domain: category === "Other / Review" ? "Review" : "Wallet"
23265:   };
23266: 
23267:   var updateResult = airoSprint7FUpdatePendingEmailResolution_(pending, resolved);
23268:   if (updateResult.updated) {
23269:     airoSprint7FRemovePendingEmailCandidate_(parsed.chat_id, pending);
23270:   }
23271: 
```

#### term_category L23258-23272

```javascript
23258:     ok: true,
23259:     answer: "A",
23260:     label: category,
23261:     category: category,
23262:     subcategory: subcategory,
23263:     cashflow_class: category === "Other / Review" ? "manual_review" : "expense",
23264:     domain: category === "Other / Review" ? "Review" : "Wallet"
23265:   };
23266: 
23267:   var updateResult = airoSprint7FUpdatePendingEmailResolution_(pending, resolved);
23268:   if (updateResult.updated) {
23269:     airoSprint7FRemovePendingEmailCandidate_(parsed.chat_id, pending);
23270:   }
23271: 
23272:   var amount = airoC3GStablePendingAmount_(pending);
```

### airoSprint7FUpsertPendingEmailCandidate_ L22172-22191

#### function_start L22172-22191

```javascript
22172: function airoSprint7FUpsertPendingEmailCandidate_(chatId, pending) {
22173:   if (!chatId || !pending) return { ok: false, reason: "missing_chat_or_pending" };
22174:   var item = airoSprint7FNormalizePendingEmailCandidate_(pending);
22175:   var identity = airoSprint7FEmailPendingCandidateIdentity_(item);
22176:   if (!identity) return { ok: false, reason: "missing_identity" };
22177: 
22178:   var list = airoSprint7FLoadPendingEmailCandidateList_(chatId);
22179:   var replaced = false;
22180:   for (var i = 0; i < list.length; i++) {
22181:     if (airoSprint7FEmailPendingCandidateIdentity_(list[i]) === identity) {
22182:       list[i] = item;
22183:       replaced = true;
22184:       break;
22185:     }
22186:   }
22187:   if (!replaced) list.push(item);
22188: 
22189:   airoSprint7FSavePendingEmailCandidateList_(chatId, list);
22190:   return { ok: true, identity: identity, count: list.length, replaced: replaced };
22191: }
```

#### function_end L22172-22191

```javascript
22172: function airoSprint7FUpsertPendingEmailCandidate_(chatId, pending) {
22173:   if (!chatId || !pending) return { ok: false, reason: "missing_chat_or_pending" };
22174:   var item = airoSprint7FNormalizePendingEmailCandidate_(pending);
22175:   var identity = airoSprint7FEmailPendingCandidateIdentity_(item);
22176:   if (!identity) return { ok: false, reason: "missing_identity" };
22177: 
22178:   var list = airoSprint7FLoadPendingEmailCandidateList_(chatId);
22179:   var replaced = false;
22180:   for (var i = 0; i < list.length; i++) {
22181:     if (airoSprint7FEmailPendingCandidateIdentity_(list[i]) === identity) {
22182:       list[i] = item;
22183:       replaced = true;
22184:       break;
22185:     }
22186:   }
22187:   if (!replaced) list.push(item);
22188: 
22189:   airoSprint7FSavePendingEmailCandidateList_(chatId, list);
22190:   return { ok: true, identity: identity, count: list.length, replaced: replaced };
22191: }
```

#### term_pending L22172-22180

```javascript
22172: function airoSprint7FUpsertPendingEmailCandidate_(chatId, pending) {
22173:   if (!chatId || !pending) return { ok: false, reason: "missing_chat_or_pending" };
22174:   var item = airoSprint7FNormalizePendingEmailCandidate_(pending);
22175:   var identity = airoSprint7FEmailPendingCandidateIdentity_(item);
22176:   if (!identity) return { ok: false, reason: "missing_identity" };
22177: 
22178:   var list = airoSprint7FLoadPendingEmailCandidateList_(chatId);
22179:   var replaced = false;
22180:   for (var i = 0; i < list.length; i++) {
```

#### term_pending L22172-22181

```javascript
22172: function airoSprint7FUpsertPendingEmailCandidate_(chatId, pending) {
22173:   if (!chatId || !pending) return { ok: false, reason: "missing_chat_or_pending" };
22174:   var item = airoSprint7FNormalizePendingEmailCandidate_(pending);
22175:   var identity = airoSprint7FEmailPendingCandidateIdentity_(item);
22176:   if (!identity) return { ok: false, reason: "missing_identity" };
22177: 
22178:   var list = airoSprint7FLoadPendingEmailCandidateList_(chatId);
22179:   var replaced = false;
22180:   for (var i = 0; i < list.length; i++) {
22181:     if (airoSprint7FEmailPendingCandidateIdentity_(list[i]) === identity) {
```

#### term_pending L22172-22182

```javascript
22172: function airoSprint7FUpsertPendingEmailCandidate_(chatId, pending) {
22173:   if (!chatId || !pending) return { ok: false, reason: "missing_chat_or_pending" };
22174:   var item = airoSprint7FNormalizePendingEmailCandidate_(pending);
22175:   var identity = airoSprint7FEmailPendingCandidateIdentity_(item);
22176:   if (!identity) return { ok: false, reason: "missing_identity" };
22177: 
22178:   var list = airoSprint7FLoadPendingEmailCandidateList_(chatId);
22179:   var replaced = false;
22180:   for (var i = 0; i < list.length; i++) {
22181:     if (airoSprint7FEmailPendingCandidateIdentity_(list[i]) === identity) {
22182:       list[i] = item;
```

#### term_pending L22172-22183

```javascript
22172: function airoSprint7FUpsertPendingEmailCandidate_(chatId, pending) {
22173:   if (!chatId || !pending) return { ok: false, reason: "missing_chat_or_pending" };
22174:   var item = airoSprint7FNormalizePendingEmailCandidate_(pending);
22175:   var identity = airoSprint7FEmailPendingCandidateIdentity_(item);
22176:   if (!identity) return { ok: false, reason: "missing_identity" };
22177: 
22178:   var list = airoSprint7FLoadPendingEmailCandidateList_(chatId);
22179:   var replaced = false;
22180:   for (var i = 0; i < list.length; i++) {
22181:     if (airoSprint7FEmailPendingCandidateIdentity_(list[i]) === identity) {
22182:       list[i] = item;
22183:       replaced = true;
```

#### term_pending L22172-22186

```javascript
22172: function airoSprint7FUpsertPendingEmailCandidate_(chatId, pending) {
22173:   if (!chatId || !pending) return { ok: false, reason: "missing_chat_or_pending" };
22174:   var item = airoSprint7FNormalizePendingEmailCandidate_(pending);
22175:   var identity = airoSprint7FEmailPendingCandidateIdentity_(item);
22176:   if (!identity) return { ok: false, reason: "missing_identity" };
22177: 
22178:   var list = airoSprint7FLoadPendingEmailCandidateList_(chatId);
22179:   var replaced = false;
22180:   for (var i = 0; i < list.length; i++) {
22181:     if (airoSprint7FEmailPendingCandidateIdentity_(list[i]) === identity) {
22182:       list[i] = item;
22183:       replaced = true;
22184:       break;
22185:     }
22186:   }
```

#### term_pending L22175-22189

```javascript
22175:   var identity = airoSprint7FEmailPendingCandidateIdentity_(item);
22176:   if (!identity) return { ok: false, reason: "missing_identity" };
22177: 
22178:   var list = airoSprint7FLoadPendingEmailCandidateList_(chatId);
22179:   var replaced = false;
22180:   for (var i = 0; i < list.length; i++) {
22181:     if (airoSprint7FEmailPendingCandidateIdentity_(list[i]) === identity) {
22182:       list[i] = item;
22183:       replaced = true;
22184:       break;
22185:     }
22186:   }
22187:   if (!replaced) list.push(item);
22188: 
22189:   airoSprint7FSavePendingEmailCandidateList_(chatId, list);
```

#### term_pending L22183-22191

```javascript
22183:       replaced = true;
22184:       break;
22185:     }
22186:   }
22187:   if (!replaced) list.push(item);
22188: 
22189:   airoSprint7FSavePendingEmailCandidateList_(chatId, list);
22190:   return { ok: true, identity: identity, count: list.length, replaced: replaced };
22191: }
```

### airoSprint7FUpdatePendingEmailResolution_ L22460-22522

#### function_start L22460-22500

```javascript
22460: function airoSprint7FUpdatePendingEmailResolution_(pending, resolved) {
22461:   var sheet = airoSprint7FEnsureResolutionHeaders_();
22462:   var headers = airoSprint7FEmailLogHeaders_();
22463: 
22464:   if (sheet.getLastRow() < 2) {
22465:     return {
22466:       updated: false,
22467:       row_number: 0,
22468:       reason: "email_log_empty"
22469:     };
22470:   }
22471: 
22472:   var values = sheet.getRange(2, 1, sheet.getLastRow() - 1, headers.length).getValues();
22473:   var messageCol = headers.indexOf("message_id");
22474:   var candidateCol = headers.indexOf("candidate_id");
22475: 
22476:   var targetRow = 0;
22477:   for (var i = 0; i < values.length; i++) {
22478:     var rowMessageId = String(values[i][messageCol] || "").trim();
22479:     var rowCandidateId = String(values[i][candidateCol] || "").trim();
22480: 
22481:     if (
22482:       rowMessageId === String(pending.message_id || "").trim() ||
22483:       rowCandidateId === String(pending.candidate_id || "").trim()
22484:     ) {
22485:       targetRow = i + 2;
22486:       break;
22487:     }
22488:   }
22489: 
22490:   if (!targetRow) {
22491:     return {
22492:       updated: false,
22493:       row_number: 0,
22494:       reason: "pending_candidate_not_found"
22495:     };
22496:   }
22497: 
22498:   var now = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyy-MM-dd'T'HH:mm:ssXXX");
22499: 
22500:   var updates = {
```

#### function_end L22482-22522

```javascript
22482:       rowMessageId === String(pending.message_id || "").trim() ||
22483:       rowCandidateId === String(pending.candidate_id || "").trim()
22484:     ) {
22485:       targetRow = i + 2;
22486:       break;
22487:     }
22488:   }
22489: 
22490:   if (!targetRow) {
22491:     return {
22492:       updated: false,
22493:       row_number: 0,
22494:       reason: "pending_candidate_not_found"
22495:     };
22496:   }
22497: 
22498:   var now = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyy-MM-dd'T'HH:mm:ssXXX");
22499: 
22500:   var updates = {
22501:     clarification_status: "resolved",
22502:     resolved_answer: resolved.answer,
22503:     resolved_label: resolved.label,
22504:     resolved_at: now,
22505:     write_allowed: "false",
22506:     write_performed: "false",
22507:     notes: "Resolved by Telegram answer in Sprint 7F-D route preview. Finance write remains disabled."
22508:   };
22509: 
22510:   Object.keys(updates).forEach(function(key) {
22511:     var col = headers.indexOf(key);
22512:     if (col >= 0) {
22513:       sheet.getRange(targetRow, col + 1).setValue(updates[key]);
22514:     }
22515:   });
22516: 
22517:   return {
22518:     updated: true,
22519:     row_number: targetRow,
22520:     resolved_at: now
22521:   };
22522: }
```

#### term_pending L22460-22468

```javascript
22460: function airoSprint7FUpdatePendingEmailResolution_(pending, resolved) {
22461:   var sheet = airoSprint7FEnsureResolutionHeaders_();
22462:   var headers = airoSprint7FEmailLogHeaders_();
22463: 
22464:   if (sheet.getLastRow() < 2) {
22465:     return {
22466:       updated: false,
22467:       row_number: 0,
22468:       reason: "email_log_empty"
```

#### term_resolution L22460-22469

```javascript
22460: function airoSprint7FUpdatePendingEmailResolution_(pending, resolved) {
22461:   var sheet = airoSprint7FEnsureResolutionHeaders_();
22462:   var headers = airoSprint7FEmailLogHeaders_();
22463: 
22464:   if (sheet.getLastRow() < 2) {
22465:     return {
22466:       updated: false,
22467:       row_number: 0,
22468:       reason: "email_log_empty"
22469:     };
```

#### term_candidate L22468-22482

```javascript
22468:       reason: "email_log_empty"
22469:     };
22470:   }
22471: 
22472:   var values = sheet.getRange(2, 1, sheet.getLastRow() - 1, headers.length).getValues();
22473:   var messageCol = headers.indexOf("message_id");
22474:   var candidateCol = headers.indexOf("candidate_id");
22475: 
22476:   var targetRow = 0;
22477:   for (var i = 0; i < values.length; i++) {
22478:     var rowMessageId = String(values[i][messageCol] || "").trim();
22479:     var rowCandidateId = String(values[i][candidateCol] || "").trim();
22480: 
22481:     if (
22482:       rowMessageId === String(pending.message_id || "").trim() ||
```

#### term_candidate L22473-22487

```javascript
22473:   var messageCol = headers.indexOf("message_id");
22474:   var candidateCol = headers.indexOf("candidate_id");
22475: 
22476:   var targetRow = 0;
22477:   for (var i = 0; i < values.length; i++) {
22478:     var rowMessageId = String(values[i][messageCol] || "").trim();
22479:     var rowCandidateId = String(values[i][candidateCol] || "").trim();
22480: 
22481:     if (
22482:       rowMessageId === String(pending.message_id || "").trim() ||
22483:       rowCandidateId === String(pending.candidate_id || "").trim()
22484:     ) {
22485:       targetRow = i + 2;
22486:       break;
22487:     }
```

#### term_pending L22476-22490

```javascript
22476:   var targetRow = 0;
22477:   for (var i = 0; i < values.length; i++) {
22478:     var rowMessageId = String(values[i][messageCol] || "").trim();
22479:     var rowCandidateId = String(values[i][candidateCol] || "").trim();
22480: 
22481:     if (
22482:       rowMessageId === String(pending.message_id || "").trim() ||
22483:       rowCandidateId === String(pending.candidate_id || "").trim()
22484:     ) {
22485:       targetRow = i + 2;
22486:       break;
22487:     }
22488:   }
22489: 
22490:   if (!targetRow) {
```

#### term_pending L22477-22491

```javascript
22477:   for (var i = 0; i < values.length; i++) {
22478:     var rowMessageId = String(values[i][messageCol] || "").trim();
22479:     var rowCandidateId = String(values[i][candidateCol] || "").trim();
22480: 
22481:     if (
22482:       rowMessageId === String(pending.message_id || "").trim() ||
22483:       rowCandidateId === String(pending.candidate_id || "").trim()
22484:     ) {
22485:       targetRow = i + 2;
22486:       break;
22487:     }
22488:   }
22489: 
22490:   if (!targetRow) {
22491:     return {
```

#### term_pending L22488-22502

```javascript
22488:   }
22489: 
22490:   if (!targetRow) {
22491:     return {
22492:       updated: false,
22493:       row_number: 0,
22494:       reason: "pending_candidate_not_found"
22495:     };
22496:   }
22497: 
22498:   var now = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyy-MM-dd'T'HH:mm:ssXXX");
22499: 
22500:   var updates = {
22501:     clarification_status: "resolved",
22502:     resolved_answer: resolved.answer,
```

### writeInternalTransferToAccountLedger_ L14519-14604

#### function_start L14519-14559

```javascript
14519: function writeInternalTransferToAccountLedger_(ss, parsed, rawText, common, transfer) {
14520:   var sharedTxnId = (common && (common.linked_txn_id || common.rowId)) || makeTxnId_({}, rawText);
14521: 
14522:   // Write Source Outflow Row
14523:   var parsedOut = {
14524:     ...parsed,
14525:     account: transfer.sourceAccount,
14526:     type: 'transfer_out',
14527:     amount: parsed.amount
14528:   };
14529:   var commonOut = {
14530:     ...common,
14531:     rowId: sharedTxnId + ':out',
14532:     linked_txn_id: sharedTxnId + ':in'
14533:   };
14534:   var outResult = writeAccountLedgerMirror_(ss, parsedOut, rawText, commonOut, transfer.sourceAccount);
14535: 
14536:   // Write Target Inflow Row
14537:   var parsedIn = {
14538:     ...parsed,
14539:     account: transfer.targetAccount,
14540:     type: 'transfer_in',
14541:     amount: parsed.amount
14542:   };
14543:   var commonIn = {
14544:     ...common,
14545:     rowId: sharedTxnId + ':in',
14546:     linked_txn_id: sharedTxnId + ':out'
14547:   };
14548:   var inResult = writeAccountLedgerMirror_(ss, parsedIn, rawText, commonIn, transfer.targetAccount);
14549: 
14550:   // Cash Ledger compatibility layer synchronization
14551:   var cashResult = null;
14552:   if (transfer.targetAccount === 'Cash') {
14553:     var parsedCashIn = {
14554:       ...parsed,
14555:       account: 'Cash',
14556:       type: 'transfer_in',
14557:       amount: parsed.amount
14558:     };
14559:     cashResult = writeCashLedgerCompatibility_(ss, parsedCashIn, rawText, common);
```

#### function_end L14564-14604

```javascript
14564:       type: 'transfer_out',
14565:       amount: parsed.amount
14566:     };
14567:     cashResult = writeCashLedgerCompatibility_(ss, parsedCashOut, rawText, common);
14568:   }
14569: 
14570:   var transferResult = {
14571:     status: 'written',
14572:     writtenTab: AIRO_CONFIG.tabs.accountLedger,
14573:     rowId: sharedTxnId,
14574:     row: (outResult && outResult.row) ? outResult.row : '',
14575:     writeVerified: Boolean(outResult && outResult.row && inResult && inResult.row),
14576:     transferInternal: true,
14577:     sourceAccount: transfer.sourceAccount,
14578:     targetAccount: transfer.targetAccount,
14579:     accountLedgerRows: [
14580:       (outResult && outResult.row) ? outResult.row : null,
14581:       (inResult && inResult.row) ? inResult.row : null
14582:     ],
14583:     cashLedgerRow: (cashResult && cashResult.row) ? cashResult.row : null
14584:   };
14585: 
14586:   if (transferResult.writeVerified) {
14587:     // AIRO_INTERNAL_TRANSFER_FINANCE_EVENT_EMISSION_V1
14588:     // Internal transfer writes two Account Ledger rows and one Finance Events index row.
14589:     recordFinanceEventForWriteResult_(ss, transferResult, common, parsed, rawText, {
14590:       event_type: 'internal_transfer',
14591:       event_source: 'telegram',
14592:       source_tab: AIRO_CONFIG.tabs.accountLedger,
14593:       source_row: String(transferResult.accountLedgerRows[0] || '') + ',' + String(transferResult.accountLedgerRows[1] || ''),
14594:       linked_txn_id: sharedTxnId,
14595:       account: String(transfer.sourceAccount || '') + ' -> ' + String(transfer.targetAccount || ''),
14596:       category: parsed.category || 'Lainnya',
14597:       amount: parsed.amount || '',
14598:       direction: 'transfer',
14599:       notes: 'internal_transfer'
14600:     });
14601:   }
14602: 
14603:   return transferResult;
14604: }
```

#### term_writeInternalTransferToAccountLedger_ L14519-14527

```javascript
14519: function writeInternalTransferToAccountLedger_(ss, parsed, rawText, common, transfer) {
14520:   var sharedTxnId = (common && (common.linked_txn_id || common.rowId)) || makeTxnId_({}, rawText);
14521: 
14522:   // Write Source Outflow Row
14523:   var parsedOut = {
14524:     ...parsed,
14525:     account: transfer.sourceAccount,
14526:     type: 'transfer_out',
14527:     amount: parsed.amount
```

#### term_linked_txn_id L14519-14528

```javascript
14519: function writeInternalTransferToAccountLedger_(ss, parsed, rawText, common, transfer) {
14520:   var sharedTxnId = (common && (common.linked_txn_id || common.rowId)) || makeTxnId_({}, rawText);
14521: 
14522:   // Write Source Outflow Row
14523:   var parsedOut = {
14524:     ...parsed,
14525:     account: transfer.sourceAccount,
14526:     type: 'transfer_out',
14527:     amount: parsed.amount
14528:   };
```

#### term_linked_txn_id L14526-14540

```javascript
14526:     type: 'transfer_out',
14527:     amount: parsed.amount
14528:   };
14529:   var commonOut = {
14530:     ...common,
14531:     rowId: sharedTxnId + ':out',
14532:     linked_txn_id: sharedTxnId + ':in'
14533:   };
14534:   var outResult = writeAccountLedgerMirror_(ss, parsedOut, rawText, commonOut, transfer.sourceAccount);
14535: 
14536:   // Write Target Inflow Row
14537:   var parsedIn = {
14538:     ...parsed,
14539:     account: transfer.targetAccount,
14540:     type: 'transfer_in',
```

#### term_linked_txn_id L14540-14554

```javascript
14540:     type: 'transfer_in',
14541:     amount: parsed.amount
14542:   };
14543:   var commonIn = {
14544:     ...common,
14545:     rowId: sharedTxnId + ':in',
14546:     linked_txn_id: sharedTxnId + ':out'
14547:   };
14548:   var inResult = writeAccountLedgerMirror_(ss, parsedIn, rawText, commonIn, transfer.targetAccount);
14549: 
14550:   // Cash Ledger compatibility layer synchronization
14551:   var cashResult = null;
14552:   if (transfer.targetAccount === 'Cash') {
14553:     var parsedCashIn = {
14554:       ...parsed,
```

#### term_Cash L14544-14558

```javascript
14544:     ...common,
14545:     rowId: sharedTxnId + ':in',
14546:     linked_txn_id: sharedTxnId + ':out'
14547:   };
14548:   var inResult = writeAccountLedgerMirror_(ss, parsedIn, rawText, commonIn, transfer.targetAccount);
14549: 
14550:   // Cash Ledger compatibility layer synchronization
14551:   var cashResult = null;
14552:   if (transfer.targetAccount === 'Cash') {
14553:     var parsedCashIn = {
14554:       ...parsed,
14555:       account: 'Cash',
14556:       type: 'transfer_in',
14557:       amount: parsed.amount
14558:     };
```

#### term_Cash L14545-14559

```javascript
14545:     rowId: sharedTxnId + ':in',
14546:     linked_txn_id: sharedTxnId + ':out'
14547:   };
14548:   var inResult = writeAccountLedgerMirror_(ss, parsedIn, rawText, commonIn, transfer.targetAccount);
14549: 
14550:   // Cash Ledger compatibility layer synchronization
14551:   var cashResult = null;
14552:   if (transfer.targetAccount === 'Cash') {
14553:     var parsedCashIn = {
14554:       ...parsed,
14555:       account: 'Cash',
14556:       type: 'transfer_in',
14557:       amount: parsed.amount
14558:     };
14559:     cashResult = writeCashLedgerCompatibility_(ss, parsedCashIn, rawText, common);
```

#### term_Cash L14546-14560

```javascript
14546:     linked_txn_id: sharedTxnId + ':out'
14547:   };
14548:   var inResult = writeAccountLedgerMirror_(ss, parsedIn, rawText, commonIn, transfer.targetAccount);
14549: 
14550:   // Cash Ledger compatibility layer synchronization
14551:   var cashResult = null;
14552:   if (transfer.targetAccount === 'Cash') {
14553:     var parsedCashIn = {
14554:       ...parsed,
14555:       account: 'Cash',
14556:       type: 'transfer_in',
14557:       amount: parsed.amount
14558:     };
14559:     cashResult = writeCashLedgerCompatibility_(ss, parsedCashIn, rawText, common);
14560:   } else if (transfer.sourceAccount === 'Cash') {
```

#### term_Cash L14547-14561

```javascript
14547:   };
14548:   var inResult = writeAccountLedgerMirror_(ss, parsedIn, rawText, commonIn, transfer.targetAccount);
14549: 
14550:   // Cash Ledger compatibility layer synchronization
14551:   var cashResult = null;
14552:   if (transfer.targetAccount === 'Cash') {
14553:     var parsedCashIn = {
14554:       ...parsed,
14555:       account: 'Cash',
14556:       type: 'transfer_in',
14557:       amount: parsed.amount
14558:     };
14559:     cashResult = writeCashLedgerCompatibility_(ss, parsedCashIn, rawText, common);
14560:   } else if (transfer.sourceAccount === 'Cash') {
14561:     var parsedCashOut = {
```

### writeRouted_ L3820-3849

#### function_start L3820-3849

```javascript
3820: function writeRouted_(ss, plannedTab, parsed, rawText, common) {
3821:   var routedResult = airoWriteRoutedCore_(
3822:     ss,
3823:     plannedTab,
3824:     parsed,
3825:     rawText,
3826:     common
3827:   );
3828: 
3829:   try {
3830:     airoTask102RefreshDashboardMetadataAfterWrite_(
3831:       ss,
3832:       routedResult
3833:     );
3834:   } catch (dashboardRefreshError) {
3835:     try {
3836:       Logger.log(
3837:         'AIRO_TASK10_1_POST_WRITE_REFRESH_ERROR=' +
3838:         String(
3839:           dashboardRefreshError &&
3840:           dashboardRefreshError.message
3841:             ? dashboardRefreshError.message
3842:             : dashboardRefreshError
3843:         )
3844:       );
3845:     } catch (loggerError) {}
3846:   }
3847: 
3848:   return routedResult;
3849: }
```

#### function_end L3820-3849

```javascript
3820: function writeRouted_(ss, plannedTab, parsed, rawText, common) {
3821:   var routedResult = airoWriteRoutedCore_(
3822:     ss,
3823:     plannedTab,
3824:     parsed,
3825:     rawText,
3826:     common
3827:   );
3828: 
3829:   try {
3830:     airoTask102RefreshDashboardMetadataAfterWrite_(
3831:       ss,
3832:       routedResult
3833:     );
3834:   } catch (dashboardRefreshError) {
3835:     try {
3836:       Logger.log(
3837:         'AIRO_TASK10_1_POST_WRITE_REFRESH_ERROR=' +
3838:         String(
3839:           dashboardRefreshError &&
3840:           dashboardRefreshError.message
3841:             ? dashboardRefreshError.message
3842:             : dashboardRefreshError
3843:         )
3844:       );
3845:     } catch (loggerError) {}
3846:   }
3847: 
3848:   return routedResult;
3849: }
```

#### term_writeRouted_ L3820-3828

```javascript
3820: function writeRouted_(ss, plannedTab, parsed, rawText, common) {
3821:   var routedResult = airoWriteRoutedCore_(
3822:     ss,
3823:     plannedTab,
3824:     parsed,
3825:     rawText,
3826:     common
3827:   );
3828: 
```

### airoWriteRoutedCore_ L3536-3818

#### function_start L3536-3576

```javascript
3536: function airoWriteRoutedCore_(ss, plannedTab, parsed, rawText, common) {
3537:   const tabName = plannedTab || AIRO_CONFIG.tabs.transactions;
3538:   const key = canonicalSheetName_(tabName);
3539: 
3540:   if (key.includes('credit card')) {
3541:     return writeCreditCardSafely_(ss, parsed, rawText, common);
3542:   }
3543: 
3544:   if (key.includes('hutang')) {
3545:     return writeHutangSafely_(ss, parsed, rawText, common);
3546:   }
3547: 
3548:   if (key.includes('aset')) {
3549:     return writeAssetSafely_(ss, parsed, rawText, common);
3550:   }
3551: 
3552:   var transfer = detectInternalTransfer_(parsed, rawText);
3553:   if (transfer) {
3554:     return writeInternalTransferToAccountLedger_(ss, parsed, rawText, common, transfer);
3555:   }
3556: 
3557:   if (key.includes('cash ledger')) {
3558:     // AIRO_SPRINT3_CASH_MIRROR_WHEN_COMPAT_DISABLED_V1
3559:     // Sprint 3 disables new Cash Ledger writes by default, but cash movement
3560:     // must still be written to Account Ledger as the primary wallet ledger.
3561:     const cashResult = writeCashLedgerCompatibility_(ss, parsed, rawText, common);
3562:     const ledgerResult = writeAccountLedgerMirror_(ss, parsed, rawText, common, AIRO_CONFIG.tabs.cash);
3563: 
3564:     if (ledgerResult && ledgerResult.status === 'written') {
3565:       // AIRO_SPRINT4_CASH_ROUTE_FINANCE_EVENT_EMISSION_V1
3566:       // Cash route returns before the generic appendByHeader_ path, so it must
3567:       // emit Finance Events here after the Account Ledger source-of-truth write.
3568:       const finalResult = {
3569:         ...ledgerResult,
3570:         writtenTab: AIRO_CONFIG.tabs.accountLedger,
3571:         cashLedgerCompatibilityStatus: cashResult && cashResult.status ? cashResult.status : '',
3572:         cashLedgerCompatibilityReason: cashResult && cashResult.reason ? cashResult.reason : ''
3573:       };
3574: 
3575:       recordFinanceEventForWriteResult_(ss, finalResult, common, parsed, rawText, {
3576:         event_type: 'transaction_created',
```

#### function_end L3778-3818

```javascript
3778:           {
3779:             event_type: 'cicilan_payment',
3780:             event_source: 'telegram',
3781:             source_tab: AIRO_CONFIG.tabs.cicilanRumah,
3782:             source_row: finalResult.row || '',
3783:             linked_txn_id: ledgerResult.entry_id
3784:           }
3785:         );
3786: 
3787:         return finalResult;
3788:       } catch (error) {
3789:         return {
3790:           status: 'partial',
3791:           reason:
3792:             'cicilan_domain_projection_exception|' +
3793:             'account_ledger_entry_id=' +
3794:             ledgerResult.entry_id +
3795:             '|' +
3796:             String(
3797:               error && error.message
3798:                 ? error.message
3799:                 : error
3800:             ),
3801:           account_ledger_entry_id: ledgerResult.entry_id,
3802:           account_ledger_result: ledgerResult,
3803:           domain_projection_status: 'failed'
3804:         };
3805:       }
3806:     });
3807:   }
3808: 
3809:   const result = appendByHeader_(ss, tabName, common, { createIfMissing: false });
3810:   recordFinanceEventForWriteResult_(ss, result, common, parsed, rawText, {
3811:     event_type: 'transaction_created',
3812:     event_source: 'telegram',
3813:     source_tab: result.writtenTab || tabName,
3814:     source_row: result.row || '',
3815:     linked_txn_id: common.linked_txn_id || common.rowId || ''
3816:   });
3817:   return result;
3818: }
```

#### term_writeInternalTransferToAccountLedger_ L3548-3562

```javascript
3548:   if (key.includes('aset')) {
3549:     return writeAssetSafely_(ss, parsed, rawText, common);
3550:   }
3551: 
3552:   var transfer = detectInternalTransfer_(parsed, rawText);
3553:   if (transfer) {
3554:     return writeInternalTransferToAccountLedger_(ss, parsed, rawText, common, transfer);
3555:   }
3556: 
3557:   if (key.includes('cash ledger')) {
3558:     // AIRO_SPRINT3_CASH_MIRROR_WHEN_COMPAT_DISABLED_V1
3559:     // Sprint 3 disables new Cash Ledger writes by default, but cash movement
3560:     // must still be written to Account Ledger as the primary wallet ledger.
3561:     const cashResult = writeCashLedgerCompatibility_(ss, parsed, rawText, common);
3562:     const ledgerResult = writeAccountLedgerMirror_(ss, parsed, rawText, common, AIRO_CONFIG.tabs.cash);
```

#### term_Cash L3551-3565

```javascript
3551: 
3552:   var transfer = detectInternalTransfer_(parsed, rawText);
3553:   if (transfer) {
3554:     return writeInternalTransferToAccountLedger_(ss, parsed, rawText, common, transfer);
3555:   }
3556: 
3557:   if (key.includes('cash ledger')) {
3558:     // AIRO_SPRINT3_CASH_MIRROR_WHEN_COMPAT_DISABLED_V1
3559:     // Sprint 3 disables new Cash Ledger writes by default, but cash movement
3560:     // must still be written to Account Ledger as the primary wallet ledger.
3561:     const cashResult = writeCashLedgerCompatibility_(ss, parsed, rawText, common);
3562:     const ledgerResult = writeAccountLedgerMirror_(ss, parsed, rawText, common, AIRO_CONFIG.tabs.cash);
3563: 
3564:     if (ledgerResult && ledgerResult.status === 'written') {
3565:       // AIRO_SPRINT4_CASH_ROUTE_FINANCE_EVENT_EMISSION_V1
```

#### term_Cash L3552-3566

```javascript
3552:   var transfer = detectInternalTransfer_(parsed, rawText);
3553:   if (transfer) {
3554:     return writeInternalTransferToAccountLedger_(ss, parsed, rawText, common, transfer);
3555:   }
3556: 
3557:   if (key.includes('cash ledger')) {
3558:     // AIRO_SPRINT3_CASH_MIRROR_WHEN_COMPAT_DISABLED_V1
3559:     // Sprint 3 disables new Cash Ledger writes by default, but cash movement
3560:     // must still be written to Account Ledger as the primary wallet ledger.
3561:     const cashResult = writeCashLedgerCompatibility_(ss, parsed, rawText, common);
3562:     const ledgerResult = writeAccountLedgerMirror_(ss, parsed, rawText, common, AIRO_CONFIG.tabs.cash);
3563: 
3564:     if (ledgerResult && ledgerResult.status === 'written') {
3565:       // AIRO_SPRINT4_CASH_ROUTE_FINANCE_EVENT_EMISSION_V1
3566:       // Cash route returns before the generic appendByHeader_ path, so it must
```

#### term_Cash L3553-3567

```javascript
3553:   if (transfer) {
3554:     return writeInternalTransferToAccountLedger_(ss, parsed, rawText, common, transfer);
3555:   }
3556: 
3557:   if (key.includes('cash ledger')) {
3558:     // AIRO_SPRINT3_CASH_MIRROR_WHEN_COMPAT_DISABLED_V1
3559:     // Sprint 3 disables new Cash Ledger writes by default, but cash movement
3560:     // must still be written to Account Ledger as the primary wallet ledger.
3561:     const cashResult = writeCashLedgerCompatibility_(ss, parsed, rawText, common);
3562:     const ledgerResult = writeAccountLedgerMirror_(ss, parsed, rawText, common, AIRO_CONFIG.tabs.cash);
3563: 
3564:     if (ledgerResult && ledgerResult.status === 'written') {
3565:       // AIRO_SPRINT4_CASH_ROUTE_FINANCE_EVENT_EMISSION_V1
3566:       // Cash route returns before the generic appendByHeader_ path, so it must
3567:       // emit Finance Events here after the Account Ledger source-of-truth write.
```

#### term_Account_Ledger L3554-3568

```javascript
3554:     return writeInternalTransferToAccountLedger_(ss, parsed, rawText, common, transfer);
3555:   }
3556: 
3557:   if (key.includes('cash ledger')) {
3558:     // AIRO_SPRINT3_CASH_MIRROR_WHEN_COMPAT_DISABLED_V1
3559:     // Sprint 3 disables new Cash Ledger writes by default, but cash movement
3560:     // must still be written to Account Ledger as the primary wallet ledger.
3561:     const cashResult = writeCashLedgerCompatibility_(ss, parsed, rawText, common);
3562:     const ledgerResult = writeAccountLedgerMirror_(ss, parsed, rawText, common, AIRO_CONFIG.tabs.cash);
3563: 
3564:     if (ledgerResult && ledgerResult.status === 'written') {
3565:       // AIRO_SPRINT4_CASH_ROUTE_FINANCE_EVENT_EMISSION_V1
3566:       // Cash route returns before the generic appendByHeader_ path, so it must
3567:       // emit Finance Events here after the Account Ledger source-of-truth write.
3568:       const finalResult = {
```

#### term_Cash L3555-3569

```javascript
3555:   }
3556: 
3557:   if (key.includes('cash ledger')) {
3558:     // AIRO_SPRINT3_CASH_MIRROR_WHEN_COMPAT_DISABLED_V1
3559:     // Sprint 3 disables new Cash Ledger writes by default, but cash movement
3560:     // must still be written to Account Ledger as the primary wallet ledger.
3561:     const cashResult = writeCashLedgerCompatibility_(ss, parsed, rawText, common);
3562:     const ledgerResult = writeAccountLedgerMirror_(ss, parsed, rawText, common, AIRO_CONFIG.tabs.cash);
3563: 
3564:     if (ledgerResult && ledgerResult.status === 'written') {
3565:       // AIRO_SPRINT4_CASH_ROUTE_FINANCE_EVENT_EMISSION_V1
3566:       // Cash route returns before the generic appendByHeader_ path, so it must
3567:       // emit Finance Events here after the Account Ledger source-of-truth write.
3568:       const finalResult = {
3569:         ...ledgerResult,
```

#### term_Cash L3556-3570

```javascript
3556: 
3557:   if (key.includes('cash ledger')) {
3558:     // AIRO_SPRINT3_CASH_MIRROR_WHEN_COMPAT_DISABLED_V1
3559:     // Sprint 3 disables new Cash Ledger writes by default, but cash movement
3560:     // must still be written to Account Ledger as the primary wallet ledger.
3561:     const cashResult = writeCashLedgerCompatibility_(ss, parsed, rawText, common);
3562:     const ledgerResult = writeAccountLedgerMirror_(ss, parsed, rawText, common, AIRO_CONFIG.tabs.cash);
3563: 
3564:     if (ledgerResult && ledgerResult.status === 'written') {
3565:       // AIRO_SPRINT4_CASH_ROUTE_FINANCE_EVENT_EMISSION_V1
3566:       // Cash route returns before the generic appendByHeader_ path, so it must
3567:       // emit Finance Events here after the Account Ledger source-of-truth write.
3568:       const finalResult = {
3569:         ...ledgerResult,
3570:         writtenTab: AIRO_CONFIG.tabs.accountLedger,
```

#### term_Cash L3559-3573

```javascript
3559:     // Sprint 3 disables new Cash Ledger writes by default, but cash movement
3560:     // must still be written to Account Ledger as the primary wallet ledger.
3561:     const cashResult = writeCashLedgerCompatibility_(ss, parsed, rawText, common);
3562:     const ledgerResult = writeAccountLedgerMirror_(ss, parsed, rawText, common, AIRO_CONFIG.tabs.cash);
3563: 
3564:     if (ledgerResult && ledgerResult.status === 'written') {
3565:       // AIRO_SPRINT4_CASH_ROUTE_FINANCE_EVENT_EMISSION_V1
3566:       // Cash route returns before the generic appendByHeader_ path, so it must
3567:       // emit Finance Events here after the Account Ledger source-of-truth write.
3568:       const finalResult = {
3569:         ...ledgerResult,
3570:         writtenTab: AIRO_CONFIG.tabs.accountLedger,
3571:         cashLedgerCompatibilityStatus: cashResult && cashResult.status ? cashResult.status : '',
3572:         cashLedgerCompatibilityReason: cashResult && cashResult.reason ? cashResult.reason : ''
3573:       };
```

### getAccountLedgerRowDetails_ L1163-1186

#### function_start L1163-1186

```javascript
1163: function getAccountLedgerRowDetails_(ss, row) {
1164:   try {
1165:     var sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.accountLedger);
1166:     if (sheet && row) {
1167:       SpreadsheetApp.flush();
1168:       // Column C: Account (3rd column)
1169:       // Column D: Amount In (4th column)
1170:       // Column E: Amount Out (5th column)
1171:       // Column F: Balance (6th column)
1172:       var values = sheet.getRange(row, 3, 1, 4).getValues()[0];
1173:       return {
1174:         account: values[0],
1175:         amountIn: values[1],
1176:         amountOut: values[2],
1177:         balance: values[3]
1178:       };
1179:     }
1180:   } catch (e) {
1181:     if (typeof Logger !== 'undefined') {
1182:       Logger.log('getAccountLedgerRowDetails_ error: ' + e.message);
1183:     }
1184:   }
1185:   return null;
1186: }
```

#### function_end L1163-1186

```javascript
1163: function getAccountLedgerRowDetails_(ss, row) {
1164:   try {
1165:     var sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.accountLedger);
1166:     if (sheet && row) {
1167:       SpreadsheetApp.flush();
1168:       // Column C: Account (3rd column)
1169:       // Column D: Amount In (4th column)
1170:       // Column E: Amount Out (5th column)
1171:       // Column F: Balance (6th column)
1172:       var values = sheet.getRange(row, 3, 1, 4).getValues()[0];
1173:       return {
1174:         account: values[0],
1175:         amountIn: values[1],
1176:         amountOut: values[2],
1177:         balance: values[3]
1178:       };
1179:     }
1180:   } catch (e) {
1181:     if (typeof Logger !== 'undefined') {
1182:       Logger.log('getAccountLedgerRowDetails_ error: ' + e.message);
1183:     }
1184:   }
1185:   return null;
1186: }
```

#### term_balance L1165-1179

```javascript
1165:     var sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.accountLedger);
1166:     if (sheet && row) {
1167:       SpreadsheetApp.flush();
1168:       // Column C: Account (3rd column)
1169:       // Column D: Amount In (4th column)
1170:       // Column E: Amount Out (5th column)
1171:       // Column F: Balance (6th column)
1172:       var values = sheet.getRange(row, 3, 1, 4).getValues()[0];
1173:       return {
1174:         account: values[0],
1175:         amountIn: values[1],
1176:         amountOut: values[2],
1177:         balance: values[3]
1178:       };
1179:     }
```

#### term_balance L1171-1185

```javascript
1171:       // Column F: Balance (6th column)
1172:       var values = sheet.getRange(row, 3, 1, 4).getValues()[0];
1173:       return {
1174:         account: values[0],
1175:         amountIn: values[1],
1176:         amountOut: values[2],
1177:         balance: values[3]
1178:       };
1179:     }
1180:   } catch (e) {
1181:     if (typeof Logger !== 'undefined') {
1182:       Logger.log('getAccountLedgerRowDetails_ error: ' + e.message);
1183:     }
1184:   }
1185:   return null;
```

### airoBuildFinanceWriteSuccessReply_ L1188-1318

#### function_start L1188-1228

```javascript
1188: function airoBuildFinanceWriteSuccessReply_(ss, plannedTab, finalTab, parsed, routedResult, tabLink) {
1189:   var spreadsheet = ss;
1190:   var pTab = plannedTab;
1191:   var fTab = finalTab;
1192:   var prs = parsed;
1193:   var rResult = routedResult;
1194:   var tLink = tabLink;
1195: 
1196:   // Handle signature compatibility: if the first argument is a string (plannedTab), shift arguments.
1197:   if (typeof ss === 'string') {
1198:     spreadsheet = null;
1199:     pTab = ss;
1200:     fTab = plannedTab;
1201:     prs = finalTab;
1202:     rResult = parsed;
1203:     tLink = routedResult;
1204:   }
1205: 
1206:   prs = prs || {};
1207:   rResult = rResult || {};
1208: 
1209:   var writtenTab = rResult.writtenTab || fTab || '';
1210:   var amount = prs.amount || '';
1211:   var category = prs.category || 'Lainnya';
1212: 
1213:   // Check if we wrote to the Account Ledger (and spreadsheet is available)
1214:   var isLedgerWrite = false;
1215:   var ledgerRow = null;
1216: 
1217:   if (spreadsheet) {
1218:     if (rResult.transferInternal === true) {
1219:       isLedgerWrite = true;
1220:     } else if (canonicalSheetName_(writtenTab) === canonicalSheetName_(AIRO_CONFIG.tabs.accountLedger)) {
1221:       isLedgerWrite = true;
1222:       ledgerRow = rResult.row;
1223:     } else if (rResult.account_ledger_result && rResult.account_ledger_result.status === 'written') {
1224:       isLedgerWrite = true;
1225:       ledgerRow = rResult.account_ledger_result.row;
1226:     }
1227:   }
1228: 
```

#### function_end L1278-1318

```javascript
1278: 
1279:       var directionText = isOutflow ? 'keluar' : 'masuk';
1280: 
1281:       if (details && details.balance !== '' && details.balance !== null && details.balance !== undefined) {
1282:         return '✅ Transaksi dicatat.\n\n' +
1283:           account + ' ' + directionText + ' ' + formattedAmt + '\n' +
1284:           'Kategori: ' + category + '\n\n' +
1285:           'Saldo ' + account + ' sekarang: ' + formatBalanceRupiah_(details.balance);
1286:       } else {
1287:         return '✅ Transaksi dicatat.\n\n' +
1288:           account + ' ' + directionText + ' ' + formattedAmt + '\n' +
1289:           'Saldo terbaru belum bisa dibaca otomatis. Cek Account Ledger untuk verifikasi.';
1290:       }
1291:     }
1292:   }
1293: 
1294:   // Domain-only / fallback
1295:   if (rResult.section === 'gold') {
1296:     var acquisitionCost = rResult.acquisitionCost || prs.amount || prs.goldPurchasePrice || 0;
1297:     var marketValue = rResult.marketValue || 0;
1298: 
1299:     if (acquisitionCost && marketValue && acquisitionCost !== marketValue) {
1300:       return '✅ Tercatat ke Google Sheet.\n\n' +
1301:         'Rencana tab: ' + pTab + '\n' +
1302:         'Ditulis ke: ' + writtenTab + '\n' +
1303:         'Akun: ' + prs.account + '\n' +
1304:         'Kategori: ' + category + '\n' +
1305:         'Biaya beli / cash outflow: ' + airoSprint7FFormatRupiah_(acquisitionCost) + '\n' +
1306:         'Estimasi nilai aset / market value: ' + airoSprint7FFormatRupiah_(marketValue) + '\n\n' +
1307:         '🔗 Buka tab: ' + tLink;
1308:     }
1309:   }
1310: 
1311:   return '✅ Tercatat ke Google Sheet.\n\n' +
1312:     'Rencana tab: ' + pTab + '\n' +
1313:     'Ditulis ke: ' + writtenTab + '\n' +
1314:     'Akun: ' + prs.account + '\n' +
1315:     'Kategori: ' + category + '\n' +
1316:     'Nominal: Rp' + amount + '\n\n' +
1317:     '🔗 Buka tab: ' + tLink;
1318: }
```

#### term_category L1205-1219

```javascript
1205: 
1206:   prs = prs || {};
1207:   rResult = rResult || {};
1208: 
1209:   var writtenTab = rResult.writtenTab || fTab || '';
1210:   var amount = prs.amount || '';
1211:   var category = prs.category || 'Lainnya';
1212: 
1213:   // Check if we wrote to the Account Ledger (and spreadsheet is available)
1214:   var isLedgerWrite = false;
1215:   var ledgerRow = null;
1216: 
1217:   if (spreadsheet) {
1218:     if (rResult.transferInternal === true) {
1219:       isLedgerWrite = true;
```

#### term_Account_Ledger L1207-1221

```javascript
1207:   rResult = rResult || {};
1208: 
1209:   var writtenTab = rResult.writtenTab || fTab || '';
1210:   var amount = prs.amount || '';
1211:   var category = prs.category || 'Lainnya';
1212: 
1213:   // Check if we wrote to the Account Ledger (and spreadsheet is available)
1214:   var isLedgerWrite = false;
1215:   var ledgerRow = null;
1216: 
1217:   if (spreadsheet) {
1218:     if (rResult.transferInternal === true) {
1219:       isLedgerWrite = true;
1220:     } else if (canonicalSheetName_(writtenTab) === canonicalSheetName_(AIRO_CONFIG.tabs.accountLedger)) {
1221:       isLedgerWrite = true;
```

#### term_balance L1233-1247

```javascript
1233:       var sourceRow = rResult.accountLedgerRows ? rResult.accountLedgerRows[0] : null;
1234:       var targetRow = rResult.accountLedgerRows ? rResult.accountLedgerRows[1] : null;
1235: 
1236:       var sourceDetails = getAccountLedgerRowDetails_(spreadsheet, sourceRow);
1237:       var targetDetails = getAccountLedgerRowDetails_(spreadsheet, targetRow);
1238: 
1239:       var formattedAmt = formatBalanceRupiah_(amount);
1240:       if (formattedAmt === 'Unknown' || !amount) {
1241:         formattedAmt = 'Rp' + amount;
1242:       }
1243: 
1244:       if (sourceDetails && targetDetails &&
1245:           sourceDetails.balance !== '' && sourceDetails.balance !== null && sourceDetails.balance !== undefined &&
1246:           targetDetails.balance !== '' && targetDetails.balance !== null && targetDetails.balance !== undefined) {
1247: 
```

#### term_balance L1239-1253

```javascript
1239:       var formattedAmt = formatBalanceRupiah_(amount);
1240:       if (formattedAmt === 'Unknown' || !amount) {
1241:         formattedAmt = 'Rp' + amount;
1242:       }
1243: 
1244:       if (sourceDetails && targetDetails &&
1245:           sourceDetails.balance !== '' && sourceDetails.balance !== null && sourceDetails.balance !== undefined &&
1246:           targetDetails.balance !== '' && targetDetails.balance !== null && targetDetails.balance !== undefined) {
1247: 
1248:         return '✅ Transfer dicatat.\n\n' +
1249:           source + ' → ' + target + ': ' + formattedAmt + '\n\n' +
1250:           'Saldo ' + source + ' sekarang: ' + formatBalanceRupiah_(sourceDetails.balance) + '\n' +
1251:           'Saldo ' + target + ' sekarang: ' + formatBalanceRupiah_(targetDetails.balance);
1252:       } else {
1253:         return '✅ Transfer dicatat.\n\n' +
```

#### term_balance L1240-1254

```javascript
1240:       if (formattedAmt === 'Unknown' || !amount) {
1241:         formattedAmt = 'Rp' + amount;
1242:       }
1243: 
1244:       if (sourceDetails && targetDetails &&
1245:           sourceDetails.balance !== '' && sourceDetails.balance !== null && sourceDetails.balance !== undefined &&
1246:           targetDetails.balance !== '' && targetDetails.balance !== null && targetDetails.balance !== undefined) {
1247: 
1248:         return '✅ Transfer dicatat.\n\n' +
1249:           source + ' → ' + target + ': ' + formattedAmt + '\n\n' +
1250:           'Saldo ' + source + ' sekarang: ' + formatBalanceRupiah_(sourceDetails.balance) + '\n' +
1251:           'Saldo ' + target + ' sekarang: ' + formatBalanceRupiah_(targetDetails.balance);
1252:       } else {
1253:         return '✅ Transfer dicatat.\n\n' +
1254:           source + ' → ' + target + ': ' + formattedAmt + '\n' +
```

#### term_balance L1244-1258

```javascript
1244:       if (sourceDetails && targetDetails &&
1245:           sourceDetails.balance !== '' && sourceDetails.balance !== null && sourceDetails.balance !== undefined &&
1246:           targetDetails.balance !== '' && targetDetails.balance !== null && targetDetails.balance !== undefined) {
1247: 
1248:         return '✅ Transfer dicatat.\n\n' +
1249:           source + ' → ' + target + ': ' + formattedAmt + '\n\n' +
1250:           'Saldo ' + source + ' sekarang: ' + formatBalanceRupiah_(sourceDetails.balance) + '\n' +
1251:           'Saldo ' + target + ' sekarang: ' + formatBalanceRupiah_(targetDetails.balance);
1252:       } else {
1253:         return '✅ Transfer dicatat.\n\n' +
1254:           source + ' → ' + target + ': ' + formattedAmt + '\n' +
1255:           'Saldo terbaru belum bisa dibaca otomatis. Cek Account Ledger untuk verifikasi.';
1256:       }
1257:     } else {
1258:       // Single Transaction
```

#### term_balance L1245-1259

```javascript
1245:           sourceDetails.balance !== '' && sourceDetails.balance !== null && sourceDetails.balance !== undefined &&
1246:           targetDetails.balance !== '' && targetDetails.balance !== null && targetDetails.balance !== undefined) {
1247: 
1248:         return '✅ Transfer dicatat.\n\n' +
1249:           source + ' → ' + target + ': ' + formattedAmt + '\n\n' +
1250:           'Saldo ' + source + ' sekarang: ' + formatBalanceRupiah_(sourceDetails.balance) + '\n' +
1251:           'Saldo ' + target + ' sekarang: ' + formatBalanceRupiah_(targetDetails.balance);
1252:       } else {
1253:         return '✅ Transfer dicatat.\n\n' +
1254:           source + ' → ' + target + ': ' + formattedAmt + '\n' +
1255:           'Saldo terbaru belum bisa dibaca otomatis. Cek Account Ledger untuk verifikasi.';
1256:       }
1257:     } else {
1258:       // Single Transaction
1259:       var rowToRead = ledgerRow;
```

#### term_Saldo L1249-1263

```javascript
1249:           source + ' → ' + target + ': ' + formattedAmt + '\n\n' +
1250:           'Saldo ' + source + ' sekarang: ' + formatBalanceRupiah_(sourceDetails.balance) + '\n' +
1251:           'Saldo ' + target + ' sekarang: ' + formatBalanceRupiah_(targetDetails.balance);
1252:       } else {
1253:         return '✅ Transfer dicatat.\n\n' +
1254:           source + ' → ' + target + ': ' + formattedAmt + '\n' +
1255:           'Saldo terbaru belum bisa dibaca otomatis. Cek Account Ledger untuk verifikasi.';
1256:       }
1257:     } else {
1258:       // Single Transaction
1259:       var rowToRead = ledgerRow;
1260:       var details = getAccountLedgerRowDetails_(spreadsheet, rowToRead);
1261:       var account = prs.account || 'Unknown';
1262:       var isOutflow = true; // default
1263:       var formattedAmt = formatBalanceRupiah_(amount);
```

## Next

Use this extract to generate Gate C.1 source patch only. Do not deploy in Gate C.1.