# AIRO Google Sheet Finance v1.2 Source Audit

Status: GENERATED / READ-ONLY AUDIT
Date: 2026-05-11
Scope: AIRO Finance Sheet Workflow
Baseline: Google Sheet Finance Balanced+ v1.1.8-final

## Purpose

This audit maps existing repository source references against the 11 confirmed Google Sheet Finance tabs.

The audit is read-only. It does not access credentials, mutate SQLite, write to Google Sheets, or restart OpenClaw.

## Confirmed Existing Tabs

1. 🏠 Dashboard
2. 💸 Transactions
3. 💵 Cash Ledger
4. 💳 Credit Card
5. 🏠 Cicilan Rumah
6. 🤝 Hutang
7. 🥇 Aset
8. 📅 Monthly Review
9. 🧾 Review Queue
10. ⚙️ Settings
11. 🔄 Sync Log

## Completion Matrix

| Tab | Current implementation status | v1.2 interpretation |
|---|---|---|
| 🏠 Dashboard | DESIGN_DONE / FORMULA_DRIVEN | Not a direct ledger write target; status UX can be improved later |
| 💸 Transactions | FULL_AUTO_CORE_READY | Preserve and regression-test |
| 💵 Cash Ledger | DESIGNED / HEADER_VALID / NOT_GENERALIZED | Needs route and sync completion |
| 💳 Credit Card | FULL_AUTO_CORE_READY / TOKOPEDIA_CC_PASS | Preserve and extend tests only |
| 🏠 Cicilan Rumah | DESIGNED / HEADER_VALID / NOT_GENERALIZED | Needs route and sync completion |
| 🤝 Hutang | DESIGNED / HEADER_VALID / NOT_GENERALIZED | Needs route and sync completion |
| 🥇 Aset | ASSET_SYNC_PATCHED | Verify latest regression; preserve append-only behavior |
| 📅 Monthly Review | DESIGNED / HEADER_VALID / REPORTING | Define refresh/report behavior, not raw capture write |
| 🧾 Review Queue | DESIGNED / HEADER_VALID / NOT_GENERALIZED | Needed as parser ambiguity guardrail |
| ⚙️ Settings | CONFIG_ONLY | Do not use as ledger target |
| 🔄 Sync Log | FULL_AUTO_CORE_READY | Preserve observability and audit rows |

## Source Evidence


### 🏠 Dashboard

Pattern: `Dashboard|dashboard|airo_ops_dashboard|airo_dashboard`

```text
scripts/personal-workflow/airo_approval_queue.py:98:def cmd_dashboard(args):
scripts/personal-workflow/airo_approval_queue.py:105:    out_dir = Path(args.output).expanduser().resolve() if args.output else Path(args.root).expanduser().resolve() / "dashboard"
scripts/personal-workflow/airo_approval_queue.py:135:<p class="small">Generated {html.escape(now())}. Local dashboard only. No action is executed from this page.</p>
scripts/personal-workflow/airo_approval_queue.py:146:    emit({"ok": True, "operation": "dashboard_generate", "db": str(db), "dashboard": str(out_file), "count": len(items)})
scripts/personal-workflow/airo_approval_queue.py:176:    d = sub.add_parser("dashboard")
scripts/personal-workflow/airo_approval_queue.py:178:    d.set_defaults(func=cmd_dashboard)
scripts/personal-workflow/airo_local_dashboard.py:84:    p = argparse.ArgumentParser(description="Airo local dashboard generator")
scripts/personal-workflow/airo_local_dashboard.py:91:    out_dir = Path(args.output).expanduser().resolve() if args.output else root / "dashboard"
scripts/personal-workflow/airo_local_dashboard.py:101:        "dashboard": str(out_file),
scripts/personal-workflow/airo_local_dashboard.py:106:        "safety": "local_dashboard_only_no_execution"
scripts/personal-workflow/airo_local_dashboard.py:110:        emit({"ok": True, "operation": "dashboard_summary", **summary})
scripts/personal-workflow/airo_local_dashboard.py:116:<title>Airo Personal Workflow Dashboard</title>
scripts/personal-workflow/airo_local_dashboard.py:139:<h1>Airo Personal Workflow Dashboard</h1>
scripts/personal-workflow/airo_local_dashboard.py:140:<p>Generated {html.escape(summary["generated"])}. Local-only dashboard. No action is executed from this page.</p>
scripts/personal-workflow/airo_local_dashboard.py:165:<p>This dashboard is read-only. It does not execute Google writes, mutate SQLite finance records, patch OpenClaw, restart services, access browser profiles, or touch EarnsAI trading runtime.</p>
scripts/personal-workflow/airo_local_dashboard.py:173:    emit({"ok": True, "operation": "dashboard_generate", **summary})
scripts/personal-workflow/airo_final_smoke.py:125:        ("dashboard_alignment", ["./bin/airo-dashboard-align"], expect_nonempty),
scripts/personal-workflow/airo_final_smoke.py:126:        ("ops_dashboard", ["python3", "scripts/personal-workflow/airo_ops_dashboard.py"], expect_nonempty),
scripts/personal-workflow/airo_daily.py:108:    dashboard = root / "dashboard" / "daily_ops.html"
scripts/personal-workflow/airo_daily.py:150:        "label": "Refresh daily ops dashboard",
scripts/personal-workflow/airo_daily.py:151:        "command": "python3 scripts/personal-workflow/airo_ops_dashboard.py"
scripts/personal-workflow/airo_daily.py:169:        "dashboard": str(dashboard),
scripts/personal-workflow/airo_daily.py:170:        "dashboard_exists": dashboard.exists(),
scripts/personal-workflow/airo_daily.py:192:    print(f"Dashboard: {summary['dashboard']}")
scripts/personal-workflow/airo_dashboard_daily_alignment.py:54:        "dashboard": daily.get("dashboard"),
scripts/personal-workflow/airo_dashboard_daily_alignment.py:61:<p>This section is generated from <code>./bin/airo-daily</code>, so the dashboard and daily CLI recommend the same next actions.</p>
scripts/personal-workflow/airo_dashboard_daily_alignment.py:77:    p = argparse.ArgumentParser(description="Align Airo dashboard with airo-daily recommendations")
scripts/personal-workflow/airo_dashboard_daily_alignment.py:83:    dashboard = root / "dashboard" / "daily_ops.html"
scripts/personal-workflow/airo_dashboard_daily_alignment.py:85:    subprocess.check_call(["python3", "scripts/personal-workflow/airo_ops_dashboard.py"], stdout=subprocess.DEVNULL)
scripts/personal-workflow/airo_dashboard_daily_alignment.py:88:    if not dashboard.exists():
scripts/personal-workflow/airo_dashboard_daily_alignment.py:89:        emit({"ok": False, "error": "daily ops dashboard not found", "dashboard": str(dashboard)}, 2)
scripts/personal-workflow/airo_dashboard_daily_alignment.py:91:    html_text = dashboard.read_text(encoding="utf-8", errors="ignore")
scripts/personal-workflow/airo_dashboard_daily_alignment.py:108:    dashboard.write_text(html_text, encoding="utf-8")
scripts/personal-workflow/airo_dashboard_daily_alignment.py:112:        "operation": "dashboard_daily_command_alignment",
scripts/personal-workflow/airo_dashboard_daily_alignment.py:113:        "dashboard": str(dashboard),
scripts/personal-workflow/airo_intent_router.py:66:    if has_any(text, ["dashboard", "daily ops", "operasi harian"]):
scripts/personal-workflow/airo_intent_router.py:71:            "intent": "dashboard",
scripts/personal-workflow/airo_intent_router.py:75:            "reason": "Message asks for dashboard.",
scripts/personal-workflow/airo_intent_router.py:76:            "recommended_next_step": "Refresh daily ops dashboard.",
scripts/personal-workflow/airo_intent_router.py:77:            "exact_safe_command": "python3 scripts/personal-workflow/airo_ops_dashboard.py"
scripts/personal-workflow/airoctl.py:14:    "dashboard": ROOT / "airo_local_dashboard.py",
scripts/personal-workflow/airoctl.py:75:    d = sub.add_parser("dashboard")
scripts/personal-workflow/airoctl.py:121:    if args.cmd == "dashboard":
scripts/personal-workflow/airoctl.py:122:        cmd = [sys.executable, tool("dashboard")]
scripts/personal-workflow/airoctl.py:125:        emit({"ok": True, "wrapper": "airoctl", "command": "dashboard", "result": run_json(cmd)})
scripts/personal-workflow/airo_ops_dashboard.py:253:    p = argparse.ArgumentParser(description="Airo daily operations dashboard with next-action recommendations")
scripts/personal-workflow/airo_ops_dashboard.py:260:    out_dir = Path(args.output).expanduser().resolve() if args.output else root / "dashboard"
scripts/personal-workflow/airo_ops_dashboard.py:301:        "operation": "daily_ops_dashboard_next_action",
scripts/personal-workflow/airo_ops_dashboard.py:304:        "dashboard": str(out_file),
scripts/personal-workflow/airo_ops_dashboard.py:328:<title>Airo Daily Ops Dashboard</title>
scripts/personal-workflow/airo_ops_dashboard.py:349:<h1>Airo Daily Ops Dashboard</h1>
scripts/personal-workflow/airo_ops_dashboard.py:350:<p>Generated {esc(summary["generated"])}. Read-only local dashboard with next-action recommendations.</p>
scripts/personal-workflow/airo_ops_dashboard.py:380:<p>This dashboard is read-only. It does not execute approved items, write to Google, mutate finance records, patch OpenClaw, restart services, access browser profiles, read token contents, or touch EarnsAI runtime.</p>
bin/airo-dashboard-align:4:exec python3 scripts/personal-workflow/airo_dashboard_daily_alignment.py "$@"
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_PREVIEW_V0_3_PASS.md:43:- Dashboard totals
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:16:1. 🏠 Dashboard
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:32:| 🏠 Dashboard | DESIGN_DONE / FORMULA_DRIVEN | Not a direct ledger write target; status UX can be improved later |
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:47:### 🏠 Dashboard
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:49:Pattern: `Dashboard|dashboard|airo_ops_dashboard|airo_dashboard`
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:52:scripts/personal-workflow/airo_approval_queue.py:98:def cmd_dashboard(args):
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:53:scripts/personal-workflow/airo_approval_queue.py:105:    out_dir = Path(args.output).expanduser().resolve() if args.output else Path(args.root).expanduser().resolve() / "dashboard"
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:54:scripts/personal-workflow/airo_approval_queue.py:135:<p class="small">Generated {html.escape(now())}. Local dashboard only. No action is executed from this page.</p>
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:55:scripts/personal-workflow/airo_approval_queue.py:146:    emit({"ok": True, "operation": "dashboard_generate", "db": str(db), "dashboard": str(out_file), "count": len(items)})
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:56:scripts/personal-workflow/airo_approval_queue.py:176:    d = sub.add_parser("dashboard")
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:57:scripts/personal-workflow/airo_approval_queue.py:178:    d.set_defaults(func=cmd_dashboard)
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:58:scripts/personal-workflow/airo_local_dashboard.py:84:    p = argparse.ArgumentParser(description="Airo local dashboard generator")
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:59:scripts/personal-workflow/airo_local_dashboard.py:91:    out_dir = Path(args.output).expanduser().resolve() if args.output else root / "dashboard"
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:60:scripts/personal-workflow/airo_local_dashboard.py:101:        "dashboard": str(out_file),
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:61:scripts/personal-workflow/airo_local_dashboard.py:106:        "safety": "local_dashboard_only_no_execution"
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:62:scripts/personal-workflow/airo_local_dashboard.py:110:        emit({"ok": True, "operation": "dashboard_summary", **summary})
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:63:scripts/personal-workflow/airo_local_dashboard.py:116:<title>Airo Personal Workflow Dashboard</title>
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:64:scripts/personal-workflow/airo_local_dashboard.py:139:<h1>Airo Personal Workflow Dashboard</h1>
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:65:scripts/personal-workflow/airo_local_dashboard.py:140:<p>Generated {html.escape(summary["generated"])}. Local-only dashboard. No action is executed from this page.</p>
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:66:scripts/personal-workflow/airo_local_dashboard.py:165:<p>This dashboard is read-only. It does not execute Google writes, mutate SQLite finance records, patch OpenClaw, restart services, access browser profiles, or touch EarnsAI trading runtime.</p>
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:67:scripts/personal-workflow/airo_local_dashboard.py:173:    emit({"ok": True, "operation": "dashboard_generate", **summary})
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:68:scripts/personal-workflow/airo_final_smoke.py:125:        ("dashboard_alignment", ["./bin/airo-dashboard-align"], expect_nonempty),
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:69:scripts/personal-workflow/airo_final_smoke.py:126:        ("ops_dashboard", ["python3", "scripts/personal-workflow/airo_ops_dashboard.py"], expect_nonempty),
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:70:scripts/personal-workflow/airo_daily.py:108:    dashboard = root / "dashboard" / "daily_ops.html"
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:71:scripts/personal-workflow/airo_daily.py:150:        "label": "Refresh daily ops dashboard",
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:72:scripts/personal-workflow/airo_daily.py:151:        "command": "python3 scripts/personal-workflow/airo_ops_dashboard.py"
```

