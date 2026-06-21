import requests
import json

url = "https://script.google.com/macros/s/AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA/exec"
data = {
    "message": {
        "chat": {
            "id": 12349
        },
        "text": "admin apply account styles"
    }
}

print("Sending admin apply account styles request to Web App...")
res = requests.post(url, json=data)
print("Response status:", res.status_code)
try:
    print(json.dumps(res.json(), indent=2))
except Exception as e:
    print("Raw text:", res.text)
