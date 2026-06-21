#!/usr/bin/env python3
import argparse, datetime, json, os, sqlite3, subprocess, sys, tempfile
from pathlib import Path

DEFAULT_ROOT = Path.home() / ".local/share/airo-personal-workflow"
SHEETS_WRITER = Path("scripts/personal-workflow/airo_google_sheets_writer.py")
SUPPORTED_ACTIONS = {"google_sheets_write"}
BLOCKED_ACTIONS = {"live_trading", "earnsai_runtime_access", "browser_profile_access", "secret_read", "cookie_read", "session_read", "finance_delete", "service_restart"}

def now():
    return datetime.datetime.now().isoformat(timespec="seconds")

def emit(obj, code=0):
    print(json.dumps(obj, indent=2, ensure_ascii=False))
    raise SystemExit(code)

def db_path(root):
    return Path(root).expanduser().resolve() / "approval_queue.sqlite"

def audit_path(root):
    p = Path(root).expanduser().resolve() / "audits" / "queue_executor_audit.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

def load_item(root, item_id):
    db = db_path(root)
    if not db.exists():
        emit({"ok": False, "error": "approval queue db not found", "db": str(db)}, 2)
    con = sqlite3.connect(str(db))
    con.row_factory = sqlite3.Row
    row = con.execute("select * from approval_queue where id=?", (item_id,)).fetchone()
    con.close()
    if not row:
        emit({"ok": False, "error": "queue item not found", "id": item_id}, 2)
    d = dict(row)
    try:
        d["payload"] = json.loads(d.pop("payload_json") or "{}")
    except Exception:
        d["payload"] = {}
    return d

def update_executed(root, item_id, note):
    db = db_path(root)
    con = sqlite3.connect(str(db))
    con.execute("update approval_queue set status=?, approval_note=?, updated_at=? where id=?", ("executed", note, now(), item_id))
    con.commit()
    con.close()

def audit(root, record):
    p = audit_path(root)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return str(p)

def nested_payload(payload):
    if isinstance(payload, dict) and isinstance(payload.get("payload"), dict):
        return payload["payload"]
    return payload if isinstance(payload, dict) else {}

def extract_rows(payload):
    p = nested_payload(payload)
    if isinstance(p.get("rows"), list):
        return p["rows"]
    if isinstance(p.get("rows_preview"), list):
        return p["rows_preview"]
    payload_file = p.get("payload_file") or payload.get("payload_file")
    if payload_file and Path(payload_file).exists():
        with open(payload_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and isinstance(data.get("rows"), list):
            return data["rows"]
        if isinstance(data, list):
            return data
    return []

def extract_range(payload, default_range):
    p = nested_payload(payload)
    return p.get("range") or payload.get("range") or default_range

def main():
    parser = argparse.ArgumentParser(description="Airo approved queue executor")
    parser.add_argument("--root", default=str(DEFAULT_ROOT))
    parser.add_argument("--id", type=int, required=True)
    parser.add_argument("--mode", choices=["dry-run", "execute"], default="dry-run")
    parser.add_argument("--approve-execute", default="NO")
    parser.add_argument("--spreadsheet-id", default=os.environ.get("AIRO_GOOGLE_SHEETS_SPREADSHEET_ID", ""))
    parser.add_argument("--range", default=os.environ.get("AIRO_GOOGLE_SHEETS_RANGE", "Airo!A:D"))
    args = parser.parse_args()

    item = load_item(args.root, args.id)
    action_type = item.get("action_type", "")
    payload = item.get("payload", {})
    status = item.get("status", "")

    base = {
        "ok": True,
        "operation": "queue_executor",
        "mode": args.mode,
        "id": args.id,
        "status": status,
        "action_type": action_type,
        "execution_performed": False
    }

    if action_type in BLOCKED_ACTIONS:
        record = {**base, "ok": False, "decision": "blocked_action_type"}
        audit_file = audit(args.root, record)
        record["audit_file"] = audit_file
        emit(record, 2)

    if action_type not in SUPPORTED_ACTIONS:
        record = {**base, "ok": False, "decision": "unsupported_action_type", "supported": sorted(SUPPORTED_ACTIONS)}
        audit_file = audit(args.root, record)
        record["audit_file"] = audit_file
        emit(record, 2)

    if status != "approved":
        record = {**base, "ok": False, "decision": "not_executable_until_approved"}
        audit_file = audit(args.root, record)
        record["audit_file"] = audit_file
        emit(record, 2)

    rows = extract_rows(payload)
    target_range = extract_range(payload, args.range)

    if not rows:
        record = {**base, "ok": False, "decision": "missing_rows_payload"}
        audit_file = audit(args.root, record)
        record["audit_file"] = audit_file
        emit(record, 2)

    preview = {
        **base,
        "decision": "ready",
        "target": {
            "spreadsheet_id_set": bool(args.spreadsheet_id),
            "range": target_range
        },
        "row_count": len(rows),
        "rows_preview": rows[:5]
    }

    if args.mode == "dry-run":
        preview["decision"] = "dry_run_ready_no_execution"
        audit_file = audit(args.root, preview)
        preview["audit_file"] = audit_file
        emit(preview)

    if args.approve_execute != "YES":
        record = {**preview, "ok": False, "decision": "execute_blocked_missing_approval_flag"}
        audit_file = audit(args.root, record)
        record["audit_file"] = audit_file
        emit(record, 2)

    if not args.spreadsheet_id:
        record = {**preview, "ok": False, "decision": "execute_blocked_missing_spreadsheet_id"}
        audit_file = audit(args.root, record)
        record["audit_file"] = audit_file
        emit(record, 2)

    if not SHEETS_WRITER.exists():
        record = {**preview, "ok": False, "decision": "execute_blocked_missing_sheets_writer"}
        audit_file = audit(args.root, record)
        record["audit_file"] = audit_file
        emit(record, 2)

    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump({"rows": rows}, f, indent=2, ensure_ascii=False)
        tmp_payload = f.name

    try:
        cmd = [
            sys.executable,
            str(SHEETS_WRITER),
            "--mode", "real",
            "--auth-method", "oauth",
            "--spreadsheet-id", args.spreadsheet_id,
            "--range", target_range,
            "--payload", tmp_payload,
            "--approve-real-write", "YES"
        ]
        out = subprocess.check_output(cmd, text=True)
        write_result = json.loads(out)
    finally:
        try:
            os.unlink(tmp_payload)
        except Exception:
            pass

    update_executed(args.root, args.id, "Executed by airo_queue_executor.py at " + now())
    record = {
        **preview,
        "decision": "executed",
        "execution_performed": True,
        "write_result": write_result
    }
    audit_file = audit(args.root, record)
    record["audit_file"] = audit_file
    emit(record)

if __name__ == "__main__":
    main()