### 💸 Transactions

Pattern: `Transactions|transactions|transaction_id|duplicate_key`

```text
scripts/personal-workflow/airo_asset_event_planner.py:12:into `plan_asset_events_from_transactions`.
scripts/personal-workflow/airo_asset_event_planner.py:37:    "linked_transaction_id",
scripts/personal-workflow/airo_asset_event_planner.py:126:def _transaction_id(row: dict[str, Any]) -> str:
scripts/personal-workflow/airo_asset_event_planner.py:127:    for key in ("transaction_id", "id", "rowid"):
scripts/personal-workflow/airo_asset_event_planner.py:236:    duplicate_key: str
scripts/personal-workflow/airo_asset_event_planner.py:245:def plan_asset_events_from_transactions(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
scripts/personal-workflow/airo_asset_event_planner.py:301:    trx_id = _transaction_id(row)
scripts/personal-workflow/airo_asset_event_planner.py:315:        "linked_transaction_id": trx_id,
scripts/personal-workflow/airo_asset_event_planner.py:343:    trx_id = _transaction_id(row)
scripts/personal-workflow/airo_asset_event_planner.py:373:    print(json.dumps(plan_asset_events_from_transactions(sample), ensure_ascii=False, indent=2))
scripts/personal-workflow/airo_credit_card_mirror_planner.py:6:- Generate 💳 Credit Card mirror operations for Tokopedia Card transactions.
scripts/personal-workflow/airo_credit_card_mirror_planner.py:75:    # Mirror only canonical 💸 Transactions operations.
scripts/personal-workflow/airo_credit_card_mirror_planner.py:77:    if target_tab != "💸 Transactions":
scripts/personal-workflow/airo_credit_card_mirror_planner.py:103:def get_transaction_id(op: dict[str, Any]) -> str:
scripts/personal-workflow/airo_credit_card_mirror_planner.py:106:    for key in ("transaction_id", "linked_txn_id", "entity_id"):
scripts/personal-workflow/airo_credit_card_mirror_planner.py:111:    duplicate_key = str(op.get("duplicate_key") or "")
scripts/personal-workflow/airo_credit_card_mirror_planner.py:112:    if ":" in duplicate_key:
scripts/personal-workflow/airo_credit_card_mirror_planner.py:113:        return duplicate_key.split(":", 1)[1]
scripts/personal-workflow/airo_credit_card_mirror_planner.py:115:    return duplicate_key
scripts/personal-workflow/airo_credit_card_mirror_planner.py:140:    transaction_id = get_transaction_id(op)
scripts/personal-workflow/airo_credit_card_mirror_planner.py:143:    if not transaction_id or not transaction_date:
scripts/personal-workflow/airo_credit_card_mirror_planner.py:153:        "cc_entry_id": "cc_" + hashlib.sha256(transaction_id.encode("utf-8")).hexdigest()[:12],
scripts/personal-workflow/airo_credit_card_mirror_planner.py:160:        "linked_txn_id": transaction_id,
scripts/personal-workflow/airo_credit_card_mirror_planner.py:161:        "notes": "auto_mirror_from_transactions_v0_9",
scripts/personal-workflow/airo_credit_card_mirror_planner.py:174:        "source_table": op.get("source_table") or "transactions",
scripts/personal-workflow/airo_credit_card_mirror_planner.py:176:        "entity_id": transaction_id,
scripts/personal-workflow/airo_credit_card_mirror_planner.py:177:        "duplicate_key": transaction_id,
scripts/personal-workflow/apps-script/airo_finance_sheet_key_exporter_v0_3.gs:5: * - reads duplicate_key/sync_hash-compatible keys from sync target tabs
scripts/personal-workflow/apps-script/airo_finance_sheet_key_exporter_v0_3.gs:27:      '💸 Transactions': exportByHeaderV03_(ss, '💸 Transactions', 1, 'duplicate_key', 'sync_hash'),
scripts/personal-workflow/apps-script/airo_finance_sheet_key_exporter_v0_3.gs:75:      duplicate_key: key,
scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs:107:    'transaction_id',
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:5: * - Appends one Tokopedia CC transaction to 💸 Transactions if missing.
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:10: * - 💸 Transactions: duplicate_key = transactions:trx_41a84be31c7e
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:27:  const txSheet = ss.getSheetByName('💸 Transactions');
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:31:  if (!txSheet) throw new Error('ABORT: 💸 Transactions tab not found.');
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:35:  validateTransactionsHeaderV10_(txSheet);
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:43:  const txHeaders = ["transaction_id", "date", "month", "type", "category", "subcategory", "description", "merchant", "amount", "account", "source", "status", "confidence", "raw_text", "synced_at", "notes", "currency", "review_status", "local_db_table", "local_db_rowid", "sync_hash", "duplicate_key", "created_at", "updated_at", "from_account", "to_account", "transfer_purpose", "asset_bucket", "pocket_name", "cashflow_treatment"];
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:44:  const txValues = ["trx_41a84be31c7e", "2026-05-10", "2026-05", "expense", "Belanja", "", "catat beli barang tokopedia 100rb pakai tokopedia credit card", "belanja", 100000, "Tokopedia CC", "telegram", "synced", 0.9, "catat beli barang tokopedia 100rb pakai tokopedia credit card", "", "", "IDR", "auto_approved", "transactions", 3, "1ed99b1b6f6bbf1e429c76b3", "transactions:trx_41a84be31c7e", "2026-05-10 09:33:21", "2026-05-10 09:33:21", "", "", "", "", "", "operating_expense"];
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:46:  const ccValues = ["cc_2a09abd97f9b", "2026-05-10", "belanja", 100000, "catat beli barang tokopedia 100rb pakai tokopedia credit card", "pending_transfer", "", "trx_41a84be31c7e", "auto_mirror_from_transactions_v0_9", "TOKPED_CC_2026-05", "2026-04-16", "2026-05-15", "2026-05", "", "FALSE"];
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:52:  const txDuplicateKey = getValueByHeaderV10_(txHeaders, txValues, 'duplicate_key');
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:55:  const existingTx = findRowByHeaderValueV10_(txSheet, 1, 'duplicate_key', txDuplicateKey);
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:80:    source_table: 'transactions',
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:82:    target_tab: '💸 Transactions + 💳 Credit Card',
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:83:    transaction_id: getValueByHeaderV10_(txHeaders, txValues, 'transaction_id'),
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:98:  Logger.log('write_scope=transactions_plus_credit_card');
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:99:  Logger.log('transaction_id=' + getValueByHeaderV10_(txHeaders, txValues, 'transaction_id'));
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:100:  Logger.log('transactions_inserted=' + String(txInserted));
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:110:    write_scope: 'transactions_plus_credit_card',
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:111:    transaction_id: getValueByHeaderV10_(txHeaders, txValues, 'transaction_id'),
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:113:    transactions_inserted: txInserted,
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:136:function validateTransactionsHeaderV10_(sheet) {
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:137:  const expected = ["transaction_id", "date", "month", "type", "category", "subcategory", "description", "merchant", "amount", "account", "source", "status", "confidence", "raw_text", "synced_at", "notes", "currency", "review_status", "local_db_table", "local_db_rowid", "sync_hash", "duplicate_key", "created_at", "updated_at", "from_account", "to_account", "transfer_purpose", "asset_bucket", "pocket_name", "cashflow_treatment"];
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:141:  validateHeaderArrayV10_('💸 Transactions', expected, seen);
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:155:    'target_tab', 'transaction_id', 'action', 'status', 'records_seen',
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:212:    entry.transaction_id,
scripts/personal-workflow/airo_full_auto_sheets_sync.py:6:- 💸 Transactions
scripts/personal-workflow/airo_full_auto_sheets_sync.py:34:    "transaction_id", "date", "month", "type", "category", "subcategory",
scripts/personal-workflow/airo_full_auto_sheets_sync.py:37:    "local_db_table", "local_db_rowid", "sync_hash", "duplicate_key",
scripts/personal-workflow/airo_full_auto_sheets_sync.py:51:    "target_tab", "transaction_id", "action", "status", "records_seen",
scripts/personal-workflow/airo_full_auto_sheets_sync.py:59:    "purpose", "amount", "source", "raw_text", "linked_transaction_id",
scripts/personal-workflow/airo_full_auto_sheets_sync.py:90:    duplicate_key: str
scripts/personal-workflow/airo_full_auto_sheets_sync.py:145:    if target_tab == "💸 Transactions":
scripts/personal-workflow/airo_full_auto_sheets_sync.py:164:def find_existing_row(snapshot: dict[str, Any], target_tab: str, duplicate_key: str, section: str = "") -> int | None:
scripts/personal-workflow/airo_full_auto_sheets_sync.py:167:        if str(item.get("duplicate_key") or "") == str(duplicate_key or ""):
scripts/personal-workflow/airo_full_auto_sheets_sync.py:177:    transaction_id = (
scripts/personal-workflow/airo_full_auto_sheets_sync.py:178:        row.get("transaction_id")
scripts/personal-workflow/airo_full_auto_sheets_sync.py:183:        or decision.get("duplicate_key")
scripts/personal-workflow/airo_full_auto_sheets_sync.py:191:        decision.get("source_table", "transactions"),
scripts/personal-workflow/airo_full_auto_sheets_sync.py:194:        transaction_id,
scripts/personal-workflow/airo_full_auto_sheets_sync.py:211:    allowed_core = {"💸 Transactions", "💳 Credit Card"}
scripts/personal-workflow/airo_full_auto_sheets_sync.py:230:    duplicate_key = str(decision.get("duplicate_key") or "")
scripts/personal-workflow/airo_full_auto_sheets_sync.py:239:            result = ApplyResult(target_tab, duplicate_key, "insert", "success", 1, f"full_auto_v1_2 asset insert:{section}")
scripts/personal-workflow/airo_full_auto_sheets_sync.py:242:            result = ApplyResult(target_tab, duplicate_key, "insert", "success", 1, "full_auto_v1_2 insert")
scripts/personal-workflow/airo_full_auto_sheets_sync.py:244:        row_number = find_existing_row(snapshot, target_tab, duplicate_key, section)
scripts/personal-workflow/airo_full_auto_sheets_sync.py:249:                    duplicate_key,
scripts/personal-workflow/airo_full_auto_sheets_sync.py:257:                result = ApplyResult(target_tab, duplicate_key, "insert_fallback", "success", 1, "full_auto_v1_1 update_missing_row_inserted")
scripts/personal-workflow/airo_full_auto_sheets_sync.py:261:                result = ApplyResult(target_tab, duplicate_key, "update", "success", 1, f"full_auto_v1_2 asset update:{section}")
scripts/personal-workflow/airo_full_auto_sheets_sync.py:264:                result = ApplyResult(target_tab, duplicate_key, "update", "success", 1, "full_auto_v1_1 update")
scripts/personal-workflow/airo_full_auto_sheets_sync.py:266:        result = ApplyResult(target_tab, duplicate_key, "skip", "skipped", 0, "not a write candidate")
scripts/personal-workflow/airo_full_auto_sheets_sync.py:333:                "duplicate_key": d.get("duplicate_key"),
```

