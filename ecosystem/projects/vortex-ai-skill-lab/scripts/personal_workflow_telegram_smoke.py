import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

_TMP = tempfile.TemporaryDirectory()
os.environ["AIRO_DB_PATH"] = str(Path(_TMP.name) / "test_airo.sqlite3")
print(f"TEST_DB={os.environ['AIRO_DB_PATH']}")

import json
from airo_personal_workflow.telegram.local_handler import handle_telegram_text

examples = [
    "Catat ini: beli makan 50k pakai tokopedia credit card",
    "bayar cicilan rumah 2500000",
    "cek cicilan rumah sudah bayar ke berapa",
    "kasih saya ringkasan bulan ini",
]

for text in examples:
    print("INPUT:", text)
    result = handle_telegram_text(text)
    print(json.dumps({
        "ok": result["ok"],
        "intent": result["intent"],
        "action": result["action"],
        "message": result["message"],
    }, ensure_ascii=False, indent=2))
    print()
    assert result["ok"] is True

print("PERSONAL_WORKFLOW_TELEGRAM_LOCAL_HANDLER_PASS")
