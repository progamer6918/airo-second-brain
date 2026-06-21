import requests
import json
import sys

url = "https://script.google.com/macros/s/AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA/exec"

try:
    with open("/home/egitaristorandas/vortex-ai-skill-lab/scratch/registries_payload.json", "r", encoding="utf-8") as f:
        payload = json.load(f)
except Exception as e:
    print(f"Error reading registries payload: {e}")
    sys.exit(1)

data = {
    "message": {
        "chat": {
            "id": 12349
        },
        "text": "admin import registries"
    },
    "categories": payload.get("categories", []),
    "accounts": payload.get("accounts", [])
}

print("Sending admin import registries request to Web App...")
res = requests.post(url, json=data)
print("Response status:", res.status_code)
try:
    print(json.dumps(res.json(), indent=2))
except Exception as e:
    print("Raw text:", res.text)