### 💵 Cash Ledger

Pattern: `Cash Ledger|cash session|cash_sessions|cash entries|cash_entries|amount_remaining`

```text
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_PROBE_V0_2_PASS.md:33:- 💵 Cash Ledger: not written
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:26:This verifies the Google Sheets write path while keeping Transactions, Credit Card, Review Queue, Aset, Hutang, Cash Ledger, and Cicilan Rumah untouched.
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:57:- 💵 Cash Ledger
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:18:3. 💵 Cash Ledger
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:34:| 💵 Cash Ledger | DESIGNED / HEADER_VALID / NOT_GENERALIZED | Needs route and sync completion |
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:221:### 💵 Cash Ledger
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:223:Pattern: `Cash Ledger|cash session|cash_sessions|cash entries|cash_entries|amount_remaining`
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_FIRST_LEDGER_WRITE_V0_7_PASS.md:38:- 💵 Cash Ledger
docs/personal-workflow/integration/AIRO_TOKOPEDIA_CC_WRITE_V1_0.md:51:- 💵 Cash Ledger
docs/personal-workflow/integration/AIRO_FULL_AUTO_SHEETS_SYNC_V1_1_4_TIMER_PASS.md:68:- 💵 Cash Ledger
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_SYNC_DRY_RUN_V0_1.md:92:- Cash Ledger sessions and cash entries
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:73:3. 💵 Cash Ledger
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:101:- 💵 Cash Ledger cash sessions: A1:H1
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:102:- 💵 Cash Ledger cash entries: J1:T1
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:120:| 💵 Cash Ledger | Cash session and cash entry ledger | DESIGNED / HEADER_VALID / NOT_GENERALIZED | Add route and sync completion plan |
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:144:- 💵 Cash Ledger
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:155:| saya hari ini pegang cash 100rb | 💵 Cash Ledger session |
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:156:| hari ini cash kepake beli makan 20rb | 💵 Cash Ledger entry |
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:188:   - 💵 Cash Ledger
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:207:- Cash Ledger route and dry-run mapping
docs/personal-workflow/integration/AIRO_TOKOPEDIA_CC_WRITE_V1_0_PASS.md:58:- 💵 Cash Ledger
docs/personal-workflow/integration/AIRO_FULL_AUTO_SHEETS_SYNC_V1_1.md:39:- 💵 Cash Ledger
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_HEADER_VALIDATION_V0_1.md:31:3. 💵 Cash Ledger
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_HEADER_VALIDATION_V0_1.md:46:- 💵 Cash Ledger cash sessions: A1:H1
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_HEADER_VALIDATION_V0_1.md:47:- 💵 Cash Ledger cash entries: J1:T1
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:42:3. 💵 Cash Ledger
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:193:## 6. Cash Ledger design
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:205:- amount_remaining
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:231:- New cash session with amount_start 100000
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:516:- Cash Ledger
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_HANDOFF.md:17:3. 💵 Cash Ledger
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_HANDOFF.md:66:Cash is isolated in Cash Ledger because cash spending is hard to monitor from bank history. Cash has sessions and entries.
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_HANDOFF.md:122:- Cash Ledger session created
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_HANDOFF.md:133:- Cash Ledger entry under active session
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_2_CARRYOVER.md:49:3. 💵 Cash Ledger
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_2_CARRYOVER.md:80:- 💵 Cash Ledger
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_2_CARRYOVER.md:89:- cash-on-hand message routes to 💵 Cash Ledger session
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_2_CARRYOVER.md:90:- cash spend routes to 💵 Cash Ledger entry
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_2_CARRYOVER.md:115:- gaps for Cash Ledger, Cicilan Rumah, Hutang, Review Queue, and Monthly Review
```

### 💳 Credit Card

Pattern: `Credit Card|credit_card|Tokopedia|billing_cycle|linked_txn_id|status_pocket_blu`

```text
scripts/personal-workflow/airo_credit_card_mirror_planner.py:3:AIRO Credit Card Mirror Planner v0.9.
scripts/personal-workflow/airo_credit_card_mirror_planner.py:6:- Generate 💳 Credit Card mirror operations for Tokopedia Card transactions.
scripts/personal-workflow/airo_credit_card_mirror_planner.py:7:- Apply Tokopedia Card billing cycle rule: 16th to 15th.
scripts/personal-workflow/airo_credit_card_mirror_planner.py:27:BILLING_SCRIPT = Path(__file__).resolve().with_name("airo_credit_card_billing_cycle.py")
scripts/personal-workflow/airo_credit_card_mirror_planner.py:49:def is_tokopedia_credit_card_text(value: Any) -> bool:
scripts/personal-workflow/airo_credit_card_mirror_planner.py:68:def is_tokopedia_credit_card_operation(op: dict[str, Any]) -> bool:
scripts/personal-workflow/airo_credit_card_mirror_planner.py:76:    # Legacy/direct 💳 Credit Card operations must not be mirrored again.
scripts/personal-workflow/airo_credit_card_mirror_planner.py:100:    return any(is_tokopedia_credit_card_text(value) for value in fields)
scripts/personal-workflow/airo_credit_card_mirror_planner.py:106:    for key in ("transaction_id", "linked_txn_id", "entity_id"):
scripts/personal-workflow/airo_credit_card_mirror_planner.py:133:def build_credit_card_mirror_operation(op: dict[str, Any]) -> dict[str, Any] | None:
scripts/personal-workflow/airo_credit_card_mirror_planner.py:134:    if not is_tokopedia_credit_card_operation(op):
scripts/personal-workflow/airo_credit_card_mirror_planner.py:137:    billing = load_module(BILLING_SCRIPT, "airo_credit_card_billing_cycle_v09")
scripts/personal-workflow/airo_credit_card_mirror_planner.py:146:    cycle = billing.compute_tokped_card_billing_cycle(transaction_date)
scripts/personal-workflow/airo_credit_card_mirror_planner.py:150:    merchant_app = row.get("merchant") or row.get("merchant_app") or "Tokopedia"
scripts/personal-workflow/airo_credit_card_mirror_planner.py:158:        "status_pocket_blu": "pending_transfer",
scripts/personal-workflow/airo_credit_card_mirror_planner.py:160:        "linked_txn_id": transaction_id,
scripts/personal-workflow/airo_credit_card_mirror_planner.py:162:        "billing_cycle_id": cycle.billing_cycle_id,
scripts/personal-workflow/airo_credit_card_mirror_planner.py:173:        "target_tab": "💳 Credit Card",
scripts/personal-workflow/airo_credit_card_mirror_planner.py:185:def build_credit_card_mirror_operations(planned_operations: list[dict[str, Any]]) -> list[dict[str, Any]]:
scripts/personal-workflow/airo_credit_card_mirror_planner.py:192:        mirror = build_credit_card_mirror_operation(op)
scripts/personal-workflow/airo_credit_card_mirror_planner.py:202:        cycle_id = str((op.get("row_preview") or {}).get("billing_cycle_id") or "")
scripts/personal-workflow/airo_credit_card_mirror_planner.py:207:        "by_billing_cycle_id": by_cycle,
scripts/personal-workflow/airo_credit_card_mirror_planner.py:224:    parser = argparse.ArgumentParser(description="AIRO Credit Card mirror planner v0.9.")
scripts/personal-workflow/airo_credit_card_mirror_planner.py:229:    mirror_ops = build_credit_card_mirror_operations(planned_ops)
scripts/personal-workflow/apps-script/airo_finance_sheet_key_exporter_v0_3.gs:28:      '💳 Credit Card': exportByHeaderV03_(ss, '💳 Credit Card', 3, 'linked_txn_id', null),
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:2: * AIRO Tokopedia CC Write v1.0
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:5: * - Appends one Tokopedia CC transaction to 💸 Transactions if missing.
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:6: * - Appends one mirror row to 💳 Credit Card if missing.
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:11: * - 💳 Credit Card: linked_txn_id = trx_41a84be31c7e
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:18:function airoFinanceTokopediaCcWriteV10() {
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:28:  const ccSheet = ss.getSheetByName('💳 Credit Card');
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:32:  if (!ccSheet) throw new Error('ABORT: 💳 Credit Card tab not found.');
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:44:  const txValues = ["trx_41a84be31c7e", "2026-05-10", "2026-05", "expense", "Belanja", "", "catat beli barang tokopedia 100rb pakai tokopedia credit card", "belanja", 100000, "Tokopedia CC", "telegram", "synced", 0.9, "catat beli barang tokopedia 100rb pakai tokopedia credit card", "", "", "IDR", "auto_approved", "transactions", 3, "1ed99b1b6f6bbf1e429c76b3", "transactions:trx_41a84be31c7e", "2026-05-10 09:33:21", "2026-05-10 09:33:21", "", "", "", "", "", "operating_expense"];
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:45:  const ccHeaders = ["cc_entry_id", "date", "merchant_app", "amount", "description", "status_pocket_blu", "transferred_at", "linked_txn_id", "notes", "billing_cycle_id", "billing_start", "billing_end", "statement_month", "due_date", "is_statement_locked"];
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:53:  const ccLinkedTxnId = getValueByHeaderV10_(ccHeaders, ccValues, 'linked_txn_id');
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:56:  const existingCc = findRowByHeaderValueV10_(ccSheet, 3, 'linked_txn_id', ccLinkedTxnId);
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:82:    target_tab: '💸 Transactions + 💳 Credit Card',
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:98:  Logger.log('write_scope=transactions_plus_credit_card');
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:101:  Logger.log('credit_card_inserted=' + String(ccInserted));
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:103:  Logger.log('billing_cycle_id=' + getValueByHeaderV10_(ccHeaders, ccValues, 'billing_cycle_id'));
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:110:    write_scope: 'transactions_plus_credit_card',
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:112:    linked_txn_id: ccLinkedTxnId,
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:114:    credit_card_inserted: ccInserted,
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:116:    billing_cycle_id: getValueByHeaderV10_(ccHeaders, ccValues, 'billing_cycle_id'),
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:145:  const expected = ["cc_entry_id", "date", "merchant_app", "amount", "description", "status_pocket_blu", "transferred_at", "linked_txn_id", "notes", "billing_cycle_id", "billing_start", "billing_end", "statement_month", "due_date", "is_statement_locked"];
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:149:  validateHeaderArrayV10_('💳 Credit Card', expected, seen);
scripts/personal-workflow/apps-script/airo_credit_card_billing_cycle_v0_8.gs:2: * AIRO Credit Card Billing Cycle v0.8
scripts/personal-workflow/apps-script/airo_credit_card_billing_cycle_v0_8.gs:5: * - Patch 💳 Credit Card header to support Tokopedia Card billing cycle.
scripts/personal-workflow/apps-script/airo_credit_card_billing_cycle_v0_8.gs:8: * This writes only 💳 Credit Card header/formatting cells.
scripts/personal-workflow/apps-script/airo_credit_card_billing_cycle_v0_8.gs:14:  const sheet = ss.getSheetByName('💳 Credit Card');
scripts/personal-workflow/apps-script/airo_credit_card_billing_cycle_v0_8.gs:17:    throw new Error('ABORT: 💳 Credit Card tab not found.');
scripts/personal-workflow/apps-script/airo_credit_card_billing_cycle_v0_8.gs:26:    'status_pocket_blu',
scripts/personal-workflow/apps-script/airo_credit_card_billing_cycle_v0_8.gs:28:    'linked_txn_id',
scripts/personal-workflow/apps-script/airo_credit_card_billing_cycle_v0_8.gs:38:      throw new Error('ABORT: base Credit Card header mismatch at position ' + String(i + 1) + '. Expected ' + expectedBase[i] + ', saw ' + currentBase[i]);
scripts/personal-workflow/apps-script/airo_credit_card_billing_cycle_v0_8.gs:43:    'billing_cycle_id',
scripts/personal-workflow/apps-script/airo_credit_card_billing_cycle_v0_8.gs:77:  Logger.log('write_scope=credit_card_header_only');
scripts/personal-workflow/apps-script/airo_credit_card_billing_cycle_v0_8.gs:83:  const sheet = ss.getSheetByName('💳 Credit Card');
scripts/personal-workflow/apps-script/airo_credit_card_billing_cycle_v0_8.gs:86:    throw new Error('ABORT: 💳 Credit Card tab not found.');
scripts/personal-workflow/apps-script/airo_credit_card_billing_cycle_v0_8.gs:95:    'status_pocket_blu',
scripts/personal-workflow/apps-script/airo_credit_card_billing_cycle_v0_8.gs:97:    'linked_txn_id',
scripts/personal-workflow/apps-script/airo_credit_card_billing_cycle_v0_8.gs:99:    'billing_cycle_id',
scripts/personal-workflow/apps-script/airo_credit_card_billing_cycle_v0_8.gs:129:    checked_range: '💳 Credit Card!A3:O3',
scripts/personal-workflow/apps-script/airo_credit_card_billing_cycle_v0_8.gs:160:    billing_cycle_id: 'TOKPED_CC_' + statementMonth,
scripts/personal-workflow/apps-script/airo_credit_card_billing_cycle_v0_8.gs:184:      got.billing_cycle_id !== item[4]
scripts/personal-workflow/airo_full_auto_sheets_sync.py:7:- 💳 Credit Card
scripts/personal-workflow/airo_full_auto_sheets_sync.py:44:    "status_pocket_blu", "transferred_at", "linked_txn_id", "notes",
scripts/personal-workflow/airo_full_auto_sheets_sync.py:45:    "billing_cycle_id", "billing_start", "billing_end", "statement_month",
scripts/personal-workflow/airo_full_auto_sheets_sync.py:147:    if target_tab == "💳 Credit Card":
scripts/personal-workflow/airo_full_auto_sheets_sync.py:179:        or row.get("linked_txn_id")
scripts/personal-workflow/airo_full_auto_sheets_sync.py:211:    allowed_core = {"💸 Transactions", "💳 Credit Card"}
scripts/personal-workflow/airo_full_auto_sheets_sync.py:335:                "billing_cycle_id": (d.get("row_preview") or {}).get("billing_cycle_id"),
scripts/personal-workflow/airo_full_auto_sheets_sync.py:340:        "scope": ["💸 Transactions", "💳 Credit Card", "🥇 Aset", "🔄 Sync Log"],
scripts/personal-workflow/airo_transaction_persistence.py:372:              currency, payment_method, billing_cycle, due_date, status, source,
scripts/personal-workflow/airo_sheets_sync_dry_run.py:373:            target_tab="💳 Credit Card",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:378:            duplicate_key=f"credit_card:{txid}",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:380:            reason="Tokopedia Credit Card detected",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:384:                "merchant_app": item.get("merchant") or "Tokopedia Credit Card",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:387:                "status_pocket_blu": "⏳ Belum",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:389:                "linked_txn_id": txid,
scripts/personal-workflow/airo_sheets_sync_dry_run.py:513:                        linked_txn_id = str(row_preview.get("linked_transaction_id") or "")
```

