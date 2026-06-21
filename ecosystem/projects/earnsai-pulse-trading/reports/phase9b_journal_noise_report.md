# EarnsAI Pulse — Phase 9B Journal Noise Control Report

## Summary
- OK: `True`
- Isolated journal path: `runtime/test_journals/phase9b_report_decisions.jsonl`
- Isolated rows generated: `5`

## Distribution
- Actions: `{'HOLD': 2, 'BUY': 2, 'SELL': 1}`
- Risk statuses: `{'REJECTED': 2, 'APPROVED_FOR_PAPER_ONLY': 3}`

## Safety
- Main journal is not required for this isolated check.
- Test journal is stored under `runtime/test_journals/`.
- Mode remains PAPER_ONLY.
- Live trading remains locked.
- No private exchange API is used.
