#!/usr/bin/env python3
"""
EARESMES Command Interface V1
==============================
Controlled human-to-job entry point.

Governance limits enforced:
  - No model/AI calls
  - No shell execution
  - No external API calls
  - No runner modification
  - User input stored ONLY as job objective (never executed)
  - Task boundary classification is deterministic metadata only (never triggers execution)
  - Capability resolution is deterministic metadata only (never triggers execution)

Standard library only. No external dependencies.

Usage:
    python3 earesmes/cli.py submit "human instruction"
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Task boundary import — deterministic classifier, no model calls
_BOUNDARY_DIR = Path(__file__).parent
if str(_BOUNDARY_DIR) not in sys.path:
    sys.path.insert(0, str(_BOUNDARY_DIR))
from task_boundary import classify as _classify_boundary  # noqa: E402
from capability_resolution import resolve as _resolve_capability  # noqa: E402



# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CLI_VERSION = "1.0.0"
CREATED_BY = "earesmes_cli"
DEFAULT_JOBS_DIR = Path(__file__).parent / "jobs"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _timestamp() -> str:
    """Return UTC timestamp string suitable for filenames and job IDs."""
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _generate_job_id(ts: str) -> str:
    return f"job_{ts}"


def _build_job(job_id: str, objective: str) -> dict:
    """Construct a validated job dict. No execution, no model calls."""
    boundary = _classify_boundary(objective)
    capability = _resolve_capability(objective)
    return {
        "job_id": job_id,
        "objective": objective,
        "executor": "manual",
        "approval": "approved",
        "status": "pending",
        "created_by": CREATED_BY,
        "boundary": boundary.to_dict(),
        "capability": capability.to_dict(),
    }


def _write_job(pending_dir: Path, job_id: str, job: dict) -> Path:
    """Write job JSON to pending dir. Returns path written."""
    pending_dir.mkdir(parents=True, exist_ok=True)
    job_path = pending_dir / f"{job_id}.json"
    job_path.write_text(json.dumps(job, indent=2) + "\n", encoding="utf-8")
    return job_path


# ---------------------------------------------------------------------------
# Subcommand: submit
# ---------------------------------------------------------------------------


def cmd_submit(args: list[str], jobs_dir: Path) -> int:
    """
    submit <objective>

    Validates input, creates a pending job JSON.
    NEVER executes the objective.
    """
    if len(args) != 1:
        print("ERROR: 'submit' requires exactly one argument: the objective text.", file=sys.stderr)
        print("Usage: python3 earesmes/cli.py submit \"human instruction\"", file=sys.stderr)
        return 1

    objective = args[0].strip()

    if not objective:
        print("ERROR: Objective must not be empty.", file=sys.stderr)
        return 1

    if len(objective) > 2000:
        print("ERROR: Objective exceeds 2000 character limit.", file=sys.stderr)
        return 1

    ts = _timestamp()
    job_id = _generate_job_id(ts)
    job = _build_job(job_id, objective)
    job_path = _write_job(jobs_dir / "pending", job_id, job)

    print(f"JOB_CREATED=PASS")
    print(f"JOB_ID={job_id}")
    print(f"JOB_PATH={job_path}")
    print(f"BOUNDARY_CATEGORY={job['boundary']['category']}")
    print(f"BOUNDARY_RISK={job['boundary']['risk']}")
    print(f"BOUNDARY_APPROVAL_REQUIRED={job['boundary']['approval_required']}")
    print(f"BOUNDARY_EXECUTOR_HINT={job['boundary']['executor_hint']}")
    print(f"CAPABILITY={job['capability']['capability']}")
    print(f"CAPABILITY_EXECUTOR_HINT={job['capability']['executor_hint']}")
    print(f"CAPABILITY_AUTHORITY={job['capability']['authority']}")
    return 0


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        print("Usage: python3 earesmes/cli.py submit \"human instruction\"", file=sys.stderr)
        return 1

    command = argv[0]
    rest = argv[1:]

    jobs_dir = DEFAULT_JOBS_DIR

    if command == "submit":
        return cmd_submit(rest, jobs_dir)

    print(f"ERROR: Unknown command '{command}'. Available: submit", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