### 🏠 Cicilan Rumah

Pattern: `Cicilan Rumah|cicilan|installment|installments|cicilan_ke`

```text
scripts/personal-workflow/apps-script/airo_finance_sheet_key_exporter_v0_3.gs:30:      '🏠 Cicilan Rumah': exportByHeaderV03_(ss, '🏠 Cicilan Rumah', 11, 'payment_id', null),
scripts/personal-workflow/airo_transaction_persistence.py:46:    "cicilan": "cicilan",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:51:    "cicilan": "Cicilan",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:438:def plan_installment_payment(row: sqlite3.Row) -> PlannedOperation:
scripts/personal-workflow/airo_sheets_sync_dry_run.py:443:        "installment_payments",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:445:        item.get("installment_id"),
scripts/personal-workflow/airo_sheets_sync_dry_run.py:447:        item.get("installment_number"),
scripts/personal-workflow/airo_sheets_sync_dry_run.py:454:        target_tab="🏠 Cicilan Rumah",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:456:        source_table="installment_payments",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:459:        duplicate_key=f"installment_payment:{payment_id}",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:461:        reason="installment payment row",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:464:            "cicilan_ke": item.get("installment_number"),
scripts/personal-workflow/airo_sheets_sync_dry_run.py:534:        if "installment_payments" in tables:
scripts/personal-workflow/airo_sheets_sync_dry_run.py:535:            for row in cur.execute("SELECT rowid, * FROM installment_payments ORDER BY rowid ASC").fetchall():
scripts/personal-workflow/airo_sheets_sync_dry_run.py:536:                ops.append(plan_installment_payment(row))
scripts/personal-workflow/airo_sheets_sync_dry_run.py:585:                "Approval Queue, conflicts, installments, and installment_payments are supported when rows exist.",
scripts/personal-workflow/airo_intent_router.py:108:    if has_any(text, ["catat", "beli", "bayar", "pengeluaran", "transaksi", "cicilan", "ringkasan", "makan", "pakai"]):
scripts/personal-workflow/airo_google_sheets_client.py:43:    SheetKeyTarget("🏠 Cicilan Rumah", 11, "payment_id", None),
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_PROBE_V0_2_PASS.md:34:- 🏠 Cicilan Rumah: not written
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:26:This verifies the Google Sheets write path while keeping Transactions, Credit Card, Review Queue, Aset, Hutang, Cash Ledger, and Cicilan Rumah untouched.
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:58:- 🏠 Cicilan Rumah
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:20:5. 🏠 Cicilan Rumah
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:36:| 🏠 Cicilan Rumah | DESIGNED / HEADER_VALID / NOT_GENERALIZED | Needs route and sync completion |
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:227:docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:26:This verifies the Google Sheets write path while keeping Transactions, Credit Card, Review Queue, Aset, Hutang, Cash Ledger, and Cicilan Rumah untouched.
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:264:docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_2_CARRYOVER.md:115:- gaps for Cash Ledger, Cicilan Rumah, Hutang, Review Queue, and Monthly Review
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:354:### 🏠 Cicilan Rumah
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:356:Pattern: `Cicilan Rumah|cicilan|installment|installments|cicilan_ke`
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_FIRST_LEDGER_WRITE_V0_7_PASS.md:39:- 🏠 Cicilan Rumah
docs/personal-workflow/integration/AIRO_TOKOPEDIA_CC_WRITE_V1_0.md:52:- 🏠 Cicilan Rumah
docs/personal-workflow/integration/AIRO_FULL_AUTO_SHEETS_SYNC_V1_1_4_TIMER_PASS.md:69:- 🏠 Cicilan Rumah
docs/personal-workflow/integration/PHASE_1M_OPENCLAW_GLOBAL_COMMAND.md:34:AIRO_WORKFLOW_MODE=dry-run airo-workflow "bayar cicilan rumah 2500000" | python3 -m json.tool
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_SYNC_DRY_RUN_V0_1.md:74:### installment_payments
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_SYNC_DRY_RUN_V0_1.md:76:Target: `🏠 Cicilan Rumah`
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_SYNC_DRY_RUN_V0_1.md:108:- Installment payment: `installment_payment:<payment_id>`
docs/personal-workflow/integration/AIRO_TELEGRAM_OPTION_A_SINGLE_FRONT_DOOR_PLAN.md:76:- bayar cicilan rumah 2500000
docs/personal-workflow/integration/AIRO_TELEGRAM_OPTION_A_SINGLE_FRONT_DOOR_PLAN.md:77:- cek cicilan rumah sudah bayar ke berapa
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:75:5. 🏠 Cicilan Rumah
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:104:- 🏠 Cicilan Rumah payment history: A11:F11
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:122:| 🏠 Cicilan Rumah | House installment payment history | DESIGNED / HEADER_VALID / NOT_GENERALIZED | Add route and sync completion plan |
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:145:- 🏠 Cicilan Rumah
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:157:| hari ini sudah bayar cicilan rumah | 🏠 Cicilan Rumah |
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:189:   - 🏠 Cicilan Rumah
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:212:- Cicilan Rumah route and dry-run mapping
docs/personal-workflow/integration/AIRO_TOKOPEDIA_CC_WRITE_V1_0_PASS.md:59:- 🏠 Cicilan Rumah
docs/personal-workflow/integration/AIRO_INTEGRATION_CONTRACT.md:12:AIRO_WORKFLOW_MODE=dry-run scripts/airo_personal_workflow_call.sh "bayar cicilan rumah 2500000"
docs/personal-workflow/integration/AIRO_INTEGRATION_CONTRACT.md:49:record_installment_payment
docs/personal-workflow/integration/AIRO_INTEGRATION_CONTRACT.md:50:check_installment
docs/personal-workflow/integration/AIRO_FULL_AUTO_SHEETS_SYNC_V1_1_3_LIVE_DRY_RUN_PASS.md:32:- 🏠 Cicilan Rumah
docs/personal-workflow/integration/AIRO_FULL_AUTO_SHEETS_SYNC_V1_1.md:40:- 🏠 Cicilan Rumah
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_PREVIEW_V0_3.md:57:- 🏠 Cicilan Rumah
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_HEADER_VALIDATION_V0_1.md:33:5. 🏠 Cicilan Rumah
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_HEADER_VALIDATION_V0_1.md:49:- 🏠 Cicilan Rumah payment history: A11:F11
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:25:- installment_payments
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:26:- installments
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:44:5. 🏠 Cicilan Rumah
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:86:- Standard installment: Rp 1.543.000
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:90:- "Sisa Cicilan" in Aset is an estimated remaining cashflow obligation: (120 - last_paid_count) × standard installment.
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:109:- Cicilan: Cicilan Rumah
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:140:  - Cicilan Rumah
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:279:## 8. Cicilan Rumah design
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:281:Cicilan Rumah tracks progress and history.
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:285:- tanggal mulai cicilan: user fills later
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:286:- total cicilan: 120
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:295:- cicilan_ke
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:304:"hari ini sudah bayar cicilan rumah"
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:309:- increment cicilan_ke from last payment
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:519:- Cicilan Rumah
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:530:- hutang/cicilan summary
docs/personal-workflow/integration/PHASE_1N_RUNTIME_VISIBILITY_CHECK.md:12:AIRO_WORKFLOW_MODE=dry-run airo-workflow "bayar cicilan rumah 2500000"
docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_PHASE_2_HANDOFF.md:23:- installment payment capture
docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_PHASE_2_HANDOFF.md:24:- installment progress check
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_HANDOFF.md:19:5. 🏠 Cicilan Rumah
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_HANDOFF.md:47:- Standard installment: Rp 1.543.000
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_HANDOFF.md:74:Cicilan progress is tracked by payment history. Sisa cicilan in Aset is estimated remaining cashflow obligation, not bank principal outstanding.
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_HANDOFF.md:140:hari ini sudah bayar cicilan rumah
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_HANDOFF.md:144:- Cicilan Rumah adds next payment row
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_HANDOFF.md:146:- progress increments from latest cicilan_ke
docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_V0_1_HANDOFF.md:35:- Parser cicilan: PASS
docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_V0_1_HANDOFF.md:56:AIRO_WORKFLOW_MODE=dry-run airo-workflow "bayar cicilan rumah 2500000"
docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_V0_1_HANDOFF.md:63:catat pembayaran cicilan
```

### 🤝 Hutang

