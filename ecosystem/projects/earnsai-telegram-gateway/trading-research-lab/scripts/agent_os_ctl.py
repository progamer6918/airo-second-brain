#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
MEMORY = ROOT / "memory"

sys.path.insert(0, str(ROOT))


def ts() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def make_targets() -> set[str]:
    mf = ROOT / "Makefile"
    if not mf.exists():
        return set()
    return set(re.findall(r"^([a-zA-Z0-9_.-]+):(?:\s|$)", mf.read_text(errors="ignore"), flags=re.M))


def count_files(pattern: str) -> int:
    return len(list(ROOT.glob(pattern)))


def latest_reports(limit: int = 12) -> list[str]:
    if not REPORTS.exists():
        return []
    return [str(p) for p in sorted(REPORTS.glob("*"))[-limit:] if p.is_file()]


def write_report(name: str, data: dict) -> Path:
    REPORTS.mkdir(exist_ok=True)
    stamp = ts()
    json_path = REPORTS / f"{name}_{stamp}.json"
    md_path = REPORTS / f"{name}_{stamp}.md"

    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [f"# {name} {stamp}", ""]
    lines.append(f"Overall: **{data.get('overall', 'DONE')}**")
    lines.append("")
    if "readiness" in data:
        lines.append("## Readiness")
        for item in data["readiness"]:
            lines.append(f"- {item['status']}: {item['name']} — {item['note']}")
        lines.append("")
    if "architecture" in data:
        lines.append("## Architecture")
        for k, v in data["architecture"].items():
            lines.append(f"- **{k}**: {v}")
        lines.append("")
    if "commands" in data:
        lines.append("## Commands")
        for cmd in data["commands"]:
            lines.append(f"- `{cmd}`")
        lines.append("")
    if "next_steps" in data:
        lines.append("## Next Steps")
        for step in data["next_steps"]:
            lines.append(f"- {step}")
        lines.append("")
    if "results" in data:
        lines.append("## Results")
        for r in data["results"]:
            lines.append(f"- {r['status']}: {r['agent']} — {r['output']}")
        lines.append("")
    if "files" in data:
        lines.append("## Files")
        for f in data["files"]:
            lines.append(f"- `{f}`")

    md_path.write_text("\n".join(lines), encoding="utf-8")
    return md_path


def plan() -> dict:
    targets = make_targets()
    readiness = [
        {
            "name": "Phase 4 command layer",
            "status": "PASS" if "phase4" in targets else "FAIL",
            "note": "`make phase4` exists and should remain source-of-truth validation.",
        },
        {
            "name": "Agent OS scaffold",
            "status": "PASS" if (ROOT / "agent_os" / "orchestrator.py").exists() else "FAIL",
            "note": "Sequential orchestrator scaffold available.",
        },
        {
            "name": "Shared memory",
            "status": "PASS" if MEMORY.exists() else "WARN",
            "note": "JSONL memory prepared; SQLite can be added later if needed.",
        },
        {
            "name": "Notion integration",
            "status": "DRY_RUN",
            "note": "Dry-run adapter only; no real Notion token/API call yet.",
        },
        {
            "name": "Cloud LLM provider",
            "status": "PLANNED",
            "note": "Use provider API later; no local AI model required.",
        },
        {
            "name": "Multi-agent mode",
            "status": "SEQUENTIAL_READY",
            "note": "Sequential specialist agents first; CrewAI/LangGraph not installed yet.",
        },
    ]

    overall = "PASS" if all(x["status"] in {"PASS", "DRY_RUN", "PLANNED", "SEQUENTIAL_READY"} for x in readiness) else "WARN"

    return {
        "overall": overall,
        "architecture": {
            "ecosystem": "Single EarnsAI ecosystem",
            "orchestrator": "EarnsAIOrchestrator",
            "agents": "ResearchAgent, RiskGuardianAgent, ReportAgent, NotionLibrarianAgent",
            "memory": "JSONL now; SQLite later",
            "notion": "Dedicated EarnsAI Notion account/workspace; dry-run first",
            "runtime": "Cloud runtime/dev environment friendly",
            "llm": "Cloud LLM provider later; no local model",
            "safety": "Research-only, no live trading, no private exchange API",
        },
        "readiness": readiness,
        "commands": [
            "make phase4",
            "make agent-os-plan",
            "make agent-os-smoke",
            "make notion-dry-run",
        ],
        "files": [
            "agent_os/orchestrator.py",
            "agent_os/guards/policy.py",
            "agent_os/memory/jsonl_store.py",
            "agent_os/notion/dry_run_adapter.py",
            "scripts/agent_os_ctl.py",
        ],
        "next_steps": [
            "Keep `make phase4` as baseline gate.",
            "Review Notion dry-run payload shape.",
            "Add guarded official Notion API adapter only after dry-run is accepted.",
            "Add cloud LLM provider adapter after memory and Notion dry-run are stable.",
            "Evaluate CrewAI/LangGraph only after sequential orchestrator is useful.",
        ],
    }


