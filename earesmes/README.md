# EARESMES Controlled Job Runner — V1

EARESMES is a **controlled job runner** — not an autonomous agent.

## Role

Coordinator only. No model calls. No autonomous planning. No self-modification.
Every state transition is deterministic and evidence-bound.

## Directory Layout

```
earesmes/
  README.md           — This file
  runner.py           — Controlled job runner (stdlib only)
  jobs/
    pending/          — Jobs awaiting execution
    running/          — Jobs currently being processed
    done/             — Completed jobs (success or failed)
  state/              — Runtime state snapshots and receipts
```

## Job Contract

Jobs are JSON files placed in `jobs/pending/`. Schema:

```json
{
  "job_id": "example",
  "objective": "Human-readable description of the job",
  "executor": "manual",
  "approval": "approved",
  "status": "pending"
}
```

### Supported Statuses

| Status           | Meaning                                      |
|------------------|----------------------------------------------|
| `pending`        | Created, awaiting runner pickup              |
| `approved`       | (alias for pending with approval set)        |
| `running`        | Runner has picked it up                      |
| `success`        | Completed successfully                       |
| `failed`         | Execution failed                             |
| `review_required`| Approval missing or invalid — requires owner |

### Approval Field

- `"approval": "approved"` — job may run
- Any other value or missing field → job moved to `review_required`

## Running the Runner

```bash
python3 earesmes/runner.py --jobs-dir earesmes/jobs --state-dir earesmes/state
```

Optional flags:
- `--once` — process one batch then exit (useful for testing)
- `--dry-run` — validate jobs but do not move state

## Receipts

Every state transition writes a receipt to `earesmes/state/receipts/`.
Receipt filename: `<job_id>_<timestamp>_<status>.json`

## Governance Limits

```
EARESMES_JOB_RUNNER_V1_LIMITS=PASS
  no_model_calls=true
  no_autonomous_planning=true
  no_recursive_loops=true
  no_self_modification=true
  no_uncontrolled_execution=true
```

## Systemd

See `systemd/earesmes-job-runner.service`.
Do **not** enable permanently without validation.
