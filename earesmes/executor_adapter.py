#!/usr/bin/env python3
"""
EARESMES Executor Adapter — V1
================================
Controlled handoff package layer.

Governance limits enforced:
  - No model/AI calls
  - No autonomous execution
  - No external API calls
  - No runner modification
  - No self-modification
  - Package creation is preparation ONLY — never triggers execution
  - Adapter does NOT launch Antigravity or any other executor

Creates a structured, filesystem-based execution package directory
that a designated executor can consume when directed by the owner.

Standard library only. No external dependencies.

Usage (standalone):
    python3 earesmes/executor_adapter.py <job_json_path>

Output directory:
    earesmes/execution_packages/<job_id>/
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ADAPTER_VERSION = "1.0.0"
CREATED_BY = "earesmes_executor_adapter"

# Capabilities that warrant an execution package (excludes owner_review/unknown
# which require manual owner action, not an execution package).
PACKAGEABLE_CAPABILITIES = {"development", "maintenance", "airo_workdesk", "knowledge"}

# Executor label written into handoff.json — informational only.
CAPABILITY_EXECUTOR_MAP = {
    "development": "antigravity",
    "maintenance": "local",
    "airo_workdesk": "awd_workflow",
    "knowledge": "asb_kcc",
    "owner_review": "owner",
    "unknown": "unknown",
}

# ---------------------------------------------------------------------------
# Package file content builders
# ---------------------------------------------------------------------------

_CONSTRAINTS_MD = """\
# EARESMES Execution Constraints

## Coordinator Role

EARESMES is a **controlled coordinator only**. It does NOT execute autonomously.

## Executor Responsibilities

Before any mutation, the executor MUST:

1. Read and confirm the objective in `objective.md`.
2. Validate scope against `handoff.json` capability and risk fields.
3. Verify no expansion beyond the stated objective is required.
4. Confirm owner approval if risk is `high`.

## Hard Limits

- **EARESMES is coordinator only.** No autonomous expansion.
- **Executor must verify before any mutation.**
- **No autonomous scope expansion** beyond the original objective.
- **No secret, credential, or sensitive data** may be written to this package.
- **Execution package is read-only metadata.** Executor writes results separately.

## Governance

```
NO_AUTONOMOUS_EXECUTION=ENFORCED
NO_SCOPE_EXPANSION=ENFORCED
COORDINATOR_ONLY=EARESMES
```
"""

_RECEIPT_CONTRACT_MD = """\
# Executor Receipt Contract

Upon completing execution, the designated executor MUST return a receipt
containing ALL of the following fields. Partial receipts are not accepted.

## Required Receipt Fields

| Field                | Description                                      |
|----------------------|--------------------------------------------------|
| `RESULT`             | PASS or FAIL                                     |
| `EXIT_CODE`          | Integer exit code (0 = success)                  |
| `CHANGED_FILES`      | List of files created, modified, or deleted      |
| `COMMIT_SHA`         | Git commit SHA if a commit was made (or NONE)    |
| `VALIDATION_EVIDENCE`| Proof that the objective was met (log, output, etc.) |

## Receipt Delivery

Return the receipt to the EARESMES state directory:

    earesmes/state/receipts/<job_id>_executor_receipt.json

## Non-Negotiable

- `EXIT_CODE=0` alone is NOT sufficient for PASS.
- `RESULT=PASS` requires verified `VALIDATION_EVIDENCE`.
- If `CHANGED_FILES` is non-empty, `COMMIT_SHA` must be present.
"""


def _objective_md(job_id: str, objective: str, capability: str, risk: str) -> str:
    return f"""\
# Execution Objective

**Job ID:** `{job_id}`
**Capability:** `{capability}`
**Risk:** `{risk}`

## Objective

{objective}

## Notes

