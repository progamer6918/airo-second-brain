import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from airo_personal_workflow.intents.parser import parse_user_message

examples = [
    "Catat ini: hari ini pakai Tokopedia Credit Card beli makanan Rp50.000",
    "beli makan 50k pakai tokopedia credit card",
    "bayar cicilan rumah 2500000",
    "cek cicilan rumah sudah bayar ke berapa",
    "kasih saya ringkasan bulan ini",
]

for text in examples:
    print("INPUT:", text)
    print(parse_user_message(text))
    print()

print("PERSONAL_WORKFLOW_SMOKE_PASS")
