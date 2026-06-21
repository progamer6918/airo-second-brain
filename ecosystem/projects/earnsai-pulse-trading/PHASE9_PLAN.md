# EarnsAI Pulse Trading — Phase 9 Plan

## Status
Phase 7 MVP and Phase 8 Evaluation Hardening have been promoted to master.

## Phase 9 Principle
Phase 9 focuses on controlled data input hardening, report cleanup, and test discipline. It does not enable live trading.

## Not Allowed in Phase 9
- No live trading.
- No private exchange API.
- No real-money execution.
- No manual buy or sell commands.
- No command that prints env files, tokens, API keys, private keys, or credentials.

## Main Goals
1. Build public/free data adapter abstraction.
2. Add deterministic data provider interface.
3. Reduce repeated journal noise during smoke tests.
4. Improve report clarity and compactness.
5. Prepare CI-style gate command.
6. Keep all execution paper-only.

## Suggested Milestones

| Milestone | Scope | Output |
|---|---|---|
| 9A | Data provider abstraction | Local fixture provider and interface |
| 9B | Journal noise control | Test journal isolation or capped test journal |
| 9C | Report cleanup | Cleaner compact report output |
| 9D | CI gate | Single command for all safe gates |
| 9E | Documentation hardening | Operator guide and safety guide |
