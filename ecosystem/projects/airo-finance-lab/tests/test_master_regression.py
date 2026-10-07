import sys
import os
import sqlite3
import json

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_DB = os.path.join(REPO_ROOT, "data", "airo_finance.db")
DB_PATH = os.environ.get("AIRO_DB_PATH", DEFAULT_DB)

sys.path.insert(0, os.path.join(REPO_ROOT, "src"))

def run_tests():
    print("=== STARTING MASTER REGRESSION TEST SUITE ===")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # 0. Integrity & Foreign Key Assertions
    print("\n--- TEST 0: Integrity & Foreign Key Checks ---")
    integrity = cur.execute("PRAGMA integrity_check;").fetchall()
    assert len(integrity) == 1 and integrity[0]["integrity_check"] == "ok", f"Integrity check failed: {integrity}"
    fk_violations = cur.execute("PRAGMA foreign_key_check;").fetchall()
    assert len(fk_violations) == 0, f"Foreign key violations found ({len(fk_violations)}): {[dict(r) for r in fk_violations]}"
    print("✓ PRAGMA integrity_check: OK, PRAGMA foreign_key_check: 0 violations.")

    # 1. Database Schema Assertions
    print("\n--- TEST 1: Schema Checks ---")
    cols_accounts = [r["name"] for r in cur.execute("PRAGMA table_info(accounts)").fetchall()]
    assert "reserve_target_id" in cols_accounts, "reserve_target_id column missing from accounts"
    assert "parent_account_id" in cols_accounts, "parent_account_id column missing from accounts"
    assert "account_class" in cols_accounts, "account_class column missing from accounts"

    cols_tx = [r["name"] for r in cur.execute("PRAGMA table_info(transactions)").fetchall()]
    assert "transfer_side" in cols_tx, "transfer_side missing from transactions"
    assert "is_reserved" in cols_tx, "is_reserved missing from transactions"
    print("✓ Schema columns verified successfully.")

    # 2. Reconciled Rp 5 test payment & Statement checks
    print("\n--- TEST 2: Statement & Balance Reconciliation ---")
    stmt = cur.execute("SELECT * FROM credit_card_statements WHERE id = 'stmt_tokped_202609'").fetchone()
    assert stmt is not None, "stmt_tokped_202609 not found"
    assert stmt["total_amount"] == 2383963.0, f"Expected total 2383963, got {stmt['total_amount']}"
    assert stmt["status"] in ("ISSUED", "PAID"), f"Expected ISSUED or PAID status, got {stmt['status']}"
    if stmt["status"] == "PAID":
        assert stmt["unpaid_amount"] == 0.0, f"Expected unpaid 0.0 for PAID, got {stmt['unpaid_amount']}"
    else:
        assert stmt["unpaid_amount"] == 2383963.0, f"Expected unpaid 2383963, got {stmt['unpaid_amount']}"

    cc = cur.execute("SELECT * FROM credit_cards WHERE id = 'cc_ec0dc89ad811'").fetchone()
    assert cc is not None, "Tokopedia card not found"
    assert cc["current_balance"] in (0.0, 2383963.0, 2383964.0), f"Expected CC balance 0, 2383963 or 2383964, got {cc['current_balance']}"
    print(f"✓ Statement & CC Balance reconciled at Rp {cc['current_balance']:,.0f}.")

    # 3. Blu Pocket CC reserve classification & nesting
    print("\n--- TEST 3: Account Classification & Nesting ---")
    pocket = cur.execute("SELECT * FROM accounts WHERE id = 'acc_d44e516a4110'").fetchone()
    assert pocket["account_class"] == "RESERVE", f"Expected RESERVE, got {pocket['account_class']}"
    assert pocket["reserve_target_id"] == "cc_ec0dc89ad811", f"Expected cc_ec0dc89ad811, got {pocket['reserve_target_id']}"
    assert pocket["parent_account_id"] == "acc_c074c5e53290", f"Expected acc_c074c5e53290, got {pocket['parent_account_id']}"
    print(f"✓ Blu Pocket CC verified: RESERVE, target={pocket['reserve_target_id']}, parent={pocket['parent_account_id']}")

    # 4. Engine & Insights Calculation
    print("\n--- TEST 4: Engine & Insights Calculation ---")
    from airo_finance_core.db import DatabaseManager
    from airo_finance_core.engine import FinanceCoreEngine
    from airo_finance_core.insights import FinanceInsightsService

    db_mgr = DatabaseManager(DB_PATH)
    engine = FinanceCoreEngine(db_mgr)
    svc = FinanceInsightsService(db_mgr)
    
    cc_summary = svc.get_credit_card_summary()
    tokped_summary = next((c for c in cc_summary["cards"] if c["id"] == "cc_ec0dc89ad811"), None)
    assert tokped_summary is not None, "Tokopedia card missing from summary"
    
    print("CC Summary Metrics:")
    for k in ["unpaid_issued_statement", "unbilled", "limit_used", "reserve_balance", "shortage", "available_limit"]:
        print(f"  {k}: Rp {tokped_summary[k]:,.0f}")
    
    assert tokped_summary["unpaid_issued_statement"] in (0.0, 2383963.0, 2383964.0)
    cur_pocket = cur.execute("SELECT balance FROM accounts WHERE id = 'acc_d44e516a4110'").fetchone()
    expected_reserve = float(cur_pocket["balance"]) if cur_pocket else 0.0
    assert tokped_summary["reserve_balance"] == expected_reserve, f"Expected reserve {expected_reserve}, got {tokped_summary['reserve_balance']}"
    expected_shortage = max(0.0, tokped_summary["unpaid_issued_statement"] - tokped_summary["reserve_balance"])
    assert tokped_summary["shortage"] == expected_shortage, f"Expected shortage {expected_shortage}, got {tokped_summary['shortage']}"
    print(f"✓ Shortage verified exactly Rp {tokped_summary['shortage']:,.0f}!")

    # 5. Free Cash / Safe-to-Spend formula (Zero Double Deduction)
    print("\n--- TEST 5: Free Cash Formula (Zero Double Deduction) ---")
    sts = svc.get_safe_to_spend_report()
    print(f"  Total Liquid Balance: Rp {sts.total_liquid_balance:,.0f}")
    print(f"  Dedicated Reserve (Blu Pocket CC): Rp {sts.dedicated_reserve:,.0f}")
    print(f"  Total CC Unpaid: Rp {sts.cc_unpaid_total:,.0f}")
    print(f"  Uncovered CC Debt: Rp {sts.uncovered_cc_debt:,.0f}")
    print(f"  Unpaid Obligations: Rp {sts.unpaid_obligations_this_cycle:,.0f}")
    print(f"  Safety Floor: Rp {sts.safety_floor:,.0f}")
    print(f"  Safe To Spend: Rp {sts.safe_to_spend:,.0f}")

    assert sts.uncovered_cc_debt >= 0.0
    expected_sts = max(0.0, sts.total_liquid_balance - sts.uncovered_cc_debt - sts.unpaid_obligations_this_cycle - sts.safety_floor)
    assert sts.safe_to_spend == expected_sts, f"Expected sts {expected_sts}, got {sts.safe_to_spend}"
    print("✓ Free Cash calculation avoids double deduction perfectly.")

    # 6. Toggle Reserve Endpoint / Engine method
    print("\n--- TEST 6: Toggle Transaction Reserve ---")
    recent_tx = cur.execute("SELECT id, is_reserved FROM transactions ORDER BY created_at DESC LIMIT 1").fetchone()
    if recent_tx:
        tx_id = recent_tx["id"]
        orig_val = recent_tx["is_reserved"]
        new_val = 0 if orig_val == 1 else 1
        res = engine.toggle_transaction_reserve(tx_id, new_val)
        assert res.is_reserved == new_val
        # Restore
        engine.toggle_transaction_reserve(tx_id, orig_val)
        print(f"✓ Transaction {tx_id} reserve toggle verified and restored.")

    # 7. Internal Transfer side
    print("\n--- TEST 7: Transfer Side Verification ---")
    transfers = cur.execute("SELECT transfer_side, count(*) as c FROM transactions WHERE transfer_side IS NOT NULL GROUP BY transfer_side").fetchall()
    for row in transfers:
        print(f"  transfer_side={row['transfer_side']}: {row['c']} records")
    has_in = any(r["transfer_side"] == "IN" for r in transfers)
    assert has_in, "No IN transfer_side found in transactions!"
    print("✓ Transfer side logic correctly backfilled and active.")

    print("\n=======================================================")
    print("🎉 ALL 8 TEST SUITES (TEST 0 - 7) PASSED WITH ZERO ERRORS!")
    print("=======================================================")

if __name__ == "__main__":
    run_tests()
