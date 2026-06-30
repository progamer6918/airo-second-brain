---
title: AIRO Arfin Gate C1A Patch Point Finder 2026-06-30
status: PASS_GATE_C1A_PATCH_POINTS_READY
source_sha256: add9d5a538e48ed8cde6049f0632cbb8318c28e7074428ccc00dae7985353b19
head: d5c22659622f8c53f200082073bfadc52c58cdc7
generated_at_commit_time: 2026-06-30T23:04:22
---

> Gate C1A read-only exact patch-point finder evidence. No source patch, deploy, API call, Gmail read, Telegram send, or workbook edit.

# AIRO Arfin Gate C1A Patch Point Finder

Generated: `2026-06-30T23:02:47`

## Verdict

```text
RESULT=PASS_GATE_C1A_PATCH_POINTS_READY
EMAIL_FALLBACK_CALLS_COUNT=9
APPROVAL_WRITE_ROUTED_COUNT=1
APPROVAL_COMMAND_APPROVE_CALL_COUNT=2
FALLBACK_DIRECT_APPROVAL_SIGNAL_COUNT=6
BLOCKERS=NONE
NO_SOURCE_PATCH=YES
NO_DEPLOY=YES
NO_GMAIL_READ=YES
NO_TELEGRAM_SEND=YES
NO_WORKBOOK_EDIT=YES
```

## Patch Points

### email_fallback_calls

- L22978 `fallback_call`: `return airoSprint7HResolveToReviewQueueFallback_(parsed, pending, "Other / Review", "Transfer");`
- L22981 `fallback_call`: `return airoSprint7HResolveToReviewQueueFallback_(parsed, pending, "Other / Review", "Abaikan");`
- L23033 `fallback_call`: `return airoSprint7HResolveToReviewQueueFallback_(parsed, pending, selectedCat, "Lainnya");`
- L23052 `fallback_call`: `return airoSprint7HResolveToReviewQueueFallback_(parsed, pending, "Other / Review", "Lainnya");`
- L23090 `fallback_call`: `return airoSprint7HResolveToReviewQueueFallback_(parsed, pending, matchedCat, "Lainnya");`
- L23093 `fallback_call`: `return airoSprint7HResolveToReviewQueueFallback_(parsed, pending, "Other / Review", "Lainnya");`
- L23118 `fallback_call`: `return airoSprint7HResolveToReviewQueueFallback_(parsed, pending, pending.selected_category, parsedOption.subcategory);`
- L23120 `fallback_call`: `return airoSprint7HResolveToReviewQueueFallback_(parsed, pending, pending.selected_category, "Lainnya");`
- L23147 `fallback_call`: `return airoSprint7HResolveToReviewQueueFallback_(parsed, pending, "Other / Review", "Lainnya");`

### approval_write_routed

- L24354 `write_routed`: `var result = writeRouted_(ss, plannedTab, parsedObj, item.raw_text, stagingResult);`

### approval_command_approve_calls

- L24464 `approve_call`: `replyText = airoSprint7HApprovalApprove_(`
- L24523 `approve_call`: `replyText = airoSprint7HApprovalApprove_(`

### fallback_direct_approval

- L23415 `direct_approval`: `"Status: pending approval.\n" +`
- L23416 `direct_approval`: `"Balas /approval untuk langsung menyetujui transaksi ini.\n" +`
- L23420 `direct_approval`: `airoTask614StoreDirectApproval_(`
- L23494 `direct_approval`: `"Status: pending approval.\n" +`
- L23495 `direct_approval`: `"Balas /approval untuk langsung menyetujui transaksi ini.\n" +`
- L23499 `direct_approval`: `airoTask614StoreDirectApproval_(`

### insert_helpers_after

- After `airoSprint7HResolveToReviewQueueFallback_` line `23526` — email funding-source helpers near Sprint7F/7H
- After `writeInternalTransferToAccountLedger_` line `14604` — funding transfer writer wrapper
- After `airoBuildFinanceWriteSuccessReply_` line `1318` — balance/readback helper

## Exact Snippets

### email_answer

#### send_telegram L22842

```javascript
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
```

#### return_json L22843

```javascript
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
```

#### question_type L22868

```javascript
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
22874:       return json_({
22875:         ok: false,
22876:         status: "AIRO_ERROR_UNKNOWN_QUESTION_TYPE",
22877:         handled: true,
22878:         finance_write_performed: false,
22879:         review_queue_write_performed: false
22880:       });
```

#### question_type L22869

```javascript
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
22874:       return json_({
22875:         ok: false,
22876:         status: "AIRO_ERROR_UNKNOWN_QUESTION_TYPE",
22877:         handled: true,
22878:         finance_write_performed: false,
22879:         review_queue_write_performed: false
22880:       });
22881:     }
```

#### question_type L22870

```javascript
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
22874:       return json_({
22875:         ok: false,
22876:         status: "AIRO_ERROR_UNKNOWN_QUESTION_TYPE",
22877:         handled: true,
22878:         finance_write_performed: false,
22879:         review_queue_write_performed: false
22880:       });
22881:     }
22882: 
```

#### question_type L22872

```javascript
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
22874:       return json_({
22875:         ok: false,
22876:         status: "AIRO_ERROR_UNKNOWN_QUESTION_TYPE",
22877:         handled: true,
22878:         finance_write_performed: false,
22879:         review_queue_write_performed: false
22880:       });
22881:     }
22882: 
22883:     var answer = textRaw.toUpperCase();
22884:     if (questionType === "direction") {
```

#### send_telegram L22873

```javascript
22865:   var state = String(pending.clarification_state || "category_pending").toLowerCase();
22866: 
22867:   if (state === "category_pending") {
22868:     var questionType = airoSprint7FInferQuestionTypeFromPending_(pending);
22869:     pending.clarification_question_type = questionType;
22870:     pending.question_type = questionType;
22871: 
22872:     if (questionType !== "category_expense" && questionType !== "category_income" && questionType !== "direction") {
22873:       sendTelegram_(parsed.chat_id, "⚠️ Tipe pertanyaan tidak dikenal. Gagal melanjutkan klarifikasi.");
22874:       return json_({
22875:         ok: false,
22876:         status: "AIRO_ERROR_UNKNOWN_QUESTION_TYPE",
22877:         handled: true,
22878:         finance_write_performed: false,
22879:         review_queue_write_performed: false
22880:       });
22881:     }
22882: 
22883:     var answer = textRaw.toUpperCase();
22884:     if (questionType === "direction") {
22885:       if (!/^[A-D]$/.test(answer)) {
```

#### return_json L22874

```javascript
22866: 
22867:   if (state === "category_pending") {
22868:     var questionType = airoSprint7FInferQuestionTypeFromPending_(pending);
22869:     pending.clarification_question_type = questionType;
22870:     pending.question_type = questionType;
22871: 
22872:     if (questionType !== "category_expense" && questionType !== "category_income" && questionType !== "direction") {
22873:       sendTelegram_(parsed.chat_id, "⚠️ Tipe pertanyaan tidak dikenal. Gagal melanjutkan klarifikasi.");
22874:       return json_({
22875:         ok: false,
22876:         status: "AIRO_ERROR_UNKNOWN_QUESTION_TYPE",
22877:         handled: true,
22878:         finance_write_performed: false,
22879:         review_queue_write_performed: false
22880:       });
22881:     }
22882: 
22883:     var answer = textRaw.toUpperCase();
22884:     if (questionType === "direction") {
22885:       if (!/^[A-D]$/.test(answer)) {
22886:         return null;
```

#### question_type L22884

```javascript
22876:         status: "AIRO_ERROR_UNKNOWN_QUESTION_TYPE",
22877:         handled: true,
22878:         finance_write_performed: false,
22879:         review_queue_write_performed: false
22880:       });
22881:     }
22882: 
22883:     var answer = textRaw.toUpperCase();
22884:     if (questionType === "direction") {
22885:       if (!/^[A-D]$/.test(answer)) {
22886:         return null;
22887:       }
22888:     } else {
22889:       if (!/^[A-E]$/.test(answer)) {
22890:         return null;
22891:       }
22892:     }
22893: 
22894:     var key = pending._property_key || ("AIRO_SPRINT7F_PENDING_EMAIL_" + String(parsed.chat_id));
22895: 
22896:     if (answer === "E") {
```

#### upsert_call L22898

```javascript
22890:         return null;
22891:       }
22892:     }
22893: 
22894:     var key = pending._property_key || ("AIRO_SPRINT7F_PENDING_EMAIL_" + String(parsed.chat_id));
22895: 
22896:     if (answer === "E") {
22897:       pending.clarification_state = "category_search_pending";
22898:       airoSprint7FUpsertPendingEmailCandidate_(parsed.chat_id, pending);
22899: 
22900:       var registry = airoSprint7CategoryContractGetRegistry_();
22901:       var categories = Object.keys(registry);
22902:       var allowed = [];
22903:       for (var c = 0; c < categories.length; c++) {
22904:         if (categories[c] !== "Other / Review") {
22905:           allowed.push(categories[c]);
22906:         }
22907:       }
22908: 
22909:       var listLines = ["Pilih kategori:"];
22910:       for (var i = 0; i < allowed.length; i++) {
```

#### send_telegram L22916

```javascript
22908: 
22909:       var listLines = ["Pilih kategori:"];
22910:       for (var i = 0; i < allowed.length; i++) {
22911:         listLines.push((i + 1) + ". " + allowed[i]);
22912:       }
22913:       listLines.push("0. Other / Review");
22914: 
22915:       var searchPrompt = listLines.join("\n");
22916:       sendTelegram_(parsed.chat_id, searchPrompt);
22917: 
22918:       return json_({
22919:         ok: true,
22920:         sprint: "7H",
22921:         status: "sprint7h_email_category_search_pending",
22922:         handled: true,
22923:         waiting: true,
22924:         finance_write_performed: false,
22925:         account_ledger_write_performed: false,
22926:         finance_events_write_performed: false,
22927:         review_queue_write_performed: false,
22928:         domain_tab_write_performed: false
```

#### return_json L22918

```javascript
22910:       for (var i = 0; i < allowed.length; i++) {
22911:         listLines.push((i + 1) + ". " + allowed[i]);
22912:       }
22913:       listLines.push("0. Other / Review");
22914: 
22915:       var searchPrompt = listLines.join("\n");
22916:       sendTelegram_(parsed.chat_id, searchPrompt);
22917: 
22918:       return json_({
22919:         ok: true,
22920:         sprint: "7H",
22921:         status: "sprint7h_email_category_search_pending",
22922:         handled: true,
22923:         waiting: true,
22924:         finance_write_performed: false,
22925:         account_ledger_write_performed: false,
22926:         finance_events_write_performed: false,
22927:         review_queue_write_performed: false,
22928:         domain_tab_write_performed: false
22929:       });
22930:     }
```

#### question_type L22932

```javascript
22924:         finance_write_performed: false,
22925:         account_ledger_write_performed: false,
22926:         finance_events_write_performed: false,
22927:         review_queue_write_performed: false,
22928:         domain_tab_write_performed: false
22929:       });
22930:     }
22931: 
22932:     if (questionType === "direction") {
22933:       if (answer === "A") {
22934:         pending.inferred_direction = "pengeluaran";
22935:         pending.clarification_question_type = "category_expense";
22936:         pending.clarification_state = "category_pending";
22937:         airoSprint7FUpsertPendingEmailCandidate_(parsed.chat_id, pending);
22938: 
22939:         var promptMsg = airoSprint7FBuildFriendlyClarificationMessage_(pending.candidate_id || pending.message_id, pending);
22940:         sendTelegram_(parsed.chat_id, promptMsg);
22941: 
22942:         return json_({
22943:           ok: true,
22944:           sprint: "7H",
```

