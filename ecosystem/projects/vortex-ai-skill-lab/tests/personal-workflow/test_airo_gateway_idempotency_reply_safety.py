import json
import os
import sqlite3
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WRAPPER = ROOT / "scripts" / "airo_personal_workflow_call.sh"


def test_wrapper_repeated_savings_command_is_idempotent_and_temp_db_only(tmp_path):
    db = tmp_path / "airo.sqlite3"
    env = os.environ.copy()
    env["AIRO_WORKFLOW_MODE"] = "dry-run"
    env["AIRO_DB_PATH"] = str(db)
    env["PYTHONPATH"] = f"{ROOT}:{env.get('PYTHONPATH', '')}"

    first = json.loads(subprocess.check_output([str(WRAPPER), "nabung 5000 ke blu"], cwd=str(ROOT), env=env, text=True))
    second = json.loads(subprocess.check_output([str(WRAPPER), "nabung 5000 ke blu"], cwd=str(ROOT), env=env, text=True))

    assert first["ok"] is True
    assert second["ok"] is True
    assert first["data"]["amount"] == 5000
    assert second["data"]["amount"] == 5000
    assert first["data"]["category"] == "tabungan"
    assert second["data"]["category"] == "tabungan"
    assert first["data"]["persist_action"] in {"insert", "skip_duplicate"}
    assert second["data"]["persist_action"] == "skip_duplicate"
    assert second["data"]["already_recorded"] is True

    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    rows = con.execute("""
        SELECT id, category, amount, payment_method, note, deleted_at
        FROM transactions
        WHERE lower(COALESCE(note,'')) = 'nabung 5000 ke blu'
        ORDER BY rowid ASC
    """).fetchall()
    con.close()

    active = [r for r in rows if not r["deleted_at"]]
    assert len(active) == 1, [dict(r) for r in rows]
    assert active[0]["amount"] == 5000
    assert active[0]["category"] == "tabungan"
    assert active[0]["payment_method"] == "BLU BCA"
