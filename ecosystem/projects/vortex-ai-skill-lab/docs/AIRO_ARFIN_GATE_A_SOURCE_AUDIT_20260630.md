---
title: AIRO Arfin Gate A Source Audit 2026-06-30
status: PASS_GATE_A_ANCHORS_IDENTIFIED_REQUIREMENT_TERMS_ALREADY_PRESENT_REVIEW_NEEDED
source_sha256: add9d5a538e48ed8cde6049f0632cbb8318c28e7074428ccc00dae7985353b19
head: cfbc12ee20049cadb065ff1b20d92d64729ac9b6
generated_at_commit_time: 2026-06-30T22:52:16
---

> Gate A read-only source audit evidence. No source patch, deploy, API call, Gmail read, Telegram send, or workbook edit.

# AIRO Arfin Gate A Source Audit

Generated: `2026-06-30T22:50:15`

## Verdict

```text
RESULT=PASS_GATE_A_ANCHORS_IDENTIFIED_REQUIREMENT_TERMS_ALREADY_PRESENT_REVIEW_NEEDED
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
- HEAD: `cfbc12ee20049cadb065ff1b20d92d64729ac9b6`
- Function count parsed: `693`

## Candidate Anchor Map

| Function | Found | Lines | Callers | Internal calls | Key notes |
|---|---:|---:|---|---|---|
| `tryHandlePendingClarificationReply_` | YES | 789-1151 | `airoOriginalDoPostForSprint7ParserPlan_` | `airoSprint7CategoryContractMissingCategoryHandleReply_, buildAssetGoldAmbiguousClarificationMessage_, buildAssetGoldClarifiedText_, cashClarificationResolvedText_, clearPendingClarification_, creditCardClarificationResolvedText_, debtAmbiguousClarificationResolvedText_, directionClarificationResolvedText_, failOrRetry_, getPendingClarification_, getProp_, makeTxnId_` | `pending:62, internal_transfer:9, balance_readback:3, telegram_reply:11` |
| `reprocessClarifiedTelegramText_` | YES | 558-576 | `tryHandlePendingClarificationReply_` | `doPost, reprocessClarifiedTelegramText_` | `-` |
| `airoSprint7FEmailAnswerMaybeHandleRoute_` | YES | 22823-23165 | `airoOriginalDoPostForSprint7ParserPlan_, doPost` | `airoSprint7CategoryContractBuildSubcategoryPrompt_, airoSprint7CategoryContractGetRegistry_, airoSprint7CategoryContractParseSubcategoryOption_, airoSprint7FBuildEmailPendingDisambiguationMessage_, airoSprint7FBuildFriendlyClarificationMessage_, airoSprint7FEmailAnswerMaybeHandleRoute_, airoSprint7FInferQuestionTypeFromPending_, airoSprint7FParseTelegramPayload_, airoSprint7FSelectPendingEmailCandidate_, airoSprint7FUpsertPendingEmailCandidate_, airoSprint7HResolveToReviewQueueFallback_, json_` | `pending:73, review_queue:9, internal_transfer:2, telegram_reply:10` |
| `airoSprint7FUpdatePendingEmailResolution_` | YES | 22460-22522 | `airoSprint7HResolveToReviewQueueFallback_` | `airoSprint7FEmailLogHeaders_, airoSprint7FEnsureResolutionHeaders_, airoSprint7FUpdatePendingEmailResolution_` | `pending:5` |
| `airoSprint7FUpsertPendingEmailCandidate_` | YES | 22172-22191 | `airoSprint7FEmailAnswerMaybeHandleRoute_, runTask8EmailMultiPendingSelfTestFromEditor` | `airoSprint7FEmailPendingCandidateIdentity_, airoSprint7FLoadPendingEmailCandidateList_, airoSprint7FNormalizePendingEmailCandidate_, airoSprint7FSavePendingEmailCandidateList_, airoSprint7FUpsertPendingEmailCandidate_` | `pending:12` |
| `airoSprint7HApprovalCommandMaybeHandleRoute_` | YES | 24419-24570 | `doPost` | `airoSprint7FParseTelegramPayload_, airoSprint7FSpreadsheet_, airoSprint7HApprovalApprove_, airoSprint7HApprovalCommandMaybeHandleRoute_, airoSprint7HApprovalDetail_, airoSprint7HApprovalFix_, airoSprint7HApprovalList_, airoSprint7HApprovalReject_, airoTask614ApprovalHelp_, airoTask614GetDirectApprovalQueueId_, airoTask614ResolveApprovalArg_, json_` | `approval:29, pending:1, telegram_reply:20` |
| `writeInternalTransferToAccountLedger_` | YES | 14519-14604 | `airoTask9CcSudahNumberMaybeHandleRoute_, airoWriteRoutedCore_` | `makeTxnId_, recordFinanceEventForWriteResult_, writeAccountLedgerMirror_, writeCashLedgerCompatibility_, writeInternalTransferToAccountLedger_` | `internal_transfer:34, idempotency:4` |
| `writeRouted_` | YES | 3820-3849 | `airoOriginalDoPostForSprint7ParserPlan_, airoSprint7CategoryContractMissingCategoryHandleReply_, airoSprint7HApprovalApprove_, failOrRetry_, processReviewQueueApproved, tryHandlePendingClarificationReply_` | `airoTask102RefreshDashboardMetadataAfterWrite_, airoWriteRoutedCore_, writeRouted_` | `-` |
| `writeAccountLedgerPrimary_` | YES | 2890-2967 | `airoWriteRoutedCore_, appendDebtPaymentAndUpdateMaster_` | `findAccountLedgerEntryById_, makeTxnId_, writeAccountLedgerMirror_, writeAccountLedgerPrimary_` | `internal_transfer:9, balance_readback:2, idempotency:9, telegram_reply:5` |
| `findAccountLedgerEntryById_` | YES | 2842-2888 | `writeAccountLedgerPrimary_` | `canonicalKey_, findAccountLedgerEntryById_, findHeader_, getSheetLoose_` | `internal_transfer:2, balance_readback:1, idempotency:2` |
| `getAccountLedgerRowDetails_` | YES | 1163-1186 | `airoBuildFinanceWriteSuccessReply_, airoTask9CcSudahNumberMaybeHandleRoute_` | `getAccountLedgerRowDetails_, getSheetLoose_` | `balance_readback:4` |
| `airoBuildFinanceWriteSuccessReply_` | YES | 1188-1318 | `airoOriginalDoPostForSprint7ParserPlan_` | `airoBuildFinanceWriteSuccessReply_, airoSprint7FFormatRupiah_, canonicalSheetName_, formatBalanceRupiah_, getAccountLedgerRowDetails_` | `internal_transfer:4, balance_readback:27, telegram_reply:1` |

## Critical Missing

- None

## Requirement Existing-Term Check

Funding-source terms already appear in source. Review required before patch.
- L249: `Blu Pocket` — `if (hasAcc("Blu Pocket") && hasAcc("Blu")) {`
- L250: `Blu Pocket` — `routes.push({ source: "Blu Pocket", target: "Blu" });`
- L321: `Blu Pocket` — `if (hasAcc("Blu Pocket") && hasAcc("Blu")) {`
- L322: `Blu Pocket` — `routes.push({ source: "Blu Pocket", target: "Blu" });`
- L348: `Blu Pocket` — `'Contoh manual: transfer ' + amount + ' dari Blu Pocket ke Blu';`
- L4611: `Blu Pocket` — `if (/\bpocket\b/i.test(t)) return 'Blu Pocket';`
- L14301: `Blu Pocket` — `if (v === 'pocket blu' || v === 'blu pocket') return 'Blu Pocket';`
- L14302: `Blu Pocket` — `if (v === 'pocket blu cc' || v === 'blu pocket cc') return 'Blu Pocket CC';`
- L17698: `Blu Pocket` — `lines.push("Total belum disisihkan ke Blu Pocket CC: " + formatBalanceRupiah_(totalPending));`
- L17921: `Blu Pocket` — `// Write to Account Ledger as internal transfer: Blu Pocket -> Blu Pocket CC`
- L17932: `Blu Pocket` — `var ledgerRawText = "transfer " + amountVal + " dr blu pocket ke blu pocket cc";`
- L17933: `Blu Pocket` — `var transferInfo = { sourceAccount: "Blu Pocket", targetAccount: "Blu Pocket CC" };`
- L17960: `Blu Pocket` — `if (vOutAcc !== "Blu Pocket") {`
- L17969: `Blu Pocket` — `} else if (vInAcc !== "Blu Pocket CC") {`
- L18009: `Blu Pocket` — `successLines.push("Transfer: Blu Pocket → Blu Pocket CC");`
- L18015: `Blu Pocket` — `successLines.push("Saldo Blu Pocket sekarang: " + formatBalanceRupiah_(sourceDetails.balance));`
- L18016: `Blu Pocket` — `successLines.push("Saldo Blu Pocket CC sekarang: " + formatBalanceRupiah_(targetDetails.balance));`
- L18114: `Blu Pocket` — `if (String(regValues[rIdx][2]).trim() === "Blu Pocket CC") {`
- L18120: `Blu Pocket` — `regSheet.appendRow(['TRUE', 'blu_pocket_cc', 'Blu Pocket CC', 'Blu', 'bank', 'Blu', 'pocket cc', 'Blu', '#4CD2FF', 'FALSE', 'TRUE', 'FALSE', 'Blu BCA Pocket CC account']);`
- L18141: `Blu Pocket` — `if ((row73Account === "" || row73Account === "null" || row73Account === "undefined") && row73In === 24000 && row73Type === "transfer_in" && row73Desc.indexOf("transfer 24000 dr blu pocket ke blu pocket cc") !== -1) {`

## Discovered Function Groups

### approval_route_candidates

- `airoOriginalDoPostForSprint7ParserPlan_` L1322-2597 (1276 lines)
- `normalizeValueForValidation_` L3989-4077 (89 lines)
- `processReviewQueueApproved` L4811-4930 (120 lines)
- `processReviewQueueApprovedOnEdit` L4932-4934 (3 lines)
- `setupReviewQueueAutoProcessor` L4936-4955 (20 lines)
- `routeReviewApprovedTab_` L4958-5004 (47 lines)
- `airoBuildSprint6DashboardFinalPlanReply_` L9824-9872 (49 lines)
- `airoSprint7SourceAllowlistDesign_` L16289-16449 (161 lines)
- `airoSprint7SourceAllowlistReadbackText_` L16451-16543 (93 lines)
- `airoSprint7SourceAllowlistMaybeHandleRoute_` L16655-16681 (27 lines)
- `airoSprint7GmailLabelFilterDesign_` L16695-16873 (179 lines)
- `airoTask611SmokeAdminCommandMaybeHandleRoute_` L17116-17259 (144 lines)
- `doPost` L17404-17525 (122 lines)
- `airoSprint7BEmailSandboxFixturesContract_` L18895-18992 (98 lines)
- `airoSprint7EReadOnlyGmailPilotStatusContract_` L19260-19331 (72 lines)
- `airoSprint7EReadOnlyGmailPilotStatusReplyText_` L19333-19374 (42 lines)
- `airoSprint7EReadOnlyGmailPilotStatusMaybeHandleRoute_` L19376-19434 (59 lines)
- `airoSprint7EOneShotReadOnlyPilotContract_` L19438-19468 (31 lines)
- `airoSprint7FContract_` L20020-20043 (24 lines)
- `airoSprint7FStatus_` L20045-20075 (31 lines)
- `airoSprint7FBuildStatusReply_` L20077-20118 (42 lines)
- `runSprint7FManualDryRunPollerFromEditor` L20155-20306 (152 lines)
- `runSprint7FBManualDryRunPollerWithTransientBodyFromEditor` L20366-20446 (81 lines)
- `runSprint7FSendOneClarificationPreviewFromEditor` L20566-20674 (109 lines)
- `runSprint7FSendOneClarificationAndLogPendingFromEditor` L20915-21008 (94 lines)
- `runSprint7GManualWritePilotFromEditor` L21123-21364 (242 lines)
- `runSprint7GTask5TargetedReadbackVerifierFromEditor` L21383-21639 (257 lines)
- `airoSprint7FDBuildNoWriteRoutePreview_` L22715-22775 (61 lines)
- `airoSprint7HResolveToReviewQueueFallback_` L23249-23526 (278 lines)
- `airoTask614DirectApprovalPropertyKey_` L23690-23692 (3 lines)

### pending_candidate_candidates

- `savePendingClarification_` L50-59 (10 lines)
- `tryHandlePendingClarificationReply_` L789-1151 (363 lines)
- `failOrRetry_` L793-844 (52 lines)
- `airoOriginalDoPostForSprint7ParserPlan_` L1322-2597 (1276 lines)
- `airoSprint6BAlertEnginePlan_` L8398-9110 (713 lines)
- `airoSprint7FBuildStatusReply_` L20077-20118 (42 lines)
- `airoSprint7FLogPendingCandidate_` L20799-20855 (57 lines)
- `airoSprint7FSavePendingPointer_` L20879-20913 (35 lines)
- `runSprint7FSendOneClarificationAndLogPendingFromEditor` L20915-21008 (94 lines)
- `runTask8EmailMultiPendingSelfTestFromEditor` L21046-21121 (76 lines)
- `airoSprint7FEmailPendingCandidateIdentity_` L22093-22104 (12 lines)
- `airoSprint7FNormalizePendingEmailCandidate_` L22106-22117 (12 lines)
- `airoSprint7FLoadPendingEmailCandidateList_` L22119-22139 (21 lines)
- `airoSprint7FSavePendingEmailCandidateList_` L22141-22170 (30 lines)
- `airoSprint7FUpsertPendingEmailCandidate_` L22172-22191 (20 lines)
- `airoSprint7FRemovePendingEmailCandidate_` L22193-22211 (19 lines)
- `airoSprint7FHasPendingEmailCandidate_` L22283-22293 (11 lines)
- `airoSprint7FSelectPendingEmailCandidate_` L22314-22354 (41 lines)
- `airoSprint7FLoadPendingEmailCandidate_` L22372-22386 (15 lines)
- `airoSprint7FResolveAnswerLabel_` L22388-22437 (50 lines)
- `airoSprint7FUpdatePendingEmailResolution_` L22460-22522 (63 lines)
- `airoSprint7FDNormalizeSourceChannel_` L22528-22538 (11 lines)
- `airoSprint7FDPrimaryAccount_` L22540-22552 (13 lines)
- `airoSprint7FDInferAction_` L22579-22670 (92 lines)
- `airoSprint7FDBuildNoWriteRoutePreview_` L22715-22775 (61 lines)
- `airoSprint7FEmailAnswerMaybeHandleRoute_` L22823-23165 (343 lines)
- `airoC3GValidateEmailWritebackCandidate_` L23230-23246 (17 lines)
- `airoSprint7HResolveToReviewQueueFallback_` L23249-23526 (278 lines)
- `airoSprint7CategoryContractMissingCategoryHandleReply_` L25299-25560 (262 lines)
- `airoSprint7HScheduledGmailPoller_` L27016-27313 (298 lines)

### review_queue_candidates

- `buildMissingCategoryClarificationMessage_` L701-721 (21 lines)
- `tryHandlePendingClarificationReply_` L789-1151 (363 lines)
- `failOrRetry_` L793-844 (52 lines)
- `airoOriginalDoPostForSprint7ParserPlan_` L1322-2597 (1276 lines)
- `styleReviewQueueSheet_` L3290-3341 (52 lines)
- `airoStyleBackendTabs_` L3387-3429 (43 lines)
- `writeAssetSafely_` L3851-3929 (79 lines)
- `normalizeValueForValidation_` L3989-4077 (89 lines)
- `normalizeDataForTab_` L4079-4091 (13 lines)
- `fieldForHeader_` L4309-4381 (73 lines)
- `routePlannedTab_` L4383-4431 (49 lines)
- `reviewIssueReasonForParsed_` L4433-4468 (36 lines)
- `parseFinanceText_` L4470-4531 (62 lines)
- `processReviewQueueApproved` L4811-4930 (120 lines)
- `processReviewQueueApprovedOnEdit` L4932-4934 (3 lines)
- `setupReviewQueueAutoProcessor` L4936-4955 (20 lines)
- `routeReviewApprovedTab_` L4958-5004 (47 lines)
- `reviewHeaderMap_` L5005-5014 (10 lines)
- `getReviewValue_` L5016-5025 (10 lines)
- `setReviewValue_` L5027-5037 (11 lines)
- `normalizeReviewAmount_` L5039-5043 (5 lines)
- `normalizeReviewAccount_` L5045-5058 (14 lines)
- `extendReviewQueueSchema_` L5060-5120 (61 lines)
- `runTask3AReviewQueueSchemaExtensionFromEditor` L5122-5126 (5 lines)
- `runTask3AReviewQueueSchemaVerifierFromEditor` L5128-5163 (36 lines)
- `refreshCashLedgerMaintenance` L5165-5235 (71 lines)
- `refreshCashReportingFormulas` L5269-5324 (56 lines)
- `refreshCashMonthlyReviewFormulas` L5326-5328 (3 lines)
- `dashboardLayoutReadOnlyAudit_` L6740-6800 (61 lines)
- `airoSprint7EmailSourceContractGuard_` L7163-7235 (73 lines)

### internal_transfer_candidates

- `canAskCashAmbiguousClarification_` L140-156 (17 lines)
- `canAskDirectionAmbiguousClarification_` L197-213 (17 lines)
- `canAskTransferIncompleteClarification_` L303-312 (10 lines)
- `airoWriteRoutedCore_` L3536-3818 (283 lines)
- `savingsEventType_` L3962-3978 (17 lines)
- `parseFinanceText_` L4470-4531 (62 lines)
- `airoSprint6DashboardFinalPlan_` L9708-9822 (115 lines)
- `handleSpecialFinanceCommand_` L10731-12006 (1276 lines)
- `writeCreditCardSafely_` L12334-12387 (54 lines)
- `markCreditCardPocketBluTransfer_` L12670-12874 (205 lines)
- `detectInternalTransfer_` L14345-14381 (37 lines)
- `writeInternalTransferToAccountLedger_` L14519-14604 (86 lines)
- `airoTask9CcSudahNumberMaybeHandleRoute_` L17742-18054 (313 lines)
- `airoSprint7EmailDryRunRouterContract_` L18712-18797 (86 lines)
- `airoSprint7BEmailSandboxFixturesContract_` L18895-18992 (98 lines)
- `airoSprint7BFixtureMatrixContract_` L19094-19152 (59 lines)
- `airoSprint7FDInferAction_` L22579-22670 (92 lines)
- `airoSprint7FDEventTypeForAction_` L22672-22684 (13 lines)
- `airoSprint7FDDomainForAction_` L22686-22691 (6 lines)
- `airoSprint7FDTargetTabsForAction_` L22693-22699 (7 lines)
- `airoSprint7FDBuildNoWriteRoutePreview_` L22715-22775 (61 lines)
- `runTask8TransferRegistrySelfTestFromEditor` L29518-29580 (63 lines)

### balance_readback_candidates

- `isClearlyNonFinanceOrTooUnclear_` L73-90 (18 lines)
- `normalizeCashClarificationAnswer_` L128-138 (11 lines)
- `canAskCashAmbiguousClarification_` L140-156 (17 lines)
- `buildCashAmbiguousClarificationMessage_` L158-169 (12 lines)
- `cashClarificationResolvedText_` L171-183 (13 lines)
- `normalizeDirectionClarificationAnswer_` L185-195 (11 lines)
- `buildDirectionAmbiguousClarificationMessage_` L215-226 (12 lines)
- `isSprint0ANonFinanceSafeReject_` L614-648 (35 lines)
- `tryHandlePendingClarificationReply_` L789-1151 (363 lines)
- `formatBalanceRupiah_` L1153-1161 (9 lines)
- `getAccountLedgerRowDetails_` L1163-1186 (24 lines)
- `airoBuildFinanceWriteSuccessReply_` L1188-1318 (131 lines)
- `airoOriginalDoPostForSprint7ParserPlan_` L1322-2597 (1276 lines)
- `writeAccountLedgerPrimary_` L2890-2967 (78 lines)
- `writeAccountLedgerMirror_` L3117-3172 (56 lines)
- `ensureAccountLedgerSheet_` L3179-3214 (36 lines)
- `stringifyReadbackCell_` L4102-4105 (4 lines)
- `buildReadbackText_` L4107-4109 (3 lines)
- `verifyAppendWrite_` L4111-4123 (13 lines)
- `appendByHeader_` L4125-4172 (48 lines)
- `airoSprint6BDuplicateSuppressionRunner_` L7828-7899 (72 lines)
- `airoSprint6BCooldownSuppressionReadback_` L7938-8001 (64 lines)
- `airoBuildSprint6BCooldownSuppressionReadbackReply_` L8003-8039 (37 lines)
- `airoSprint6BAckAlert_` L8041-8084 (44 lines)
- `airoSprint6BAlertEnginePlan_` L8398-9110 (713 lines)
- `airoSprint6DashboardFinalReadback_` L9160-9398 (239 lines)
- `airoBuildSprint6DashboardFinalReadbackReply_` L9400-9457 (58 lines)
- `airoSprint6DashboardFinalBuild_` L9459-9663 (205 lines)
- `airoBuildSprint6DashboardFinalBuildReply_` L9665-9680 (16 lines)
- `airoSprint6DashboardFinalPlan_` L9708-9822 (115 lines)

### success_reply_candidates

- `airoBuildFinanceWriteSuccessReply_` L1188-1318 (131 lines)
- `airoOriginalDoPostForSprint7ParserPlan_` L1322-2597 (1276 lines)
- `writeAccountLedgerPrimary_` L2890-2967 (78 lines)
- `stringifyReadbackCell_` L4102-4105 (4 lines)
- `buildReadbackText_` L4107-4109 (3 lines)
- `verifyAppendWrite_` L4111-4123 (13 lines)
- `appendByHeader_` L4125-4172 (48 lines)
- `airoBuildSprint6EnsureAuditLogReply_` L6884-6894 (11 lines)
- `airoBuildSprint7EmailSourceContractGuardReply_` L7237-7278 (42 lines)
- `airoBuildSprint6BTriggerLifecycleReply_` L7794-7826 (33 lines)
- `airoSprint6BDuplicateSuppressionRunner_` L7828-7899 (72 lines)
- `airoBuildSprint6BDuplicateSuppressionRunnerReply_` L7901-7936 (36 lines)
- `airoSprint6BCooldownSuppressionReadback_` L7938-8001 (64 lines)
- `airoBuildSprint6BCooldownSuppressionReadbackReply_` L8003-8039 (37 lines)
- `airoSprint6BAckAlert_` L8041-8084 (44 lines)
- `airoBuildSprint6BAckAlertReply_` L8086-8096 (11 lines)
- `airoBuildSprint6BControlledSendTestReply_` L8180-8193 (14 lines)
- `airoBuildSprint6BAlertRunnerSafeModeReply_` L8365-8396 (32 lines)
- `airoBuildSprint6BAlertEnginePlanReply_` L9112-9158 (47 lines)
- `airoSprint6DashboardFinalReadback_` L9160-9398 (239 lines)
- `airoBuildSprint6DashboardFinalReadbackReply_` L9400-9457 (58 lines)
- `airoSprint6DashboardFinalBuild_` L9459-9663 (205 lines)
- `airoBuildSprint6DashboardFinalBuildReply_` L9665-9680 (16 lines)
- `airoBuildSprint6DashboardFinalPlanReply_` L9824-9872 (49 lines)
- `airoBuildSprint5ReconciliationReply_` L10487-10554 (68 lines)
- `airoBuildFindSmokeReply_` L10680-10729 (50 lines)
- `handleSpecialFinanceCommand_` L10731-12006 (1276 lines)
- `appendCreditCardPurchase_` L12616-12668 (53 lines)
- `appendDebtPaymentAndUpdateMaster_` L13082-13353 (272 lines)
- `airoSprint7FixtureMatrixReadbackText_` L15716-15784 (69 lines)

### idempotency_candidates

- `canAskDebtAmbiguousClarification_` L457-476 (20 lines)
- `debtAmbiguousClarificationResolvedText_` L578-612 (35 lines)
- `airoOriginalDoPostForSprint7ParserPlan_` L1322-2597 (1276 lines)
- `getFinanceEventsHeaders_` L2659-2678 (20 lines)
- `financeEventPayloadJson_` L2714-2731 (18 lines)
- `buildFinanceEvent_` L2733-2753 (21 lines)
- `writeCashLedger_` L2783-2818 (36 lines)
- `withAccountLedgerPrimaryLock_` L2825-2840 (16 lines)
- `findAccountLedgerEntryById_` L2842-2888 (47 lines)
- `writeAccountLedgerPrimary_` L2890-2967 (78 lines)
- `findProjectionRowByLedgerEntryId_` L2969-3059 (91 lines)
- `writeAccountLedgerMirror_` L3117-3172 (56 lines)
- `ensureAccountLedgerSheet_` L3179-3214 (36 lines)
- `recordFinanceEventForWriteResult_` L3481-3534 (54 lines)
- `airoWriteRoutedCore_` L3536-3818 (283 lines)
- `writeAssetSafely_` L3851-3929 (79 lines)
- `appendToAssetSection_` L3931-3960 (30 lines)
- `buildRowByHeader_` L4219-4299 (81 lines)
- `fieldForHeader_` L4309-4381 (73 lines)
- `processReviewQueueApproved` L4811-4930 (120 lines)
- `extendReviewQueueSchema_` L5060-5120 (61 lines)
- `runTask3AReviewQueueSchemaVerifierFromEditor` L5128-5163 (36 lines)
- `appendGoldAssetRow_` L5628-5723 (96 lines)
- `setupDashboardNetWorthPanel` L6564-6679 (116 lines)
- `cleanupDuplicateNetWorthPanels` L6681-6734 (54 lines)
- `airoSprint7EmailSourceContractGuard_` L7163-7235 (73 lines)
- `airoBuildSprint7EmailSourceContractGuardReply_` L7237-7278 (42 lines)
- `airoSprint6BTriggerHandlerSafe_` L7280-7306 (27 lines)
- `airoSprint6BGuardedTriggerStatus_` L7359-7376 (18 lines)
- `airoSprint6BInstallGuardedTrigger_` L7378-7428 (51 lines)

## Gate A Next Decision

Use this audit to choose exact patch anchors. Do not patch until owner approves Gate B patch design.