#### question_type L22935

```javascript
22927:         review_queue_write_performed: false,
22928:         domain_tab_write_performed: false
22929:       });
22930:     }
22931: 
22932:     if (questionType === "direction") {
22933:       if (answer === "A") {
22934:         pending.inferred_direction = "pengeluaran";
22935:         pending.clarification_question_type = "category_expense";
22936:         pending.clarification_state = "category_pending";
22937:         airoSprint7FUpsertPendingEmailCandidate_(parsed.chat_id, pending);
22938: 
22939:         var promptMsg = airoSprint7FBuildFriendlyClarificationMessage_(pending.candidate_id || pending.message_id, pending);
22940:         sendTelegram_(parsed.chat_id, promptMsg);
22941: 
22942:         return json_({
22943:           ok: true,
22944:           sprint: "7H",
22945:           status: "sprint7h_email_direction_pengeluaran_selected",
22946:           handled: true,
22947:           waiting: true,
```

#### upsert_call L22937

```javascript
22929:       });
22930:     }
22931: 
22932:     if (questionType === "direction") {
22933:       if (answer === "A") {
22934:         pending.inferred_direction = "pengeluaran";
22935:         pending.clarification_question_type = "category_expense";
22936:         pending.clarification_state = "category_pending";
22937:         airoSprint7FUpsertPendingEmailCandidate_(parsed.chat_id, pending);
22938: 
22939:         var promptMsg = airoSprint7FBuildFriendlyClarificationMessage_(pending.candidate_id || pending.message_id, pending);
22940:         sendTelegram_(parsed.chat_id, promptMsg);
22941: 
22942:         return json_({
22943:           ok: true,
22944:           sprint: "7H",
22945:           status: "sprint7h_email_direction_pengeluaran_selected",
22946:           handled: true,
22947:           waiting: true,
22948:           finance_write_performed: false,
22949:           account_ledger_write_performed: false,
```

#### send_telegram L22940

```javascript
22932:     if (questionType === "direction") {
22933:       if (answer === "A") {
22934:         pending.inferred_direction = "pengeluaran";
22935:         pending.clarification_question_type = "category_expense";
22936:         pending.clarification_state = "category_pending";
22937:         airoSprint7FUpsertPendingEmailCandidate_(parsed.chat_id, pending);
22938: 
22939:         var promptMsg = airoSprint7FBuildFriendlyClarificationMessage_(pending.candidate_id || pending.message_id, pending);
22940:         sendTelegram_(parsed.chat_id, promptMsg);
22941: 
22942:         return json_({
22943:           ok: true,
22944:           sprint: "7H",
22945:           status: "sprint7h_email_direction_pengeluaran_selected",
22946:           handled: true,
22947:           waiting: true,
22948:           finance_write_performed: false,
22949:           account_ledger_write_performed: false,
22950:           finance_events_write_performed: false,
22951:           review_queue_write_performed: false,
22952:           domain_tab_write_performed: false
```

#### return_json L22942

```javascript
22934:         pending.inferred_direction = "pengeluaran";
22935:         pending.clarification_question_type = "category_expense";
22936:         pending.clarification_state = "category_pending";
22937:         airoSprint7FUpsertPendingEmailCandidate_(parsed.chat_id, pending);
22938: 
22939:         var promptMsg = airoSprint7FBuildFriendlyClarificationMessage_(pending.candidate_id || pending.message_id, pending);
22940:         sendTelegram_(parsed.chat_id, promptMsg);
22941: 
22942:         return json_({
22943:           ok: true,
22944:           sprint: "7H",
22945:           status: "sprint7h_email_direction_pengeluaran_selected",
22946:           handled: true,
22947:           waiting: true,
22948:           finance_write_performed: false,
22949:           account_ledger_write_performed: false,
22950:           finance_events_write_performed: false,
22951:           review_queue_write_performed: false,
22952:           domain_tab_write_performed: false
22953:         });
22954:       }
```

#### question_type L22957

```javascript
22949:           account_ledger_write_performed: false,
22950:           finance_events_write_performed: false,
22951:           review_queue_write_performed: false,
22952:           domain_tab_write_performed: false
22953:         });
22954:       }
22955:       if (answer === "B") {
22956:         pending.inferred_direction = "pemasukan";
22957:         pending.clarification_question_type = "category_income";
22958:         pending.clarification_state = "category_pending";
22959:         airoSprint7FUpsertPendingEmailCandidate_(parsed.chat_id, pending);
22960: 
22961:         var promptMsg = airoSprint7FBuildFriendlyClarificationMessage_(pending.candidate_id || pending.message_id, pending);
22962:         sendTelegram_(parsed.chat_id, promptMsg);
22963: 
22964:         return json_({
22965:           ok: true,
22966:           sprint: "7H",
22967:           status: "sprint7h_email_direction_pemasukan_selected",
22968:           handled: true,
22969:           waiting: true,
```

#### upsert_call L22959

```javascript
22951:           review_queue_write_performed: false,
22952:           domain_tab_write_performed: false
22953:         });
22954:       }
22955:       if (answer === "B") {
22956:         pending.inferred_direction = "pemasukan";
22957:         pending.clarification_question_type = "category_income";
22958:         pending.clarification_state = "category_pending";
22959:         airoSprint7FUpsertPendingEmailCandidate_(parsed.chat_id, pending);
22960: 
22961:         var promptMsg = airoSprint7FBuildFriendlyClarificationMessage_(pending.candidate_id || pending.message_id, pending);
22962:         sendTelegram_(parsed.chat_id, promptMsg);
22963: 
22964:         return json_({
22965:           ok: true,
22966:           sprint: "7H",
22967:           status: "sprint7h_email_direction_pemasukan_selected",
22968:           handled: true,
22969:           waiting: true,
22970:           finance_write_performed: false,
22971:           account_ledger_write_performed: false,
```

#### send_telegram L22962

```javascript
22954:       }
22955:       if (answer === "B") {
22956:         pending.inferred_direction = "pemasukan";
22957:         pending.clarification_question_type = "category_income";
22958:         pending.clarification_state = "category_pending";
22959:         airoSprint7FUpsertPendingEmailCandidate_(parsed.chat_id, pending);
22960: 
22961:         var promptMsg = airoSprint7FBuildFriendlyClarificationMessage_(pending.candidate_id || pending.message_id, pending);
22962:         sendTelegram_(parsed.chat_id, promptMsg);
22963: 
22964:         return json_({
22965:           ok: true,
22966:           sprint: "7H",
22967:           status: "sprint7h_email_direction_pemasukan_selected",
22968:           handled: true,
22969:           waiting: true,
22970:           finance_write_performed: false,
22971:           account_ledger_write_performed: false,
22972:           finance_events_write_performed: false,
22973:           review_queue_write_performed: false,
22974:           domain_tab_write_performed: false
```

#### return_json L22964

```javascript
22956:         pending.inferred_direction = "pemasukan";
22957:         pending.clarification_question_type = "category_income";
22958:         pending.clarification_state = "category_pending";
22959:         airoSprint7FUpsertPendingEmailCandidate_(parsed.chat_id, pending);
22960: 
22961:         var promptMsg = airoSprint7FBuildFriendlyClarificationMessage_(pending.candidate_id || pending.message_id, pending);
22962:         sendTelegram_(parsed.chat_id, promptMsg);
22963: 
22964:         return json_({
22965:           ok: true,
22966:           sprint: "7H",
22967:           status: "sprint7h_email_direction_pemasukan_selected",
22968:           handled: true,
22969:           waiting: true,
22970:           finance_write_performed: false,
22971:           account_ledger_write_performed: false,
22972:           finance_events_write_performed: false,
22973:           review_queue_write_performed: false,
22974:           domain_tab_write_performed: false
22975:         });
22976:       }
```

#### fallback_call L22978

```javascript
22970:           finance_write_performed: false,
22971:           account_ledger_write_performed: false,
22972:           finance_events_write_performed: false,
22973:           review_queue_write_performed: false,
22974:           domain_tab_write_performed: false
22975:         });
22976:       }
22977:       if (answer === "C") {
22978:         return airoSprint7HResolveToReviewQueueFallback_(parsed, pending, "Other / Review", "Transfer");
22979:       }
22980:       if (answer === "D") {
22981:         return airoSprint7HResolveToReviewQueueFallback_(parsed, pending, "Other / Review", "Abaikan");
22982:       }
22983:     }
22984: 
22985:     var selectedCat = "";
22986:     if (questionType === "category_expense") {
22987:       var categoryMap = {
22988:         A: "Food & Drink",
22989:         B: "Transport",
22990:         C: "Groceries",
```

#### fallback_call L22981

```javascript
22973:           review_queue_write_performed: false,
22974:           domain_tab_write_performed: false
22975:         });
22976:       }
22977:       if (answer === "C") {
22978:         return airoSprint7HResolveToReviewQueueFallback_(parsed, pending, "Other / Review", "Transfer");
22979:       }
22980:       if (answer === "D") {
22981:         return airoSprint7HResolveToReviewQueueFallback_(parsed, pending, "Other / Review", "Abaikan");
22982:       }
22983:     }
22984: 
22985:     var selectedCat = "";
22986:     if (questionType === "category_expense") {
22987:       var categoryMap = {
22988:         A: "Food & Drink",
22989:         B: "Transport",
22990:         C: "Groceries",
22991:         D: "Utilities"
22992:       };
22993:       selectedCat = categoryMap[answer];
```

#### question_type L22986

```javascript
22978:         return airoSprint7HResolveToReviewQueueFallback_(parsed, pending, "Other / Review", "Transfer");
22979:       }
22980:       if (answer === "D") {
22981:         return airoSprint7HResolveToReviewQueueFallback_(parsed, pending, "Other / Review", "Abaikan");
22982:       }
22983:     }
22984: 
22985:     var selectedCat = "";
22986:     if (questionType === "category_expense") {
22987:       var categoryMap = {
22988:         A: "Food & Drink",
22989:         B: "Transport",
22990:         C: "Groceries",
22991:         D: "Utilities"
22992:       };
22993:       selectedCat = categoryMap[answer];
22994:     } else if (questionType === "category_income") {
22995:       var categoryMap = {
22996:         A: "Gaji / income",
22997:         B: "Refund",
22998:         C: "Transfer antar akun sendiri",
```

#### question_type L22994

```javascript
22986:     if (questionType === "category_expense") {
22987:       var categoryMap = {
22988:         A: "Food & Drink",
22989:         B: "Transport",
22990:         C: "Groceries",
22991:         D: "Utilities"
22992:       };
22993:       selectedCat = categoryMap[answer];
22994:     } else if (questionType === "category_income") {
22995:       var categoryMap = {
22996:         A: "Gaji / income",
22997:         B: "Refund",
22998:         C: "Transfer antar akun sendiri",
22999:         D: "Piutang dibayar"
23000:       };
23001:       selectedCat = categoryMap[answer];
23002:     }
23003: 
23004:     if (!selectedCat) {
23005:       return null;
23006:     }
```

#### selected_category L23013

```javascript
23005:       return null;
23006:     }
23007: 
23008:     var registry = airoSprint7CategoryContractGetRegistry_();
23009:     var catData = registry[selectedCat];
23010:     var subs = (catData && catData.subcategories) ? catData.subcategories : [];
23011: 
23012:     if (subs.length > 0) {
23013:       pending.selected_category = selectedCat;
23014:       pending.clarification_state = "subcategory_pending";
23015:       airoSprint7FUpsertPendingEmailCandidate_(parsed.chat_id, pending);
23016: 
23017:       var subPrompt = airoSprint7CategoryContractBuildSubcategoryPrompt_(selectedCat);
23018:       sendTelegram_(parsed.chat_id, subPrompt);
23019: 
23020:       return json_({
23021:         ok: true,
23022:         sprint: "7H",
23023:         status: "sprint7h_email_category_selected",
23024:         handled: true,
23025:         waiting: true,
```

