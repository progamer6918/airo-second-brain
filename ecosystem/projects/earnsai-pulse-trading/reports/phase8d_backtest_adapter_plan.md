# EarnsAI Pulse — Phase 8D Backtest Adapter Plan

## Status
- OK: `True`
- Plan valid: `True`
- Mode: `PAPER_ONLY`
- Live trading locked: `True`
- Private exchange API used: `False`
- Execution enabled: `False`

## Purpose
Define a safe interface for future backtest integration without enabling live trading.

## Scope
- Input source: `Deterministic fixtures and JSONL journal outputs.`
- Output target: `Local reports only.`
- This phase defines the adapter interface only.
- This phase does not run live trading.
- This phase does not use private exchange API.

## Fixture Readiness
- Total scenarios: `4`
- Passed: `4`
- Failed: `0`

| Scenario | Observed Trend | Candidate Action | Final Action | Risk Status | Confidence | Passed |
|---|---|---|---|---|---|---|
| bullish | bullish | BUY | BUY | APPROVED_FOR_PAPER_ONLY | 0.7447499999999998 | True |
| bearish | bearish | SELL | SELL | APPROVED_FOR_PAPER_ONLY | 0.7237499999999999 | True |
| flat | flat | HOLD | HOLD | REJECTED | 0.48 | True |
| volatile | bullish | BUY | BUY | APPROVED_FOR_PAPER_ONLY | 0.7447499999999998 | True |

## Planned Adapter Steps
- Read deterministic fixture scenarios.
- Run existing multi-agent cycle per fixture.
- Collect final action, risk status, and confidence.
- Summarize backtest-readiness without executing orders.
- Write JSON and Markdown planning reports.

## Safety Notes
- No live trading.
- No private exchange API.
- No real-money execution.
- No automatic FreqTrade process start.
- Adapter remains interface/planning only in Phase 8D.
