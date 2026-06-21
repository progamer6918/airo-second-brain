#!/usr/bin/env python3
import argparse, datetime, html, json, os, sqlite3
from pathlib import Path

DEFAULT_ROOT = Path.home() / ".local/share/airo-personal-workflow"
FORBIDDEN_WORDS = ["secret", "token", "cookie", "session", "password", ".env", "client_secret"]

def now():
    return datetime.datetime.now().isoformat(timespec="seconds")

def emit(obj, code=0):
    print(json.dumps(obj, indent=2, ensure_ascii=False))
    raise SystemExit(code)

def db_connect(root):
    root = Path(root).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    db = root / "approval_queue.sqlite"
    con = sqlite3.connect(str(db))
    con.row_factory = sqlite3.Row
    con.execute("""
    create table if not exists approval_queue (
        id integer primary key autoincrement,
        created_at text not null,
        updated_at text not null,
        source text not null,
        action_type text not null,
        title text not null,
        payload_json text not null,
        risk_level text not null,
        status text not null,
        approval_note text not null
    )
    """)
    con.commit()
    return con, db

def blocked_text(text):
    low = text.lower()
    return [w for w in FORBIDDEN_WORDS if w in low]

def cmd_add(args):
    con, db = db_connect(args.root)
    payload = {}
    if args.payload:
        with open(args.payload, "r", encoding="utf-8") as f:
            payload = json.load(f)
    raw = json.dumps(payload, ensure_ascii=False)
    blocked = blocked_text(args.title + " " + raw)
    if blocked:
        emit({"ok": False, "error": "blocked secret-like queue payload", "blocked_terms": blocked}, 2)
    con.execute("""
    insert into approval_queue
    (created_at, updated_at, source, action_type, title, payload_json, risk_level, status, approval_note)
    values (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (now(), now(), args.source, args.action_type, args.title, raw, args.risk_level, "pending", ""))
    con.commit()
    item_id = con.execute("select last_insert_rowid()").fetchone()[0]
    con.close()
    emit({"ok": True, "operation": "queue_add", "id": item_id, "status": "pending", "db": str(db)})

def rows_to_items(rows):
    items = []
    for r in rows:
        d = dict(r)
        try:
            d["payload"] = json.loads(d.pop("payload_json") or "{}")
        except Exception:
            d["payload"] = {}
        items.append(d)
    return items

def cmd_list(args):
    con, db = db_connect(args.root)
    if args.status == "all":
        rows = con.execute("select * from approval_queue order by id desc limit ?", (args.limit,)).fetchall()
    else:
        rows = con.execute("select * from approval_queue where status=? order by id desc limit ?", (args.status, args.limit)).fetchall()
    con.close()
    emit({"ok": True, "operation": "queue_list", "db": str(db), "count": len(rows), "items": rows_to_items(rows)})

def cmd_set_status(args, status):
    con, db = db_connect(args.root)
    row = con.execute("select * from approval_queue where id=?", (args.id,)).fetchone()
    if not row:
        emit({"ok": False, "error": "queue item not found", "id": args.id}, 2)
    if row["status"] not in ("pending", "approved"):
        emit({"ok": False, "error": "queue item is not mutable", "id": args.id, "status": row["status"]}, 2)
    if status == "approved" and row["status"] != "pending":
        emit({"ok": False, "error": "only pending item can be approved", "id": args.id}, 2)
    if status == "rejected" and row["status"] not in ("pending", "approved"):
        emit({"ok": False, "error": "item cannot be rejected", "id": args.id}, 2)
    con.execute("update approval_queue set status=?, approval_note=?, updated_at=? where id=?", (status, args.note, now(), args.id))
    con.commit()
    con.close()
    emit({"ok": True, "operation": "queue_" + status, "id": args.id, "status": status, "db": str(db)})

def cmd_dashboard(args):
    con, db = db_connect(args.root)
    rows = con.execute("select * from approval_queue order by id desc limit 100").fetchall()
    items = rows_to_items(rows)
    counts = {}
    for item in items:
        counts[item["status"]] = counts.get(item["status"], 0) + 1
    out_dir = Path(args.output).expanduser().resolve() if args.output else Path(args.root).expanduser().resolve() / "dashboard"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "index.html"
    cards = []
    for item in items:
        cards.append(
            "<div class='card'>"
            f"<h2>#{item['id']} {html.escape(item['title'])}</h2>"
            f"<p><b>Status:</b> {html.escape(item['status'])} | <b>Risk:</b> {html.escape(item['risk_level'])} | <b>Type:</b> {html.escape(item['action_type'])}</p>"
            f"<p><b>Source:</b> {html.escape(item['source'])}</p>"
            f"<pre>{html.escape(json.dumps(item.get('payload', {}), indent=2, ensure_ascii=False))}</pre>"
            f"<p><b>Note:</b> {html.escape(item.get('approval_note') or '')}</p>"
            "</div>"
        )
    page = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Airo Approval Queue</title>
<style>
body {{ font-family: system-ui, sans-serif; margin: 32px; background: #f7f7f7; color: #111; }}
h1 {{ margin-bottom: 4px; }}
.summary {{ margin: 16px 0; padding: 16px; background: white; border-radius: 12px; }}
.card {{ margin: 16px 0; padding: 16px; background: white; border-radius: 12px; border: 1px solid #ddd; }}
pre {{ white-space: pre-wrap; background: #f0f0f0; padding: 12px; border-radius: 8px; overflow: auto; }}
.small {{ color: #555; }}
</style>
</head>
<body>
<h1>Airo Local Approval Queue</h1>
<p class="small">Generated {html.escape(now())}. Local dashboard only. No action is executed from this page.</p>
<div class="summary">
<b>Total shown:</b> {len(items)}<br>
<b>Counts:</b> {html.escape(json.dumps(counts, ensure_ascii=False))}
</div>
{''.join(cards) if cards else '<p>No queue items.</p>'}
</body>
</html>
"""
    out_file.write_text(page, encoding="utf-8")
    con.close()
    emit({"ok": True, "operation": "dashboard_generate", "db": str(db), "dashboard": str(out_file), "count": len(items)})

def main():
    p = argparse.ArgumentParser(description="Airo local approval queue")
    p.add_argument("--root", default=str(DEFAULT_ROOT))
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add")
    a.add_argument("--source", default="airo")
    a.add_argument("--action-type", required=True)
    a.add_argument("--title", required=True)
    a.add_argument("--payload", default="")
    a.add_argument("--risk-level", choices=["low", "medium", "high"], default="medium")
    a.set_defaults(func=cmd_add)

    l = sub.add_parser("list")
    l.add_argument("--status", choices=["pending", "approved", "rejected", "executed", "all"], default="pending")
    l.add_argument("--limit", type=int, default=50)
    l.set_defaults(func=cmd_list)

    ap = sub.add_parser("approve")
    ap.add_argument("--id", type=int, required=True)
    ap.add_argument("--note", required=True)
    ap.set_defaults(func=lambda args: cmd_set_status(args, "approved"))

    r = sub.add_parser("reject")
    r.add_argument("--id", type=int, required=True)
    r.add_argument("--note", required=True)
    r.set_defaults(func=lambda args: cmd_set_status(args, "rejected"))

    d = sub.add_parser("dashboard")
    d.add_argument("--output", default="")
    d.set_defaults(func=cmd_dashboard)

    args = p.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