#### selected_subcategory L23014

```javascript
23006:     }
23007: 
23008:     var registry = airoSprint7CategoryContractGetRegistry_();
23009:     var catData = registry[selectedCat];
23010:     var subs = (catData && catData.subcategories) ? catData.subcategories : [];
23011: 
23012:     if (subs.length > 0) {
23013:       pending.selected_category = selectedCat;
23014:       pending.clarification_state = "subcategory_pending";
23015:       airoSprint7FUpsertPendingEmailCandidate_(parsed.chat_id, pending);
23016: 
23017:       var subPrompt = airoSprint7CategoryContractBuildSubcategoryPrompt_(selectedCat);
23018:       sendTelegram_(parsed.chat_id, subPrompt);
23019: 
23020:       return json_({
23021:         ok: true,
23022:         sprint: "7H",
23023:         status: "sprint7h_email_category_selected",
23024:         handled: true,
23025:         waiting: true,
23026:         finance_write_performed: false,
```

#### upsert_call L23015

```javascript
23007: 
23008:     var registry = airoSprint7CategoryContractGetRegistry_();
23009:     var catData = registry[selectedCat];
23010:     var subs = (catData && catData.subcategories) ? catData.subcategories : [];
23011: 
23012:     if (subs.length > 0) {
23013:       pending.selected_category = selectedCat;
23014:       pending.clarification_state = "subcategory_pending";
23015:       airoSprint7FUpsertPendingEmailCandidate_(parsed.chat_id, pending);
23016: 
23017:       var subPrompt = airoSprint7CategoryContractBuildSubcategoryPrompt_(selectedCat);
23018:       sendTelegram_(parsed.chat_id, subPrompt);
23019: 
23020:       return json_({
23021:         ok: true,
23022:         sprint: "7H",
23023:         status: "sprint7h_email_category_selected",
23024:         handled: true,
23025:         waiting: true,
23026:         finance_write_performed: false,
23027:         account_ledger_write_performed: false,
```

#### send_telegram L23018

```javascript
23010:     var subs = (catData && catData.subcategories) ? catData.subcategories : [];
23011: 
23012:     if (subs.length > 0) {
23013:       pending.selected_category = selectedCat;
23014:       pending.clarification_state = "subcategory_pending";
23015:       airoSprint7FUpsertPendingEmailCandidate_(parsed.chat_id, pending);
23016: 
23017:       var subPrompt = airoSprint7CategoryContractBuildSubcategoryPrompt_(selectedCat);
23018:       sendTelegram_(parsed.chat_id, subPrompt);
23019: 
23020:       return json_({
23021:         ok: true,
23022:         sprint: "7H",
23023:         status: "sprint7h_email_category_selected",
23024:         handled: true,
23025:         waiting: true,
23026:         finance_write_performed: false,
23027:         account_ledger_write_performed: false,
23028:         finance_events_write_performed: false,
23029:         review_queue_write_performed: false,
23030:         domain_tab_write_performed: false
```

#### return_json L23020

```javascript
23012:     if (subs.length > 0) {
23013:       pending.selected_category = selectedCat;
23014:       pending.clarification_state = "subcategory_pending";
23015:       airoSprint7FUpsertPendingEmailCandidate_(parsed.chat_id, pending);
23016: 
23017:       var subPrompt = airoSprint7CategoryContractBuildSubcategoryPrompt_(selectedCat);
23018:       sendTelegram_(parsed.chat_id, subPrompt);
23019: 
23020:       return json_({
23021:         ok: true,
23022:         sprint: "7H",
23023:         status: "sprint7h_email_category_selected",
23024:         handled: true,
23025:         waiting: true,
23026:         finance_write_performed: false,
23027:         account_ledger_write_performed: false,
23028:         finance_events_write_performed: false,
23029:         review_queue_write_performed: false,
23030:         domain_tab_write_performed: false
23031:       });
23032:     } else {
```

### fallback

#### update_resolution L23267

```javascript
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
```

#### remove_pending L23269

```javascript
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
```

#### return_json L23282

```javascript
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
23290:       review_queue_write_performed: false,
23291:       domain_tab_write_performed: false,
23292:       telegram_send_performed: true,
23293:       email_modified: false,
23294:       trigger_created: false
```

#### notes_raw L23302

```javascript
23294:       trigger_created: false
23295:     });
23296:   }
23297: 
23298:   var rowData = {
23299:     queue_id: "review:emc:" + pending.message_id,
23300:     created_at: Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyy-MM-dd HH:mm:ss"),
23301:     source: "import",
23302:     raw_text: "Subject: " + pending.subject + " | Amount: Rp" + amount + " | Sender: " + pending.sender,
23303:     parsed_type: "expense",
23304:     parsed_category: category,
23305:     parsed_subcategory: subcategory,
23306:     parsed_amount: amount,
23307:     parsed_currency: "IDR",
23308:     parsed_account: account,
23309: 
23310:     // Task 3B: Email identity extension fields
23311:     email_candidate_id: pending.candidate_id || "",
23312:     gmail_message_id: pending.message_id || "",
23313:     gmail_thread_id: pending.thread_id || "",
23314:     email_provider: pending.provider || "",
```

#### review_queue L23324

```javascript
23316:     duplicate_key: "review:emc:" + pending.message_id,
23317:     write_policy: "staging",
23318:     write_status: "pending",
23319:     linked_event_id: "",
23320:     linked_account_ledger_entry_id: "",
23321: 
23322:     // Fallback fields for legacy compatibility
23323:     intent: "expense",
23324:     target_tab: "🧾 Review Queue",
23325:     reason: "email_candidate_resolved_ingestion",
23326:     amount: amount,
23327:     account: account,
23328:     category: category === "Other / Review" ? "Other / Review" : (category + " / " + subcategory),
23329:     status: "pending",
23330:     notes: "Sprint 7H scheduled poller resolved candidate. Category: " + category + ", Subcategory: " + subcategory,
23331:     parser: "email"
23332:   };
23333: 
23334:   // Dedupe check: scan review queue for existing duplicate_key matching review:emc:<message_id>
23335:   var keyToFind = "review:emc:" + pending.message_id;
23336:   var sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.review);
```

#### notes_raw L23330

```javascript
23322:     // Fallback fields for legacy compatibility
23323:     intent: "expense",
23324:     target_tab: "🧾 Review Queue",
23325:     reason: "email_candidate_resolved_ingestion",
23326:     amount: amount,
23327:     account: account,
23328:     category: category === "Other / Review" ? "Other / Review" : (category + " / " + subcategory),
23329:     status: "pending",
23330:     notes: "Sprint 7H scheduled poller resolved candidate. Category: " + category + ", Subcategory: " + subcategory,
23331:     parser: "email"
23332:   };
23333: 
23334:   // Dedupe check: scan review queue for existing duplicate_key matching review:emc:<message_id>
23335:   var keyToFind = "review:emc:" + pending.message_id;
23336:   var sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.review);
23337:   var duplicateFound = false;
23338:   var existingRowIndex = -1;
23339:   if (sheet && sheet.getLastRow() >= 2) {
23340:     var header = findHeader_(sheet);
23341:     if (header) {
23342:       var headerList = header.headers;
```

#### review_queue L23334

```javascript
23326:     amount: amount,
23327:     account: account,
23328:     category: category === "Other / Review" ? "Other / Review" : (category + " / " + subcategory),
23329:     status: "pending",
23330:     notes: "Sprint 7H scheduled poller resolved candidate. Category: " + category + ", Subcategory: " + subcategory,
23331:     parser: "email"
23332:   };
23333: 
23334:   // Dedupe check: scan review queue for existing duplicate_key matching review:emc:<message_id>
23335:   var keyToFind = "review:emc:" + pending.message_id;
23336:   var sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.review);
23337:   var duplicateFound = false;
23338:   var existingRowIndex = -1;
23339:   if (sheet && sheet.getLastRow() >= 2) {
23340:     var header = findHeader_(sheet);
23341:     if (header) {
23342:       var headerList = header.headers;
23343:       var dupKeyCol = -1;
23344:       for (var c = 0; c < headerList.length; c++) {
23345:         if (canonicalKey_(headerList[c]) === "duplicate_key") {
23346:           dupKeyCol = c;
```

#### append L23376

```javascript
23368:   var targetRow = 0;
23369: 
23370:   if (duplicateFound) {
23371:     // Correct/update the existing row in-place with the proper mapped values
23372:     if (sheet) {
23373:       var header = findHeader_(sheet);
23374:       if (header) {
23375:         var headerList = header.headers;
23376:         var rowValues = buildRowByHeader_(headerList, rowData);
23377:         sheet.getRange(existingRowIndex, 1, 1, rowValues.length).setValues([rowValues]);
23378:         targetRow = existingRowIndex;
23379: 
23380:         // Readback check for duplicate update
23381:         var readbackValues = sheet.getRange(existingRowIndex, 1, 1, sheet.getLastColumn()).getValues()[0];
23382:         var checkQueueIdCol = -1;
23383:         var checkAmountCol = -1;
23384:         var checkAccountCol = -1;
23385:         var checkStatusCol = -1;
23386:         for (var c = 0; c < headerList.length; c++) {
23387:           var canonicalCheck = canonicalKey_(headerList[c]);
23388:           var field = fieldForHeader_(headerList[c]);
```

#### review_queue L23411

```javascript
23403:           readAccount === account &&
23404:           readStatus === "pending"
23405:         ) {
23406:           readbackVerified = true;
23407:         }
23408:       }
23409:     }
23410: 
23411:     var replyText = "Resolusi transaksi email tersimpan ke Review Queue.\n\n" +
23412:                     "Nominal: " + airoSprint7FFormatRupiah_(amount) + "\n" +
23413:                     "Akun: " + account + "\n" +
23414:                     "Kategori: " + category + (category === "Other / Review" ? "" : (" / " + subcategory)) + "\n" +
23415:                     "Status: pending approval.\n" +
23416:                     "Balas /approval untuk langsung menyetujui transaksi ini.\n" +
23417:                     "Readback: " + (readbackVerified ? "PASS." : "Failed.");
23418: 
23419:     if (readbackVerified && targetRow > 0) {
23420:     airoTask614StoreDirectApproval_(
23421:       parsed.chat_id,
23422:       keyToFind,
23423:       targetRow
```

#### direct_approval L23415

```javascript
23407:         }
23408:       }
23409:     }
23410: 
23411:     var replyText = "Resolusi transaksi email tersimpan ke Review Queue.\n\n" +
23412:                     "Nominal: " + airoSprint7FFormatRupiah_(amount) + "\n" +
23413:                     "Akun: " + account + "\n" +
23414:                     "Kategori: " + category + (category === "Other / Review" ? "" : (" / " + subcategory)) + "\n" +
23415:                     "Status: pending approval.\n" +
23416:                     "Balas /approval untuk langsung menyetujui transaksi ini.\n" +
23417:                     "Readback: " + (readbackVerified ? "PASS." : "Failed.");
23418: 
23419:     if (readbackVerified && targetRow > 0) {
23420:     airoTask614StoreDirectApproval_(
23421:       parsed.chat_id,
23422:       keyToFind,
23423:       targetRow
23424:     );
23425:   }
23426: 
23427:   sendTelegram_(parsed.chat_id, replyText);
```

#### direct_approval L23416