Pattern: `Hutang|hutang|debt|HT-001|remaining balance`

```text
scripts/personal-workflow/airo_transaction_persistence.py:47:    "hutang": "hutang",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:52:    "hutang": "Hutang",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:583:                "Cash/Hutang/Aset special routing now includes v1.2B asset event planner when applicable.",
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_PROBE_V0_2_PASS.md:35:- 🤝 Hutang: not written
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:26:This verifies the Google Sheets write path while keeping Transactions, Credit Card, Review Queue, Aset, Hutang, Cash Ledger, and Cicilan Rumah untouched.
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:59:- 🤝 Hutang
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:21:6. 🤝 Hutang
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:37:| 🤝 Hutang | DESIGNED / HEADER_VALID / NOT_GENERALIZED | Needs route and sync completion |
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:227:docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:26:This verifies the Google Sheets write path while keeping Transactions, Credit Card, Review Queue, Aset, Hutang, Cash Ledger, and Cicilan Rumah untouched.
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:264:docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_2_CARRYOVER.md:115:- gaps for Cash Ledger, Cicilan Rumah, Hutang, Review Queue, and Monthly Review
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:378:docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:26:This verifies the Google Sheets write path while keeping Transactions, Credit Card, Review Queue, Aset, Hutang, Cash Ledger, and Cicilan Rumah untouched.
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:382:docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:227:docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:26:This verifies the Google Sheets write path while keeping Transactions, Credit Card, Review Queue, Aset, Hutang, Cash Ledger, and Cicilan Rumah untouched.
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:383:docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:264:docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_2_CARRYOVER.md:115:- gaps for Cash Ledger, Cicilan Rumah, Hutang, Review Queue, and Monthly Review
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:426:docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:530:- hutang/cicilan summary
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:441:### 🤝 Hutang
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:443:Pattern: `Hutang|hutang|debt|HT-001|remaining balance`
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_FIRST_LEDGER_WRITE_V0_7_PASS.md:40:- 🤝 Hutang
docs/personal-workflow/integration/AIRO_TOKOPEDIA_CC_WRITE_V1_0.md:53:- 🤝 Hutang
docs/personal-workflow/integration/AIRO_FULL_AUTO_SHEETS_SYNC_V1_1_4_TIMER_PASS.md:70:- 🤝 Hutang
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_SYNC_DRY_RUN_V0_1.md:93:- Hutang payments by person
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:76:6. 🤝 Hutang
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:105:- 🤝 Hutang master: A2:H2
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:106:- 🤝 Hutang payment history: A9:H9
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:123:| 🤝 Hutang | Debt master and repayment history | DESIGNED / HEADER_VALID / NOT_GENERALIZED | Add route and sync completion plan |
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:146:- 🤝 Hutang
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:158:| hari ini bayar hutang ke mamak egit 1 juta | 🤝 Hutang |
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:190:   - 🤝 Hutang
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:213:- Hutang route and dry-run mapping
docs/personal-workflow/integration/AIRO_TOKOPEDIA_CC_WRITE_V1_0_PASS.md:60:- 🤝 Hutang
docs/personal-workflow/integration/AIRO_FULL_AUTO_SHEETS_SYNC_V1_1.md:41:- 🤝 Hutang
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_HEADER_VALIDATION_V0_1.md:34:6. 🤝 Hutang
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_HEADER_VALIDATION_V0_1.md:50:- 🤝 Hutang master: A2:H2
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_HEADER_VALIDATION_V0_1.md:51:- 🤝 Hutang payment history: A9:H9
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:45:6. 🤝 Hutang
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:57:- Hutang needs per-person principal, repayment history, and remaining balance.
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:93:Hutang active initial rows:
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:95:- HT-001 Mamak Egit: Rp 15.000.000
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:99:Total initial hutang aktif: Rp 25.000.000
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:110:- Hutang: Bayar Hutang
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:132:  - Total hutang aktif
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:141:  - Total Hutang
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:313:## 9. Hutang design
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:315:Hutang tracks debt owed by the user to people.
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:319:- hutang_id
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:324:- sisa_hutang
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:331:- hutang_id
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:342:"hari ini bayar hutang ke mamak egit 1 juta"
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:346:- Add payment history row for HT-001
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:347:- Reduce Mamak Egit remaining balance
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:348:- Optional Transactions row with type transfer/debt_payment depending sync mapping
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:518:- Hutang
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:530:- hutang/cicilan summary
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_HANDOFF.md:20:6. 🤝 Hutang
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_HANDOFF.md:51:Active debts:
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_HANDOFF.md:56:- Total hutang aktif: Rp 25.000.000
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_HANDOFF.md:76:### 5. Hutang
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_HANDOFF.md:78:Hutang is tracked per person with master balance and payment history.
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_HANDOFF.md:148:### Hutang
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_HANDOFF.md:152:hari ini bayar hutang ke mamak egit 1 juta
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_HANDOFF.md:156:- Hutang payment history row
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_HANDOFF.md:157:- HT-001 remaining balance decreases
docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_V0_1_HANDOFF.md:109:OpenClaw/Airo harus memakai airo-workflow untuk personal finance/productivity request seperti catat transaksi, credit card, cicilan, hutang, tagihan, cek cicilan, dan ringkasan bulan ini.
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_2_CARRYOVER.md:52:6. 🤝 Hutang
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_2_CARRYOVER.md:82:- 🤝 Hutang
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_2_CARRYOVER.md:92:- hutang payment routes to 🤝 Hutang
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_2_CARRYOVER.md:115:- gaps for Cash Ledger, Cicilan Rumah, Hutang, Review Queue, and Monthly Review
```

### 🥇 Aset

Pattern: `Aset|asset|assets|gold|emas|savings_transfer|Gold Ledger`

```text
scripts/personal-workflow/airo_asset_event_planner.py:1:"""Airo asset-event planner v1.2A.
scripts/personal-workflow/airo_asset_event_planner.py:3:Pure planner for Google Sheet tab `🥇 Aset`.
scripts/personal-workflow/airo_asset_event_planner.py:12:into `plan_asset_events_from_transactions`.
scripts/personal-workflow/airo_asset_event_planner.py:23:ASSET_TAB = "🥇 Aset"
scripts/personal-workflow/airo_asset_event_planner.py:24:SAVINGS_LEDGER_SECTION = "savings_transfer_ledger"
scripts/personal-workflow/airo_asset_event_planner.py:25:GOLD_LEDGER_SECTION = "gold_ledger"
scripts/personal-workflow/airo_asset_event_planner.py:43:    "gold_event_id",
scripts/personal-workflow/airo_asset_event_planner.py:94:        "asset_bucket",
scripts/personal-workflow/airo_asset_event_planner.py:245:def plan_asset_events_from_transactions(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
scripts/personal-workflow/airo_asset_event_planner.py:263:    gold = _plan_gold(row, text)
scripts/personal-workflow/airo_asset_event_planner.py:264:    if gold is not None:
scripts/personal-workflow/airo_asset_event_planner.py:265:        plans.append(gold)
scripts/personal-workflow/airo_asset_event_planner.py:317:        "notes": "planned_by_airo_asset_event_planner_v1_2A",
scripts/personal-workflow/airo_asset_event_planner.py:322:def _plan_gold(row: dict[str, Any], text: str) -> AssetPlan | None:
scripts/personal-workflow/airo_asset_event_planner.py:323:    asset_bucket = _clean(row.get("asset_bucket")).lower()
scripts/personal-workflow/airo_asset_event_planner.py:324:    if "emas" not in text and "gold" not in text and asset_bucket not in {"emas", "gold"}:
scripts/personal-workflow/airo_asset_event_planner.py:334:    elif re.search(r"\b(beli|buy|tambah|nabun[g]? emas)\b", text):
scripts/personal-workflow/airo_asset_event_planner.py:345:    sync_hash = _sync_hash("gold", trx_id, _date(row), action, grams, total, raw)
scripts/personal-workflow/airo_asset_event_planner.py:346:    event_id = _hash("gold", trx_id or raw, _date(row), action, grams, total)
scripts/personal-workflow/airo_asset_event_planner.py:349:        "gold_event_id": event_id,
scripts/personal-workflow/airo_asset_event_planner.py:361:        "notes": "planned_by_airo_asset_event_planner_v1_2A; gram_is_canonical_quantity",
scripts/personal-workflow/airo_asset_event_planner.py:363:    return AssetPlan(ASSET_TAB, GOLD_LEDGER_SECTION, event_id, sync_hash, out, "gold event detected")
scripts/personal-workflow/airo_asset_event_planner.py:370:        {"id": "trx_demo_3", "transaction_date": "2026-05-10", "note": "beli emas 1 gram 1800000 pakai bca", "source": "demo"},
scripts/personal-workflow/airo_asset_event_planner.py:373:    print(json.dumps(plan_asset_events_from_transactions(sample), ensure_ascii=False, indent=2))
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:43:  const txHeaders = ["transaction_id", "date", "month", "type", "category", "subcategory", "description", "merchant", "amount", "account", "source", "status", "confidence", "raw_text", "synced_at", "notes", "currency", "review_status", "local_db_table", "local_db_rowid", "sync_hash", "duplicate_key", "created_at", "updated_at", "from_account", "to_account", "transfer_purpose", "asset_bucket", "pocket_name", "cashflow_treatment"];
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:137:  const expected = ["transaction_id", "date", "month", "type", "category", "subcategory", "description", "merchant", "amount", "account", "source", "status", "confidence", "raw_text", "synced_at", "notes", "currency", "review_status", "local_db_table", "local_db_rowid", "sync_hash", "duplicate_key", "created_at", "updated_at", "from_account", "to_account", "transfer_purpose", "asset_bucket", "pocket_name", "cashflow_treatment"];
scripts/personal-workflow/airo_full_auto_sheets_sync.py:39:    "asset_bucket", "pocket_name", "cashflow_treatment",
scripts/personal-workflow/airo_full_auto_sheets_sync.py:64:    "gold_event_id", "date", "action", "grams_in", "grams_out",
scripts/personal-workflow/airo_full_auto_sheets_sync.py:70:def asset_append_range(section: str) -> str:
scripts/personal-workflow/airo_full_auto_sheets_sync.py:71:    if section == "savings_transfer_ledger":
scripts/personal-workflow/airo_full_auto_sheets_sync.py:73:    if section == "gold_ledger":
scripts/personal-workflow/airo_full_auto_sheets_sync.py:75:    raise ValueError(f"Unsupported 🥇 Aset section: {section}")
scripts/personal-workflow/airo_full_auto_sheets_sync.py:77:def asset_update_range(section: str, row_number: int) -> str:
scripts/personal-workflow/airo_full_auto_sheets_sync.py:78:    if section == "savings_transfer_ledger":
scripts/personal-workflow/airo_full_auto_sheets_sync.py:80:    if section == "gold_ledger":
scripts/personal-workflow/airo_full_auto_sheets_sync.py:82:    raise ValueError(f"Unsupported 🥇 Aset section: {section}")
scripts/personal-workflow/airo_full_auto_sheets_sync.py:151:    if target_tab == "🥇 Aset" and section == "savings_transfer_ledger":
scripts/personal-workflow/airo_full_auto_sheets_sync.py:153:    if target_tab == "🥇 Aset" and section == "gold_ledger":
scripts/personal-workflow/airo_full_auto_sheets_sync.py:159:    if target_tab == "🥇 Aset" and section:
scripts/personal-workflow/airo_full_auto_sheets_sync.py:181:        or row.get("gold_event_id")
scripts/personal-workflow/airo_full_auto_sheets_sync.py:222:        if target_tab == "🥇 Aset" and action in {"insert_candidate", "update_candidate"}:
scripts/personal-workflow/airo_full_auto_sheets_sync.py:237:        if target_tab == "🥇 Aset":
scripts/personal-workflow/airo_full_auto_sheets_sync.py:238:            client.append_values_to_range(target_tab, asset_append_range(section), values)
scripts/personal-workflow/airo_full_auto_sheets_sync.py:239:            result = ApplyResult(target_tab, duplicate_key, "insert", "success", 1, f"full_auto_v1_2 asset insert:{section}")
scripts/personal-workflow/airo_full_auto_sheets_sync.py:246:            if target_tab == "🥇 Aset":
scripts/personal-workflow/airo_full_auto_sheets_sync.py:253:                    f"asset update row not found for section:{section}; refusing insert_fallback",
scripts/personal-workflow/airo_full_auto_sheets_sync.py:259:            if target_tab == "🥇 Aset":
scripts/personal-workflow/airo_full_auto_sheets_sync.py:260:                client.update_values_to_range(target_tab, asset_update_range(section, row_number), values)
scripts/personal-workflow/airo_full_auto_sheets_sync.py:261:                result = ApplyResult(target_tab, duplicate_key, "update", "success", 1, f"full_auto_v1_2 asset update:{section}")
scripts/personal-workflow/airo_full_auto_sheets_sync.py:340:        "scope": ["💸 Transactions", "💳 Credit Card", "🥇 Aset", "🔄 Sync Log"],
scripts/personal-workflow/airo_transaction_persistence.py:228:            "cashflow_treatment": "asset_transfer",
scripts/personal-workflow/airo_transaction_persistence.py:255:    if "emas" in text or re.search(r"\bgold\b", text):
scripts/personal-workflow/airo_transaction_persistence.py:257:            "intent": "gold_asset",
scripts/personal-workflow/airo_transaction_persistence.py:260:            "cashflow_treatment": "asset_purchase",
scripts/personal-workflow/airo_transaction_persistence.py:302:        (account_id, account_name, "asset", account_name, "active", now, now),
scripts/personal-workflow/airo_sheets_sync_dry_run.py:26:ASSET_PLANNER_SCRIPT = Path(__file__).resolve().with_name("airo_asset_event_planner.py")
scripts/personal-workflow/airo_sheets_sync_dry_run.py:53:    "aset": "Aset",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:151:def load_asset_planner_module():
scripts/personal-workflow/airo_sheets_sync_dry_run.py:155:    spec = importlib.util.spec_from_file_location("airo_asset_event_planner", ASSET_PLANNER_SCRIPT)
scripts/personal-workflow/airo_sheets_sync_dry_run.py:170:        return "asset_transfer", "transfer"
scripts/personal-workflow/airo_sheets_sync_dry_run.py:181:    if "emas" in text or "gold" in text or cat == "investasi":
scripts/personal-workflow/airo_sheets_sync_dry_run.py:182:        return "asset_purchase", "asset_purchase"
scripts/personal-workflow/airo_sheets_sync_dry_run.py:354:        "asset_bucket": "",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:497:        asset_planner_warning = ""
scripts/personal-workflow/airo_sheets_sync_dry_run.py:506:                asset_planner = load_asset_planner_module()
scripts/personal-workflow/airo_sheets_sync_dry_run.py:507:                if asset_planner is not None:
scripts/personal-workflow/airo_sheets_sync_dry_run.py:510:                    for asset_plan in asset_planner.plan_asset_events_from_transactions(tx_dicts):
scripts/personal-workflow/airo_sheets_sync_dry_run.py:511:                        row_preview = dict(asset_plan.get("row") or {})
scripts/personal-workflow/airo_sheets_sync_dry_run.py:512:                        section = str(asset_plan.get("section") or "")
scripts/personal-workflow/airo_sheets_sync_dry_run.py:516:                            target_tab=str(asset_plan.get("target_tab") or "🥇 Aset"),
scripts/personal-workflow/airo_sheets_sync_dry_run.py:520:                            entity_id=linked_txn_id or str(asset_plan.get("duplicate_key") or ""),
scripts/personal-workflow/airo_sheets_sync_dry_run.py:521:                            duplicate_key=str(asset_plan.get("duplicate_key") or ""),
scripts/personal-workflow/airo_sheets_sync_dry_run.py:522:                            sync_hash=str(asset_plan.get("sync_hash") or ""),
scripts/personal-workflow/airo_sheets_sync_dry_run.py:523:                            reason=str(asset_plan.get("reason") or "asset event detected"),
scripts/personal-workflow/airo_sheets_sync_dry_run.py:528:                asset_planner_warning = "asset planner skipped: " + str(exc)
scripts/personal-workflow/airo_sheets_sync_dry_run.py:583:                "Cash/Hutang/Aset special routing now includes v1.2B asset event planner when applicable.",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:584:                asset_planner_warning,
scripts/personal-workflow/airo_sheets_sync_write_preview.py:147:    lookup_tab = f"{target_tab}::{section}" if target_tab == "🥇 Aset" and section else target_tab
scripts/personal-workflow/airo_google_sheets_client.py:45:    SheetKeyTarget("🥇 Aset", 3, "savings_event_id", "sync_hash", "🥇 Aset::savings_transfer_ledger"),
scripts/personal-workflow/airo_google_sheets_client.py:46:    SheetKeyTarget("🥇 Aset", 24, "gold_event_id", "sync_hash", "🥇 Aset::gold_ledger"),
```

