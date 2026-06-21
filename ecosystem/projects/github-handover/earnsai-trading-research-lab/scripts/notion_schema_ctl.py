#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
SCHEMA_JSON = ROOT / "agent_os" / "notion" / "schema.json"

sys.path.insert(0, str(ROOT))


def ts() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def write_report(name: str, data: dict) -> Path:
    REPORTS.mkdir(exist_ok=True)
    stamp = ts()
    json_path = REPORTS / f"{name}_{stamp}.json"
    md_path = REPORTS / f"{name}_{stamp}.md"

    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [f"# {name} {stamp}", ""]
    lines.append(f"Overall: **{data.get('overall', 'DONE')}**")
    lines.append("")
    for section in ("summary", "databases", "guard", "next_steps"):
        if section not in data:
            continue
        lines.append(f"## {section.replace('_', ' ').title()}")
        value = data[section]
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    label = item.get("name") or item.get("operation") or item.get("key") or "item"
                    note = item.get("purpose") or item.get("status") or item.get("note") or ""
                    lines.append(f"- **{label}**: {note}")
                else:
                    lines.append(f"- {item}")
        elif isinstance(value, dict):
            for k, v in value.items():
                lines.append(f"- **{k}**: {v}")
        else:
            lines.append(str(value))
        lines.append("")

    md_path.write_text("\n".join(lines), encoding="utf-8")
    return md_path


def load_schema() -> dict:
    if not SCHEMA_JSON.exists():
        raise SystemExit("Schema JSON not found.")
    return json.loads(SCHEMA_JSON.read_text(encoding="utf-8"))


def schema_report() -> dict:
    schema = load_schema()
    return {
        "overall": "PASS",
        "summary": {
            "mode": schema.get("mode"),
            "workspace_boundary": schema.get("workspace_boundary"),
            "database_count": len(schema.get("databases", [])),
            "blocked_operations_count": len(schema.get("blocked_operations", [])),
        },
        "databases": schema.get("databases", []),
        "guard": {
            "real_api_called": False,
            "token_read": False,
            "destructive_actions": False,
            "status": "Schema blueprint ready for review.",
        },
        "next_steps": [
            "Create matching databases/pages in dedicated EarnsAI Notion workspace.",
            "Collect root page/database IDs manually without exposing tokens.",
            "Add IDs to .env locally only, never paste values to chat.",
            "Switch adapter from DRY_RUN_ONLY to guarded official API only after approval.",
        ],
    }


def guard_check() -> dict:
    from agent_os.notion.guarded_api_adapter import GuardedNotionAdapter, NotionGuardConfig

    adapter = GuardedNotionAdapter(NotionGuardConfig())
    env_status = adapter.env_status()
    plan = adapter.build_research_log_plan(
        "EarnsAI Guard Check",
        {
            "phase": "Phase 4",
            "mode": "dry_run",
            "live_trading": "DISABLED",
            "private_exchange_api": "DISABLED",
        },
    )

    return {
        "overall": "PASS",
        "summary": {
            "guard_mode": adapter.config.mode,
            "real_api_called": False,
            "values_printed": False,
        },
        "guard": {
            "present_env_keys": ", ".join(env_status["present_keys"]) if env_status["present_keys"] else "none",
            "missing_env_keys": ", ".join(env_status["missing_keys"]) if env_status["missing_keys"] else "none",
            "plan_dry_run": plan["dry_run"],
            "target_boundary": plan["target_boundary"],
        },
        "next_steps": [
            "Keep DRY_RUN_ONLY until Notion schema is accepted.",
            "Do not paste NOTION_TOKEN or page IDs into chat.",
            "Use .env locally when real guarded write is added later.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="EarnsAI Notion schema control")
    parser.add_argument("command", choices=["schema", "guard-check"])
    args = parser.parse_args()

    if args.command == "schema":
        data = schema_report()
        report = write_report("notion_schema", data)
    elif args.command == "guard-check":
        data = guard_check()
        report = write_report("notion_guard_check", data)
    else:
        raise SystemExit("Unknown command")

    print(f"EarnsAI Notion: {args.command}")
    print(f"Overall: {data.get('overall')}")
    print(f"Report: {report}")


if __name__ == "__main__":
    main()
