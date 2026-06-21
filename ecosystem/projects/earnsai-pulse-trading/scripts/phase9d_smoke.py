#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.ci_safe_gate import run_ci_safe_gate


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    result = run_ci_safe_gate()

    assert_true(result["ok"] is True, "CI safe gate must pass")
    assert_true(Path(result["report_path"]).exists(), "CI safe gate report must exist")
    assert_true(len(result["results"]) >= 8, "CI safe gate must run expected gates")
    assert_true(all(item["ok"] is True for item in result["results"]), "all CI gates must pass")

    print(
        "PHASE9D_SMOKE PASS "
        f"gates={len(result['results'])} "
        f"report={result['report_path']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
