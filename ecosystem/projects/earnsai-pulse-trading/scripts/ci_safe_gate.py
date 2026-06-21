#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class GateResult:
    name: str
    command: str
    ok: bool
    output_tail: str


GATES = [
    ("security_scan", "python3 scripts/security_scan.py"),
    ("doctor", "python3 scripts/doctor.py"),
    ("phase7_full_gate", "make phase7-full-gate"),
    ("phase8_full_gate", "make phase8-full-gate"),
    ("phase9a_gate", "make phase9a-gate"),
    ("phase9b_gate", "make phase9b-gate"),
    ("phase9c_gate", "make phase9c-gate"),
    ("compact_report", "make compact-report"),
]


def run_command(command: str) -> tuple[bool, str]:
    completed = subprocess.run(
        command,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return completed.returncode == 0, completed.stdout


def tail(text: str, lines: int = 20) -> str:
    parts = text.strip().splitlines()
    return "\n".join(parts[-lines:])


def run_ci_safe_gate() -> dict:
    results: list[GateResult] = []

    for name, command in GATES:
        ok, output = run_command(command)
        results.append(
            GateResult(
                name=name,
                command=command,
                ok=ok,
                output_tail=tail(output),
            )
        )

        if not ok:
            break

    all_ok = all(item.ok for item in results)

    report_path = Path("reports/phase9d_ci_safe_gate_report.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# EarnsAI Pulse — Phase 9D CI Safe Gate Report",
        "",
        f"- Generated at: `{datetime.now(timezone.utc).isoformat()}`",
        f"- Overall OK: `{all_ok}`",
        "",
        "## Gate Results",
        "",
        "| Gate | Command | OK |",
        "|---|---|---|",
    ]

    for item in results:
        lines.append(f"| {item.name} | `{item.command}` | `{item.ok}` |")

    lines.extend(["", "## Output Tails", ""])

    for item in results:
        lines.append(f"### {item.name}")
        lines.append("")
        lines.append("```text")
        lines.append(item.output_tail)
        lines.append("```")
        lines.append("")

    lines.extend(
        [
            "## Safety",
            "- CI safe gate does not enable live trading.",
            "- CI safe gate does not use private exchange API.",
            "- CI safe gate validates paper/dry-run safety posture.",
            "- CI safe gate is local-only.",
        ]
    )

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return {
        "ok": all_ok,
        "report_path": str(report_path),
        "results": [
            {
                "name": item.name,
                "command": item.command,
                "ok": item.ok,
            }
            for item in results
        ],
    }


def main() -> int:
    result = run_ci_safe_gate()

    print(
        "CI_SAFE_GATE "
        f"ok={result['ok']} "
        f"report={result['report_path']} "
        f"gates={len(result['results'])}"
    )

    for item in result["results"]:
        print(f"- {item['name']}: {item['ok']}")

    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
