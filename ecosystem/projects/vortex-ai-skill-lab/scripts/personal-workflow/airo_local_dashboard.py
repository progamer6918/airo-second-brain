#!/usr/bin/env python3
import argparse, datetime, html, json, os, sqlite3
from pathlib import Path

DEFAULT_ROOT = Path.home() / ".local/share/airo-personal-workflow"

def now():
    return datetime.datetime.now().isoformat(timespec="seconds")

def emit(obj, code=0):
    print(json.dumps(obj, indent=2, ensure_ascii=False))
    raise SystemExit(code)

def read_queue(root, limit=50):
    db = root / "approval_queue.sqlite"
    if not db.exists():
        return {"exists": False, "db": str(db), "items": [], "counts": {}}
    con = sqlite3.connect(str(db))
    con.row_factory = sqlite3.Row
    rows = con.execute("select * from approval_queue order by id desc limit ?", (limit,)).fetchall()
    con.close()
    items = []
    counts = {}
    for r in rows:
        d = dict(r)
        counts[d.get("status", "unknown")] = counts.get(d.get("status", "unknown"), 0) + 1
        try:
            d["payload"] = json.loads(d.pop("payload_json") or "{}")
        except Exception:
            d["payload"] = {}
        items.append(d)
    return {"exists": True, "db": str(db), "items": items, "counts": counts}

def read_receipts(root, limit=30):
    db = root / "receipts" / "manifest.sqlite"
    if not db.exists():
        return {"exists": False, "db": str(db), "items": [], "count": 0}
    con = sqlite3.connect(str(db))
    con.row_factory = sqlite3.Row
    rows = con.execute("select id, created_at, original_name, sha256, size_bytes, kind, mime, source, status, note from receipt_attachments order by id desc limit ?", (limit,)).fetchall()
    con.close()
    return {"exists": True, "db": str(db), "items": [dict(r) for r in rows], "count": len(rows)}

def badge(text):
    return f"<span class='badge'>{html.escape(str(text))}</span>"

def render_queue(items):
    if not items:
        return "<p class='muted'>No approval queue items found.</p>"
    cards = []
    for item in items:
        payload = item.get("payload", {})
        preview = json.dumps(payload, indent=2, ensure_ascii=False)
        cards.append(
            "<article class='card'>"
            f"<div class='row'><h3>#{item.get('id')} {html.escape(item.get('title',''))}</h3>{badge(item.get('status'))}{badge(item.get('risk_level'))}</div>"
            f"<p><b>Type:</b> {html.escape(item.get('action_type',''))} &nbsp; <b>Source:</b> {html.escape(item.get('source',''))}</p>"
            f"<p><b>Created:</b> {html.escape(item.get('created_at',''))} &nbsp; <b>Updated:</b> {html.escape(item.get('updated_at',''))}</p>"
            f"<pre>{html.escape(preview[:4000])}</pre>"
            f"<p class='muted'>{html.escape(item.get('approval_note') or '')}</p>"
            "</article>"
        )
    return "\n".join(cards)

def render_receipts(items):
    if not items:
        return "<p class='muted'>No receipt attachments found.</p>"
    rows = []
    for item in items:
        rows.append(
            "<tr>"
            f"<td>{html.escape(str(item.get('id','')))}</td>"
            f"<td>{html.escape(item.get('created_at',''))}</td>"
            f"<td>{html.escape(item.get('original_name',''))}</td>"
            f"<td>{html.escape(item.get('kind',''))}</td>"
            f"<td>{html.escape(str(item.get('size_bytes','')))}</td>"
            f"<td><code>{html.escape(str(item.get('sha256',''))[:16])}</code></td>"
            f"<td>{html.escape(item.get('status',''))}</td>"
            "</tr>"
        )
    return "<table><thead><tr><th>ID</th><th>Created</th><th>Name</th><th>Kind</th><th>Bytes</th><th>SHA256</th><th>Status</th></tr></thead><tbody>" + "\n".join(rows) + "</tbody></table>"

