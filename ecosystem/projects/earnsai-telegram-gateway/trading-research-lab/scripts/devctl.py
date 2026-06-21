#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
AUDIT = ROOT / ".audit"

REDACT_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|api[_-]?secret|secret|token|password)\s*[:=]\s*['\"]?[^'\"\s]+"),
    re.compile(r"(?i)(BYBIT_API_SECRET|BYBIT_API_KEY|OPENAI_API_KEY|GEMINI_API_KEY|GROQ_API_KEY|NOTION_TOKEN)\s*=\s*.+"),
]

DANGER_PATTERNS = [
    "create_order",
    "market_order",
    "limit_order",
    "withdraw",
    "api_secret",
    "apiSecret",
    "leverage",
    "private api",
    "BYBIT_API_SECRET",
    "BYBIT_API_KEY",
]

EXCLUDE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".dev-archives",
    ".audit",
    "reports",
}

def ts() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")

def redact(s: str) -> str:
    for pat in REDACT_PATTERNS:
        s = pat.sub(lambda m: m.group(0).split("=")[0] + "=<REDACTED>" if "=" in m.group(0) else "<REDACTED>", s)
    return s

def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except Exception:
        return str(p)

def make_targets() -> set[str]:
    mf = ROOT / "Makefile"
    if not mf.exists():
        return set()
    text = mf.read_text(errors="ignore")
    return set(re.findall(r"^([a-zA-Z0-9_.-]+):(?:\s|$)", text, flags=re.M))

def run_make(target: str, timeout: int = 120) -> dict:
    log_path = AUDIT / f"make_{target}_{ts()}.log"
    result = {
        "target": target,
        "status": "SKIP",
        "returncode": None,
        "log": rel(log_path),
    }

    targets = make_targets()
    if target not in targets:
        result["reason"] = "target_missing"
        return result

    proc = subprocess.run(
        ["make", target],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
    )
    output = redact(proc.stdout or "")
    log_path.write_text(output, encoding="utf-8")
    result["returncode"] = proc.returncode
    result["status"] = "PASS" if proc.returncode == 0 else "FAIL"
    result["tail"] = "\n".join(output.splitlines()[-20:])
    return result

def iter_text_files():
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        if p.name.startswith(".env"):
            continue
        if rel(p) in {"scripts/devctl.py", "AGENTS.md", "test_langsung.py", "check_balance.py"}:
            continue
        if p.suffix.lower() not in {".py", ".md", ".txt", ".json", ".yml", ".yaml", ".sh", ".toml", ".cfg", ".ini"} and p.name != "Makefile":
            continue
        try:
            if p.stat().st_size > 700_000:
                continue
        except OSError:
            continue
        yield p

