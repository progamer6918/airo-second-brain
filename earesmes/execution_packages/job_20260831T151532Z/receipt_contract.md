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
