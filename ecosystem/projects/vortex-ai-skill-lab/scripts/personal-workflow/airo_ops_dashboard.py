#!/usr/bin/env python3
import argparse, datetime, html, json, sqlite3
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

def esc(value):
    return html.escape(str(value if value is not None else ""))

def read_jsonl(path, limit=40):
    p = Path(path)
    if not p.exists():
        return []
    rows = []
    for line in p.read_text(encoding="utf-8", errors="ignore").splitlines()[-limit:]:
        try:
            rows.append(json.loads(line))
        except Exception:
            rows.append({"ok": False, "raw": line[:1000]})
    return list(reversed(rows))

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

def read_queue(root, limit=200):
    db = root / "approval_queue.sqlite"
    result = {
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
        return result

    con = sqlite3.connect(str(db))
    con.row_factory = sqlite3.Row
    rows = con.execute("select * from approval_queue order by id desc limit ?", (limit,)).fetchall()
    con.close()

    for row in rows:
        item = dict(row)
        item["payload"] = parse_payload(item.pop("payload_json", ""))
        status = item.get("status", "unknown")
        result["counts"][status] = result["counts"].get(status, 0) + 1
        result["items"].append(item)
        if status in result:
            result[status].append(item)

    return result

def read_receipts(root, limit=50):
    db = root / "receipts" / "manifest.sqlite"
    result = {"db": str(db), "exists": db.exists(), "items": [], "count": 0}
    if not db.exists():
        return result
    con = sqlite3.connect(str(db))
    con.row_factory = sqlite3.Row
    rows = con.execute("select id, created_at, original_name, sha256, size_bytes, kind, mime, source, status, note from receipt_attachments order by id desc limit ?", (limit,)).fetchall()
    con.close()
    result["items"] = [dict(r) for r in rows]
    result["count"] = len(result["items"])
    return result

def list_files(path, pattern, limit=30):
    p = Path(path)
    if not p.exists():
        return []
    files = sorted(p.glob(pattern), key=lambda x: x.stat().st_mtime, reverse=True)[:limit]
    return [
        {
            "name": f.name,
            "path": str(f),
            "size_bytes": f.stat().st_size,
            "modified": datetime.datetime.fromtimestamp(f.stat().st_mtime).isoformat(timespec="seconds")
        }
        for f in files
    ]

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

    if action in BLOCKED_ACTIONS:
        return {
            **base,
            "decision": "blocked_action",
            "next_action": "Do not execute.",
            "recommended_command": None
        }

    if status == "pending":
        return {
            **base,
            "decision": "approval_review_required",
            "next_action": "Inspect then approve or reject.",
            "inspect_command": f"python3 scripts/personal-workflow/airo_approval_review.py inspect --id {item_id}",
            "approve_command_template": f"python3 scripts/personal-workflow/airo_approval_review.py approve --id {item_id} --note \"approved after review\"",
            "reject_command_template": f"python3 scripts/personal-workflow/airo_approval_review.py reject --id {item_id} --note \"rejected after review\""
        }

    if status == "approved" and action == "google_sheets_write":
        return {
            **base,
            "decision": "google_sheets_executor_dry_run_recommended",
            "next_action": "Run queue executor dry-run.",
            "dry_run_command": f"python3 scripts/personal-workflow/airo_queue_executor.py --id {item_id} --mode dry-run",
            "execute_command_template": f"python3 scripts/personal-workflow/airo_queue_executor.py --id {item_id} --mode execute --spreadsheet-id \"<sheet_id>\" --approve-execute YES"
        }

    if status == "approved" and action == "sqlite_mutation":
        return {
            **base,
            "decision": "transaction_executor_dry_run_recommended",
            "next_action": "Run transaction executor dry-run.",
            "dry_run_command": f"python3 scripts/personal-workflow/airo_transaction_executor.py --id {item_id} --mode dry-run",
            "execute_command_template": f"python3 scripts/personal-workflow/airo_transaction_executor.py --id {item_id} --mode execute --approve-execute YES"
        }

    if status == "approved" and action == "receipt_to_transaction":
        return {
            **base,
            "decision": "receipt_needs_transaction_proposal",
            "next_action": "Create transaction proposal dry-run first.",
            "recommended_command": "python3 scripts/personal-workflow/airo_transaction_proposal.py receipt.pdf --mode dry-run --description \"...\" --amount \"...\""
        }

    if status == "approved":
        return {
            **base,
            "decision": "approved_but_unsupported_executor",
            "next_action": "Inspect manually.",
            "recommended_command": f"python3 scripts/personal-workflow/airo_approval_review.py inspect --id {item_id}"
        }

    if status == "executed":
        return {
            **base,
            "decision": "already_executed",
            "next_action": "No execution action required."
        }

    if status == "rejected":
        return {
            **base,
            "decision": "rejected",
            "next_action": "No execution action required."
        }

    return {
        **base,
        "decision": "manual_review_required",
        "next_action": "Inspect manually.",
        "recommended_command": f"python3 scripts/personal-workflow/airo_approval_review.py inspect --id {item_id}"
    }

def failure_items(*audit_lists):
    failed = []
    for audits in audit_lists:
        for item in audits:
            decision = str(item.get("decision", "")).lower()
            if item.get("ok") is False or "error" in item or "blocked" in decision:
                failed.append(item)
    return failed[:30]

def card(title, body):
    return f"<section class='card'><h2>{esc(title)}</h2>{body}</section>"

def metric(title, value, note=""):
    return f"<div class='metric'><span>{esc(title)}</span><b>{esc(value)}</b><small>{esc(note)}</small></div>"

def table(rows, cols):
    if not rows:
        return "<p class='muted'>No records found.</p>"
    head = "".join(f"<th>{esc(c)}</th>" for c in cols)
    body = []
    for r in rows:
        body.append("<tr>" + "".join(f"<td>{esc(r.get(c,''))}</td>" for c in cols) + "</tr>")
    return f"<table><thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table>"

def recommendation_cards(items, limit=30):
    if not items:
        return "<p class='muted'>No actionable queue items found.</p>"
    out = []
    for item in items[:limit]:
        rec = recommendation_for(item)
        payload = json.dumps(item.get("payload", {}), indent=2, ensure_ascii=False)[:2500]
        commands = []
        for key in ["inspect_command", "dry_run_command", "recommended_command", "approve_command_template", "reject_command_template", "execute_command_template"]:
            if rec.get(key):
                commands.append(f"<p><b>{esc(key)}:</b></p><pre>{esc(rec[key])}</pre>")
        out.append(
            "<div class='item'>"
            f"<h3>#{esc(item.get('id'))} {esc(item.get('title'))}</h3>"
            f"<p><b>Status:</b> {esc(item.get('status'))} | <b>Type:</b> {esc(item.get('action_type'))} | <b>Risk:</b> {esc(item.get('risk_level'))}</p>"
            f"<p><b>Decision:</b> {esc(rec.get('decision'))}</p>"
            f"<p><b>Next action:</b> {esc(rec.get('next_action'))}</p>"
            + "".join(commands) +
            f"<details><summary>Payload preview</summary><pre>{esc(payload)}</pre></details>"
            "</div>"
        )
    return "".join(out)

def json_cards(items, limit=20):
    if not items:
        return "<p class='muted'>No audit records found.</p>"
    return "".join(f"<pre>{esc(json.dumps(item, indent=2, ensure_ascii=False)[:3500])}</pre>" for item in items[:limit])

def main():
    p = argparse.ArgumentParser(description="Airo daily operations dashboard with next-action recommendations")
    p.add_argument("--root", default=str(DEFAULT_ROOT))
    p.add_argument("--output", default="")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    root = Path(args.root).expanduser().resolve()
    out_dir = Path(args.output).expanduser().resolve() if args.output else root / "dashboard"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "daily_ops.html"

    queue = read_queue(root)
    receipts = read_receipts(root)
    queue_executor_audits = read_jsonl(root / "audits" / "queue_executor_audit.jsonl")
    transaction_executor_audits = read_jsonl(root / "audits" / "transaction_executor_audit.jsonl")
    recommendation_audits = read_jsonl(root / "audits" / "executor_recommendation_audit.jsonl")
    approval_review_audits = read_jsonl(root / "audits" / "approval_review_audit.jsonl")
    sync_audits = read_jsonl(root / "audits" / "sheets_sync_audit.jsonl")
    fallback_audits = read_jsonl(root / "audits" / "google_fallback_audit.jsonl")
    failed = failure_items(queue_executor_audits, transaction_executor_audits, sync_audits, fallback_audits)

    fallback_exports = list_files(root / "exports" / "google_api_fallback", "*.csv")
    sheet_fallback_exports = list_files(root / "exports" / "sheets_fallback", "*.csv")

    sync_ready = {
        "oauth_client_exists": (root / "google" / "oauth_client.local.json").exists(),
        "oauth_token_exists": (root / "google" / "token.local.json").exists(),
        "oauth_client": file_meta(root / "google" / "oauth_client.local.json"),
        "oauth_token": file_meta(root / "google" / "token.local.json")
    }

    actionable = queue["pending"] + queue["approved"]
    recommendations = [recommendation_for(i) for i in actionable]

    top_actions = []
    if queue["pending"]:
        top_actions.append("Review pending approvals.")
    if queue["approved"]:
        top_actions.append("Run dry-run executor for approved queue items.")
    if not sync_ready["oauth_token_exists"]:
        top_actions.append("OAuth token is missing. Use CSV fallback or restore OAuth flow before real Sheets sync.")
    if failed:
        top_actions.append("Review failed or blocked audit records.")
    if not top_actions:
        top_actions.append("No urgent action detected. Continue normal capture and review flow.")

    summary = {
        "ok": True,
        "operation": "daily_ops_dashboard_next_action",
        "generated": now(),
        "root": str(root),
        "dashboard": str(out_file),
        "queue_counts": queue["counts"],
        "pending_count": len(queue["pending"]),
        "approved_count": len(queue["approved"]),
        "executed_count": len(queue["executed"]),
        "rejected_count": len(queue["rejected"]),
        "actionable_count": len(actionable),
        "recommendations": recommendations,
        "sync_ready": sync_ready,
        "fallback_export_count": len(fallback_exports) + len(sheet_fallback_exports),
        "failed_audit_count_shown": len(failed),
        "top_actions": top_actions,
        "read_only": True
    }

    if args.json:
        emit(summary)

    action_list = "".join(f"<li>{esc(a)}</li>" for a in top_actions)

    page = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Airo Daily Ops Dashboard</title>
<style>
body {{ margin:0; font-family:system-ui,-apple-system,Segoe UI,sans-serif; background:#f5f7fb; color:#111827; }}
header {{ background:#111827; color:white; padding:30px 38px; }}
main {{ max-width:1360px; margin:auto; padding:28px 38px; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(210px,1fr)); gap:16px; margin:20px 0 28px; }}
.metric {{ background:white; border:1px solid #e5e7eb; border-radius:16px; padding:18px; box-shadow:0 1px 2px rgba(0,0,0,.04); }}
.metric span {{ display:block; color:#4b5563; }}
.metric b {{ display:block; font-size:30px; margin:6px 0; }}
.metric small {{ color:#6b7280; }}
.card {{ background:white; border:1px solid #e5e7eb; border-radius:16px; padding:20px; margin:18px 0; box-shadow:0 1px 2px rgba(0,0,0,.04); }}
.item {{ border-top:1px solid #e5e7eb; padding:14px 0; }}
pre {{ background:#f3f4f6; padding:12px; border-radius:10px; overflow:auto; white-space:pre-wrap; }}
table {{ width:100%; border-collapse:collapse; }}
th,td {{ text-align:left; padding:10px; border-bottom:1px solid #e5e7eb; font-size:14px; vertical-align:top; }}
th {{ background:#f9fafb; }}
.muted {{ color:#6b7280; }}
</style>
</head>
<body>
<header>
<h1>Airo Daily Ops Dashboard</h1>
<p>Generated {esc(summary["generated"])}. Read-only local dashboard with next-action recommendations.</p>
</header>
<main>
<div class="grid">
{metric("Pending approvals", len(queue["pending"]), "review first")}
{metric("Approved items", len(queue["approved"]), "dry-run next")}
{metric("Executed items", len(queue["executed"]), "completed")}
{metric("Rejected items", len(queue["rejected"]), "no execution")}
{metric("Actionable items", len(actionable), "pending + approved")}
{metric("Failed/error audits", len(failed), "needs attention")}
{metric("Fallback CSV files", len(fallback_exports) + len(sheet_fallback_exports), "manual import path")}
{metric("OAuth token", "OK" if sync_ready["oauth_token_exists"] else "MISSING", "content not read")}
</div>

{card("Top Next Actions", "<ul>" + action_list + "</ul>")}
{card("Actionable Queue Recommendations", recommendation_cards(actionable))}
{card("Pending Approval Summary", recommendation_cards(queue["pending"]))}
{card("Approved Executor Recommendations", recommendation_cards(queue["approved"]))}
{card("Google Sync Readiness", f"<pre>{esc(json.dumps(sync_ready, indent=2, ensure_ascii=False))}</pre>")}
{card("Rejected / Error / Blocked Visibility", json_cards(failed))}
{card("Executor Recommendation Audits", json_cards(recommendation_audits))}
{card("Approval Review Audits", json_cards(approval_review_audits))}
{card("Queue Executor Audits", json_cards(queue_executor_audits))}
{card("Transaction Executor Audits", json_cards(transaction_executor_audits))}
{card("Google Sheets Sync Audits", json_cards(sync_audits))}
{card("Fallback CSV Exports", table(fallback_exports + sheet_fallback_exports, ["name","size_bytes","modified","path"]))}
{card("Receipt Attachments", table(receipts["items"], ["id","created_at","original_name","kind","size_bytes","status","source"]))}

<section class="card">
<h2>Safety Boundary</h2>
<p>This dashboard is read-only. It does not execute approved items, write to Google, mutate finance records, patch OpenClaw, restart services, access browser profiles, read token contents, or touch EarnsAI runtime.</p>
</section>
</main>
</body>
</html>
"""
    out_file.write_text(page, encoding="utf-8")
    emit(summary)

if __name__ == "__main__":
    main()
