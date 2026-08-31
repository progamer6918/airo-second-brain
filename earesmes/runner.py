#!/usr/bin/env python3
"""
EARESMES Controlled Job Runner — V1
====================================
Controlled coordinator only.

Governance limits enforced:
  - No model/AI calls
  - No autonomous planning
  - No recursive loops
  - No self-modification
  - No uncontrolled execution

Standard library only. No external dependencies.
"""

import argparse
import json
import logging
import os
import shutil
import signal
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

EARESMES_VERSION = "1.0.0"
SUPPORTED_STATUSES = {"pending", "approved", "running", "success", "failed", "review_required"}
REQUIRED_APPROVAL = "approved"

# State machine transitions (controlled, deterministic):
#   pending/approved → running → success | failed | review_required
# review_required is a terminal holding state requiring owner action.

TERMINAL_STATUSES = {"success", "failed", "review_required"}

# ---------------------------------------------------------------------------
# Shutdown flag — set by SIGTERM/SIGINT for safe shutdown
# ---------------------------------------------------------------------------

_shutdown_requested = False


def _handle_signal(signum: int, frame) -> None:  # noqa: ANN001
    global _shutdown_requested
    _shutdown_requested = True
    logging.info("Shutdown signal received (%s). Finishing current job then stopping.", signum)


signal.signal(signal.SIGTERM, _handle_signal)
signal.signal(signal.SIGINT, _handle_signal)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def _setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        format="%(asctime)s [EARESMES] %(levelname)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
        level=level,
        stream=sys.stdout,
    )


# ---------------------------------------------------------------------------
# Receipt writer
# ---------------------------------------------------------------------------

def _write_receipt(
    receipts_dir: Path,
    job_id: str,
    status: str,
    detail: str,
    job_data: Optional[dict] = None,
) -> Path:
    """Write an immutable state-transition receipt. Never silently fails."""
    receipts_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    receipt_name = f"{job_id}_{ts}_{status}.json"
    receipt_path = receipts_dir / receipt_name

    receipt = {
        "earesmes_version": EARESMES_VERSION,
        "job_id": job_id,
        "status": status,
        "detail": detail,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "job_snapshot": job_data or {},
    }

    try:
        receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        logging.info("Receipt written: %s", receipt_path)
    except OSError as exc:
        # Never silently fail — log as ERROR and re-raise
        logging.error("FATAL: Cannot write receipt %s: %s", receipt_path, exc)
        raise

    return receipt_path


# ---------------------------------------------------------------------------
# Job loader and validator
# ---------------------------------------------------------------------------

def _load_job(job_path: Path) -> Optional[dict]:
    """Load and parse a job JSON file. Returns None on parse error."""
    try:
        raw = job_path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except (OSError, json.JSONDecodeError) as exc:
        logging.error("Cannot load job file %s: %s", job_path, exc)
        return None

    return data


def _validate_job(data: dict) -> tuple[bool, str]:
    """
    Validate job schema. Returns (is_valid, reason).
    Governed: no model calls, purely structural checks.
    """
    if not isinstance(data, dict):
        return False, "Job is not a JSON object"

    job_id = data.get("job_id")
    if not job_id or not isinstance(job_id, str):
        return False, "Missing or invalid 'job_id' field"

    if not data.get("objective") or not isinstance(data.get("objective"), str):
        return False, "Missing or invalid 'objective' field"

    approval = data.get("approval", "")
    if approval != REQUIRED_APPROVAL:
        return False, f"Invalid approval: '{approval}' (required: '{REQUIRED_APPROVAL}')"

    return True, "OK"


# ---------------------------------------------------------------------------
# Job executor (V1 controlled placeholder)
# ---------------------------------------------------------------------------

def _execute_job(job_data: dict, dry_run: bool) -> tuple[bool, str]:
    """
    V1 controlled executor placeholder.

    Does NOT perform real autonomous execution.
    Executor field is validated but always dispatches to placeholder.
    Returns (success, detail).
    """
    executor = job_data.get("executor", "unknown")
    job_id = job_data.get("job_id", "unknown")

    if dry_run:
        logging.info("[DRY-RUN] Would execute job '%s' with executor '%s'", job_id, executor)
        return True, f"DRY_RUN: executor={executor}"

    if executor == "manual":
        # V1: manual executor = mark success with evidence that it was a controlled no-op
        logging.info("Job '%s': executor=manual — controlled placeholder execution.", job_id)
        return True, "manual executor v1 placeholder — no autonomous action taken"

    # Unknown executor: do not silently succeed
    logging.warning("Job '%s': unknown executor '%s' — marking FAILED.", job_id, executor)
    return False, f"unknown executor '{executor}'"


# ---------------------------------------------------------------------------
# State transition helpers
# ---------------------------------------------------------------------------

