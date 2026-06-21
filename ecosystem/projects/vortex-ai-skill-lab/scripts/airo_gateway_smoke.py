import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

_TMP = tempfile.TemporaryDirectory()
os.environ["AIRO_DB_PATH"] = str(Path(_TMP.name) / "test_airo_gateway.sqlite3")
print(f"TEST_DB={os.environ['AIRO_DB_PATH']}")

from airo_personal_workflow.gateway import handle_text

examples = [
    "catat beli makan 50k pakai tokopedia credit card",
    "bayar cicilan rumah 2500000",
    "cek cicilan rumah sudah bayar ke berapa",
    "kasih saya ringkasan bulan ini",
]

for text in examples:
    result = handle_text(text)
    print(json.dumps({
        "input": text,
        "ok": result["ok"],
        "intent": result["intent"],
        "action": result["action"],
        "message": result["message"],
    }, ensure_ascii=False, indent=2))
    assert result["ok"] is True

print("AIRO_GATEWAY_SMOKE_PASS")
