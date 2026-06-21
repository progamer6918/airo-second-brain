# GitHub Branch Protection Readiness Checklist

## Result
Branch protection is not enabled yet. This document defines the readiness checklist before protection is applied.

## Current Verified Branches
- main is the stable default branch candidate.
- local-issue-workflow remains the active working branch.
- main and local-issue-workflow must stay synchronized after verified checkpoints.

## Recommended Protection Rules
- Require pull request before merging into main when collaboration starts.
- Require CI Safe Gate to pass before merging into main.
- Block force pushes to main.
- Block deletion of main.
- Keep local-issue-workflow available for safe local issue execution.

## Safety Boundary
- PAPER_ONLY remains enforced.
- Live trading remains locked.
- Private exchange API usage remains disabled.
- Real-money trading remains disabled.
- Secrets, tokens, credentials, cookies, sessions, private keys, API keys, and .env files must never be committed or printed.

## Before Enabling Protection
- Confirm GitHub Actions CI Safe workflow is green in GitHub UI.
- Confirm main is selected as the default branch.
- Confirm no subprojects are accidentally included.
- Confirm no generated reports or signal outputs are staged.