```javascript
23408:       }
23409:     }
23410: 
23411:     var replyText = "Resolusi transaksi email tersimpan ke Review Queue.\n\n" +
23412:                     "Nominal: " + airoSprint7FFormatRupiah_(amount) + "\n" +
23413:                     "Akun: " + account + "\n" +
23414:                     "Kategori: " + category + (category === "Other / Review" ? "" : (" / " + subcategory)) + "\n" +
23415:                     "Status: pending approval.\n" +
23416:                     "Balas /approval untuk langsung menyetujui transaksi ini.\n" +
23417:                     "Readback: " + (readbackVerified ? "PASS." : "Failed.");
23418: 
23419:     if (readbackVerified && targetRow > 0) {
23420:     airoTask614StoreDirectApproval_(
23421:       parsed.chat_id,
23422:       keyToFind,
23423:       targetRow
23424:     );
23425:   }
23426: 
23427:   sendTelegram_(parsed.chat_id, replyText);
23428: 
```

#### direct_approval L23420

```javascript
23412:                     "Nominal: " + airoSprint7FFormatRupiah_(amount) + "\n" +
23413:                     "Akun: " + account + "\n" +
23414:                     "Kategori: " + category + (category === "Other / Review" ? "" : (" / " + subcategory)) + "\n" +
23415:                     "Status: pending approval.\n" +
23416:                     "Balas /approval untuk langsung menyetujui transaksi ini.\n" +
23417:                     "Readback: " + (readbackVerified ? "PASS." : "Failed.");
23418: 
23419:     if (readbackVerified && targetRow > 0) {
23420:     airoTask614StoreDirectApproval_(
23421:       parsed.chat_id,
23422:       keyToFind,
23423:       targetRow
23424:     );
23425:   }
23426: 
23427:   sendTelegram_(parsed.chat_id, replyText);
23428: 
23429:     return json_({
23430:       ok: true,
23431:       sprint: "7H",
23432:       mode: "scheduled_polling_resolution",
```

#### return_json L23429

```javascript
23421:       parsed.chat_id,
23422:       keyToFind,
23423:       targetRow
23424:     );
23425:   }
23426: 
23427:   sendTelegram_(parsed.chat_id, replyText);
23428: 
23429:     return json_({
23430:       ok: true,
23431:       sprint: "7H",
23432:       mode: "scheduled_polling_resolution",
23433:       status: "success",
23434:       handled: true,
23435:       resolved: true,
23436:       write_performed: true,
23437:       target_row: existingRowIndex,
23438:       readback_verified: readbackVerified,
23439:       duplicate_prevented: true,
23440:       gmail_read_performed: false,
23441:       gmail_modified: false,
```

#### append L23450

```javascript
23442:       mail_trigger_created: false,
23443:       account_ledger_write_performed: false,
23444:       finance_events_write_performed: false,
23445:       review_queue_write_performed: true,
23446:       domain_tab_write_performed: false
23447:     });
23448:   }
23449: 
23450:   var appendRes = appendByHeader_(ss, AIRO_CONFIG.tabs.review, rowData, { createIfMissing: false });
23451: 
23452:   if (appendRes && appendRes.status === "written") {
23453:     targetRow = appendRes.row;
23454:     var sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.review);
23455:     if (sheet) {
23456:       var header = findHeader_(sheet);
23457:       if (header) {
23458:         var readbackValues = sheet.getRange(targetRow, 1, 1, sheet.getLastColumn()).getValues()[0];
23459:         var checkHeaders = header.headers;
23460:         var checkQueueIdCol = -1;
23461:         var checkAmountCol = -1;
23462:         var checkAccountCol = -1;
```

#### review_queue L23490

```javascript
23482:           readStatus === "pending"
23483:         ) {
23484:           readbackVerified = true;
23485:         }
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
```

#### direct_approval L23494

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
```

#### direct_approval L23495

```javascript
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
```

#### direct_approval L23499

```javascript
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
```

#### return_json L23508

```javascript
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
```

### approval_approve

#### return_text L24232

```javascript
24224:               "Kategori: " + item.parsed_category + (item.parsed_subcategory ? (" / " + item.parsed_subcategory) : "") + "\n" +
24225:               "Status: rejected\n" +
24226:               "Readback: PASS.";
24227:   return reply;
24228: }
24229: 
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

#### return_text L24236

```javascript
24228: }
24229: 
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
```

#### review_header L24238

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
```

#### return_text L24239

```javascript
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
```

#### review_header L24241

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
24248:     ? airoTask614FindReviewItemByQueueId_(ss, arg)
24249:     : airoSprint7HFindItemInSheet_(
24250:         ss,
24251:         arg,
24252:         pendingItems
24253:       );
```

#### return_text L24255

```javascript
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
```

#### set_review_value L24258

```javascript
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

#### return_text L24260

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
24267:   if (item.write_status !== "pending" && item.review_status !== "pending") {
24268:     return "Gagal: status bukan pending (write_status: " + item.write_status + ", review_status: " + item.review_status + ").";
24269:   }
24270:   if (item.linked_account_ledger_entry_id !== "" || item.linked_event_id !== "") {
24271:     return "Gagal: linked ledger atau event sudah terisi.";
24272:   }
```

#### return_text L24265

```javascript
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
24271:     return "Gagal: linked ledger atau event sudah terisi.";
24272:   }
24273: 
24274:   // Required fields checks
24275:   if (!item.parsed_type) return "Gagal: parsed_type kosong.";
24276:   if (!item.parsed_amount || isNaN(item.parsed_amount) || item.parsed_amount <= 0) return "Gagal: parsed_amount tidak valid.";
24277:   if (!item.parsed_account) return "Gagal: parsed_account kosong.";
```

#### set_review_value L24267

```javascript
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
24271:     return "Gagal: linked ledger atau event sudah terisi.";
24272:   }
24273: 
24274:   // Required fields checks
24275:   if (!item.parsed_type) return "Gagal: parsed_type kosong.";
24276:   if (!item.parsed_amount || isNaN(item.parsed_amount) || item.parsed_amount <= 0) return "Gagal: parsed_amount tidak valid.";
24277:   if (!item.parsed_account) return "Gagal: parsed_account kosong.";
24278:   if (!item.parsed_category) return "Gagal: parsed_category kosong.";
24279: 
```

#### set_review_value L24268

```javascript
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
24271:     return "Gagal: linked ledger atau event sudah terisi.";
24272:   }
24273: 
24274:   // Required fields checks
24275:   if (!item.parsed_type) return "Gagal: parsed_type kosong.";
24276:   if (!item.parsed_amount || isNaN(item.parsed_amount) || item.parsed_amount <= 0) return "Gagal: parsed_amount tidak valid.";
24277:   if (!item.parsed_account) return "Gagal: parsed_account kosong.";
24278:   if (!item.parsed_category) return "Gagal: parsed_category kosong.";
24279: 
24280:   var registry = airoSprint7CategoryContractGetRegistry_();
```

#### account L24270

```javascript
24262: 
24263:   // Pre-checks
24264:   if (item.write_policy !== "staging") {
24265:     return "Gagal: write_policy bukan staging (" + item.write_policy + ").";
24266:   }
24267:   if (item.write_status !== "pending" && item.review_status !== "pending") {
24268:     return "Gagal: status bukan pending (write_status: " + item.write_status + ", review_status: " + item.review_status + ").";
24269:   }
24270:   if (item.linked_account_ledger_entry_id !== "" || item.linked_event_id !== "") {
24271:     return "Gagal: linked ledger atau event sudah terisi.";
24272:   }
24273: 
24274:   // Required fields checks
24275:   if (!item.parsed_type) return "Gagal: parsed_type kosong.";
24276:   if (!item.parsed_amount || isNaN(item.parsed_amount) || item.parsed_amount <= 0) return "Gagal: parsed_amount tidak valid.";
24277:   if (!item.parsed_account) return "Gagal: parsed_account kosong.";
24278:   if (!item.parsed_category) return "Gagal: parsed_category kosong.";
24279: 
24280:   var registry = airoSprint7CategoryContractGetRegistry_();
24281:   var catData = registry[item.parsed_category];
24282:   if (catData && catData.subcategories && catData.subcategories.length > 0) {
```

#### return_text L24271

```javascript
24263:   // Pre-checks
24264:   if (item.write_policy !== "staging") {
24265:     return "Gagal: write_policy bukan staging (" + item.write_policy + ").";
24266:   }
24267:   if (item.write_status !== "pending" && item.review_status !== "pending") {
24268:     return "Gagal: status bukan pending (write_status: " + item.write_status + ", review_status: " + item.review_status + ").";
24269:   }
24270:   if (item.linked_account_ledger_entry_id !== "" || item.linked_event_id !== "") {
24271:     return "Gagal: linked ledger atau event sudah terisi.";
24272:   }
24273: 
24274:   // Required fields checks
24275:   if (!item.parsed_type) return "Gagal: parsed_type kosong.";
24276:   if (!item.parsed_amount || isNaN(item.parsed_amount) || item.parsed_amount <= 0) return "Gagal: parsed_amount tidak valid.";
24277:   if (!item.parsed_account) return "Gagal: parsed_account kosong.";
24278:   if (!item.parsed_category) return "Gagal: parsed_category kosong.";
24279: 
24280:   var registry = airoSprint7CategoryContractGetRegistry_();
24281:   var catData = registry[item.parsed_category];
24282:   if (catData && catData.subcategories && catData.subcategories.length > 0) {
24283:     if (!item.parsed_subcategory) {
```

#### return_text L24275

```javascript
24267:   if (item.write_status !== "pending" && item.review_status !== "pending") {
24268:     return "Gagal: status bukan pending (write_status: " + item.write_status + ", review_status: " + item.review_status + ").";
24269:   }
24270:   if (item.linked_account_ledger_entry_id !== "" || item.linked_event_id !== "") {
24271:     return "Gagal: linked ledger atau event sudah terisi.";
24272:   }
24273: 
24274:   // Required fields checks
24275:   if (!item.parsed_type) return "Gagal: parsed_type kosong.";
24276:   if (!item.parsed_amount || isNaN(item.parsed_amount) || item.parsed_amount <= 0) return "Gagal: parsed_amount tidak valid.";
24277:   if (!item.parsed_account) return "Gagal: parsed_account kosong.";
24278:   if (!item.parsed_category) return "Gagal: parsed_category kosong.";
24279: 
24280:   var registry = airoSprint7CategoryContractGetRegistry_();
24281:   var catData = registry[item.parsed_category];
24282:   if (catData && catData.subcategories && catData.subcategories.length > 0) {
24283:     if (!item.parsed_subcategory) {
24284:       return "Gagal: parsed_subcategory kosong untuk kategori " + item.parsed_category + ".";
24285:     }
24286:   }
24287: 
```

#### return_text L24276

```javascript
24268:     return "Gagal: status bukan pending (write_status: " + item.write_status + ", review_status: " + item.review_status + ").";
24269:   }
24270:   if (item.linked_account_ledger_entry_id !== "" || item.linked_event_id !== "") {
24271:     return "Gagal: linked ledger atau event sudah terisi.";
24272:   }
24273: 
24274:   // Required fields checks
24275:   if (!item.parsed_type) return "Gagal: parsed_type kosong.";
24276:   if (!item.parsed_amount || isNaN(item.parsed_amount) || item.parsed_amount <= 0) return "Gagal: parsed_amount tidak valid.";
24277:   if (!item.parsed_account) return "Gagal: parsed_account kosong.";
24278:   if (!item.parsed_category) return "Gagal: parsed_category kosong.";
24279: 
24280:   var registry = airoSprint7CategoryContractGetRegistry_();
24281:   var catData = registry[item.parsed_category];
24282:   if (catData && catData.subcategories && catData.subcategories.length > 0) {
24283:     if (!item.parsed_subcategory) {
24284:       return "Gagal: parsed_subcategory kosong untuk kategori " + item.parsed_category + ".";
24285:     }
24286:   }
24287: 
24288:   if (!item.email_candidate_id) return "Gagal: email_candidate_id kosong.";
```

