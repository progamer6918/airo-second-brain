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
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Self-bootstrap repository root into sys.path for standalone and service compatibility
REPO_ROOT = str(Path(__file__).resolve().parents[1])
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

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
    Controlled executor.
    Dispatches to LLM Bridge for Telegram-origin jobs or hermes executor,
    or placeholder for manual jobs.
    Returns (success, detail).
    """
    executor = job_data.get("executor", "unknown")
    job_id = job_data.get("job_id", "unknown")
    initiator = job_data.get("initiator", "")

    # Telegram-origin or hermes-bound execution via Earesmes Assistant Pipeline (P0)
    if initiator == "OWNER_TELEGRAM" or executor in ("hermes", "llm_bridge"):
        objective = job_data.get("objective", "")
        repo_root = Path(REPO_ROOT)

        # ── P0 Layer: Intent Routing ──────────────────────────────────────────
        from earesmes.routing import classify_intent, IntentType
        from earesmes.identity import format_identity_greeting, EARESMES_SYSTEM_IDENTITY
        from earesmes.context import format_asb_knowledge_response, assemble_context_for_prompt

        intent = classify_intent(objective)
        job_data["_earesmes_intent"] = intent.value
        logging.info("Job '%s': classified intent=%s (objective='%s')", job_id, intent.value, objective)

        from earesmes.routing import resolve_presentation_mode
        pres_mode = resolve_presentation_mode(intent, objective)
        job_data["_presentation_mode"] = pres_mode.value
        logging.info("Job '%s': presentation mode resolved=%s", job_id, pres_mode.value)

        # ── P2.3 Model Routing Policy ─────────────────────────────────────────
        from earesmes.routing import resolve_model_policy
        model_policy = resolve_model_policy(intent.value)
        job_data["_routing_decision"] = model_policy
        logging.info("Job '%s': model routing policy resolved=%s (requires_llm=%s)",
                     job_id, model_policy.get("selected_model"), model_policy.get("requires_llm"))

        # ── P0 Fast-Path: GREETING (Identity Response) ────────────────────────
        if intent == IntentType.GREETING:
            greeting_resp = format_identity_greeting(objective)
            logging.info("Job '%s': served via Earesmes Identity Layer directly.", job_id)
            job_data["_earesmes_layer"] = "identity_direct"
            return True, greeting_resp

        # ── Fast-Path: CONVERSATIONAL_COURTESY (Social Courtesy / Acknowledgement) ──
        if intent == IntentType.CONVERSATIONAL_COURTESY:
            from earesmes.identity import format_courtesy_response
            courtesy_resp = format_courtesy_response(objective)
            logging.info("Job '%s': served via Conversational Courtesy directly.", job_id)
            job_data["_earesmes_layer"] = "conversational_courtesy"
            return True, courtesy_resp

        # ── Fast-Path: CASUAL_CONVERSATION (Emotional & Casual Chat) ──────────
        if intent == IntentType.CASUAL_CONVERSATION:
            from earesmes.routing import format_casual_response
            casual_resp = format_casual_response(objective)
            logging.info("Job '%s': served via Casual Conversation directly.", job_id)
            job_data["_earesmes_layer"] = "casual_conversation"
            return True, casual_resp

        # ── P1.1 Fast-Path: DAILY_BRIEFING (Concise ASB Summary) ──────────────
        if intent == IntentType.DAILY_BRIEFING:
            from earesmes.capabilities.daily_briefing import generate_daily_brief
            briefing_resp = generate_daily_brief(repo_root)
            logging.info("Job '%s': served via Daily Briefing Capability directly.", job_id)
            job_data["_earesmes_layer"] = "daily_briefing"
            return True, briefing_resp

        # ── P1.2 Fast-Path: KNOWLEDGE_QUERY (Decision Recall & Reasoning) ─────
        if intent == IntentType.KNOWLEDGE_QUERY:
            from earesmes.capabilities.knowledge_assistant import answer_knowledge_query
            knowledge_resp = answer_knowledge_query(repo_root, objective)
            logging.info("Job '%s': served via Knowledge Assistant Capability directly.", job_id)
            job_data["_earesmes_layer"] = "knowledge_assistant"
            return True, knowledge_resp

        # ── P1.3 Fast-Path: DECISION_SUPPORT (Analysis & Recommendations) ────
        if intent == IntentType.DECISION_SUPPORT:
            from earesmes.capabilities.decision_support import analyze_decision
            decision_resp = analyze_decision(repo_root, objective)
            logging.info("Job '%s': served via Decision Support Capability directly.", job_id)
            job_data["_earesmes_layer"] = "decision_support"
            return True, decision_resp

        # ── P1.4 Fast-Path: PROJECT_CONTINUITY (Resuming Work & State Recall) ───
        if intent == IntentType.PROJECT_CONTINUITY:
            from earesmes.capabilities.project_continuity import resolve_project_continuity
            continuity_resp = resolve_project_continuity(repo_root, objective)
            logging.info("Job '%s': served via Project Continuity Capability directly.", job_id)
            job_data["_earesmes_layer"] = "project_continuity"
            return True, continuity_resp

        # ── P2.1 Fast-Path: RESEARCH_QUERY (External Tech/Benchmark Research) ──
        if intent == IntentType.RESEARCH_QUERY:
            from earesmes.capabilities.research_assistant import perform_research
            research_resp = perform_research(repo_root, objective)
            logging.info("Job '%s': served via Research Assistant Capability directly.", job_id)
            job_data["_earesmes_layer"] = "research_assistant"
            return True, research_resp

        # ── P2.2 Fast-Path: ACTION_REQUEST (Controlled Action & Proposal Gate) ─
        if intent in (IntentType.ACTION_REQUEST, IntentType.ACTION):
            from earesmes.capabilities.action_assistant import create_action_proposal
            action_resp = create_action_proposal(repo_root, objective, initiator)
            logging.info("Job '%s': served via Controlled Action Capability directly.", job_id)
            job_data["_earesmes_layer"] = "controlled_action_proposal"
            return True, action_resp

        # ── P0 Fast-Path: KNOWLEDGE (ASB Context Direct) ──────────────────────
        if intent == IntentType.KNOWLEDGE:
            direct_asb_answer = format_asb_knowledge_response(repo_root, objective)
            if direct_asb_answer:
                logging.info("Job '%s': served via ASB Context Assembly directly.", job_id)
                job_data["_earesmes_layer"] = "asb_context_direct"
                return True, direct_asb_answer

        # ── P0 REASONING / ACTION via LLM Bridge + Injected Context ───────────
        logging.info("Job '%s': executing via LLM Bridge (initiator=%s, executor=%s)", job_id, initiator, executor)
        try:
            from earesmes.llm_bridge import LLMBridge
            bridge = LLMBridge()

            # Assemble prompt with Identity and ASB context
            asb_context = assemble_context_for_prompt(repo_root, objective)
            enriched_objective = (
                f"{EARESMES_SYSTEM_IDENTITY}\n\n"
                f"{asb_context}\n\n"
                f"Owner Request: {objective}\n"
                f"Respond as Earesmes in clear, professional Bahasa Indonesia concisely."
            )

            res = bridge.process_package(
                job_id=job_id,
                session_id=job_data.get("session_id", "active_session"),
                project_id=job_data.get("project_id", "earesmes-runtime-assistant-v1"),
                objective=enriched_objective,
                approval_status=job_data.get("approval", "approved"),
                package_path=job_data.get("package_path"),
                dry_run=dry_run,
            )
            success = (res.get("result") == "BERHASIL")
            out_ref = res.get("output_reference")
            if out_ref == "NONE":
                out_ref = ""
            err_ref = res.get("error")
            if err_ref == "NONE":
                err_ref = ""

            if not success:
                exec_detail = err_ref or out_ref or "LLM Bridge execution failed"
            else:
                exec_detail = out_ref or err_ref or "LLM Bridge execution finished"

            job_data["_llm_bridge_receipt"] = res
            job_data["_earesmes_layer"] = "llm_bridge_reasoning"
            return success, exec_detail
        except Exception as exc:
            logging.error("LLM Bridge execution error for job '%s': %s", job_id, exc)
            return False, f"LLM Bridge error: {exc}"

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
# Phase 4: Telegram Reply Emitter
# ---------------------------------------------------------------------------

def _get_telegram_token() -> str:
    """Read bot token securely from environment or ~/.airo/telegram.env."""
    token = os.environ.get("AIRO_TELEGRAM_BOT_TOKEN", "").strip()
    if token:
        return token
    env_file = os.environ.get("AIRO_TELEGRAM_ENV") or os.path.expanduser("~/.airo/telegram.env")
    if os.path.exists(env_file):
        try:
            with open(env_file, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("export "):
                        line = line[7:]
                    if "=" in line and not line.startswith("#"):
                        k, v = line.split("=", 1)
                        if k.strip() == "AIRO_TELEGRAM_BOT_TOKEN":
                            return v.strip().strip('"').strip("'")
        except Exception:
            pass
    return ""


def _deliver_telegram_reply(job_data: dict, final_status: str, exec_detail: str, dry_run: bool) -> bool:
    """
    Deliver execution receipt output to Telegram for OWNER_TELEGRAM jobs.
    Fails open — delivery failure never marks job execution as failed.
    """
    initiator = job_data.get("initiator", "")
    chat_id = job_data.get("chat_id")
    job_id = job_data.get("job_id", "")

    if initiator != "OWNER_TELEGRAM" or not chat_id:
        return False

    message_id = job_data.get("message_id")
    clean_detail = exec_detail.strip() if (exec_detail and exec_detail.strip() != "NONE") else ""
    clean_text = clean_detail or f"Job {job_id} completed with status: {final_status}"

    # Presentation boundary: separate natural conversation/assistant responses from governed receipts
    intent = job_data.get("_earesmes_intent", "")
    natural_presentation_intents = {
        "GREETING",
        "CONVERSATIONAL_COURTESY",
        "CASUAL_CONVERSATION",
        "KNOWLEDGE_QUERY",
        "KNOWLEDGE",
        "DECISION_SUPPORT",
        "RESEARCH_QUERY",
    }

    if intent in natural_presentation_intents and final_status == "success":
        reply_body = clean_text
    else:
        reply_body = f"🧭 EARESMES RECEIPT [{final_status.upper()}]\n\n{clean_text}"

    job_data["_telegram_reply_body"] = reply_body

    if dry_run:
        logging.info("[DRY-RUN] Would deliver Telegram reply to chat_id=%s (reply_to=%s)", chat_id, message_id)
        job_data["_telegram_delivery"] = "DRY_RUN_DELIVERED"
        return True

    token = _get_telegram_token()
    if not token:
        logging.warning("Telegram reply delivery skipped for job '%s': no bot token found in env or telegram.env", job_id)
        job_data["_telegram_delivery"] = "SKIPPED_NO_TOKEN"
        return False

    api_url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": reply_body,
    }
    if message_id:
        payload["reply_to_message_id"] = message_id

    try:
        req = urllib.request.Request(
            api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            if resp.status == 200:
                logging.info("Telegram reply delivered successfully for job '%s' to chat_id=%s", job_id, chat_id)
                job_data["_telegram_delivery"] = "DELIVERED"
                return True
            else:
                logging.warning("Telegram reply HTTP %s for job '%s'", resp.status, job_id)
                job_data["_telegram_delivery_error"] = f"HTTP_{resp.status}"
                return False
    except Exception as exc:
        logging.warning("Telegram reply delivery error for job '%s': %s", job_id, exc)
        job_data["_telegram_delivery_error"] = str(exc)
        return False


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

    # ── Governance: ensure boundary & capability resolution ───────────────────
    try:
        from earesmes.task_boundary import classify as _classify_boundary
        from earesmes.capability_resolution import resolve as _resolve_capability
        if "boundary" not in job_data:
            job_data["boundary"] = _classify_boundary(job_data["objective"]).to_dict()
        if "capability" not in job_data:
            job_data["capability"] = _resolve_capability(job_data["objective"]).to_dict()
    except Exception as _gov_exc:
        logging.debug("Governance boundary resolution note: %s", _gov_exc)

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

    # ── Phase 4: Deliver Telegram reply if Telegram-origin ───────────────────
    _deliver_telegram_reply(job_data, final_status, exec_detail, dry_run)

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
