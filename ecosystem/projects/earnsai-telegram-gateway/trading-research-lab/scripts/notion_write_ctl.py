#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = ROOT / ".env"
REPORTS = ROOT / "reports"


def ts() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def load_env() -> dict[str, str]:
    values: dict[str, str] = {}
    if ENV_FILE.exists():
        for raw in ENV_FILE.read_text(errors="ignore").splitlines():
            line = raw.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                values[k.strip()] = v.strip().strip("'").strip('"')
    return values


def notion_request(method: str, path: str, token: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.notion.com/v1{path}",
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        },
        method=method,
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def extract_title(page: dict[str, Any]) -> str:
    for prop in page.get("properties", {}).values():
        if prop.get("type") == "title":
            return "".join(x.get("plain_text", "") for x in prop.get("title", [])).strip()
    return "<title_not_found>"


def write_report(name: str, data: dict[str, Any]) -> Path:
    REPORTS.mkdir(exist_ok=True)
    stamp = ts()
    json_path = REPORTS / f"{name}_{stamp}.json"
    md_path = REPORTS / f"{name}_{stamp}.md"

    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

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

    md_path.write_text("\n".join(lines), encoding="utf-8")
    return md_path


def guarded_append_once(approved_once: bool) -> dict[str, Any]:
    env = load_env()
    token = env.get("NOTION_TOKEN", "")
    page_id = env.get("NOTION_ROOT_PAGE_ID", "")
    write_mode = env.get("NOTION_WRITE_MODE", "DRY_RUN_ONLY") or "DRY_RUN_ONLY"

    base_safety = {
        "values_printed": False,
        "real_write_called": False,
        "approval_required": True,
        "approved_once_flag": approved_once,
        "notion_write_mode": write_mode,
        "delete_allowed": False,
        "bulk_update_allowed": False,
        "share_or_invite_allowed": False,
        "workspace_settings_allowed": False,
        "live_trading": "DISABLED",
        "private_exchange_api": "DISABLED",
    }

    if not approved_once:
        return {
            "overall": "FAIL",
            "safety": base_safety,
            "result": {"status": "BLOCKED", "reason": "missing --approved-once"},
            "next_steps": ["Run only after explicit user approval."],
        }

    if not token or not page_id:
        return {
            "overall": "FAIL",
            "safety": base_safety,
            "result": {"status": "BLOCKED", "reason": "missing NOTION_TOKEN or NOTION_ROOT_PAGE_ID"},
            "next_steps": ["Fill `.env` locally and rerun preflight."],
        }

    try:
        page = notion_request("GET", f"/pages/{page_id.replace('-', '')}", token)
        title = extract_title(page)

        if "Mission Control" not in title:
            return {
                "overall": "FAIL",
                "safety": base_safety,
                "result": {
                    "status": "BLOCKED",
                    "reason": "root page title did not match Mission Control boundary",
                    "page_title": title,
                },
                "next_steps": ["Check NOTION_ROOT_PAGE_ID before attempting any write."],
            }

        now = datetime.now().isoformat(timespec="seconds")
        payload = {
            "children": [
                {
                    "object": "block",
                    "type": "callout",
                    "callout": {
                        "icon": {"type": "emoji", "emoji": "✅"},
                        "color": "green_background",
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": (
                                        "EarnsAI Agent OS connected successfully. "
                                        "Mode: Phase 4 Research Only. "
                                        "Live trading: DISABLED. "
                                        "Private exchange API: DISABLED. "
                                        f"Timestamp: {now}."
                                    )
                                },
                            }
                        ],
                    },
                }
            ]
        }

        response = notion_request("PATCH", f"/blocks/{page_id.replace('-', '')}/children", token, payload)
        base_safety["real_write_called"] = True

        return {
            "overall": "PASS",
            "safety": base_safety,
            "result": {
                "status": "PASS",
                "operation": "append_block_children",
                "target_page_title": title,
                "blocks_appended": len(response.get("results", [])),
                "notion_object": response.get("object"),
            },
            "next_steps": [
                "Open Mission Control Dashboard and confirm the EarnsAI callout appeared.",
                "Keep full database writes disabled until schema mapping is intentionally enabled.",
            ],
        }

    except urllib.error.HTTPError as e:
        return {
            "overall": "FAIL",
            "safety": base_safety,
            "result": {"status": "FAIL", "reason": f"HTTP {e.code}"},
            "next_steps": ["Check Notion token, root page ID, and connection permission."],
        }
    except Exception as e:
        return {
            "overall": "FAIL",
            "safety": base_safety,
            "result": {"status": "FAIL", "reason": type(e).__name__},
            "next_steps": ["Inspect report and retry only after diagnosis."],
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="EarnsAI guarded Notion write control")
    parser.add_argument("command", choices=["append-once"])
    parser.add_argument("--approved-once", action="store_true")
    args = parser.parse_args()

    data = guarded_append_once(args.approved_once)
    report = write_report("notion_guarded_append", data)

    print(f"EarnsAI Notion Write: {args.command}")
    print(f"Overall: {data.get('overall')}")
    print(f"Report: {report}")

    result = data.get("result", {})
    print(f"Status: {result.get('status')}")
    if result.get("target_page_title"):
        print(f"Target page: {result.get('target_page_title')}")
    if result.get("blocks_appended") is not None:
        print(f"Blocks appended: {result.get('blocks_appended')}")
    if result.get("reason"):
        print(f"Reason: {result.get('reason')}")


if __name__ == "__main__":
    main()
