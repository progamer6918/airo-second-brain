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
