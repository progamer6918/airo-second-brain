from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

from earnsai.agents.orchestrator import run_once
from earnsai.data.provider_runner import run_cycle_from_provider
from earnsai.journal.jsonl_store import read_jsonl


DEFAULT_TEST_JOURNAL = Path("runtime/test_journals/phase9b_decisions.jsonl")


def get_test_journal_path(name: str = "phase9b") -> Path:
    safe_name = "".join(ch for ch in name if ch.isalnum() or ch in {"_", "-"}).strip() or "phase9b"
    return Path("runtime/test_journals") / f"{safe_name}_decisions.jsonl"


def reset_journal(path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("", encoding="utf-8")
    return target


@contextmanager
def isolated_journal(path: str | Path = DEFAULT_TEST_JOURNAL) -> Iterator[Path]:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)

    old_value = os.environ.get("EARNSAI_JOURNAL_PATH")
    os.environ["EARNSAI_JOURNAL_PATH"] = str(target)

    try:
        yield target
    finally:
        if old_value is None:
            os.environ.pop("EARNSAI_JOURNAL_PATH", None)
        else:
            os.environ["EARNSAI_JOURNAL_PATH"] = old_value


def count_rows(path: str | Path) -> int:
    return len(read_jsonl(path, limit=0))


def run_isolated_journal_check(path: str | Path = DEFAULT_TEST_JOURNAL) -> dict[str, Any]:
    target = reset_journal(path)

    with isolated_journal(target):
        run_once(action="HOLD", confidence=0.0)
        run_cycle_from_provider(scenario="bullish")
        run_cycle_from_provider(scenario="bearish")
        run_cycle_from_provider(scenario="flat")
        run_cycle_from_provider(scenario="volatile")

    rows = read_jsonl(target, limit=0)

    actions: dict[str, int] = {}
    risks: dict[str, int] = {}

    for row in rows:
        final = row.get("final", {})
        if isinstance(final, dict):
            action = str(final.get("action", "UNKNOWN"))
            risk = str(final.get("risk_status", "UNKNOWN"))
            actions[action] = actions.get(action, 0) + 1
            risks[risk] = risks.get(risk, 0) + 1

    return {
        "ok": len(rows) == 5,
        "path": str(target),
        "rows": len(rows),
        "actions": actions,
        "risk_statuses": risks,
    }


def write_journal_noise_report(path: str | Path = "reports/phase9b_journal_noise_report.md") -> dict[str, Any]:
    test_path = get_test_journal_path("phase9b_report")
    result = run_isolated_journal_check(test_path)

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)

    content = f"""# EarnsAI Pulse — Phase 9B Journal Noise Control Report

## Summary
- OK: `{result["ok"]}`
- Isolated journal path: `{result["path"]}`
- Isolated rows generated: `{result["rows"]}`

## Distribution
- Actions: `{result["actions"]}`
- Risk statuses: `{result["risk_statuses"]}`

## Safety
- Main journal is not required for this isolated check.
- Test journal is stored under `runtime/test_journals/`.
- Mode remains PAPER_ONLY.
- Live trading remains locked.
- No private exchange API is used.
"""

    target.write_text(content, encoding="utf-8")

    return {
        "ok": result["ok"],
        "path": str(target),
        "noise_control": result,
    }
