import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
wrapper = ROOT / "scripts" / "airo_personal_workflow_call.sh"

tmp = tempfile.TemporaryDirectory()
env = os.environ.copy()
env["AIRO_WORKFLOW_MODE"] = "dry-run"
env["AIRO_DB_PATH"] = str(Path(tmp.name) / "contract_test.sqlite3")

tests = [
    "catat beli makan 50k pakai tokopedia credit card",
    "bayar cicilan rumah 2500000",
    "cek cicilan rumah sudah bayar ke berapa",
    "kasih saya ringkasan bulan ini",
]

for text in tests:
    out = subprocess.check_output([str(wrapper), text], cwd=str(ROOT), env=env, text=True)
    data = json.loads(out)

    print(json.dumps({
        "input": text,
        "ok": data.get("ok"),
        "intent": data.get("intent"),
        "action": data.get("action"),
        "message": data.get("message"),
    }, ensure_ascii=False, indent=2))

    assert data.get("ok") is True
    assert "message" in data

print("AIRO_INTEGRATION_CONTRACT_SMOKE_PASS")
