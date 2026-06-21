# GitHub Branch Policy

## Stable Branch
- main is the stable GitHub default branch candidate.
- main must stay synchronized with verified safe checkpoints.

## Working Branch
- local-issue-workflow remains the active working branch for local task execution.
- Work should be documented through local issue files before important commits.

## Safety Boundary
- PAPER_ONLY remains enforced.
- Live trading stays locked.
- Private exchange API usage stays disabled.
- Secrets, tokens, credentials, sessions, cookies, private keys, and .env files must never be committed or printed.

## Commit Rule
- Run python3 scripts/ci_safe_gate.py before important commits.
- Restore generated reports and signal outputs before committing workflow documentation.
- Do not push subprojects from the main trading repo.