def smoke() -> dict:
    from agent_os.orchestrator import EarnsAIOrchestrator

    orch = EarnsAIOrchestrator()
    results = orch.run_demo()

    return {
        "overall": "PASS",
        "mode": "SEQUENTIAL_DRY_RUN",
        "live_trading": "DISABLED",
        "private_exchange_api": "DISABLED",
        "results": [
            {
                "agent": r.agent,
                "status": r.status,
                "output": r.output,
            }
            for r in results
        ],
        "next_steps": [
            "Inspect generated notion_dry_run report.",
            "Prepare official Notion API adapter with allowlist and audit log.",
        ],
    }


def notion_dry_run() -> dict:
    from agent_os.notion.dry_run_adapter import NotionDryRunAdapter

    adapter = NotionDryRunAdapter()
    payload = {
        "title": "EarnsAI Phase 4 Research Log",
        "status": "ready_for_guarded_notion_adapter",
        "source": "agent_os_ctl.py",
        "live_trading": "DISABLED",
        "private_exchange_api": "DISABLED",
        "workspace_boundary": "Dedicated EarnsAI Notion workspace only",
    }
    files = adapter.write_research_log(payload)

    return {
        "overall": "PASS",
        "notion_mode": "DRY_RUN_ONLY",
        "real_api_called": False,
        "files": list(files.values()),
        "next_steps": [
            "Confirm Notion database/page schema.",
            "Add .env.example keys without real tokens.",
            "Build official Notion API adapter in guarded mode.",
        ],
    }


def run_phase4_gate() -> bool:
    proc = subprocess.run(
        ["make", "phase4"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=240,
    )
    (ROOT / ".audit").mkdir(exist_ok=True)
    (ROOT / ".audit" / f"agent_os_phase4_gate_{ts()}.log").write_text(proc.stdout, encoding="utf-8")
    return proc.returncode == 0


def main() -> None:
    parser = argparse.ArgumentParser(description="EarnsAI Agent OS control")
    parser.add_argument("command", choices=["plan", "smoke", "notion-dry-run"])
    parser.add_argument("--skip-phase4-gate", action="store_true")
    args = parser.parse_args()

    if not args.skip_phase4_gate:
        ok = run_phase4_gate()
        if not ok:
            print("Phase4 gate failed. Run `make phase4` and inspect latest report.")
            raise SystemExit(1)

    if args.command == "plan":
        data = plan()
        report = write_report("agent_os_plan", data)
    elif args.command == "smoke":
        data = smoke()
        report = write_report("agent_os_smoke", data)
    elif args.command == "notion-dry-run":
        data = notion_dry_run()
        report = write_report("agent_os_notion_dry_run", data)
    else:
        raise SystemExit("Unknown command")

    print(f"EarnsAI Agent OS: {args.command}")
    print(f"Overall: {data.get('overall')}")
    print(f"Report: {report}")


if __name__ == "__main__":
    main()