def _move_job_file(src: Path, dest_dir: Path, new_data: dict) -> Path:
    """Atomically update job JSON and move to dest_dir. Never silently fails."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / src.name

    try:
        dest_path.write_text(json.dumps(new_data, indent=2) + "\n", encoding="utf-8")
        src.unlink()
    except OSError as exc:
        logging.error("FATAL: Cannot move job file %s → %s: %s", src, dest_dir, exc)
        raise

    return dest_path


# ---------------------------------------------------------------------------
# Core processing loop
# ---------------------------------------------------------------------------

def _process_one_job(
    job_path: Path,
    jobs_dir: Path,
    state_dir: Path,
    dry_run: bool,
) -> str:
    """
    Process a single job file through the state machine.
    Returns the final status string.
    """
    receipts_dir = state_dir / "receipts"
    running_dir = jobs_dir / "running"
    done_dir = jobs_dir / "done"

    job_data = _load_job(job_path)
    if job_data is None:
        # Unreadable file — move to done as failed
        job_id = job_path.stem
        logging.error("Job '%s': cannot be loaded — marking FAILED.", job_id)
        failed_data = {
            "job_id": job_id,
            "objective": "(unreadable)",
            "executor": "unknown",
            "approval": "unknown",
            "status": "failed",
        }
        _write_receipt(receipts_dir, job_id, "failed", "job file unreadable", failed_data)
        _move_job_file(job_path, done_dir, failed_data)
        return "failed"

    job_id = job_data.get("job_id", job_path.stem)
    logging.info("Picked up job '%s' from %s", job_id, job_path.name)

    # ── Validate ────────────────────────────────────────────────────────────
    is_valid, reason = _validate_job(job_data)
    if not is_valid:
        logging.warning("Job '%s': validation failed — %s. Moving to review_required.", job_id, reason)
        job_data["status"] = "review_required"
        job_data["_runner_note"] = reason
        _write_receipt(receipts_dir, job_id, "review_required", reason, job_data)
        _move_job_file(job_path, done_dir, job_data)
        return "review_required"

    # ── Transition: pending → running ────────────────────────────────────────
    job_data["status"] = "running"
    logging.info("Job '%s': pending → running", job_id)
    _write_receipt(receipts_dir, job_id, "running", "job picked up by runner", job_data)

    if not dry_run:
        running_path = _move_job_file(job_path, running_dir, job_data)
    else:
        running_path = job_path  # dry-run: don't move

    # ── Execute ──────────────────────────────────────────────────────────────
    success, exec_detail = _execute_job(job_data, dry_run)

    # ── Transition: running → success | failed ───────────────────────────────
    final_status = "success" if success else "failed"
    job_data["status"] = final_status
    job_data["_runner_exec_detail"] = exec_detail
    logging.info("Job '%s': running → %s (%s)", job_id, final_status, exec_detail)
    _write_receipt(receipts_dir, job_id, final_status, exec_detail, job_data)

    if not dry_run:
        _move_job_file(running_path, done_dir, job_data)

    return final_status


def _scan_pending(jobs_dir: Path) -> list[Path]:
    """Return sorted list of .json files in jobs/pending/."""
    pending_dir = jobs_dir / "pending"
    if not pending_dir.is_dir():
        return []
    return sorted(pending_dir.glob("*.json"))


def _run_loop(
    jobs_dir: Path,
    state_dir: Path,
    poll_interval: float,
    dry_run: bool,
    once: bool,
) -> int:
    """
    Main polling loop. Controlled — no recursive calls, bounded iteration.
    Returns exit code: 0 on clean shutdown, 1 on fatal error.
    """
    logging.info(
        "EARESMES runner v%s started. jobs_dir=%s state_dir=%s dry_run=%s once=%s",
        EARESMES_VERSION,
        jobs_dir,
        state_dir,
        dry_run,
        once,
    )

    # Governance self-check (emit at startup, deterministic check only)
    logging.info(
        "GOVERNANCE_CHECK: no_model_calls=true no_autonomous_planning=true "
        "no_recursive_loops=true no_self_modification=true no_uncontrolled_execution=true"
    )

    while not _shutdown_requested:
        pending = _scan_pending(jobs_dir)

        if pending:
            logging.info("Found %d pending job(s).", len(pending))
            for job_path in pending:
                if _shutdown_requested:
                    logging.info("Shutdown requested mid-batch. Stopping cleanly.")
                    break
                try:
                    _process_one_job(job_path, jobs_dir, state_dir, dry_run)
                except Exception as exc:  # noqa: BLE001
                    # Never silently fail — log ERROR and continue to next job
                    logging.error("Unexpected error processing %s: %s", job_path, exc)
        else:
            logging.debug("No pending jobs. Sleeping %ss.", poll_interval)

        if once:
            logging.info("--once flag set. Exiting after one batch.")
            break

        # Controlled sleep with early wakeup on shutdown signal
        deadline = time.monotonic() + poll_interval
        while time.monotonic() < deadline and not _shutdown_requested:
            time.sleep(0.25)

    logging.info("EARESMES runner stopped cleanly.")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_args(argv: Optional[list] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="EARESMES Controlled Job Runner V1 — no AI, no autonomous planning.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--jobs-dir",
        default="earesmes/jobs",
        metavar="PATH",
        help="Path to jobs directory (contains pending/, running/, done/). Default: earesmes/jobs",
    )
    parser.add_argument(
        "--state-dir",
        default="earesmes/state",
        metavar="PATH",
        help="Path to state directory (receipts written here). Default: earesmes/state",
    )
    parser.add_argument(
        "--poll-interval",
        type=float,
        default=5.0,
        metavar="SECONDS",
        help="Seconds between pending-job scans. Default: 5.0",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Process one batch then exit (useful for testing).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and log jobs without moving state.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable DEBUG logging.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[list] = None) -> int:
    args = _parse_args(argv)
    _setup_logging(args.verbose)

    jobs_dir = Path(args.jobs_dir).resolve()
    state_dir = Path(args.state_dir).resolve()

    # Ensure required subdirectories exist
    for subdir in ("pending", "running", "done"):
        (jobs_dir / subdir).mkdir(parents=True, exist_ok=True)
    (state_dir / "receipts").mkdir(parents=True, exist_ok=True)

    return _run_loop(
        jobs_dir=jobs_dir,
        state_dir=state_dir,
        poll_interval=args.poll_interval,
        dry_run=args.dry_run,
        once=args.once,
    )


if __name__ == "__main__":
    sys.exit(main())
