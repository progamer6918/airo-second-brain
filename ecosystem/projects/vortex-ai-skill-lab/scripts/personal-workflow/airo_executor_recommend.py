#!/usr/bin/env python3
import argparse, datetime, json, sqlite3
from pathlib import Path

DEFAULT_ROOT = Path.home() / ".local/share/airo-personal-workflow"

BLOCKED_ACTIONS = {
    "live_trading",
    "earnsai_runtime_access",
    "browser_profile_access",
    "secret_read",
    "cookie_read",
    "session_read",
    "finance_delete",
    "service_restart"
}

def now():
    return datetime.datetime.now().isoformat(timespec="seconds")

def emit(obj, code=0):
    print(json.dumps(obj, indent=2, ensure_ascii=False))
    raise SystemExit(code)

def db_path(root):
    return Path(root).expanduser().resolve() / "approval_queue.sqlite"

def audit_path(root):
    p = Path(root).expanduser().resolve() / "audits" / "executor_recommendation_audit.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

def audit(root, record):
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

def parse_item(row):
    d = dict(row)
    raw = d.pop("payload_json", "") if "payload_json" in d else ""
    try:
        d["payload"] = json.loads(raw or "{}")
    except Exception:
        d["payload"] = {"raw": raw}
    return d

def load_item(root, item_id):
    con = connect(root)
    row = con.execute("select * from approval_queue where id=?", (item_id,)).fetchone()
    con.close()
    if not row:
        emit({"ok": False, "error": "queue item not found", "id": item_id}, 2)
    return parse_item(row)

def recommend(item):
    item_id = item.get("id")
    status = item.get("status")
    action = item.get("action_type")
    payload = item.get("payload", {})

    base = {
        "item_id": item_id,
        "status": status,
        "action_type": action,
        "execution_performed": False
    }

    if action in BLOCKED_ACTIONS:
        return {
            **base,
            "ok": False,
            "decision": "blocked_action",
            "reason": "Action is outside Airo Personal Workflow safety boundary.",
            "recommended_command": None
        }

    if status != "approved":
        return {
            **base,
            "ok": True,
            "decision": "not_ready_approval_required",
            "inspect_command": f"python3 scripts/personal-workflow/airo_approval_review.py inspect --id {item_id}",
            "approve_command_template": f"python3 scripts/personal-workflow/airo_approval_review.py approve --id {item_id} --note \"approved after review\"",
            "reject_command_template": f"python3 scripts/personal-workflow/airo_approval_review.py reject --id {item_id} --note \"rejected after review\""
        }

    if action == "google_sheets_write":
        detected_range = None
        if isinstance(payload, dict):
            detected_range = payload.get("range")
            if not detected_range and isinstance(payload.get("payload"), dict):
                detected_range = payload["payload"].get("range")

        return {
            **base,
            "ok": True,
            "decision": "google_sheets_executor_dry_run_recommended",
            "dry_run_command": f"python3 scripts/personal-workflow/airo_queue_executor.py --id {item_id} --mode dry-run",
            "execute_command_template": f"python3 scripts/personal-workflow/airo_queue_executor.py --id {item_id} --mode execute --spreadsheet-id \"<sheet_id>\" --approve-execute YES",
            "detected_range": detected_range,
            "warning": "Run dry-run first. Real Google Sheets write requires explicit user approval."
        }

    if action == "sqlite_mutation":
        return {
            **base,
            "ok": True,
            "decision": "transaction_executor_dry_run_recommended",
            "dry_run_command": f"python3 scripts/personal-workflow/airo_transaction_executor.py --id {item_id} --mode dry-run",
            "execute_command_template": f"python3 scripts/personal-workflow/airo_transaction_executor.py --id {item_id} --mode execute --approve-execute YES",
            "warning": "Run dry-run first. Real transaction write requires explicit user approval."
        }

    if action == "receipt_to_transaction":
        return {
            **base,
            "ok": True,
            "decision": "receipt_review_needs_transaction_proposal",
            "recommended_command": "python3 scripts/personal-workflow/airo_transaction_proposal.py receipt.pdf --mode dry-run --description \"...\" --amount \"...\"",
            "warning": "Receipt review is not executed directly. Convert to transaction proposal first."
        }

    return {
        **base,
        "ok": True,
        "decision": "unsupported_action_type",
        "recommended_command": f"python3 scripts/personal-workflow/airo_approval_review.py inspect --id {item_id}",
        "warning": "No safe executor recommendation is available for this action type."
    }

def main():
    p = argparse.ArgumentParser(description="Airo executor command recommendation helper")
    p.add_argument("--root", default=str(DEFAULT_ROOT))
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("recommend")
    a.add_argument("--id", type=int, required=True)

    b = sub.add_parser("list-approved")
    b.add_argument("--limit", type=int, default=20)

    c = sub.add_parser("list-actionable")
    c.add_argument("--limit", type=int, default=20)

    args = p.parse_args()
    root = args.root

    if args.cmd == "recommend":
        item = load_item(root, args.id)
        rec = recommend(item)
        record = {
            "ok": True,
            "operation": "executor_recommendation",
            "item": item,
            "recommendation": rec,
            "execution_performed": False
        }
        record["audit_file"] = audit(root, record)
        emit(record)

    if args.cmd == "list-approved":
        con = connect(root)
        rows = con.execute("select * from approval_queue where status='approved' order by id desc limit ?", (args.limit,)).fetchall()
        con.close()
        items = [parse_item(r) for r in rows]
        recommendations = [recommend(i) for i in items]
        record = {
            "ok": True,
            "operation": "executor_recommendation_list_approved",
            "count": len(recommendations),
            "recommendations": recommendations,
            "execution_performed": False
        }
        record["audit_file"] = audit(root, record)
        emit(record)

    if args.cmd == "list-actionable":
        con = connect(root)
        rows = con.execute(
            "select * from approval_queue where status in ('pending','approved') order by id desc limit ?",
            (args.limit,)
        ).fetchall()
        con.close()
        items = [parse_item(r) for r in rows]
        recommendations = [recommend(i) for i in items]
        record = {
            "ok": True,
            "operation": "executor_recommendation_list_actionable",
            "count": len(recommendations),
            "recommendations": recommendations,
            "execution_performed": False
        }
        record["audit_file"] = audit(root, record)
        emit(record)

if __name__ == "__main__":
    main()
