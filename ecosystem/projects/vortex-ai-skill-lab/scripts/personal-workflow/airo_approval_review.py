#!/usr/bin/env python3
import argparse, datetime, json, sqlite3, textwrap
from pathlib import Path

DEFAULT_ROOT = Path.home() / ".local/share/airo-personal-workflow"

def now():
    return datetime.datetime.now().isoformat(timespec="seconds")

def emit(obj, code=0):
    print(json.dumps(obj, indent=2, ensure_ascii=False))
    raise SystemExit(code)

def db_path(root):
    return Path(root).expanduser().resolve() / "approval_queue.sqlite"

def audit_path(root):
    p = Path(root).expanduser().resolve() / "audits" / "approval_review_audit.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

def write_audit(root, record):
    p = audit_path(root)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return str(p)

def connect(root):
    db = db_path(root)
    if not db.exists():
        emit({"ok": False, "error": "approval queue db not found", "db": str(db)}, 2)
    con = sqlite3.connect(str(db))
    con.row_factory = sqlite3.Row
    return con

def parse_payload(raw):
    try:
        return json.loads(raw or "{}")
    except Exception:
        return {"raw": raw or ""}

def row_to_item(row):
    d = dict(row)
    d["payload"] = parse_payload(d.pop("payload_json", ""))
    return d

def load_item(root, item_id):
    con = connect(root)
    row = con.execute("select * from approval_queue where id=?", (item_id,)).fetchone()
    con.close()
    if not row:
        emit({"ok": False, "error": "queue item not found", "id": item_id}, 2)
    return row_to_item(row)

def item_summary(item):
    payload = item.get("payload", {})
    payload_keys = sorted(payload.keys()) if isinstance(payload, dict) else []
    return {
        "id": item.get("id"),
        "title": item.get("title"),
        "status": item.get("status"),
        "action_type": item.get("action_type"),
        "risk_level": item.get("risk_level"),
        "source": item.get("source"),
        "created_at": item.get("created_at"),
        "updated_at": item.get("updated_at"),
        "approval_note": item.get("approval_note"),
        "payload_keys": payload_keys,
        "payload_preview": json.dumps(payload, ensure_ascii=False)[:900]
    }

def recommendation_for(item):
    item_id = item.get("id")
    status = item.get("status")
    action = item.get("action_type")

    base = {
        "item_id": item_id,
        "status": status,
        "action_type": action,
        "execution_performed": False
    }

    if status == "pending":
        return {
            **base,
            "decision": "approval_review_required",
            "next_action": "Inspect item, then approve or reject.",
            "inspect_command": f"python3 scripts/personal-workflow/airo_approval_review.py inspect --id {item_id}",
            "approve_command": f"python3 scripts/personal-workflow/airo_approval_review.py approve --id {item_id} --confirm YES --note \"approved after review\"",
            "reject_command": f"python3 scripts/personal-workflow/airo_approval_review.py reject --id {item_id} --confirm YES --note \"rejected after review\""
        }

    if status == "approved" and action == "google_sheets_write":
        return {
            **base,
            "decision": "dry_run_google_sheets_executor",
            "next_action": "Run queue executor dry-run.",
            "dry_run_command": f"python3 scripts/personal-workflow/airo_queue_executor.py --id {item_id} --mode dry-run",
            "execute_command_template": f"python3 scripts/personal-workflow/airo_queue_executor.py --id {item_id} --mode execute --spreadsheet-id \"<sheet_id>\" --approve-execute YES"
        }

    if status == "approved" and action == "sqlite_mutation":
        return {
            **base,
            "decision": "dry_run_transaction_executor",
            "next_action": "Run transaction executor dry-run.",
            "dry_run_command": f"python3 scripts/personal-workflow/airo_transaction_executor.py --id {item_id} --mode dry-run",
            "execute_command_template": f"python3 scripts/personal-workflow/airo_transaction_executor.py --id {item_id} --mode execute --approve-execute YES"
        }

    if status == "approved":
        return {
            **base,
            "decision": "approved_manual_review",
            "next_action": "Use executor recommendation helper.",
            "recommended_command": f"python3 scripts/personal-workflow/airo_executor_recommend.py recommend --id {item_id}"
        }

    return {
        **base,
        "decision": "no_execution_action",
        "next_action": "No executor action required."
    }

