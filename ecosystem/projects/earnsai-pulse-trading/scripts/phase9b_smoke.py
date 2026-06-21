#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from earnsai.common.config import get_config
from earnsai.evaluation.journal_control import (
    count_rows,
    get_test_journal_path,
    isolated_journal,
    reset_journal,
    run_isolated_journal_check,
    write_journal_noise_report,
)
from earnsai.journal.jsonl_store import read_jsonl
from earnsai.data.provider_runner import run_cycle_from_provider


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    cfg = get_config()
    main_journal = Path(cfg.journal_path)
    main_before = count_rows(main_journal) if main_journal.exists() else 0

    test_path = get_test_journal_path("phase9b_smoke")
    reset_journal(test_path)

    with isolated_journal(test_path):
        run_cycle_from_provider(scenario="bullish")
        run_cycle_from_provider(scenario="flat")

    test_rows = read_jsonl(test_path, limit=0)
    main_after = count_rows(main_journal) if main_journal.exists() else 0

    assert_true(len(test_rows) == 2, "isolated journal must receive exactly two rows")
    assert_true(main_after == main_before, "main journal row count must not change during isolated journal context")

    result = run_isolated_journal_check(get_test_journal_path("phase9b_check"))
    assert_true(result["ok"] is True, "isolated journal check must pass")
    assert_true(result["rows"] == 5, "isolated check must write five rows")

    report = write_journal_noise_report()
    assert_true(report["ok"] is True, "journal noise report must be ok")
    assert_true(Path(report["path"]).exists(), "journal noise report must exist")

    print(
        "PHASE9B_SMOKE PASS "
        f"main_before={main_before} "
        f"main_after={main_after} "
        f"isolated_rows={len(test_rows)} "
        f"report={report['path']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