### 📅 Monthly Review

Pattern: `Monthly Review|monthly review|category breakdown|Snapshot Bulan Ini`

```text
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_PROBE_V0_2_PASS.md:37:- 📅 Monthly Review: not written
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:61:- 📅 Monthly Review
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:23:8. 📅 Monthly Review
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:39:| 📅 Monthly Review | DESIGNED / HEADER_VALID / REPORTING | Define refresh/report behavior, not raw capture write |
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:264:docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_2_CARRYOVER.md:115:- gaps for Cash Ledger, Cicilan Rumah, Hutang, Review Queue, and Monthly Review
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:383:docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:264:docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_2_CARRYOVER.md:115:- gaps for Cash Ledger, Cicilan Rumah, Hutang, Review Queue, and Monthly Review
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:455:docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:264:docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_2_CARRYOVER.md:115:- gaps for Cash Ledger, Cicilan Rumah, Hutang, Review Queue, and Monthly Review
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:458:docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:383:docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:264:docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_2_CARRYOVER.md:115:- gaps for Cash Ledger, Cicilan Rumah, Hutang, Review Queue, and Monthly Review
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:511:docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_2_CARRYOVER.md:115:- gaps for Cash Ledger, Cicilan Rumah, Hutang, Review Queue, and Monthly Review
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:601:### 📅 Monthly Review
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:603:Pattern: `Monthly Review|monthly review|category breakdown|Snapshot Bulan Ini`
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_FIRST_LEDGER_WRITE_V0_7_PASS.md:42:- 📅 Monthly Review
docs/personal-workflow/integration/AIRO_TOKOPEDIA_CC_WRITE_V1_0.md:55:- 📅 Monthly Review
docs/personal-workflow/integration/AIRO_FULL_AUTO_SHEETS_SYNC_V1_1_4_TIMER_PASS.md:72:- 📅 Monthly Review
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:78:8. 📅 Monthly Review
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:110:- 📅 Monthly Review category breakdown: A12:E12
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:125:| 📅 Monthly Review | Reporting and monthly category review | DESIGNED / HEADER_VALID / REPORTING | Define refresh/report behavior |
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:148:- 📅 Monthly Review
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:192:   - 📅 Monthly Review
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:217:- Monthly Review reporting refresh
docs/personal-workflow/integration/AIRO_TOKOPEDIA_CC_WRITE_V1_0_PASS.md:62:- 📅 Monthly Review
docs/personal-workflow/integration/AIRO_FULL_AUTO_SHEETS_SYNC_V1_1.md:43:- 📅 Monthly Review
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_HEADER_VALIDATION_V0_1.md:36:8. 📅 Monthly Review
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_HEADER_VALIDATION_V0_1.md:55:- 📅 Monthly Review category breakdown: A12:E12
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:47:8. 📅 Monthly Review
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:134:- Snapshot Bulan Ini:
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:511:## 12. Monthly Review
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:513:Monthly Review is formula-driven. It reads:
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_HANDOFF.md:22:8. 📅 Monthly Review
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_2_CARRYOVER.md:54:8. 📅 Monthly Review
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_2_CARRYOVER.md:84:- 📅 Monthly Review
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_2_CARRYOVER.md:115:- gaps for Cash Ledger, Cicilan Rumah, Hutang, Review Queue, and Monthly Review
```

### 🧾 Review Queue

Pattern: `Review Queue|review_queue|approval_queue|ambiguity|confidence|review_status`

