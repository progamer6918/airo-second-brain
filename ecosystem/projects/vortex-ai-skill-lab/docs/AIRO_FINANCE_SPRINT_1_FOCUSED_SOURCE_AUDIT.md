# AIRO Finance — Sprint 1 Focused Source Audit

Status: FOCUSED AUDIT  
Sprint: Sprint 1 — Account Ledger Hardening  
Generated at: 2026-05-24 12:42:35  
Runtime scope: Source/test audit only; no runtime patch in this micro-step  
Canonical source: docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md

## 1. Purpose

This document locates the most likely runtime writer, route, dry-run, and test files needed for Sprint 1 Account Ledger Hardening.

Sprint 1 must not patch runtime behavior until the exact writer/route/test surface is mapped.

## 2. Top Candidate Files

| Rank | File | Signal Score |
|---:|---|---:|
| 1 | `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs` | 1563 |
| 2 | `scripts/personal-workflow/airo_sheets_sync_dry_run.py` | 124 |
| 3 | `scripts/personal-workflow/airo_cash_ledger_planner.py` | 117 |
| 4 | `scripts/personal-workflow/airo_transaction_persistence.py` | 105 |
| 5 | `scripts/personal-workflow/airo_finance_sheet_v12_regression.py` | 95 |
| 6 | `scripts/personal-workflow/airo_full_auto_sheets_sync.py` | 65 |
| 7 | `scripts/personal-workflow/airo_review_queue_planner.py` | 56 |
| 8 | `scripts/personal-workflow/airo_cicilan_rumah_planner.py` | 51 |
| 9 | `scripts/personal-workflow/airo_hutang_planner.py` | 46 |
| 10 | `scripts/personal-workflow/airo_finance_sheet_v12_mapper_preview.py` | 39 |
| 11 | `scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs` | 39 |
| 12 | `scripts/personal-workflow/runtime-tests/airo_finance_clarification_regression.sh` | 38 |
| 13 | `tests/personal-workflow/test_airo_cash_ledger_planner.py` | 36 |
| 14 | `scripts/personal-workflow/airo_asset_event_planner.py` | 35 |
| 15 | `tests/personal-workflow/test_airo_full_auto_sheets_sync_v13_write_path.py` | 23 |
| 16 | `tests/personal-workflow/test_airo_cicilan_rumah_planner.py` | 19 |
| 17 | `scripts/personal-workflow/airo_regression_smoke.sh` | 18 |
| 18 | `scripts/personal-workflow/apps-script/airo_credit_card_billing_cycle_v0_8.gs` | 16 |
| 19 | `scripts/personal-workflow/airo_finance_sheet_v12_status.py` | 15 |
| 20 | `scripts/personal-workflow/airo_transaction_executor.py` | 14 |
| 21 | `tests/personal-workflow/test_airo_finance_sheet_v12_mapper_preview.py` | 13 |
| 22 | `tests/personal-workflow/test_airo_gateway_finance_contract.py` | 12 |
| 23 | `scripts/personal-workflow/airo_approval_review.py` | 11 |
| 24 | `tests/personal-workflow/test_airo_finance_language_contract.py` | 11 |
| 25 | `scripts/personal-workflow/airo_approval_queue.py` | 10 |
| 26 | `tests/personal-workflow/test_airo_asset_event_planner.py` | 10 |
| 27 | `scripts/personal-workflow/airo_credit_card_mirror_planner.py` | 9 |
| 28 | `scripts/personal-workflow/airo_queue_executor.py` | 9 |
| 29 | `scripts/personal-workflow/airo_sheets_sync_write_preview.py` | 9 |
| 30 | `scripts/personal_workflow_db_smoke.py` | 9 |
| 31 | `tests/personal-workflow/test_airo_finance_sheet_v12_status.py` | 9 |
| 32 | `scripts/personal-workflow/airo_action_gate.py` | 8 |
| 33 | `scripts/personal-workflow/airo_transaction_proposal.py` | 8 |
| 34 | `scripts/personal-workflow/airo_executor_recommend.py` | 7 |
| 35 | `scripts/personal-workflow/airo_account_aliases.py` | 6 |
| 36 | `scripts/personal-workflow/airoctl.py` | 6 |
| 37 | `scripts/personal-workflow/apps-script/airo_finance_sheet_key_exporter_v0_3.gs` | 6 |
| 38 | `scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs` | 6 |
| 39 | `tests/personal-workflow/test_airo_finance_contract_v1_1.py` | 6 |
| 40 | `tests/personal-workflow/test_airo_review_queue_planner.py` | 6 |

## 3. Focused Pattern Findings

### sheet access / append

#### Term: getSheetByName

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2543: const exact = ss.getSheetByName(wanted);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5732: let sheet = ss.getSheetByName(name);`
- `scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:27: const txSheet = ss.getSheetByName('💸 Transactions');`
- `scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:28: const ccSheet = ss.getSheetByName('💳 Credit Card');`
- `scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:29: const syncLog = ss.getSheetByName('🔄 Sync Log');`
- `scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:122: const sheet = ss.getSheetByName('⚙️ Settings');`
- `scripts/personal-workflow/apps-script/airo_credit_card_billing_cycle_v0_8.gs:14: const sheet = ss.getSheetByName('💳 Credit Card');`
- `scripts/personal-workflow/apps-script/airo_credit_card_billing_cycle_v0_8.gs:83: const sheet = ss.getSheetByName('💳 Credit Card');`
- `scripts/personal-workflow/apps-script/airo_finance_sheet_key_exporter_v0_3.gs:40: const sheet = ss.getSheetByName(tabName);`
- `scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs:28: const syncLog = ss.getSheetByName('🔄 Sync Log');`
- `scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs:81: const sheet = ss.getSheetByName('⚙️ Settings');`

#### Term: appendRow

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5689: sheet.appendRow([`
- `scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:65: txSheet.appendRow(txValues);`
- `scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:72: ccSheet.appendRow(ccValues);`
- `scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:205: sheet.appendRow([`
- `scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs:62: syncLog.appendRow(row);`

