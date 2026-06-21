import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

_TMP = tempfile.TemporaryDirectory()
os.environ["AIRO_DB_PATH"] = str(Path(_TMP.name) / "test_airo.sqlite3")
print(f"TEST_DB={os.environ['AIRO_DB_PATH']}")

from airo_personal_workflow.db.repository import record_from_text, check_installment, monthly_summary
from airo_personal_workflow.intents.parser import parse_user_message

examples = [
    "Catat ini: hari ini pakai Tokopedia Credit Card beli makanan Rp50.000",
    "beli makan 50k pakai tokopedia credit card",
    "bayar cicilan rumah 2500000",
    "cek cicilan rumah sudah bayar ke berapa",
    "kasih saya ringkasan bulan ini",
]

print("=== PARSER CHECK ===")
for text in examples:
    print("INPUT:", text)
    print(parse_user_message(text))
    print()

print("=== DB RECORD CHECK ===")
for text in examples[:3]:
    print("RECORD:", text)
    print(record_from_text(text))
    print()

result = check_installment("Cicilan Rumah")
summary = monthly_summary("2026-05")

print("=== CHECK INSTALLMENT ===")
print(result)
print("=== MONTHLY SUMMARY ===")
print(summary)

assert result["found"] is True
assert result["installment"]["paid_installments"] == 1
assert summary["transactions"]["count"] == 2
assert summary["installment_payments"]["count"] == 1

print("PERSONAL_WORKFLOW_DB_SMOKE_PASS")
