#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
ENV_FILE = ROOT / ".env"

MINIMAL_REQUIRED_KEYS = [
    "NOTION_TOKEN",
    "NOTION_ROOT_PAGE_ID",
    "NOTION_WRITE_MODE",
]

OPTIONAL_DB_KEYS = [
    "NOTION_RESEARCH_JOURNAL_DB_ID",
    "NOTION_STRATEGY_REGISTRY_DB_ID",
    "NOTION_BACKTEST_LOGS_DB_ID",
    "NOTION_DECISION_JOURNAL_DB_ID",
    "NOTION_RISK_FLAGS_DB_ID",
    "NOTION_AGENT_ACTIVITY_LOG_DB_ID",
]

def ts() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")

def load_env() -> dict[str, str]:
    values = {}
    if ENV_FILE.exists():
        for raw in ENV_FILE.read_text(errors="ignore").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            values[k.strip()] = v.strip().strip("'").strip('"')
    for k, v in os.environ.items():
        if k.startswith("NOTION_"):
            values.setdefault(k, v)
    return values

def masked(value: str | None) -> dict:
    if not value:
        return {"present": False, "length": 0, "preview": None}
    return {"present": True, "length": len(value), "preview": "<SET_NOT_PRINTED>"}

def write_report(name: str, data: dict) -> Path:
    REPORTS.mkdir(exist_ok=True)
    stamp = ts()
    jp = REPORTS / f"{name}_{stamp}.json"
    mp = REPORTS / f"{name}_{stamp}.md"
    jp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [f"# {name} {stamp}", "", f"Overall: **{data['overall']}**", ""]
    lines.append("## Mode")
    lines.append(f"- **config_mode**: {data['config_mode']}")
    lines.append(f"- **canonical_file**: .env")
    lines.append(f"- **values_printed**: False")
    lines.append("")
    lines.append("## Minimal Required Keys")
    for row in data["minimal_keys"]:
        status = "SET" if row["present"] else "MISSING"
        lines.append(f"- {status}: `{row['key']}` length={row['length']} value={row['preview']}")
    lines.append("")
    lines.append("## Optional Database IDs")
    for row in data["optional_keys"]:
        status = "SET" if row["present"] else "blank"
        lines.append(f"- {status}: `{row['key']}`")
    lines.append("")
    lines.append("## Next Steps")
    for step in data["next_steps"]:
        lines.append(f"- {step}")

    mp.write_text("\n".join(lines), encoding="utf-8")
    return mp

def env_check() -> dict:
    values = load_env()

    minimal_rows = []
    missing = []
    for key in MINIMAL_REQUIRED_KEYS:
        row = {"key": key, **masked(values.get(key))}
        minimal_rows.append(row)
        if not row["present"]:
            missing.append(key)

    optional_rows = []
    for key in OPTIONAL_DB_KEYS:
        optional_rows.append({"key": key, **masked(values.get(key))})

    write_mode = values.get("NOTION_WRITE_MODE", "DRY_RUN_ONLY") or "DRY_RUN_ONLY"
    unsafe_mode = write_mode not in {"DRY_RUN_ONLY", "GUARDED_WRITE"}

    overall = "PASS" if not missing and not unsafe_mode else "WARN"

    return {
        "overall": overall,
        "config_mode": "MINIMAL_ROOT_PAGE_MODE",
        "missing_keys": missing,
        "notion_write_mode": write_mode,
        "minimal_keys": minimal_rows,
        "optional_keys": optional_rows,
        "next_steps": [
            "For current minimal mode, only NOTION_TOKEN, NOTION_ROOT_PAGE_ID, and NOTION_WRITE_MODE are required.",
            "Optional database IDs can stay blank until full Notion database mode is needed.",
            "Never paste NOTION_TOKEN or page/database IDs into chat.",
            "Keep NOTION_WRITE_MODE=DRY_RUN_ONLY until guarded write is explicitly enabled.",
        ],
    }

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["env-check", "id-map", "preflight"])
    args = parser.parse_args()

    data = env_check()
    report = write_report("notion_env_check", data)

    print(f"EarnsAI Notion Env: {args.command}")
    print(f"Overall: {data['overall']}")
    print(f"Config mode: {data['config_mode']}")
    print(f"Missing minimal keys: {len(data['missing_keys'])}")
    print(f"Optional DB IDs set: {sum(1 for r in data['optional_keys'] if r['present'])}")
    print(f"Report: {report}")

if __name__ == "__main__":
    main()
