#!/usr/bin/env python3
import argparse, csv, datetime, hashlib, json, os, sys
from pathlib import Path

DEFAULT_ROOT = Path.home() / ".local/share/airo-personal-workflow"
DEFAULT_RANGE = "Airo!A:D"

def now():
    return datetime.datetime.now().isoformat(timespec="seconds")

def emit(obj, code=0):
    print(json.dumps(obj, indent=2, ensure_ascii=False))
    raise SystemExit(code)

def read_rows(path):
    if not path:
        return [["timestamp", "source", "description", "amount"], [now(), "airo-sync", "sample dry-run row", "0"]]
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and isinstance(data.get("rows"), list):
        return data["rows"]
    if isinstance(data, list):
        return data
    emit({"ok": False, "error": "payload must be JSON list or object with rows"}, 2)

def row_hash(row):
    raw = json.dumps(row, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def audit_file(root):
    p = Path(root).expanduser().resolve() / "audits" / "sheets_sync_audit.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

def write_audit(root, record):
    p = audit_file(root)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return str(p)

def csv_fallback(root, rows, name="airo_sheets_fallback"):
    out_dir = Path(root).expanduser().resolve() / "exports" / "sheets_fallback"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    out = out_dir / f"{name}_{stamp}.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    return str(out)

def load_seen(root):
    p = Path(root).expanduser().resolve() / "audits" / "sheets_sync_seen_hashes.json"
    if not p.exists():
        return set(), p
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        return set(data.get("hashes", [])), p
    except Exception:
        return set(), p

def save_seen(path, hashes):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"updated_at": now(), "hashes": sorted(hashes)}, indent=2), encoding="utf-8")

def cmd_preflight(args):
    root = Path(args.root).expanduser().resolve()
    oauth_client = root / "google" / "oauth_client.local.json"
    oauth_token = root / "google" / "token.local.json"
    result = {
        "ok": True,
        "operation": "sheets_sync_preflight",
        "root": str(root),
        "oauth_client_exists": oauth_client.exists(),
        "oauth_token_exists": oauth_token.exists(),
        "spreadsheet_id_set": bool(args.spreadsheet_id),
        "range": args.range,
        "online_check_requested": args.online,
        "online_check_performed": False,
        "content_read": False,
        "write_performed": False
    }

    if args.online:
        if args.approve_online_check != "YES":
            emit({**result, "ok": False, "error": "online check blocked: pass --approve-online-check YES"}, 2)
        try:
            from google.oauth2.credentials import Credentials
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build
        except Exception as e:
            emit({**result, "ok": False, "error": "google libraries unavailable", "detail": str(e)}, 2)
        if not oauth_token.exists():
            emit({**result, "ok": False, "error": "oauth token not found"}, 2)
        if not args.spreadsheet_id:
            emit({**result, "ok": False, "error": "spreadsheet id required for online check"}, 2)
        creds = Credentials.from_authorized_user_file(str(oauth_token), ["https://www.googleapis.com/auth/spreadsheets"])
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
        service = build("sheets", "v4", credentials=creds)
        meta = service.spreadsheets().get(spreadsheetId=args.spreadsheet_id, fields="sheets.properties.title").execute()
        titles = [s["properties"]["title"] for s in meta.get("sheets", [])]
        tab = args.range.split("!", 1)[0] if "!" in args.range else ""
        result.update({
            "online_check_performed": True,
            "sheet_titles": titles,
            "target_tab": tab,
            "target_tab_exists": tab in titles if tab else None,
            "content_read": False,
            "write_performed": False
        })

    audit = write_audit(root, result)
    result["audit_file"] = audit
    emit(result)

def cmd_prepare(args):
    rows = read_rows(args.payload)
    seen, seen_path = load_seen(args.root)
    hashes = [row_hash(r) for r in rows]
    duplicate_hashes = [h for h in hashes if h in seen]
    new_hashes = [h for h in hashes if h not in seen]

    result = {
        "ok": True,
        "operation": "sheets_sync_prepare_append",
        "range": args.range,
        "row_count": len(rows),
        "new_row_hash_count": len(new_hashes),
        "duplicate_hash_count": len(duplicate_hashes),
        "duplicate_hashes_preview": duplicate_hashes[:5],
        "rows_preview": rows[:5],
        "write_performed": False,
        "fallback_csv": None
    }

    if args.write_seen == "YES":
        save_seen(seen_path, set(seen).union(hashes))
        result["seen_hashes_updated"] = True
        result["seen_hashes_file"] = str(seen_path)
    else:
        result["seen_hashes_updated"] = False

    if args.fallback_csv:
        result["fallback_csv"] = csv_fallback(args.root, rows)

    audit = write_audit(args.root, result)
    result["audit_file"] = audit
    emit(result)

def main():
    p = argparse.ArgumentParser(description="Airo Google Sheets sync reliability helper")
    p.add_argument("--root", default=str(DEFAULT_ROOT))
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("preflight")
    a.add_argument("--spreadsheet-id", default=os.environ.get("AIRO_GOOGLE_SHEETS_SPREADSHEET_ID", ""))
    a.add_argument("--range", default=os.environ.get("AIRO_GOOGLE_SHEETS_RANGE", DEFAULT_RANGE))
    a.add_argument("--online", action="store_true")
    a.add_argument("--approve-online-check", default="NO")
    a.set_defaults(func=cmd_preflight)

    b = sub.add_parser("prepare-append")
    b.add_argument("--payload", default="")
    b.add_argument("--range", default=os.environ.get("AIRO_GOOGLE_SHEETS_RANGE", DEFAULT_RANGE))
    b.add_argument("--write-seen", default="NO")
    b.add_argument("--fallback-csv", action="store_true")
    b.set_defaults(func=cmd_prepare)

    args = p.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
