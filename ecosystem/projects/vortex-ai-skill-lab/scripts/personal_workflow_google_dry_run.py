import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

_TMP = tempfile.TemporaryDirectory()
os.environ["AIRO_DB_PATH"] = str(Path(_TMP.name) / "test_airo.sqlite3")
print(f"TEST_DB={os.environ['AIRO_DB_PATH']}")

from airo_personal_workflow.db.repository import record_from_text
from airo_personal_workflow.adapters.google.workspace_dry_run import generate_google_workspace_plan

period = sys.argv[1] if len(sys.argv) > 1 else "2026-05"

record_from_text("Catat ini: beli makan 50k pakai tokopedia credit card")
record_from_text("bayar cicilan rumah 2500000")

result = generate_google_workspace_plan(period)
print(json.dumps(result, ensure_ascii=False, indent=2))

assert result["dry_run"] is True
assert result["safety"]["oauth_used"] is False
assert result["safety"]["google_api_called"] is False
assert result["safety"]["token_required"] is False

for item in result["files"].values():
    assert item["exists"] is True
    assert item["size"] > 0

print("PERSONAL_WORKFLOW_GOOGLE_DRY_RUN_PASS")
