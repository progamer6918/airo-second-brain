# EarnsAI Pulse — Phase 8B Journal Analytics

## Safety Snapshot
- Mode: `PAPER_ONLY`
- Live trading locked: `True`
- Safety OK: `True`
- Latest signal action: `BUY`
- Latest risk status: `APPROVED_FOR_PAPER_ONLY`

## Journal Overview
- Total rows: `500`
- Events: `{'multi_agent_decision': 464, 'decision': 36}`
- Phases: `{'7C': 464, '7C_COMPAT': 36}`
- Actions: `{'BUY': 250, 'HOLD': 143, 'SELL': 107}`
- Risk statuses: `{'APPROVED_FOR_PAPER_ONLY': 357, 'REJECTED': 143}`

## Rates
- Approved paper-only: `71.4%`
- Rejected: `28.6%`
- Blocked: `0.0%`
- HOLD: `28.6%`
- BUY: `50.0%`
- SELL: `21.4%`

## Confidence Buckets
`{'0.60-0.79': 357, '0.00-0.29': 36, '0.30-0.59': 107}`

## Latest Journal Rows

| Phase | Event | Action | Risk Status | Confidence |
|---|---|---|---|---|
| 7C | multi_agent_decision | HOLD | REJECTED | 0.48 |
| 7C | multi_agent_decision | BUY | APPROVED_FOR_PAPER_ONLY | 0.7447499999999998 |
| 7C | multi_agent_decision | BUY | APPROVED_FOR_PAPER_ONLY | 0.7447499999999998 |
| 7C | multi_agent_decision | SELL | APPROVED_FOR_PAPER_ONLY | 0.7237499999999999 |
| 7C | multi_agent_decision | HOLD | REJECTED | 0.48 |
| 7C | multi_agent_decision | BUY | APPROVED_FOR_PAPER_ONLY | 0.7447499999999998 |
| 7C | multi_agent_decision | BUY | APPROVED_FOR_PAPER_ONLY | 0.7447499999999998 |
| 7C | multi_agent_decision | SELL | APPROVED_FOR_PAPER_ONLY | 0.7237499999999999 |
| 7C | multi_agent_decision | HOLD | REJECTED | 0.48 |
| 7C | multi_agent_decision | BUY | APPROVED_FOR_PAPER_ONLY | 0.7447499999999998 |

## Notes
- This report is for paper/dry-run evaluation only.
- It does not imply live trading readiness.
- Private exchange API remains disabled.