def main():
    p = argparse.ArgumentParser(description="Airo local dashboard generator")
    p.add_argument("--root", default=str(DEFAULT_ROOT))
    p.add_argument("--output", default="")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    root = Path(args.root).expanduser().resolve()
    out_dir = Path(args.output).expanduser().resolve() if args.output else root / "dashboard"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "index.html"

    queue = read_queue(root)
    receipts = read_receipts(root)

    summary = {
        "generated": now(),
        "root": str(root),
        "dashboard": str(out_file),
        "approval_queue_exists": queue["exists"],
        "approval_counts": queue["counts"],
        "receipt_manifest_exists": receipts["exists"],
        "receipt_count_shown": receipts["count"],
        "safety": "local_dashboard_only_no_execution"
    }

    if args.json:
        emit({"ok": True, "operation": "dashboard_summary", **summary})

    page = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Airo Personal Workflow Dashboard</title>
<style>
body {{ margin: 0; font-family: system-ui, -apple-system, Segoe UI, sans-serif; background: #f5f6f8; color: #111827; }}
header {{ padding: 28px 36px; background: #111827; color: white; }}
main {{ padding: 28px 36px; max-width: 1200px; margin: auto; }}
h1, h2, h3 {{ margin: 0 0 12px; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin: 20px 0; }}
.metric {{ background: white; border: 1px solid #e5e7eb; border-radius: 14px; padding: 18px; box-shadow: 0 1px 2px rgba(0,0,0,.04); }}
.metric b {{ font-size: 28px; display: block; margin-top: 6px; }}
.section {{ margin-top: 30px; }}
.card {{ background: white; border: 1px solid #e5e7eb; border-radius: 14px; padding: 18px; margin: 14px 0; box-shadow: 0 1px 2px rgba(0,0,0,.04); }}
.row {{ display: flex; gap: 10px; align-items: center; justify-content: space-between; flex-wrap: wrap; }}
.badge {{ display: inline-block; padding: 4px 10px; background: #eef2ff; border: 1px solid #c7d2fe; border-radius: 999px; font-size: 12px; margin-left: 6px; }}
pre {{ white-space: pre-wrap; background: #f3f4f6; padding: 12px; border-radius: 10px; overflow: auto; }}
table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 14px; overflow: hidden; }}
th, td {{ text-align: left; padding: 10px; border-bottom: 1px solid #e5e7eb; font-size: 14px; }}
th {{ background: #f9fafb; }}
.muted {{ color: #6b7280; }}
code {{ background: #f3f4f6; padding: 2px 5px; border-radius: 5px; }}
</style>
</head>
<body>
<header>
<h1>Airo Personal Workflow Dashboard</h1>
<p>Generated {html.escape(summary["generated"])}. Local-only dashboard. No action is executed from this page.</p>
</header>
<main>
<section class="grid">
<div class="metric">Pending approvals<b>{queue["counts"].get("pending", 0)}</b></div>
<div class="metric">Approved items<b>{queue["counts"].get("approved", 0)}</b></div>
<div class="metric">Rejected items<b>{queue["counts"].get("rejected", 0)}</b></div>
<div class="metric">Receipts shown<b>{receipts["count"]}</b></div>
</section>

<section class="section">
<h2>Approval Queue</h2>
<p class="muted">DB: {html.escape(queue["db"])}</p>
{render_queue(queue["items"])}
</section>

<section class="section">
<h2>Receipt Attachments</h2>
<p class="muted">Manifest: {html.escape(receipts["db"])}</p>
{render_receipts(receipts["items"])}
</section>

<section class="section">
<h2>Safety Boundary</h2>
<div class="card">
<p>This dashboard is read-only. It does not execute Google writes, mutate SQLite finance records, patch OpenClaw, restart services, access browser profiles, or touch EarnsAI trading runtime.</p>
</div>
</section>
</main>
</body>
</html>
"""
    out_file.write_text(page, encoding="utf-8")
    emit({"ok": True, "operation": "dashboard_generate", **summary})

if __name__ == "__main__":
    main()
