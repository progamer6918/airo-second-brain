# Phase 1B Import Fix

## Issue

Running `python3 scripts/personal_workflow_smoke.py` from repo root can fail with:

`ModuleNotFoundError: No module named 'airo_personal_workflow'`

## Cause

Python sets `sys.path[0]` to the script directory, which is `scripts/`, not the repository root.

## Fix

The smoke script now inserts the repository root into `sys.path` before importing `airo_personal_workflow`.

## Expected Result

`PERSONAL_WORKFLOW_SMOKE_PASS`\n