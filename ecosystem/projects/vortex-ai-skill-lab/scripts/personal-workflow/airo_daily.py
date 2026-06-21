#!/usr/bin/env python3
import argparse, datetime, json, sqlite3
from pathlib import Path

DEFAULT_ROOT = Path.home() / ".local/share/airo-personal-workflow"

def now():
    return datetime.datetime.now().isoformat(timespec="seconds")

def emit(obj, code=0):
    print(json.dumps(obj, indent=2, ensure_ascii=False))
    raise SystemExit(code)

def jsonl_count(path):
    p = Path(path)
    if not p.exists():
        return {"path": str(p), "exists": False, "lines": 0}
    return {"path": str(p), "exists": True, "lines": len(p.read_text(encoding="utf-8", errors="ignore").splitlines())}

def file_meta(path):
    p = Path(path)
    return {
        "path": str(p),
        "exists": p.exists(),
        "is_file": p.is_file() if p.exists() else False,
        "size_bytes": p.stat().st_size if p.exists() and p.is_file() else None,
        "content_read": False
    }

def parse_payload(raw):
    try:
        return json.loads(raw or "{}")
    except Exception:
        return {"raw": raw or ""}

def read_queue(root, limit=100):
    db = root / "approval_queue.sqlite"
    out = {
        "db": str(db),
        "exists": db.exists(),
        "items": [],
        "counts": {},
        "pending": [],
        "approved": [],
        "executed": [],
        "rejected": []
    }
    if not db.exists():
        return out

    con = sqlite3.connect(str(db))
    con.row_factory = sqlite3.Row
    rows = con.execute("select * from approval_queue order by id desc limit ?", (limit,)).fetchall()
    con.close()

    for row in rows:
        item = dict(row)
        item["payload"] = parse_payload(item.pop("payload_json", ""))
        status = item.get("status", "unknown")
        out["counts"][status] = out["counts"].get(status, 0) + 1
        out["items"].append(item)
        if status in out:
            out[status].append(item)

    return out

def recommend(item):
    item_id = item.get("id")
    status = item.get("status")
    action = item.get("action_type")

    if status == "pending":
        return {
            "item_id": item_id,
            "next_action": "review",
            "command": f"python3 scripts/personal-workflow/airo_approval_review.py inspect --id {item_id}"
        }

    if status == "approved" and action == "google_sheets_write":
        return {
            "item_id": item_id,
            "next_action": "dry_run_google_sheets_executor",
            "command": f"python3 scripts/personal-workflow/airo_queue_executor.py --id {item_id} --mode dry-run"
        }

    if status == "approved" and action == "sqlite_mutation":
        return {
            "item_id": item_id,
            "next_action": "dry_run_transaction_executor",
            "command": f"python3 scripts/personal-workflow/airo_transaction_executor.py --id {item_id} --mode dry-run"
        }

    if status == "approved":
        return {
            "item_id": item_id,
            "next_action": "manual_executor_review",
            "command": f"python3 scripts/personal-workflow/airo_executor_recommend.py recommend --id {item_id}"
        }

    return {
        "item_id": item_id,
        "next_action": "none",
        "command": None
    }

def build_daily(root):
    queue = read_queue(root)
    dashboard = root / "dashboard" / "daily_ops.html"

    audits = {
        "approval_review": jsonl_count(root / "audits" / "approval_review_audit.jsonl"),
        "executor_recommendation": jsonl_count(root / "audits" / "executor_recommendation_audit.jsonl"),
        "queue_executor": jsonl_count(root / "audits" / "queue_executor_audit.jsonl"),
        "transaction_executor": jsonl_count(root / "audits" / "transaction_executor_audit.jsonl"),
        "sheets_sync": jsonl_count(root / "audits" / "sheets_sync_audit.jsonl"),
        "google_fallback": jsonl_count(root / "audits" / "google_fallback_audit.jsonl")
    }

    sync = {
        "oauth_client_exists": (root / "google" / "oauth_client.local.json").exists(),
        "oauth_token_exists": (root / "google" / "token.local.json").exists(),
        "oauth_client": file_meta(root / "google" / "oauth_client.local.json"),
        "oauth_token": file_meta(root / "google" / "token.local.json")
    }

    actionable = queue["pending"] + queue["approved"]
    recommendations = [recommend(i) for i in actionable[:20]]

    next_actions = []
    if queue["pending"]:
        next_actions.append({
            "priority": 1,
            "label": "Review pending approvals",
            "command": "python3 scripts/personal-workflow/airo_approval_review.py list --status pending --limit 10"
        })
    if queue["approved"]:
        next_actions.append({
            "priority": 2,
            "label": "Dry-run approved queue items",
            "command": "python3 scripts/personal-workflow/airo_executor_recommend.py list-approved --limit 10"
        })
    if not sync["oauth_token_exists"]:
        next_actions.append({
            "priority": 3,
            "label": "Google OAuth token missing; use fallback status",
            "command": "python3 scripts/personal-workflow/airo_google_fallback.py status"
        })
    next_actions.append({
        "priority": 4,
        "label": "Refresh daily ops dashboard",
        "command": "python3 scripts/personal-workflow/airo_ops_dashboard.py"
    })

    return {
        "ok": True,
        "operation": "airo_daily",
        "generated": now(),
        "root": str(root),
        "queue_counts": queue["counts"],
        "pending_count": len(queue["pending"]),
        "approved_count": len(queue["approved"]),
        "executed_count": len(queue["executed"]),
        "rejected_count": len(queue["rejected"]),
        "actionable_count": len(actionable),
        "recommendations": recommendations,
        "next_actions": next_actions,
        "google_sync_readiness": sync,
        "audit_counts": audits,
        "dashboard": str(dashboard),
        "dashboard_exists": dashboard.exists(),
        "read_only": True,
        "execution_performed": False,
        "safety": {
            "secret_read": False,
            "token_content_read": False,
            "credential_content_read": False,
            "browser_profile_access": False,
            "google_write": False,
            "sqlite_mutation": False,
            "service_restart": False,
            "earnsai_runtime_access": False,
            "live_trading": False
        }
    }

def print_text(summary):
    print("AIRO DAILY")
    print(f"Generated: {summary['generated']}")
    print(f"Pending approvals: {summary['pending_count']}")
    print(f"Approved items: {summary['approved_count']}")
    print(f"Actionable items: {summary['actionable_count']}")
    print(f"Dashboard: {summary['dashboard']}")
    print("")
    print("Next actions:")
    for item in summary["next_actions"]:
        print(f"- {item['label']}")
        print(f"  {item['command']}")
    if summary["recommendations"]:
        print("")
        print("Item recommendations:")
        for rec in summary["recommendations"][:10]:
            print(f"- #{rec['item_id']} {rec['next_action']}")
            if rec.get("command"):
                print(f"  {rec['command']}")

def main():
    p = argparse.ArgumentParser(description="Airo unified daily command")
    p.add_argument("--root", default=str(DEFAULT_ROOT))
    p.add_argument("--text", action="store_true")
    args = p.parse_args()

    root = Path(args.root).expanduser().resolve()
    summary = build_daily(root)

    if args.text:
        print_text(summary)
        return

    emit(summary)

if __name__ == "__main__":
    main()
