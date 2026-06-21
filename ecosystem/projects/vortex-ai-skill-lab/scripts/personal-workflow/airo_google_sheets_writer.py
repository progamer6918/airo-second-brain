#!/usr/bin/env python3
import argparse, datetime, json, os
from pathlib import Path

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
FORBIDDEN_ENV_NAMES = ["GOOGLE_CLIENT_SECRET", "GOOGLE_REFRESH_TOKEN", "GOOGLE_ACCESS_TOKEN", "GOOGLE_COOKIE", "GOOGLE_SESSION"]

def die(msg, code=1):
    print(json.dumps({"ok": False, "error": msg}, ensure_ascii=False))
    raise SystemExit(code)

def load_rows(path):
    if not path:
        return [["timestamp", "source", "description", "amount"], [datetime.datetime.now().isoformat(), "airo", "dry-run sample", "0"]]
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "rows" in data:
        data = data["rows"]
    if not isinstance(data, list) or not all(isinstance(r, list) for r in data):
        die("payload must be a list of rows or object with rows")
    return data

def get_oauth_creds(oauth_client_path, oauth_token_path):
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow

    token_path = Path(oauth_token_path).expanduser()
    client_path = Path(oauth_client_path).expanduser()

    if not client_path.exists():
        die("real write blocked: OAuth client JSON not found")

    creds = None
    if token_path.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
        except Exception:
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(client_path), SCOPES)
            creds = flow.run_local_server(port=0)
        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(creds.to_json(), encoding="utf-8")
        try:
            os.chmod(token_path, 0o600)
        except Exception:
            pass

    return creds

def main():
    p = argparse.ArgumentParser(description="Airo Google Sheets writer with approval gate")
    p.add_argument("--mode", choices=["dry-run", "real"], default=os.environ.get("AIRO_SHEETS_MODE", "dry-run"))
    p.add_argument("--auth-method", choices=["oauth"], default="oauth")
    p.add_argument("--spreadsheet-id", default=os.environ.get("AIRO_GOOGLE_SHEETS_SPREADSHEET_ID", ""))
    p.add_argument("--range", default=os.environ.get("AIRO_GOOGLE_SHEETS_RANGE", "Airo!A:D"))
    p.add_argument("--payload", default="")
    p.add_argument("--approve-real-write", default="NO")
    p.add_argument("--oauth-client", default=os.environ.get("AIRO_GOOGLE_OAUTH_CLIENT", str(Path.home() / ".local/share/airo-personal-workflow/google/oauth_client.local.json")))
    p.add_argument("--oauth-token", default=os.environ.get("AIRO_GOOGLE_TOKEN_PATH", str(Path.home() / ".local/share/airo-personal-workflow/google/token.local.json")))
    args = p.parse_args()

    rows = load_rows(args.payload)

    if args.mode == "dry-run":
        print(json.dumps({
            "ok": True,
            "mode": "dry-run",
            "auth_method": "oauth",
            "operation": "append_rows",
            "spreadsheet_id_set": bool(args.spreadsheet_id),
            "range": args.range,
            "row_count": len(rows),
            "rows_preview": rows[:5],
            "approval_required": False
        }, indent=2, ensure_ascii=False))
        return

    if args.approve_real_write != "YES":
        die("real write blocked: pass --approve-real-write YES")
    if not args.spreadsheet_id:
        die("real write blocked: missing spreadsheet id")
    if any(os.environ.get(k) for k in FORBIDDEN_ENV_NAMES):
        die("real write blocked: forbidden secret-like env var detected")

    from googleapiclient.discovery import build
    creds = get_oauth_creds(args.oauth_client, args.oauth_token)
    service = build("sheets", "v4", credentials=creds)

    result = service.spreadsheets().values().append(
        spreadsheetId=args.spreadsheet_id,
        range=args.range,
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body={"values": rows},
    ).execute()

    print(json.dumps({
        "ok": True,
        "mode": "real",
        "auth_method": "oauth",
        "operation": "append_rows",
        "spreadsheet_id_set": True,
        "range": args.range,
        "updated_range": result.get("updates", {}).get("updatedRange"),
        "updated_rows": result.get("updates", {}).get("updatedRows")
    }, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
