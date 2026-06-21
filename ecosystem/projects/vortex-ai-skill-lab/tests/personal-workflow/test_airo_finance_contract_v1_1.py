import json
import os
import sqlite3
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WRAPPER = ROOT / "scripts" / "airo_personal_workflow_call.sh"


CASES = [
    ("nabung 5000 ke blu", 5000, "tabungan", "BLU BCA"),
    ("nabung 5rb ke blu", 5000, "tabungan", "BLU BCA"),
    ("nabung 5 ribu ke blu", 5000, "tabungan", "BLU BCA"),
    ("nabung 5k ke blu", 5000, "tabungan", "BLU BCA"),
    ("tarik cash 50000 dari blu", 50000, "cash_withdrawal", "BLU BCA"),
    ("topup gopay 20rb dari blu", 20000, "ewallet_topup", "BLU BCA"),
]


def run_cmd(text, db):
    env = os.environ.copy()
    env["AIRO_WORKFLOW_MODE"] = "dry-run"
    env["AIRO_DB_PATH"] = str(db)
    env["PYTHONPATH"] = f"{ROOT}:{env.get('PYTHONPATH', '')}"
    return json.loads(subprocess.check_output([str(WRAPPER), text], cwd=str(ROOT), env=env, text=True))


def test_finance_contract_v1_1_matrix(tmp_path):
    db = tmp_path / "airo.sqlite3"

    for text, amount, category, payment_method in CASES:
        out = run_cmd(text, db)
        assert out["ok"] is True, out
        assert out["data"]["amount"] == amount, out
        assert out["data"]["category"] == category, out
        assert out["data"]["payment_method"] == payment_method, out

    dup = run_cmd("nabung 5000 ke blu", db)
    assert dup["ok"] is True
    assert dup["data"]["persist_action"] == "skip_duplicate"

    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    rows = con.execute("SELECT note, amount, category, payment_method, deleted_at FROM transactions").fetchall()
    con.close()

    active = [r for r in rows if not r["deleted_at"]]
    assert len(active) == len(CASES), [dict(r) for r in rows]
