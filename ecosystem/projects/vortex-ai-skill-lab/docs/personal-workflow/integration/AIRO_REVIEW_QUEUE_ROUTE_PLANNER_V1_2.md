# AIRO Review Queue Route Planner v1.2

Status: IMPLEMENTED / READ-ONLY PLANNER
Date: 2026-05-11
Scope: AIRO Finance Sheet Workflow

## Purpose

This artifact adds a local read-only planner for ambiguous finance messages.

It supports the v1.2 goal that parser ambiguity must go to:

🧾 Review Queue

The planner does not perform Google writes, SQLite mutations, credential reads, or OpenClaw restarts.

## Artifact

Script:

scripts/personal-workflow/airo_review_queue_planner.py

Test:

tests/personal-workflow/test_airo_review_queue_planner.py

## Behavior

The planner evaluates a raw finance message and returns a deterministic plan.

It routes to 🧾 Review Queue when it detects:

- low confidence
- missing amount
- missing or unknown account
- missing or unknown category
- unclear debt person
- cash entry without enough detail
- cicilan rumah payment where default amount handling is needed

If no review is needed, it returns the suggested finance domain tab.

## Safety

The planner is dry-run only.

Safety fields are always false:

- google_write_performed
- sqlite_mutation_performed
- credential_read_performed
- openclaw_restart_performed

## Next Item

Integrate the planner into the dry-run/write-preview mapper so low-confidence or incomplete finance captures can become Review Queue candidates without touching production Google writes.
