#!/usr/bin/env python3
import argparse
import json
import os
import urllib.request
import urllib.error
from pathlib import Path


NOTION_VERSION = "2022-06-28"


def load_notion_token() -> str:
    token = os.environ.get("NOTION_TOKEN", "").strip()
    if token:
        return token

    env_path = Path.home() / ".config" / "openclaw" / "secrets" / "notion.env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            if key.strip() == "NOTION_TOKEN":
                return value.strip().strip('"').strip("'")

    raise SystemExit("ERROR: NOTION_TOKEN not found in shell or ~/.config/openclaw/secrets/notion.env")


def patch_recent_capture(page_id: str, routed_to: str, destination_db: str, destination_url: str, reason: str, status: str):
    token = load_notion_token()

    payload = {
        "properties": {
            "Routed To": {"select": {"name": routed_to}},
            "Destination DB": {"rich_text": [{"text": {"content": destination_db}}]},
            "Destination URL": {"url": destination_url},
            "Reason": {"rich_text": [{"text": {"content": reason}}]},
            "Status": {"select": {"name": status}},
        }
    }

    req = urllib.request.Request(
        f"https://api.notion.com/v1/pages/{page_id}",
        data=json.dumps(payload).encode("utf-8"),
        method="PATCH",
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(json.dumps({
                "ok": True,
                "page_id": data.get("id"),
                "url": data.get("url"),
                "status": data.get("properties", {}).get("Status", {}).get("select", {}).get("name"),
                "routed_to": data.get("properties", {}).get("Routed To", {}).get("select", {}).get("name"),
                "destination_db": destination_db,
                "destination_url": destination_url,
            }, indent=2))
    except urllib.error.HTTPError as e:
        print(e.read().decode("utf-8"))
        raise


def main():
    parser = argparse.ArgumentParser(description="Update Recent Captures audit trail after final routing.")
    parser.add_argument("--page-id", required=True)
    parser.add_argument("--routed-to", required=True)
    parser.add_argument("--destination-db", required=True)
    parser.add_argument("--destination-url", required=True)
    parser.add_argument("--reason", required=True)
    parser.add_argument("--status", default="Routed")

    args = parser.parse_args()

    patch_recent_capture(
        page_id=args.page_id,
        routed_to=args.routed_to,
        destination_db=args.destination_db,
        destination_url=args.destination_url,
        reason=args.reason,
        status=args.status,
    )


if __name__ == "__main__":
    main()
