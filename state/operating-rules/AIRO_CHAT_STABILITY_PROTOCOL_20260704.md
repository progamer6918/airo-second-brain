# AIRO Chat Stability Protocol — 2026-07-04

## Status

Owner-approved operating rule.

## Problem

AIRO sessions became unstable even in new chats because the workflow repeatedly placed too much operational state inside chat turns:

- oversized WSL commands;
- oversized pasted logs;
- too many gates combined into one command;
- runtime, validation, and docs commit combined too often;
- chat used as primary state instead of ASB;
- full evidence copied into chat instead of summarized with log paths and ASB docs.

## Rule

When the user says “chat rusak”, “chat lo rusak”, or equivalent:

1. Stop runtime/deploy/workbook mutation immediately.
2. Do not continue the active technical gate.
3. Summarize current state in under 20 lines.
4. Move durable state/evidence into ASB.
5. Resume only with a smaller next gate.

## Command Size Rule

- Prefer one command per turn.
- Prefer compact commands.
- Avoid commands longer than roughly 120 lines in chat.
- If a script must be long, split into smaller gates.
- Do not combine source patch, runtime run, readback, and docs commit in one command unless explicitly necessary.

## Output Rule

User should paste only the final summary block unless asked otherwise:

- RESULT
- EXIT_CODE
- LOG_PATH
- COMMIT_SHA, if any
- VALIDATION_DOC, if any
- PASS/BLOCKED reason
- last 40–80 lines when needed

Full logs should stay in `/tmp` and be summarized into ASB validation docs.

## Gate Separation Rule

Separate these gates by default:

1. docs-only canonicalization;
2. read-only audit;
3. local source patch/static validation;
4. source commit;
5. clasp push;
6. runtime manual refresh;
7. readback validation;
8. owner visual sanity;
9. scheduler, only if explicitly approved.

## Runtime Rule

Do not start runtime/deploy/workbook mutation in a chat that is already showing stability problems.

## ASB Rule

ASB is the durable state. Chat is only an execution surface.

Every long-running AIRO sequence should checkpoint to ASB after 2–3 gates or after any PASS that changes project direction.
