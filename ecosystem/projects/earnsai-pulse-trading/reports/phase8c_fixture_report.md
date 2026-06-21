# EarnsAI Pulse — Phase 8C Fixture Report

## Summary
- OK: `True`
- Total scenarios: `4`
- Passed: `4`
- Failed: `0`

## Scenario Results

| Scenario | Expected Trend | Observed Trend | Expected Candidate | Observed Candidate | Final Action | Risk Status | Passed |
|---|---|---|---|---|---|---|---|
| bullish | bullish | bullish | BUY | BUY | BUY | APPROVED_FOR_PAPER_ONLY | True |
| bearish | bearish | bearish | SELL | SELL | SELL | APPROVED_FOR_PAPER_ONLY | True |
| flat | flat | flat | HOLD | HOLD | HOLD | REJECTED | True |
| volatile | bullish | bullish | BUY | BUY | BUY | APPROVED_FOR_PAPER_ONLY | True |

## Safety
- All fixture runs remain paper-only.
- Live trading remains locked.
- Private exchange API is not used.
- This report is deterministic and intended for evaluation hardening.