#### return_text L24277

```javascript
24269:   }
24270:   if (item.linked_account_ledger_entry_id !== "" || item.linked_event_id !== "") {
24271:     return "Gagal: linked ledger atau event sudah terisi.";
24272:   }
24273: 
24274:   // Required fields checks
24275:   if (!item.parsed_type) return "Gagal: parsed_type kosong.";
24276:   if (!item.parsed_amount || isNaN(item.parsed_amount) || item.parsed_amount <= 0) return "Gagal: parsed_amount tidak valid.";
24277:   if (!item.parsed_account) return "Gagal: parsed_account kosong.";
24278:   if (!item.parsed_category) return "Gagal: parsed_category kosong.";
24279: 
24280:   var registry = airoSprint7CategoryContractGetRegistry_();
24281:   var catData = registry[item.parsed_category];
24282:   if (catData && catData.subcategories && catData.subcategories.length > 0) {
24283:     if (!item.parsed_subcategory) {
24284:       return "Gagal: parsed_subcategory kosong untuk kategori " + item.parsed_category + ".";
24285:     }
24286:   }
24287: 
24288:   if (!item.email_candidate_id) return "Gagal: email_candidate_id kosong.";
24289:   if (item.source === "email") {
```

#### return_text L24278

```javascript
24270:   if (item.linked_account_ledger_entry_id !== "" || item.linked_event_id !== "") {
24271:     return "Gagal: linked ledger atau event sudah terisi.";
24272:   }
24273: 
24274:   // Required fields checks
24275:   if (!item.parsed_type) return "Gagal: parsed_type kosong.";
24276:   if (!item.parsed_amount || isNaN(item.parsed_amount) || item.parsed_amount <= 0) return "Gagal: parsed_amount tidak valid.";
24277:   if (!item.parsed_account) return "Gagal: parsed_account kosong.";
24278:   if (!item.parsed_category) return "Gagal: parsed_category kosong.";
24279: 
24280:   var registry = airoSprint7CategoryContractGetRegistry_();
24281:   var catData = registry[item.parsed_category];
24282:   if (catData && catData.subcategories && catData.subcategories.length > 0) {
24283:     if (!item.parsed_subcategory) {
24284:       return "Gagal: parsed_subcategory kosong untuk kategori " + item.parsed_category + ".";
24285:     }
24286:   }
24287: 
24288:   if (!item.email_candidate_id) return "Gagal: email_candidate_id kosong.";
24289:   if (item.source === "email") {
24290:     if (!item.gmail_message_id) return "Gagal: gmail_message_id kosong.";
```

#### category L24281

```javascript
24273: 
24274:   // Required fields checks
24275:   if (!item.parsed_type) return "Gagal: parsed_type kosong.";
24276:   if (!item.parsed_amount || isNaN(item.parsed_amount) || item.parsed_amount <= 0) return "Gagal: parsed_amount tidak valid.";
24277:   if (!item.parsed_account) return "Gagal: parsed_account kosong.";
24278:   if (!item.parsed_category) return "Gagal: parsed_category kosong.";
24279: 
24280:   var registry = airoSprint7CategoryContractGetRegistry_();
24281:   var catData = registry[item.parsed_category];
24282:   if (catData && catData.subcategories && catData.subcategories.length > 0) {
24283:     if (!item.parsed_subcategory) {
24284:       return "Gagal: parsed_subcategory kosong untuk kategori " + item.parsed_category + ".";
24285:     }
24286:   }
24287: 
24288:   if (!item.email_candidate_id) return "Gagal: email_candidate_id kosong.";
24289:   if (item.source === "email") {
24290:     if (!item.gmail_message_id) return "Gagal: gmail_message_id kosong.";
24291:     if (!item.gmail_thread_id) return "Gagal: gmail_thread_id kosong.";
24292:   }
24293: 
```

#### category L24283

```javascript
24275:   if (!item.parsed_type) return "Gagal: parsed_type kosong.";
24276:   if (!item.parsed_amount || isNaN(item.parsed_amount) || item.parsed_amount <= 0) return "Gagal: parsed_amount tidak valid.";
24277:   if (!item.parsed_account) return "Gagal: parsed_account kosong.";
24278:   if (!item.parsed_category) return "Gagal: parsed_category kosong.";
24279: 
24280:   var registry = airoSprint7CategoryContractGetRegistry_();
24281:   var catData = registry[item.parsed_category];
24282:   if (catData && catData.subcategories && catData.subcategories.length > 0) {
24283:     if (!item.parsed_subcategory) {
24284:       return "Gagal: parsed_subcategory kosong untuk kategori " + item.parsed_category + ".";
24285:     }
24286:   }
24287: 
24288:   if (!item.email_candidate_id) return "Gagal: email_candidate_id kosong.";
24289:   if (item.source === "email") {
24290:     if (!item.gmail_message_id) return "Gagal: gmail_message_id kosong.";
24291:     if (!item.gmail_thread_id) return "Gagal: gmail_thread_id kosong.";
24292:   }
24293: 
24294:   var parsedDate = null;
24295:   var candidateDateRaw = parseDate_(item.raw_text || "");
```

#### return_text L24284

```javascript
24276:   if (!item.parsed_amount || isNaN(item.parsed_amount) || item.parsed_amount <= 0) return "Gagal: parsed_amount tidak valid.";
24277:   if (!item.parsed_account) return "Gagal: parsed_account kosong.";
24278:   if (!item.parsed_category) return "Gagal: parsed_category kosong.";
24279: 
24280:   var registry = airoSprint7CategoryContractGetRegistry_();
24281:   var catData = registry[item.parsed_category];
24282:   if (catData && catData.subcategories && catData.subcategories.length > 0) {
24283:     if (!item.parsed_subcategory) {
24284:       return "Gagal: parsed_subcategory kosong untuk kategori " + item.parsed_category + ".";
24285:     }
24286:   }
24287: 
24288:   if (!item.email_candidate_id) return "Gagal: email_candidate_id kosong.";
24289:   if (item.source === "email") {
24290:     if (!item.gmail_message_id) return "Gagal: gmail_message_id kosong.";
24291:     if (!item.gmail_thread_id) return "Gagal: gmail_thread_id kosong.";
24292:   }
24293: 
24294:   var parsedDate = null;
24295:   var candidateDateRaw = parseDate_(item.raw_text || "");
24296:   var candidateDate = airoEnsureDateObject_(candidateDateRaw);
```

#### return_text L24288

```javascript
24280:   var registry = airoSprint7CategoryContractGetRegistry_();
24281:   var catData = registry[item.parsed_category];
24282:   if (catData && catData.subcategories && catData.subcategories.length > 0) {
24283:     if (!item.parsed_subcategory) {
24284:       return "Gagal: parsed_subcategory kosong untuk kategori " + item.parsed_category + ".";
24285:     }
24286:   }
24287: 
24288:   if (!item.email_candidate_id) return "Gagal: email_candidate_id kosong.";
24289:   if (item.source === "email") {
24290:     if (!item.gmail_message_id) return "Gagal: gmail_message_id kosong.";
24291:     if (!item.gmail_thread_id) return "Gagal: gmail_thread_id kosong.";
24292:   }
24293: 
24294:   var parsedDate = null;
24295:   var candidateDateRaw = parseDate_(item.raw_text || "");
24296:   var candidateDate = airoEnsureDateObject_(candidateDateRaw);
24297:   if (candidateDate && !isNaN(candidateDate.getTime())) {
24298:     parsedDate = candidateDate;
24299:   }
24300:   if (!parsedDate) {
```

#### return_text L24290

```javascript
24282:   if (catData && catData.subcategories && catData.subcategories.length > 0) {
24283:     if (!item.parsed_subcategory) {
24284:       return "Gagal: parsed_subcategory kosong untuk kategori " + item.parsed_category + ".";
24285:     }
24286:   }
24287: 
24288:   if (!item.email_candidate_id) return "Gagal: email_candidate_id kosong.";
24289:   if (item.source === "email") {
24290:     if (!item.gmail_message_id) return "Gagal: gmail_message_id kosong.";
24291:     if (!item.gmail_thread_id) return "Gagal: gmail_thread_id kosong.";
24292:   }
24293: 
24294:   var parsedDate = null;
24295:   var candidateDateRaw = parseDate_(item.raw_text || "");
24296:   var candidateDate = airoEnsureDateObject_(candidateDateRaw);
24297:   if (candidateDate && !isNaN(candidateDate.getTime())) {
24298:     parsedDate = candidateDate;
24299:   }
24300:   if (!parsedDate) {
24301:     var receivedAtCol = map["received_at"];
24302:     var receivedAtVal = (receivedAtCol !== undefined && item.rowData) ? item.rowData[receivedAtCol] : "";
```

#### return_text L24291

```javascript
24283:     if (!item.parsed_subcategory) {
24284:       return "Gagal: parsed_subcategory kosong untuk kategori " + item.parsed_category + ".";
24285:     }
24286:   }
24287: 
24288:   if (!item.email_candidate_id) return "Gagal: email_candidate_id kosong.";
24289:   if (item.source === "email") {
24290:     if (!item.gmail_message_id) return "Gagal: gmail_message_id kosong.";
24291:     if (!item.gmail_thread_id) return "Gagal: gmail_thread_id kosong.";
24292:   }
24293: 
24294:   var parsedDate = null;
24295:   var candidateDateRaw = parseDate_(item.raw_text || "");
24296:   var candidateDate = airoEnsureDateObject_(candidateDateRaw);
24297:   if (candidateDate && !isNaN(candidateDate.getTime())) {
24298:     parsedDate = candidateDate;
24299:   }
24300:   if (!parsedDate) {
24301:     var receivedAtCol = map["received_at"];
24302:     var receivedAtVal = (receivedAtCol !== undefined && item.rowData) ? item.rowData[receivedAtCol] : "";
24303:     var receivedAtDate = airoEnsureDateObject_(receivedAtVal);
```

#### category L24323

```javascript
24315:   }
24316:   if (!parsedDate) {
24317:     parsedDate = new Date();
24318:   }
24319: 
24320:   var parsedObj = {
24321:     date: parsedDate,
24322:     type: item.parsed_type,
24323:     category: item.parsed_category,
24324:     subcategory: item.parsed_subcategory,
24325:     description: item.raw_text,
24326:     amount: item.parsed_amount,
24327:     account: item.parsed_account,
24328:     creditor: parseCreditor_(item.raw_text || ""),
24329:     merchant: parseMerchant_(item.raw_text || ""),
24330:     billingCycleId: Utilities.formatDate(parsedDate, Session.getScriptTimeZone(), "yyyy-MM"),
24331:     assetSection: parseAssetSection_(item.raw_text || ""),
24332:     needsReview: false
24333:   };
24334: 
24335:   var stagingResult = {
```

#### category L24324

```javascript
24316:   if (!parsedDate) {
24317:     parsedDate = new Date();
24318:   }
24319: 
24320:   var parsedObj = {
24321:     date: parsedDate,
24322:     type: item.parsed_type,
24323:     category: item.parsed_category,
24324:     subcategory: item.parsed_subcategory,
24325:     description: item.raw_text,
24326:     amount: item.parsed_amount,
24327:     account: item.parsed_account,
24328:     creditor: parseCreditor_(item.raw_text || ""),
24329:     merchant: parseMerchant_(item.raw_text || ""),
24330:     billingCycleId: Utilities.formatDate(parsedDate, Session.getScriptTimeZone(), "yyyy-MM"),
24331:     assetSection: parseAssetSection_(item.raw_text || ""),
24332:     needsReview: false
24333:   };
24334: 
24335:   var stagingResult = {
24336:     rowId: "review:" + item.queue_id,
```

#### amount L24326