```text
scripts/personal-workflow/airo_approval_queue.py:18:    db = root / "approval_queue.sqlite"
scripts/personal-workflow/airo_approval_queue.py:22:    create table if not exists approval_queue (
scripts/personal-workflow/airo_approval_queue.py:53:    insert into approval_queue
scripts/personal-workflow/airo_approval_queue.py:76:        rows = con.execute("select * from approval_queue order by id desc limit ?", (args.limit,)).fetchall()
scripts/personal-workflow/airo_approval_queue.py:78:        rows = con.execute("select * from approval_queue where status=? order by id desc limit ?", (args.status, args.limit)).fetchall()
scripts/personal-workflow/airo_approval_queue.py:84:    row = con.execute("select * from approval_queue where id=?", (args.id,)).fetchone()
scripts/personal-workflow/airo_approval_queue.py:93:    con.execute("update approval_queue set status=?, approval_note=?, updated_at=? where id=?", (status, args.note, now(), args.id))
scripts/personal-workflow/airo_approval_queue.py:100:    rows = con.execute("select * from approval_queue order by id desc limit 100").fetchall()
scripts/personal-workflow/airo_local_dashboard.py:15:    db = root / "approval_queue.sqlite"
scripts/personal-workflow/airo_local_dashboard.py:20:    rows = con.execute("select * from approval_queue order by id desc limit ?", (limit,)).fetchall()
scripts/personal-workflow/airo_local_dashboard.py:102:        "approval_queue_exists": queue["exists"],
scripts/personal-workflow/airo_queue_executor.py:18:    return Path(root).expanduser().resolve() / "approval_queue.sqlite"
scripts/personal-workflow/airo_queue_executor.py:31:    row = con.execute("select * from approval_queue where id=?", (item_id,)).fetchone()
scripts/personal-workflow/airo_queue_executor.py:45:    con.execute("update approval_queue set status=?, approval_note=?, updated_at=? where id=?", ("executed", note, now(), item_id))
scripts/personal-workflow/airo_transaction_executor.py:33:    return Path(root).expanduser().resolve() / "approval_queue.sqlite"
scripts/personal-workflow/airo_transaction_executor.py:52:    row = con.execute("select * from approval_queue where id=?", (item_id,)).fetchone()
scripts/personal-workflow/airo_transaction_executor.py:65:    con.execute("update approval_queue set status=?, approval_note=?, updated_at=? where id=?", ("executed", note, now(), item_id))
scripts/personal-workflow/airo_action_gate.py:5:QUEUE = Path("scripts/personal-workflow/airo_approval_queue.py")
scripts/personal-workflow/airo_approval_review.py:15:    return Path(root).expanduser().resolve() / "approval_queue.sqlite"
scripts/personal-workflow/airo_approval_review.py:49:    row = con.execute("select * from approval_queue where id=?", (item_id,)).fetchone()
scripts/personal-workflow/airo_approval_review.py:150:        "update approval_queue set status=?, approval_note=?, updated_at=? where id=?",
scripts/personal-workflow/airo_approval_review.py:218:            rows = con.execute("select * from approval_queue order by id desc limit ?", (args.limit,)).fetchall()
scripts/personal-workflow/airo_approval_review.py:220:            rows = con.execute("select * from approval_queue where status=? order by id desc limit ?", (args.status, args.limit)).fetchall()
scripts/personal-workflow/apps-script/airo_finance_sheet_key_exporter_v0_3.gs:29:      '🧾 Review Queue': exportByHeaderV03_(ss, '🧾 Review Queue', 1, 'queue_id', 'sync_hash'),
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:43:  const txHeaders = ["transaction_id", "date", "month", "type", "category", "subcategory", "description", "merchant", "amount", "account", "source", "status", "confidence", "raw_text", "synced_at", "notes", "currency", "review_status", "local_db_table", "local_db_rowid", "sync_hash", "duplicate_key", "created_at", "updated_at", "from_account", "to_account", "transfer_purpose", "asset_bucket", "pocket_name", "cashflow_treatment"];
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:137:  const expected = ["transaction_id", "date", "month", "type", "category", "subcategory", "description", "merchant", "amount", "account", "source", "status", "confidence", "raw_text", "synced_at", "notes", "currency", "review_status", "local_db_table", "local_db_rowid", "sync_hash", "duplicate_key", "created_at", "updated_at", "from_account", "to_account", "transfer_purpose", "asset_bucket", "pocket_name", "cashflow_treatment"];
scripts/personal-workflow/airo_full_auto_sheets_sync.py:36:    "confidence", "raw_text", "synced_at", "notes", "currency", "review_status",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:259:            target_tab="🧾 Review Queue",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:260:            action="route_review_queue",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:276:                "review_status": "pending",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:298:            target_tab="🧾 Review Queue",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:299:            action="route_review_queue",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:317:                "review_status": "pending",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:339:        "confidence": 0.90,
scripts/personal-workflow/airo_sheets_sync_dry_run.py:344:        "review_status": "auto_approved",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:397:def plan_approval_queue(row: sqlite3.Row) -> PlannedOperation:
scripts/personal-workflow/airo_sheets_sync_dry_run.py:402:        "approval_queue",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:413:        target_tab="🧾 Review Queue",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:415:        source_table="approval_queue",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:418:        duplicate_key=f"review:approval_queue:{rowid}",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:424:            "source": "sqlite_approval_queue",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:428:            "review_status": item.get("status") or "pending",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:430:            "local_db_table": "approval_queue",
scripts/personal-workflow/airo_sheets_sync_dry_run.py:530:        if "approval_queue" in tables:
scripts/personal-workflow/airo_sheets_sync_dry_run.py:531:            for row in cur.execute("SELECT rowid, * FROM approval_queue ORDER BY rowid ASC").fetchall():
scripts/personal-workflow/airo_sheets_sync_dry_run.py:532:                ops.append(plan_approval_queue(row))
scripts/personal-workflow/airo_daily.py:37:    db = root / "approval_queue.sqlite"
scripts/personal-workflow/airo_daily.py:53:    rows = con.execute("select * from approval_queue order by id desc limit ?", (limit,)).fetchall()
scripts/personal-workflow/airo_executor_recommend.py:26:    return Path(root).expanduser().resolve() / "approval_queue.sqlite"
scripts/personal-workflow/airo_executor_recommend.py:58:    row = con.execute("select * from approval_queue where id=?", (item_id,)).fetchone()
scripts/personal-workflow/airo_executor_recommend.py:172:        rows = con.execute("select * from approval_queue where status='approved' order by id desc limit ?", (args.limit,)).fetchall()
scripts/personal-workflow/airo_executor_recommend.py:189:            "select * from approval_queue where status in ('pending','approved') order by id desc limit ?",
scripts/personal-workflow/airo_intent_router.py:28:            "confidence": "high",
scripts/personal-workflow/airo_intent_router.py:43:            "confidence": "high",
scripts/personal-workflow/airo_intent_router.py:57:            "intent": "approval_queue_view",
scripts/personal-workflow/airo_intent_router.py:58:            "confidence": "high",
scripts/personal-workflow/airo_intent_router.py:72:            "confidence": "high",
scripts/personal-workflow/airo_intent_router.py:86:            "confidence": "high",
scripts/personal-workflow/airo_intent_router.py:100:            "confidence": "high",
scripts/personal-workflow/airo_intent_router.py:114:            "confidence": "medium",
scripts/personal-workflow/airo_intent_router.py:128:        "confidence": "low",
scripts/personal-workflow/airoctl.py:10:    "queue": ROOT / "airo_approval_queue.py",
scripts/personal-workflow/airo_ops_dashboard.py:57:    db = root / "approval_queue.sqlite"
scripts/personal-workflow/airo_ops_dashboard.py:73:    rows = con.execute("select * from approval_queue order by id desc limit ?", (limit,)).fetchall()
scripts/personal-workflow/airo_google_sheets_client.py:42:    SheetKeyTarget("🧾 Review Queue", 1, "queue_id", "sync_hash"),
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_PREVIEW_V0_3_PASS.md:42:- 🧾 Review Queue
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_PROBE_V0_2_PASS.md:32:- 🧾 Review Queue: not written
docs/personal-workflow/integration/AIRO_FINANCE_LANGUAGE_CONTRACT_V1_0.md:67:- gold without price goes to Review Queue.
docs/personal-workflow/integration/AIRO_FINANCE_LANGUAGE_CONTRACT_V1_0.md:69:Ambiguous parser cases go to Review Queue.
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:26:This verifies the Google Sheets write path while keeping Transactions, Credit Card, Review Queue, Aset, Hutang, Cash Ledger, and Cicilan Rumah untouched.
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:56:- 🧾 Review Queue
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:24:9. 🧾 Review Queue
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:40:| 🧾 Review Queue | DESIGNED / HEADER_VALID / NOT_GENERALIZED | Needed as parser ambiguity guardrail |
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:52:scripts/personal-workflow/airo_approval_queue.py:98:def cmd_dashboard(args):
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:53:scripts/personal-workflow/airo_approval_queue.py:105:    out_dir = Path(args.output).expanduser().resolve() if args.output else Path(args.root).expanduser().resolve() / "dashboard"
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:54:scripts/personal-workflow/airo_approval_queue.py:135:<p class="small">Generated {html.escape(now())}. Local dashboard only. No action is executed from this page.</p>
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:55:scripts/personal-workflow/airo_approval_queue.py:146:    emit({"ok": True, "operation": "dashboard_generate", "db": str(db), "dashboard": str(out_file), "count": len(items)})
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:56:scripts/personal-workflow/airo_approval_queue.py:176:    d = sub.add_parser("dashboard")
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:57:scripts/personal-workflow/airo_approval_queue.py:178:    d.set_defaults(func=cmd_dashboard)
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:111:docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:52:scripts/personal-workflow/airo_approval_queue.py:98:def cmd_dashboard(args):
```

### ⚙️ Settings

Pattern: `Settings|approval phrase|write gate|write-gate|APPROVE GOOGLE SHEETS`

```text
scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs:12: * - Put the exact phrase in ⚙️ Settings column B where column A is:
scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs:16: * I APPROVE GOOGLE SHEETS WRITE FOR AIRO FINANCE
scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs:22:  const expectedApproval = 'I APPROVE GOOGLE SHEETS WRITE FOR AIRO FINANCE';
scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs:25:    throw new Error('ABORT: Google Sheets write approval phrase missing or invalid.');
scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs:81:  const sheet = ss.getSheetByName('⚙️ Settings');
scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs:83:    throw new Error('ABORT: ⚙️ Settings tab not found.');
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:14: * - ⚙️ Settings / Google Write Approval Phrase
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:15: * - I APPROVE GOOGLE SHEETS WRITE FOR AIRO FINANCE
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:21:  const expectedApproval = 'I APPROVE GOOGLE SHEETS WRITE FOR AIRO FINANCE';
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:24:    throw new Error('ABORT: Google Sheets write approval phrase missing or invalid.');
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:122:  const sheet = ss.getSheetByName('⚙️ Settings');
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:123:  if (!sheet) throw new Error('ABORT: ⚙️ Settings tab not found.');
scripts/personal-workflow/airo_full_auto_sheets_sync.py:10:No per-write approval phrase.
scripts/personal-workflow/airo_sheets_ledger_write_v0_4.py:13:- Enforce approval phrase and write scope before any future write mode.
scripts/personal-workflow/airo_sheets_ledger_write_v0_4.py:28:APPROVAL_PHRASE = "I APPROVE GOOGLE SHEETS WRITE FOR AIRO FINANCE"
scripts/personal-workflow/airo_sheets_ledger_write_v0_4.py:44:        raise SystemExit("ABORT: Google Sheets write approval phrase missing or invalid.")
scripts/personal-workflow/airo_sheets_ledger_write_v0_4.py:90:            "approval phrase is required for future write mode",
scripts/personal-workflow/airo_sheets_ledger_write_v0_4.py:106:        help="Exact approval phrase required only for future write mode.",
scripts/personal-workflow/airo_google_sheets_client.py:13:No approval phrase.
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_PROBE_V0_2_PASS.md:10:The Apps Script write-gate probe was run successfully.
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_PROBE_V0_2_PASS.md:47:The temporary approval phrase in ⚙️ Settings may be cleared after the probe.
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_PROBE_V0_2_PASS.md:51:I APPROVE GOOGLE SHEETS WRITE FOR AIRO FINANCE
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:30:Real write requires exact approval phrase:
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:32:I APPROVE GOOGLE SHEETS WRITE FOR AIRO FINANCE
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:34:For the Apps Script write probe artifact, the phrase is read from the Settings sheet.
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:38:1. open ⚙️ Settings
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:40:3. set its value in column B to the exact approval phrase
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:62:- ⚙️ Settings, except user manually entering approval phrase
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:76:- validates approval phrase from ⚙️ Settings
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:25:10. ⚙️ Settings
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:41:| ⚙️ Settings | CONFIG_ONLY | Do not use as ledger target |
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:727:### ⚙️ Settings
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:729:Pattern: `Settings|approval phrase|write gate|write-gate|APPROVE GOOGLE SHEETS`
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:732:scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs:12: * - Put the exact phrase in ⚙️ Settings column B where column A is:
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:733:scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs:16: * I APPROVE GOOGLE SHEETS WRITE FOR AIRO FINANCE
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:734:scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs:22:  const expectedApproval = 'I APPROVE GOOGLE SHEETS WRITE FOR AIRO FINANCE';
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:735:scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs:25:    throw new Error('ABORT: Google Sheets write approval phrase missing or invalid.');
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:736:scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs:81:  const sheet = ss.getSheetByName('⚙️ Settings');
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:737:scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs:83:    throw new Error('ABORT: ⚙️ Settings tab not found.');
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:738:scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:14: * - ⚙️ Settings / Google Write Approval Phrase
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:739:scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:15: * - I APPROVE GOOGLE SHEETS WRITE FOR AIRO FINANCE
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:740:scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:21:  const expectedApproval = 'I APPROVE GOOGLE SHEETS WRITE FOR AIRO FINANCE';
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:741:scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:24:    throw new Error('ABORT: Google Sheets write approval phrase missing or invalid.');
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:742:scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:122:  const sheet = ss.getSheetByName('⚙️ Settings');
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:743:scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:123:  if (!sheet) throw new Error('ABORT: ⚙️ Settings tab not found.');
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:744:scripts/personal-workflow/airo_full_auto_sheets_sync.py:10:No per-write approval phrase.
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:745:scripts/personal-workflow/airo_sheets_ledger_write_v0_4.py:13:- Enforce approval phrase and write scope before any future write mode.
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:746:scripts/personal-workflow/airo_sheets_ledger_write_v0_4.py:28:APPROVAL_PHRASE = "I APPROVE GOOGLE SHEETS WRITE FOR AIRO FINANCE"
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:747:scripts/personal-workflow/airo_sheets_ledger_write_v0_4.py:44:        raise SystemExit("ABORT: Google Sheets write approval phrase missing or invalid.")
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:748:scripts/personal-workflow/airo_sheets_ledger_write_v0_4.py:90:            "approval phrase is required for future write mode",
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:749:scripts/personal-workflow/airo_sheets_ledger_write_v0_4.py:106:        help="Exact approval phrase required only for future write mode.",
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:750:scripts/personal-workflow/airo_google_sheets_client.py:13:No approval phrase.
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:751:docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_PROBE_V0_2_PASS.md:10:The Apps Script write-gate probe was run successfully.
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:752:docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_PROBE_V0_2_PASS.md:47:The temporary approval phrase in ⚙️ Settings may be cleared after the probe.
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:753:docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_PROBE_V0_2_PASS.md:51:I APPROVE GOOGLE SHEETS WRITE FOR AIRO FINANCE
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:754:docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:30:Real write requires exact approval phrase:
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:755:docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:32:I APPROVE GOOGLE SHEETS WRITE FOR AIRO FINANCE
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:756:docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:34:For the Apps Script write probe artifact, the phrase is read from the Settings sheet.
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:757:docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:38:1. open ⚙️ Settings
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:758:docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:40:3. set its value in column B to the exact approval phrase
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:759:docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:62:- ⚙️ Settings, except user manually entering approval phrase
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:760:docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:76:- validates approval phrase from ⚙️ Settings
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:761:docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:25:10. ⚙️ Settings
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:762:docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:41:| ⚙️ Settings | CONFIG_ONLY | D
docs/personal-workflow/integration/AIRO_TOKOPEDIA_CC_WRITE_V1_0.md:59:Requires exact approval phrase in ⚙️ Settings:
docs/personal-workflow/integration/AIRO_TOKOPEDIA_CC_WRITE_V1_0.md:61:I APPROVE GOOGLE SHEETS WRITE FOR AIRO FINANCE
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_SYNC_DRY_RUN_V0_1.md:138:`I APPROVE GOOGLE SHEETS WRITE FOR AIRO FINANCE`
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_LEDGER_WRITE_V0_4.md:35:Requires exact approval phrase:
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_LEDGER_WRITE_V0_4.md:37:`I APPROVE GOOGLE SHEETS WRITE FOR AIRO FINANCE`
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:80:10. ⚙️ Settings
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_COMPLETION_PLAN.md:127:| ⚙️ Settings | Config and approval gate surface | CONFIG_ONLY | Do not use as finance ledger target |
docs/personal-workflow/integration/AIRO_FULL_AUTO_SHEETS_SYNC_V1_1.md:14:No per-write approval phrase.
docs/personal-workflow/integration/AIRO_FULL_AUTO_SHEETS_SYNC_V1_1.md:84:No approval phrase is required.
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_HEADER_VALIDATION_V0_1.md:38:10. ⚙️ Settings
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_HEADER_VALIDATION_V0_1.md:99:Design Google Sheets write-gate behavior.
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_HEADER_VALIDATION_V0_1.md:103:1. explicit user approval phrase
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_HEADER_VALIDATION_V0_1.md:116:I APPROVE GOOGLE SHEETS WRITE FOR AIRO FINANCE
docs/personal-workflow/integration/AIRO_FULL_AUTO_ASSET_SYNC_V1_2B_INTEGRATION.md:33:- No approval phrase is required.
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_DESIGN_LOG.md:49:10. ⚙️ Settings
docs/personal-workflow/handoff/AIRO_GOOGLE_SHEET_FINANCE_V1_1_8_HANDOFF.md:24:10. ⚙️ Settings
```