#### Term: setValues

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1590: .setValues([ACCOUNT_LEDGER_HEADERS]);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1603: .setValues([ACCOUNT_LEDGER_HEADERS]);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1805: sheet.getRange(targetRow, spec.startCol, 1, values.length).setValues([values]);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1989: created.getRange(1, 1, 1, headers.length).setValues([headers]);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1991: created.getRange(2, 1, 1, headers.length).setValues([createdValues]);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2014: sheet.getRange(targetRow, 1, 1, values.length).setValues([values]);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:3376: sheet.getRange(targetRow, 1, 1, width).setValues([row.slice(0, width)]);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5736: sheet.getRange(1, 1, 1, 6).setValues([[`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6166: sheet.getRange(targetRow, 1, 1, row.length).setValues([row]);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6511: sheet.getRange(targetRow, 1, 1, row.length).setValues([row]);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6584: range.setValues(fixed);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6660: descRange.setValues(statusValues);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6664: statusRange.setValues(descValues);`
- `scripts/personal-workflow/apps-script/airo_credit_card_billing_cycle_v0_8.gs:51: sheet.getRange('J3:O3').setValues([billingHeaders]);`

#### Term: getRange

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1453: const headers = sheet.getRange(1, 1, 1, lastCol).getDisplayValues()[0];`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1469: if (inCol) sheet.getRange(rowNumber, inCol).setValue(inflow ? amount : '');`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1470: if (outCol) sheet.getRange(rowNumber, outCol).setValue(inflow ? '' : amount);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1563: sheet.getRange(r, 6).setFormula(formula);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1589: sheet.getRange(1, 1, 1, ACCOUNT_LEDGER_HEADERS.length)`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1597: var existingHeaders = sheet.getRange(1, 1, 1, lastCol).getValues()[0]`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1602: sheet.getRange(1, 1, 1, ACCOUNT_LEDGER_HEADERS.length)`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1615: var headerRange = sheet.getRange(1, 1, 1, 13);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1630: sheet.getRange('B:B').setNumberFormat('yyyy-mm-dd');`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1631: sheet.getRange('D:F').setNumberFormat('"Rp" #,##0');`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1656: var account = sheet.getRange(row, 3).getDisplayValue();`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1658: sheet.getRange(row, 1, 1, 13).setFontColor(color);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1667: var values = sheet.getRange(2, 3, lastRow - 1, 1).getDisplayValues();`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1670: sheet.getRange(i + 2, 1, 1, 13).setFontColor(color);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1805: sheet.getRange(targetRow, spec.startCol, 1, values.length).setValues([values]);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1834: const range = sheet.getRange(targetRow, startCol, 1, values.length);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1969: const readbackRawValues = sheet.getRange(row, col, 1, values.length).getValues()[0];`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1989: created.getRange(1, 1, 1, headers.length).setValues([headers]);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1991: created.getRange(2, 1, 1, headers.length).setValues([createdValues]);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2014: sheet.getRange(targetRow, 1, 1, values.length).setValues([values]);`

#### Term: Account Ledger

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:20: accountLedger: '📒 Account Ledger',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1513: * Mirrors cash movement to the Account Ledger tab.`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1573: * Ensures the 📒 Account Ledger tab exists with the correct headers.`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2944: `ARRAYFORMULA(IFERROR(TEXT('📒 Account Ledger'!B:B;"yyyy-mm");LEFT(TO_TEXT('📒 Account Ledger'!B:B);7)))`;`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2947: `REGEXMATCH('📒 Account Ledger'!C:C;"^Cash( Umum\| Bensin)?$")`;`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2950: `=IFERROR(SUM(FILTER('📒 Account Ledger'!D:D;${accountLedgerCashAccountFilterFormula};${accountLedgerMonthKeyFormula}=TO_TEXT($B$2)));0)`;`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2953: `=IFERROR(SUM(FILTER('📒 Account Ledger'!E:E;${accountLedgerCashAccountFilterFormula};${accountLedgerMonthKeyFormula}=TO_TEXT($B$2)));0)`;`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2959: `=IFERROR("💵 Cash Aktif"&CHAR(10)&TEXT((SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Bensin"))-(SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Bensin"));"Rp #,##0");"💵 Cash Aktif"&CHAR(10)&"— catat dulu —")`;`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:4258: dashboard.getRange('D17').setFormula(`=IFERROR(((SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Bensin"))-(SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Bensin")))+'🥇 Aset'!B17+'🥇 Aset'!B18;0)`);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5242: 'Account Ledger Cash inflows recent/top:\n' +`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5249: 'Buka Account Ledger: ' + link`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5421: 'Account Ledger Cash in: Rp' + accountIn + '\n' +`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5422: 'Account Ledger Cash out: Rp' + accountOut + '\n' +`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5423: 'Account Ledger Cash net: Rp' + accountNet + '\n\n' +`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5426: 'Buka Account Ledger: ' + link`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5474: monthly_b6_uses_account_ledger: monthlyB6.indexOf('Account Ledger') >= 0,`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5475: monthly_e6_uses_account_ledger: monthlyE6.indexOf('Account Ledger') >= 0,`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5477: dashboard_d17_uses_account_ledger: dashboardD17.indexOf('Account Ledger') >= 0`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5485: 'Monthly B6 pakai Account Ledger: ' + result.monthly_b6_uses_account_ledger + '\n' +`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5486: 'Monthly E6 pakai Account Ledger: ' + result.monthly_e6_uses_account_ledger + '\n' +`

### account ledger schema

#### Term: entry_id

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1485: entry_id: entryId,`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1539: entry_id: entryId,`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1579: 'entry_id', 'date', 'account', 'amount_in', 'amount_out',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2087: if (headerKey === 'entry_id' \|\| headerKey.includes('entry_id')) {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2088: return data.entry_id \|\| data.linked_txn_id \|\| '';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6107: normalized.includes('cc_entry_id') &&`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6146: cc_entry_id: common.linked_txn_id \|\| makeTxnId_({}, rawText),`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6817: * Safe to run multiple times: it is append-only, performs strict deduplication based on entry_id`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6910: var entryId = getFieldValue_(rowObj, 'entry_id', cashHeaders) \|\| getFieldValue_(rowObj, 'linked_txn_id', cashHeaders);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6960: var entryId = getFieldValue_(rowObj, 'entry_id', accountHeaders) \|\| getFieldValue_(rowObj, 'linked_txn_id', accountHeaders);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6972: var cashEntryId = getFieldValue_(cashRow, 'entry_id', cashHeaders) \|\| getFieldValue_(cashRow, 'linked_txn_id', cashHeaders);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7024: entry_id: entryId,`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7169: var entryIdVal = String(rowObj['entry_id'] \|\| '').trim().toLowerCase();`
- `scripts/personal-workflow/airo_sheets_sync_dry_run.py:382: "cc_entry_id": f"cc_{txid}",`
- `scripts/personal-workflow/airo_cash_ledger_planner.py:157: entry_id = cash_id_for(raw_text, operation, source)`
- `scripts/personal-workflow/airo_cash_ledger_planner.py:169: "cash_id": entry_id,`
- `scripts/personal-workflow/airo_cash_ledger_planner.py:170: "duplicate_key": target_tab + ":" + entry_id,`
- `scripts/personal-workflow/airo_full_auto_sheets_sync.py:43: "cc_entry_id", "date", "merchant_app", "amount", "description",`
- `scripts/personal-workflow/airo_full_auto_sheets_sync.py:147: V13_CASH_ENTRY_HEADERS = ["entry_id","session_id","date","description","category","amount","direction","balance_after","source","sync_hash","notes"]`
- `scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:45: const ccHeaders = ["cc_entry_id", "date", "merchant_app", "amount", "description", "status_pocket_blu", "transferred_at", "linked_txn_id", "notes", "billing_cycle_id", "billing_start", "billing_end", "statement_month", "due_date", "is_statement_locked"];`

#### Term: amount_in

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1467: const inCol = findCashLedgerExactHeaderCol_(sheet, 'amount_in');`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1498: amount_in: cashInflow ? parsed.amount : '',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1542: amount_in: isInflow ? amount : '',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1579: 'entry_id', 'date', 'account', 'amount_in', 'amount_out',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2129: headerKey === 'amount_in' \|\|`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2130: headerKey.includes('amount_in') \|\|`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2138: return cashInflow ? (data.amount_in \|\| data.amount \|\| '') : (data.amount_in ?? '');`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2174: // Important: check amount_in / amount_out before generic amount,`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2177: h === 'amount_in' \|\|`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2178: h.includes('amount_in') \|\|`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2186: return 'amount_in';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2879: sheet.getRange(r, 17).setValue(amount);         // amount_in`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2882: sheet.getRange(r, 17).clearContent();           // amount_in`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5075: const cashInCol = findColumn_(cashInfo, ['amount_in', 'cash_in', 'nominal_masuk', 'masuk'], 17);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5077: const accountInCol = findColumn_(accountInfo, ['amount_in', 'cash_in', 'nominal_masuk', 'masuk'], 4);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5158: const cashInCol = findColumn_(cashInfo, ['amount_in', 'cash_in', 'nominal_masuk', 'masuk'], 17);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5181: const accountInCol = findColumn_(accountInfo, ['amount_in', 'cash_in', 'nominal_masuk', 'masuk'], 4);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5352: const cashInCol = findColumn_(cashInfo, ['amount_in', 'cash_in', 'nominal_masuk', 'masuk'], 17);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5355: const accountInCol = findColumn_(accountInfo, ['amount_in', 'cash_in', 'nominal_masuk', 'masuk'], 4);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6858: return f === 'amount' \|\| f === 'amount_in' \|\| f === 'amount_out' \|\| canonicalKey_(h) === 'amount';`

#### Term: amount_out

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1468: const outCol = findCashLedgerExactHeaderCol_(sheet, 'amount_out');`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1499: amount_out: cashInflow ? '' : parsed.amount,`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1543: amount_out: isInflow ? '' : amount,`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1579: 'entry_id', 'date', 'account', 'amount_in', 'amount_out',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2116: headerKey === 'amount_out' \|\|`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2117: headerKey.includes('amount_out') \|\|`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2125: return cashInflow ? '' : (data.amount_out ?? data.amount ?? '');`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2174: // Important: check amount_in / amount_out before generic amount,`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2175: // otherwise amount_out may be filled as expense for cash inflow rows.`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2190: h === 'amount_out' \|\|`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2191: h.includes('amount_out') \|\|`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2199: return 'amount_out';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2878: sheet.getRange(r, 16).clearContent();           // amount_out`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2881: sheet.getRange(r, 16).setValue(amount);         // amount_out`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5074: const cashOutCol = findColumn_(cashInfo, ['amount_out', 'cash_out', 'nominal_keluar', 'keluar'], 16);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5078: const accountOutCol = findColumn_(accountInfo, ['amount_out', 'cash_out', 'nominal_keluar', 'keluar'], 5);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5351: const cashOutCol = findColumn_(cashInfo, ['amount_out', 'cash_out', 'nominal_keluar', 'keluar'], 16);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5356: const accountOutCol = findColumn_(accountInfo, ['amount_out', 'cash_out', 'nominal_keluar', 'keluar'], 5);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6858: return f === 'amount' \|\| f === 'amount_in' \|\| f === 'amount_out' \|\| canonicalKey_(h) === 'amount';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6880: return canonicalKey_(h) === 'amount_out';`

#### Term: balance

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:189: if (/^(d\|4)$/i.test(t) \|\| /\b(saldo\|balance\|tercatat\|awal\|akhir)\b/i.test(t)) return 'balance';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1514: * Balance is intentionally left blank for Google Sheet formulas.`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1544: balance: '',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1580: 'balance', 'type', 'category', 'description', 'raw_text',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5269: if (/^admin\s+(audit\|check\|cek)\s+cash\s+(parity\|balance\|total\|ledger)/i.test(text)) {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6818: * and key properties, and populates balance formulas dynamically without overwriting existing data.`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7029: balance: '',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7042: // Set formula balance`
- `scripts/personal-workflow/airo_finance_sheet_v12_regression.py:130: checks.append(check(hutang["normalized"]["balance_after"] == 14000000, "hutang remaining balance preview works"))`
- `scripts/personal-workflow/airo_full_auto_sheets_sync.py:147: V13_CASH_ENTRY_HEADERS = ["entry_id","session_id","date","description","category","amount","direction","balance_after","source","sync_hash","notes"]`
- `scripts/personal-workflow/airo_full_auto_sheets_sync.py:149: V13_HUTANG_HEADERS = ["payment_id","date","debt_id","creditor","amount","account","balance_before","balance_after","source","sync_hash","notes"]`
- `scripts/personal-workflow/airo_full_auto_sheets_sync.py:173: "account", "balance_before", "balance_after", "status", "notes",`
- `scripts/personal-workflow/airo_hutang_planner.py:23: "balance": 15000000,`
- `scripts/personal-workflow/airo_hutang_planner.py:28: "balance": 5000000,`
- `scripts/personal-workflow/airo_hutang_planner.py:33: "balance": 5000000,`
- `scripts/personal-workflow/airo_hutang_planner.py:136: balance_before = int(debt_data["balance"]) if debt_data else None`
- `scripts/personal-workflow/airo_hutang_planner.py:137: balance_after = None`
- `scripts/personal-workflow/airo_hutang_planner.py:138: if balance_before is not None and amount is not None:`
- `scripts/personal-workflow/airo_hutang_planner.py:139: balance_after = max(balance_before - amount, 0)`
- `scripts/personal-workflow/airo_hutang_planner.py:161: "balance_before": balance_before,`

#### Term: type

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:444: const type = String((parsed && parsed.type) \|\| '').toLowerCase();`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:447: if (type && type !== 'asset') return false;`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:489: type: 'application/json',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:497: type: 'private'`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:697: if (!pending \|\| !pending.type) return null;`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:730: clarification_type: pending.type,`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:746: if (pending.type === 'missing_amount_account') {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:773: if (pending.type === 'cc_ambiguous') {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:849: if (pending.type === 'asset_gold_ambiguous') {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:858: clarification_type: 'asset_gold_ambiguous'`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:873: clarification_type: 'asset_gold_ambiguous'`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:881: if (pending.type === 'debt_ambiguous') {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:933: if (pending.type === 'missing_category') {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:975: if (pending.type === 'transfer_incomplete') {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1005: if (pending.type === 'direction_ambiguous') {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1032: if (pending.type === 'cash_ambiguous') {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1058: if (pending.type === 'missing_account') {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1103: (typeof update !== 'undefined' && update) ? update :`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1104: (typeof payload !== 'undefined' && payload) ? payload :`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1105: (typeof data !== 'undefined' && data) ? data :`

#### Term: category

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:75: const category = String((parsed && parsed.category) \|\| '').trim().toLowerCase();`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:85: (category && category !== 'lainnya');`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:104: const category = String((parsed && parsed.category) \|\| '').trim().toLowerCase();`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:107: if (!category \|\| category === 'lainnya') return false;`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:118: 'Saya tangkap ini transaksi kategori ' + ((parsed && parsed.category) \|\| '-') + ', tapi nominal dan akun belum jelas.\n\n' +`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:144: const category = String((parsed && parsed.category) \|\| '').trim().toLowerCase();`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:152: return !hasClearMeaning \|\| category === 'lainnya';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:199: const category = String((parsed && parsed.category) \|\| '').trim().toLowerCase();`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:203: if (category && category !== 'lainnya') return false;`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:371: function normalizeMissingCategoryClarificationAnswer_(text) {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:443: const category = String((parsed && parsed.category) \|\| '').toLowerCase();`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:446: if (category && category !== 'aset') return false;`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:562: function canAskAmountOnlyMissingCategoryClarification_(parsed, rawText) {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:569: const category = String((parsed && parsed.category) \|\| '').trim().toLowerCase();`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:572: const genericCategory = !category \|\| category === 'lainnya' \|\| category === 'other' \|\| category === 'unknown';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:573: if (!genericCategory) return false;`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:575: // URL/gid/chat transcript noise must not become amount/category evidence.`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:599: function canAskMissingCategoryClarification_(parsed, rawText) {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:603: const category = String((parsed && parsed.category) \|\| '').trim().toLowerCase();`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:607: if (category && category !== 'lainnya') return false;`

#### Term: raw_text

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1422: readback_raw_text: routedResult.readbackRawText \|\| '',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1476: raw_text: rawText,`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1548: raw_text: rawText,`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1580: 'balance', 'type', 'category', 'description', 'raw_text',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1796: raw_text: data.raw_text,`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1814: const text = String(data.raw_text \|\| '').toLowerCase();`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2166: return ['date', 'amount', 'description', 'category', 'account', 'status', 'raw_text', 'type']`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2211: raw_text: ['raw_text', 'raw text', 'pesan', 'message', 'telegram_text', 'input_text'],`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2468: const text = String((data && data.raw_text) \|\| '').toLowerCase();`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2648: const rawText = String(getReviewValue_(row, map, ['raw_text', 'message', 'telegram_text']) \|\| '').trim();`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:3358: // K raw_text`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:3402: const hasRawText = normalized.includes('raw_text');`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:3433: raw_text: ['raw_text', 'pesan', 'message'],`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:3613: normalized.includes('raw_text')`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5159: const cashDescCol = findColumn_(cashInfo, ['description', 'deskripsi', 'raw_text', 'catatan'], 10);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5742: 'raw_text'`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6862: return f === 'description' \|\| f === 'raw_text' \|\| f === 'notes' \|\| canonicalKey_(h) === 'description';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6911: var desc = getFieldValue_(rowObj, 'description', cashHeaders) \|\| getFieldValue_(rowObj, 'raw_text', cashHeaders);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6992: var entryId = cashEntryId \|\| makeTxnId_({}, getFieldValue_(cashRow, 'description', cashHeaders) \|\| getFieldValue_(cashRow, 'raw_text', cashHeaders) \|\| 'backfill');`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7005: var rawTextVal = getFieldValue_(cashRow, 'raw_text', cashHeaders) \|\| getFieldValue_(cashRow, 'description', cashHeaders) \|\| '';`

#### Term: source_tab

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1549: source_tab: sourceTab,`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1581: 'source_tab', 'linked_txn_id', 'notes'`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2149: if (headerKey === 'source_tab' \|\| headerKey.includes('source_tab')) {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2150: return data.source_tab \|\| data.source \|\| '';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5183: const accountSourceCol = findColumn_(accountInfo, ['source_tab', 'source'], 11);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7034: source_tab: AIRO_CONFIG.tabs.cash,`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7125: * Audit function for Account Ledger to identify missing source_tab, cash backfill rows, and duplicate candidates.`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7168: var sourceTabVal = String(rowObj['source_tab'] \|\| '').trim();`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7172: // Check empty source_tab`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7245: * Safe, specific manual cleanup function for duplicate rows and blank source_tab in Account Ledger.`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7323: // Find column index of source_tab`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7326: if (canonicalKey_(headers[c]) === 'source_tab') {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7333: throw new Error('Could not find column index of source_tab');`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7336: // Repair missing source_tab values for remaining rows`
- `scripts/personal-workflow/airo_sheets_sync_dry_run.py:65: source_table: str`
- `scripts/personal-workflow/airo_sheets_sync_dry_run.py:218: source_table="transactions",`
- `scripts/personal-workflow/airo_sheets_sync_dry_run.py:231: source_table="transactions",`
- `scripts/personal-workflow/airo_sheets_sync_dry_run.py:261: source_table="transactions",`
- `scripts/personal-workflow/airo_sheets_sync_dry_run.py:300: source_table="transactions",`
- `scripts/personal-workflow/airo_sheets_sync_dry_run.py:362: source_table="transactions",`

#### Term: linked_txn_id

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1481: const entryId = common.linked_txn_id \|\| makeTxnId_({}, rawText);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1517: const entryId = common.rowId \|\| common.linked_txn_id \|\| makeTxnId_({}, rawText);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1550: linked_txn_id: common.linked_txn_id \|\| '',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1581: 'source_tab', 'linked_txn_id', 'notes'`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1798: linked_txn_id: data.linked_txn_id,`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2088: return data.entry_id \|\| data.linked_txn_id \|\| '';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2214: linked_txn_id: ['linked_txn_id', 'linked transaction id', 'transaction_id', 'txn_id', 'linked_id'],`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:3361: common.linked_txn_id \|\| makeTxnId_({}, rawText),`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6146: cc_entry_id: common.linked_txn_id \|\| makeTxnId_({}, rawText),`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6153: linked_txn_id: common.linked_txn_id \|\| makeTxnId_({}, rawText),`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6420: pay_id: common.linked_txn_id \|\| makeTxnId_({}, rawText),`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6483: pay_id: common.linked_txn_id \|\| makeTxnId_({}, rawText),`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6910: var entryId = getFieldValue_(rowObj, 'entry_id', cashHeaders) \|\| getFieldValue_(rowObj, 'linked_txn_id', cashHeaders);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6960: var entryId = getFieldValue_(rowObj, 'entry_id', accountHeaders) \|\| getFieldValue_(rowObj, 'linked_txn_id', accountHeaders);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6972: var cashEntryId = getFieldValue_(cashRow, 'entry_id', cashHeaders) \|\| getFieldValue_(cashRow, 'linked_txn_id', cashHeaders);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7035: linked_txn_id: getFieldValue_(cashRow, 'linked_txn_id', cashHeaders) \|\| '',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7405: var sharedTxnId = (common && (common.linked_txn_id \|\| common.rowId)) \|\| makeTxnId_({}, rawText);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7417: linked_txn_id: sharedTxnId + ':in'`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7431: linked_txn_id: sharedTxnId + ':out'`
- `scripts/personal-workflow/airo_sheets_sync_dry_run.py:389: "linked_txn_id": txid,`

### transfer handling

#### Term: internal transfer

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:4701: 'test phase d internal transfer blu cash',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:4702: 'test phase d internal transfer cash blu',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:4703: 'test phase d internal transfer bca cash',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:4704: 'test phase d internal transfer cash bca',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:4957: 'test phase d internal transfer bca blu',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:4958: 'test phase d internal transfer blu cash',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:4959: 'test phase d internal transfer cash blu',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:4960: 'test phase d internal transfer blu bca',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:4961: 'test phase d internal transfer bca cash',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:4962: 'test phase d internal transfer cash bca',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7369: * Detects whether the transaction represents an internal transfer between Cash, Blu, and BCA.`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7401: * Writes an internal transfer to the Account Ledger as two separate entries (outflow and inflow)`
- `scripts/personal-workflow/airo_transaction_persistence.py:236: "merchant": "Internal Transfer",`

#### Term: transfer

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:80: /\b(beli\|bayar\|jajan\|makan\|minum\|kopi\|sarapan\|siang\|malam\|cash\|tunai\|bca\|blu\|cc\|credit card\|kartu kredit\|tokopedia\|shopee\|grab\|gojek\|transfer\|tf\|topup\|tarik\|masuk\|keluar\|terima\|diterima\|gaji\|refund\|hutang\|utang\|pinjam\|cicilan\|kpr\|angsuran\|emas\|aset\|saldo)\b/i.test(text);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:111: if (/\b(hutang\|utang\|pinjam\|pinjaman\|cicilan\|kpr\|angsuran\|emas\|gold\|aset\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit)\b/i.test(text)) return false;`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:188: if (/^(c\|3)$/i.test(t) \|\| /\b(transfer\|tf\|pindah)\b/i.test(t)) return 'transfer';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:205: const hasClearAction = /\b(beli\|bayar\|makan\|minum\|kopi\|jajan\|transfer\|tf\|dari\|ke\|masuk\|keluar\|gaji\|refund\|terima\|diterima\|topup\|tarik\|cc\|credit card\|cash\|tunai)\b/i.test(text);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:216: 'C. Transfer\n' +`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:237: function normalizeTransferRouteClarificationAnswer_(text) {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:270: function canAskTransferIncompleteClarification_(parsed, rawText) {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:275: if (!/\b(transfer\|tf\|pindah)\b/i.test(text)) return false;`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:283: function buildTransferIncompleteClarificationMessage_(parsed) {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:285: 'Transfer Rp' + ((parsed && parsed.amount) \|\| 0) + ' ini dari akun mana ke akun mana?\n\n' +`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:291: 'Contoh manual: transfer 100000 dari bca ke blu'`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:295: function transferClarificationResolvedText_(pending, rawText) {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:296: const route = normalizeTransferRouteClarificationAnswer_(rawText);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:300: return 'transfer ' + amount + ' dari ' + route.source.toLowerCase() + ' ke ' + route.target.toLowerCase();`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:323: if (/\b(beli\|belanja\|bayar tagihan\|bayar cc\|lunas\|pelunasan\|alokasi\|pocket\|blu cc\|belum ke blu\|dari blu\|ke blu\|transferred\|transfer)\b/i.test(text)) {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:546: /\b(beli\|bayar\|jajan\|makan\|minum\|kopi\|bensin\|parkir\|tol\|grab\|gojek\|shopee\|tokopedia\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit\|hutang\|utang\|pinjam\|cicilan\|kpr\|emas\|gold\|aset\|nabung\|tabung\|saving\|gaji\|refund\|terima\|masuk\|keluar\|saldo\|tagihan\|angsuran)\b/i.test(original);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:591: /\b(beli\|bayar\|jajan\|makan\|minum\|kopi\|bensin\|parkir\|tol\|grab\|gojek\|shopee\|tokopedia\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit\|hutang\|utang\|pinjam\|cicilan\|kpr\|emas\|gold\|aset\|nabung\|tabung\|saving\|gaji\|refund\|terima\|masuk\|keluar)\b/i.test(text);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:609: if (/\b(transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit\|tokopedia cc\|tokopedia card\|hutang\|utang\|pinjam\|pinjaman\|cicilan rumah\|kpr\|angsuran rumah\|emas\|gold\|aset\|nabung\|tabung\|saving\|savings\|investasi\|gaji\|refund\|terima\|diterima\|masuk)\b/i.test(text)) return false;`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:654: if (/\b(hutang\|utang\|pinjam\|pinjaman\|cicilan rumah\|kpr\|angsuran rumah\|emas\|gold\|aset\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit)\b/i.test(text)) {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:691: '- transfer 100000 dari bca ke blu'`

#### Term: :in

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6927: if (entryStr.slice(-3) === ':in') {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7417: linked_txn_id: sharedTxnId + ':in'`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7430: rowId: sharedTxnId + ':in',`

#### Term: :out

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6929: } else if (entryStr.slice(-4) === ':out') {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7416: rowId: sharedTxnId + ':out',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7431: linked_txn_id: sharedTxnId + ':out'`

#### Term: linked_transaction_id

- `scripts/personal-workflow/airo_sheets_sync_dry_run.py:594: linked_txn_id = str(row_preview.get("linked_transaction_id") or "")`
- `scripts/personal-workflow/airo_full_auto_sheets_sync.py:59: "purpose", "amount", "source", "raw_text", "linked_transaction_id",`
- `scripts/personal-workflow/airo_asset_event_planner.py:37: "linked_transaction_id",`
- `scripts/personal-workflow/airo_asset_event_planner.py:315: "linked_transaction_id": trx_id,`

#### Term: linked_txn_id

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1481: const entryId = common.linked_txn_id \|\| makeTxnId_({}, rawText);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1517: const entryId = common.rowId \|\| common.linked_txn_id \|\| makeTxnId_({}, rawText);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1550: linked_txn_id: common.linked_txn_id \|\| '',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1581: 'source_tab', 'linked_txn_id', 'notes'`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1798: linked_txn_id: data.linked_txn_id,`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2088: return data.entry_id \|\| data.linked_txn_id \|\| '';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2214: linked_txn_id: ['linked_txn_id', 'linked transaction id', 'transaction_id', 'txn_id', 'linked_id'],`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:3361: common.linked_txn_id \|\| makeTxnId_({}, rawText),`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6146: cc_entry_id: common.linked_txn_id \|\| makeTxnId_({}, rawText),`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6153: linked_txn_id: common.linked_txn_id \|\| makeTxnId_({}, rawText),`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6420: pay_id: common.linked_txn_id \|\| makeTxnId_({}, rawText),`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6483: pay_id: common.linked_txn_id \|\| makeTxnId_({}, rawText),`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6910: var entryId = getFieldValue_(rowObj, 'entry_id', cashHeaders) \|\| getFieldValue_(rowObj, 'linked_txn_id', cashHeaders);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6960: var entryId = getFieldValue_(rowObj, 'entry_id', accountHeaders) \|\| getFieldValue_(rowObj, 'linked_txn_id', accountHeaders);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6972: var cashEntryId = getFieldValue_(cashRow, 'entry_id', cashHeaders) \|\| getFieldValue_(cashRow, 'linked_txn_id', cashHeaders);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7035: linked_txn_id: getFieldValue_(cashRow, 'linked_txn_id', cashHeaders) \|\| '',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7405: var sharedTxnId = (common && (common.linked_txn_id \|\| common.rowId)) \|\| makeTxnId_({}, rawText);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7417: linked_txn_id: sharedTxnId + ':in'`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7431: linked_txn_id: sharedTxnId + ':out'`
- `scripts/personal-workflow/airo_sheets_sync_dry_run.py:389: "linked_txn_id": txid,`

### cash handling

#### Term: Cash Ledger

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:15: cash: '💵 Cash Ledger',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1714: if (key.includes('cash ledger')) {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1888: // Cash Ledger movement type validation.`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5244: 'Cash Ledger inflows recent/top:\n' +`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5418: 'Cash Ledger in: Rp' + cashIn + '\n' +`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5419: 'Cash Ledger out: Rp' + cashOut + '\n' +`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5420: 'Cash Ledger net: Rp' + cashNet + '\n\n' +`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6816: * Manual backfill function to migrate historical data from 💵 Cash Ledger to 📒 Account Ledger.`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6826: throw new Error('Cash Ledger sheet not found');`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6836: throw new Error('Header not found in Cash Ledger');`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6847: // Validate required fields in Cash Ledger`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6866: throw new Error('Cash Ledger is missing required columns (Date, Account, Amount, or Description)');`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6890: // Read Cash Ledger rows`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7402: * and synchronizes with the Cash Ledger compatibility layer if one of the accounts is Cash.`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7435: // Cash Ledger compatibility layer synchronization`
- `scripts/personal-workflow/airo_sheets_sync_dry_run.py:409: if target_tab in {"💵 Cash Ledger", "🏠 Cicilan Rumah", "🤝 Hutang"}:`
- `scripts/personal-workflow/airo_cash_ledger_planner.py:2: """AIRO Cash Ledger planner v1.2.`
- `scripts/personal-workflow/airo_cash_ledger_planner.py:4: Read-only planner for Cash Ledger routing.`
- `scripts/personal-workflow/airo_cash_ledger_planner.py:19: CASH_LEDGER_TAB = "💵 Cash Ledger"`
- `scripts/personal-workflow/airo_cash_ledger_planner.py:189: "AIRO Cash Ledger Planner v1.2",`

#### Term: Cash Umum

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1645: if (v === 'cash umum') return '#1a73e8';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1680: return isCashBensinText_(text) ? 'Cash Bensin' : 'Cash Umum';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1685: return v === 'cash' \|\| v === 'cash umum' \|\| v === 'cash bensin';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2959: `=IFERROR("💵 Cash Aktif"&CHAR(10)&TEXT((SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Bensin"))-(SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Bensin"));"Rp #,##0");"💵 Cash Aktif"&CHAR(10)&"— catat dulu —")`;`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:4258: dashboard.getRange('D17').setFormula(`=IFERROR(((SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Bensin"))-(SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Bensin")))+'🥇 Aset'!B17+'🥇 Aset'!B18;0)`);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:4697: 'test cash umum',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:4699: 'test phase d cash umum',`

#### Term: Cash Bensin

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1646: if (v === 'cash bensin') return '#e8710a';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1680: return isCashBensinText_(text) ? 'Cash Bensin' : 'Cash Umum';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1685: return v === 'cash' \|\| v === 'cash umum' \|\| v === 'cash bensin';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2959: `=IFERROR("💵 Cash Aktif"&CHAR(10)&TEXT((SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Bensin"))-(SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Bensin"));"Rp #,##0");"💵 Cash Aktif"&CHAR(10)&"— catat dulu —")`;`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:4258: dashboard.getRange('D17').setFormula(`=IFERROR(((SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Bensin"))-(SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Bensin")))+'🥇 Aset'!B17+'🥇 Aset'!B18;0)`);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:4698: 'test cash bensin',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:4700: 'test phase d cash bensin',`
- `scripts/personal-workflow/airo_regression_smoke.sh:56: post_case "$((BASE+5))"  "cash bensin masuk 30000 hari ini"                      "Cash Ledger"`

#### Term: cash

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:15: cash: '💵 Cash Ledger',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:63: if (/^(c\|3)$/i.test(t) \|\| /\b(cash\|tunai)\b/i.test(t)) return 'Cash';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:80: /\b(beli\|bayar\|jajan\|makan\|minum\|kopi\|sarapan\|siang\|malam\|cash\|tunai\|bca\|blu\|cc\|credit card\|kartu kredit\|tokopedia\|shopee\|grab\|gojek\|transfer\|tf\|topup\|tarik\|masuk\|keluar\|terima\|diterima\|gaji\|refund\|hutang\|utang\|pinjam\|cicilan\|kpr\|angsuran\|emas\|aset\|saldo)\b/i.test(text);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:111: if (/\b(hutang\|utang\|pinjam\|pinjaman\|cicilan\|kpr\|angsuran\|emas\|gold\|aset\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit)\b/i.test(text)) return false;`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:121: '- 8rb cash\n' +`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:128: function normalizeCashClarificationAnswer_(text) {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:131: if (/^(a\|1)$/i.test(t) \|\| /\b(masuk\|terima\|diterima\|income\|pemasukan)\b/i.test(t)) return 'cash_in';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:132: if (/^(b\|2)$/i.test(t) \|\| /\b(keluar\|kepake\|terpakai\|pakai\|bayar\|beli\|expense\|pengeluaran)\b/i.test(t)) return 'cash_out';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:133: if (/^(c\|3)$/i.test(t) \|\| /\b(pegang\|saldo awal\|awal\|start)\b/i.test(t)) return 'cash_start';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:134: if (/^(d\|4)$/i.test(t) \|\| /\b(sisa\|remaining\|saldo akhir\|akhir)\b/i.test(t)) return 'cash_remaining';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:140: function canAskCashAmbiguousClarification_(parsed, rawText) {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:147: if (account !== 'cash') return false;`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:148: if (!/\b(cash\|tunai)\b/i.test(text)) return false;`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:155: function buildCashAmbiguousClarificationMessage_(parsed) {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:157: 'Saya tangkap ada transaksi Cash Rp' + ((parsed && parsed.amount) \|\| 0) + ', tapi maksudnya belum jelas.\n\n' +`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:159: 'A. Cash masuk\n' +`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:160: 'B. Cash keluar\n' +`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:161: 'C. Saldo cash awal / saya pegang cash\n' +`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:162: 'D. Sisa cash\n' +`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:168: function cashClarificationResolvedText_(pending, rawText) {`

#### Term: cash_sessions

- No match in top candidates.

#### Term: cash_entries

- No match in top candidates.

### domain wallet outflow handling

#### Term: cc_payment

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:308: if (/^(b\|2)$/i.test(t) \|\| /\b(bayar tagihan\|bayar cc\|payment\|tagihan\|lunas\|pelunasan)\b/i.test(t)) return 'cc_payment';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:363: if (choice === 'cc_payment') return 'CC_PAYMENT_HELP_ONLY';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:787: if (resolvedText === 'CC_PAYMENT_HELP_ONLY') {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2478: if (isCreditCardPaymentText_(t)) return 'cc_payment';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6096: return t \|\| 'cc_payment';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6204: issue_reason: 'cc_payment_amount_or_columns_missing'`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6242: issue_reason: 'cc_payment_no_matching_pending_purchase'`

#### Term: asset_purchase

- `scripts/personal-workflow/airo_sheets_sync_dry_run.py:182: return "asset_purchase", "asset_purchase"`
- `scripts/personal-workflow/airo_transaction_persistence.py:261: "cashflow_treatment": "asset_purchase",`

#### Term: debt_payment

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:386: if (/^(b\|2)$/i.test(t) \|\| /\b(bayar hutang\|bayar utang\|lunasi\|nyicil\|cicil)\b/i.test(t)) return 'debt_payment';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:517: if (choice === 'debt_payment') return 'DEBT_NEEDS_COMPLETE_REWRITE';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2481: if (isDebtPaymentText_(t)) return 'debt_payment';`

#### Term: installment

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:4611: cicilan_ke: findCol_(['cicilan_ke', 'cicilan ke', 'angsuran_ke', 'installment_no']),`
- `scripts/personal-workflow/airo_sheets_sync_dry_run.py:519: def plan_installment_payment(row: sqlite3.Row) -> PlannedOperation:`
- `scripts/personal-workflow/airo_sheets_sync_dry_run.py:524: "installment_payments",`
- `scripts/personal-workflow/airo_sheets_sync_dry_run.py:526: item.get("installment_id"),`
- `scripts/personal-workflow/airo_sheets_sync_dry_run.py:528: item.get("installment_number"),`
- `scripts/personal-workflow/airo_sheets_sync_dry_run.py:537: source_table="installment_payments",`
- `scripts/personal-workflow/airo_sheets_sync_dry_run.py:540: duplicate_key=f"installment_payment:{payment_id}",`
- `scripts/personal-workflow/airo_sheets_sync_dry_run.py:542: reason="installment payment row",`
- `scripts/personal-workflow/airo_sheets_sync_dry_run.py:545: "cicilan_ke": item.get("installment_number"),`
- `scripts/personal-workflow/airo_sheets_sync_dry_run.py:615: if "installment_payments" in tables:`
- `scripts/personal-workflow/airo_sheets_sync_dry_run.py:616: for row in cur.execute("SELECT rowid, * FROM installment_payments ORDER BY rowid ASC").fetchall():`
- `scripts/personal-workflow/airo_sheets_sync_dry_run.py:617: ops.append(plan_installment_payment(row))`
- `scripts/personal-workflow/airo_sheets_sync_dry_run.py:666: "Approval Queue, conflicts, installments, and installment_payments are supported when rows exist.",`
- `scripts/personal-workflow/airo_full_auto_sheets_sync.py:148: V13_CICILAN_RUMAH_HEADERS = ["payment_id","date","cicilan_ke","amount","standard_installment","usual_paid_amount","remaining_after_payment","total_tenor","due_day","source","sync_hash","notes"]`
- `scripts/personal-workflow/airo_cicilan_rumah_planner.py:22: STANDARD_INSTALLMENT = 1543000`
- `scripts/personal-workflow/airo_cicilan_rumah_planner.py:123: "standard_installment": STANDARD_INSTALLMENT,`
- `scripts/personal-workflow/airo_finance_sheet_v12_status.py:61: role="house installment payment history",`
- `scripts/personal_workflow_db_smoke.py:13: from airo_personal_workflow.db.repository import record_from_text, check_installment, monthly_summary`
- `scripts/personal_workflow_db_smoke.py:36: result = check_installment("Cicilan Rumah")`
- `scripts/personal_workflow_db_smoke.py:39: print("=== CHECK INSTALLMENT ===")`

#### Term: cicilan

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:17: cicilanRumah: '🏠 Cicilan Rumah',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:80: /\b(beli\|bayar\|jajan\|makan\|minum\|kopi\|sarapan\|siang\|malam\|cash\|tunai\|bca\|blu\|cc\|credit card\|kartu kredit\|tokopedia\|shopee\|grab\|gojek\|transfer\|tf\|topup\|tarik\|masuk\|keluar\|terima\|diterima\|gaji\|refund\|hutang\|utang\|pinjam\|cicilan\|kpr\|angsuran\|emas\|aset\|saldo)\b/i.test(text);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:111: if (/\b(hutang\|utang\|pinjam\|pinjaman\|cicilan\|kpr\|angsuran\|emas\|gold\|aset\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit)\b/i.test(text)) return false;`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:546: /\b(beli\|bayar\|jajan\|makan\|minum\|kopi\|bensin\|parkir\|tol\|grab\|gojek\|shopee\|tokopedia\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit\|hutang\|utang\|pinjam\|cicilan\|kpr\|emas\|gold\|aset\|nabung\|tabung\|saving\|gaji\|refund\|terima\|masuk\|keluar\|saldo\|tagihan\|angsuran)\b/i.test(original);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:591: /\b(beli\|bayar\|jajan\|makan\|minum\|kopi\|bensin\|parkir\|tol\|grab\|gojek\|shopee\|tokopedia\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit\|hutang\|utang\|pinjam\|cicilan\|kpr\|emas\|gold\|aset\|nabung\|tabung\|saving\|gaji\|refund\|terima\|masuk\|keluar)\b/i.test(text);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:609: if (/\b(transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit\|tokopedia cc\|tokopedia card\|hutang\|utang\|pinjam\|pinjaman\|cicilan rumah\|kpr\|angsuran rumah\|emas\|gold\|aset\|nabung\|tabung\|saving\|savings\|investasi\|gaji\|refund\|terima\|diterima\|masuk)\b/i.test(text)) return false;`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:654: if (/\b(hutang\|utang\|pinjam\|pinjaman\|cicilan rumah\|kpr\|angsuran rumah\|emas\|gold\|aset\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit)\b/i.test(text)) {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2247: if (/\b(cicilan rumah\|kpr\|angsuran rumah\|bayar rumah)\b/i.test(text)) return AIRO_CONFIG.tabs.cicilanRumah;`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2283: if (/\b(hutang\|utang\|pinjam\|pinjaman\|cicilan rumah\|kpr\|angsuran rumah\|cash\|tunai)\b/i.test(text)) {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2292: if (/\b(cicilan rumah\|kpr\|angsuran rumah\|bayar rumah)\b/i.test(text) && !/\b\d+(?:[.,]\d+)?\s*(jt\|juta\|rb\|ribu\|k)?\b/i.test(text)) {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2293: return 'cicilan_rumah_amount_unclear';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2432: if (/\b(cicilan rumah\|kpr\|angsuran rumah)\b/i.test(t)) return 'Cicilan Rumah';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2748: if (/\b(cicilan rumah\|kpr\|angsuran rumah\|bayar rumah)\b/i.test(text) \|\| parsed.category === 'Cicilan Rumah') {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2749: return AIRO_CONFIG.tabs.cicilanRumah;`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:4437: 'Cicilan',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:4534: if (/^admin\s+(audit\|check\|cek)\s+(cicilan\s+rumah\|cicilan\|kpr\|angsuran\s+rumah)\s+(rows\|row\|headers\|header\|testrows\|test\|status)/i.test(text)) {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:4536: const sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.cicilanRumah);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:4539: sendTelegram_(chatId, 'Cicilan Rumah audit gagal: sheet Cicilan Rumah tidak ditemukan.');`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:4543: command: 'cicilan_rumah_rows_runtime_audit',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:4544: reason: 'cicilan_rumah_sheet_missing'`

### balance logic

#### Term: balance

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:189: if (/^(d\|4)$/i.test(t) \|\| /\b(saldo\|balance\|tercatat\|awal\|akhir)\b/i.test(t)) return 'balance';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1514: * Balance is intentionally left blank for Google Sheet formulas.`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1544: balance: '',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1580: 'balance', 'type', 'category', 'description', 'raw_text',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5269: if (/^admin\s+(audit\|check\|cek)\s+cash\s+(parity\|balance\|total\|ledger)/i.test(text)) {`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6818: * and key properties, and populates balance formulas dynamically without overwriting existing data.`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7029: balance: '',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:7042: // Set formula balance`
- `scripts/personal-workflow/airo_finance_sheet_v12_regression.py:130: checks.append(check(hutang["normalized"]["balance_after"] == 14000000, "hutang remaining balance preview works"))`
- `scripts/personal-workflow/airo_full_auto_sheets_sync.py:147: V13_CASH_ENTRY_HEADERS = ["entry_id","session_id","date","description","category","amount","direction","balance_after","source","sync_hash","notes"]`
- `scripts/personal-workflow/airo_full_auto_sheets_sync.py:149: V13_HUTANG_HEADERS = ["payment_id","date","debt_id","creditor","amount","account","balance_before","balance_after","source","sync_hash","notes"]`
- `scripts/personal-workflow/airo_full_auto_sheets_sync.py:173: "account", "balance_before", "balance_after", "status", "notes",`
- `scripts/personal-workflow/airo_hutang_planner.py:23: "balance": 15000000,`
- `scripts/personal-workflow/airo_hutang_planner.py:28: "balance": 5000000,`
- `scripts/personal-workflow/airo_hutang_planner.py:33: "balance": 5000000,`
- `scripts/personal-workflow/airo_hutang_planner.py:136: balance_before = int(debt_data["balance"]) if debt_data else None`
- `scripts/personal-workflow/airo_hutang_planner.py:137: balance_after = None`
- `scripts/personal-workflow/airo_hutang_planner.py:138: if balance_before is not None and amount is not None:`
- `scripts/personal-workflow/airo_hutang_planner.py:139: balance_after = max(balance_before - amount, 0)`
- `scripts/personal-workflow/airo_hutang_planner.py:161: "balance_before": balance_before,`

#### Term: previous_balance

- No match in top candidates.

#### Term: amount_in

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1467: const inCol = findCashLedgerExactHeaderCol_(sheet, 'amount_in');`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1498: amount_in: cashInflow ? parsed.amount : '',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1542: amount_in: isInflow ? amount : '',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1579: 'entry_id', 'date', 'account', 'amount_in', 'amount_out',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2129: headerKey === 'amount_in' \|\|`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2130: headerKey.includes('amount_in') \|\|`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2138: return cashInflow ? (data.amount_in \|\| data.amount \|\| '') : (data.amount_in ?? '');`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2174: // Important: check amount_in / amount_out before generic amount,`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2177: h === 'amount_in' \|\|`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2178: h.includes('amount_in') \|\|`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2186: return 'amount_in';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2879: sheet.getRange(r, 17).setValue(amount);         // amount_in`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2882: sheet.getRange(r, 17).clearContent();           // amount_in`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5075: const cashInCol = findColumn_(cashInfo, ['amount_in', 'cash_in', 'nominal_masuk', 'masuk'], 17);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5077: const accountInCol = findColumn_(accountInfo, ['amount_in', 'cash_in', 'nominal_masuk', 'masuk'], 4);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5158: const cashInCol = findColumn_(cashInfo, ['amount_in', 'cash_in', 'nominal_masuk', 'masuk'], 17);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5181: const accountInCol = findColumn_(accountInfo, ['amount_in', 'cash_in', 'nominal_masuk', 'masuk'], 4);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5352: const cashInCol = findColumn_(cashInfo, ['amount_in', 'cash_in', 'nominal_masuk', 'masuk'], 17);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5355: const accountInCol = findColumn_(accountInfo, ['amount_in', 'cash_in', 'nominal_masuk', 'masuk'], 4);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6858: return f === 'amount' \|\| f === 'amount_in' \|\| f === 'amount_out' \|\| canonicalKey_(h) === 'amount';`

#### Term: amount_out

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1468: const outCol = findCashLedgerExactHeaderCol_(sheet, 'amount_out');`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1499: amount_out: cashInflow ? '' : parsed.amount,`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1543: amount_out: isInflow ? '' : amount,`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1579: 'entry_id', 'date', 'account', 'amount_in', 'amount_out',`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2116: headerKey === 'amount_out' \|\|`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2117: headerKey.includes('amount_out') \|\|`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2125: return cashInflow ? '' : (data.amount_out ?? data.amount ?? '');`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2174: // Important: check amount_in / amount_out before generic amount,`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2175: // otherwise amount_out may be filled as expense for cash inflow rows.`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2190: h === 'amount_out' \|\|`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2191: h.includes('amount_out') \|\|`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2199: return 'amount_out';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2878: sheet.getRange(r, 16).clearContent();           // amount_out`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:2881: sheet.getRange(r, 16).setValue(amount);         // amount_out`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5074: const cashOutCol = findColumn_(cashInfo, ['amount_out', 'cash_out', 'nominal_keluar', 'keluar'], 16);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5078: const accountOutCol = findColumn_(accountInfo, ['amount_out', 'cash_out', 'nominal_keluar', 'keluar'], 5);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5351: const cashOutCol = findColumn_(cashInfo, ['amount_out', 'cash_out', 'nominal_keluar', 'keluar'], 16);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:5356: const accountOutCol = findColumn_(accountInfo, ['amount_out', 'cash_out', 'nominal_keluar', 'keluar'], 5);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6858: return f === 'amount' \|\| f === 'amount_in' \|\| f === 'amount_out' \|\| canonicalKey_(h) === 'amount';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:6880: return canonicalKey_(h) === 'amount_out';`

#### Term: saldo

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:80: /\b(beli\|bayar\|jajan\|makan\|minum\|kopi\|sarapan\|siang\|malam\|cash\|tunai\|bca\|blu\|cc\|credit card\|kartu kredit\|tokopedia\|shopee\|grab\|gojek\|transfer\|tf\|topup\|tarik\|masuk\|keluar\|terima\|diterima\|gaji\|refund\|hutang\|utang\|pinjam\|cicilan\|kpr\|angsuran\|emas\|aset\|saldo)\b/i.test(text);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:133: if (/^(c\|3)$/i.test(t) \|\| /\b(pegang\|saldo awal\|awal\|start)\b/i.test(t)) return 'cash_start';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:134: if (/^(d\|4)$/i.test(t) \|\| /\b(sisa\|remaining\|saldo akhir\|akhir)\b/i.test(t)) return 'cash_remaining';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:150: const hasClearMeaning = /\b(masuk\|keluar\|terima\|diterima\|beli\|bayar\|kepake\|terpakai\|pegang\|saldo\|sisa\|dari\|ke\|bensin\|bbm)\b/i.test(text);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:161: 'C. Saldo cash awal / saya pegang cash\n' +`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:176: if (direction === 'cash_start') return ('saya pegang cash ' + amount + ' saldo awal ' + tail).trim();`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:177: if (direction === 'cash_remaining') return ('sisa cash ' + amount + ' saldo akhir ' + tail).trim();`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:189: if (/^(d\|4)$/i.test(t) \|\| /\b(saldo\|balance\|tercatat\|awal\|akhir)\b/i.test(t)) return 'balance';`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:217: 'D. Saldo awal/saldo tercatat\n' +`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:546: /\b(beli\|bayar\|jajan\|makan\|minum\|kopi\|bensin\|parkir\|tol\|grab\|gojek\|shopee\|tokopedia\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit\|hutang\|utang\|pinjam\|cicilan\|kpr\|emas\|gold\|aset\|nabung\|tabung\|saving\|gaji\|refund\|terima\|masuk\|keluar\|saldo\|tagihan\|angsuran)\b/i.test(original);`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1015: 'D. Saldo awal/saldo tercatat\n' +`
- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs:1041: 'C. Saldo cash awal / saya pegang cash\n' +`
- `scripts/personal-workflow/airo_sheets_sync_dry_run.py:178: if "topup" in text or "top up" in text or "isi saldo" in text:`
- `scripts/personal-workflow/airo_transaction_persistence.py:248: if re.search(r"\b(topup\|top up\|isi saldo)\b", text):`

## 4. Likely Sprint 1 Surfaces

### Runtime writer surface

Needs confirmation from exact file audit:

- Google Sheets append/write helpers
- Account Ledger row append/update function
- balance update function
- duplicate/idempotency checks
- source_tab and linked_txn_id assignment

### Routing surface

Needs confirmation from exact file audit:

- internal transfer route
- cash in/out route
- CC payment route
- asset purchase route
- debt payment route
- cicilan payment route if wallet movement is touched

### Test surface

Needs confirmation from exact file audit:

- local parser/planner tests
- dry-run mapper tests
- Apps Script regression or syntax check command
- finance route guard tests

## 5. Sprint 1 Patch Order Recommendation

Do not start with Cash Ledger deletion. That is Sprint 3.

Patch order should be smallest safe gap first:

1. Source audit exact Account Ledger writer and tests.
2. Add regression for current internal transfer two-sided behavior if missing.
3. Harden linked_txn_id/source_tab consistency for Account Ledger movement rows.
4. Harden cash movement into Account Ledger without removing Cash Ledger compatibility.
5. Harden CC payment wallet outflow.
6. Harden asset/debt wallet outflow.
7. Verify balance consistency.

## 6. Exact Audit Targets for Next Micro-Step

The next command should inspect the top candidate files directly and produce a patch plan with file/function names for:

- Account Ledger append/update function
- balance calculation logic
- internal transfer writer
- cash movement writer or compatibility path
- CC payment wallet outflow path
- asset purchase wallet outflow path
- debt payment wallet outflow path
- linked_txn_id handling
- source_tab handling
- existing regression command set

No runtime patch should be made until this exact file/function map exists.
