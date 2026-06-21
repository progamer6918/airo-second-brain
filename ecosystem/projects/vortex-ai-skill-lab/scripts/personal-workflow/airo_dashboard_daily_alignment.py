#!/usr/bin/env python3
import argparse, html, json, subprocess
from pathlib import Path

DEFAULT_ROOT = Path.home() / ".local/share/airo-personal-workflow"

def emit(obj, code=0):
    print(json.dumps(obj, indent=2, ensure_ascii=False))
    raise SystemExit(code)

def run_json(cmd):
    out = subprocess.check_output(cmd, text=True)
    return json.loads(out)

def esc(x):
    return html.escape(str(x if x is not None else ""))

def command_block(label, cmd):
    if not cmd:
        return ""
    return f"<p><b>{esc(label)}:</b></p><pre>{esc(cmd)}</pre>"

def build_section(daily):
    next_actions = daily.get("next_actions", [])
    recommendations = daily.get("recommendations", [])

    action_html = []
    for item in next_actions[:10]:
        action_html.append(
            "<div class='item'>"
            f"<h3>{esc(item.get('label'))}</h3>"
            + command_block("command", item.get("command"))
            + "</div>"
        )

    rec_html = []
    for rec in recommendations[:20]:
        rec_html.append(
            "<div class='item'>"
            f"<h3>Queue #{esc(rec.get('item_id'))}: {esc(rec.get('next_action'))}</h3>"
            + command_block("recommended command", rec.get("command"))
            + "</div>"
        )

    if not action_html:
        action_html.append("<p class='muted'>No daily next actions found.</p>")
    if not rec_html:
        rec_html.append("<p class='muted'>No queue item recommendations found.</p>")

    summary = {
        "pending_count": daily.get("pending_count"),
        "approved_count": daily.get("approved_count"),
        "actionable_count": daily.get("actionable_count"),
        "dashboard": daily.get("dashboard"),
        "google_sync_readiness": daily.get("google_sync_readiness", {}),
    }

    return f"""
<section class="card" id="airo-daily-command-alignment">
<h2>Airo Daily Command Alignment</h2>
<p>This section is generated from <code>./bin/airo-daily</code>, so the dashboard and daily CLI recommend the same next actions.</p>
<div class="grid">
<div class="metric"><span>Pending approvals</span><b>{esc(summary.get("pending_count"))}</b><small>review first</small></div>
<div class="metric"><span>Approved items</span><b>{esc(summary.get("approved_count"))}</b><small>dry-run next</small></div>
<div class="metric"><span>Actionable items</span><b>{esc(summary.get("actionable_count"))}</b><small>pending + approved</small></div>
</div>
<h3>Daily next actions</h3>
{''.join(action_html)}
<h3>Queue item recommendations</h3>
{''.join(rec_html)}
<h3>Daily JSON summary</h3>
<pre>{esc(json.dumps(summary, indent=2, ensure_ascii=False))}</pre>
</section>
"""

def main():
    p = argparse.ArgumentParser(description="Align Airo dashboard with airo-daily recommendations")
    p.add_argument("--root", default=str(DEFAULT_ROOT))
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    root = Path(args.root).expanduser().resolve()
    dashboard = root / "dashboard" / "daily_ops.html"

    subprocess.check_call(["python3", "scripts/personal-workflow/airo_ops_dashboard.py"], stdout=subprocess.DEVNULL)
    daily = run_json(["python3", "scripts/personal-workflow/airo_daily.py", "--root", str(root)])

    if not dashboard.exists():
        emit({"ok": False, "error": "daily ops dashboard not found", "dashboard": str(dashboard)}, 2)

    html_text = dashboard.read_text(encoding="utf-8", errors="ignore")
    section = build_section(daily)

    marker = '<section class="card" id="airo-daily-command-alignment">'
    if marker in html_text:
        start = html_text.index(marker)
        end = html_text.find("</section>", start)
        if end != -1:
            end += len("</section>")
            html_text = html_text[:start] + section + html_text[end:]
        else:
            html_text = html_text + "\n" + section
    elif "</main>" in html_text:
        html_text = html_text.replace("</main>", section + "\n</main>")
    else:
        html_text = html_text + "\n" + section

    dashboard.write_text(html_text, encoding="utf-8")

    result = {
        "ok": True,
        "operation": "dashboard_daily_command_alignment",
        "dashboard": str(dashboard),
        "pending_count": daily.get("pending_count"),
        "approved_count": daily.get("approved_count"),
        "actionable_count": daily.get("actionable_count"),
        "next_action_count": len(daily.get("next_actions", [])),
        "recommendation_count": len(daily.get("recommendations", [])),
        "read_only": True,
        "execution_performed": False,
        "google_write": False,
        "sqlite_mutation": False
    }

    emit(result)

if __name__ == "__main__":
    main()