def security_scan() -> dict:
    """
    Security scanner v3.

    Purpose:
    - FAIL/WARN only for active runtime files that can execute private exchange/live trading paths.
    - Ignore historical checkpoints, archives, reports, docs, schemas, and policy guards.
    """
    active_risk_patterns = [
        re.compile(r"(?i)\.create_order\s*\("),
        re.compile(r"(?i)\bcreate_order\s*\("),
        re.compile(r"(?i)\bmarket_order\s*\("),
        re.compile(r"(?i)\blimit_order\s*\("),
        re.compile(r"(?i)\bwithdraw\s*\("),
        re.compile(r"(?i)os\.getenv\(\s*['\"]BYBIT_API_(KEY|SECRET)['\"]"),
        re.compile(r"(?i)\bccxt\.[a-z0-9_]+\s*\("),
        re.compile(r"(?i)\b(api_secret|api_key)\s*=\s*['\"][^'\"]{12,}['\"]"),
        re.compile(r"(?i)['\"]secret['\"]\s*:\s*['\"][^'\"]{12,}['\"]"),
    ]

    ignored_prefixes = (
        ".dev-archives/",
        ".audit/",
        "reports/",
        "checkpoints/",
        "agent_os/docs/",
        "agent_os/notion/schema",
    )

    policy_or_reference_files = {
        "AGENTS.md",
        "README.md",
        ".env.example",
        "agent_os/README.md",
        "agent_os/guards/policy.py",
        "agent_os/orchestrator.py",
        "agent_os/notion/dry_run_adapter.py",
        "agent_os/notion/guarded_api_adapter.py",
        "agent_os/notion/schema.md",
        "agent_os/notion/schema.json",
        "scripts/devctl.py",
        "scripts/agent_os_ctl.py",
        "scripts/notion_schema_ctl.py",
        "test_langsung.py",
        "check_balance.py",
    }

    active_runtime_allowlist = {
        "simple_pulse_bot.py",
        "paper_bot.py",
        "paper_bot_lazy.py",
        "integrated_paper_bot.py",
        "analytics.py",
        "report.py",
        "data/collector.py",
        "backtest/ma_crossover.py",
        "backtest/ma_crossover_rm.py",
        "backtest/optimizer.py",
        "paper-trading/live_checker.py",
        "paper-trading/notifier.py",
    }

    active_hits = []
    ignored_mentions = []

    for p in iter_text_files():
        rpath = rel(p)

        if rpath.startswith(ignored_prefixes):
            continue

        try:
            text = p.read_text(errors="ignore")
        except Exception:
            continue

        is_disabled_stub = "SECURITY DISABLED" in text or "Disabled by EarnsAI Phase 4 safety policy" in text
        is_policy_or_reference = (
            rpath in policy_or_reference_files
            or rpath.startswith("agent_os/guards/")
            or rpath.startswith("agent_os/notion/")
            or rpath.endswith(".md")
            or rpath.endswith(".json")
            or rpath.endswith(".example")
        )

        is_active_runtime = rpath in active_runtime_allowlist

        for i, line in enumerate(text.splitlines(), 1):
            stripped = line.strip()
            if not stripped:
                continue

            matched_active = [pat.pattern for pat in active_risk_patterns if pat.search(stripped)]

            if matched_active:
                if is_active_runtime and not is_disabled_stub and not is_policy_or_reference:
                    active_hits.append({
                        "file": rpath,
                        "line": i,
                        "signal": "active_runtime_risk",
                        "preview": redact(stripped)[:180],
                    })
                else:
                    ignored_mentions.append({
                        "file": rpath,
                        "line": i,
                        "signal": "ignored_reference_or_historical_context",
                        "preview": redact(stripped)[:180],
                    })
                continue

            low = stripped.lower()
            if any(x.lower() in low for x in DANGER_PATTERNS):
                ignored_mentions.append({
                    "file": rpath,
                    "line": i,
                    "signal": "keyword_reference_only",
                    "preview": redact(stripped)[:180],
                })

    return {
        "status": "PASS" if not active_hits else "WARN",
        "hits": active_hits[:80],
        "hit_count": len(active_hits),
        "ignored_mention_count": len(ignored_mentions),
        "ignored_mentions_sample": ignored_mentions[:20],
    }


def project_scan() -> dict:
    py_files = [rel(p) for p in ROOT.rglob("*.py") if not any(part in EXCLUDE_DIRS for part in p.parts)]
    report_files = [rel(p) for p in REPORTS.glob("*") if p.is_file()] if REPORTS.exists() else []
    return {
        "root": str(ROOT),
        "make_targets": sorted(make_targets()),
        "python_file_count": len(py_files),
        "python_files_sample": sorted(py_files)[:80],
        "report_count": len(report_files),
        "latest_reports": sorted(report_files)[-20:],
    }

def doctor() -> dict:
    checks = []

    checks.append({
        "name": "root_has_makefile",
        "status": "PASS" if (ROOT / "Makefile").exists() else "FAIL",
    })

    checks.append({
        "name": "baseline_checkpoint_v319",
        "status": "PASS" if (ROOT / "checkpoints" / "simple_pulse_bot_v3_1_9_sequential_handler_verified.py").exists() else "WARN",
    })

    checks.append({
        "name": "active_bot_exists",
        "status": "PASS" if (ROOT / "simple_pulse_bot.py").exists() else "FAIL",
    })

    checks.append({
        "name": "research_reports_exist",
        "status": "PASS" if REPORTS.exists() and any(REPORTS.glob("research_report_*.md")) else "WARN",
    })

    checks.append({
        "name": "phase4_target_exists",
        "status": "PASS" if "phase4" in make_targets() else "FAIL",
    })

    sec = security_scan()
    checks.append({
        "name": "security_scan_no_private_api_signals",
        "status": sec["status"],
        "hit_count": sec["hit_count"],
    })

    overall = "PASS"
    if any(c["status"] == "FAIL" for c in checks):
        overall = "FAIL"
    elif any(c["status"] == "WARN" for c in checks):
        overall = "WARN"

    return {
        "overall": overall,
        "checks": checks,
        "security": sec,
        "scan": project_scan(),
    }

