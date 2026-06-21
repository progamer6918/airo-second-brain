#!/usr/bin/env bash
set -Eeuo pipefail

REPO_DIR="${AIRO_REPO_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
DB="$HOME/.local/share/airo-personal-workflow/airo.sqlite3"
ENVFILE="$HOME/.config/airo-personal-workflow/sheets-sync.env"

cd "$REPO_DIR"

echo "== local wrapper temp DB idempotency =="
BEFORE_COUNT="$(python3 - <<'PY'
import sqlite3
from pathlib import Path
db = Path.home() / ".local/share/airo-personal-workflow/airo.sqlite3"
con = sqlite3.connect(db)
print(con.execute("SELECT COUNT(*) FROM transactions WHERE lower(COALESCE(note,''))='nabung 5000 ke blu'").fetchone()[0])
con.close()
PY
)"

TMP_DIR="$(mktemp -d)"
TMP_DB="$TMP_DIR/airo.sqlite3"

AIRO_WORKFLOW_MODE=dry-run \
AIRO_DB_PATH="$TMP_DB" \
PYTHONPATH="$REPO_DIR:${PYTHONPATH:-}" \
  ./scripts/airo_personal_workflow_call.sh "nabung 5000 ke blu" > "$TMP_DIR/first.json"

AIRO_WORKFLOW_MODE=dry-run \
AIRO_DB_PATH="$TMP_DB" \
PYTHONPATH="$REPO_DIR:${PYTHONPATH:-}" \
  ./scripts/airo_personal_workflow_call.sh "nabung 5000 ke blu" > "$TMP_DIR/second.json"

AFTER_COUNT="$(python3 - <<'PY'
import sqlite3
from pathlib import Path
db = Path.home() / ".local/share/airo-personal-workflow/airo.sqlite3"
con = sqlite3.connect(db)
print(con.execute("SELECT COUNT(*) FROM transactions WHERE lower(COALESCE(note,''))='nabung 5000 ke blu'").fetchone()[0])
con.close()
PY
)"

python3 - <<PY
import json
import sqlite3
from pathlib import Path

tmp = Path("$TMP_DIR")
first = json.loads((tmp / "first.json").read_text())
second = json.loads((tmp / "second.json").read_text())

print("FIRST_MESSAGE=", first.get("message"))
print("SECOND_MESSAGE=", second.get("message"))
print("REAL_DB_COUNT_BEFORE=", "$BEFORE_COUNT")
print("REAL_DB_COUNT_AFTER=", "$AFTER_COUNT")

assert first["ok"] is True, first
assert second["ok"] is True, second
assert first["data"]["amount"] == 5000, first
assert second["data"]["amount"] == 5000, second
assert first["data"]["category"] == "tabungan", first
assert second["data"]["category"] == "tabungan", second
assert first["data"]["payment_method"] == "BLU BCA", first
assert second["data"]["payment_method"] == "BLU BCA", second
assert second["data"].get("persist_action") == "skip_duplicate", second
assert "$BEFORE_COUNT" == "$AFTER_COUNT", ("real DB changed", "$BEFORE_COUNT", "$AFTER_COUNT")

con = sqlite3.connect("$TMP_DB")
con.row_factory = sqlite3.Row
rows = con.execute("""
SELECT rowid, id, amount, category, payment_method, note, deleted_at
FROM transactions
WHERE lower(COALESCE(note,''))='nabung 5000 ke blu'
ORDER BY rowid
""").fetchall()
con.close()

active = [r for r in rows if not r["deleted_at"]]
assert len(active) == 1, [dict(r) for r in rows]
print("WRAPPER_TEMP_DB_IDEMPOTENCY_PASS")
PY

echo "== real DB canonical state =="
python3 - <<'PY'
import sqlite3
from pathlib import Path
db = Path.home() / ".local/share/airo-personal-workflow/airo.sqlite3"
con = sqlite3.connect(db)
con.row_factory = sqlite3.Row
rows = con.execute("""
SELECT rowid, id, amount, category, payment_method, note, deleted_at, updated_at
FROM transactions
WHERE lower(COALESCE(note,''))='nabung 5000 ke blu'
ORDER BY rowid
""").fetchall()
for r in rows:
    print(dict(r))
active = [r for r in rows if not r["deleted_at"]]
assert len(active) == 1, [dict(r) for r in active]
assert active[0]["id"] == "trx_a8ad5c2eec99", dict(active[0])
assert active[0]["amount"] == 5000, dict(active[0])
assert active[0]["category"] == "tabungan", dict(active[0])
assert active[0]["payment_method"] == "BLU BCA", dict(active[0])
print("REAL_DB_CANONICAL_PASS")
con.close()
PY

echo "== OpenClaw service env =="
systemctl --user cat openclaw-gateway.service | grep -E 'AIRO_REPO_DIR|PYTHONPATH|ExecStart|PATH=' || true
systemctl --user is-active --quiet openclaw-gateway.service
echo "OPENCLAW_ACTIVE_PASS"

echo "== live Sheets dry-run =="
test -f "$ENVFILE"
set -a
. "$ENVFILE"
set +a

PYBIN="${AIRO_SYNC_PYTHON:-python3}"
OUT="/tmp/airo_finance_prod_regression_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUT"

"$PYBIN" - <<'PYTEST'
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

def load(name, relpath):
    path = Path(relpath)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

persistence = load("airo_transaction_persistence", "scripts/personal-workflow/airo_transaction_persistence.py")
dryrun = load("airo_sheets_sync_dry_run", "scripts/personal-workflow/airo_sheets_sync_dry_run.py")

raw = "kayaknya bayar sesuatu kemarin"
db_path = Path(tempfile.mkdtemp(prefix="airo_rq_regression_")) / "review_queue.sqlite"

persist = persistence.persist_review_queue_candidate(raw, db_path, source="prod_regression_target")
report = dryrun.build_report(db_path)
text = json.dumps({"persist": persist, "report": report}, ensure_ascii=False, default=str)

assert persist.get("target_tab") == "🧾 Review Queue", persist
assert raw in text, text
assert "🧾 Review Queue" in text or "Review Queue" in text, text
assert "candidate" in text, text

print("REVIEW_QUEUE_DRY_RUN_TARGET_PASS")
PYTEST

"$PYBIN" scripts/personal-workflow/airo_full_auto_sheets_sync.py \
  --mode dry-run \
  --snapshot-out "$OUT/snapshot.json" \
  --preview-out "$OUT/preview.json" \
  --report-out "$OUT/report.json" \
  > "$OUT/stdout.json"

"$PYBIN" - <<PY
import json
from pathlib import Path
out = Path("$OUT")
preview = json.loads((out / "preview.json").read_text())
report = json.loads((out / "report.json").read_text())
write = [
    d for d in preview.get("decisions", [])
    if d.get("preview_action") in {"insert_candidate", "update_candidate"}
]
print("LIVE_OUT=", out)
print("REPORT_WRITE_CANDIDATE_COUNT=", report.get("write_candidate_count"))
print("TOTAL_WRITE_CANDIDATES=", len(write))
for d in write:
    print({
        "target_tab": d.get("target_tab"),
        "duplicate_key": d.get("duplicate_key"),
        "preview_action": d.get("preview_action"),
        "reason": d.get("reason"),
    })
if len(write) == 0:
    print("SHEETS_DRY_RUN_IDEMPOTENT_PASS")
else:
    print("SHEETS_DRY_RUN_PENDING_WRITE_CANDIDATES=", len(write))
    print("SHEETS_DRY_RUN_PREVIEW_PASS")
PY

echo
echo "PASS: AIRO finance production regression passed."
