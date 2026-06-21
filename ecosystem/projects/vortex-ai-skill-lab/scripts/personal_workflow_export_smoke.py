import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

_TMP = tempfile.TemporaryDirectory()
os.environ["AIRO_DB_PATH"] = str(Path(_TMP.name) / "test_airo.sqlite3")
print(f"TEST_DB={os.environ['AIRO_DB_PATH']}")

from pathlib import Path

from airo_personal_workflow.db.repository import record_from_text, monthly_summary
from airo_personal_workflow.exports.exporter import (
    export_installments_csv,
    export_summary_json,
    export_transactions_csv,
)
from airo_personal_workflow.reports.monthly import generate_monthly_markdown

period = "2026-05"

record_from_text("Catat ini: beli makan 50k pakai tokopedia credit card")
record_from_text("bayar cicilan rumah 2500000")

summary = monthly_summary(period)
files = [
    export_transactions_csv(period),
    export_installments_csv(period),
    export_summary_json(summary, period),
    generate_monthly_markdown(period),
]

for f in files:
    path = Path(f)
    print(f"FILE_READY={path} exists={path.exists()} size={path.stat().st_size if path.exists() else 0}")
    assert path.exists()
    assert path.stat().st_size > 0

print("PERSONAL_WORKFLOW_EXPORT_SMOKE_PASS")
