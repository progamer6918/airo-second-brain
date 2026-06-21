# EarnsAI Pulse Trading — Phase 8 Plan

## Status
Phase 7 MVP has been promoted to master and validated.

## Phase 8 Principle
Phase 8 must improve evaluation quality, stability, observability, and test discipline without enabling live trading.

## Not Allowed in Phase 8
- No live trading.
- No private exchange API.
- No real-money execution.
- No manual buy or sell command.
- No command that prints env files, tokens, API keys, private keys, or credentials.

## Main Goals
1. Improve signal evaluation.
2. Add metrics for decision quality.
3. Add deterministic test fixtures.
4. Add paper-only performance summary.
5. Add better journal analysis.
6. Add safer data ingestion abstraction.
7. Prepare optional backtesting integration.
8. Keep FreqTrade dry-run only.

## Suggested Phase 8 Milestones

| Milestone | Scope | Output |
|---|---|---|
| 8A | Evaluation metrics baseline | Signal count, HOLD ratio, approval ratio, latest signal safety |
| 8B | Journal analytics | Markdown and JSON report from JSONL |
| 8C | Deterministic data fixtures | Repeatable price scenarios |
| 8D | Backtest adapter planning | Interface only, no heavy integration yet |
| 8E | Telegram report commands | report, metrics, and health commands |
| 8F | Stability hardening | More tests and failure-mode checks |

## Recommended First Step
Start with Phase 8A Evaluation Metrics Baseline.
