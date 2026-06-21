#!/usr/bin/env python3
import argparse, csv, datetime, json
from pathlib import Path

DEFAULT_ROOT = Path.home() / ".local/share/airo-personal-workflow"

def now():
    return datetime.datetime.now().isoformat(timespec="seconds")

def emit(obj, code=0):
    print(json.dumps(obj, indent=2, ensure_ascii=False))
    raise SystemExit(code)

def read_rows(path):
    if not path:
        return [
            ["timestamp", "source", "description", "amount"],
            [now(), "airo-google-fallback", "sample fallback export row", "0"]
        ]
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and isinstance(data.get("rows"), list):
        return data["rows"]
    if isinstance(data, list):
        return data
    emit({"ok": False, "error": "payload must be JSON list or object with rows"}, 2)

def file_meta(path):
    p = Path(path).expanduser()
    return {
        "path": str(p),
        "exists": p.exists(),
        "is_file": p.is_file() if p.exists() else False,
        "size_bytes": p.stat().st_size if p.exists() and p.is_file() else None,
        "content_read": False
    }

def write_csv(root, rows, prefix):
    out_dir = Path(root).expanduser().resolve() / "exports" / "google_api_fallback"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    out = out_dir / f"{prefix}_{stamp}.csv"
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    return out

def audit(root, record):
    p = Path(root).expanduser().resolve() / "audits" / "google_fallback_audit.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return str(p)

def cmd_status(args):
    root = Path(args.root).expanduser().resolve()
    fallback_dir = root / "exports" / "google_api_fallback"
    files = []
    if fallback_dir.exists():
        for f in sorted(fallback_dir.glob("*.csv"), key=lambda x: x.stat().st_mtime, reverse=True)[:20]:
            files.append({
                "name": f.name,
                "path": str(f),
                "size_bytes": f.stat().st_size,
                "modified": datetime.datetime.fromtimestamp(f.stat().st_mtime).isoformat(timespec="seconds")
            })
    result = {
        "ok": True,
        "operation": "google_api_fallback_status",
        "root": str(root),
        "oauth_client": file_meta(root / "google" / "oauth_client.local.json"),
        "oauth_token": file_meta(root / "google" / "token.local.json"),
        "fallback_dir": str(fallback_dir),
        "fallback_csv_count_shown": len(files),
        "fallback_csv_files": files,
        "content_read": False
    }
    result["audit_file"] = audit(root, result)
    emit(result)

def cmd_csv_export(args):
    rows = read_rows(args.payload)
    out = write_csv(args.root, rows, args.prefix)
    result = {
        "ok": True,
        "operation": "csv_fallback_export",
        "csv_path": str(out),
        "row_count": len(rows),
        "rows_preview": rows[:5],
        "google_write_performed": False,
        "manual_import_required": True,
        "next_steps": [
            "Open Google Sheets manually.",
            "Open the target spreadsheet.",
            "Use File > Import or paste the CSV rows into the target tab.",
            "Verify row count manually.",
            "Keep the CSV as local fallback audit evidence."
        ]
    }
    result["audit_file"] = audit(args.root, result)
    emit(result)

def cmd_manual_checklist(args):
    result = {
        "ok": True,
        "operation": "manual_google_sheets_import_checklist",
        "checklist": [
            "Generate fallback CSV with airo_google_fallback.py csv-export.",
            "Open the target Google Sheet manually.",
            "Confirm the target tab name, usually Airo.",
            "Import or paste rows from the CSV.",
            "Verify timestamp/source/description/amount columns.",
            "Record manual import in the local approval note or project log if needed.",
            "Do not paste OAuth token, credential JSON, cookie, or browser session anywhere."
        ],
        "google_api_required": False,
        "billing_required": False,
        "write_performed": False
    }
    result["audit_file"] = audit(args.root, result)
    emit(result)

def cmd_apps_script_plan(args):
    proposal = {
        "ok": True,
        "operation": "apps_script_web_app_fallback_plan",
        "status": "proposal_only_not_deployed",
        "purpose": "Use Google Apps Script as a future fallback write path if Google Cloud API access becomes unavailable.",
        "concept": [
            "Create Apps Script bound to the Airo Google Sheet.",
            "Implement a doPost endpoint that appends approved rows.",
            "Protect endpoint with a local shared passphrase or signed payload later.",
            "Airo local tool sends approved rows only after queue approval.",
            "Keep CSV fallback as secondary backup."
        ],
        "not_done_in_this_phase": [
            "No Apps Script project created.",
            "No Web App deployed.",
            "No endpoint URL stored.",
            "No secret generated.",
            "No external write performed."
        ],
        "approval_needed_before_future_deployment": True
    }
    proposal["audit_file"] = audit(args.root, proposal)
    emit(proposal)

def main():
    p = argparse.ArgumentParser(description="Airo Google API fallback helper")
    p.add_argument("--root", default=str(DEFAULT_ROOT))
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("status")
    a.set_defaults(func=cmd_status)

    b = sub.add_parser("csv-export")
    b.add_argument("--payload", default="")
    b.add_argument("--prefix", default="airo_google_fallback")
    b.set_defaults(func=cmd_csv_export)

    c = sub.add_parser("manual-checklist")
    c.set_defaults(func=cmd_manual_checklist)

    d = sub.add_parser("apps-script-plan")
    d.set_defaults(func=cmd_apps_script_plan)

    args = p.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