def update_status(root, item_id, status, note, confirm):
    item = load_item(root, item_id)
    current = item.get("status")

    if current == "executed":
        emit({"ok": False, "decision": "blocked", "error": "executed item cannot be changed", "id": item_id}, 2)

    if confirm != "YES":
        record = {
            "ok": False,
            "operation": f"approval_review_{status}",
            "id": item_id,
            "previous_status": current,
            "new_status": None,
            "decision": "blocked_missing_confirm_yes",
            "required_flag": "--confirm YES",
            "execution_performed": False,
            "status_changed": False
        }
        record["audit_file"] = write_audit(root, record)
        emit(record, 2)

    con = connect(root)
    con.execute(
        "update approval_queue set status=?, approval_note=?, updated_at=? where id=?",
        (status, note, now(), item_id)
    )
    con.commit()
    con.close()

    updated = load_item(root, item_id)
    record = {
        "ok": True,
        "operation": f"approval_review_{status}",
        "id": item_id,
        "previous_status": current,
        "new_status": status,
        "note": note,
        "execution_performed": False,
        "status_changed": True
    }
    record["audit_file"] = write_audit(root, record)
    return updated, record

def print_compact(items):
    if not items:
        print("No items found.")
        return
    for item in items:
        title = str(item.get("title") or "")[:70]
        print(f"#{item.get('id')} [{item.get('status')}] {item.get('action_type')} risk={item.get('risk_level')} :: {title}")
        rec = recommendation_for(item)
        cmd = rec.get("dry_run_command") or rec.get("inspect_command") or rec.get("recommended_command")
        if cmd:
            print(f"  next: {cmd}")

def main():
    p = argparse.ArgumentParser(description="Airo approval review CLI with safer UX")
    p.add_argument("--root", default=str(DEFAULT_ROOT))
    p.add_argument("--text", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("list")
    a.add_argument("--status", default="pending", choices=["pending", "approved", "rejected", "executed", "all"])
    a.add_argument("--limit", type=int, default=20)
    a.add_argument("--compact", action="store_true")

    b = sub.add_parser("summary")
    b.add_argument("--id", type=int, required=True)

    c = sub.add_parser("inspect")
    c.add_argument("--id", type=int, required=True)

    d = sub.add_parser("recommend")
    d.add_argument("--id", type=int, required=True)

    e = sub.add_parser("approve")
    e.add_argument("--id", type=int, required=True)
    e.add_argument("--note", default="approved from approval review CLI")
    e.add_argument("--confirm", default="NO")

    f = sub.add_parser("reject")
    f.add_argument("--id", type=int, required=True)
    f.add_argument("--note", default="rejected from approval review CLI")
    f.add_argument("--confirm", default="NO")

    args = p.parse_args()
    root = args.root

    if args.cmd == "list":
        con = connect(root)
        if args.status == "all":
            rows = con.execute("select * from approval_queue order by id desc limit ?", (args.limit,)).fetchall()
        else:
            rows = con.execute("select * from approval_queue where status=? order by id desc limit ?", (args.status, args.limit)).fetchall()
        con.close()
        items = [row_to_item(r) for r in rows]
        if args.compact or args.text:
            print_compact(items)
            return
        emit({
            "ok": True,
            "operation": "approval_review_list",
            "status": args.status,
            "count": len(items),
            "items": items,
            "execution_performed": False
        })

    if args.cmd == "summary":
        item = load_item(root, args.id)
        emit({
            "ok": True,
            "operation": "approval_review_summary",
            "summary": item_summary(item),
            "recommendation": recommendation_for(item),
            "execution_performed": False
        })

    if args.cmd == "inspect":
        item = load_item(root, args.id)
        emit({
            "ok": True,
            "operation": "approval_review_inspect",
            "item": item,
            "summary": item_summary(item),
            "recommendation": recommendation_for(item),
            "execution_performed": False
        })

    if args.cmd == "recommend":
        item = load_item(root, args.id)
        emit({
            "ok": True,
            "operation": "approval_review_recommend",
            "recommendation": recommendation_for(item),
            "execution_performed": False
        })

    if args.cmd == "approve":
        item, record = update_status(root, args.id, "approved", args.note, args.confirm)
        emit({
            "ok": True,
            "operation": "approval_review_approve",
            "item": item,
            "summary": item_summary(item),
            "audit": record,
            "recommendation": recommendation_for(item),
            "execution_performed": False
        })

    if args.cmd == "reject":
        item, record = update_status(root, args.id, "rejected", args.note, args.confirm)
        emit({
            "ok": True,
            "operation": "approval_review_reject",
            "item": item,
            "summary": item_summary(item),
            "audit": record,
            "execution_performed": False
        })

if __name__ == "__main__":
    main()
