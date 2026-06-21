#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
ENV_FILE = ROOT / ".env"

def ts():
    return datetime.now().strftime("%Y%m%d-%H%M%S")

def load_env():
    values = {}
    if ENV_FILE.exists():
        for raw in ENV_FILE.read_text(errors="ignore").splitlines():
            line = raw.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                values[k.strip()] = v.strip().strip("'").strip('"')
    return values

def write_report(name, data):
    REPORTS.mkdir(exist_ok=True)
    stamp = ts()
    jp = REPORTS / f"{name}_{stamp}.json"
    mp = REPORTS / f"{name}_{stamp}.md"
    jp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    lines = [f"# {name} {stamp}", "", f"Overall: **{data.get('overall')}**", ""]
    lines.append("## Safety")
    for k, v in data.get("safety", {}).items():
        lines.append(f"- **{k}**: {v}")
    lines.append("")
    lines.append("## Result")
    for k, v in data.get("result", {}).items():
        lines.append(f"- **{k}**: {v}")
    lines.append("")
    lines.append("## Next Steps")
    for step in data.get("next_steps", []):
        lines.append(f"- {step}")
    mp.write_text("\n".join(lines), encoding="utf-8")
    return mp

def notion_get_page(token, page_id):
    req = urllib.request.Request(
        f"https://api.notion.com/v1/pages/{page_id.replace('-', '')}",
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        },
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))

def title_from_page(page):
    for prop in page.get("properties", {}).values():
        if prop.get("type") == "title":
            return "".join(x.get("plain_text", "") for x in prop.get("title", [])).strip()
    return "<title_not_found>"

def read_check():
    env = load_env()
    token = env.get("NOTION_TOKEN", "")
    page_id = env.get("NOTION_ROOT_PAGE_ID", "")
    write_mode = env.get("NOTION_WRITE_MODE", "DRY_RUN_ONLY") or "DRY_RUN_ONLY"

    base = {
        "safety": {
            "values_printed": False,
            "real_write_called": False,
            "notion_write_mode": write_mode,
        }
    }

    if not token or not page_id:
        return {
            "overall": "WARN",
            **base,
            "result": {"status": "SKIPPED", "reason": "missing NOTION_TOKEN or NOTION_ROOT_PAGE_ID"},
            "next_steps": ["Fill `.env`, then run `make notion-read-check` again."],
        }

    try:
        page = notion_get_page(token, page_id)
        return {
            "overall": "PASS",
            **base,
            "result": {
                "status": "PASS",
                "token_present": True,
                "root_page_id_present": True,
                "page_title": title_from_page(page),
            },
            "next_steps": ["Run `make notion-append-dry-run`.", "Guarded write still requires explicit approval."],
        }
    except urllib.error.HTTPError as e:
        return {
            "overall": "FAIL",
            **base,
            "result": {"status": "FAIL", "reason": f"HTTP {e.code}"},
            "next_steps": ["Check token, root page ID, and Notion connection permission."],
        }

def append_dry_run():
    env = load_env()
    return {
        "overall": "PASS",
        "safety": {
            "values_printed": False,
            "real_write_called": False,
            "notion_write_mode": env.get("NOTION_WRITE_MODE", "DRY_RUN_ONLY"),
            "delete_allowed": False,
            "bulk_update_allowed": False,
        },
        "result": {
            "status": "PASS",
            "dry_run": True,
            "operation": "append_block_children",
            "target": "🚀 Mission Control Dashboard",
            "preview": "EarnsAI Agent OS dry-run log. No real Notion write performed.",
        },
        "next_steps": ["Next step is guarded append-write, only after explicit approval."],
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["read-check", "append-dry-run"])
    args = parser.parse_args()

    data = read_check() if args.command == "read-check" else append_dry_run()
    report = write_report("notion_" + args.command.replace("-", "_"), data)

    print(f"EarnsAI Notion Minimal: {args.command}")
    print(f"Overall: {data.get('overall')}")
    print(f"Report: {report}")
    result = data.get("result", {})
    if result.get("page_title"):
        print("Page title:", result["page_title"])
    if result.get("reason"):
        print("Reason:", result["reason"])

if __name__ == "__main__":
    main()