```javascript
24318:   }
24319: 
24320:   var parsedObj = {
24321:     date: parsedDate,
24322:     type: item.parsed_type,
24323:     category: item.parsed_category,
24324:     subcategory: item.parsed_subcategory,
24325:     description: item.raw_text,
24326:     amount: item.parsed_amount,
24327:     account: item.parsed_account,
24328:     creditor: parseCreditor_(item.raw_text || ""),
24329:     merchant: parseMerchant_(item.raw_text || ""),
24330:     billingCycleId: Utilities.formatDate(parsedDate, Session.getScriptTimeZone(), "yyyy-MM"),
24331:     assetSection: parseAssetSection_(item.raw_text || ""),
24332:     needsReview: false
24333:   };
24334: 
24335:   var stagingResult = {
24336:     rowId: "review:" + item.queue_id,
24337:     linked_txn_id: "review:" + item.queue_id
24338:   };
```

#### account L24327

```javascript
24319: 
24320:   var parsedObj = {
24321:     date: parsedDate,
24322:     type: item.parsed_type,
24323:     category: item.parsed_category,
24324:     subcategory: item.parsed_subcategory,
24325:     description: item.raw_text,
24326:     amount: item.parsed_amount,
24327:     account: item.parsed_account,
24328:     creditor: parseCreditor_(item.raw_text || ""),
24329:     merchant: parseMerchant_(item.raw_text || ""),
24330:     billingCycleId: Utilities.formatDate(parsedDate, Session.getScriptTimeZone(), "yyyy-MM"),
24331:     assetSection: parseAssetSection_(item.raw_text || ""),
24332:     needsReview: false
24333:   };
24334: 
24335:   var stagingResult = {
24336:     rowId: "review:" + item.queue_id,
24337:     linked_txn_id: "review:" + item.queue_id
24338:   };
24339: 
```

#### route_review L24341

```javascript
24333:   };
24334: 
24335:   var stagingResult = {
24336:     rowId: "review:" + item.queue_id,
24337:     linked_txn_id: "review:" + item.queue_id
24338:   };
24339: 
24340:   // AIRO_TASK8_HUTANG_DIRECT_APPROVAL_ROUTED_PROJECTION_FIX_V1
24341:   var plannedTab = routeReviewApprovedTab_(parsedObj, item.raw_text);
24342:   var approvalType = String(parsedObj.type || "").toLowerCase();
24343:   var approvalCategory = String(parsedObj.category || "").toLowerCase();
24344:   var approvalSubcategory = String(parsedObj.subcategory || "");
24345:   if (
24346:     approvalType === "debt_payment" ||
24347:     (
24348:       approvalCategory === "debt & obligations" &&
24349:       /\b(hutang|utang)\b/i.test(approvalSubcategory)
24350:     )
24351:   ) {
24352:     plannedTab = AIRO_CONFIG.tabs.hutang;
24353:   }
```

#### category L24343

```javascript
24335:   var stagingResult = {
24336:     rowId: "review:" + item.queue_id,
24337:     linked_txn_id: "review:" + item.queue_id
24338:   };
24339: 
24340:   // AIRO_TASK8_HUTANG_DIRECT_APPROVAL_ROUTED_PROJECTION_FIX_V1
24341:   var plannedTab = routeReviewApprovedTab_(parsedObj, item.raw_text);
24342:   var approvalType = String(parsedObj.type || "").toLowerCase();
24343:   var approvalCategory = String(parsedObj.category || "").toLowerCase();
24344:   var approvalSubcategory = String(parsedObj.subcategory || "");
24345:   if (
24346:     approvalType === "debt_payment" ||
24347:     (
24348:       approvalCategory === "debt & obligations" &&
24349:       /\b(hutang|utang)\b/i.test(approvalSubcategory)
24350:     )
24351:   ) {
24352:     plannedTab = AIRO_CONFIG.tabs.hutang;
24353:   }
24354:   var result = writeRouted_(ss, plannedTab, parsedObj, item.raw_text, stagingResult);
24355:   var writePerformed = false;
```

#### category L24344

```javascript
24336:     rowId: "review:" + item.queue_id,
24337:     linked_txn_id: "review:" + item.queue_id
24338:   };
24339: 
24340:   // AIRO_TASK8_HUTANG_DIRECT_APPROVAL_ROUTED_PROJECTION_FIX_V1
24341:   var plannedTab = routeReviewApprovedTab_(parsedObj, item.raw_text);
24342:   var approvalType = String(parsedObj.type || "").toLowerCase();
24343:   var approvalCategory = String(parsedObj.category || "").toLowerCase();
24344:   var approvalSubcategory = String(parsedObj.subcategory || "");
24345:   if (
24346:     approvalType === "debt_payment" ||
24347:     (
24348:       approvalCategory === "debt & obligations" &&
24349:       /\b(hutang|utang)\b/i.test(approvalSubcategory)
24350:     )
24351:   ) {
24352:     plannedTab = AIRO_CONFIG.tabs.hutang;
24353:   }
24354:   var result = writeRouted_(ss, plannedTab, parsedObj, item.raw_text, stagingResult);
24355:   var writePerformed = false;
24356:   var financeEventWritten = false;
```

### approval_command

#### approval_arg L24423

```javascript
24415:     return "Gagal menulis transaksi ke ledger.";
24416:   }
24417: }
24418: 
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
```

#### approval_arg L24430

```javascript
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
```

#### send_telegram L24436

```javascript
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
```

#### return_json L24442

```javascript
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
```

#### approval_arg L24449

```javascript
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
24460:       replyText =
24461:         "Tidak ada transaksi terakhir yang siap disetujui.\n\n" +
```

#### approval_arg L24462

```javascript
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
24464:       replyText = airoSprint7HApprovalApprove_(
24465:         ss,
24466:         directQueueId
24467:       );
24468: 
24469:       writePerformed =
24470:         replyText.indexOf(
24471:           "Transaksi berhasil disetujui"
24472:         ) !== -1;
24473:     }
24474: 
```