def write_report(name: str, data: dict) -> Path:
    REPORTS.mkdir(exist_ok=True)
    AUDIT.mkdir(exist_ok=True)
    stamp = ts()
    json_path = REPORTS / f"{name}_{stamp}.json"
    md_path = REPORTS / f"{name}_{stamp}.md"

    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [f"# {name} {stamp}", ""]
    if "overall" in data:
        lines.append(f"Overall: **{data['overall']}**")
        lines.append("")
    if "checks" in data:
        lines.append("## Checks")
        for c in data["checks"]:
            extra = f" — hit_count={c.get('hit_count')}" if "hit_count" in c else ""
            lines.append(f"- {c['status']}: {c['name']}{extra}")
        lines.append("")
    if "commands" in data:
        lines.append("## Command Results")
        for r in data["commands"]:
            lines.append(f"- {r['status']}: make {r['target']} → `{r['log']}`")
        lines.append("")
    if "security" in data:
        sec = data["security"]
        lines.append("## Security Scan")
        lines.append(f"- Status: {sec['status']}")
        lines.append(f"- Hit count: {sec['hit_count']}")
        for h in sec.get("hits", [])[:20]:
            lines.append(f"- {h['file']}:{h['line']} — {h['preview']}")
        lines.append("")
    if "scan" in data:
        scan = data["scan"]
        lines.append("## Project Scan")
        lines.append(f"- Root: `{scan['root']}`")
        lines.append(f"- Python files: {scan['python_file_count']}")
        lines.append(f"- Reports: {scan['report_count']}")
        lines.append("")
        lines.append("### Make Targets")
        for t in scan["make_targets"]:
            lines.append(f"- make {t}")

    md_path.write_text("\n".join(lines), encoding="utf-8")
    return md_path

def phase4() -> dict:
    command_sequence = [
        "verify-v319",
        "phase4-status",
        "lab-health",
        "lab-latest",
        "state-doctor",
    ]

    results = []
    for target in command_sequence:
        try:
            results.append(run_make(target, timeout=180))
        except subprocess.TimeoutExpired:
            results.append({"target": target, "status": "FAIL", "reason": "timeout"})
        except Exception as e:
            results.append({"target": target, "status": "FAIL", "reason": type(e).__name__, "detail": str(e)})

    d = doctor()
    hard_fail = any(r["status"] == "FAIL" for r in results)
    overall = "FAIL" if hard_fail or d["overall"] == "FAIL" else ("WARN" if d["overall"] == "WARN" or any(r["status"] == "SKIP" for r in results) else "PASS")

    return {
        "overall": overall,
        "mode": "PHASE4_RESEARCH_ONLY",
        "live_trading": "DISABLED",
        "private_exchange_api": "DISABLED",
        "commands": results,
        "checks": d["checks"],
        "security": d["security"],
        "scan": d["scan"],
    }

def main():
    parser = argparse.ArgumentParser(description="EarnsAI Dev Command Library")
    parser.add_argument("command", choices=["doctor", "scan", "security", "phase4"])
    args = parser.parse_args()

    if args.command == "doctor":
        data = doctor()
        report = write_report("devctl_doctor", data)
    elif args.command == "scan":
        data = {"scan": project_scan(), "security": security_scan()}
        report = write_report("devctl_scan", data)
    elif args.command == "security":
        data = {"security": security_scan()}
        data["overall"] = data["security"]["status"]
        report = write_report("devctl_security", data)
    elif args.command == "phase4":
        data = phase4()
        report = write_report("devctl_phase4", data)
    else:
        raise SystemExit("Unknown command")

    print(f"EarnsAI devctl: {args.command}")
    print(f"Overall: {data.get('overall', 'DONE')}")
    print(f"Report: {rel(report)}")

    if data.get("overall") == "FAIL":
        print("Action: open the report and paste only the failing section.")
        sys.exit(1)

    if args.command in {"phase4", "doctor", "security"}:
        sec = data.get("security", {})
        if sec.get("hit_count", 0):
            print(f"Security signals: {sec.get('hit_count')} redacted hit(s). Review report.")

if __name__ == "__main__":
    main()