- This is the verbatim human-authored objective. Do not interpret beyond its literal scope.
- Executor must NOT expand, infer, or add sub-tasks autonomously.
- All actions must be directly traceable to this objective statement.
"""


def _handoff_json(
    job_id: str,
    executor: str,
    capability: str,
    risk: str,
) -> dict:
    return {
        "adapter_version": ADAPTER_VERSION,
        "job_id": job_id,
        "executor": executor,
        "capability": capability,
        "risk": risk,
        "status": "READY_FOR_EXECUTION",
        "created_by": CREATED_BY,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "governance": {
            "no_autonomous_execution": True,
            "no_scope_expansion": True,
            "coordinator_only": "earesmes",
            "executor_must_verify_before_mutation": True,
        },
    }


# ---------------------------------------------------------------------------
# Core public API
# ---------------------------------------------------------------------------

def create_execution_package(
    job: dict,
    packages_base_dir: Optional[Path] = None,
) -> Path:
    """
    Create a structured execution package directory for a validated job.

    Does NOT execute anything. Does NOT call any external service.
    Returns the path to the created package directory.

    Args:
        job: Validated job dict (must contain job_id, objective, capability, boundary).
        packages_base_dir: Base directory for packages. Defaults to
                           earesmes/execution_packages/ relative to this file.

    Raises:
        ValueError: If job is missing required fields.
        OSError: If package directory cannot be written.
    """
    # -- Validate input -------------------------------------------------------
    job_id = job.get("job_id")
    if not job_id or not isinstance(job_id, str):
        raise ValueError("job missing valid 'job_id'")

    objective = job.get("objective")
    if not objective or not isinstance(objective, str):
        raise ValueError(f"job '{job_id}' missing valid 'objective'")

    capability_block = job.get("capability", {})
    capability = capability_block.get("capability", "unknown")
    executor = capability_block.get("executor_hint") or CAPABILITY_EXECUTOR_MAP.get(capability, "unknown")

    boundary_block = job.get("boundary", {})
    risk = boundary_block.get("risk", "unknown")

    # -- Resolve package dir --------------------------------------------------
    if packages_base_dir is None:
        packages_base_dir = Path(__file__).parent / "execution_packages"

    package_dir = packages_base_dir / job_id
    package_dir.mkdir(parents=True, exist_ok=True)

    # -- Write objective.md ---------------------------------------------------
    (package_dir / "objective.md").write_text(
        _objective_md(job_id, objective, capability, risk),
        encoding="utf-8",
    )

    # -- Write constraints.md -------------------------------------------------
    (package_dir / "constraints.md").write_text(
        _CONSTRAINTS_MD,
        encoding="utf-8",
    )

    # -- Write handoff.json ---------------------------------------------------
    handoff = _handoff_json(job_id, executor, capability, risk)
    (package_dir / "handoff.json").write_text(
        json.dumps(handoff, indent=2) + "\n",
        encoding="utf-8",
    )

    # -- Write receipt_contract.md --------------------------------------------
    (package_dir / "receipt_contract.md").write_text(
        _RECEIPT_CONTRACT_MD,
        encoding="utf-8",
    )

    return package_dir


def should_create_package(job: dict) -> bool:
    """
    Return True if this job's capability warrants an execution package.

    Only development, maintenance, airo_workdesk, and knowledge
    capabilities are packaged. owner_review and unknown require
    direct owner action — no package is created.
    """
    capability = job.get("capability", {}).get("capability", "unknown")
    return capability in PACKAGEABLE_CAPABILITIES


# ---------------------------------------------------------------------------
# Standalone CLI (for testing / validation only)
# ---------------------------------------------------------------------------

def _main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        print(
            "Usage: python3 earesmes/executor_adapter.py <job_json_path>",
            file=sys.stderr,
        )
        return 1

    job_path = Path(argv[0])
    if not job_path.exists():
        print(f"ERROR: Job file not found: {job_path}", file=sys.stderr)
        return 1

    try:
        job = json.loads(job_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: Cannot read job file: {exc}", file=sys.stderr)
        return 1

    if not should_create_package(job):
        capability = job.get("capability", {}).get("capability", "unknown")
        print(f"EXECUTION_PACKAGE_CREATED=NO")
        print(f"REASON=capability '{capability}' requires owner action — no package created")
        return 0

    try:
        package_dir = create_execution_package(job)
    except (ValueError, OSError) as exc:
        print(f"ERROR: Package creation failed: {exc}", file=sys.stderr)
        return 1

    print(f"EXECUTION_PACKAGE_CREATED=YES")
    print(f"PATH={package_dir}")
    print(f"STATUS=READY_FOR_EXECUTION")
    return 0


if __name__ == "__main__":
    sys.exit(_main())