#### approve_call L24464

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
24471:           "Transaksi berhasil disetujui"
24472:         ) !== -1;
24473:     }
24474: 
24475:   } else if (cmd === "help") {
24476:     replyText = airoTask614ApprovalHelp_();
```

#### approval_arg L24490

```javascript
24482:     );
24483: 
24484:   } else if (
24485:     cmd === "detail" ||
24486:     cmd === "approve" ||
24487:     cmd === "reject" ||
24488:     cmd === "fix"
24489:   ) {
24490:     resolvedArg = airoTask614ResolveApprovalArg_(
24491:       parsed.chat_id,
24492:       arg
24493:     );
24494: 
24495:     if (
24496:       resolvedArg ===
24497:       "__AIRO_TASK614_SNAPSHOT_REQUIRED__"
24498:     ) {
24499:       replyText =
24500:         "Nomor approval belum terkunci atau sudah kedaluwarsa.\n\n" +
24501:         "Jalankan /approval list terlebih dahulu.";
24502: 
```

#### approval_arg L24492

```javascript
24484:   } else if (
24485:     cmd === "detail" ||
24486:     cmd === "approve" ||
24487:     cmd === "reject" ||
24488:     cmd === "fix"
24489:   ) {
24490:     resolvedArg = airoTask614ResolveApprovalArg_(
24491:       parsed.chat_id,
24492:       arg
24493:     );
24494: 
24495:     if (
24496:       resolvedArg ===
24497:       "__AIRO_TASK614_SNAPSHOT_REQUIRED__"
24498:     ) {
24499:       replyText =
24500:         "Nomor approval belum terkunci atau sudah kedaluwarsa.\n\n" +
24501:         "Jalankan /approval list terlebih dahulu.";
24502: 
24503:     } else if (
24504:       resolvedArg ===
```

#### approval_arg L24496

```javascript
24488:     cmd === "fix"
24489:   ) {
24490:     resolvedArg = airoTask614ResolveApprovalArg_(
24491:       parsed.chat_id,
24492:       arg
24493:     );
24494: 
24495:     if (
24496:       resolvedArg ===
24497:       "__AIRO_TASK614_SNAPSHOT_REQUIRED__"
24498:     ) {
24499:       replyText =
24500:         "Nomor approval belum terkunci atau sudah kedaluwarsa.\n\n" +
24501:         "Jalankan /approval list terlebih dahulu.";
24502: 
24503:     } else if (
24504:       resolvedArg ===
24505:       "__AIRO_TASK614_ITEM_NOT_IN_SNAPSHOT__"
24506:     ) {
24507:       replyText =
24508:         "Nomor tidak ditemukan pada daftar approval terakhir.\n\n" +
```

#### approval_arg L24500

```javascript
24492:       arg
24493:     );
24494: 
24495:     if (
24496:       resolvedArg ===
24497:       "__AIRO_TASK614_SNAPSHOT_REQUIRED__"
24498:     ) {
24499:       replyText =
24500:         "Nomor approval belum terkunci atau sudah kedaluwarsa.\n\n" +
24501:         "Jalankan /approval list terlebih dahulu.";
24502: 
24503:     } else if (
24504:       resolvedArg ===
24505:       "__AIRO_TASK614_ITEM_NOT_IN_SNAPSHOT__"
24506:     ) {
24507:       replyText =
24508:         "Nomor tidak ditemukan pada daftar approval terakhir.\n\n" +
24509:         "Jalankan /approval list untuk memperbarui daftar.";
24510: 
24511:     } else if (!resolvedArg) {
24512:       replyText =
```

#### approval_arg L24501

```javascript
24493:     );
24494: 
24495:     if (
24496:       resolvedArg ===
24497:       "__AIRO_TASK614_SNAPSHOT_REQUIRED__"
24498:     ) {
24499:       replyText =
24500:         "Nomor approval belum terkunci atau sudah kedaluwarsa.\n\n" +
24501:         "Jalankan /approval list terlebih dahulu.";
24502: 
24503:     } else if (
24504:       resolvedArg ===
24505:       "__AIRO_TASK614_ITEM_NOT_IN_SNAPSHOT__"
24506:     ) {
24507:       replyText =
24508:         "Nomor tidak ditemukan pada daftar approval terakhir.\n\n" +
24509:         "Jalankan /approval list untuk memperbarui daftar.";
24510: 
24511:     } else if (!resolvedArg) {
24512:       replyText =
24513:         "Nomor transaksi belum diberikan.\n\n" +
```

#### approval_arg L24504

```javascript
24496:       resolvedArg ===
24497:       "__AIRO_TASK614_SNAPSHOT_REQUIRED__"
24498:     ) {
24499:       replyText =
24500:         "Nomor approval belum terkunci atau sudah kedaluwarsa.\n\n" +
24501:         "Jalankan /approval list terlebih dahulu.";
24502: 
24503:     } else if (
24504:       resolvedArg ===
24505:       "__AIRO_TASK614_ITEM_NOT_IN_SNAPSHOT__"
24506:     ) {
24507:       replyText =
24508:         "Nomor tidak ditemukan pada daftar approval terakhir.\n\n" +
24509:         "Jalankan /approval list untuk memperbarui daftar.";
24510: 
24511:     } else if (!resolvedArg) {
24512:       replyText =
24513:         "Nomor transaksi belum diberikan.\n\n" +
24514:         "Contoh: /approval " + cmd + " 1";
24515: 
24516:     } else if (cmd === "detail") {
```

#### approval_arg L24508

```javascript
24500:         "Nomor approval belum terkunci atau sudah kedaluwarsa.\n\n" +
24501:         "Jalankan /approval list terlebih dahulu.";
24502: 
24503:     } else if (
24504:       resolvedArg ===
24505:       "__AIRO_TASK614_ITEM_NOT_IN_SNAPSHOT__"
24506:     ) {
24507:       replyText =
24508:         "Nomor tidak ditemukan pada daftar approval terakhir.\n\n" +
24509:         "Jalankan /approval list untuk memperbarui daftar.";
24510: 
24511:     } else if (!resolvedArg) {
24512:       replyText =
24513:         "Nomor transaksi belum diberikan.\n\n" +
24514:         "Contoh: /approval " + cmd + " 1";
24515: 
24516:     } else if (cmd === "detail") {
24517:       replyText = airoSprint7HApprovalDetail_(
24518:         ss,
24519:         resolvedArg
24520:       );
```

#### approval_arg L24509

```javascript
24501:         "Jalankan /approval list terlebih dahulu.";
24502: 
24503:     } else if (
24504:       resolvedArg ===
24505:       "__AIRO_TASK614_ITEM_NOT_IN_SNAPSHOT__"
24506:     ) {
24507:       replyText =
24508:         "Nomor tidak ditemukan pada daftar approval terakhir.\n\n" +
24509:         "Jalankan /approval list untuk memperbarui daftar.";
24510: 
24511:     } else if (!resolvedArg) {
24512:       replyText =
24513:         "Nomor transaksi belum diberikan.\n\n" +
24514:         "Contoh: /approval " + cmd + " 1";
24515: 
24516:     } else if (cmd === "detail") {
24517:       replyText = airoSprint7HApprovalDetail_(
24518:         ss,
24519:         resolvedArg
24520:       );
24521: 
```

#### approval_arg L24511

```javascript
24503:     } else if (
24504:       resolvedArg ===
24505:       "__AIRO_TASK614_ITEM_NOT_IN_SNAPSHOT__"
24506:     ) {
24507:       replyText =
24508:         "Nomor tidak ditemukan pada daftar approval terakhir.\n\n" +
24509:         "Jalankan /approval list untuk memperbarui daftar.";
24510: 
24511:     } else if (!resolvedArg) {
24512:       replyText =
24513:         "Nomor transaksi belum diberikan.\n\n" +
24514:         "Contoh: /approval " + cmd + " 1";
24515: 
24516:     } else if (cmd === "detail") {
24517:       replyText = airoSprint7HApprovalDetail_(
24518:         ss,
24519:         resolvedArg
24520:       );
24521: 
24522:     } else if (cmd === "approve") {
24523:       replyText = airoSprint7HApprovalApprove_(
```

#### approval_arg L24514

```javascript
24506:     ) {
24507:       replyText =
24508:         "Nomor tidak ditemukan pada daftar approval terakhir.\n\n" +
24509:         "Jalankan /approval list untuk memperbarui daftar.";
24510: 
24511:     } else if (!resolvedArg) {
24512:       replyText =
24513:         "Nomor transaksi belum diberikan.\n\n" +
24514:         "Contoh: /approval " + cmd + " 1";
24515: 
24516:     } else if (cmd === "detail") {
24517:       replyText = airoSprint7HApprovalDetail_(
24518:         ss,
24519:         resolvedArg
24520:       );
24521: 
24522:     } else if (cmd === "approve") {
24523:       replyText = airoSprint7HApprovalApprove_(
24524:         ss,
24525:         resolvedArg
24526:       );
```

#### approval_arg L24519

```javascript
24511:     } else if (!resolvedArg) {
24512:       replyText =
24513:         "Nomor transaksi belum diberikan.\n\n" +
24514:         "Contoh: /approval " + cmd + " 1";
24515: 
24516:     } else if (cmd === "detail") {
24517:       replyText = airoSprint7HApprovalDetail_(
24518:         ss,
24519:         resolvedArg
24520:       );
24521: 
24522:     } else if (cmd === "approve") {
24523:       replyText = airoSprint7HApprovalApprove_(
24524:         ss,
24525:         resolvedArg
24526:       );
24527: 
24528:       writePerformed =
24529:         replyText.indexOf(
24530:           "Transaksi berhasil disetujui"
24531:         ) !== -1;
```

#### approve_call L24523

```javascript
24515: 
24516:     } else if (cmd === "detail") {
24517:       replyText = airoSprint7HApprovalDetail_(
24518:         ss,
24519:         resolvedArg
24520:       );
24521: 
24522:     } else if (cmd === "approve") {
24523:       replyText = airoSprint7HApprovalApprove_(
24524:         ss,
24525:         resolvedArg
24526:       );
24527: 
24528:       writePerformed =
24529:         replyText.indexOf(
24530:           "Transaksi berhasil disetujui"
24531:         ) !== -1;
24532: 
24533:     } else if (cmd === "reject") {
24534:       replyText = airoSprint7HApprovalReject_(
24535:         ss,
```

#### approval_arg L24525

```javascript
24517:       replyText = airoSprint7HApprovalDetail_(
24518:         ss,
24519:         resolvedArg
24520:       );
24521: 
24522:     } else if (cmd === "approve") {
24523:       replyText = airoSprint7HApprovalApprove_(
24524:         ss,
24525:         resolvedArg
24526:       );
24527: 
24528:       writePerformed =
24529:         replyText.indexOf(
24530:           "Transaksi berhasil disetujui"
24531:         ) !== -1;
24532: 
24533:     } else if (cmd === "reject") {
24534:       replyText = airoSprint7HApprovalReject_(
24535:         ss,
24536:         resolvedArg
24537:       );
```

#### approval_arg L24536

```javascript
24528:       writePerformed =
24529:         replyText.indexOf(
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
```

#### approval_arg L24547

```javascript
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
```

#### approval_arg L24553

```javascript
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
```

#### send_telegram L24558

```javascript
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

#### return_json L24561

```javascript
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
24571: 
24572: function runTask3BCorrectiveRepairFromEditor() {
24573:   var ss = airoSprint7FSpreadsheet_();
```

#### approval_arg L24564

```javascript
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
24571: 
24572: function runTask3BCorrectiveRepairFromEditor() {
24573:   var ss = airoSprint7FSpreadsheet_();
24574:   var sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.review);
24575:   if (!sheet) return "Sheet missing";
24576:   var header = findHeader_(sheet);
```

#### approval_arg L24565

```javascript
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
24571: 
24572: function runTask3BCorrectiveRepairFromEditor() {
24573:   var ss = airoSprint7FSpreadsheet_();
24574:   var sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.review);
24575:   if (!sheet) return "Sheet missing";
24576:   var header = findHeader_(sheet);
24577:   if (!header) return "Header missing";
```

#### approval_arg L24566

```javascript
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
24571: 
24572: function runTask3BCorrectiveRepairFromEditor() {
24573:   var ss = airoSprint7FSpreadsheet_();
24574:   var sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.review);
24575:   if (!sheet) return "Sheet missing";
24576:   var header = findHeader_(sheet);
24577:   if (!header) return "Header missing";
24578: 
```

#### approval_arg L24567

```javascript
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
24571: 
24572: function runTask3BCorrectiveRepairFromEditor() {
24573:   var ss = airoSprint7FSpreadsheet_();
24574:   var sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.review);
24575:   if (!sheet) return "Sheet missing";
24576:   var header = findHeader_(sheet);
24577:   if (!header) return "Header missing";
24578: 
24579:   var headers = header.headers;
```

### success_reply

#### ledger_entry L1213

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
1220:     } else if (canonicalSheetName_(writtenTab) === canonicalSheetName_(AIRO_CONFIG.tabs.accountLedger)) {
1221:       isLedgerWrite = true;
1222:       ledgerRow = rResult.row;
1223:     } else if (rResult.account_ledger_result && rResult.account_ledger_result.status === 'written') {
1224:       isLedgerWrite = true;
1225:       ledgerRow = rResult.account_ledger_result.row;
```

#### ledger_entry L1214

```javascript
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
```

#### internal_transfer L1218

```javascript
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
1229:   if (isLedgerWrite) {
1230:     if (rResult.transferInternal === true) {
```

#### ledger_entry L1219

```javascript
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
1229:   if (isLedgerWrite) {
1230:     if (rResult.transferInternal === true) {
1231:       var source = rResult.sourceAccount || 'Sumber';
```

#### ledger_entry L1220

```javascript
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
1229:   if (isLedgerWrite) {
1230:     if (rResult.transferInternal === true) {
1231:       var source = rResult.sourceAccount || 'Sumber';
1232:       var target = rResult.targetAccount || prs.account || 'Tujuan';
```

#### ledger_entry L1221

```javascript
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
1229:   if (isLedgerWrite) {
1230:     if (rResult.transferInternal === true) {
1231:       var source = rResult.sourceAccount || 'Sumber';
1232:       var target = rResult.targetAccount || prs.account || 'Tujuan';
1233:       var sourceRow = rResult.accountLedgerRows ? rResult.accountLedgerRows[0] : null;
```

#### ledger_entry L1224

```javascript
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
1229:   if (isLedgerWrite) {
1230:     if (rResult.transferInternal === true) {
1231:       var source = rResult.sourceAccount || 'Sumber';
1232:       var target = rResult.targetAccount || prs.account || 'Tujuan';
1233:       var sourceRow = rResult.accountLedgerRows ? rResult.accountLedgerRows[0] : null;
1234:       var targetRow = rResult.accountLedgerRows ? rResult.accountLedgerRows[1] : null;
1235: 
1236:       var sourceDetails = getAccountLedgerRowDetails_(spreadsheet, sourceRow);
```

#### ledger_entry L1229

```javascript
1221:       isLedgerWrite = true;
1222:       ledgerRow = rResult.row;
1223:     } else if (rResult.account_ledger_result && rResult.account_ledger_result.status === 'written') {
1224:       isLedgerWrite = true;
1225:       ledgerRow = rResult.account_ledger_result.row;
1226:     }
1227:   }
1228: 
1229:   if (isLedgerWrite) {
1230:     if (rResult.transferInternal === true) {
1231:       var source = rResult.sourceAccount || 'Sumber';
1232:       var target = rResult.targetAccount || prs.account || 'Tujuan';
1233:       var sourceRow = rResult.accountLedgerRows ? rResult.accountLedgerRows[0] : null;
1234:       var targetRow = rResult.accountLedgerRows ? rResult.accountLedgerRows[1] : null;
1235: 
1236:       var sourceDetails = getAccountLedgerRowDetails_(spreadsheet, sourceRow);
1237:       var targetDetails = getAccountLedgerRowDetails_(spreadsheet, targetRow);
1238: 
1239:       var formattedAmt = formatBalanceRupiah_(amount);
1240:       if (formattedAmt === 'Unknown' || !amount) {
1241:         formattedAmt = 'Rp' + amount;
```

#### internal_transfer L1230

```javascript
1222:       ledgerRow = rResult.row;
1223:     } else if (rResult.account_ledger_result && rResult.account_ledger_result.status === 'written') {
1224:       isLedgerWrite = true;
1225:       ledgerRow = rResult.account_ledger_result.row;
1226:     }
1227:   }
1228: 
1229:   if (isLedgerWrite) {
1230:     if (rResult.transferInternal === true) {
1231:       var source = rResult.sourceAccount || 'Sumber';
1232:       var target = rResult.targetAccount || prs.account || 'Tujuan';
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
```

#### internal_transfer L1231

```javascript
1223:     } else if (rResult.account_ledger_result && rResult.account_ledger_result.status === 'written') {
1224:       isLedgerWrite = true;
1225:       ledgerRow = rResult.account_ledger_result.row;
1226:     }
1227:   }
1228: 
1229:   if (isLedgerWrite) {
1230:     if (rResult.transferInternal === true) {
1231:       var source = rResult.sourceAccount || 'Sumber';
1232:       var target = rResult.targetAccount || prs.account || 'Tujuan';
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
```

#### internal_transfer L1232

```javascript
1224:       isLedgerWrite = true;
1225:       ledgerRow = rResult.account_ledger_result.row;
1226:     }
1227:   }
1228: 
1229:   if (isLedgerWrite) {
1230:     if (rResult.transferInternal === true) {
1231:       var source = rResult.sourceAccount || 'Sumber';
1232:       var target = rResult.targetAccount || prs.account || 'Tujuan';
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
```

#### internal_transfer L1233

```javascript
1225:       ledgerRow = rResult.account_ledger_result.row;
1226:     }
1227:   }
1228: 
1229:   if (isLedgerWrite) {
1230:     if (rResult.transferInternal === true) {
1231:       var source = rResult.sourceAccount || 'Sumber';
1232:       var target = rResult.targetAccount || prs.account || 'Tujuan';
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
```

#### internal_transfer L1234

```javascript
1226:     }
1227:   }
1228: 
1229:   if (isLedgerWrite) {
1230:     if (rResult.transferInternal === true) {
1231:       var source = rResult.sourceAccount || 'Sumber';
1232:       var target = rResult.targetAccount || prs.account || 'Tujuan';
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
```

#### balance L1236

```javascript
1228: 
1229:   if (isLedgerWrite) {
1230:     if (rResult.transferInternal === true) {
1231:       var source = rResult.sourceAccount || 'Sumber';
1232:       var target = rResult.targetAccount || prs.account || 'Tujuan';
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
1248:         return '✅ Transfer dicatat.\n\n' +
```

#### balance L1237

```javascript
1229:   if (isLedgerWrite) {
1230:     if (rResult.transferInternal === true) {
1231:       var source = rResult.sourceAccount || 'Sumber';
1232:       var target = rResult.targetAccount || prs.account || 'Tujuan';
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
1248:         return '✅ Transfer dicatat.\n\n' +
1249:           source + ' → ' + target + ': ' + formattedAmt + '\n\n' +
```

#### balance L1239

```javascript
1231:       var source = rResult.sourceAccount || 'Sumber';
1232:       var target = rResult.targetAccount || prs.account || 'Tujuan';
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
1248:         return '✅ Transfer dicatat.\n\n' +
1249:           source + ' → ' + target + ': ' + formattedAmt + '\n\n' +
1250:           'Saldo ' + source + ' sekarang: ' + formatBalanceRupiah_(sourceDetails.balance) + '\n' +
1251:           'Saldo ' + target + ' sekarang: ' + formatBalanceRupiah_(targetDetails.balance);
```

#### internal_transfer L1244

```javascript
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
1248:         return '✅ Transfer dicatat.\n\n' +
1249:           source + ' → ' + target + ': ' + formattedAmt + '\n\n' +
1250:           'Saldo ' + source + ' sekarang: ' + formatBalanceRupiah_(sourceDetails.balance) + '\n' +
1251:           'Saldo ' + target + ' sekarang: ' + formatBalanceRupiah_(targetDetails.balance);
1252:       } else {
1253:         return '✅ Transfer dicatat.\n\n' +
1254:           source + ' → ' + target + ': ' + formattedAmt + '\n' +
1255:           'Saldo terbaru belum bisa dibaca otomatis. Cek Account Ledger untuk verifikasi.';
1256:       }
```

#### balance L1245

```javascript
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
```

#### balance L1246

```javascript
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

#### internal_transfer L1249

```javascript
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
1255:           'Saldo terbaru belum bisa dibaca otomatis. Cek Account Ledger untuk verifikasi.';
1256:       }
1257:     } else {
1258:       // Single Transaction
1259:       var rowToRead = ledgerRow;
1260:       var details = getAccountLedgerRowDetails_(spreadsheet, rowToRead);
1261:       var account = prs.account || 'Unknown';
```

#### balance L1250

```javascript
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
1255:           'Saldo terbaru belum bisa dibaca otomatis. Cek Account Ledger untuk verifikasi.';
1256:       }
1257:     } else {
1258:       // Single Transaction
1259:       var rowToRead = ledgerRow;
1260:       var details = getAccountLedgerRowDetails_(spreadsheet, rowToRead);
1261:       var account = prs.account || 'Unknown';
1262:       var isOutflow = true; // default
```

#### balance L1251

```javascript
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

#### internal_transfer L1254

```javascript
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
1260:       var details = getAccountLedgerRowDetails_(spreadsheet, rowToRead);
1261:       var account = prs.account || 'Unknown';
1262:       var isOutflow = true; // default
1263:       var formattedAmt = formatBalanceRupiah_(amount);
1264:       if (formattedAmt === 'Unknown' || !amount) {
1265:         formattedAmt = 'Rp' + amount;
1266:       }
```

#### balance L1255

```javascript
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
1260:       var details = getAccountLedgerRowDetails_(spreadsheet, rowToRead);
1261:       var account = prs.account || 'Unknown';
1262:       var isOutflow = true; // default
1263:       var formattedAmt = formatBalanceRupiah_(amount);
1264:       if (formattedAmt === 'Unknown' || !amount) {
1265:         formattedAmt = 'Rp' + amount;
1266:       }
1267: 
```

#### balance L1260

```javascript
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
1264:       if (formattedAmt === 'Unknown' || !amount) {
1265:         formattedAmt = 'Rp' + amount;
1266:       }
1267: 
1268:       if (details) {
1269:         account = details.account || account;
1270:         if (details.amountIn !== '' && details.amountIn !== null && details.amountIn !== undefined && Number(details.amountIn) > 0) {
1271:           isOutflow = false;
1272:           formattedAmt = formatBalanceRupiah_(details.amountIn);
```

#### balance L1263

```javascript
1255:           'Saldo terbaru belum bisa dibaca otomatis. Cek Account Ledger untuk verifikasi.';
1256:       }
1257:     } else {
1258:       // Single Transaction
1259:       var rowToRead = ledgerRow;
1260:       var details = getAccountLedgerRowDetails_(spreadsheet, rowToRead);
1261:       var account = prs.account || 'Unknown';
1262:       var isOutflow = true; // default
1263:       var formattedAmt = formatBalanceRupiah_(amount);
1264:       if (formattedAmt === 'Unknown' || !amount) {
1265:         formattedAmt = 'Rp' + amount;
1266:       }
1267: 
1268:       if (details) {
1269:         account = details.account || account;
1270:         if (details.amountIn !== '' && details.amountIn !== null && details.amountIn !== undefined && Number(details.amountIn) > 0) {
1271:           isOutflow = false;
1272:           formattedAmt = formatBalanceRupiah_(details.amountIn);
1273:         } else if (details.amountOut !== '' && details.amountOut !== null && details.amountOut !== undefined && Number(details.amountOut) > 0) {
1274:           isOutflow = true;
1275:           formattedAmt = formatBalanceRupiah_(details.amountOut);
```

#### balance L1272

```javascript
1264:       if (formattedAmt === 'Unknown' || !amount) {
1265:         formattedAmt = 'Rp' + amount;
1266:       }
1267: 
1268:       if (details) {
1269:         account = details.account || account;
1270:         if (details.amountIn !== '' && details.amountIn !== null && details.amountIn !== undefined && Number(details.amountIn) > 0) {
1271:           isOutflow = false;
1272:           formattedAmt = formatBalanceRupiah_(details.amountIn);
1273:         } else if (details.amountOut !== '' && details.amountOut !== null && details.amountOut !== undefined && Number(details.amountOut) > 0) {
1274:           isOutflow = true;
1275:           formattedAmt = formatBalanceRupiah_(details.amountOut);
1276:         }
1277:       }
1278: 
1279:       var directionText = isOutflow ? 'keluar' : 'masuk';
1280: 
1281:       if (details && details.balance !== '' && details.balance !== null && details.balance !== undefined) {
1282:         return '✅ Transaksi dicatat.\n\n' +
1283:           account + ' ' + directionText + ' ' + formattedAmt + '\n' +
1284:           'Kategori: ' + category + '\n\n' +
```

#### balance L1275

```javascript
1267: 
1268:       if (details) {
1269:         account = details.account || account;
1270:         if (details.amountIn !== '' && details.amountIn !== null && details.amountIn !== undefined && Number(details.amountIn) > 0) {
1271:           isOutflow = false;
1272:           formattedAmt = formatBalanceRupiah_(details.amountIn);
1273:         } else if (details.amountOut !== '' && details.amountOut !== null && details.amountOut !== undefined && Number(details.amountOut) > 0) {
1274:           isOutflow = true;
1275:           formattedAmt = formatBalanceRupiah_(details.amountOut);
1276:         }
1277:       }
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
```

#### balance L1281

```javascript
1273:         } else if (details.amountOut !== '' && details.amountOut !== null && details.amountOut !== undefined && Number(details.amountOut) > 0) {
1274:           isOutflow = true;
1275:           formattedAmt = formatBalanceRupiah_(details.amountOut);
1276:         }
1277:       }
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
```

#### balance L1285

```javascript
1277:       }
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
```

### transfer_writer

#### linked L14520

```javascript
14512:     workbook_write_performed: false,
14513:     telegram_send_performed: false,
14514:     gmail_modified: false,
14515:     deploy_performed: false
14516:   };
14517: }
14518: 
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
```

#### source_account L14525

```javascript
14517: }
14518: 
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
```

#### linked L14532

```javascript
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
```

#### source_account L14534

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
14541:     amount: parsed.amount
14542:   };
14543:   var commonIn = {
14544:     ...common,
14545:     rowId: sharedTxnId + ':in',
14546:     linked_txn_id: sharedTxnId + ':out'
```

#### target_account L14539

```javascript
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
```

#### linked L14546

```javascript
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
```

#### target_account L14548

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
14555:       account: 'Cash',
14556:       type: 'transfer_in',
14557:       amount: parsed.amount
14558:     };
14559:     cashResult = writeCashLedgerCompatibility_(ss, parsedCashIn, rawText, common);
14560:   } else if (transfer.sourceAccount === 'Cash') {
```

#### target_account L14552

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
14559:     cashResult = writeCashLedgerCompatibility_(ss, parsedCashIn, rawText, common);
14560:   } else if (transfer.sourceAccount === 'Cash') {
14561:     var parsedCashOut = {
14562:       ...parsed,
14563:       account: 'Cash',
14564:       type: 'transfer_out',
```

#### ledger_write L14559

```javascript
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
14562:       ...parsed,
14563:       account: 'Cash',
14564:       type: 'transfer_out',
14565:       amount: parsed.amount
14566:     };
14567:     cashResult = writeCashLedgerCompatibility_(ss, parsedCashOut, rawText, common);
14568:   }
14569: 
14570:   var transferResult = {
14571:     status: 'written',
```

#### source_account L14560

```javascript
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
14562:       ...parsed,
14563:       account: 'Cash',
14564:       type: 'transfer_out',
14565:       amount: parsed.amount
14566:     };
14567:     cashResult = writeCashLedgerCompatibility_(ss, parsedCashOut, rawText, common);
14568:   }
14569: 
14570:   var transferResult = {
14571:     status: 'written',
14572:     writtenTab: AIRO_CONFIG.tabs.accountLedger,
```

#### ledger_write L14567

```javascript
14559:     cashResult = writeCashLedgerCompatibility_(ss, parsedCashIn, rawText, common);
14560:   } else if (transfer.sourceAccount === 'Cash') {
14561:     var parsedCashOut = {
14562:       ...parsed,
14563:       account: 'Cash',
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
```

#### source_account L14577

```javascript
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
```

#### target_account L14578

```javascript
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
```

#### ledger_write L14589

```javascript
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
```

#### linked L14594

```javascript
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
14605: 
14606: function airoLiveSchemaVerifyOnly() {
```

#### source_account L14595

```javascript
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
14605: 
14606: function airoLiveSchemaVerifyOnly() {
14607:   const spreadsheetId =
```

## Next

Proceed to Gate C1B source patch only, no deploy.