### 🔄 Sync Log

Pattern: `Sync Log|sync_log|run_id|records_inserted|records_skipped|records_failed`

```text
scripts/personal-workflow/apps-script/airo_finance_sheet_key_exporter_v0_3.gs:31:      '🔄 Sync Log': exportByHeaderV03_(ss, '🔄 Sync Log', 2, 'sync_id', null)
scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs:5: * - Appends one probe row to 🔄 Sync Log only.
scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs:28:  const syncLog = ss.getSheetByName('🔄 Sync Log');
scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs:30:    throw new Error('ABORT: 🔄 Sync Log tab not found.');
scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs:46:    '🔄 Sync Log',
scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs:66:  Logger.log('write_scope=sync_log_only');
scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs:68:  Logger.log('run_id=' + runId);
scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs:73:    write_scope: 'sync_log_only',
scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs:75:    run_id: runId,
scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs:102:    'run_id',
scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs:111:    'records_inserted',
scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs:113:    'records_skipped',
scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs:114:    'records_failed',
scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs:131:    throw new Error('ABORT: 🔄 Sync Log missing headers: ' + missing.join(', '));
scripts/personal-workflow/apps-script/airo_finance_write_gate_v0_2.gs:137:        'ABORT: 🔄 Sync Log header order mismatch at position ' +
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:7: * - Appends one audit row to 🔄 Sync Log.
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:29:  const syncLog = ss.getSheetByName('🔄 Sync Log');
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:33:  if (!syncLog) throw new Error('ABORT: 🔄 Sync Log tab not found.');
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:79:    run_id: runId,
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:87:    records_inserted: txInserted + ccInserted,
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:89:    records_skipped: skipped,
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:90:    records_failed: 0,
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:102:  Logger.log('records_skipped=' + String(skipped));
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:104:  Logger.log('run_id=' + runId);
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:115:    records_skipped: skipped,
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:117:    run_id: runId
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:154:    'sync_id', 'run_id', 'source_db', 'source_table', 'source_rowid',
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:156:    'records_inserted', 'records_updated', 'records_skipped', 'records_failed',
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:162:  validateHeaderArrayV10_('🔄 Sync Log', expected, seen);
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:207:    entry.run_id,
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:216:    entry.records_inserted,
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:218:    entry.records_skipped,
scripts/personal-workflow/apps-script/airo_tokopedia_cc_write_v1_0.gs:219:    entry.records_failed,
scripts/personal-workflow/airo_full_auto_sheets_sync.py:8:- 🔄 Sync Log
scripts/personal-workflow/airo_full_auto_sheets_sync.py:50:    "sync_id", "run_id", "source_db", "source_table", "source_rowid",
scripts/personal-workflow/airo_full_auto_sheets_sync.py:52:    "records_inserted", "records_updated", "records_skipped", "records_failed",
scripts/personal-workflow/airo_full_auto_sheets_sync.py:149:    if target_tab == "🔄 Sync Log":
scripts/personal-workflow/airo_full_auto_sheets_sync.py:174:def build_sync_log_row(run_id: str, decision: dict[str, Any], action: str, status: str, message: str) -> list[Any]:
scripts/personal-workflow/airo_full_auto_sheets_sync.py:189:        run_id,
scripts/personal-workflow/airo_full_auto_sheets_sync.py:228:def apply_decision(client, snapshot: dict[str, Any], decision: dict[str, Any], run_id: str) -> ApplyResult:
scripts/personal-workflow/airo_full_auto_sheets_sync.py:268:    client.append_values("🔄 Sync Log", build_sync_log_row(run_id, decision, result.action, result.status, result.message))
scripts/personal-workflow/airo_full_auto_sheets_sync.py:305:    run_id = "full_auto_v1_2_" + datetime.now().strftime("%Y%m%d_%H%M%S")
scripts/personal-workflow/airo_full_auto_sheets_sync.py:312:            results.append(apply_decision(client, snapshot, decision, run_id))
scripts/personal-workflow/airo_full_auto_sheets_sync.py:321:        "run_id": run_id,
scripts/personal-workflow/airo_full_auto_sheets_sync.py:340:        "scope": ["💸 Transactions", "💳 Credit Card", "🥇 Aset", "🔄 Sync Log"],
scripts/personal-workflow/airo_sheets_sync_dry_run.py:483:    run_id = "dryrun_" + datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:8]
scripts/personal-workflow/airo_sheets_sync_dry_run.py:538:        sync_log_preview = {
scripts/personal-workflow/airo_sheets_sync_dry_run.py:540:            "run_id": run_id,
scripts/personal-workflow/airo_sheets_sync_dry_run.py:549:            "records_inserted": sum(1 for op in ops if op.action == "insert_or_update"),
scripts/personal-workflow/airo_sheets_sync_dry_run.py:551:            "records_skipped": sum(1 for op in ops if op.action.startswith("skip")),
scripts/personal-workflow/airo_sheets_sync_dry_run.py:552:            "records_failed": 0,
scripts/personal-workflow/airo_sheets_sync_dry_run.py:562:            "run_id": run_id,
scripts/personal-workflow/airo_sheets_sync_dry_run.py:578:            "sync_log_preview": sync_log_preview,
scripts/personal-workflow/airo_sheets_ledger_write_v0_4.py:48:    allowed = {"sync_log_only", "transactions_review_cc"}
scripts/personal-workflow/airo_sheets_sync_write_preview.py:306:    run_id = "write_preview_" + datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:8]
scripts/personal-workflow/airo_sheets_sync_write_preview.py:311:        "run_id": run_id,
scripts/personal-workflow/airo_sheets_sync_write_preview.py:316:        "source_dry_run_id": dry_report.get("run_id"),
scripts/personal-workflow/airo_google_sheets_client.py:44:    SheetKeyTarget("🔄 Sync Log", 2, "sync_id", None),
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_PROBE_V0_2_PASS.md:16:- write_scope=sync_log_only
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_PROBE_V0_2_PASS.md:18:- run_id=write_probe_20260510_074005_f7513e
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_PROBE_V0_2_PASS.md:26:- 🔄 Sync Log
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_PROBE_V0_2_PASS.md:41:The Google Sheet write path works for a controlled Sync Log append.
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:16:- Sync Log header fixed to final 19-column layout
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:24:🔄 Sync Log
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:50:- 🔄 Sync Log only
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:77:- validates 🔄 Sync Log final header shape
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:78:- appends one row to 🔄 Sync Log
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:86:## Expected Sync Log row
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:91:- run_id: generated
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:94:- target_tab: 🔄 Sync Log
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:98:- records_inserted: 0
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:100:- records_skipped: 0
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:101:- records_failed: 0
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:125:- write_scope=sync_log_only
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:127:- run_id=write_probe_20260510_074005_f7513e
docs/personal-workflow/integration/AIRO_GOOGLE_SHEETS_WRITE_GATE_V0_2.md:129:Interpretation: controlled Google Sheets write path works for 🔄 Sync Log only. Finance ledger writes remain disabled.
docs/personal-workflow/integration/AIRO_FULL_AUTO_SHEETS_SYNC_V1_1_1_SMOKE_HARDENING.md:24:- scope includes 💸 Transactions, 💳 Credit Card, 🔄 Sync Log
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:26:11. 🔄 Sync Log
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:42:| 🔄 Sync Log | FULL_AUTO_CORE_READY | Preserve observability and audit rows |
docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_SOURCE_AUDIT.md:343:scripts/personal-workflow/airo_full_auto_sheets_sync.py:340:        "scope": ["💸 Transactions", "💳 Credit Card", "🥇 Aset", "🔄 Sync Log"],
```

## Safe Conclusion

The 11-tab sheet structure is already defined and header-validated in v1.1.8.

The strongest implementation areas remain:

- 💸 Transactions
- 💳 Credit Card
- 🔄 Sync Log
- 🥇 Aset

The v1.2 completion focus remains:

- 💵 Cash Ledger
- 🏠 Cicilan Rumah
- 🤝 Hutang
- 🧾 Review Queue
- 📅 Monthly Review

## Recommended Next Execution Batch

Do not attempt every remaining tab at once.

Recommended order:

1. Inspect dry-run/write-preview mapper internals.
2. Identify whether 🧾 Review Queue or 💵 Cash Ledger has the smallest safe patch.
3. Patch only one missing route at a time.
4. Run dry-run/write-preview regression.
5. Avoid Telegram production smoke until local dry-run is clean and the Telegram guardrail is followed.

## Safety Confirmation

- No Google write was performed.
- No SQLite mutation was performed.
- No credentials, tokens, .env files, OAuth files, cookies, sessions, browser profiles, or private keys were read.
- Restricted paths EarnsAI, runtime, and trading were not intentionally scanned.
- OpenClaw was not patched or restarted.
